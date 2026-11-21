<script setup lang="ts">
import { ref } from "vue";
import { assetUrl } from "../assets";
defineProps<{ img: string; title: string }>();
const failed = ref(false);
</script>

<template>
  <figure class="adv-chart">
    <div class="adv-chart-frame">
      <a v-if="!failed" :href="assetUrl(img)" target="_blank" rel="noopener" :aria-label="`查看大图：${title}`">
        <img :src="assetUrl(img)" :alt="title" loading="lazy" @error="failed = true" />
      </a>
      <span v-else class="adv-chart-fallback">暂时无法显示大图，请参考页面上的文字说明。</span>
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
  padding: 48px 24px;
  font-size: 13.5px;
  color: var(--vp-c-text-3);
  letter-spacing: 0.05em;
}

figcaption {
  margin-top: 10px;
  text-align: center;
  font-size: 13px;
  color: var(--vp-c-text-2);
}
</style>
