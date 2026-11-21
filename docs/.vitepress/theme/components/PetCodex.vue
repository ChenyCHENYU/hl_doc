<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import codex from "../../data/pet-codex.json";
import stats2026 from "../../data/pet-stats-2026.json";
import { assetUrl } from "../assets";
import PetQuickView from "./PetQuickView.vue";

const statByName = new Map((stats2026 as { name: string }[]).map((s) => [s.name, s]));

interface PetEntry {
  id: number;
  name: string;
  sheet: string;
  element: string;
  type: string;
  evolveIllegal: string;
  evolveNormal: string;
  source: string;
  note: string;
  image: { file: string; ossKey: string; url: string } | null;
  price: { sys: string; original: string; discount: string; special: string } | null;
}

const pets = codex as PetEntry[];

const withImg = pets.filter((p) => p.image).length;
const withStats = pets.filter((p) => statByName.has(p.name)).length;
const withPrice = pets.filter((p) => p.price).length;
const evolved = new Set(pets.flatMap((p) => [p.evolveNormal, p.evolveIllegal]).filter(Boolean));
const lineages = pets.filter((p) => p.evolveNormal && !evolved.has(p.name)).length;

const ELEMENTS: Record<string, { label: string; glyph: string; color: string }> = {
  metal: { label: "金", glyph: "金", color: "#d4af37" },
  wood: { label: "木", glyph: "木", color: "#5cae7d" },
  water: { label: "水", glyph: "水", color: "#5b9bd5" },
  fire: { label: "火", glyph: "火", color: "#e0664f" },
  earth: { label: "土", glyph: "土", color: "#c4875a" },
  shop: { label: "店", glyph: "店", color: "#b8860b" },
  forge: { label: "锻", glyph: "锻", color: "#97a0b0" },
};

const TABS = [
  { key: "all", label: "全部" },
  { key: "metal", label: "金属性" },
  { key: "wood", label: "木属性" },
  { key: "water", label: "水属性" },
  { key: "fire", label: "火属性" },
  { key: "earth", label: "土属性" },
  { key: "shop", label: "新山宠店" },
  { key: "forge", label: "锻造" },
];

const activeTab = ref("all");
const keyword = ref("");
const limit = ref(60);
const quickView = ref<InstanceType<typeof PetQuickView> | null>(null);
const failedImages = ref(new Set<number>());

const filtered = computed(() => {
  const k = keyword.value.trim().normalize("NFKC").toLowerCase();
  return pets.filter((p) => {
    if (activeTab.value !== "all" && p.element !== activeTab.value) return false;
    if (!k) return true;
    return [p.name, p.type, p.source, p.evolveNormal, p.evolveIllegal]
      .some((value) => value?.normalize("NFKC").toLowerCase().includes(k));
  });
});

const visible = computed(() => filtered.value.slice(0, limit.value));
const orderedPetIds = computed(() => filtered.value.map((pet) => pet.id));

watch([activeTab, keyword], () => {
  limit.value = 60;
});

function imgUrl(p: PetEntry): string {
  if (!p.image || failedImages.value.has(p.id)) return "";
  return import.meta.env.DEV ? assetUrl(p.image.ossKey) : p.image.url;
}

onMounted(() => {
  const id = new URLSearchParams(window.location.search).get("pet");
  if (id) void quickView.value?.open(Number(id));
});

function clearLinkPreview() {
  const url = new URL(window.location.href);
  if (!url.searchParams.has("pet")) return;
  url.searchParams.delete("pet");
  window.history.replaceState(window.history.state, "", url);
}
</script>

<template>
  <div class="pet-codex">
    <div class="codex-overview">
      <div class="codex-overview-main"><b>{{ pets.length }}</b> 宠物条目</div>
      <div class="codex-counts">
        <span>图鉴图 <b>{{ withImg }}</b></span>
        <span>2026 属性 <b>{{ withStats }}</b></span>
        <a href="/pets/prices">重塑价格 <b>{{ withPrice }}</b></a>
        <a href="/pets/evolutions">进化系谱 <b>{{ lineages }}</b></a>
      </div>
    </div>

    <div class="codex-tools">
      <div class="codex-tabs" role="group" aria-label="按属性筛选">
        <button
          v-for="tab in TABS"
          :key="tab.key"
          type="button"
          :aria-pressed="activeTab === tab.key"
          @click="activeTab = tab.key"
        >
          {{ tab.label }}
        </button>
      </div>
      <input v-model="keyword" type="search" aria-label="搜索宠物" placeholder="宠物名、类型、出处或进化形态" />
    </div>

    <p class="codex-result" aria-live="polite">
      找到 {{ filtered.length }} 条，显示 {{ visible.length }} 条
    </p>

    <div v-if="visible.length" class="codex-cards">
      <a
        v-for="p in visible"
        :key="p.id"
        :href="`/pets/${p.id}`"
        class="codex-card vp-raw"
        :style="{ '--pet-color': ELEMENTS[p.element]?.color || '#b8860b' }"
        :aria-label="`查看${p.name}详情`"
        aria-haspopup="dialog"
        @click="quickView?.openFromLink($event, p.id)"
      >
        <div class="codex-card-art">
          <img v-if="imgUrl(p)" :src="imgUrl(p)" alt="" loading="lazy" @error="failedImages.add(p.id)" />
          <span v-else aria-hidden="true">{{ ELEMENTS[p.element]?.glyph || "宠" }}</span>
        </div>
        <div class="codex-card-info">
          <strong>{{ p.name }}</strong>
          <span>{{ p.type && !/^？+$/.test(p.type) ? p.type : "类型待补" }}</span>
        </div>
        <span v-if="p.price" class="codex-card-price">可重塑</span>
      </a>
    </div>
    <p v-else class="codex-empty">没有匹配的宠物，试试切换属性或调整关键词。</p>

    <p v-if="filtered.length > limit" class="codex-more">
      <button type="button" @click="limit += 60">加载更多（还剩 {{ filtered.length - limit }} 条）</button>
    </p>

    <PetQuickView ref="quickView" :pet-ids="orderedPetIds" @close="clearLinkPreview" />
  </div>
</template>

<style scoped>
.pet-codex {
  color: var(--field-ink);
}
.pet-codex a, .pet-codex button { transition: border-color .15s ease, background-color .15s ease, color .15s ease; }
.pet-codex :is(a, button, input):focus-visible { outline: 2px solid var(--field-accent); outline-offset: 3px; }
.codex-overview { display: flex; align-items: baseline; flex-wrap: wrap; gap: 8px 24px; padding: 13px 16px; background: var(--field-tint); border: 1px solid var(--field-line); border-radius: 12px; }
.codex-overview-main { font-size: 14px; color: var(--field-muted); }
.codex-overview-main b { color: var(--field-ink); font-size: 20px; margin-right: 4px; }
.codex-counts { display: flex; flex-wrap: wrap; gap: 3px 16px; font-size: 13px; color: var(--field-muted); }
.codex-counts b { font-variant-numeric: tabular-nums; }
.codex-counts a { color: var(--field-accent); }
.codex-tools { display: grid; gap: 10px; margin-top: 16px; }
.codex-tabs { display: flex; flex-wrap: wrap; gap: 6px; }
.codex-tabs button, .codex-more button { min-height: 36px; padding: 4px 11px; border: 1px solid var(--field-line); border-radius: 8px; background: var(--field-paper); color: var(--field-muted); font-size: 14px; font-weight: 600; }
.codex-tabs button[aria-pressed="true"] { background: var(--field-action); border-color: var(--field-action); color: var(--field-action-text); }
.codex-tabs button:hover, .codex-more button:hover { border-color: var(--field-accent); }
.codex-tools input { padding: 8px 12px; min-height: 43px; width: min(100%, 390px); border: 1px solid var(--field-line); border-radius: 9px; background: var(--field-paper); color: var(--field-ink); font-size: 16px; }
.codex-tools input::placeholder { color: var(--field-muted); opacity: 1; }
.pet-codex .codex-result { margin: 10px 0; color: var(--field-muted); font-size: 13px; }
.codex-cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 146px), 1fr)); gap: 10px; }
.codex-cards a.codex-card { display: flex; flex-direction: column; position: relative; min-width: 0; border: 1px solid var(--field-line); border-radius: 12px; background: var(--field-paper); padding: 7px; text-decoration: none; }
.codex-cards a.codex-card:hover { border-color: var(--field-accent); }
.codex-card-art { display: grid; place-items: center; min-height: 68px; aspect-ratio: 1.6; border-radius: 7px; background: color-mix(in srgb, var(--pet-color) 8%, #fcfaf4); overflow: hidden; }
.codex-card-art img { height: 100%; max-height: 100px; width: 100%; object-fit: contain; image-rendering: pixelated; padding: 7px; }
.codex-card-art > span { color: #514d3f; font-family: var(--field-serif); font-size: 28px; font-weight: 700; }
.codex-card-info { display: grid; gap: 1px; padding: 7px 4px 3px; }
.codex-card-info strong { color: var(--field-ink); font-size: 15px; line-height: 1.35; overflow-wrap: anywhere; }
.codex-card-info > span { color: var(--field-muted); font-size: 12px; line-height: 1.55; }
.codex-card-price { align-self: flex-start; margin: auto 4px 2px; color: var(--field-accent); font-size: 11px; }
.codex-more { text-align: center; }
.codex-empty { color: var(--field-muted); }
@media (max-width: 600px) {
  .codex-cards { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }
}
</style>
