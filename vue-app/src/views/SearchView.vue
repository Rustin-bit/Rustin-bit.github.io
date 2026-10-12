<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { loadPoems } from '../composables/usePoems'

const route = useRoute()
const allPoems = ref([])

document.title = '搜索结果'

const keyword = computed(() => route.query.keyword || '')
const poetFilter = computed(() => route.query.poet || null)
const page = computed(() => Number(route.query.page) || 1)

const results = computed(() => {
  return allPoems.value.filter((poem) => {
    if (poetFilter.value && poem.author !== poetFilter.value) return false
    if (poem.title.includes(keyword.value)) return true
    return poem.paragraphs.some((line) => line.includes(keyword.value))
  })
})

const totalCount = computed(() => results.value.length)
const pageSize = 20
const totalPages = computed(() => Math.ceil(totalCount.value / pageSize) || 1)
const pageResults = computed(() => {
  const start = (page.value - 1) * pageSize
  return results.value.slice(start, start + pageSize)
})

onMounted(async () => {
  allPoems.value = await loadPoems()
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
      <router-link
        v-if="page > 1"
        :to="{ path: '/search', query: { keyword, poet: poetFilter, page: page - 1 } }"
      >
        <span lang="en">Prev</span>
      </router-link>

      <span lang="en">Page {{ page }} of {{ totalPages }}</span>

      <router-link
        v-if="page < totalPages"
        :to="{ path: '/search', query: { keyword, poet: poetFilter, page: page + 1 } }"
      >
        <span lang="en">Next</span>
      </router-link>
    </div>

    <br />
    <a href="/home" class="home-btn"></a>
  </div>
</template>
