from openai import OpenAI
import os
client = OpenAI(
    api_key="sk-c66e57cd09e8406c9bbae8092c61ad16",
    base_url="https://api.deepseek.com"
)
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import json
import os
import jieba
from collections import Counter
from fastapi.staticfiles import StaticFiles
import pandas as pd
import random

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# ===== 读取诗歌 =====
poems = []
for file in os.listdir():
    if file.startswith("poet.tang") and file.endswith(".json"):
        with open(file, "r", encoding="utf-8") as f:
            poems.extend(json.load(f))

for i, poem in enumerate(poems):
    poem["id"] = i

# ===== 读取诗人 =====
with open("authors.tang.json", "r", encoding="utf-8") as f:
    poets = json.load(f)


# ===== 修改首页路由，指向封面 =====
@app.get("/", response_class=HTMLResponse)
def cover(request: Request):
    return templates.TemplateResponse("cover.html", {"request": request})

# ===== 新增一个路由指向原来的首页（搜索页面）=====
@app.get("/home", response_class=HTMLResponse)
def home(request: Request):

    df = pd.read_csv("data/palace_news.csv")

    news_list = df.to_dict(orient="records")

    random_news = random.sample(news_list, 5)

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "palace_news": random_news
        }
    )


# ===== 诗人页面 =====
@app.get("/poet", response_class=HTMLResponse)
def poet_page(request: Request, name: str, page: int = 1):

    poet_info = next((p for p in poets if p["name"] == name), None)
    poet_poems = [poem for poem in poems if poem["author"] == name]

    # ===== 分页逻辑 =====
    page_size = 20
    start = (page - 1) * page_size
    end = start + page_size

    total_pages = (len(poet_poems) + page_size - 1) // page_size
    page_poems = poet_poems[start:end]

    return templates.TemplateResponse("poet.html", {
        "request": request,
        "poet": poet_info,
        "poems": page_poems,
        "page": page,
        "total_pages": total_pages,
        "name": name
    })

# ===== 标题关键词搜索 =====
@app.get("/search", response_class=HTMLResponse)
def search_page(request: Request, keyword: str, poet: str = None, page: int = 1):

    results = []

    for poem in poems:

        if poet and poem["author"] != poet:
            continue

        if keyword in poem["title"] or \
           any(keyword in line for line in poem["paragraphs"]):

            results.append(poem)

    total_count = len(results)

    page_size = 20
    start = (page - 1) * page_size
    end = start + page_size

    page_results = results[start:end]
    total_pages = (total_count + page_size - 1) // page_size

    return templates.TemplateResponse("search.html", {
        "request": request,
        "results": page_results,
        "keyword": keyword,
        "total_count": total_count,
        "page": page,
        "total_pages": total_pages
    })

# ===== 诗歌id =====
@app.get("/poem/{poem_id}", response_class=HTMLResponse)
def poem_detail(request: Request, poem_id: int):

    poem = poems[poem_id]

    return templates.TemplateResponse("poem_detail.html", {
        "request": request,
        "poem": poem,
        "poem_id": poem_id
    })

# ===== Deepseek解释 =====
@app.get("/ai_explain/{poem_id}")
def ai_explain(poem_id: int, lang: str = "english"):

    # 1️⃣ 找到对应诗歌
    poem = next((p for p in poems if p["id"] == poem_id), None)

    if not poem:
        return JSONResponse({"result": "Poem not found."})

    poem_text = "\n".join(poem["paragraphs"])
    title = poem["title"]
    author = poem["author"]

    # 2️⃣ 根据语言生成 prompt
    if lang == "english":
        instruction = "Please explain this Tang dynasty poem in clear English. Include Translation, cultural background and literary analysis."

    elif lang == "chinese":
        instruction = "请用学术性中文详细解析这首唐诗，包括创作背景、意象分析和情感表达。"

    elif lang == "japanese":
        instruction = "この唐詩を正確な日本語に翻訳し、その創作背景、重要な意象、そして感情表現について解説してください。"

    elif lang == "french":
        instruction = "Veuillez traduire ce poème des Tang avec précision en français, et expliquer le contexte de sa création, ses images importantes ainsi que l'expression des émotions."

    elif lang == "spanish":
        instruction = "Por favor, traduce este poema de la dinastía Tang con precisión al español y explica el contexto de su creación, las imágenes importantes y la expresión de las emociones."

    elif lang == "german":
        instruction = "Bitte übersetzen Sie dieses Gedicht aus der Tang-Dynastie präzise ins Deutsche und erläutern Sie den historischen Hintergrund, die wichtigsten Bilder sowie den Ausdruck von Emotionen."

    elif lang == "russian":
        instruction = "Пожалуйста, точно переведите это стихотворение эпохи Тан на русский язык и объясните контекст его создания, важные образы и выражение эмоций."

    else:
        instruction = "Please explain this Tang dynasty poem in English."

    prompt = f"""
Title: {title}
Author: {author}

Poem:
{poem_text}

{instruction}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return {"result": response.choices[0].message.content}


# 读取翻译 CSV
df = pd.read_csv("data/word_translation.csv")
translation_dict = dict(zip(df["word"], df["translation"]))
# ===== 词云 =====
@app.get("/wordfreq")
def get_wordfreq():

    all_text = ""

    for poem in poems:
        all_text += "".join(poem["paragraphs"])

    words = jieba.lcut(all_text)

    exclude_words = {"全唐诗", "京本作", "一作"}  # 用集合查询效率更高
    
    # 2. 去掉单字词 + 过滤指定排除词
    words = [
        w for w in words 
        if len(w) > 1 and w not in exclude_words  # 新增排除条件
    ]

    freq = Counter(words)

    # 取前100高频词
    top_words = freq.most_common(100)

    # ✅ 打印到终端
    print("\n===== Top 100 Word Frequency =====")
    for i, (word, count) in enumerate(top_words, 1):
        print(count)

    result = []

    for word, count in top_words:
        result.append({
            "name": word,
            "value": count,
            "translation": translation_dict.get(word, "")
        })

    return result


@app.get("/wordcloud", response_class=HTMLResponse)
def wordcloud_page(request: Request):
    return templates.TemplateResponse("wordcloud.html", {"request": request})

@app.get("/poet_wordfreq/{name}")
def get_poet_wordfreq(name: str):

    all_text = ""

    # 只拼接该诗人的诗
    for poem in poems:
        if poem["author"] == name:
            all_text += "".join(poem["paragraphs"])

    # 分词
    words = jieba.lcut(all_text)

    # 去掉单字
    words = [w for w in words if len(w) > 1]

    # 可选：去停用词
    stopwords = set(["之", "其", "而", "不", "也", "于", "兮", "乎", "者", "矣"])
    words = [w for w in words if w not in stopwords]

    freq = Counter(words)

    top_words = freq.most_common(100)

    return JSONResponse(
        content=[{"name": w, "value": c} for w, c in top_words]
    )

#数量统计页面路由
@app.get("/ranking", response_class=HTMLResponse)
def ranking(request: Request):
    return templates.TemplateResponse("ranking.html", {"request": request})

#诗歌数量统计
@app.get("/poet_rank")
def poet_rank():

    counter = Counter()

    exclude_poets = {"无名氏", "不详"}
    
    for poem in poems:
        poet = poem["author"]

        if poet in exclude_poets:
            continue

        counter[poet] += 1

    # 取前20
    top20 = counter.most_common(20)

    return [{"name": p, "value": c} for p, c in top20]

@app.get("/keyword")
def keyword_page(request: Request, keyword: str, page: int = 1):

    page_size = 20

    # 找到包含关键词的诗
    results = []
    for poem in poems:
        text = "".join(poem["paragraphs"])
        if keyword in text:
            results.append(poem)

    total_count = len(results)

    total_pages = (total_count + page_size - 1) // page_size

    start = (page - 1) * page_size
    end = start + page_size

    page_results = results[start:end]

    return templates.TemplateResponse(
        "keyword.html",
        {
            "request": request,
            "keyword": keyword,
            "results": page_results,
            "total_count": total_count,
            "page": page,
            "total_pages": total_pages
        }
    )

@app.get("/keyword_poet_rank")
def keyword_poet_rank(keyword: str):

    counter = Counter()

    for poem in poems:

        text = "".join(poem.get("paragraphs", []))

        if keyword and keyword in text:

            poet = poem.get("author")

            if poet and poet != "无名氏":
                counter[poet] += 1

    top10 = counter.most_common(10)

    return [{"name": k, "value": v} for k, v in top10]

