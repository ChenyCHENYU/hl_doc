<script setup lang="ts">
defineProps<{ cat: string; src: string }>();
</script>

<template>
  <div class="th-wrap">
    <div class="th-crumb">
      <a href="/guide/">宝典指南</a>
      <span class="th-sep">/</span>
      <a :href="`/guide/#${cat}`">{{ cat }}</a>
    </div>
    <span class="th-src">{{ src }} · 游戏内宝典原文整理</span>
  </div>
</template>

<style scoped>
.th-wrap {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin: 0 0 20px;
  padding: 12px 16px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
}

.th-crumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13.5px;
}

.th-crumb a {
  color: var(--vp-c-brand-1);
  font-weight: 600;
  text-decoration: none;
}

.th-crumb a:hover {
  text-decoration: underline;
}

.th-sep {
  color: var(--vp-c-text-3);
}

.th-src {
  font-size: 12px;
  color: var(--vp-c-text-3);
  font-family: var(--vp-font-family-mono);
}
</style>
