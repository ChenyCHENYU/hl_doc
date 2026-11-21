<script setup lang="ts">
import { helpCategories } from "../../data/helpToc";
import cardsData from "../../data/help-cards.json";

const cardTopics = new Map(
  (cardsData as { topic: string; cat: string }[]).map((c) => {
    const key = { 人物相关: "gr", 宠物相关: "cw", 战斗相关: "xx", 帮派相关: "wh", 其他帮助: "gl" }[c.cat] ?? "gl";
    return [c.topic + "|" + c.cat, `/guide/cards/${key}`];
  })
);

const ICONS: Record<string, string> = {
  gr: "人",
  cw: "宠",
  xx: "战",
  wh: "帮",
  gl: "杂",
};

const COLORS: Record<string, string> = {
  gr: "#4d8fd1",
  cw: "#b8860b",
  xx: "#d15a5a",
  wh: "#2e9e6f",
  gl: "#97a0b0",
};

function topicLink(source: string, title: string, cat: string): string {
  const card = cardTopics.get(title + "|" + cat);
  if (card) return card;
  return `/guide/topics/${source.replace(/\.htm$/, "")}`;
}
</script>

<template>
  <div v-for="cat in helpCategories" :key="cat.key" class="gc-cat">
    <h3 :id="cat.title" class="gc-cat-title">
      <span class="gc-icon" :style="{ color: COLORS[cat.key], borderColor: COLORS[cat.key] + '55', background: COLORS[cat.key] + '14' }">{{ ICONS[cat.key] ?? "书" }}</span>
      {{ cat.title }}
      <span class="gc-count">{{ cat.topics.length }} 个专题 · 点击进入</span>
    </h3>
    <div class="gc-grid">
      <a
        v-for="t in cat.topics"
        :key="t.title + t.source"
        :href="topicLink(t.source, t.title, cat.title)"
        class="gc-topic"
        :title="'来源：游戏内宝典 ' + t.source"
      >
        <span class="gc-topic-name">{{ t.title }}</span>
        <svg class="gc-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M5 12h14M12 5l7 7-7 7" />
        </svg>
      </a>
    </div>
  </div>
</template>

<style scoped>
.gc-cat {
  margin: 8px 0 28px;
}

.gc-cat-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 17px;
  font-weight: 700;
  color: var(--vp-c-text-1);
  margin: 0 0 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--vp-c-divider);
}

.gc-icon {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  background: rgba(184, 134, 11, 0.08);
  border: 1px solid rgba(184, 134, 11, 0.22);
  border-radius: 8px;
}

.dark .gc-icon {
  background: rgba(240, 201, 78, 0.1);
  border-color: rgba(240, 201, 78, 0.28);
}

.gc-count {
  font-size: 12px;
  font-weight: 500;
  color: var(--vp-c-text-3);
}

.gc-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 10px;
}

.gc-topic {
  display: flex;
  align-items: center;
  gap: 8px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  padding: 12px 14px;
  text-decoration: none;
  background: var(--vp-c-bg-soft);
  transition: border-color 0.15s, transform 0.15s, box-shadow 0.15s;
}

.gc-topic:hover {
  border-color: rgba(184, 134, 11, 0.45);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(184, 134, 11, 0.12);
}

.dark .gc-topic:hover {
  border-color: rgba(240, 201, 78, 0.45);
  box-shadow: 0 8px 20px rgba(240, 201, 78, 0.16);
}

.gc-topic-name {
  font-size: 14.5px;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.gc-topic-src {
  font-size: 11px;
  color: var(--vp-c-text-3);
  font-family: var(--vp-font-family-mono);
}

.gc-arrow {
  margin-left: auto;
  color: var(--vp-c-brand-1);
  opacity: 0;
  transform: translateX(-4px);
  transition: opacity 0.15s, transform 0.15s;
  flex-shrink: 0;
}

.gc-topic:hover .gc-arrow {
  opacity: 1;
  transform: translateX(0);
}
</style>
