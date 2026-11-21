<script setup lang="ts">
defineProps<{ img: string; title: string }>();
</script>

<template>
  <figure class="adv-chart">
    <div class="adv-chart-frame">
      <img :src="img" :alt="title" loading="lazy" @error="($event.target as HTMLElement).closest('.adv-chart-frame')?.classList.add('img-failed'); ($event.target as HTMLElement).remove()" />
      <span class="adv-chart-fallback">大图已归档 · 待 OSS 图床上线后展示</span>
    </div>
    <figcaption>{{ title }}</figcaption>
  </figure>
</template>

<style scoped>
.adv-chart {
  margin: 20px 0 28px;
}

.adv-chart-frame {
  position: relative;
  border-radius: 14px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
}

.adv-chart-frame img {
  width: 100%;
  height: auto;
  display: block;
}

.adv-chart-fallback {
  display: none;
  padding: 48px 24px;
  font-size: 13.5px;
  color: var(--vp-c-text-3);
  letter-spacing: 0.05em;
}

.adv-chart-frame.img-failed .adv-chart-fallback {
  display: block;
}

figcaption {
  margin-top: 10px;
  text-align: center;
  font-size: 13px;
  color: var(--vp-c-text-2);
}
</style>
