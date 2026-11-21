<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import pets from "../../data/pet-codex.json";
import library from "../../data/library.json";
import tower from "../../data/tower-defense.json";
import { items } from "../../data/items";

type Group = "全部" | "攻略" | "地图" | "宠物" | "物品" | "天关" | "文库";
type Entry = { group: Exclude<Group, "全部">; title: string; url: string; detail: string; aliases?: string; key?: string };
const groups: Group[] = ["全部", "攻略", "地图", "宠物", "物品", "天关", "文库"];

const guideEntries: Entry[] = [
  { group: "攻略", title: "火属性任务", url: "/quests/fire", detail: "14 项准备、19 条火行令，附限时事项与坐标。", aliases: "火任务 火行令 风火令 冰晶 烟火 林捕头的玉佩" },
  { group: "攻略", title: "水属性任务", url: "/quests/water", detail: "水行令路线、苦行龟、超强毒药和兽玉的准备办法。", aliases: "水任务 水行令 风火令" },
  { group: "攻略", title: "仙魔飞升全指南", url: "/quests/ascension", detail: "按称号查下一阶的人物等级、出征宠和飞升条件。", aliases: "一转 二转 三转 四转 五转 过劫 散仙 301级苦行龟" },
  { group: "攻略", title: "进化幻化公式", url: "/quests/formula", detail: "进化、幻化与装备相关的玩家资料。", aliases: "幻化 进化 装备" },
  { group: "攻略", title: "回归指引", url: "/quests/return", detail: "给重新回到幻灵的玩家。", aliases: "回归 新手 手机" },
  { group: "地图", title: "新山练级地点对照", url: "/maps/", detail: "回廊一至三层与清幽古洞，按坐标、怪物和风险查资料。", aliases: "新山城 新山 练级 练满 开荒 防御" },
  { group: "地图", title: "新山一 · 九曲回廊（1）", url: "/maps/#new-mountain-1", detail: "新山一的坐标、怪物和防御参考。", aliases: "新山一 新山1 九曲回廊1" },
  { group: "地图", title: "新山二 · 九曲回廊（2）", url: "/maps/#new-mountain-2", detail: "新山二两处练级点及不同怪组。", aliases: "新山二 新山2 九曲回廊2 4500防 4500点防御" },
  { group: "地图", title: "新山三 · 九曲回廊（3）", url: "/maps/#new-mountain-3", detail: "同一点的两种防御参考、不同坐标与带阵风险。", aliases: "新山三 新山3 九曲回廊3 4500防 4500点防御 4600防 5000防" },
  { group: "地图", title: "新山四 · 清幽古洞", url: "/maps/#new-mountain-4", detail: "古洞练级的防御参考、怪物与版本说明。", aliases: "新山四 新山4 清幽古洞" },
  { group: "地图", title: "玉洁桥 · 冰晶换取点", url: "/maps/#ice-crystal", detail: "常枫坐标、20:00–21:00 时段与冰石前置。", aliases: "玉洁桥 常枫 冰晶 冰石 火行令10" },
];
const catalog: Entry[] = [
  ...guideEntries,
  ...pets.map((pet): Entry => ({
    group: "宠物", title: pet.name, url: `/pets/${pet.id}`,
    detail: [pet.sheet, pet.type, pet.source].filter(Boolean).join(" · ") || "宠物档案",
    aliases: [pet.evolveNormal, pet.note].filter(Boolean).join(" "),
  })),
  ...items.filter((item) => item.name?.trim()).map((item): Entry => ({
    group: "物品", key: `item-${item.id}`, title: item.name.replace(/^※/, ""), url: `/items/?q=${encodeURIComponent(item.name.replace(/^※/, ""))}`,
    detail: item.note || "暂无物品说明", aliases: item.inventer,
  })),
  ...tower.map((row): Entry => ({
    group: "天关", title: `天关 ${row.floor} · ${row.monster}`, url: `/monsters/?floor=${encodeURIComponent(row.floor)}#天关防御参数表`,
    detail: [row.mode, row.element, row.defHuman && `人防参考 ${row.defHuman}`].filter(Boolean).join(" · "),
    aliases: `天关 ${row.floor}关 第${row.floor}关 ${row.monster}`,
  })),
  ...library.map((entry): Entry => ({ group: "文库", title: entry.title, url: `/guide/library/${entry.slug}`, detail: `玩家文库 · ${entry.cat}` })),
];

function normalize(text: string) {
  return text.normalize("NFKC").toLowerCase().replace(/[^\p{Letter}\p{Number}]+/gu, "");
}

const indexed = catalog.map((entry) => ({
  entry,
  title: normalize(entry.title),
  aliases: normalize(entry.aliases ?? ""),
  detail: normalize(entry.detail),
}));

const input = ref("");
const group = ref<Group>("全部");
const expanded = ref(false);
const query = computed(() => input.value.trim());
const matches = computed(() => {
  const term = normalize(query.value);
  if (!term) return guideEntries.filter((entry) => group.value === "全部" || group.value === entry.group);
  return indexed.flatMap(({ entry, title, aliases, detail }) => {
    if (group.value !== "全部" && entry.group !== group.value) return [];
    const score = title === term ? 90 : title.startsWith(term) ? 65 : title.includes(term) ? 50 :
      aliases.includes(term) ? 40 : detail.includes(term) ? 15 : 0;
    return score ? [{ entry, score: score + (entry.group === "文库" ? 0 : 12) }] : [];
  }).sort((a, b) => b.score - a.score).map(({ entry }) => entry);
});

onMounted(() => {
  input.value = new URLSearchParams(window.location.search).get("q") ?? "";
});

function updateSearch() {
  expanded.value = false;
  const url = new URL(window.location.href);
  if (query.value) url.searchParams.set("q", query.value);
  else url.searchParams.delete("q");
  window.history.replaceState(window.history.state, "", url);
}

function filter(value: Group) {
  expanded.value = false;
  group.value = value;
}
</script>

<template>
  <div class="field-ui field-reading ps-search">
    <form class="field-search" action="/search/" role="search" @submit.prevent="updateSearch">
      <input v-model="input" name="q" type="search" aria-label="搜索资料" placeholder="试试：火任务、新山三、苦行龟、天关 53" @input="updateSearch" />
      <button type="submit">搜索</button>
    </form>
    <div class="ps-filters" role="group" aria-label="筛选资料类型">
      <button v-for="g in groups" :key="g" type="button" :aria-pressed="group === g" @click="filter(g)">{{ g }}</button>
    </div>
    <p class="ps-state" role="status">{{ query ? `找到 ${matches.length} 条资料` : "常用查询" }}</p>
    <ul v-if="matches.length" class="ps-results">
      <li v-for="item in (expanded ? matches : matches.slice(0, 20))" :key="item.key ?? item.url + item.title">
        <a :href="item.url">
          <div><span class="ps-kind">{{ item.group }}</span><strong>{{ item.title }}</strong></div>
          <p>{{ item.detail }}</p>
        </a>
      </li>
    </ul>
    <p v-else class="ps-empty">这组里没有找到结果。可以切回「全部」，或试试地图简称、NPC 名和数字关卡。</p>
    <button v-if="!expanded && matches.length > 20" class="ps-more" type="button" @click="expanded = true">显示剩余 {{ matches.length - 20 }} 条</button>
  </div>
</template>

<style scoped>
.ps-search { margin: 24px auto 50px; }
.ps-filters { display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0; }
.ps-filters button, .ps-more { border: 1px solid var(--field-line); padding: 6px 12px; min-height: 36px; border-radius: 8px; color: var(--field-muted); background: var(--field-paper); }
.ps-filters button[aria-pressed="true"] { background: var(--field-action); color: var(--field-action-text); border-color: transparent; }
.ps-state { color: var(--field-muted); font-size: 14px; }
.ps-results { display: grid; gap: 8px; padding: 0; list-style: none; }
.ps-results li { padding: 0; margin: 0; }
.ps-results a { display: block; padding: 11px 15px; color: var(--field-ink); background: var(--field-paper); border: 1px solid var(--field-line); border-radius: 11px; text-decoration: none; }
.ps-results a:hover { border-color: var(--field-accent); }
.ps-results a > div { display: flex; flex-wrap: wrap; align-items: baseline; gap: 9px; }
.ps-results a strong { font-weight: 750; }
.ps-kind { color: var(--field-accent); font-size: 12px; font-weight: 700; }
.ps-results p, .ps-empty { margin: 2px 0 0; color: var(--field-muted); font-size: 14px; overflow-wrap: anywhere; }
</style>
