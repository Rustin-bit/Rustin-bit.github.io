// 原每个模板里都重复粘贴了同一段"点击水波纹"脚本，这里合并成一处，
// 行为与原版逐字一致（60px 波纹，600ms 后移除）。
export function installRippleEffect() {
  document.addEventListener('click', function (e) {
    const ripple = document.createElement('span')
    ripple.classList.add('ripple')

    const size = 60

    ripple.style.width = size + 'px'
    ripple.style.height = size + 'px'

    ripple.style.left = e.clientX - size / 2 + 'px'
    ripple.style.top = e.clientY - size / 2 + 'px'

    document.body.appendChild(ripple)

    setTimeout(() => {
      ripple.remove()
    }, 600)
  })
}
