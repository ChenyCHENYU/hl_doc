<script setup lang="ts">
import { computed, ref } from "vue";
import codex from "../../data/pet-codex.json";

interface Pet {
  id: number;
  name: string;
  element: string;
  type: string;
  evolveIllegal: string;
  evolveNormal: string;
  image: { file: string; ossKey: string; url: string } | null;
}

const pets = codex as Pet[];
const byName = new Map(pets.map((p) => [p.name, p]));

const ELEMENTS: Record<string, { label: string; color: string }> = {
  metal: { label: "金", color: "#d4af37" },
  wood: { label: "木", color: "#5cae7d" },
  water: { label: "水", color: "#5b9bd5" },
  fire: { label: "火", color: "#e0664f" },
  earth: { label: "土", color: "#c4875a" },
};

function buildChain(startName: string): Pet[] {
  const chain: Pet[] = [];
  const seen = new Set<string>();
  let cur = byName.get(startName);
  while (cur && !seen.has(cur.name)) {
    chain.push(cur);
    seen.add(cur.name);
    cur = cur.evolveNormal ? byName.get(cur.evolveNormal) : undefined;
  }
  return chain;
}

function pickLineage(el: string): Pet[] | null {
  const starters = pets.filter(
    (p) => p.element === el && p.evolveNormal && !pets.some((q) => q.evolveNormal === p.name || q.evolveIllegal === p.name)
  );
  let best: Pet[] | null = null;
  for (const s of starters) {
    const chain = buildChain(s.name);
    if (chain.length >= 3 && chain.every((p) => p.image)) {
      if (!best || chain.length > best.length) best = chain;
      if (best.length >= 4) break;
    }
  }
  if (!best) {
    for (const s of pets.filter((p) => p.element === el && p.image)) {
      const chain = buildChain(s.name);
      if (chain.length >= 3 && chain.every((p) => p.image) && (!best || chain.length > best.length)) {
        best = chain;
      }
    }
  }
  return best && best.length >= 3 ? best : null;
}

const lineages = (["metal", "wood", "water", "fire", "earth"] as const)
  .map((el) => ({ el, chain: pickLineage(el) }))
  .filter((l): l is { el: string; chain: Pet[] } => !!l.chain);

const active = ref(lineages[0]?.el ?? "metal");
const current = computed(() => lineages.find((l) => l.el === active.value)?.chain ?? []);
const finalName = computed(() => current.value[current.value.length - 1]?.name ?? "");

const TIER_LABELS = ["一级进化宠", "二级进化宠", "三级进化宠", "终级宠物"];

function imgUrl(p: Pet): string | null {
  if (!p.image) return null;
  return import.meta.env.DEV ? `/hl-assets/${p.image.ossKey}` : p.image.url;
}

function onImgError(e: Event) {
  const el = e.target as HTMLElement;
  el.closest(".evo2-node-img")?.classList.add("img-failed");
  el.remove();
}

const RULES = [
  { k: "进化条件", v: "500 级 + 忠诚 100" },
  { k: "防变异", v: "五行同属性地图进化" },
  { k: "终级获取", v: "两只 1000 级双幻化三级宠" },
  { k: "勋章", v: "进化后全额继承" },
];
</script>

<template>
  <div class="evo2">
    <div class="evo2-tabs">
      <button
        v-for="l in lineages"
        :key="l.el"
        class="evo2-tab"
        :class="{ active: active === l.el }"
        :style="active === l.el ? { borderColor: ELEMENTS[l.el].color, color: ELEMENTS[l.el].color } : {}"
        @click="active = l.el"
      >
        {{ ELEMENTS[l.el].label }}系 · {{ l.chain[l.chain.length - 1].name }}
      </button>
    </div>

    <div class="evo2-flow">
      <template v-for="(p, i) in current" :key="p.name">
        <div class="evo2-col">
          <a :href="`/pets/`" class="evo2-node" :style="{ '--el': ELEMENTS[p.element]?.color || '#b8860b' }">
            <div class="evo2-node-img" :class="{ 'no-img': !p.image }">
              <span class="evo2-glyph">{{ ELEMENTS[p.element]?.label }}</span>
              <img v-if="p.image" :src="imgUrl(p) || ''" :alt="p.name" loading="lazy" @error="onImgError" />
            </div>
            <div class="evo2-node-name">{{ p.name }}</div>
            <div class="evo2-node-tier" :class="{ final: i === current.length - 1 }">
              {{ TIER_LABELS[Math.min(i, 3)] }}
            </div>
          </a>
          <div v-if="p.evolveIllegal" class="evo2-branch">
            <span class="evo2-branch-line"></span>
            <span class="evo2-branch-chip">非法 → {{ p.evolveIllegal }}</span>
          </div>
        </div>
        <div v-if="i < current.length - 1" class="evo2-arrow" :style="{ color: ELEMENTS[p.element]?.color }">&#10142;</div>
      </template>
    </div>

    <div class="evo2-rules">
      <div v-for="r in RULES" :key="r.k" class="evo2-rule">
        <span class="evo2-rule-k">{{ r.k }}</span>
        <span class="evo2-rule-v">{{ r.v }}</span>
      </div>
    </div>

    <div class="evo2-links">
      深入阅读：
      <a href="/guide/library/">文库《进化幻化全攻略》《五转飞养宠问题》</a> ·
      <a href="/advanced/charts">图表《宠物进化表 2026》</a> ·
      <a href="/pets/">全部 {{ pets.length }} 只宠物档案</a>
    </div>
  </div>
</template>

<style scoped>
.evo2 {
  margin: 0 0 8px;
}

.evo2-tabs {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-bottom: 26px;
}

.evo2-tab {
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-2);
  border-radius: 999px;
  padding: 7px 18px;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.15s, border-color 0.15s;
}

.evo2-tab:hover {
  transform: translateY(-1px);
}

.evo2-flow {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 26px;
}

.evo2-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.evo2-node {
  width: 150px;
  text-decoration: none;
  border-radius: 14px;
  border: 1px solid var(--vp-c-divider);
  background:
    linear-gradient(var(--vp-c-bg), var(--vp-c-bg)) padding-box,
    linear-gradient(160deg, color-mix(in srgb, var(--el) 60%, transparent), transparent 60%) border-box;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.evo2-node:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px -10px color-mix(in srgb, var(--el) 55%, transparent);
}

.evo2-node-img {
  position: relative;
  aspect-ratio: 1 / 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  overflow: hidden;
}

.dark .evo2-node-img {
  background: #f7f5f0;
}

.evo2-node-img img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 10px;
  image-rendering: pixelated;
}

.evo2-glyph {
  display: none;
  font-size: 42px;
  font-weight: 800;
  color: color-mix(in srgb, var(--el) 60%, var(--vp-c-text-3));
}

.evo2-node-img.no-img .evo2-glyph,
.evo2-node-img.img-failed .evo2-glyph {
  display: block;
}

.evo2-node-name {
  padding: 8px 10px 2px;
  text-align: center;
  font-size: 15px;
  font-weight: 700;
  color: var(--vp-c-text-1);
}

.evo2-node-tier {
  padding: 0 10px 10px;
  text-align: center;
  font-size: 12px;
  color: var(--vp-c-text-3);
}

.evo2-node-tier.final {
  color: var(--vp-c-brand-1);
  font-weight: 700;
}

.evo2-branch {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.evo2-branch-line {
  width: 1px;
  height: 12px;
  border-left: 1px dashed var(--vp-c-divider);
}

.evo2-branch-chip {
  font-size: 12px;
  color: var(--vp-c-text-3);
  border: 1px dashed var(--vp-c-divider);
  border-radius: 8px;
  padding: 2px 8px;
  white-space: nowrap;
}

.evo2-arrow {
  align-self: center;
  margin-top: 60px;
  font-size: 22px;
}

.evo2-rules {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 10px;
  margin-bottom: 18px;
}

.evo2-rule {
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
  padding: 10px 14px;
}

.evo2-rule-k {
  flex-shrink: 0;
  font-size: 12px;
  font-weight: 700;
  color: var(--vp-c-brand-1);
}

.evo2-rule-v {
  font-size: 12.5px;
  color: var(--vp-c-text-2);
}

.evo2-links {
  text-align: center;
  font-size: 13px;
  color: var(--vp-c-text-2);
}

.evo2-links a {
  color: var(--vp-c-brand-1);
  font-weight: 600;
  text-decoration: none;
}

.evo2-links a:hover {
  text-decoration: underline;
}

@media (max-width: 760px) {
  .evo2-flow {
    flex-direction: column;
    align-items: center;
  }

  .evo2-arrow {
    margin-top: 0;
    transform: rotate(90deg);
  }
}
</style>
