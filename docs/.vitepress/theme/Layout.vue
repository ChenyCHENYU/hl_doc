<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import { useRouter } from 'vitepress'
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import ReadingProgress from './components/ReadingProgress.vue'
import NotFound from './components/NotFound.vue'
import CommentBox from './components/CommentBox.vue'

const { Layout } = DefaultTheme

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
  }
)
</script>

<template>
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
   路由切换进度条
   ═══════════════════════════════════════════ */
.nav-progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9998;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, var(--field-accent), var(--field-wood), var(--field-accent));
  background-size: 200% 100%;
  animation: progress-slide 0.8s ease-in-out infinite;
  border-radius: 0 1px 1px 0;
}

/* ═══════════════════════════════════════════
   过渡动画
   ═══════════════════════════════════════════ */
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
@keyframes progress-slide {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
