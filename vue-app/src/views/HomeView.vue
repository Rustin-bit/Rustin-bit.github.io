<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBodyScrollLock } from '../composables/useBodyScrollLock'

useBodyScrollLock()

const router = useRouter()
const palaceNews = ref([])
const poetName = ref('')
const keywordInput = ref('')

function submitPoetSearch(e) {
  e.preventDefault()
  router.push({ path: '/poet', query: { name: poetName.value } })
}

function submitKeywordSearch(e) {
  e.preventDefault()
  router.push({ path: '/keyword', query: { keyword: keywordInput.value } })
}

// 等价于 Python random.sample(news_list, 5)：Fisher-Yates 洗牌后取前 N 个
function sampleRandom(arr, n) {
  const copy = arr.slice()
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[copy[i], copy[j]] = [copy[j], copy[i]]
  }
  return copy.slice(0, n)
}

onMounted(async () => {
  const res = await fetch(`${import.meta.env.BASE_URL}data/palace_news.json`)
  const newsList = await res.json()
  palaceNews.value = sampleRandom(newsList, 5)
})
</script>

<template>
  <div>
    <a
      href="https://adp.cloud.tencent.com/adp/?spaceId=default_space#/app/knowledge/app-config?appid=2031381381141682368&appType=knowledge_qa&spaceId=default_space"
      class="agent-container"
      target="_blank"
    >
      <div class="agent-circle"></div>
      <img src="/static/Yee.svg" class="agent-img" />
      <div class="agent-bubble">💡 Ask Yee about Tang Poetry</div>
    </a>

    <h1 class="main-title">
      <span lang="en"><i>Tang Poetry</i> AI Smart Platform</span>
    </h1>

    <div class="center-container">
      <div class="palace-news">
        <h2 class="section-title">
          <span lang="en">Palace News</span>
        </h2>

        <ul>
          <li v-for="(item, idx) in palaceNews" :key="idx">
            <a :href="item.link">{{ item.news }}</a>
          </li>
        </ul>
      </div>

      <!-- 按诗人搜索 -->
      <div class="search-section">
        <h2>
          <span lang="en">Search by Poet</span>
        </h2>
        <form action="/poet" method="get" @submit="submitPoetSearch">
          <input
            type="text"
            name="name"
            v-model="poetName"
            placeholder="Enter poet's name in Chinese"
          />
          <button type="submit">
            <span lang="en">Search</span>
          </button>
        </form>
      </div>

      <!-- 按关键字搜索 -->
      <div class="search-section">
        <h2>
          <span lang="en">Search by Keyword</span>
        </h2>
        <form action="/keyword" method="get" @submit="submitKeywordSearch">
          <input
            type="text"
            name="keyword"
            v-model="keywordInput"
            placeholder="Enter keyword in Chinese"
          />
          <button type="submit">
            <span lang="en">Search</span>
          </button>
        </form>
      </div>

      <!-- 词云按钮 -->
      <div class="cloud-button">
        <button @click="router.push('/wordcloud')">
          <span lang="en">
            <i>Tang Poetry</i> Word Cloud
          </span>
        </button>
        <!-- 数量按钮 -->
        <button @click="router.push('/ranking')">
          <span lang="en"> Poet Ranking by Poem Count </span>
        </button>
      </div>
    </div>
  </div>
</template>

