<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";
import { useRoute } from "vitepress";

const progress = ref(0);
const route = useRoute();
const enabled = /\/guide\/library\/lib-/.test(route.path);
let handler = () => {};

onMounted(() => {
  if (!enabled) return;
  handler = () => {
    const h = document.documentElement;
    const total = h.scrollHeight - h.clientHeight;
    progress.value = total > 0 ? (h.scrollTop / total) * 100 : 0;
  };
  window.addEventListener("scroll", handler, { passive: true });
  handler();
});

onUnmounted(() => window.removeEventListener("scroll", handler));
</script>

<template>
  <div v-if="enabled" class="rp-bar" :style="{ width: progress + '%' }"></div>
</template>

<style scoped>
.rp-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  z-index: 90;
  background: linear-gradient(90deg, #b8860b, #f5d67b);
  box-shadow: 0 0 8px rgba(212, 175, 55, 0.6);
  transition: width 0.1s linear;
}
</style>
