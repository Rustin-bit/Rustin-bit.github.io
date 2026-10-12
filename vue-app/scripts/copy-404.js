// GitHub Pages 没有 Netlify 式的 SPA 通配重定向（_redirects），
// 标准解法是把 404.html 变成 index.html 的副本：GitHub Pages 对任何
// 不存在的路径（比如 /poem/123）都会回退渲染 404.html，但浏览器地址栏
// 仍保持原路径不变，于是 Vue Router 的 history 模式能照常读取到正确路径。
import { copyFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const __dirname = dirname(fileURLToPath(import.meta.url))
const distDir = join(__dirname, '..', 'dist')

copyFileSync(join(distDir, 'index.html'), join(distDir, '404.html'))
console.log('copied dist/index.html -> dist/404.html')
