<script setup lang="ts">
import { computed, ref } from "vue";
import prices from "../../data/pet-prices.json";
import codex from "../../data/pet-codex.json";

interface PriceRow {
  sys: string;
  name: string;
  original: string;
  discount: string;
  special: string;
  charge50: string;
  charge10: string;
}

const rows = prices as PriceRow[];

// 同名宠物 → 图鉴详情链接
const petIdByName = new Map<string, number>(
  (codex as { id: number; name: string }[]).map((p) => [p.name, p.id])
);

const sysList = ["全部", ...Array.from(new Set(rows.map((r) => r.sys))).filter(Boolean)];
const activeSys = ref("全部");
const keyword = ref("");
const limit = ref(80);

function fmt(v: string): string {
  const n = Number(v);
  if (Number.isFinite(n) && v !== "") return n.toFixed(2).replace(/\.00$/, "");
  return v;
}

const filtered = computed(() => {
  const k = keyword.value.trim();
  return rows.filter((r) => {
    if (activeSys.value !== "全部" && r.sys !== activeSys.value) return false;
    if (!k) return true;
    return r.name.includes(k);
  });
});

const visible = computed(() => filtered.value.slice(0, limit.value));

const sysAvg = computed(() => {
  const groups = new Map<string, number[]>();
  for (const r of rows) {
    const v = Number(r.special);
    if (!Number.isFinite(v) || !r.sys) continue;
    groups.set(r.sys, [...(groups.get(r.sys) ?? []), v]);
  }
  const list = [...groups.entries()].map(([sys, vs]) => ({ sys, avg: Math.round(vs.reduce((a, b) => a + b, 0) / vs.length) }));
  const max = Math.max(...list.map((x) => x.avg));
  return list.map((x) => ({ ...x, pct: (x.avg / max) * 100 }));
});
</script>

<template>
  <div class="pc-wrap">
    <div class="pc-toolbar">
      <div class="pc-tabs">
        <button
          v-for="s in sysList"
          :key="s"
          class="pc-tab"
          :class="{ active: activeSys === s }"
          @click="activeSys = s"
        >
          {{ s }}
        </button>
      </div>
      <input v-model="keyword" class="item-search pc-search" type="search" placeholder="搜索幻兽名字" />
    </div>

    <div class="sys-bars">
      <div v-for="b in sysAvg" :key="b.sys" class="sys-bar">
        <span class="sys-bar-label">{{ b.sys }}</span>
        <div class="sys-bar-track"><div class="sys-bar-fill" :style="{ width: b.pct + '%' }"></div></div>
        <span class="sys-bar-val">{{ b.avg }}</span>
      </div>
    </div>

    <p class="item-count">命中 {{ filtered.length }} 条 / 共 {{ rows.length }} 条，当前显示 {{ visible.length }} 条</p>

    <table>
      <thead>
        <tr>
          <th>系别</th>
          <th>幻兽名字</th>
          <th>原价（灵石）</th>
          <th>折扣</th>
          <th>特惠价（灵石）</th>
          <th>50 元充值价</th>
          <th>10 元充值价</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in visible" :key="r.sys + r.name">
          <td class="pp-sys">{{ r.sys }}</td>
          <td class="pp-name">
            <a v-if="petIdByName.get(r.name)" :href="`/pets/${petIdByName.get(r.name)}`">{{ r.name }}</a>
            <template v-else>{{ r.name }}</template>
          </td>
          <td>{{ fmt(r.original) }}</td>
          <td>{{ fmt(r.discount) }}</td>
          <td class="pp-hot">{{ fmt(r.special) }}</td>
          <td>{{ fmt(r.charge50) }}</td>
          <td>{{ fmt(r.charge10) }}</td>
        </tr>
      </tbody>
    </table>

    <p v-if="filtered.length > limit" class="item-count">
      <a @click.prevent="limit += 100" href="#">加载更多（还剩 {{ filtered.length - limit }} 条）</a>
    </p>
    <p v-else class="item-count">已显示全部结果</p>
  </div>
</template>

<style scoped>
.pp-sys {
  white-space: nowrap;
  color: var(--vp-c-text-2);
}

.pp-name {
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.pp-hot {
  color: var(--vp-c-brand-1);
  font-weight: 700;
}
</style>

<style>
.sys-bars {
  display: grid;
  gap: 8px;
  margin: 4px 0 16px;
  max-width: 640px;
}

.sys-bar {
  display: grid;
  grid-template-columns: 48px 1fr 72px;
  align-items: center;
  gap: 10px;
  font-size: 12.5px;
}

.sys-bar-label {
  color: var(--vp-c-text-2);
  font-weight: 600;
}

.sys-bar-track {
  height: 10px;
  border-radius: 999px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  overflow: hidden;
}

.sys-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #b8860b, #f5d67b);
  border-radius: 999px;
}

.sys-bar-val {
  color: var(--vp-c-brand-1);
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  text-align: right;
}
</style>
