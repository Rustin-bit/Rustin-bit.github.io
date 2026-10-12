import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

// 部署到 GitHub Pages 的项目页（https://用户名.github.io/仓库名/）时，
// 构建前设置环境变量 BASE_PATH=/仓库名/ 即可，默认根路径部署不用改。
const base = process.env.BASE_PATH || '/'

// https://vite.dev/config/
export default defineConfig({
  base,
  plugins: [vue()],
})
