<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import tower from "../../data/tower-defense.json";

interface TowerRow {
  mode: string;
  floor: string;
  level: string;
  monster: string;
  element: string;
  maxAtk: string;
  defHuman: string;
  defEarth: string;
  defFire: string;
  defWater: string;
  defWood: string;
  defMetal: string;
  agi: string;
}

const rows = tower as TowerRow[];
const keyword = ref("");
const limit = ref(40);
onMounted(() => {
  keyword.value = new URLSearchParams(window.location.search).get("floor") ?? "";
});

const EL: Record<string, string> = { 金: "#d4af37", 木: "#5cae7d", 水: "#5b9bd5", 火: "#e0664f", 土: "#c4875a" };

const filtered = computed(() => {
  const k = keyword.value.trim();
  if (!k) return rows;
  return rows.filter((r) => r.monster.includes(k) || r.element.includes(k) || r.floor === k);
});
const visible = computed(() => filtered.value.slice(0, limit.value));

const maxDef = computed(() => Math.max(...rows.map((r) => Number(r.defHuman) || 0)));
const hardFloor = computed(() => {
  let best = rows[0];
  let gap = 0;
  for (let i = 1; i < rows.length; i++) {
    const d = (Number(rows[i].defHuman) || 0) - (Number(rows[i - 1].defHuman) || 0);
    if (d > gap) { gap = d; best = rows[i]; }
  }
  return `第 ${best.floor} 关 (+${gap})`;
});
const maxAkiFloor = computed(() => {
  const best = rows.reduce((a, b) => (Number(b.maxAtk) > Number(a.maxAtk) ? b : a), rows[0]);
  return `第 ${best.floor} 关`;
});
function line(get: (r: TowerRow) => number, max: number): string {
  return rows
    .map((r, i) => `${(i / (rows.length - 1)) * 640},${145 - (get(r) / max) * 135}`)
    .join(" ");
}
const scale = Math.max(1, maxDef.value, ...rows.map((row) => Number(row.maxAtk) || 0));
const defLine = computed(() => line((r) => Number(r.defHuman) || 0, scale));
const atkLine = computed(() => line((r) => Number(r.maxAtk) || 0, scale));
</script>

<template>
  <div class="pc-wrap">
    <div class="dash-cards">
      <div class="dash-card"><b>{{ rows.length }}</b><span>总关数</span></div>
      <div class="dash-card"><b>{{ maxDef }}</b><span>最高人防需求</span></div>
      <div class="dash-card"><b>{{ hardFloor }}</b><span>防御陡增关卡</span></div>
      <div class="dash-card"><b>{{ maxAkiFloor }}</b><span>攻击峰值关</span></div>
    </div>

    <svg viewBox="0 0 640 150" class="dash-chart" preserveAspectRatio="none">
      <polyline :points="defLine" class="dash-line" />
      <polyline :points="atkLine" class="dash-line atk" />
    </svg>
    <p class="item-count" style="margin:0 0 6px">
      <span class="lg gold">— 人防需求曲线</span> <span class="lg red">— 最大攻击曲线</span>（横轴 1–{{ rows.length }} 关）
    </p>

    <div class="pc-toolbar">
      <p class="item-count" style="margin: 0">共 {{ rows.length }} 关 · 支持按关数 / 怪物名 / 属性筛选</p>
      <input v-model="keyword" class="item-search pc-search" type="search" placeholder="如：10 / 厚皮鳄 / 火" aria-label="筛选天关关数、怪物或属性" />
    </div>

    <div class="lookup-scroll" role="region" aria-label="天关防御表" tabindex="0">
    <table>
      <thead>
        <tr>
          <th>关数</th>
          <th>等级</th>
          <th>怪物</th>
          <th>属性</th>
          <th>最大攻击</th>
          <th>人防需求</th>
          <th>金防</th>
          <th>木防</th>
          <th>水防</th>
          <th>火防</th>
          <th>土防</th>
          <th>敏捷</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in visible" :key="r.floor + r.monster">
          <td class="pp-sys">{{ r.floor }}</td>
          <td>{{ r.level }}</td>
          <td class="pp-name">{{ r.monster }}</td>
          <td><span class="tower-el" :style="{ color: EL[r.element], borderColor: EL[r.element] }">{{ r.element }}</span></td>
          <td>{{ r.maxAtk }}</td>
          <td class="pp-hot">{{ r.defHuman }}</td>
          <td>{{ r.defMetal }}</td>
          <td>{{ r.defWood }}</td>
          <td>{{ r.defWater }}</td>
          <td>{{ r.defFire }}</td>
          <td>{{ r.defEarth }}</td>
          <td>{{ r.agi }}</td>
        </tr>
      </tbody>
    </table>
    </div>

    <p v-if="filtered.length > limit" class="item-count">
      <a @click.prevent="limit += 40" href="#">加载更多（还剩 {{ filtered.length - limit }} 关）</a>
    </p>
  </div>
</template>

<style scoped>
.tower-el {
  display: inline-block;
  font-size: 12px;
  font-weight: 700;
  border: 1px solid;
  border-radius: 6px;
  padding: 0 8px;
}
</style>

<style>
.dash-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
  margin-bottom: 14px;
}

.dash-card {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.dash-card b {
  font-size: 20px;
  color: var(--vp-c-brand-1);
  font-variant-numeric: tabular-nums;
}

.dash-card span {
  font-size: 12px;
  color: var(--vp-c-text-3);
}

.dash-chart {
  width: 100%;
  height: 150px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  margin-bottom: 6px;
}

.dash-line {
  fill: none;
  stroke: var(--vp-c-brand-1);
  stroke-width: 2;
}

.dash-line.atk {
  stroke: #d15a5a;
  stroke-dasharray: 4 3;
  opacity: 0.8;
}

.lg.gold { color: var(--vp-c-brand-1); font-weight: 600; }
.lg.red { color: #d15a5a; font-weight: 600; }
</style>
