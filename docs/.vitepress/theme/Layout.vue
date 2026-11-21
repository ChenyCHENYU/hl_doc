<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import { useRouter } from 'vitepress'
import { ref, computed, watch } from 'vue'
import ReadingProgress from './components/ReadingProgress.vue'
import NotFound from './components/NotFound.vue'
import CommentBox from './components/CommentBox.vue'

const { Layout } = DefaultTheme

// ─── 路由切换过渡 ───
const router = useRouter()
// 文章类页面底部挂评论区（文库/专题/任务/养成/陈列馆/宠物详情），列表与首页不挂
const COMMENT_ROUTES = /^(\/guide\/library\/(lib|bd)-|\/guide\/topics\/|\/quests\/(?!ascend$)|\/advanced\/manxing-|\/museum\/|\/pets\/\d+)/
const showComments = computed(() => COMMENT_ROUTES.test(router.route.path))
const routePath = computed(() => router.route.path.replace(/\.html$/, '').replace(/\/$/, '') || '/')
const contentMode = computed(() => {
  const path = routePath.value
  if (/^\/(pets(?:\/(?:prices|evolutions))?|items|monsters|resources|heroes|guide\/library)$/.test(path)) return 'wide'
  if (/^\/(quests\/.+|advanced\/manxing-.+|guide\/(?:library|topics)\/.+|pets\/\d+|search|maps|about)$/.test(path)) return 'reading'
  return 'catalog'
})
const isNavigating = ref(false)

watch(
  () => router.route.path,
  () => {
    isNavigating.value = true
    setTimeout(() => { isNavigating.value = false }, 480)
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
  <div class="wiki-frame" :data-content-mode="contentMode">
    <Layout>
      <template #not-found>
        <NotFound />
      </template>
      <template #doc-after>
        <CommentBox v-if="showComments" />
      </template>
    </Layout>
  </div>
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
