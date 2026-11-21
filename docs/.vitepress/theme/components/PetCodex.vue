<script setup lang="ts">
import { computed, ref, watch } from "vue";
import codex from "../../data/pet-codex.json";
import stats2026 from "../../data/pet-stats-2026.json";

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

const filtered = computed(() => {
  const k = keyword.value.trim().toLowerCase();
  return pets.filter((p) => {
    if (activeTab.value !== "all" && p.element !== activeTab.value) return false;
    if (!k) return true;
    return (
      p.name.toLowerCase().includes(k) ||
      p.type.includes(keyword.value.trim()) ||
      p.source.includes(keyword.value.trim()) ||
      p.evolveNormal.includes(keyword.value.trim()) ||
      p.evolveIllegal.includes(keyword.value.trim())
    );
  });
});

const visible = computed(() => filtered.value.slice(0, limit.value));

watch([activeTab, keyword], () => {
  limit.value = 60;
});

function imgUrl(p: PetEntry): string | null {
  if (!p.image) return null;
  return import.meta.env.DEV ? `/hl-assets/${p.image.ossKey}` : p.image.url;
}

function onImgError(e: Event, p: PetEntry) {
  const el = e.target as HTMLElement;
  const wrap = el.closest(".pc-img");
  if (wrap) wrap.classList.add("img-failed");
  el.remove();
}

function typeClass(t: string): string {
  if (t.includes("敏")) return "t-agile";
  if (t.includes("血")) return "t-blood";
  if (t.includes("攻")) return "t-attack";
  if (t.includes("防")) return "t-defense";
  return "t-misc";
}

</script>

<template>
  <div class="pc-wrap">
    <div class="dash-cards">
      <div class="dash-card"><b>{{ pets.length }}</b><span>宠物条目</span></div>
      <div class="dash-card"><b>{{ withImg }}</b><span>图鉴图</span></div>
      <div class="dash-card"><b>{{ withStats }}</b><span>2026 标准属性</span></div>
      <div class="dash-card"><b>{{ withPrice }}</b><span>重塑价格</span></div>
      <div class="dash-card"><b>{{ lineages }}</b><span>进化系谱</span></div>
    </div>

    <div class="pc-toolbar">
      <div class="pc-tabs">
        <button
          v-for="tab in TABS"
          :key="tab.key"
          class="pc-tab"
          :class="{ active: activeTab === tab.key }"
          :style="activeTab === tab.key && tab.key !== 'all' ? { borderColor: ELEMENTS[tab.key]?.color, color: ELEMENTS[tab.key]?.color, background: ELEMENTS[tab.key]?.color + '14' } : {}"
          @click="activeTab = tab.key"
        >
          {{ tab.label }}
        </button>
      </div>
      <input v-model="keyword" class="item-search pc-search" type="search" placeholder="搜索宠物名 / 类型 / 出处 / 进化形态" />
    </div>

    <p class="item-count">
      命中 {{ filtered.length }} 只 / 共收录 {{ pets.length }} 条，当前显示 {{ visible.length }} 条（点卡片看详情）
    </p>

    <div class="pc-grid">
      <a
        v-for="p in visible"
        :key="p.id"
        :href="`/pets/${p.id}`"
        class="pc-card"
        :style="{ '--el': ELEMENTS[p.element]?.color || '#b8860b' }"
      >
        <div class="pc-img" :class="{ 'no-img': !p.image }">
          <span class="pc-el-glyph">{{ ELEMENTS[p.element]?.glyph }}</span>
          <img v-if="p.image" :src="imgUrl(p) || ''" :alt="p.name" loading="lazy" @error="onImgError($event, p)" />
        </div>
        <div class="pc-meta">
          <div class="pc-name">{{ p.name }}</div>
          <span class="pc-type" :class="typeClass(p.type)">{{ p.type && !/^？+$/.test(p.type) ? p.type : "未知" }}</span>
        </div>
        <span v-if="p.price" class="pc-price-flag">重塑</span>
      </a>
    </div>

    <p v-if="filtered.length > limit" class="item-count">
      <a @click.prevent="limit += 60" href="#">加载更多（还剩 {{ filtered.length - limit }} 条）</a>
    </p>
    <p v-else class="item-count">已显示全部结果</p>

  </div>
</template>
