import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'cover', component: () => import('../views/CoverView.vue') },
  { path: '/home', name: 'home', component: () => import('../views/HomeView.vue') },
  { path: '/poet', name: 'poet', component: () => import('../views/PoetView.vue') },
  { path: '/search', name: 'search', component: () => import('../views/SearchView.vue') },
  { path: '/poem/:id', name: 'poem', component: () => import('../views/PoemDetailView.vue') },
  { path: '/wordcloud', name: 'wordcloud', component: () => import('../views/WordCloudView.vue') },
  { path: '/ranking', name: 'ranking', component: () => import('../views/RankingView.vue') },
  { path: '/keyword', name: 'keyword', component: () => import('../views/KeywordView.vue') },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
