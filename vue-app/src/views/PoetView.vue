<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { loadPoems, loadAuthors, loadPoetWordfreq } from '../composables/usePoems'

const route = useRoute()
const router = useRouter()

const poets = ref([])
const allPoems = ref([])

const name = computed(() => route.query.name || '')
const page = computed(() => Number(route.query.page) || 1)

const poetInfo = computed(() => poets.value.find((p) => p.name === name.value) || null)
const poetPoems = computed(() => allPoems.value.filter((poem) => poem.author === name.value))

const pageSize = 20
const totalPages = computed(() => Math.ceil(poetPoems.value.length / pageSize) || 1)
const pagePoems = computed(() => {
  const start = (page.value - 1) * pageSize
  return poetPoems.value.slice(start, start + pageSize)
})

function ensureEchartsLoaded() {
  return new Promise((resolve) => {
    if (window.echarts && window.echarts.getInstanceByDom) {
      // echarts-wordcloud 注册到 echarts 上，需要确认两者都已加载
      if (document.querySelector('script[data-echarts-wordcloud]')) {
        resolve()
        return
      }
    }
    const base = document.createElement('script')
    base.src = 'https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js'
    base.onload = () => {
      const wc = document.createElement('script')
      wc.src = 'https://cdn.jsdelivr.net/npm/echarts-wordcloud/dist/echarts-wordcloud.min.js'
      wc.dataset.echartsWordcloud = 'true'
      wc.onload = () => resolve()
      document.head.appendChild(wc)
    }
    document.head.appendChild(base)
  })
}

async function renderWordCloud() {
  if (!poetInfo.value) return

  await ensureEchartsLoaded()
  await nextTick()

  const dom = document.getElementById('poetCloud')
  if (!dom) return

  const chart = window.echarts.init(dom)

  const wordfreqByPoet = await loadPoetWordfreq()
  const data = wordfreqByPoet[poetInfo.value.name] || []

  const option = {
    series: [
      {
        type: 'wordCloud',
        rotationRange: [0, 0], // 横向
        sizeRange: [15, 60],
        textStyle: {
          fontFamily: 'FontChinese',
          color: function () {
            return (
              'rgb(' +
              Math.round(Math.random() * 200) +
              ',' +
              Math.round(Math.random() * 200) +
              ',' +
              Math.round(Math.random() * 200) +
              ')'
            )
          },
        },
        data,
      },
    ],
  }

  chart.setOption(option)

  chart.on('click', function (params) {
    router.push({ path: '/search', query: { keyword: params.name, poet: poetInfo.value.name } })
  })
}

onMounted(async () => {
  const [poemsData, authorsData] = await Promise.all([loadPoems(), loadAuthors()])
  allPoems.value = poemsData
  poets.value = authorsData
  await renderWordCloud()
})

watch(name, async () => {
  await renderWordCloud()
})

watch(
  poetInfo,
  (p) => {
    document.title = p ? p.name : 'Poet Not Found'
  },
  { immediate: true },
)
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

    <template v-if="poetInfo">
      <div class="poet-header">
        <h1>{{ poetInfo.name }}</h1>
        <p>{{ poetInfo.desc }}</p>
        <h2>{{ poetInfo.name }} <span lang="en">Word Cloud</span></h2>
      </div>

      <div id="poetCloud" style="height: 500px"></div>

      <h2 class="section-title">
        <span lang="en">Poem list</span>
      </h2>

      <div class="poem-grid">
        <div class="poem-card" v-for="poem in pagePoems" :key="poem.id">
          <h3>{{ poem.title }}</h3>

          <!-- 只显示前两句 -->
          <p v-for="(line, idx) in poem.paragraphs.slice(0, 2)" :key="idx">{{ line }}</p>

          <router-link class="detail-link" :to="`/poem/${poem.id}`">
            <span lang="en">View Details</span>
          </router-link>
        </div>
      </div>

      <div class="pagination">
        <router-link v-if="page > 1" :to="{ path: '/poet', query: { name, page: page - 1 } }">
          <span lang="en">Prev</span>
        </router-link>

        <span lang="en">Page {{ page }} of {{ totalPages }}</span>

        <router-link
          v-if="page < totalPages"
          :to="{ path: '/poet', query: { name, page: page + 1 } }"
        >
          <span lang="en">Next</span>
        </router-link>
      </div>
    </template>

    <template v-else>
      <h2>
        <span lang="en">Poet Not Found</span>
      </h2>
    </template>

    <br />
    <a href="/home" class="home-btn"></a>
  </div>
</template>

<style>
/* 定义fontC字体 */
@font-face {
  font-family: 'FontC';
  src: url('/static/fontC.ttf') format('truetype');
  font-display: swap;
}
</style>
