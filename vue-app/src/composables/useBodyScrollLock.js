import { onMounted, onUnmounted } from 'vue'

// 原站各页是独立 HTML 文档，body 的 overflow:hidden 只对当页生效；
// 迁移到 SPA 后每个路由的 CSS chunk 会常驻 <head>，若用 CSS 声明
// body{overflow:hidden} 会在离开该页后持续污染后续路由。这里改为
// 挂载时加锁、卸载时还原，复现原站“每页各自控制是否可滚动”的行为。
export function useBodyScrollLock() {
  let prevOverflow = ''

  onMounted(() => {
    prevOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
  })

  onUnmounted(() => {
    document.body.style.overflow = prevOverflow
  })
}
