<script setup>
import { useRouter } from 'vue-router'
import { useBodyScrollLock } from '../composables/useBodyScrollLock'

useBodyScrollLock()

const router = useRouter()

function handleStart(e) {
  e.preventDefault()
  document.querySelector('.cover').classList.add('fade-out')
  setTimeout(function () {
    router.push('/home')
  }, 600)
}
</script>

<template>
  <div class="cover">
    <div class="button-wrapper">
      <a href="/home" class="start-btn" id="startBtn" @click="handleStart">START</a>
    </div>
  </div>
</template>

<style scoped>
/* 基础重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:global(body),
:global(html) {
  width: 100%;
  height: 100%;
  font-family: 'Segoe UI', '微软雅黑', sans-serif;
}

/* 封面容器 - 使用背景图片方式 */
.cover {
  width: 100%;
  height: 100%;
  position: relative;
  background-image: url('/static/cover.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  transition: opacity 2s ease, transform 2s ease;
}

/* 淡出动画 */
.cover.fade-out {
  opacity: 0;
  transform: scale(1.05);
}

/* 半透明遮罩 */
.cover::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.2); /* 微弱的暗色遮罩，让按钮更明显 */
  z-index: 1;
}

/* 按钮容器 - 绝对定位到下方 */
.button-wrapper {
  position: absolute;
  bottom: 8%; /* 距离底部12%，可以调整这个值来控制上下位置 */
  left: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  z-index: 2;
}

/* START 按钮样式 */
.start-btn {
  display: inline-block;
  padding: 10px 15px; /* 调整内边距控制按钮大小 */
  background-color: rgb(249, 238, 205);
  color: #3a2c1b;
  font-size: 1.1rem; /* 字体大小 */
  font-weight: bold;
  letter-spacing: 4px;
  text-transform: uppercase;
  text-decoration: none;
  border-radius: 50px;
  border: 2px solid #d8d2c2;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  cursor: pointer;
}

/* 悬停效果 */
.start-btn:hover {
  background-color: #c9a227;
  color: white;
  border-color: #b58c1f;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(201, 162, 39, 0.4);
}

/* 点击效果 */
.start-btn:active {
  transform: translateY(0px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}
</style>
