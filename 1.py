import json
import glob
import jieba
from collections import Counter

all_text = ""

# 读取所有 poet.tang.*.json 文件
files = glob.glob("poet.tang.*.json")

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        poems = json.load(f)

        for poem in poems:
            all_text += "".join(poem["paragraphs"])

# 分词
words = jieba.lcut(all_text)

exclude_words = {"全唐诗", "京本作"}

words = [
    w for w in words
    if len(w) > 1 and w not in exclude_words
]

freq = Counter(words)

top_words = freq.most_common(200)

for w, c in top_words:
    print(w)