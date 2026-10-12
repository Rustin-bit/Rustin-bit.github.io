<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBodyScrollLock } from '../composables/useBodyScrollLock'

document.title = 'Poet Ranking'

useBodyScrollLock()

const router = useRouter()

function ensureEchartsLoaded() {
  return new Promise((resolve) => {
    if (window.echarts) {
      resolve()
      return
    }
    const script = document.createElement('script')
    script.src = 'https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js'
    script.onload = () => resolve()
    document.head.appendChild(script)
  })
}

onMounted(async () => {
  await ensureEchartsLoaded()

  const res = await fetch(`${import.meta.env.BASE_URL}data/poet_rank.json`)
  const data = await res.json()

  const names = data.map((d) => d.name)
  const values = data.map((d) => d.value)

  const chart = window.echarts.init(document.getElementById('chart'))

  const option = {
    textStyle: {
      fontFamily: 'FontChinese',
    },

    xAxis: {
      type: 'value',
      axisLabel: {
        fontFamily: 'FontEnglish',
        color: '#3a2c1b',
        fontSize: 15,
      },
    },

    yAxis: {
      type: 'category',
      data: names,
      inverse: true, // 排名高的在上面
      axisLabel: {
        fontSize: 15,
        color: '#3a2c1b',
      },
    },

    series: [
      {
        type: 'bar',
        data: values,
        itemStyle: {
          color: function (params) {
            const i = params.dataIndex
            if (i == 0) return '#5a0f0f'
            if (i == 1) return '#8b3a2b'
            if (i == 2) return '#c9971a'
            return '#f5d76e'
          },
        },
        label: {
          show: true,
          position: 'right',
          fontFamily: 'FontEnglish',
        },
      },
    ],
  }

  chart.setOption(option)

  chart.on('click', function (params) {
    const poet = params.name
    router.push({ path: '/poet', query: { name: poet } })
  })
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

    <h1 class="section-title">
      <span lang="en"> Top 20 Tang Poets </span>
    </h1>

    <div id="chart" style="width: 1200px; height: 700px; margin: auto"></div>
  </div>
</template>
