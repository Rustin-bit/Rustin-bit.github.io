// 全站共享的诗歌/诗人数据加载器。
// 原 main.py 在进程启动时把所有 poet.tang.*.json / authors.tang.json
// 读入内存一次，这里用模块级单例缓存达到同样的"只加载一次"效果。

let poemsPromise = null
let authorsPromise = null
let poetWordfreqPromise = null

export function loadPoems() {
  if (!poemsPromise) {
    poemsPromise = fetch(`${import.meta.env.BASE_URL}data/poems.json`).then((r) => r.json())
  }
  return poemsPromise
}

export function loadAuthors() {
  if (!authorsPromise) {
    authorsPromise = fetch(`${import.meta.env.BASE_URL}data/authors.json`).then((r) => r.json())
  }
  return authorsPromise
}

// 按诗人名查词频，对应原 /poet_wordfreq/{name}。所有诗人的数据
// 合并在一个 JSON 里（key 为诗人名），一次性加载后在内存中查表。
export function loadPoetWordfreq() {
  if (!poetWordfreqPromise) {
    poetWordfreqPromise = fetch(`${import.meta.env.BASE_URL}data/poet_wordfreq.json`).then((r) =>
      r.json(),
    )
  }
  return poetWordfreqPromise
}
