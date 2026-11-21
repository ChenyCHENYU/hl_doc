<script setup lang="ts">
import { assetUrl } from "../assets";

const shortcuts = [
  { label: "火任务", query: "火任务" },
  { label: "新山三", query: "新山三" },
  { label: "苦行龟", query: "苦行龟" },
  { label: "天关 53", query: "天关 53" },
];

const routes = [
  { glyph: "火", tone: "fire", category: "五行任务", title: "跟做火属性任务", text: "先查材料和限时事项，再按 19 条火行令逐步完成。", url: "/quests/fire" },
  { glyph: "练", tone: "wood", category: "地图与练级", title: "选一处练级地点", text: "对照新山回廊各层，查坐标、参考防御和带阵风险。", url: "/maps/" },
  { glyph: "飞", tone: "gold", category: "人物成长", title: "查看下一阶飞升", text: "分清人物等级、出征宠物和仙魔两条路线。", url: "/quests/ascension" },
];

const entries = [
  { url: "/pets/", name: "宠物图鉴", detail: "出处、成长与进化" },
  { url: "/items/", name: "物品大全", detail: "用途与 NPC" },
  { url: "/monsters/", name: "天关配装", detail: "关卡和防御参数" },
  { url: "/guide/library/", name: "玩家文库", detail: "攻略原文与旧版资料" },
];

const pets = [
  { id: 118, name: "苦行龟", type: "水", key: "hl/pets/water/d5754277ae.png" },
  { id: 17, name: "雪凤凰", type: "金", key: "hl/pets/metal/893901c3fb.png" },
  { id: 233, name: "霹雳虎", type: "火", key: "hl/pets/fire/e5fa4ecfa0.jpeg" },
];
</script>

<template>
  <main class="portal-home field-ui">
    <div class="portal-shell">
      <section class="portal-hero" aria-labelledby="portal-title">
        <div class="hero-copy">
          <p class="hero-kicker"><span></span> 幻灵游侠 2.5 · 非官方玩家资料站</p>
          <h1 id="portal-title">幻灵宝典<span>.</span></h1>
          <p class="hero-summary">任务怎么做、宠物去哪抓、下一阶怎么飞。玩到哪，就查到哪。</p>
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

      <section class="portal-section" aria-labelledby="route-title">
        <div class="portal-heading">
          <h2 id="route-title">今天要做什么？</h2>
          <a href="/quests/">全部任务攻略 <span aria-hidden="true">↗</span></a>
        </div>
        <div class="route-grid">
          <a v-for="r in routes" :key="r.url" class="route-card" :data-tone="r.tone" :href="r.url">
            <span class="route-glyph" aria-hidden="true">{{ r.glyph }}</span>
            <span class="route-copy"><small>{{ r.category }}</small><strong>{{ r.title }}</strong><span>{{ r.text }}</span></span>
            <span class="route-arrow" aria-hidden="true">↗</span>
          </a>
        </div>
      </section>

      <section class="portal-bottom" aria-label="资料入口和宠物">
        <div>
          <div class="portal-heading"><h2>资料索引</h2></div>
          <div class="portal-index">
            <a v-for="entry in entries" :key="entry.url" :href="entry.url">
              <div><strong>{{ entry.name }}</strong><span>{{ entry.detail }}</span></div>
              <span aria-hidden="true">↗</span>
            </a>
          </div>
        </div>
        <div>
          <div class="portal-heading"><h2>常查宠物</h2><a href="/pets/">全部宠物 <span aria-hidden="true">↗</span></a></div>
          <div class="portal-pets">
            <a v-for="pet in pets" :key="pet.id" :href="`/pets/${pet.id}`">
              <span class="pet-art"><img :src="assetUrl(pet.key)" width="68" height="68" alt="" loading="lazy" @error="($event.target as HTMLElement).hidden = true" /></span>
              <strong>{{ pet.name }}</strong><span>{{ pet.type }}系</span>
            </a>
          </div>
        </div>
      </section>
      <footer class="portal-credit"><span>幻灵宝典 · 玩家整理</span><a href="/about/">资料来源与勘误</a></footer>
    </div>
  </main>
</template>

<style scoped>
.portal-home { background: var(--field-bg); color: var(--field-ink); }
.portal-shell { width: min(1216px, 100% - 96px); margin: auto; }
.portal-hero { display: grid; grid-template-columns: 1.02fr 1fr; align-items: center; gap: clamp(24px, 5vw, 80px); padding: 62px 0 44px; }
.hero-copy, .portal-art { min-width: 0; }
.hero-kicker { display: flex; align-items: center; gap: 9px; color: var(--field-muted); font-size: 13px; font-weight: 650; letter-spacing: .05em; }
.hero-kicker span { width: 7px; height: 7px; background: var(--field-accent); border-radius: 50%; }
.hero-copy h1 { margin: 18px 0 16px; font-family: var(--field-serif); font-size: clamp(55px, 6.6vw, 106px); line-height: 1.04; letter-spacing: -.075em; font-weight: 850; }
.hero-copy h1 span { color: var(--field-accent); margin-left: .06em; }
.hero-summary { margin-bottom: 25px; max-width: 33ch; color: var(--field-muted); font-size: 17px; line-height: 1.72; }
.portal-search { max-width: 510px; }
.portal-suggestions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.portal-suggestions a { padding: 5px 11px; font-size: 13px; font-weight: 600; line-height: 1.65; color: var(--field-accent); background: var(--field-tint); border-radius: 999px; }
.portal-suggestions a:hover { color: var(--field-ink); }
.portal-art { margin: 0; padding: 8px; background: var(--field-paper); border: 1px solid var(--field-line); border-radius: 20px; box-shadow: 0 14px 42px rgb(58 46 22 / 9%); }
.portal-art img { width: 100%; height: auto; aspect-ratio: 740 / 410; display: block; object-fit: cover; border-radius: 13px; }
.portal-art figcaption { padding: 7px 5px 1px; color: var(--field-muted); font-size: 12px; }
.portal-section, .portal-bottom { padding: 26px 0 31px; border-top: 1px solid var(--field-line); }
.portal-heading { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; margin-bottom: 17px; }
.portal-heading h2 { margin: 0; color: var(--field-ink); font-family: var(--field-serif); font-size: clamp(24px, 3vw, 34px); font-weight: 800; line-height: 1.35; }
.portal-heading > a { color: var(--field-accent); font-size: 13px; font-weight: 700; }
.route-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
.route-card { display: flex; align-items: flex-start; gap: 13px; min-width: 0; padding: 18px; border: 1px solid var(--field-line); border-radius: 14px; background: var(--field-paper); }
.route-card:hover, .portal-index a:hover, .portal-pets a:hover { border-color: var(--field-accent); }
.route-card[data-tone="fire"] { --route-color: var(--field-fire); }
.route-card[data-tone="wood"] { --route-color: var(--field-wood); }
.route-card[data-tone="gold"] { --route-color: var(--field-accent); }
.route-glyph { display: grid; place-items: center; flex: 0 0 40px; height: 40px; color: var(--route-color); background: color-mix(in srgb, var(--route-color) 10%, var(--field-paper)); border-radius: 10px; font-family: var(--field-serif); font-size: 21px; font-weight: 800; }
.route-copy { display: grid; gap: 3px; flex: 1; min-width: 0; }
.route-copy small { color: var(--route-color); font-size: 12px; font-weight: 700; }
.route-copy strong { color: var(--field-ink); font-size: 18px; line-height: 1.45; }
.route-copy > span { color: var(--field-muted); font-size: 14px; line-height: 1.65; }
.route-arrow { color: var(--route-color); }
.portal-bottom { display: grid; grid-template-columns: 1.12fr 1fr; gap: 32px; }
.portal-index, .portal-pets { display: grid; gap: 10px; }
.portal-index { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.portal-pets { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.portal-index a, .portal-pets a { background: var(--field-paper); border: 1px solid var(--field-line); border-radius: 12px; }
.portal-index a { display: flex; justify-content: space-between; align-items: center; gap: 5px; padding: 10px 13px; }
.portal-index strong, .portal-index div span { display: block; }
.portal-index div span, .portal-pets a > span:last-child { color: var(--field-muted); font-size: 13px; }
.portal-index a > span { color: var(--field-accent); }
.portal-pets a { display: grid; justify-items: center; text-align: center; padding: 9px 5px; }
.pet-art { display: grid; place-items: center; width: 68px; height: 68px; background: var(--field-tint); border-radius: 12px; margin-bottom: 4px; overflow: hidden; }
.pet-art img { object-fit: contain; }
.portal-credit { display: flex; justify-content: space-between; gap: 12px; border-top: 1px solid var(--field-line); padding: 19px 0 27px; color: var(--field-muted); font-size: 13px; }
.portal-credit a:hover { color: var(--field-accent); }
@media (max-width: 1000px) {
  .portal-shell { width: min(100% - 44px, 920px); }
  .portal-hero { padding-top: 42px; }
  .route-card { padding: 14px; gap: 9px; }
  .route-arrow { display: none; }
}
@media (max-width: 710px) {
  .portal-shell { width: calc(100% - 32px); }
  .portal-hero { grid-template-columns: 1fr; gap: 22px; padding: 32px 0 25px; }
  .hero-copy h1 { font-size: clamp(52px, 13vw, 78px); margin-top: 12px; }
  .hero-summary { margin-bottom: 17px; font-size: 16px; }
  .portal-art img { max-height: 210px; }
  .route-grid, .portal-bottom { grid-template-columns: 1fr; }
  .portal-bottom { gap: 22px; }
  .route-arrow { display: block; }
}
</style>
