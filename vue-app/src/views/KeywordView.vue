<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { loadPoems } from '../composables/usePoems'

document.title = 'Keyword Analysis'

const route = useRoute()
const router = useRouter()
const allPoems = ref([])

const keyword = computed(() => route.query.keyword || '')
const page = computed(() => Number(route.query.page) || 1)
const pageSize = 20

const results = computed(() =>
  allPoems.value.filter((poem) => poem.paragraphs.join('').includes(keyword.value)),
)
const totalCount = computed(() => results.value.length)
const totalPages = computed(() => Math.ceil(totalCount.value / pageSize) || 1)
const pageResults = computed(() => {
  const start = (page.value - 1) * pageSize
  return results.value.slice(start, start + pageSize)
})

// ===== 等价于 main.py /keyword_poet_rank 的 Counter 逻辑 =====
const poetRankData = computed(() => {
  const counter = new Map()
  for (const poem of allPoems.value) {
    const text = (poem.paragraphs || []).join('')
    if (keyword.value && text.includes(keyword.value)) {
      const poet = poem.author
      if (poet && poet !== '无名氏') {
        counter.set(poet, (counter.get(poet) || 0) + 1)
      }
    }
  }
  return [...counter.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([name, value]) => ({ name, value }))
})

function ensureEchartsLoaded() {
  return new Promise((resolve) => {
    if (window.echarts) {
      resolve()
      return
    }
    const script = document.createElement('script')
    script.src = 'https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js'
    script.onload = () => resolve()
    document.head.appendChild(script)
  })
}

let chart = null

async function renderChart() {
  await ensureEchartsLoaded()
  await nextTick()

  const dom = document.getElementById('poetPie')
  if (!dom) return

  if (!chart) {
    chart = window.echarts.init(dom)
  }

  const option = {
    color: [
      '#5a0f0f',
      '#6b1414',
      '#7a1f1f',
      '#8b3a2b',
      '#a45a2a',
      '#b8860b',
      '#c9971a',
      '#d4aa2a',
      '#e6c24f',
      '#f5d76e',
    ],
    tooltip: { trigger: 'item' },
    legend: { orient: 'vertical', left: 'left' },
    series: [
      {
        type: 'pie',
        radius: '70%',
        data: poetRankData.value,
        label: {
          fontSize: 16,
          fontFamily: 'FontChinese',
          formatter: '{b}: {d}%',
        },
        itemStyle: { borderRadius: 6 },
      },
    ],
  }

  chart.setOption(option)

  chart.off('click')
  chart.on('click', function (params) {
    const poet = params.name
    router.push({ path: '/search', query: { keyword: keyword.value, poet } })
  })
}

onMounted(async () => {
  allPoems.value = await loadPoems()
  await renderChart()
})

watch(poetRankData, async () => {
  await renderChart()
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
    <div class="poet-header">
      <h1><span lang="en">Poems Containing</span> "{{ keyword }}"</h1>

      <p style="font-size: 18px">
        <span lang="en"><strong>{{ totalCount }}</strong> poems found</span>
      </p>
    </div>

    <!-- 诗人比例饼图 -->
    <h2 class="section-title">
      <span lang="en">Top Poets Using the Word</span> "{{ keyword }}"
    </h2>

    <div class="chart-container">
      <div id="poetPie"></div>
    </div>

    <h2 class="section-title">
      <span lang="en">Poem List</span>
    </h2>

    <div class="poem-grid">
      <div class="poem-card" v-for="poem in pageResults" :key="poem.id">
        <h3>{{ poem.title }} —— {{ poem.author }}</h3>

        <p v-for="(line, idx) in poem.paragraphs.slice(0, 2)" :key="idx">{{ line }}</p>

        <router-link class="detail-link" :to="`/poem/${poem.id}`">
          <span lang="en">View Details</span>
        </router-link>
      </div>
    </div>

    <div class="pagination">
      <router-link v-if="page > 1" :to="{ path: '/keyword', query: { keyword, page: page - 1 } }">
        <span lang="en">Prev</span>
      </router-link>

      <span lang="en">Page {{ page }} of {{ totalPages }}</span>

      <router-link
        v-if="page < totalPages"
        :to="{ path: '/keyword', query: { keyword, page: page + 1 } }"
      >
        <span lang="en">Next</span>
      </router-link>
    </div>

    <br />
    <a href="/home" class="home-btn"></a>
  </div>
</template>
