<template>
  <div class="premium-home">

    <!-- ===== HERO ===== -->
    <section class="hero-section">
      <div class="hero-mesh" aria-hidden="true"></div>
      <div class="hero-grid" aria-hidden="true"></div>
      <div class="hero-noise" aria-hidden="true"></div>

      <div class="hero-inner">
        <div class="hero-badge">
          <span class="badge-dot"></span>
          <span class="badge-label">幻灵游侠 2.5 · 非官方粉丝资料站</span>
        </div>

        <h1 class="hero-title">
          <span class="title-base">幻灵</span><span class="title-gradient">宝典</span>
        </h1>

        <p class="hero-tagline">把游戏内的宝典、宠物与物品资料线上化、结构化 · 数据提取自 2.5 客户端与玩家整理表格，与官方指南交叉核对</p>

        <div class="hero-cta">
          <a href="/pets/" class="cta-primary">
            <span>宠物图鉴</span>
            <svg class="cta-arrow" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </a>
          <a href="/advanced/" class="cta-secondary">
            <span>养成进阶</span>
          </a>
          <a href="/about/" class="cta-secondary">
            <span>关于本站</span>
          </a>
        </div>

        <a href="/items/" class="hero-eco">
          <span class="eco-star">★</span>
          <span>物品直达 — <strong>{{ itemCount }} 条物品描述</strong>，名称 / 描述 / 出处 NPC 全文检索</span>
          <span class="eco-arrow">→</span>
        </a>
      </div>
    </section>

    <!-- ===== SCENARIOS ===== -->
    <section class="preview-section" style="padding-top:72px;padding-bottom:8px;">
      <div class="preview-inner">
        <header class="section-header reveal-item">
          <div class="section-eyebrow"><span class="eyebrow-line"></span><span>开始之前</span></div>
          <h2 class="section-heading">今天你想玩什么？</h2>
          <p class="section-sub">按玩家旅程组织的三个入口，新手 30 秒找到自己的路线</p>
        </header>
        <div class="scen-grid reveal-item">
          <a href="/quests/ascension" class="scen-card">
            <span class="scen-icon">启</span>
            <div class="scen-body">
              <b>新手开荒 · 从 0 到五转</b>
              <p>建号第一只苦行龟 → 301 级飞散仙 → 武当山飞地仙 → 一路飞到天神/魔尊，全流程一页讲清。</p>
              <span class="scen-tags">飞升全指南 · 称号阶梯 · 投胎规则</span>
            </div>
          </a>
          <a href="/monsters/" class="scen-card">
            <span class="scen-icon">关</span>
            <div class="scen-body">
              <b>天关配装 · 打不过就看表</b>
              <p>82 关怪物、五行、最大攻击与防御需求全量数据，配装前查一眼少走弯路。</p>
              <span class="scen-tags">天关防御参数 · 怪物手册</span>
            </div>
          </a>
          <a href="/pets/" class="scen-card">
            <span class="scen-icon">宠</span>
            <div class="scen-body">
              <b>宠物养成 · 从抓宠到满属性</b>
              <p>333 只宠物档案、32 条进化系谱、重塑价格与 2026 标准属性，附满属性打造三部曲。</p>
              <span class="scen-tags">图鉴 · 系谱 · 满属性攻略</span>
            </div>
          </a>
        </div>
      </div>
    </section>

    <!-- ===== PET PREVIEW ===== -->
    <section class="preview-section">
      <div class="preview-inner">
        <header class="section-header reveal-item">
          <div class="section-eyebrow">
            <span class="eyebrow-line"></span>
            <span>宠物图鉴</span>
          </div>
          <h2 class="section-heading">明星宠物 · 玩家心中的经典</h2>
          <p class="section-sub">霹雳虎 · 裁决精灵 · 考拉熊 · 白骨战士 · 小法师……点击进图鉴看 {{ petCount }} 只宠物全档案（进化链 / 出处 / 重塑价格 / 2026 标准属性）</p>
        </header>

        <div class="preview-grid reveal-item">
          <a
            v-for="p in previewPets"
            :key="p.id"
            href="/pets/"
            class="preview-card"
            :style="{ '--el': elementMeta[p.element]?.color || '#b8860b' }"
          >
            <div class="preview-img" :class="{ 'no-img': !p.image }">
              <span class="preview-glyph">{{ elementMeta[p.element]?.glyph }}</span>
              <img v-if="p.image" :src="petImg(p)" :alt="p.name" loading="lazy" @error="onPreviewError" />
            </div>
            <span class="preview-tier" :class="starTier(p.name)?.cls">{{ starTier(p.name)?.label }}</span>
            <div class="preview-name">{{ p.name }}</div>
            <div class="preview-type">{{ p.type && !/^？+$/.test(p.type) ? p.type : (elementMeta[p.element]?.label || '?') + '属性' }}</div>
          </a>
        </div>
      </div>
    </section>

    <!-- ===== EVOLUTION ===== -->
    <section class="evo-section">
      <div class="evo-inner">
        <header class="section-header reveal-item">
          <div class="section-eyebrow">
            <span class="eyebrow-line"></span>
            <span>宠物进化</span>
          </div>
          <h2 class="section-heading">四级进化体系 · 真实系谱</h2>
          <p class="section-sub">真实系谱数据驱动 · 五行各选一条完整进化链，含非法分支、进化条件与终级目标</p>
        </header>

        <div class="reveal-item"><EvolutionShowcase /></div>

        <div class="evo-links reveal-item">
          深入阅读：
          <a href="/pets/evolutions">进化系谱大全（全部 32 条链路）</a> ·
          <a href="/guide/library/">文库《进化幻化全攻略》</a> ·
          <a href="/advanced/charts">图表《宠物进化表 2026》</a> ·
          <a href="/pets/">全部宠物档案</a>
        </div>
      </div>
    </section>

    <!-- ===== DATA BAND ===== -->
    <section class="band-section">
      <div class="band-inner reveal-item">
        <div class="band-stats">
          <div v-for="stat in stats" :key="stat.label" class="band-stat">
            <b>{{ stat.number }}</b>
            <span>{{ stat.label }}</span>
          </div>
        </div>
        <div class="band-divider"></div>
        <div class="band-pills">
          <a v-for="f in features.filter((x) => x.link)" :key="f.title" :href="f.link" class="pill">{{ f.icon }} {{ f.title }}</a>
        </div>
        <p class="band-copy">
          非官方粉丝资料站 · 数据来源：游戏客户端（2.5）/ 玩家整理表格 / <a href="https://hl.99.com/guide/" target="_blank" rel="noopener noreferrer">官方指南</a> ·
          版权归网龙/天晴数码，异议即撤 · 详见<a href="/about/">关于本站</a>
        </p>
      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { items } from "../../data/items";
import { helpCategories } from "../../data/helpToc";
import codex from "../../data/pet-codex.json";
import library from "../../data/library.json";
import tower from "../../data/tower-defense.json";
import stats2026 from "../../data/pet-stats-2026.json";
import gallery from "../../data/gallery.json";

const itemCount = items.length;
const petCount = codex.length;
const libCount = library.length;
const towerCount = tower.length;
const stat2026Count = stats2026.length;
const galleryCount = gallery.length;

const elementMeta: Record<string, { label: string; glyph: string; color: string }> = {
  metal: { label: "金", glyph: "金", color: "#d4af37" },
  wood: { label: "木", glyph: "木", color: "#5cae7d" },
  water: { label: "水", glyph: "水", color: "#5b9bd5" },
  fire: { label: "火", glyph: "火", color: "#e0664f" },
  earth: { label: "土", glyph: "土", color: "#c4875a" },
  shop: { label: "店", glyph: "店", color: "#b8860b" },
  forge: { label: "锻", glyph: "锻", color: "#97a0b0" },
};

function petImg(p: any): string {
  return import.meta.env.DEV ? `/hl-assets/${p.image.ossKey}` : p.image.url;
}

function onPreviewError(e: Event) {
  const el = e.target as HTMLElement;
  const wrap = el.closest(".preview-img");
  if (wrap) wrap.classList.add("img-failed");
  el.remove();
}

const STAR_PETS = ["霹雳虎", "裁决精灵", "幻晶刚", "冰晶刚", "寿眉", "白骨战士", "小法师", "考拉熊", "白骨魅姬", "斑斑虎"];

const previewPets = (() => {
  const picks: any[] = [];
  for (const name of STAR_PETS) {
    const hit = codex.find((p: any) => p.name === name && p.image);
    if (hit) picks.push(hit);
  }
  if (picks.length < 10) {
    for (const el of ["metal", "water", "earth", "fire", "wood"]) {
      const extra = codex.find((p: any) => p.element === el && p.image && p.type && !/^？+$/.test(p.type) && !picks.includes(p));
      if (extra) picks.push(extra);
    }
  }
  return picks.slice(0, 10);
})();

const STAR_TIERS: Record<string, { label: string; cls: string }> = {
  幻晶刚: { label: "终级", cls: "t-legend" },
  裁决精灵: { label: "终级", cls: "t-legend" },
  冰晶刚: { label: "终级", cls: "t-legend" },
  霹雳虎: { label: "经典", cls: "t-classic" },
  斑斑虎: { label: "经典", cls: "t-classic" },
  白骨战士: { label: "经典", cls: "t-classic" },
  考拉熊: { label: "人气", cls: "t-pop" },
  小法师: { label: "人气", cls: "t-pop" },
  寿眉: { label: "人气", cls: "t-pop" },
  白骨魅姬: { label: "人气", cls: "t-pop" },
};

function starTier(name: string) {
  return STAR_TIERS[name];
}

const stats = [
  { number: petCount, label: "宠物条目" },
  { number: libCount, label: "玩家文库" },
  { number: itemCount, label: "物品条目" },
  { number: towerCount, label: "天关数据" },
  { number: stat2026Count, label: "2026 标准属性" },
  { number: galleryCount, label: "画廊壁纸" },
];

const features = [
  {
    icon: "宠",
    title: "宠物图鉴",
    details: `${petCount} 只宠物按五行分栏，进化链、抓取出处、重塑价格、2026 标准属性一页全查。`,
    link: "/pets/",
  },
  {
    icon: "书",
    title: "宝典指南",
    details: "游戏内 77 页帮助 + 玩家文库 139 篇论坛精华攻略，五大分类全量线上化。",
    link: "/guide/",
  },
  {
    icon: "物",
    title: "物品大全",
    details: `${itemCount} 条物品描述全文检索，名称 / 出处 NPC 一搜即达。`,
    link: "/items/",
  },
  {
    icon: "怪",
    title: "怪物手册",
    details: `天关防御参数 ${towerCount} 关全量表：怪物、五行、最大攻击与防御配装参考。`,
    link: "/monsters/",
  },
  {
    icon: "炼",
    title: "养成进阶",
    details: "满属性打造三部曲、锻造五行相克、招系数排名等 7 张玩法图表与小技巧。",
    link: "/advanced/",
  },
  {
    icon: "任",
    title: "任务攻略",
    details: "水火属性任务、全部飞升流程、2025 新宠终极规则、手机回归指引。",
    link: "/quests/",
  },
  {
    icon: "英",
    title: "幻灵英雄墙",
    details: "玩家风采展示：宠物养成大师、帮派领袖、商人玩家，投稿入驻。",
    link: "/heroes/",
  },
  {
    icon: "库",
    title: "资源库",
    details: "优化资源包全量编目 + 高清壁纸画廊，站内直接浏览。",
    link: "/resources/",
  },
  {
    icon: "图",
    title: "地图导航",
    details: "城市与野外地图索引、传送点说明，规划中。",
  },
];

onMounted(() => {
  const els = document.querySelectorAll('.reveal-item');
  if (!els.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
  );

  els.forEach((el) => observer.observe(el));
});
</script>

<style scoped lang="scss">
@use "./index.scss";
</style>
