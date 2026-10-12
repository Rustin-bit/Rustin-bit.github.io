<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

document.title = 'Tang Poetry Word Cloud'

const router = useRouter()

function ensureEchartsLoaded() {
  return new Promise((resolve) => {
    if (window.echarts && document.querySelector('script[data-echarts-wordcloud]')) {
      resolve()
      return
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

onMounted(async () => {
  await ensureEchartsLoaded()

  let currentPage = 1
  const pageSize = 10
  let globalData = []
  const chart = window.echarts.init(document.getElementById('main'))

  const res = await fetch(`${import.meta.env.BASE_URL}data/wordfreq.json`)
  const data = await res.json()

  data.forEach((item) => {
    item.color =
      'rgb(' +
      Math.round(Math.random() * 200) +
      ',' +
      Math.round(Math.random() * 200) +
      ',' +
      Math.round(Math.random() * 200) +
      ')'
  })

  const option = {
    series: [
      {
        type: 'wordCloud',
        shape: 'circle',
        gridSize: 6,
        sizeRange: [15, 70],
        rotationRange: [0, 0],
        textStyle: {
          fontFamily: 'FontChinese',
          color: function (params) {
            return params.data.color
          },
        },
        data,
      },
    ],
  }

  chart.setOption(option)
  createRanking(data)

  chart.on('click', function (params) {
    const word = params.name
    router.push({ path: '/keyword', query: { keyword: word } })
  })

  function createRanking(d) {
    globalData = d
    renderPage()
  }

  function renderPage() {
    const rank = document.getElementById('rankList')
    rank.innerHTML = ''

    const start = (currentPage - 1) * pageSize
    const end = start + pageSize
    const pageData = globalData.slice(start, end)

    pageData.forEach((item, i) => {
      const div = document.createElement('div')

      div.className = 'rank-item'
      div.dataset.word = item.name

      div.innerHTML = `
            <span class="rank-index">${start + i + 1}</span>

            <span class="rank-word" style="color:${item.color}">
            ${item.name}
            </span>

            <span class="rank-en">
            ${item.translation}
            </span>

            <span class="rank-count">
            ${item.value}
            </span>
            `

      rank.appendChild(div)
      div.addEventListener('mouseenter', function () {
        highlightWord(item.name)
      })
      div.addEventListener('mouseleave', function () {
        resetWordCloud()
      })
    })

    const totalPage = Math.ceil(globalData.length / pageSize)
    document.getElementById('pageInfo').innerText = currentPage + ' / ' + totalPage
  }

  window.nextPage = function () {
    const totalPage = Math.ceil(globalData.length / pageSize)
    if (currentPage < totalPage) {
      currentPage++
      renderPage()
    }
  }

  window.prevPage = function () {
    if (currentPage > 1) {
      currentPage--
      renderPage()
    }
  }

  function highlightWord(word) {
    chart.setOption({
      series: [
        {
          textStyle: {
            color: function (params) {
              if (params.name === word) {
                return '#5a0f0f' // 高亮
              }
              return 'rgba(120,120,120,0.25)' // 其他词淡化
            },
          },
          emphasis: {
            textStyle: {
              fontSize: 100, // 高亮词放大
            },
          },
        },
      ],
    })
  }

  function resetWordCloud() {
    chart.setOption({
      series: [
        {
          textStyle: {
            color: function (params) {
              return params.data.color
            },
          },
          emphasis: {
            textStyle: {
              fontSize: null,
            },
          },
        },
      ],
    })
  }
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
    <h1>
      <span lang="en"><i>Tang Poetry</i> Word Cloud</span>
    </h1>

    <div class="layout">
      <!-- 词云 -->
      <div id="main"></div>

      <!-- Ranking -->
      <div class="ranking">
        <h2 class="section-title">
          <span lang="en">Word Frequency Ranking</span>
        </h2>

        <div id="rankList"></div>

        <div class="pagination-rank">
          <button onclick="window.prevPage()"><span lang="en">Prev</span></button>

          <span id="pageInfo"></span>

          <button onclick="window.nextPage()"><span lang="en">Next</span></button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  width: 1200px;
  margin: auto;
  gap: 40px;
}

#main {
  width: 1500px;
  height: 500px;
  margin-left: -200px;
  margin-top: 80px;
}

.ranking {
  width: 50%;
  margin-right: 100px;
}

.rank-item {
  display: flex;
  align-items: center;
  padding: 6px 0;
  border-bottom: 1px solid #eee;
  font-size: 16px;
}

.rank-index {
  width: 40px;
  text-align: right;
  margin-right: 20px;
  font-family: FontEnglish;
}

.rank-word {
  width: 80px;
  font-family: FontChinese;
}

.rank-en {
  width: 120px;
  font-family: FontEnglish;
  color: #777;
}

.rank-count {
  width: 60px;
  text-align: right;
  font-family: FontEnglish;
}

.pagination-rank {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
}

.pagination-rank button {
  background: #c9a227; /* 金色 */
  color: white;
  border: none;
  padding: 6px 14px;
  border-radius: 6px;
  font-family: FontEnglish;
  cursor: pointer;
  transition: 0.2s;
}

.pagination-rank button:hover {
  background: #a8841c;
}

:global(body) {
  overflow: hidden;
}
</style>

<style>
@font-face {
  font-family: 'FontChinese';
  src: url('/static/fontC.ttf');
}
</style>
