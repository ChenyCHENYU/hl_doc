<script setup lang="ts">
import { computed } from "vue";
import library from "../../data/library.json";

interface LibEntry {
  slug: string;
  title: string;
  cat: string;
}

const props = defineProps<{ cat: string; topic: string }>();

const STATIC: Record<string, { label: string; href: string }[]> = {
  人物相关: [
    { label: "称号阶梯与飞升路线", href: "/guide/titles" },
    { label: "任务攻略 · 飞升流程", href: "/quests/ascend" },
  ],
  宠物相关: [
    { label: "宠物图鉴总览", href: "/pets/" },
    { label: "进化系谱大全", href: "/pets/evolutions" },
    { label: "重塑价格表", href: "/pets/prices" },
  ],
  战斗相关: [
    { label: "天关防御参数表", href: "/monsters/" },
    { label: "招系数排名图表", href: "/advanced/charts" },
  ],
  帮派相关: [
    { label: "幻灵英雄墙", href: "/heroes/" },
  ],
  其他帮助: [
    { label: "物品大全", href: "/items/" },
    { label: "资源库", href: "/resources/" },
  ],
  任务攻略: [
    { label: "宝典指南", href: "/guide/" },
    { label: "全部飞升攻略", href: "/quests/ascend" },
  ],
};

const KEYWORDS: Record<string, string[]> = {
  宠物相关: ["宠物", "宠", "进化", "幻化", "练级", "抓"],
  战斗相关: ["PK", "战斗", "武功", "克"],
  人物相关: ["飞升", "转", "装备", "称号"],
  帮派相关: ["帮派", "帮"],
  其他帮助: ["锻造", "交易", "银行"],
  任务攻略: ["任务", "飞升"],
};

const relatedLib = computed(() => {
  const kws = KEYWORDS[props.cat] ?? [];
  const topicChars = new Set(props.topic.split(""));
  return (library as LibEntry[])
    .map((e) => {
      let score = 0;
      if (kws.some((k) => e.title.includes(k))) score += 2;
      score += [...props.topic].filter((c) => e.title.includes(c)).length;
      return { e, score };
    })
    .filter((x) => x.score >= 3)
    .sort((a, b) => b.score - a.score)
    .slice(0, 3)
    .map((x) => ({ label: `文库 · ${x.e.title.slice(0, 16)}`, href: `/guide/library/${x.e.slug}` }));
});

const all = computed(() => [...(STATIC[props.cat] ?? []), ...relatedLib.value]);
</script>

<template>
  <div v-if="all.length" class="tr-wrap">
    <div class="tr-title">相关内容</div>
    <div class="tr-grid">
      <a v-for="r in all" :key="r.href + r.label" :href="r.href" class="tr-link">
        <span>{{ r.label }}</span>
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M5 12h14M12 5l7 7-7 7" />
        </svg>
      </a>
    </div>
  </div>
</template>

<style scoped>
.tr-wrap {
  margin: 36px 0 8px;
  padding-top: 18px;
  border-top: 1px solid var(--vp-c-divider);
}

.tr-title {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.2em;
  color: var(--vp-c-text-3);
  margin-bottom: 12px;
}

.tr-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 8px;
}

.tr-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 9px;
  padding: 9px 13px;
  font-size: 13px;
  color: var(--vp-c-text-2);
  text-decoration: none;
  background: var(--vp-c-bg-soft);
  transition: border-color 0.15s, color 0.15s, transform 0.15s;
}

.tr-link:hover {
  border-color: rgba(184, 134, 11, 0.45);
  color: var(--vp-c-brand-1);
  transform: translateY(-1px);
}

.tr-link svg {
  flex-shrink: 0;
  opacity: 0;
  transition: opacity 0.15s;
  color: var(--vp-c-brand-1);
}

.tr-link:hover svg {
  opacity: 1;
}
</style>
