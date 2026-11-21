<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import { useRouter } from 'vitepress'
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import ReadingProgress from './components/ReadingProgress.vue'
import NotFound from './components/NotFound.vue'
import CommentBox from './components/CommentBox.vue'

const { Layout } = DefaultTheme

// ─── 初始加载动画 ───
const showLoading = ref(true)

onMounted(() => {
  requestAnimationFrame(() => {
    setTimeout(() => {
      showLoading.value = false
    }, 160)
  })
})

// ─── 路由切换过渡 ───
const router = useRouter()
// 文章类页面底部挂评论区（文库/专题/任务/养成/陈列馆/宠物详情），列表与首页不挂
const COMMENT_ROUTES = /^(\/guide\/library\/(lib|bd)-|\/guide\/topics\/|\/quests\/(?!ascend$)|\/advanced\/manxing-|\/museum\/|\/pets\/\d+)/
const showComments = computed(() => COMMENT_ROUTES.test(router.route.path))
// 文章页正文阅读列宽（长文本不限宽会堆成难读的长行）；SSR 无 document，仅客户端执行
if (typeof document !== "undefined") {
  watch(
    () => router.route.path,
    () => {
      document.body.classList.toggle('hc-article', COMMENT_ROUTES.test(router.route.path));
    },
    { immediate: true }
  );
}
const isNavigating = ref(false)

const compactTableHeaders = new Set([
  'ID',
  '编号',
  '序号',
  '名称',
  '出处',
  '版本',
  '数量',
  '操作'
])

const optimizeDocumentTables = () => {
  document.querySelectorAll<HTMLTableElement>('.vp-doc table').forEach((table) => {
    table.querySelectorAll('.is-compact-column').forEach((cell) => {
      cell.classList.remove('is-compact-column')
    })

    const headers = Array.from(table.querySelectorAll<HTMLTableCellElement>('thead th'))
    const rows = Array.from(table.querySelectorAll<HTMLTableRowElement>('tbody tr'))

    headers.forEach((header, columnIndex) => {
      const cells = rows
        .map((row) => row.children.item(columnIndex))
        .filter((cell): cell is Element => cell !== null)

      const headerText = header.textContent?.replace(/\s+/g, '') ?? ''
      const allCellsAreShort = cells.length > 0 && cells.every((cell) => {
        const text = cell.textContent?.replace(/\s+/g, ' ').trim() ?? ''
        const hasComplexContent = cell.querySelector('ul, ol, pre, br') !== null
        return !hasComplexContent && text.length <= 12
      })

      if (compactTableHeaders.has(headerText) || allCellsAreShort) {
        const compactCells = [header, ...cells]
        compactCells.forEach((cell) => {
          cell.classList.add('is-compact-column')
        })
      }
    })
  })
}

const scheduleTableOptimization = () => {
  nextTick(() => {
    requestAnimationFrame(optimizeDocumentTables)
  })
}

onMounted(scheduleTableOptimization)

// ─── 全局弹窗兜底：ESC 关闭 + 打开时锁定背景滚动 ───
// Teleport 把 .pc-overlay 挂在 body 直下，childList 级监听即可
const syncOverlayLock = () => {
  document.body.style.overflow = document.querySelector('body > .pc-overlay') ? 'hidden' : ''
}
const onGlobalKeydown = (e: KeyboardEvent) => {
  if (e.key !== 'Escape') return
  const close = document.querySelector<HTMLButtonElement>('body > .pc-overlay .pc-close')
  if (close) close.click()
}
let overlayObserver: MutationObserver | null = null

onMounted(() => {
  overlayObserver = new MutationObserver(syncOverlayLock)
  overlayObserver.observe(document.body, { childList: true })
  document.addEventListener('keydown', onGlobalKeydown)
  syncOverlayLock()
})
onUnmounted(() => {
  overlayObserver?.disconnect()
  document.removeEventListener('keydown', onGlobalKeydown)
  document.body.style.overflow = ''
})

watch(
  () => router.route.path,
  () => {
    isNavigating.value = true
    nextTick(() => {
      setTimeout(() => {
        isNavigating.value = false
      }, 480)
    })
    scheduleTableOptimization()
    nextTick(() => {
      const content = document.querySelector('.VPDoc .main')
      if (!content) return
      content.classList.remove('page-transition')
      void (content as HTMLElement).offsetWidth
      content.classList.add('page-transition')
      setTimeout(() => content.classList.remove('page-transition'), 400)
    })
  }
)
</script>

<template>
  <!-- 初始加载屏 -->
  <Transition name="loading-fade">
    <div v-if="showLoading" class="app-loading">
      <div class="app-loading__container">
        <!-- SVG Logo 动画 -->
        <svg class="app-loading__logo" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle
            cx="40" cy="40" r="36"
            stroke="url(#loading-gradient)"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-dasharray="180 226"
            class="app-loading__ring"
          />
          <circle
            cx="40" cy="40" r="24"
            stroke="url(#loading-gradient)"
            stroke-width="1.5"
            stroke-dasharray="100 151"
            opacity="0.5"
            class="app-loading__ring app-loading__ring--inner"
          />
          <path
            d="M40 24L46 40L62 40L49 49L54 65L40 56L26 65L31 49L18 40L34 40Z"
            stroke="url(#loading-gradient)"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="app-loading__icon"
          />
          <defs>
            <linearGradient id="loading-gradient" x1="0" y1="0" x2="80" y2="80">
              <stop offset="0%" stop-color="#b8860b" />
              <stop offset="100%" stop-color="#d4af37" />
            </linearGradient>
          </defs>
        </svg>
        <!-- 品牌文字 -->
        <div class="app-loading__text">幻灵宝典</div>
        <div class="app-loading__dots">
          <span /><span /><span />
        </div>
      </div>
    </div>
  </Transition>

  <!-- 路由切换进度条 -->
  <Transition name="nav-progress">
    <div v-if="isNavigating" class="nav-progress-bar" />
  </Transition>

  <!-- 主内容 -->
  <ReadingProgress />
  <Layout>
    <template #not-found>
      <NotFound />
    </template>
    <template #doc-after>
      <CommentBox v-if="showComments" />
    </template>
  </Layout>
</template>

<style>
/* ═══════════════════════════════════════════
   初始加载屏
   ═══════════════════════════════════════════ */
.app-loading {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
}
.dark .app-loading {
  background: #09090b;
}

.app-loading__container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.app-loading__logo {
  width: 80px;
  height: 80px;
}

/* 外圈旋转 */
.app-loading__ring {
  transform-origin: center;
  animation: ring-spin 1.8s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}
.app-loading__ring--inner {
  animation-direction: reverse;
  animation-duration: 2.4s;
}

/* 中心图标描边动画 */
.app-loading__icon {
  /* 图标直接完整呈现：停留仅百余毫秒，慢描边动画等于看不见 */
  stroke-dasharray: none;
}

/* 品牌文字 */
.app-loading__text {
  font-family: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 6px;
  background: linear-gradient(135deg, #b8860b, #d4af37);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 加载圆点 */
.app-loading__dots {
  display: flex;
  gap: 6px;
}
.app-loading__dots span {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: linear-gradient(135deg, #b8860b, #d4af37);
  animation: dot-pulse 1.2s ease-in-out infinite;
}
.app-loading__dots span:nth-child(2) { animation-delay: 0.15s; }
.app-loading__dots span:nth-child(3) { animation-delay: 0.3s; }

/* ═══════════════════════════════════════════
   路由切换进度条
   ═══════════════════════════════════════════ */
.nav-progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9998;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #b8860b, #f5d67b, #b8860b);
  background-size: 200% 100%;
  animation: progress-slide 0.8s ease-in-out infinite;
  border-radius: 0 1px 1px 0;
}

/* ═══════════════════════════════════════════
   过渡动画
   ═══════════════════════════════════════════ */
.loading-fade-leave-active {
  transition: opacity 0.28s ease;
}
.loading-fade-leave-to {
  opacity: 0;
}

.nav-progress-enter-active {
  transition: opacity 0.25s cubic-bezier(0.22, 0.61, 0.36, 1);
}
.nav-progress-leave-active {
  transition: opacity 0.45s cubic-bezier(0.22, 0.61, 0.36, 1);
}
.nav-progress-enter-from,
.nav-progress-leave-to {
  opacity: 0;
}

/* ═══════════════════════════════════════════
   关键帧
   ═══════════════════════════════════════════ */
@keyframes ring-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes dot-pulse {
  0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
  40% { opacity: 1; transform: scale(1.2); }
}

@keyframes progress-slide {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
