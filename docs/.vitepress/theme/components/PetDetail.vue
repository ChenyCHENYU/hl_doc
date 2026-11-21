<script setup lang="ts">
import { computed } from "vue";
import { useData } from "vitepress";
import codex from "../../data/pet-codex.json";
import stats2026 from "../../data/pet-stats-2026.json";
import library from "../../data/library.json";
import { evoImgUrl, EVO_ELEMENTS } from "../evolution";

const { params } = useData();
const pet = computed(
  () => (codex as any[]).find((p) => String(p.id) === String(params.value.id)) ?? null
);

const EL = EVO_ELEMENTS;

const lineage = computed(() => {
  if (!pet.value?.evolveNormal && !isTarget(pet.value)) return [pet.value];
  const chain = [];
  let root = pet.value;
  const names = new Set<string>();
  const byName = new Map((codex as any[]).map((p) => [p.name, p]));
  while (true) {
    const prev = (codex as any[]).find(
      (p) => (p.evolveNormal === root.name || p.evolveIllegal === root.name) && !names.has(p.name)
    );
    if (!prev || names.has(prev.name)) break;
    root = prev;
    names.add(prev.name);
  }
  let cur: any = root;
  const seen = new Set<string>();
  while (cur && !seen.has(cur.name)) {
    chain.push(cur);
    seen.add(cur.name);
    cur = cur.evolveNormal ? byName.get(cur.evolveNormal) : null;
  }
  return chain;
});

function isTarget(p: any): boolean {
  return (codex as any[]).some((q) => q.evolveNormal === p?.name || q.evolveIllegal === p?.name);
}

const statMap = new Map<string, any>((stats2026 as any[]).map((s) => [s.name, s]));
const stat = computed(() => (pet.value?.name ? statMap.get(pet.value.name) : null));

const dist = computed<number[]>(() => {
  if (!stat.value) return [];
  const m = (stat.value.dist as string).match(/(\d+)%/g);
  return m ? m.map((x) => parseInt(x)) : [];
});

const related = computed(() => {
  if (!pet.value) return [];
  return (library as any[])
    .filter((e) => e.title.includes(pet.value.name) || (pet.value.evolveNormal && e.title.includes(pet.value.evolveNormal)))
    .slice(0, 4);
});

function tierLabel(i: number, len: number): string {
  if (i === len - 1) return "终级";
  return `${["一", "二", "三", "四"][i] ?? i + 1}级`;
}

function onImgError(e: Event) {
  const el = e.target as HTMLElement;
  el.closest(".pd-img")?.classList.add("img-failed");
  el.remove();
}

const R = 50;
const CENTER = 66;
function pt(i: number, n: number, r: number): [number, number] {
  const a = (Math.PI * 2 * i) / n - Math.PI / 2;
  return [CENTER + Math.cos(a) * r, CENTER + Math.sin(a) * r];
}
const poly = computed(() =>
  dist.value.map((v, i) => pt(i, dist.value.length, (v / 100) * R).join(",")).join(" ")
);
const gridPoly = computed(() =>
  dist.value.map((_, i) => pt(i, dist.value.length, R).join(",")).join(" ")
);

// ── 五维雷达：攻 / 防 / 敏 / 血 / 成长（按 2026 全表每轴最大值归一）──
const AXES = ["攻", "防", "敏", "血", "成"];
function parseAttrs(s: any): number[] {
  const fields = [s.atk, s.def, s.agi, s.hp];
  if (fields.some((value) => value == null || value === "")) return [];
  const values = fields.map(Number);
  return values.every(Number.isFinite) ? values : [];
}
function parseGrowth(s: any): number | null {
  if (s.growth3 == null || s.growth3 === "") return null;
  const growth = Number(s.growth3);
  return Number.isFinite(growth) ? growth : null;
}
const radarMax = (() => {
  const mx = [0, 0, 0, 0, 0];
  for (const s of stats2026 as any[]) {
    const a = parseAttrs(s);
    const growth = parseGrowth(s);
    if (a.length < 4 || growth == null) continue;
    const vals = [...a, growth];
    vals.forEach((v, i) => {
      if (Number.isFinite(v) && v > mx[i]) mx[i] = v;
    });
  }
  return mx;
})();
const radarVals = computed<number[]>(() => {
  if (!stat.value) return [];
  const a = parseAttrs(stat.value);
  const growth = parseGrowth(stat.value);
  if (a.length < 4 || growth == null) return [];
  return [...a, growth];
});
const radarPoly = computed(() =>
  radarVals.value
    .map((v, i) => pt(i, 5, Math.min(1, v / (radarMax[i] || 1)) * R).join(","))
    .join(" ")
);
const radarGrid = computed(() => AXES.map((_, i) => pt(i, 5, R).join(",")).join(" "));
const radarLabels = computed(() =>
  AXES.map((ax, i) => {
    const [x, y] = pt(i, 5, R + 12);
    return { ax, x: +x.toFixed(1), y: +y.toFixed(1) };
  })
);
</script>

<template>
  <div v-if="pet" class="pd">
    <div class="pd-crumb">
      <a href="/pets/">宠物图鉴</a><span>/</span>
      <a href="/pets/">{{ EL[pet.element]?.label }}系</a><span>/</span>
      <b>{{ pet.name }}</b>
    </div>

    <div class="pd-head">
      <div class="pd-img" :style="{ '--el': EL[pet.element]?.color }">
        <span class="pd-glyph">{{ EL[pet.element]?.label }}</span>
        <img v-if="pet.image" :src="evoImgUrl(pet)" :alt="pet.name" @error="onImgError" />
      </div>
      <div class="pd-main">
        <h1 class="pd-name">{{ pet.name }}</h1>
        <div class="pd-badges">
          <span class="pd-badge" :style="{ color: EL[pet.element]?.color, borderColor: EL[pet.element]?.color }">{{ pet.sheet }}</span>
          <span class="pd-badge type">{{ pet.type && !/^？+$/.test(pet.type) ? pet.type : "未知" }}</span>
        </div>

        <div v-if="stat" class="pd-2026">
          <div class="pd-2026-title">2026 标准属性</div>
          <div class="pd-2026-body">
            <svg v-if="radarVals.length === 5" class="pd-radar" viewBox="0 0 132 132">
              <polygon :points="radarGrid" class="pd-radar-grid" />
              <polygon :points="radarPoly" class="pd-radar-fill" />
              <circle cx="66" cy="66" r="50" class="pd-radar-ring" />
              <text v-for="l in radarLabels" :key="l.ax" :x="l.x" :y="l.y" class="pd-radar-label">{{ l.ax }}</text>
            </svg>
            <svg v-else-if="dist.length >= 3" class="pd-radar" viewBox="0 0 132 132">
              <polygon :points="gridPoly" class="pd-radar-grid" />
              <polygon :points="poly" class="pd-radar-fill" />
              <circle cx="66" cy="66" r="50" class="pd-radar-ring" />
            </svg>
            <div class="pd-2026-rows">
              <div v-if="stat.hp"><b>一级属性</b><span>攻 {{ stat.atk }} / 防 {{ stat.def }} / 敏 {{ stat.agi }} / 血 {{ stat.hp }}</span></div>
              <div v-else><b>一级属性</b><span>原始表格待复核</span></div>
              <div v-if="stat.hp"><b>生长率</b><span>三围 {{ stat.growth3 }} · 生命 {{ stat.growthHp }}</span></div>
              <div><b>分配比例</b><span>{{ stat.dist }}</span></div>
              <div><b>分类</b><span>{{ stat.group }} · {{ stat.type }}</span></div>
            </div>
          </div>
        </div>

        <div v-if="pet.price" class="pd-price">
          <b>重塑特惠</b><span class="pd-price-num">{{ pet.price.special }}</span><span>灵石（原价 {{ pet.price.original }} · 折扣 {{ pet.price.discount }}）</span>
        </div>
      </div>
    </div>

    <div class="pd-sec">
      <h2>进化系谱</h2>
      <div class="pd-chain">
        <template v-for="(p, i) in lineage" :key="p.id">
          <a :href="`/pets/${p.id}`" class="pd-chain-node" :class="{ me: p.id === pet.id }">
            <img v-if="p.image" :src="evoImgUrl(p)!" alt="" />
            <span v-else class="pd-chain-glyph">{{ EL[p.element]?.label }}</span>
            <i>{{ p.name }}</i>
            <em>{{ tierLabel(i, lineage.length) }}</em>
          </a>
          <span v-if="i < lineage.length - 1" class="pd-chain-arrow">&#10142;</span>
        </template>
        <a href="/pets/evolutions" class="pd-chain-more">全部系谱 &#8250;</a>
      </div>
      <p v-if="pet.evolveIllegal" class="pd-illegal">非法进化分支 → <b>{{ pet.evolveIllegal }}</b></p>
    </div>

    <div class="pd-sec">
      <h2>详细资料</h2>
      <div class="pd-rows">
        <div class="pd-row"><span>抓取出处</span><p>{{ pet.source || "暂无可靠出处" }}</p></div>
        <div v-if="pet.note" class="pd-row"><span>备注</span><p>{{ pet.note }}</p></div>
      </div>
    </div>

    <div v-if="related.length" class="pd-sec">
      <h2>出现在这些攻略里</h2>
      <div class="pd-related">
        <a v-for="r in related" :key="r.slug" :href="`/guide/library/${r.slug}`" class="pd-rel-card">
          <b>{{ r.title }}</b><span>{{ r.cat }}</span>
        </a>
      </div>
    </div>
  </div>
  <div v-else>
    <p>未找到该宠物，<a href="/pets/">返回图鉴</a>。</p>
  </div>
</template>

<style scoped>
.pd {
  margin: 18px 0 32px;
}

.pd-crumb {
  display: flex;
  gap: 8px;
  font-size: 13px;
  color: var(--vp-c-text-3);
  margin-bottom: 18px;
}

.pd-crumb a {
  color: var(--vp-c-brand-1);
  text-decoration: none;
}

.pd-crumb b {
  color: var(--vp-c-text-1);
}

.pd-head {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 24px;
  margin-bottom: 28px;
}

.pd-img {
  position: relative;
  aspect-ratio: 1;
  border-radius: 16px;
  border: 1.5px solid color-mix(in srgb, var(--el) 55%, transparent);
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 18px 44px -16px color-mix(in srgb, var(--el) 45%, transparent);
  overflow: hidden;
}

.dark .pd-img {
  background: #f7f5f0;
}

.pd-img img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 18px;
  image-rendering: pixelated;
}

.pd-glyph {
  display: none;
  font-size: 80px;
  font-weight: 800;
  color: color-mix(in srgb, var(--el) 60%, var(--vp-c-text-3));
}

.pd-img.img-failed .pd-glyph,
.pd-img:not(:has(img)) .pd-glyph {
  display: block;
}

.pd-name {
  margin: 0 0 10px;
  font-size: 34px;
  font-weight: 800;
  color: var(--vp-c-text-1);
}

.pd-badges {
  display: flex;
  gap: 8px;
  margin-bottom: 18px;
}

.pd-badge {
  font-size: 12px;
  font-weight: 600;
  border: 1px solid;
  border-radius: 999px;
  padding: 2px 12px;
}

.pd-badge.type {
  color: var(--vp-c-text-2);
  border-color: var(--vp-c-divider);
}

.pd-2026 {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  padding: 14px 16px;
  margin-bottom: 14px;
}

.pd-2026-title {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: var(--vp-c-text-3);
  margin-bottom: 10px;
}

.pd-2026-body {
  display: flex;
  gap: 18px;
  align-items: center;
}

.pd-radar {
  width: 132px;
  height: 132px;
  flex-shrink: 0;
}

.pd-radar-ring {
  fill: none;
  stroke: var(--vp-c-divider);
}

.pd-radar-label {
  font-size: 10px;
  font-weight: 700;
  fill: var(--vp-c-text-2);
  text-anchor: middle;
  dominant-baseline: middle;
}

.pd-radar-grid {
  fill: none;
  stroke: var(--vp-c-divider);
  stroke-dasharray: 3 3;
}

.pd-radar-fill {
  fill: rgba(184, 134, 11, 0.25);
  stroke: var(--vp-c-brand-1);
  stroke-width: 1.5;
  transform-origin: 66px 66px;
  animation: hl-radar-in 0.7s cubic-bezier(0.34, 1.4, 0.44, 1) both;
}

.pd-radar-label {
  animation: hl-fade-up 0.5s ease both;
}

.pd-radar-label:nth-of-type(1) { animation-delay: 0.25s; }
.pd-radar-label:nth-of-type(2) { animation-delay: 0.32s; }
.pd-radar-label:nth-of-type(3) { animation-delay: 0.39s; }
.pd-radar-label:nth-of-type(4) { animation-delay: 0.46s; }
.pd-radar-label:nth-of-type(5) { animation-delay: 0.53s; }

@media (prefers-reduced-motion: reduce) {
  .pd-radar-fill, .pd-radar-label { animation: none; }
}

.pd-2026-rows {
  display: grid;
  gap: 6px;
  font-size: 13px;
}

.pd-2026-rows div {
  display: flex;
  gap: 10px;
}

.pd-2026-rows b {
  color: var(--vp-c-text-3);
  width: 4.5em;
  flex-shrink: 0;
}

.pd-2026-rows span {
  color: var(--vp-c-text-2);
  font-variant-numeric: tabular-nums;
}

.pd-price {
  display: flex;
  align-items: baseline;
  gap: 10px;
  border: 1px solid var(--vp-c-brand-soft);
  background: var(--vp-c-brand-soft);
  border-radius: 10px;
  padding: 10px 16px;
  font-size: 13px;
  color: var(--vp-c-text-2);
}

.pd-price b {
  color: var(--vp-c-brand-1);
}

.pd-price-num {
  font-size: 20px;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  font-variant-numeric: tabular-nums;
}

.pd-sec h2 {
  font-size: 18px;
  font-weight: 700;
  color: var(--vp-c-text-1);
  margin: 26px 0 12px;
}

.pd-chain {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.pd-chain-node {
  width: 88px;
  border-radius: 10px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
  text-decoration: none;
  overflow: hidden;
  transition: transform 0.15s, border-color 0.15s;
}

.pd-chain-node:hover {
  transform: translateY(-2px);
}

.pd-chain-node.me {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 0 0 1px var(--vp-c-brand-soft);
}

.pd-chain-node img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: contain;
  background: #fff;
  padding: 5px;
  image-rendering: pixelated;
  display: block;
}

.pd-chain-glyph {
  display: block;
  text-align: center;
  padding: 24px 0;
  font-size: 22px;
  font-weight: 800;
  color: var(--vp-c-text-3);
}

.pd-chain-node i {
  display: block;
  text-align: center;
  font-style: normal;
  font-size: 12px;
  font-weight: 700;
  color: var(--vp-c-text-1);
  padding-top: 4px;
}

.pd-chain-node em {
  display: block;
  text-align: center;
  font-style: normal;
  font-size: 12px;
  color: var(--vp-c-text-3);
  padding-bottom: 6px;
}

.pd-chain-node.me em {
  color: var(--vp-c-brand-1);
  font-weight: 700;
}

.pd-chain-arrow {
  color: var(--vp-c-brand-1);
}

.pd-chain-more {
  font-size: 12.5px;
  color: var(--vp-c-brand-1);
  text-decoration: none;
  margin-left: 6px;
}

.pd-illegal {
  margin: 10px 0 0;
  font-size: 12.5px;
  color: var(--vp-c-text-3);
}

.pd-illegal b {
  color: var(--vp-c-text-2);
}

.pd-rows {
  display: grid;
  gap: 10px;
}

.pd-row {
  display: grid;
  grid-template-columns: 5em 1fr;
  gap: 10px;
  font-size: 14px;
  line-height: 1.8;
}

.pd-row span {
  font-weight: 700;
  color: var(--vp-c-brand-1);
}

.pd-row p {
  margin: 0;
  color: var(--vp-c-text-2);
}

.pd-related {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 10px;
}

.pd-rel-card {
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  padding: 12px 14px;
  text-decoration: none;
  background: var(--vp-c-bg-soft);
  transition: border-color 0.15s, transform 0.15s;
}

.pd-rel-card:hover {
  border-color: rgba(184, 134, 11, 0.45);
  transform: translateY(-2px);
}

.pd-rel-card b {
  display: block;
  font-size: 13px;
  color: var(--vp-c-text-1);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pd-rel-card span {
  font-size: 12px;
  color: var(--vp-c-text-3);
}

@media (max-width: 760px) {
  .pd-head {
    grid-template-columns: 1fr;
  }

  .pd-img {
    max-width: 240px;
  }

  /* 雷达 + 属性行竖排，避免 132px 雷达把属性行挤出视口 */
  .pd-2026-body {
    flex-direction: column;
    align-items: flex-start;
  }
}

/* 网格 1fr 列默认 min-width:auto，长名字/徽章会把 .pd-main 顶出容器（移动端 4px 溢出） */
.pd-main {
  min-width: 0;
}

.pd-name {
  overflow-wrap: anywhere;
}
</style>
