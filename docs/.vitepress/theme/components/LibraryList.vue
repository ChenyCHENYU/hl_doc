<script setup lang="ts">
import { computed, ref } from "vue";
import library from "../../data/library.json";

interface LibEntry {
  slug: string;
  title: string;
  cat: string;
  paras: number;
}

const entries = library as LibEntry[];
const cats = ["全部", ...Array.from(new Set(entries.map((e) => e.cat)))];
const activeCat = ref("全部");
const keyword = ref("");

const filtered = computed(() => {
  const k = keyword.value.trim();
  return entries.filter((e) => {
    if (activeCat.value !== "全部" && e.cat !== activeCat.value) return false;
    if (!k) return true;
    return e.title.includes(k);
  });
});

const CAT_COLOR: Record<string, string> = {
  宠物练级: "#5cae7d",
  宠物养成: "#b8860b",
  宠物分布: "#5b9bd5",
  "锻造-武器": "#d15a5a",
  "锻造-防具": "#4d8fd1",
  "锻造-饰品": "#9a7fd1",
  "锻造-其他": "#c4875a",
  战斗与PK: "#d1893b",
  综合其他: "#97a0b0",
};

const CAT_ICON: Record<string, string> = {
  宠物练级: "练",
  宠物养成: "养",
  宠物分布: "布",
  "锻造-武器": "武",
  "锻造-防具": "甲",
  "锻造-饰品": "饰",
  "锻造-其他": "锻",
  战斗与PK: "斗",
  综合其他: "汇",
};
</script>

<template>
  <div class="pc-wrap">
    <div class="pc-toolbar">
      <div class="pc-tabs">
        <button
          v-for="c in cats"
          :key="c"
          class="pc-tab"
          :class="{ active: activeCat === c }"
          @click="activeCat = c"
        >
          {{ c }}<span v-if="c !== '全部'" class="lib-tab-count">{{ entries.filter((e) => e.cat === c).length }}</span>
        </button>
      </div>
      <input v-model="keyword" class="item-search pc-search" type="search" placeholder="搜索文章标题" />
    </div>

    <p class="item-count">命中 {{ filtered.length }} 篇 / 共 {{ entries.length }} 篇</p>

    <div class="lib-grid">
      <a v-for="e in filtered" :key="e.slug" :href="`/guide/library/${e.slug}`" class="lib-card" :style="{ borderLeftColor: CAT_COLOR[e.cat] ?? 'var(--vp-c-divider)' }">
        <span class="lib-icon" :style="{ color: CAT_COLOR[e.cat], borderColor: (CAT_COLOR[e.cat] ?? '#b8860b') + '55', background: (CAT_COLOR[e.cat] ?? '#b8860b') + '14' }">{{ CAT_ICON[e.cat] ?? "汇" }}</span>
        <div class="lib-body">
          <div class="lib-title">{{ e.title }}</div>
          <div class="lib-meta">
            <span class="lib-cat">{{ e.cat }}</span>
            <span>{{ e.paras }} 段</span>
          </div>
        </div>
        <svg class="lib-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M5 12h14M12 5l7 7-7 7" />
        </svg>
      </a>
    </div>
  </div>
</template>

<style scoped>
.lib-tab-count {
  font-size: 12px;
  opacity: 0.65;
  margin-left: 4px;
}

.lib-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 10px;
  margin: 12px 0 24px;
}

.lib-card {
  display: flex;
  align-items: center;
  gap: 14px;
  border: 1px solid var(--vp-c-divider);
  border-left: 3px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 14px 16px;
  text-decoration: none;
  background: var(--vp-c-bg-soft);
  transition: border-color 0.15s, transform 0.15s, box-shadow 0.15s;
}

.lib-card:hover {
  border-color: rgba(184, 134, 11, 0.45);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(184, 134, 11, 0.12);
}

.dark .lib-card:hover {
  border-color: rgba(240, 201, 78, 0.45);
  box-shadow: 0 8px 20px rgba(240, 201, 78, 0.16);
}

.lib-icon {
  flex-shrink: 0;
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  background: rgba(184, 134, 11, 0.08);
  border: 1px solid rgba(184, 134, 11, 0.22);
  border-radius: 10px;
}

.dark .lib-icon {
  background: rgba(240, 201, 78, 0.1);
  border-color: rgba(240, 201, 78, 0.28);
}

.lib-body {
  min-width: 0;
  flex: 1;
}

.lib-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--vp-c-text-1);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.lib-meta {
  display: flex;
  gap: 10px;
  margin-top: 4px;
  font-size: 12px;
  color: var(--vp-c-text-3);
}

.lib-cat {
  color: var(--vp-c-brand-1);
}

.lib-arrow {
  flex-shrink: 0;
  color: var(--vp-c-brand-1);
  opacity: 0;
  transform: translateX(-4px);
  transition: opacity 0.15s, transform 0.15s;
}

.lib-card:hover .lib-arrow {
  opacity: 1;
  transform: translateX(0);
}
</style>
