"""
一次性离线脚本：把 main.py 里依赖 Python 运行时的数据处理
（jieba 分词、Counter 统计、CSV 读取）预先跑一遍，产出纯静态 JSON，
供 Vue 前端直接 fetch 使用，运行期不再需要任何后端。

用法：
    cd 全唐诗en
    python scripts/prepare_static_data.py

语料是固定历史数据集，基本不会变；只有新增/修改诗歌数据时才需要重新运行。
"""

import json
import os
from collections import Counter

import jieba
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "vue-app", "public", "data")

os.makedirs(OUT_DIR, exist_ok=True)


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False)
    try:
        print(f"wrote {os.path.relpath(path, ROOT)} ({os.path.getsize(path)} bytes)")
    except UnicodeEncodeError:
        pass


# ===== 读取诗歌（与 main.py 完全一致的加载顺序，保证 id 不变） =====
poems = []
for file in sorted(os.listdir(ROOT)):
    if file.startswith("poet.tang") and file.endswith(".json"):
        with open(os.path.join(ROOT, file), "r", encoding="utf-8") as f:
            poems.extend(json.load(f))

for i, poem in enumerate(poems):
    poem["id"] = i

write_json(os.path.join(OUT_DIR, "poems.json"), poems)

# ===== 读取诗人 =====
with open(os.path.join(ROOT, "authors.tang.json"), "r", encoding="utf-8") as f:
    poets = json.load(f)

write_json(os.path.join(OUT_DIR, "authors.json"), poets)

# ===== palace_news.csv -> palace_news.json =====
df_news = pd.read_csv(os.path.join(ROOT, "data", "palace_news.csv"))
write_json(os.path.join(OUT_DIR, "palace_news.json"), df_news.to_dict(orient="records"))

# ===== word_translation.csv -> translation_dict =====
df_trans = pd.read_csv(os.path.join(ROOT, "data", "word_translation.csv"))
translation_dict = dict(zip(df_trans["word"], df_trans["translation"]))

# ===== /wordfreq 逻辑（全站词频） =====
all_text = ""
for poem in poems:
    all_text += "".join(poem["paragraphs"])

words = jieba.lcut(all_text)

exclude_words = {"全唐诗", "京本作", "一作"}
words = [w for w in words if len(w) > 1 and w not in exclude_words]

freq = Counter(words)
top_words = freq.most_common(100)

wordfreq_result = [
    {"name": word, "value": count, "translation": translation_dict.get(word, "")}
    for word, count in top_words
]
write_json(os.path.join(OUT_DIR, "wordfreq.json"), wordfreq_result)

# ===== /poet_rank 逻辑 =====
counter = Counter()
exclude_poets = {"无名氏", "不详"}
for poem in poems:
    poet = poem["author"]
    if poet in exclude_poets:
        continue
    counter[poet] += 1

poet_rank_result = [{"name": p, "value": c} for p, c in counter.most_common(20)]
write_json(os.path.join(OUT_DIR, "poet_rank.json"), poet_rank_result)

# ===== /poet_wordfreq/{name} 逻辑：为语料中出现的每个诗人预生成一份，
# 合并进单个 JSON（key 为诗人名），避免个别诗人名含有制表符等
# 非法文件名字符时导致单独文件写入失败 =====
poet_stopwords = {"之", "其", "而", "不", "也", "于", "兮", "乎", "者", "矣"}

poems_by_author = {}
for poem in poems:
    poems_by_author.setdefault(poem["author"], []).append(poem)

poet_wordfreq_result = {}
for name, author_poems in poems_by_author.items():
    all_text = "".join("".join(p["paragraphs"]) for p in author_poems)

    words = jieba.lcut(all_text)
    words = [w for w in words if len(w) > 1]
    words = [w for w in words if w not in poet_stopwords]

    freq = Counter(words)
    top_words = freq.most_common(100)

    poet_wordfreq_result[name] = [{"name": w, "value": c} for w, c in top_words]

write_json(os.path.join(OUT_DIR, "poet_wordfreq.json"), poet_wordfreq_result)
print(f"wrote poet_wordfreq.json for {len(poet_wordfreq_result)} poets")
print("done.")
