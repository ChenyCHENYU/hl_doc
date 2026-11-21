<script setup lang="ts">
import { computed, ref } from "vue";
import codex from "../../data/pet-codex.json";
import { computeLineages, evoImgUrl, EVO_ELEMENTS, type EvoPet, type Lineage } from "../evolution";
import PetQuickView from "./PetQuickView.vue";

const all = computeLineages(codex as EvoPet[]);
const TABS = ["全部", "金", "木", "水", "火", "土"];
const active = ref("全部");
const keyword = ref("");
const quickView = ref<InstanceType<typeof PetQuickView> | null>(null);

const shown = computed<Lineage[]>(() => {
  let list = all;
  if (active.value !== "全部") {
    const code = Object.entries(EVO_ELEMENTS).find(([, v]) => v.label === active.value)?.[0];
    if (code) list = list.filter((l) => l.element === code);
  }
  const k = keyword.value.trim();
  if (k) {
    list = list.filter((l) => l.chain.some((p) => p.name.includes(k)));
  }
  return list;
});
const shownPetIds = computed(() => Array.from(new Set(shown.value.flatMap((lineage) => lineage.chain.map((pet) => pet.id)))));

const petCount = new Set(all.flatMap((l) => l.chain.map((p) => p.name))).size;

function onImgError(e: Event) {
  const el = e.target as HTMLElement;
  el.closest(".ex-node-img")?.classList.add("img-failed");
  el.remove();
}

function tier(i: number, len: number): string {
  if (i === len - 1) return "终级";
  return `${["一", "二", "三", "四"][i] ?? i + 1}级`;
}
</script>

<template>
  <div class="ex-wrap">
    <div class="pc-toolbar">
      <div class="pc-tabs">
        <button
          v-for="t in TABS"
          :key="t"
          class="pc-tab"
          type="button"
          :aria-pressed="active === t"
          :class="{ active: active === t }"
          @click="active = t"
        >
          {{ t }}
        </button>
      </div>
      <input v-model="keyword" class="item-search pc-search" type="search" placeholder="按宠物名搜系谱（如：狼 / 晶刚）" aria-label="按宠物名筛选系谱" />
    </div>

    <p class="item-count">
      {{ all.length }} 条进化系谱 · 覆盖 {{ petCount }} 只宠物 · 当前显示 {{ shown.length }} 条
    </p>

    <div v-for="(l, li) in shown" :key="li" class="ex-lineage" :style="{ '--el': EVO_ELEMENTS[l.element]?.color }">
      <span class="ex-badge">{{ EVO_ELEMENTS[l.element]?.label }}系</span>
      <div class="ex-chain">
        <template v-for="(p, i) in l.chain" :key="p.name + i">
          <a :href="`/pets/${p.id}`" aria-haspopup="dialog" class="ex-node vp-raw" :class="{ final: i === l.chain.length - 1 }" @click="quickView?.openFromLink($event, p.id)">
            <div class="ex-node-img" :class="{ 'no-img': !p.image }">
              <span class="ex-glyph">{{ EVO_ELEMENTS[p.element]?.label }}</span>
              <img v-if="p.image" :src="evoImgUrl(p) || ''" :alt="p.name" loading="lazy" @error="onImgError" />
            </div>
            <span class="ex-name">{{ p.name }}</span>
            <span class="ex-tier">{{ tier(i, l.chain.length) }}</span>
          </a>
          <span v-if="i < l.chain.length - 1" class="ex-arrow">&#10142;</span>
        </template>
      </div>
      <div v-if="l.chain.some((p) => p.evolveIllegal)" class="ex-illegal">
        <template v-for="(p, i) in l.chain" :key="'il' + i">
          <span v-if="p.evolveIllegal" class="ex-illegal-chip">{{ p.name }} 非法 → {{ p.evolveIllegal }}</span>
        </template>
      </div>
    </div>

    <p v-if="!shown.length" class="item-count">没有匹配的系谱，换个关键词试试。</p>
    <PetQuickView ref="quickView" :pet-ids="shownPetIds" />
  </div>
</template>

<style scoped>
.ex-wrap {
  margin: 16px 0 32px;
}

.ex-lineage {
  position: relative;
  border: 1px solid var(--vp-c-divider);
  border-radius: 14px;
  background: var(--vp-c-bg-soft);
  padding: 18px 18px 14px 64px;
  margin-bottom: 14px;
}

.ex-badge {
  position: absolute;
  left: 16px;
  top: 20px;
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  font-weight: 800;
  color: var(--el);
  border: 1.5px solid var(--el);
  border-radius: 10px;
  background: color-mix(in srgb, var(--el) 10%, transparent);
}

.ex-chain {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.ex-node {
  width: 96px;
  border-radius: 10px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  text-decoration: none;
  overflow: hidden;
  transition: transform 0.15s, box-shadow 0.15s;
}

.ex-node:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px -8px color-mix(in srgb, var(--el) 55%, transparent);
}

.ex-node.final {
  border-color: color-mix(in srgb, var(--el) 65%, transparent);
  box-shadow: 0 0 0 1px color-mix(in srgb, var(--el) 40%, transparent);
}

.ex-node-img {
  aspect-ratio: 1 / 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  position: relative;
}

.dark .ex-node-img {
  background: #f7f5f0;
}

.ex-node-img img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 6px;
  image-rendering: pixelated;
}

.ex-glyph {
  display: none;
  font-size: 26px;
  font-weight: 800;
  color: color-mix(in srgb, var(--el) 60%, var(--vp-c-text-3));
}

.ex-node-img.no-img .ex-glyph,
.ex-node-img.img-failed .ex-glyph {
  display: block;
}

.ex-name {
  display: block;
  text-align: center;
  font-size: 12.5px;
  font-weight: 700;
  color: var(--vp-c-text-1);
  padding-top: 5px;
}

.ex-tier {
  display: block;
  text-align: center;
  font-size: 12px;
  color: var(--vp-c-text-3);
  padding-bottom: 6px;
}

.ex-node.final .ex-tier {
  color: var(--el);
  font-weight: 700;
}

.ex-arrow {
  color: var(--el);
  font-size: 15px;
  flex-shrink: 0;
}

.ex-illegal {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.ex-illegal-chip {
  font-size: 12px;
  color: var(--vp-c-text-3);
  border: 1px dashed var(--vp-c-divider);
  border-radius: 7px;
  padding: 2px 8px;
}

@media (max-width: 700px) {
  .ex-lineage {
    padding-left: 18px;
    padding-top: 56px;
  }
}
</style>
