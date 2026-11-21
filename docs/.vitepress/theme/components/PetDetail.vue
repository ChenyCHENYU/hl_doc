<script setup lang="ts">
import { computed, ref } from "vue";
import { useData } from "vitepress";
import codex from "../../data/pet-codex.json";
import stats2026 from "../../data/pet-stats-2026.json";
import library from "../../data/library.json";
import { formatPetPriceYuan, readPetPrice } from "../../data/pet-price-format";
import { evoImgUrl, EVO_ELEMENTS } from "../evolution";

const props = defineProps<{ id?: string | number; inDialog?: boolean }>();
const emit = defineEmits<{ select: [id: number] }>();
const { params } = useData();
const pet = computed(
  () => (codex as any[]).find((p) => String(p.id) === String(props.id ?? params.value.id)) ?? null
);

const EL = EVO_ELEMENTS;
const price = computed(() => pet.value?.price ?? null);
const discount = computed(() => {
  const value = readPetPrice(price.value?.discount);
  return value != null && value <= 1
    ? `${Number((value * 10).toFixed(2))} 折`
    : price.value?.discount || "—";
});

const lineage = computed(() => {
  if (!pet.value) return [];
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

const failedImages = ref(new Set<number>());
function displayImage(p: (typeof codex)[number]) {
  return failedImages.value.has(p.id) ? null : evoImgUrl(p);
}

function selectChainPet(event: MouseEvent, id: number) {
  if (!props.inDialog || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  event.preventDefault();
  emit("select", id);
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
  <div v-if="pet" class="pd" :class="{ 'pd--dialog': inDialog }">
    <div v-if="!inDialog" class="pd-crumb">
      <a href="/pets/">宠物图鉴</a><span>/</span>
      <a href="/pets/">{{ EL[pet.element]?.label }}系</a><span>/</span>
      <b>{{ pet.name }}</b>
    </div>

    <div class="pd-head">
      <div class="pd-img" :style="{ '--el': EL[pet.element]?.color || 'var(--field-accent)' }">
        <img v-if="displayImage(pet)" :key="pet.id" :src="displayImage(pet)!" :alt="pet.name" @error="failedImages.add(pet.id)" />
        <span v-else class="pd-glyph" aria-hidden="true">{{ EL[pet.element]?.label || '宠' }}</span>
      </div>
      <div class="pd-main">
        <h1 v-if="!inDialog" class="pd-name">{{ pet.name }}</h1>
        <div class="pd-badges">
          <span v-if="!inDialog" class="pd-badge">{{ pet.sheet }}</span>
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

        <div v-if="price" class="pd-price">
          <div class="pd-price-stones">
            <div><b>重塑特惠</b> <strong>{{ price.special || "—" }}</strong> 灵石</div>
            <span>原价 {{ price.original || "—" }} 灵石 · {{ discount }}</span>
          </div>
          <div v-if="readPetPrice(price.charge50) != null || readPetPrice(price.charge10) != null" class="pd-price-reference">
            <span>旧表人民币参考</span>
            <span>50 元档 {{ formatPetPriceYuan(price.charge50) }}</span>
            <span>10 元档 {{ formatPetPriceYuan(price.charge10) }}</span>
            <a href="/pets/prices">看换算说明</a>
          </div>
        </div>
      </div>
    </div>

    <div class="pd-sec">
      <component :is="inDialog ? 'h3' : 'h2'">进化系谱</component>
      <div class="pd-chain">
        <template v-for="(p, i) in lineage" :key="p.id">
          <a :href="`/pets/${p.id}`" class="pd-chain-node" :class="{ me: p.id === pet.id, 'vp-raw': inDialog }" :aria-current="p.id === pet.id ? 'true' : undefined" @click="selectChainPet($event, p.id)">
            <img v-if="displayImage(p)" :src="displayImage(p)!" alt="" loading="lazy" @error="failedImages.add(p.id)" />
            <span v-else class="pd-chain-glyph">{{ EL[p.element]?.label || '宠' }}</span>
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
      <component :is="inDialog ? 'h3' : 'h2'">详细资料</component>
      <div class="pd-rows">
        <div class="pd-row"><span>抓取出处</span><p>{{ pet.source || "暂无可靠出处" }}</p></div>
        <div v-if="pet.note" class="pd-row"><span>备注</span><p>{{ pet.note }}</p></div>
      </div>
    </div>

    <div v-if="related.length" class="pd-sec">
      <component :is="inDialog ? 'h3' : 'h2'">出现在这些攻略里</component>
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

.pd--dialog {
  margin: 0 0 18px;
  font-size: 14px;
  line-height: 1.6;
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
  grid-template-columns: minmax(150px, 225px) minmax(0, 1fr);
  align-items: start;
  gap: 24px;
  margin-bottom: 28px;
}

.pd--dialog .pd-head { grid-template-columns: minmax(110px, 156px) minmax(0, 1fr); gap: 16px; margin-bottom: 14px; }
.pd--dialog .pd-badges { margin-bottom: 8px; }

.pd-img {
  position: relative;
  aspect-ratio: 1;
  border-radius: 16px;
  border: 1.5px solid color-mix(in srgb, var(--el) 55%, transparent);
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
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
  font-size: 80px;
  font-weight: 800;
  color: color-mix(in srgb, var(--el) 60%, var(--vp-c-text-3));
}

.pd-name {
  margin: 0 0 10px;
  font-size: 34px;
  font-weight: 800;
  color: var(--vp-c-text-1);
}

.pd-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 18px;
}

.pd-badge {
  font-size: 12px;
  font-weight: 600;
  border: 1px solid;
  border-radius: 999px;
  padding: 2px 12px;
  color: var(--field-accent);
  border-color: var(--field-line);
}

.pd-badge.type {
  color: var(--vp-c-text-2);
  border-color: var(--vp-c-divider);
}

.pd-2026 {
  border: 1px solid var(--field-line);
  border-radius: 12px;
  background: var(--field-paper);
  padding: 14px 16px;
  margin-bottom: 14px;
}

.pd-2026-title {
  font-size: 12px;
  font-weight: 700;
  color: var(--field-muted);
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
  stroke: var(--field-line);
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
  stroke: var(--field-line);
  stroke-dasharray: 3 3;
}

.pd-radar-fill {
  fill: color-mix(in srgb, var(--field-accent) 20%, transparent);
  stroke: var(--field-accent);
  stroke-width: 1.5;
}

.pd-2026-rows {
  display: grid;
  min-width: 0;
  gap: 6px;
  font-size: 13px;
}

.pd-2026-rows div {
  display: flex;
  gap: 10px;
}

.pd-2026-rows b {
  color: var(--field-muted);
  width: 4.5em;
  flex-shrink: 0;
}

.pd-2026-rows span {
  color: var(--field-ink);
  overflow-wrap: anywhere;
  font-variant-numeric: tabular-nums;
}

.pd-price {
  border: 1px solid var(--field-line);
  background: var(--field-tint);
  border-radius: 10px;
  padding: 9px 12px;
  font-size: 13px;
  color: var(--field-muted);
}

.pd-price-stones, .pd-price-reference {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 0 10px;
}

.pd-price-stones b, .pd-price-stones strong, .pd-price-reference a { color: var(--field-accent); }
.pd-price-stones strong {
  font-size: 20px;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
}

.pd-price-reference {
  margin-top: 4px;
  border-top: 1px solid var(--field-line);
  padding-top: 4px;
  font-variant-numeric: tabular-nums;
}

.pd-sec :is(h2,h3) {
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
  grid-template-columns: 5em minmax(0, 1fr);
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
  overflow-wrap: anywhere;
}

.pd-related {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 220px), 1fr));
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
  overflow-wrap: anywhere;
}

.pd-rel-card span {
  font-size: 12px;
  color: var(--vp-c-text-3);
}

@media (max-width: 760px) {
  .pd-head {
    grid-template-columns: 1fr;
  }

  .pd-img { max-width: 180px; }

  .pd-2026-body { flex-wrap: wrap; gap: 10px; }
  .pd-radar { width: 100px; height: 100px; }
}

@media (max-width: 600px) {
  .pd--dialog .pd-head {
    grid-template-columns: 78px minmax(0, 1fr);
    gap: 8px;
  }
  .pd--dialog .pd-main { display: contents; }
  .pd--dialog .pd-img { max-width: none; }
  .pd--dialog .pd-img img { padding: 5px; }
  .pd--dialog .pd-glyph { font-size: 40px; }
  .pd--dialog .pd-badges { margin: 0; align-self: center; }
  .pd--dialog .pd-2026, .pd--dialog .pd-price { grid-column: 1 / -1; margin: 0; }
  .pd--dialog .pd-2026-body:has(.pd-radar) { display: grid; grid-template-columns: 86px minmax(0, 1fr); gap: 7px; align-items: center; }
  .pd--dialog .pd-radar { width: 86px; height: 86px; }
  .pd--dialog .pd-2026-rows div { gap: 5px; }
}

/* 网格 1fr 列默认 min-width:auto，长名字/徽章会把 .pd-main 顶出容器（移动端 4px 溢出） */
.pd-main {
  min-width: 0;
}

.pd-name {
  overflow-wrap: anywhere;
}
</style>
