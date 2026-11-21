<script setup lang="ts">
import { nextTick, ref, shallowRef } from "vue";
import { assetUrl } from "../assets";
import { EVO_ELEMENTS } from "../evolution";
import type PetQuickView from "../components/PetQuickView.vue";
import { data } from "./catalog.data";

const shortcuts = [
  { label: "火任务", query: "火任务" },
  { label: "新山三", query: "新山三" },
  { label: "苦行龟", query: "苦行龟" },
  { label: "天关 53", query: "天关 53" },
];

const routes = [
  { glyph: "火", tone: "fire", title: "火属性任务", text: "查材料、限时事项与火行令路线。", url: "/quests/fire" },
  { glyph: "练", tone: "wood", title: "找练级地点", text: "对照新山各层坐标、怪物与风险。", url: "/maps/" },
  { glyph: "飞", tone: "gold", title: "升仙与入魔", text: "从凡人到五转，查下一阶所需条件。", url: "/quests/ascension" },
  { glyph: "关", tone: "wood", title: "天关配装", text: "按关卡或怪物查看攻击与防御参考。", url: "/monsters/" },
  { glyph: "养", tone: "gold", title: "宠物养成", text: "查询来源、系谱、重塑价格与标准属性。", url: "/pets/" },
  { glyph: "锻", tone: "fire", title: "进阶打造", text: "查满属性实操、五行锻造和招式系数。", url: "/advanced/" },
];

const collections = [
  {
    name: "攻略与养成",
    links: [
      { url: "/guide/", name: "宝典指南", detail: "游戏内帮助与分类目录" },
      { url: "/quests/", name: "任务攻略", detail: "水火任务、飞升、新宠与回归" },
      { url: "/advanced/", name: "养成进阶", detail: "满属性、锻造与玩法图表" },
    ],
  },
  {
    name: "图鉴与查表",
    links: [
      { url: "/pets/", name: "宠物图鉴", detail: "出处、成长与进化" },
      { url: "/pets/prices", name: "重塑价格", detail: "原价、折扣与充值参考" },
      { url: "/items/", name: "物品大全", detail: "用途与出处 NPC" },
      { url: "/maps/", name: "地图与练级", detail: "坐标、怪物与风险" },
      { url: "/monsters/", name: "怪物手册", detail: "天关怪物和防御参数" },
    ],
  },
  {
    name: "文库与收藏",
    links: [
      { url: "/guide/library/", name: "玩家文库", detail: "完整文章与历史攻略" },
      { url: "/resources/", name: "资源库与画廊", detail: "资料包、图片与壁纸" },
      { url: "/heroes/", name: "幻灵英雄墙", detail: "玩家与帮派风采" },
      { url: "/museum/", name: "历史陈列馆", detail: "版本记忆与年代档案" },
    ],
  },
];

const missingArt = ref(new Set<number>());
const featuredIds = data.pets.map(pet => pet.id);
const quickViewComponent = shallowRef<typeof PetQuickView | null>(null);
const quickView = ref<InstanceType<typeof PetQuickView> | null>(null);
const previewIds = ref(featuredIds);
let previewRequest = 0;

async function openPetPreview(event: MouseEvent, id: number, ids: number[]) {
  if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  if (typeof HTMLDialogElement === "undefined" || typeof HTMLDialogElement.prototype.showModal !== "function") return;
  const trigger = event.currentTarget as HTMLAnchorElement;
  event.preventDefault();
  const request = ++previewRequest;
  previewIds.value = ids;
  try {
    quickViewComponent.value ??= (await import("../components/PetQuickView.vue")).default;
    await nextTick();
    if (request === previewRequest) await quickView.value?.open(id, trigger);
  } catch {
    if (request === previewRequest) window.location.assign(trigger.href);
  }
}

function markMissing(id: number) {
  missingArt.value.add(id);
}
function elementLabel(element: string) {
  return EVO_ELEMENTS[element]?.label ?? "宠";
}
</script>

<template>
  <main class="portal-home field-ui">
    <div class="portal-shell">
      <section class="portal-hero" aria-labelledby="portal-title">
        <div class="hero-copy">
          <p class="hero-kicker">幻灵游侠 2.5 · 玩家资料站</p>
          <h1 id="portal-title">幻灵宝典</h1>
          <p class="hero-summary">查任务流程、宠物出处、成长配方和下一阶飞升条件。</p>
          <form class="field-search portal-search" action="/search/" role="search">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" stroke="currentColor" stroke-width="1.8"/><path d="m16 16 4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
            <input name="q" aria-label="查任务、宠物、物品或地图" placeholder="搜任务、宠物、物品或地图" type="search" required />
            <button type="submit">查资料</button>
          </form>
          <div class="portal-suggestions" aria-label="快速查询">
            <a v-for="item in shortcuts" :key="item.query" :href="`/search/?q=${encodeURIComponent(item.query)}`">{{ item.label }}</a>
          </div>
        </div>
        <figure class="portal-art">
          <img src="/hero-bg.png" width="740" height="410" alt="幻灵游侠旧版插画，海岸边的飞毯与码头" fetchpriority="high" />
          <figcaption>《幻灵游侠》旧版插画 · 天晴数码</figcaption>
        </figure>
      </section>

      <dl class="portal-stats" aria-label="站内资料数量">
        <div v-for="stat in data.stats" :key="stat.name">
          <dt><a :href="stat.url">{{ stat.name }}</a></dt>
          <dd>{{ stat.count }}</dd>
        </div>
      </dl>

      <section class="portal-section" aria-labelledby="route-title">
        <div class="portal-heading">
          <h2 id="route-title">今天要做什么？</h2>
          <a href="/quests/">全部任务攻略 <span aria-hidden="true">↗</span></a>
        </div>
        <div class="route-grid">
          <a v-for="r in routes" :key="r.url" class="route-card" :data-tone="r.tone" :href="r.url">
            <span class="route-glyph" aria-hidden="true">{{ r.glyph }}</span>
            <span class="route-copy"><strong>{{ r.title }}</strong><span>{{ r.text }}</span></span>
            <span class="route-arrow" aria-hidden="true">↗</span>
          </a>
        </div>
      </section>

      <section class="portal-section" aria-labelledby="catalog-title">
        <div class="portal-heading">
          <h2 id="catalog-title">资料索引</h2>
          <a href="/guide/catalog">全部栏目 <span aria-hidden="true">↗</span></a>
        </div>
        <div class="collection-grid">
          <section v-for="section in collections" :key="section.name" class="collection">
            <h3>{{ section.name }}</h3>
            <ul>
              <li v-for="entry in section.links" :key="entry.url">
                <a :href="entry.url">
                  <span><strong>{{ entry.name }}</strong><small>{{ entry.detail }}</small></span>
                  <span class="collection-arrow" aria-hidden="true">↗</span>
                </a>
              </li>
            </ul>
          </section>
        </div>
      </section>

      <section class="portal-section portal-pet-section" aria-labelledby="pet-title">
        <div class="portal-heading">
          <h2 id="pet-title">经典宠物</h2>
          <a href="/pets/">全部 {{ data.stats[0].count }} 只宠物 <span aria-hidden="true">↗</span></a>
        </div>
        <ul class="portal-pets">
          <li v-for="pet in data.pets" :key="pet.id">
            <a
              class="vp-raw"
              :href="`/pets/?pet=${pet.id}`"
              :style="{ '--pet-accent': EVO_ELEMENTS[pet.element]?.color }"
              aria-haspopup="dialog"
              @click="openPetPreview($event, pet.id, featuredIds)"
            >
              <span class="pet-art">
                <img v-if="pet.image && !missingArt.has(pet.id)" :src="assetUrl(pet.image)" width="76" height="66" alt="" loading="lazy" @error="markMissing(pet.id)" />
                <b v-else aria-hidden="true">{{ elementLabel(pet.element) }}</b>
              </span>
              <strong>{{ pet.name }}</strong>
              <small>{{ elementLabel(pet.element) }}系</small>
            </a>
          </li>
        </ul>
      </section>

      <section class="portal-section portal-evolution" aria-labelledby="evolution-title">
        <div class="portal-heading">
          <h2 id="evolution-title">五行进化系谱</h2>
          <a href="/pets/evolutions">浏览全部 {{ data.evolutionCount }} 条系谱 <span aria-hidden="true">↗</span></a>
        </div>
        <EvolutionShowcase @preview="openPetPreview" />
      </section>

      <footer class="portal-credit">
        <p>非官方玩家资料站 · 内容整理自游戏客户端、玩家资料表格及<a href="https://hl.99.com/guide/" target="_blank" rel="noopener noreferrer">官方指南</a>。游戏原始素材版权归网龙、天晴数码。</p>
        <a href="/about/">资料来源与勘误</a>
      </footer>
    </div>
    <component :is="quickViewComponent" v-if="quickViewComponent" ref="quickView" :pet-ids="previewIds" />
  </main>
</template>

<style scoped>
.portal-home { color: var(--field-ink); background: var(--field-bg); }
.portal-shell { width: min(1160px, 100% - 64px); margin: auto; }
.portal-hero { display: grid; grid-template-columns: 1.04fr 1fr; align-items: center; gap: clamp(23px, 5vw, 68px); padding: 42px 0 33px; }
.hero-copy, .portal-art { min-width: 0; }
.hero-kicker { margin: 0; color: var(--field-accent); font-size: 13px; font-weight: 650; }
.hero-copy h1 { margin: 11px 0 9px; font-family: var(--field-serif); font-size: clamp(48px, 5.8vw, 81px); line-height: 1.15; letter-spacing: -.035em; font-weight: 800; }
.hero-summary { margin: 0 0 20px; color: var(--field-muted); font-size: 16px; line-height: 1.65; }
.portal-search { max-width: 510px; }
.portal-suggestions { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 12px; }
.portal-suggestions a { padding: 4px 10px; font-size: 13px; color: var(--field-ink); background: var(--field-tint); border-radius: 999px; }
.portal-suggestions a:hover { color: var(--field-accent); }
.portal-art { margin: 0; }
.portal-art img { width: 100%; height: auto; aspect-ratio: 740 / 410; display: block; object-fit: cover; border-radius: 13px; border: 1px solid var(--field-line); }
.portal-art figcaption { margin: 6px 1px 0; color: var(--field-muted); font-size: 12px; }
.portal-stats { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); margin: 0 0 28px; padding: 10px 0; border-block: 1px solid var(--field-line); }
.portal-stats div { display: flex; flex-direction: column-reverse; align-items: center; gap: 2px; padding: 7px 5px; text-align: center; }
.portal-stats div + div { border-inline-start: 1px solid var(--field-line); }
.portal-stats dd { margin: 0; font-size: clamp(21px, 2.5vw, 27px); font-weight: 750; line-height: 1.2; font-variant-numeric: tabular-nums; }
.portal-stats dt { color: var(--field-muted); font-size: 13px; }
.portal-stats dt a:hover { color: var(--field-accent); text-decoration: underline; text-underline-offset: 3px; }
.portal-section { padding: 25px 0 28px; border-bottom: 1px solid var(--field-line); }
.portal-stats + .portal-section { padding-top: 0; }
.portal-heading { display: flex; align-items: baseline; justify-content: space-between; flex-wrap: wrap; gap: 6px 14px; margin-bottom: 14px; }
.portal-heading h2 { margin: 0; color: var(--field-ink); font-family: var(--field-serif); font-size: clamp(23px, 2.6vw, 32px); font-weight: 800; line-height: 1.4; }
.portal-heading > a { color: var(--field-accent); font-size: 13px; font-weight: 700; }
.portal-heading > a:hover { text-decoration: underline; text-underline-offset: 4px; }
.route-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }
.route-card { display: flex; align-items: flex-start; gap: 10px; min-width: 0; padding: 13px; border: 1px solid var(--field-line); border-radius: 10px; background: var(--field-paper); }
.route-card:hover { border-color: var(--field-accent); }
.route-card[data-tone="fire"] { --route-color: var(--field-fire); }
.route-card[data-tone="wood"] { --route-color: var(--field-wood); }
.route-card[data-tone="gold"] { --route-color: var(--field-accent); }
.route-glyph { display: grid; place-items: center; flex: 0 0 36px; height: 36px; color: var(--route-color); background: color-mix(in srgb, var(--route-color) 10%, var(--field-paper)); border-radius: 8px; font-family: var(--field-serif); font-size: 18px; font-weight: 800; }
.route-copy { display: grid; gap: 2px; flex: 1; min-width: 0; }
.route-copy strong, .collection strong { color: var(--field-ink); font-size: 15px; line-height: 1.45; }
.route-copy > span, .collection small { color: var(--field-muted); font-size: 13px; line-height: 1.6; }
.route-arrow, .collection-arrow { color: var(--field-accent); }
.collection-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: clamp(12px, 3vw, 36px); }
.collection h3 { margin: 0; padding: 7px 0; color: var(--field-accent); font-size: 14px; }
.collection ul, .portal-pets { margin: 0; padding: 0; list-style: none; }
.collection li { border-top: 1px solid var(--field-line); }
.collection a { display: flex; align-items: center; justify-content: space-between; gap: 8px; min-height: 53px; padding: 6px 3px; }
.collection a:hover strong { color: var(--field-accent); }
.collection strong, .collection small { display: block; }
.portal-pets { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 8px; }
.portal-pets a { display: grid; grid-template-areas: "art name" "art type"; grid-template-columns: minmax(0, 60px) minmax(0, 1fr); align-items: end; column-gap: 6px; min-height: 75px; padding: 5px 7px; background: var(--field-paper); border: 1px solid var(--field-line); border-radius: 9px; }
.portal-pets a:hover { border-color: var(--field-accent); }
.pet-art { grid-area: art; align-self: center; display: grid; place-items: center; height: 58px; overflow: hidden; }
.pet-art img { width: 100%; height: 100%; object-fit: contain; border-radius: 7px; }
.pet-art b { color: var(--field-accent); padding: 7px; font-family: var(--field-serif); font-size: 18px; border-radius: 7px; background: color-mix(in srgb, var(--pet-accent, var(--field-accent)) 12%, var(--field-paper)); }
.portal-pets strong { grid-area: name; font-size: 13px; line-height: 1.4; overflow-wrap: anywhere; }
.portal-pets small { grid-area: type; align-self: start; color: var(--field-muted); font-size: 12px; }
.portal-credit { display: flex; justify-content: space-between; gap: 14px 26px; padding: 20px 0 28px; color: var(--field-muted); font-size: 13px; line-height: 1.7; }
.portal-credit p { margin: 0; }
.portal-credit > a { flex: none; color: var(--field-accent); }
.portal-credit p a { color: var(--field-accent); }
.portal-credit a:hover { text-decoration: underline; text-underline-offset: 3px; }
@media (max-width: 950px) {
  .portal-shell { width: calc(100% - 38px); }
  .hero-copy h1 { font-size: clamp(43px, 7vw, 63px); }
  .portal-pets { grid-template-columns: repeat(4, minmax(0, 1fr)); }
}
@media (max-width: 680px) {
  .portal-shell { width: calc(100% - 30px); }
  .portal-hero { grid-template-columns: 1fr; gap: 15px; padding: 25px 0 15px; }
  .hero-copy h1 { margin: 7px 0; }
  .hero-summary { margin-bottom: 13px; }
  .portal-art img { max-height: 150px; }
  .portal-stats { grid-template-columns: repeat(3, minmax(0, 1fr)); row-gap: 5px; margin-bottom: 20px; }
  .portal-stats div:nth-child(4) { border-inline-start: 0; }
  .route-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 7px; }
  .route-card { padding: 9px 8px; gap: 6px; }
  .route-glyph { flex-basis: 28px; height: 30px; font-size: 15px; }
  .route-arrow { display: none; }
  .route-copy strong { font-size: 14px; }
  .collection-grid { grid-template-columns: 1fr; }
  .portal-pets { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .portal-pets a { grid-template-columns: minmax(0, 48px) minmax(0, 1fr); min-height: 61px; padding: 3px 4px; }
  .pet-art { height: 48px; }
  .portal-credit { flex-wrap: wrap; }
}
@media (max-width: 354px) {
  .route-grid { grid-template-columns: 1fr; }
  .portal-pets { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
</style>
