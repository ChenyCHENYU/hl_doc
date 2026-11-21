<script setup lang="ts">
import { computed } from "vue";
import { authorByKey } from "../../data/authors";

const props = defineProps<{ author: string; compact?: boolean }>();

const a = computed(() => authorByKey[props.author]);

const avatar = computed(() => {
  const qq = a.value?.qq;
  if (qq && /^\d{5,11}$/.test(qq)) return `https://q1.qlogo.cn/g?b=qq&nk=${qq}&s=100`;
  return "";
});

const TAG_TONES = ["#b8860b", "#2e9e6f", "#4d8fd1", "#d15a5a", "#8a6fd0", "#c4875a"];
function tone(i: number): string {
  return TAG_TONES[i % TAG_TONES.length];
}
</script>

<template>
  <aside v-if="a" class="au" :class="{ isCompact: compact }">
    <div class="au-main">
      <img v-if="avatar" class="au-avatar" :src="avatar" :alt="a.name" loading="lazy" />
      <span v-else class="au-avatar au-fallback">{{ a.name.slice(0, 1) }}</span>
      <div class="au-who">
        <div class="au-name-row">
          <b class="au-name">{{ a.name }}</b>
          <span v-if="a.qq" class="au-qq">QQ {{ a.qq }}</span>
        </div>
        <div class="au-tags">
          <span
            v-for="(t, i) in a.tags"
            :key="t"
            class="au-tag"
            :style="{ color: tone(i), borderColor: tone(i) + '66', background: tone(i) + '14' }"
          >{{ t }}</span>
        </div>
      </div>
    </div>
    <p class="au-contribution">{{ a.contribution }}</p>
    <div v-if="a.works?.length && !compact" class="au-works">
      <a v-for="w in a.works" :key="w.link" :href="w.link" class="au-work">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        {{ w.title }}
      </a>
    </div>
  </aside>
</template>

<style scoped>
.au {
  margin: 22px 0;
  padding: 16px 18px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 14px;
  background: var(--vp-c-bg-soft);
  max-width: 760px;
}

.au.isCompact {
  padding: 12px 14px;
}

.au-main {
  display: flex;
  align-items: center;
  gap: 12px;
}

.au-avatar {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  background: #fff;
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.05);
}

.au-fallback {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-size: 20px;
  font-weight: 800;
}

.isCompact .au-avatar {
  width: 36px;
  height: 36px;
  font-size: 16px;
}

.au-who {
  min-width: 0;
  flex: 1;
}

.au-name-row {
  display: flex;
  align-items: baseline;
  gap: 10px;
  flex-wrap: wrap;
}

.au-name {
  font-size: 16px;
  font-weight: 800;
  color: var(--vp-c-text-1);
}

.au-qq {
  font-size: 12px;
  font-weight: 600;
  color: var(--vp-c-brand-1);
  border: 1px solid var(--vp-c-brand-soft);
  border-radius: 999px;
  padding: 1px 10px;
  font-variant-numeric: tabular-nums;
}

.au-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 6px;
}

.au-tag {
  font-size: 11.5px;
  font-weight: 700;
  border: 1px solid;
  border-radius: 999px;
  padding: 1px 10px;
  white-space: nowrap;
}

.au-contribution {
  margin: 12px 0 0;
  font-size: 13px;
  line-height: 1.85;
  color: var(--vp-c-text-2);
}

.isCompact .au-contribution {
  margin-top: 8px;
  font-size: 12.5px;
}

.au-works {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.au-work {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 30px;
  padding: 4px 13px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  background: var(--vp-c-bg);
  color: var(--vp-c-brand-1);
  font-size: 12.5px;
  font-weight: 600;
  text-decoration: none;
  transition: border-color 0.15s, transform 0.15s;
}

.au-work:hover {
  border-color: var(--vp-c-brand-1);
  transform: translateY(-1px);
}
</style>
