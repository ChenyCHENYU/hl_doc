<script setup lang="ts">
import { computed, ref, watch } from "vue";
import prices from "../../data/pet-prices.json";
import codex from "../../data/pet-codex.json";
import { formatPetPriceYuan, petRechargeTiers, readPetPrice } from "../../data/pet-price-format";
import PetQuickView from "./PetQuickView.vue";

const rows = prices.map((price, index) => ({ ...price, index, amount: readPetPrice(price.special) }));
const petIdByName = new Map(codex.map((pet) => [pet.name, pet.id]));
const sysList = ["全部", "金系", "木系", "水系", "火系", "土系"];
const activeSys = ref("全部");
const keyword = ref("");
const order = ref("source");
const pageSize = 40;
const limit = ref(pageSize);
const calculatorAmount = ref<string | number>(228);
const calculatorStones = computed(() => readPetPrice(calculatorAmount.value));
const quickView = ref<InstanceType<typeof PetQuickView> | null>(null);

const stonesFormat = new Intl.NumberFormat("zh-CN", { maximumFractionDigits: 2 });
const counts = new Map(sysList.map((sys) => [sys, rows.filter((row) => row.sys === sys).length]));

function formatStones(value: string) {
  const amount = readPetPrice(value);
  return amount == null ? value || "—" : stonesFormat.format(amount);
}

function formatDiscount(value: string) {
  const discount = readPetPrice(value);
  return discount == null ? value || "—" : `${stonesFormat.format(discount * 10)} 折`;
}

function calculatePrice(rate: number) {
  return formatPetPriceYuan(calculatorStones.value == null ? null : calculatorStones.value * rate);
}

watch([activeSys, keyword, order], () => { limit.value = pageSize; });

const filtered = computed(() => {
  const query = keyword.value.trim();
  const found = rows.filter((row) =>
    (activeSys.value === "全部" || row.sys === activeSys.value) && row.name.includes(query),
  );
  if (order.value === "source") return found;
  const direction = order.value === "low" ? 1 : -1;
  return found.sort((a, b) => {
    if (a.amount == null) return b.amount == null ? 0 : 1;
    if (b.amount == null) return -1;
    return (a.amount - b.amount) * direction;
  });
});
const visible = computed(() => filtered.value.slice(0, limit.value));
const visiblePetIds = computed(() => [...new Set(visible.value.flatMap((row) => petIdByName.get(row.name) ?? []))]);

const averages = sysList.slice(1).flatMap((sys) => {
  const matching = rows.filter((row) => row.sys === sys && row.amount != null);
  if (!matching.length) return [];
  const average = Math.round(matching.reduce((total, row) => total + (row.amount ?? 0), 0) / matching.length);
  return [{ sys, avg: average }];
});
const averageMax = Math.max(1, ...averages.map((row) => row.avg));
</script>

<template>
  <div class="pet-prices field-ui">
    <section class="price-calculator" aria-labelledby="price-calculator-title">
      <div class="price-calculator-input">
        <h2 id="price-calculator-title">灵石换算</h2>
        <label class="price-stones-input">
          <span class="screen-reader-only">要换算的灵石数量</span>
          <input v-model="calculatorAmount" type="number" inputmode="numeric" min="0" step="any" />
          <span aria-hidden="true">灵石</span>
        </label>
      </div>
      <div v-for="tier in petRechargeTiers" :key="tier.amount" class="price-estimate">
        <span>{{ tier.amount }} 元档 · 人民币参考</span>
        <output aria-live="polite">{{ calculatePrice(tier.yuanPerStone) }}</output>
      </div>
    </section>

    <p class="price-note">换算取自原表：50 元档每灵石 ¥0.03623，10 元档每元 27 灵石。按实际使用的灵石折算，当前充值请以<a href="https://hl.99.com/" target="_blank" rel="noopener noreferrer">游戏官网</a>的充值入口为准。</p>

    <section class="price-catalog" aria-labelledby="price-catalog-title">
      <h2 id="price-catalog-title">查宠物重塑价格</h2>
      <div class="price-filters">
        <label class="price-filter">
          <span class="screen-reader-only">搜索宠物名称</span>
          <input v-model="keyword" type="search" placeholder="搜索宠物名称" />
        </label>
        <label class="price-filter">
          <span class="screen-reader-only">价格排序</span>
          <select v-model="order">
            <option value="source">原表顺序</option>
            <option value="low">特惠价从低到高</option>
            <option value="high">特惠价从高到低</option>
          </select>
        </label>
      </div>
      <div class="price-elements" role="group" aria-label="按五行筛选价格">
        <button v-for="sys in sysList" :key="sys" type="button" :aria-pressed="activeSys === sys" @click="activeSys = sys">
          {{ sys }} <span>{{ sys === "全部" ? rows.length : counts.get(sys) }}</span>
        </button>
      </div>
      <p class="price-count" role="status">找到 {{ filtered.length }} 条价格 · 显示 {{ visible.length }} 条</p>

      <div v-if="visible.length" class="price-table-wrap">
        <table class="price-table">
          <caption class="screen-reader-only">宠物重塑价格与人民币折算</caption>
          <thead>
            <tr>
              <th scope="col">宠物</th>
              <th scope="col">灵石价格</th>
              <th scope="col">人民币参考</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in visible" :key="row.index">
              <th scope="row">
                <a
                  v-if="petIdByName.has(row.name)"
                  class="vp-raw"
                  :href="`/pets/${petIdByName.get(row.name)}`"
                  aria-haspopup="dialog"
                  @click="quickView?.openFromLink($event, petIdByName.get(row.name) ?? 0)"
                >{{ row.name }}</a>
                <strong v-else>{{ row.name }}</strong>
                <small class="price-trait">{{ row.sys }}</small>
              </th>
              <td>
                <div class="price-main"><strong>{{ formatStones(row.special) }}</strong> <span>特惠</span></div>
                <small class="price-secondary">原价 {{ formatStones(row.original) }} · {{ formatDiscount(row.discount) }}</small>
              </td>
              <td>
                <div class="price-yuan"><span>50 元档</span><b>{{ formatPetPriceYuan(row.charge50) }}</b></div>
                <div class="price-yuan"><span>10 元档</span><b>{{ formatPetPriceYuan(row.charge10) }}</b></div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="price-empty">未找到宠物，试试其他名称或切回「全部」。</p>
      <button v-if="visible.length < filtered.length" class="price-more" type="button" @click="limit += pageSize">
        显示更多价格（还剩 {{ filtered.length - visible.length }} 条）
      </button>
    </section>

    <details class="price-summary">
      <summary>各系平均特惠价与数据来源</summary>
      <p>平均值按《重塑宠物价格.xlsx》「幻兽价格」中各系记录计算，单位为灵石。人民币列保留工作簿的计算结果，按两位小数显示。</p>
      <dl class="price-averages">
        <div v-for="group in averages" :key="group.sys">
          <dt>{{ group.sys }}</dt>
          <dd><meter :value="group.avg" :max="averageMax" :aria-label="`${group.sys}平均特惠价`" /><b>{{ formatStones(String(group.avg)) }}</b></dd>
        </div>
      </dl>
      <p><a href="https://news.99.com/content/2013-05-01/20130501230407292.shtml" target="_blank" rel="noopener noreferrer">官方充值系统公告</a>说明充值后在游戏内领取灵石，公告没有公布各档兑换数量。</p>
    </details>
    <PetQuickView ref="quickView" :pet-ids="visiblePetIds" />
  </div>
</template>

<style scoped>
.pet-prices {
  color: var(--field-ink);
  font-variant-numeric: tabular-nums;
}

.pet-prices h2 {
  margin: 0;
  padding: 0;
  border: 0;
}

.price-calculator {
  display: grid;
  grid-template-columns: 1.35fr 1fr 1fr;
  align-items: stretch;
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--field-line);
  border-radius: 16px;
  background: var(--field-paper);
}

.price-calculator h2 {
  margin-bottom: 8px;
  font-size: 18px;
  line-height: 1.4;
}

.price-calculator-input,
.price-estimate,
.price-filter {
  min-width: 0;
}

.price-estimate {
  display: grid;
  align-content: center;
  gap: 7px;
  padding: 10px 12px;
  border-radius: 10px;
  background: var(--field-tint);
}

.price-estimate > span,
.price-note,
.price-count,
.price-trait,
.price-secondary,
.price-main span,
.price-yuan span {
  color: var(--field-muted);
}

.price-estimate > span {
  font-size: 12px;
  line-height: 1.35;
}

.price-estimate output {
  color: var(--field-action);
  font-size: clamp(18px, 3vw, 27px);
  font-weight: 750;
  overflow-wrap: anywhere;
}

.price-stones-input {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-inline: 10px;
  border: 1px solid var(--field-line);
  border-radius: 8px;
}

.price-stones-input:focus-within {
  border-color: var(--field-accent);
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--field-accent) 36%, transparent);
}

.price-stones-input input,
.price-filter input,
.price-filter select {
  min-height: 42px;
  width: 100%;
  min-width: 0;
  color: var(--field-ink);
  font-size: 16px;
}

.price-stones-input input:focus-visible {
  outline: none;
}

.price-stones-input span:last-child {
  flex: none;
  color: var(--field-muted);
  font-size: 14px;
}

.price-note {
  margin: 10px 0 0;
  font-size: 13px;
}

.price-catalog {
  margin-top: 27px;
}

.price-catalog h2 {
  margin-bottom: 11px;
  font-size: 21px;
  line-height: 1.5;
}

.price-filters {
  display: grid;
  grid-template-columns: minmax(0, 1fr) max-content;
  gap: 9px;
}

.price-filter input,
.price-filter select {
  padding-inline: 10px;
  border: 1px solid var(--field-line);
  border-radius: 8px;
  background: var(--field-paper);
}

.price-filter input::placeholder {
  color: var(--field-muted);
}

.price-filter :is(input, select):focus-visible {
  border-color: transparent;
  outline-offset: 0;
}

.price-filter select {
  appearance: auto;
  padding-right: 21px;
  font-size: 14px;
}

.price-elements {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin: 11px 0 6px;
}

.price-elements button,
.price-more {
  min-height: 40px;
  padding: 5px 11px;
  border: 1px solid var(--field-line);
  border-radius: 8px;
  background: var(--field-paper);
  color: var(--field-ink);
  font-size: 14px;
}

.price-elements button:hover,
.price-more:hover {
  border-color: var(--field-accent);
}

.price-elements button[aria-pressed="true"] {
  border-color: var(--field-action);
  background: var(--field-action);
  color: var(--field-action-text);
}

.price-elements button span {
  font-size: 12px;
  opacity: .88;
}

.price-count {
  margin: 10px 0 6px;
  font-size: 13px;
}

.price-table-wrap {
  width: 100%;
  overflow: auto;
  border: 1px solid var(--field-line);
  border-radius: 12px;
}

.pet-prices table.price-table {
  display: table;
  width: 100%;
  margin: 0;
  border-collapse: collapse;
  table-layout: fixed;
}

.price-table thead th {
  color: var(--field-ink);
  background: var(--field-tint);
  font-size: 13px;
  text-align: left;
}

.pet-prices .price-table :is(th, td) {
  border: 0;
  border-bottom: 1px solid var(--field-line);
  padding: 9px 13px;
  vertical-align: middle;
  white-space: normal;
  overflow-wrap: anywhere;
}

.price-table tbody th {
  background: transparent;
  text-align: left;
}

.price-table tr {
  border: 0;
  background: var(--field-paper);
}

.price-table tbody tr:nth-child(even) {
  background: color-mix(in srgb, var(--field-tint) 26%, var(--field-paper));
}

.price-table tbody tr:last-child > * {
  border-bottom: 0;
}

.price-table tbody th :is(a, strong) {
  color: var(--field-ink);
  font-weight: 700;
}

.price-table tbody th a:hover {
  color: var(--field-accent);
}

.price-table small {
  display: block;
  font-size: 12px;
  line-height: 1.5;
}

.price-main,
.price-yuan {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 2px 6px;
  line-height: 1.45;
}

.price-main strong {
  color: var(--field-accent);
  font-size: 16px;
}

.price-yuan b {
  color: var(--field-ink);
  font-size: 13px;
}

.price-main span,
.price-yuan span {
  font-size: 12px;
}

.price-more {
  margin-top: 10px;
}

.price-empty {
  padding: 12px;
  border-radius: 11px;
  background: var(--field-tint);
}

.price-summary {
  margin-top: 23px;
  padding: 11px 14px;
  border: 1px solid var(--field-line);
  border-radius: 11px;
  color: var(--field-muted);
  font-size: 13px;
}

.price-summary summary {
  cursor: pointer;
  color: var(--field-ink);
  font-weight: 650;
}

.price-summary p {
  margin: 7px 0;
}

.price-averages {
  display: grid;
  gap: 4px;
  margin-block: 7px;
}

.price-averages > div,
.price-averages dd {
  display: flex;
  align-items: center;
  gap: 6px;
}

.price-averages dt {
  min-width: 3em;
}

.price-averages dd {
  margin: 0;
}

.price-averages meter {
  width: 110px;
}

.screen-reader-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}

@media (max-width: 560px) {
  .price-calculator {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    padding: 11px;
    gap: 7px;
  }
  .price-calculator-input {
    grid-column: 1 / -1;
  }
  .price-estimate {
    padding: 7px 9px;
  }
  .pet-prices .price-table :is(th, td) {
    padding: 7px;
  }
}

@media (max-width: 360px) {
  .price-filters { grid-template-columns: 1fr; }
}
</style>
