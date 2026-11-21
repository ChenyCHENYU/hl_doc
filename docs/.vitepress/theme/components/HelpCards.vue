<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRouter } from "vitepress";
import { highlight } from "../text";
import cardsData from "../../data/help-cards.json";

interface CardEntry {
  cat: string;
  topic: string;
  src: string;
  intro: string[];
  terms: { term: string; def: string }[];
  plain: string[];
  tips: string[];
  sections?: { title: string | null; terms: { term: string; def: string }[]; paras: string[] }[];
}

function isStep(ln: string): boolean {
  return /^(\d{1,2}[、.．)）]|[一二三四五六七八九十][、.．])/u.test(ln);
}

// 剥掉段落自带的编号前缀（步骤条自己有计数器，避免序号重复）
const NUM_HEAD = /^\s*(?:\d{1,2}[、.．)）]|[一二三四五六七八九十]+[、.．]|（[一二三四五六七八九十]+）)\s*/;
function stripNum(ln: string): string {
  return ln.replace(NUM_HEAD, "");
}

// 短问句/短语 = 原文的小节标题（"如何使用武功PK？""武功PK有什么限制？"）
function isHeading(ln: string): boolean {
  const t = ln.trim();
  if (t.length > 16) return false;
  if (t.endsWith("？") || t.endsWith("？")) return true;
  if (/^(如何|什么|为什么|哪些|怎么|怎样)/.test(t) && t.length <= 14) return true;
  return t.length <= 8 && !/[。；，,]$/u.test(t);
}

type Block = { kind: "h"; text: string } | { kind: "steps"; items: string[] } | { kind: "p"; text: string };

// 把一组原文段落编译成 填标题/步骤组/要点块，保持原文顺序
function compileBlocks(paras: string[]): Block[] {
  const blocks: Block[] = [];
  const rest: { block: Block; ops: boolean }[] = [];
  let steps: string[] | null = null;
  const flushSteps = () => {
    if (steps && steps.length) blocks.push({ kind: "steps", items: steps });
    steps = null;
  };
  for (const raw of paras) {
    const t = raw.trim();
    if (isHeading(t)) {
      flushSteps();
      blocks.push({ kind: "h", text: t });
    } else if (isStep(t)) {
      (steps ??= []).push(stripNum(t));
    } else {
      flushSteps();
      rest.push({ block: { kind: "p", text: t }, ops: OP_RE.test(t) });
    }
  }
  flushSteps();
  // 无编号的连续操作描述（幻化/进化这类）→ 合成一组步骤
  if (rest.length >= 3 && rest.filter((r) => r.ops).length >= Math.ceil(rest.length * 0.6)) {
    blocks.push({ kind: "steps", items: rest.map((r) => r.block.text) });
  } else {
    blocks.push(...rest.map((r) => r.block));
  }
  return blocks;
}

// 整句警示（命名禁则 / 删号等）单独渲染为警告行
const WARN_LINE = /注意|请勿|不要|千万|禁止|删号|封号|举报/;
function warnLine(s: string): boolean {
  return WARN_LINE.test(s);
}

// intro 首行常是源文档的小节标题，与专题名重复 → 过滤短标题行；同时拆开内嵌换行
function pickIntro(c: CardEntry): string[] {
  return c.intro
    .flatMap((p) => p.split(/[\r\n]+/))
    .map((p) => p.trim())
    .filter((p) => p.length > 10);
}

// 长段落按句拆行，避免文字墙；过短碎片并回前句
function sentences(p: string): string[] {
  if (p.length <= 90) return [p];
  const parts = p.split(/(?<=[。！？；])/).filter((s) => s.trim());
  const out: string[] = [];
  for (const s of parts) {
    if (out.length && s.trim().length < 8) out[out.length - 1] += s;
    else out.push(s);
  }
  return out;
}

// 操作型动词（无编号的连续操作描述 → 合成步骤组）
const OP_RE = /点击|双击|选择|输入|打开|放置|弹出|确认|预览|拖动|按下/;

// 页签徽章 = 内容块总量（步骤/要点/词条），操作类专题不再显示 0
function contentCount(c: CardEntry): number {
  if (c.sections?.length) {
    return c.sections.reduce((n, s) => n + s.paras.length + s.terms.length, 0);
  }
  return c.plain.length + c.terms.length + c.tips.length;
}

const props = defineProps<{ cat: string }>();
const entries = computed(() => (cardsData as CardEntry[]).filter((c) => c.cat === props.cat));
const active = ref(0);
const cur = computed(() => entries.value[active.value] ?? null);


// 路由离开本页时重置页签
const router = useRouter();
watch(
  () => router.route.path,
  () => {
    active.value = 0;
  }
);

// 切换页签后把面板滚回可视区（短专题在长专题之后会被留在屏幕外）
function switchTo(i: number) {
  active.value = i;
  requestAnimationFrame(() => {
    const panel = document.querySelector(".ht-panel");
    if (!panel) return;
    const top = panel.getBoundingClientRect().top + window.scrollY - 130;
    if (window.scrollY > top - 40) {
      window.scrollTo({ top: Math.max(top, 0), behavior: "smooth" });
    }
  });
}
</script>

<template>
  <div v-if="cur" class="ht">
    <div class="ht-tabs" role="tablist">
      <button
        v-for="(c, i) in entries"
        :key="c.topic + c.src"
        class="ht-tab"
        :class="{ active: i === active }"
        role="tab"
        :aria-selected="i === active"
        @click="switchTo(i)"
      >
        <span class="ht-tab-name">{{ c.topic }}</span>
        <span class="ht-tab-count">{{ contentCount(c) }}</span>
      </button>
    </div>

    <div class="ht-panel" :key="cur.topic + cur.src">
      <header class="ht-head">
        <div class="ht-head-main">
          <div class="ht-kicker">{{ cur.cat }} · 专题</div>
          <h2 class="ht-title">{{ cur.topic }}</h2>
        </div>
        <span class="ht-chips">
          <span class="ht-count-chip">{{ cur.terms.length }} 词条</span>
        </span>
      </header>

      <p v-for="p in pickIntro(cur)" :key="p" class="hc-lead" v-html="highlight(p)"></p>

      <template v-if="cur.sections && cur.sections.length">
        <template v-for="(sc, si) in cur.sections" :key="'sc' + si">
          <div v-if="sc.title" class="hc-sec-title">{{ sc.title }}</div>
          <template v-for="(b, bi) in compileBlocks(sc.paras)" :key="'b' + bi">
            <div v-if="b.kind === 'h'" class="hc-sec-title">{{ b.text }}</div>
            <ol v-else-if="b.kind === 'steps'" class="hc-steps">
              <li v-for="(q, qi) in b.items" :key="qi" v-html="highlight(q)"></li>
            </ol>
            <div v-else class="hc-key">
              <p
                v-for="(s, i2) in sentences(b.text)"
                :key="i2"
                :class="{ 'is-warn-line': warnLine(s) }"
                v-html="highlight(s)"
              ></p>
            </div>
          </template>
          <div v-if="sc.terms.length" class="td-grid">
            <div v-for="t in sc.terms" :key="t.term" class="td-card">
              <div class="td-term">{{ t.term }}</div>
              <div class="td-def" v-html="highlight(t.def)"></div>
            </div>
          </div>
        </template>
      </template>

      <template v-else>
        <div v-if="cur.plain.length || cur.tips.length" class="hc-keys">
          <div class="hc-keys-title">核心要点</div>
          <template v-for="(b, bi) in compileBlocks(cur.plain)" :key="'b' + bi">
            <div v-if="b.kind === 'h'" class="hc-sec-title">{{ b.text }}</div>
            <ol v-else-if="b.kind === 'steps'" class="hc-steps">
              <li v-for="(q, qi) in b.items" :key="qi" v-html="highlight(q)"></li>
            </ol>
            <div v-else class="hc-key">
              <p
                v-for="(s, i2) in sentences(b.text)"
                :key="i2"
                :class="{ 'is-warn-line': warnLine(s) }"
                v-html="highlight(s)"
              ></p>
            </div>
          </template>
        </div>

        <div v-if="cur.terms.length" class="ht-terms">
          <div class="hc-terms-title">词条 · {{ cur.terms.length }} 项</div>
          <div class="td-grid">
            <div v-for="t in cur.terms" :key="t.term" class="td-card">
              <div class="td-term">{{ t.term }}</div>
              <div class="td-def" v-html="highlight(t.def)"></div>
            </div>
          </div>
        </div>
      </template>

      <div v-for="t in cur.tips" :key="'tip' + t" class="hc-key is-tip" v-html="highlight(t)"></div>

      <footer class="ht-foot">
        <button v-if="active > 0" class="ht-page" @click="switchTo(active - 1)">‹ 上一篇：{{ entries[active - 1].topic }}</button>
        <span v-else class="ht-page is-disabled">已是第一篇</span>
        <span class="ht-src">来源：游戏内宝典 · {{ cur.src }}</span>
        <button v-if="active < entries.length - 1" class="ht-page is-next" @click="switchTo(active + 1)">下一篇：{{ entries[active + 1].topic }} ›</button>
        <span v-else class="ht-page is-disabled">已是最后一篇</span>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.ht {
  margin: 18px 0 30px;
}

/* ── 页签条：吸顶，实底容器 ── */
.ht-tabs {
  position: sticky;
  top: calc(var(--vp-nav-height, 56px) + 10px);
  z-index: 20;
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 10px 12px;
  margin: 6px 0 20px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 14px;
  background: var(--vp-c-bg);
  box-shadow: 0 6px 24px -12px rgba(0, 0, 0, 0.25);
  scrollbar-width: none;
}

.ht-tabs::-webkit-scrollbar {
  display: none;
}

.ht-tab {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  min-height: 36px;
  padding: 6px 16px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  background: transparent;
  color: var(--vp-c-text-1);
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: border-color 0.15s, color 0.15s, background 0.15s;
}

.ht-tab:hover {
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
}

.ht-tab.active {
  background: var(--vp-c-brand-1);
  color: var(--vp-c-bg);
  font-weight: 700;
}

.ht-tab-count {
  font-size: 11.5px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  opacity: 0.72;
}

/* ── 面板：卡片容器（与页面背景拉开层次）── */
.ht-panel {
  border: 1px solid var(--vp-c-divider);
  border-radius: 16px;
  background: var(--vp-c-bg);
  padding: 24px 28px 22px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06), 0 10px 32px -18px rgba(0, 0, 0, 0.25);
  animation: ht-in 0.22s ease both;
}

.dark .ht-panel {
  background: rgba(255, 255, 255, 0.028);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04), 0 12px 36px -20px rgba(0, 0, 0, 0.55);
}

@keyframes ht-in {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .ht-panel {
    animation: none;
  }
}

.ht-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px 16px;
  margin-bottom: 16px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--vp-c-divider);
}

.ht-head-main {
  min-width: 0;
}

.ht-kicker {
  font-size: 11.5px;
  font-weight: 800;
  letter-spacing: 0.18em;
  color: var(--vp-c-brand-1);
  margin-bottom: 4px;
}

.ht-title {
  margin: 0;
  font-size: 22px;
  font-weight: 800;
  letter-spacing: 0.02em;
  color: var(--vp-c-text-1);
}

.ht-chips {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding-bottom: 3px;
}

.ht-count-chip {
  font-size: 12px;
  font-weight: 700;
  color: var(--vp-c-brand-1);
  border: 1px solid var(--vp-c-brand-soft);
  border-radius: 999px;
  padding: 2px 10px;
}

/* ── 词条：词典行式（标签列定宽对齐）── */
.td-grid {
  display: block;
  margin: 10px 0 16px;
}

.td-card {
  display: grid;
  grid-template-columns: 11em 1fr;
  gap: 4px 16px;
  padding: 9px 2px;
  border-bottom: 1px dashed var(--vp-c-divider);
}

.td-card:last-child {
  border-bottom: none;
}

.td-term {
  font-size: 13.5px;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  line-height: 1.7;
}

.td-def {
  font-size: 13.5px;
  line-height: 1.75;
  color: var(--vp-c-text-2);
}

/* ── 底部翻页 ── */
.ht-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 22px;
  padding-top: 14px;
  border-top: 1px solid var(--vp-c-divider);
}

.ht-page {
  min-height: 36px;
  padding: 7px 16px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg);
  color: var(--vp-c-brand-1);
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  transition: border-color 0.15s, transform 0.15s;
}

.ht-page:hover {
  border-color: var(--vp-c-brand-1);
  transform: translateY(-1px);
}

.ht-page.is-disabled {
  color: var(--vp-c-text-3);
  cursor: default;
  transform: none;
  border-style: dashed;
}

.ht-src {
  font-size: 11.5px;
  color: var(--vp-c-text-3);
  font-family: var(--vp-font-family-mono);
}

@media (max-width: 560px) {
  .ht-panel {
    padding: 18px 16px 16px;
  }

  .td-card {
    grid-template-columns: 1fr;
    gap: 2px;
  }

  .ht-title {
    font-size: 18px;
  }
}
</style>

<style>
.hc-lead {
  font-size: 15px;
  line-height: 1.9;
  color: var(--vp-c-text-1);
  margin: 12px 0 16px;
}

/* 要点区不再套色块（面板卡片已是容器），仅保留小节标签 */
.hc-keys {
  margin-bottom: 18px;
}

.hc-keys-title {
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.22em;
  color: var(--vp-c-brand-1);
  margin-bottom: 8px;
}

.hc-key {
  font-size: 13.5px;
  line-height: 1.85;
  color: var(--vp-c-text-2);
  padding-left: 12px;
  border-left: 3px solid var(--vp-c-brand-1);
  margin: 8px 0 0;
}

.hc-key p {
  margin: 0 0 6px;
}

.hc-key p:last-child {
  margin-bottom: 0;
}

/* 整句警示：命名禁则、删号处罚等 */
.hc-key p.is-warn-line {
  display: block;
  margin: 6px 0 0;
  padding: 7px 10px;
  border-left: 3px solid #c0392b;
  border-radius: 0 8px 8px 0;
  background: rgba(192, 57, 43, 0.06);
  color: var(--vp-c-text-2);
}

.dark .hc-key p.is-warn-line {
  background: rgba(231, 76, 60, 0.1);
}

.hc-key.is-tip {
  border-left-color: #2e9e6f;
  background: rgba(46, 158, 111, 0.06);
  border-radius: 0 8px 8px 0;
  padding: 8px 10px;
}

.hc-terms-title {
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.22em;
  color: var(--vp-c-text-3);
  margin-bottom: 10px;
}

.hl-key {
  color: var(--vp-c-brand-1);
  font-weight: 700;
}
</style>

<style>
.hc-sec-title {
  font-size: 13px;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  margin: 16px 0 8px;
  padding-left: 10px;
  border-left: 3px solid var(--vp-c-brand-1);
}

.hc-steps {
  margin: 10px 0 14px;
  padding: 0;
  list-style: none;
  counter-reset: st;
}

.hc-steps li {
  counter-increment: st;
  position: relative;
  padding: 0 0 14px 34px;
  font-size: 13.5px;
  line-height: 1.8;
  color: var(--vp-c-text-2);
}

.hc-steps li:last-child {
  padding-bottom: 4px;
}

/* 序号圆点 */
.hc-steps li::before {
  content: counter(st);
  position: absolute;
  left: 0;
  top: 0;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 11.5px;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
  border: 1px solid var(--vp-c-brand-soft);
}

/* 竖向连接线 */
.hc-steps li::after {
  content: "";
  position: absolute;
  left: 11px;
  top: 26px;
  bottom: 0;
  width: 2px;
  border-radius: 2px;
  background: var(--vp-c-brand-soft);
}

.hc-steps li:last-child::after {
  display: none;
}
</style>
