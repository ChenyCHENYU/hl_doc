<script setup lang="ts">
// 锻造 · 乾坤五行炉 概念可视化（数据来自 help23 原文）
import { EVO_ELEMENTS } from "../evolution";

const EL = EVO_ELEMENTS as Record<string, { label: string; color: string }>;

type El = keyof typeof EL;

// 装备 → 五行 属性映射
const EQUIP: { name: string; el: El; stat: string }[] = [
  { name: "武器", el: "fire", stat: "攻击" },
  { name: "防具", el: "metal", stat: "防御" },
  { name: "鞋", el: "water", stat: "敏捷" },
  { name: "身饰", el: "wood", stat: "内力" },
  { name: "头饰", el: "earth", stat: "血量" },
];

// 使用流程
const STEPS = [
  { t: "得炉", d: "完成相关任务获得乾坤五行炉" },
  { t: "投料", d: "宠物、物品、甚至银子都可以丢进炉里" },
  { t: "选主炼", d: "系统询问本次炼化的主要成份" },
  { t: "预览炼化", d: "不满意就调整物品位置多试几次，往往有意外效果" },
];

// 相生环：金→水→木→火→土→金
const SHENG: [El, El][] = [
  ["metal", "water"],
  ["water", "wood"],
  ["wood", "fire"],
  ["fire", "earth"],
  ["earth", "metal"],
];
// 相克星：金克木 木克土 土克水 水克火 火克金
const KE: [El, El][] = [
  ["metal", "wood"],
  ["wood", "earth"],
  ["earth", "water"],
  ["water", "fire"],
  ["fire", "metal"],
];

const C = 130;
const R = 92;
function pt(i: number, r = R): [number, number] {
  const a = (Math.PI * 2 * i) / 5 - Math.PI / 2;
  return [C + Math.cos(a) * r, C + Math.sin(a) * r];
}
const ORDER: El[] = ["metal", "water", "wood", "fire", "earth"];
const nodes = ORDER.map((el, i) => ({ el, ...pt(i) }));
const labelOf = (el: El) => EL[el]?.label ?? el;
const colorOf = (el: El) => EL[el]?.color ?? "#888";

// 弧线上带箭头（相生，顺时针外环）
function arcPath(i: number): string {
  const [x1, y1] = pt(i);
  const [x2, y2] = pt((i + 1) % 5);
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  const nx = mx - C;
  const ny = my - C;
  const len = Math.hypot(nx, ny) || 1;
  const ox = (nx / len) * 14;
  const oy = (ny / len) * 14;
  const a1 = [x1 + ox * 0.9 + (-oy / 14) * 6, y1 + oy * 0.9 + (ox / 14) * 6];
  const a2 = [x2 + ox * 0.9 + (-oy / 14) * 6, y2 + oy * 0.9 + (ox / 14) * 6];
  return `M ${a1[0]} ${a1[1]} L ${a2[0]} ${a2[1]}`;
}

// 四条生克规则（主炼=装备，陪炼=加入物）
const RULES: {
  key: string;
  name: string;
  main: El;
  side: El;
  rel: "sheng" | "ke";
  dir: "m2s" | "s2m";
  effect: string;
  example: string;
  tone: "up" | "down" | "mix";
}[] = [
  {
    key: "r1",
    name: "主炼生陪炼",
    main: "fire",
    side: "earth",
    rel: "sheng",
    dir: "m2s",
    effect: "主炼装备获得陪炼物对应的属性（上升）",
    example: "武器（火）＋ 头饰（土）→ 武器附带加血",
    tone: "up",
  },
  {
    key: "r2",
    name: "陪炼生主炼",
    main: "fire",
    side: "wood",
    rel: "sheng",
    dir: "s2m",
    effect: "双方对应属性都上升，主炼装备为主",
    example: "武器（火）＋ 身饰（木）→ 攻击、内力双双上升",
    tone: "up",
  },
  {
    key: "r3",
    name: "主炼克陪炼",
    main: "fire",
    side: "metal",
    rel: "ke",
    dir: "m2s",
    effect: "主炼装备的对应属性下降（可为负）",
    example: "武器（火）＋ 防具（金）→ 武器防御下降——故意用它压低装备使用等级",
    tone: "down",
  },
  {
    key: "r4",
    name: "陪炼克主炼",
    main: "fire",
    side: "water",
    rel: "ke",
    dir: "s2m",
    effect: "直接降低主炼装备对应属性，陪炼越好降得越多",
    example: "武器（火）＋ 鞋（水）→ 武器攻击下降",
    tone: "down",
  },
];

const TONE: Record<string, { label: string; cls: string }> = {
  up: { label: "属性 ↑", cls: "is-up" },
  down: { label: "属性 ↓", cls: "is-down" },
  mix: { label: "混合", cls: "is-mix" },
};

const legendSheng = SHENG.map(([a, b]) => `${labelOf(a)}生${labelOf(b)}`).join(" · ");
const legendKe = KE.map(([a, b]) => `${labelOf(a)}克${labelOf(b)}`).join(" · ");
</script>

<template>
  <div class="fg">
    <section class="fg-sec">
      <h3 class="fg-title">装备五行 · 一图看懂</h3>
      <div class="fg-equip">
        <div v-for="e in EQUIP" :key="e.name" class="fg-equip-cell" :style="{ '--el': colorOf(e.el) }">
          <span class="fg-equip-el">{{ labelOf(e.el) }}</span>
          <b class="fg-equip-name">{{ e.name }}</b>
          <span class="fg-equip-stat">主加{{ e.stat }}</span>
        </div>
      </div>
      <p class="fg-note">身饰主要指加内力的装备，其他身饰作特殊物品对待。</p>
    </section>

    <section class="fg-sec fg-cycle-sec">
      <h3 class="fg-title">五行生克环</h3>
      <div class="fg-cycle">
        <svg viewBox="0 0 260 260" class="fg-svg" aria-label="五行生克关系图">
          <!-- 相克内星 -->
          <line
            v-for="([a, b], i) in KE"
            :key="'k' + i"
            :x1="nodes[ORDER.indexOf(a)].x"
            :y1="nodes[ORDER.indexOf(a)].y"
            :x2="nodes[ORDER.indexOf(b)].x"
            :y2="nodes[ORDER.indexOf(b)].y"
            class="fg-ke-line"
          />
          <!-- 相生外环（带箭头线段） -->
          <g v-for="(s, i) in SHENG" :key="'s' + i">
            <path :d="arcPath(i)" class="fg-sheng-line" />
            <circle :r="2.6" class="fg-sheng-dot">
              <animateMotion :dur="`${2.4 + i * 0.3}s`" repeatCount="indefinite" :path="arcPath(i)" />
            </circle>
          </g>
          <!-- 节点 -->
          <g v-for="n in nodes" :key="n.el">
            <circle :cx="n.x" :cy="n.y" r="20" class="fg-node" :style="{ stroke: colorOf(n.el) }" />
            <text :x="n.x" :y="n.y + 5.5" class="fg-node-text" :fill="colorOf(n.el)">{{ labelOf(n.el) }}</text>
          </g>
        </svg>
        <div class="fg-legend">
          <p><span class="fg-dot sheng"></span>外环相生：{{ legendSheng }}</p>
          <p><span class="fg-dot ke"></span>内星相克：{{ legendKe }}</p>
        </div>
      </div>
    </section>

    <section class="fg-sec">
      <h3 class="fg-title">使用流程</h3>
      <ol class="fg-steps">
        <li v-for="(s, i) in STEPS" :key="s.t">
          <b>{{ i + 1 }}. {{ s.t }}</b>
          <span>{{ s.d }}</span>
        </li>
      </ol>
    </section>

    <section class="fg-sec">
      <h3 class="fg-title">四条核心规则 · 生克定属性</h3>
      <div class="fg-rules">
        <article v-for="r in RULES" :key="r.key" class="fg-rule" :class="TONE[r.tone].cls">
          <header>
            <span class="fg-pair">
              <i :style="{ background: colorOf(r.main) }">{{ labelOf(r.main) }}</i>
              <em class="fg-rel">{{ r.rel === "sheng" ? "生" : "克" }}</em>
              <i :style="{ background: colorOf(r.side) }">{{ labelOf(r.side) }}</i>
            </span>
            <span class="fg-rule-tone">{{ TONE[r.tone].label }}</span>
          </header>
          <b class="fg-rule-name">{{ r.name }}</b>
          <p class="fg-rule-effect">{{ r.effect }}</p>
          <p class="fg-rule-example">{{ r.example }}</p>
        </article>
      </div>
      <aside class="fg-tip">
        <b>压等小技巧</b>：攻 500 的刀要求修行 8000，你只有 3500？用「主炼克陪炼」把不重要的属性炼负，
        使用等级会随之降到你能装备的区间——属性是拿来换的。
      </aside>
    </section>
  </div>
</template>

<style scoped>
.fg {
  margin: 20px 0 28px;
  display: grid;
  gap: 26px;
}

.fg-sec {
  min-width: 0;
}

.fg-title {
  margin: 0 0 12px;
  font-size: 16px;
  font-weight: 800;
  color: var(--vp-c-text-1);
  padding-left: 10px;
  border-left: 3px solid var(--vp-c-brand-1);
}

/* ── 装备映射 ── */
.fg-equip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(128px, 1fr));
  gap: 10px;
}

.fg-equip-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  padding: 14px 10px 12px;
  border: 1px solid var(--vp-c-divider);
  border-top: 3px solid var(--el);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
}

.fg-equip-el {
  font-size: 20px;
  font-weight: 800;
  color: var(--el);
  line-height: 1.1;
}

.fg-equip-name {
  font-size: 14px;
  color: var(--vp-c-text-1);
}

.fg-equip-stat {
  font-size: 12px;
  color: var(--vp-c-text-3);
}

.fg-note {
  margin: 8px 0 0;
  font-size: 12px;
  color: var(--vp-c-text-3);
}

/* ── 五行环 ── */
.fg-cycle {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 18px;
}

.fg-svg {
  width: 250px;
  height: 250px;
  flex-shrink: 0;
}

.fg-sheng-line {
  fill: none;
  stroke: var(--vp-c-brand-1);
  stroke-width: 1.8;
  marker-end: none;
}

.fg-sheng-dot {
  fill: var(--vp-c-brand-1);
}

.fg-ke-line {
  stroke: #b0563c;
  stroke-width: 1.2;
  stroke-dasharray: 5 4;
  opacity: 0.75;
  animation: hl-ke-flow 2.6s linear infinite;
}

@keyframes hl-ke-flow {
  to { stroke-dashoffset: -18; }
}

.fg-node {
  fill: var(--vp-c-bg);
  stroke-width: 2.5;
  animation: hl-node-breathe 3.6s ease-in-out infinite;
}

.fg-node {
  fill: var(--vp-c-bg);
  stroke-width: 2.5;
}

.fg-node-text {
  font-size: 15px;
  font-weight: 800;
  text-anchor: middle;
}

.fg-legend {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 13px;
  color: var(--vp-c-text-2);
  min-width: 200px;
  flex: 1;
}

.fg-legend p {
  margin: 0;
  line-height: 1.7;
}

.fg-dot {
  display: inline-block;
  width: 14px;
  height: 3px;
  border-radius: 2px;
  margin-right: 8px;
  vertical-align: middle;
}

.fg-dot.sheng {
  background: var(--vp-c-brand-1);
}

.fg-dot.ke {
  background: #b0563c;
}

/* ── 流程 ── */
.fg-steps {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 10px;
  counter-reset: fs;
}

.fg-steps li {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px 14px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
}

.fg-steps b {
  font-size: 14px;
  color: var(--vp-c-brand-1);
}

.fg-steps span {
  font-size: 12.5px;
  line-height: 1.7;
  color: var(--vp-c-text-2);
}

/* ── 规则卡 ── */
.fg-rules {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 12px;
}

.fg-rule {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 14px 16px;
  border: 1px solid var(--vp-c-divider);
  border-left: 3px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
}

.fg-rule.is-up {
  border-left-color: #2e9e6f;
}

.fg-rule.is-down {
  border-left-color: #b0563c;
}

.fg-rule header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.fg-pair {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.fg-pair i {
  font-style: normal;
  width: 26px;
  height: 26px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  color: #fff;
  font-size: 13px;
  font-weight: 800;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.fg-rel {
  font-style: normal;
  font-size: 13px;
  font-weight: 800;
  color: var(--vp-c-text-3);
}

.fg-rule-tone {
  font-size: 12px;
  font-weight: 800;
}

.is-up .fg-rule-tone {
  color: #2e9e6f;
}

.is-down .fg-rule-tone {
  color: #b0563c;
}

.fg-rule-name {
  font-size: 14.5px;
  color: var(--vp-c-text-1);
}

.fg-rule-effect {
  margin: 0;
  font-size: 13px;
  line-height: 1.7;
  color: var(--vp-c-text-2);
}

.fg-rule {
  animation: hl-fade-up 0.5s ease both;
}

.fg-rule:nth-child(1) { animation-delay: 0.05s; }
.fg-rule:nth-child(2) { animation-delay: 0.15s; }
.fg-rule:nth-child(3) { animation-delay: 0.25s; }
.fg-rule:nth-child(4) { animation-delay: 0.35s; }

.fg-equip-cell {
  animation: hl-pop 0.45s ease both;
}

.fg-equip-cell:nth-child(1) { animation-delay: 0.05s; }
.fg-equip-cell:nth-child(2) { animation-delay: 0.11s; }
.fg-equip-cell:nth-child(3) { animation-delay: 0.17s; }
.fg-equip-cell:nth-child(4) { animation-delay: 0.23s; }
.fg-equip-cell:nth-child(5) { animation-delay: 0.29s; }

@media (prefers-reduced-motion: reduce) {
  .fg-ke-line, .fg-node, .fg-rule, .fg-equip-cell { animation: none; }
}

.fg-rule-example {
  margin: 2px 0 0;
  padding: 8px 10px;
  border-radius: 8px;
  background: var(--vp-c-bg);
  font-size: 12.5px;
  line-height: 1.7;
  color: var(--vp-c-text-3);
}

/* ── 技巧 ── */
.fg-tip {
  margin-top: 14px;
  padding: 12px 16px;
  border-left: 3px solid var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
  border-radius: 0 10px 10px 0;
  font-size: 13.5px;
  line-height: 1.85;
  color: var(--vp-c-text-2);
}

.fg-tip b {
  color: var(--vp-c-brand-1);
}
</style>
