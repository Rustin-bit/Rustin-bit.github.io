<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { loadPoems } from '../composables/usePoems'

const route = useRoute()
const poem = ref(null)
const poemId = ref(Number(route.params.id))

const language = ref('english')
const loadingText = ref('')
const resultHtml = ref('')
const fadeIn = ref(false)

function ensureMarkedLoaded() {
  return new Promise((resolve) => {
    if (window.marked) {
      resolve()
      return
    }
    const script = document.createElement('script')
    script.src = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js'
    script.onload = () => resolve()
    document.head.appendChild(script)
  })
}

// ===== 与 main.py /ai_explain 完全一致的多语言 prompt 构造 =====
const INSTRUCTIONS = {
  english:
    'Please explain this Tang dynasty poem in clear English. Include Translation, cultural background and literary analysis.',
  chinese: '请用学术性中文详细解析这首唐诗，包括创作背景、意象分析和情感表达。',
  japanese:
    'この唐詩を正確な日本語に翻訳し、その創作背景、重要な意象、そして感情表現について解説してください。',
  french:
    'Veuillez traduire ce poème des Tang avec précision en français, et expliquer le contexte de sa création, ses images importantes ainsi que l\'expression des émotions.',
  spanish:
    'Por favor, traduce este poema de la dinastía Tang con precisión al español y explica el contexto de su creación, las imágenes importantes y la expresión de las emociones.',
  german:
    'Bitte übersetzen Sie dieses Gedicht aus der Tang-Dynastie präzise ins Deutsche und erläutern Sie den historischen Hintergrund, die wichtigsten Bilder sowie den Ausdruck von Emotionen.',
  russian:
    'Пожалуйста, точно переведите это стихотворение эпохи Тан на русский язык и объясните контекст его создания, важные образы и выражение эмоций.',
}

const DEEPSEEK_API_KEY = 'sk-c66e57cd09e8406c9bbae8092c61ad16'

async function generateAI() {
  loadingText.value = 'Generating analysis, please wait...'
  resultHtml.value = ''
  fadeIn.value = false

  const instruction = INSTRUCTIONS[language.value] || 'Please explain this Tang dynasty poem in English.'
  const poemText = poem.value.paragraphs.join('\n')

  const prompt = `
Title: ${poem.value.title}
Author: ${poem.value.author}

Poem:
${poemText}

${instruction}
`

  try {
    const [, res] = await Promise.all([
      ensureMarkedLoaded(),
      fetch('https://api.deepseek.com/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${DEEPSEEK_API_KEY}`,
        },
        body: JSON.stringify({
          model: 'deepseek-chat',
          messages: [{ role: 'user', content: prompt }],
          temperature: 0.7,
        }),
      }),
    ])

    const data = await res.json()
    loadingText.value = ''
    resultHtml.value = window.marked.parse(data.choices[0].message.content)
    fadeIn.value = true
  } catch (error) {
    loadingText.value = 'Error loading analysis.'
    console.error(error)
  }
}

onMounted(async () => {
  const poems = await loadPoems()
  poem.value = poems[poemId.value]
  if (poem.value) {
    document.title = poem.value.title
  }
})
</script>

<template>
  <div v-if="poem" class="detail-container">
    <a
      href="https://adp.cloud.tencent.com/adp/?spaceId=default_space#/app/knowledge/app-config?appid=2031381381141682368&appType=knowledge_qa&spaceId=default_space"
      class="agent-container"
      target="_blank"
    >
      <div class="agent-circle"></div>
      <img src="/static/Yee.svg" class="agent-img" />
      <div class="agent-bubble">💡 Ask Yee about Tang Poetry</div>
    </a>

    <!-- 左侧：诗歌原文 -->
    <div class="poem-section">
      <h1 class="poem-title">{{ poem.title }}</h1>
      <h3 class="poem-author">{{ poem.author }}</h3>

      <div class="poem-content">
        <p v-for="(line, idx) in poem.paragraphs" :key="idx">{{ line }}</p>
      </div>

      <a href="/home" class="home-btn"></a>
    </div>

    <!-- 右侧：AI解诗板块 -->
    <div class="ai-section">
      <h2 class="ai-title">
        <span lang="en">AI Poetry Analysis</span>
      </h2>

      <!-- 语言选择 -->
      <div class="ai-controls">
        <label>
          <span lang="en">Language:</span>
        </label>
        <select id="language" v-model="language">
          <option value="english">English</option>
          <option value="chinese">中文</option>
          <option value="japanese">日本語</option>
          <option value="french">Français</option>
          <option value="spanish">Español</option>
          <option value="german">Deutsch</option>
          <option value="russian">Русский</option>
        </select>

        <button @click="generateAI" class="ai-btn">
          <span lang="en">Generate</span>
        </button>
      </div>

      <!-- 加载提示 -->
      <div class="loading-text">{{ loadingText }}</div>

      <!-- 结果区域 -->
      <div class="ai-result" :class="{ 'fade-in': fadeIn }" v-html="resultHtml"></div>
    </div>
  </div>
</template>

<style scoped>
:global(html),
:global(body) {
  height: 100%;
  margin: 0;
  overflow: hidden; /* 页面不滚动 */
}
.detail-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 50px;

  padding: 60px 8%;
  box-sizing: border-box;

  height: 100vh; /* 占满屏幕 */
}
.poem-section {
  background: rgba(255, 255, 255, 0.9);

  height: 100%;
  overflow-y: auto; /* 出现独立滚动条 */

  padding: 40px;
  border-radius: 12px;

  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
}
.ai-section {
  background: rgba(255, 255, 255, 0.95);

  height: 100%;
  overflow-y: auto; /* 第二个滚动条 */

  padding: 40px;
  border-radius: 12px;

  border: 2px solid #d8d2c2;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
}
</style>
