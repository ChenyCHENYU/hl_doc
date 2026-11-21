<script setup lang="ts">
import { computed } from "vue";
import flowsData from "../../data/quest-flows.json";
import codex from "../../data/pet-codex.json";
import { EVO_ELEMENTS } from "../evolution";

const props = defineProps<{ flow: string }>();

interface Step {
  n: number;
  text: string;
  note: string;
}
interface Flow {
  title: string;
  lead: string;
  prep: { term: string; text: string }[];
  steps: Step[];
}

const flow = computed<Flow | null>(() => (flowsData as Record<string, Flow>)[props.flow] ?? null);

// 宠物名 → 图鉴信息（按名长降序，避免短名截断长名）
type Pet = { id: number; name: string; element: string; img: string | null; color: string };
const EL = EVO_ELEMENTS as Record<string, { label: string; color: string }>;
const petByName = new Map<string, Pet>();
for (const p of codex as any[]) {
  petByName.set(p.name, {
    id: p.id,
    name: p.name,
    element: p.element,
    img: p.image?.file ?? null,
    color: EL[p.element]?.color ?? "#b8860b",
  });
}
const petNames = [...petByName.keys()].sort((a, b) => b.length - a.length);

function petsIn(text: string): Pet[] {
  const found: Pet[] = [];
  for (const nm of petNames) {
    if (found.length >= 6) break;
    if (text.includes(nm)) {
      const p = petByName.get(nm)!;
      if (!found.some((f) => f.name === nm)) found.push(p);
    }
  }
  return found;
}

function escapeHtml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// 步骤文本 → 宠物名替换为带头像的内链 chip
function richText(text: string): string {
  let html = escapeHtml(text);
  let used = 0;
  for (const nm of petNames) {
    if (used >= 3) break;
    if (!html.includes(nm)) continue;
    const p = petByName.get(nm)!;
    const img = p.img
      ? `<img src="/hl-assets/hl/pets/${p.img}" alt="${nm}" loading="lazy">`
      : `<i style="background:${p.color}">${EL[p.element]?.label ?? "宠"}</i>`;
    html = html.replace(
      new RegExp(nm, "g"),
      `<a class="qf-chip" href="/pets/${p.id}" title="查看 ${nm} 图鉴">${img}<b>${nm}</b></a>`
    );
    used++;
  }
  return html;
}

// 总况
const stats = computed(() => {
  if (!flow.value) return null;
  const f = flow.value;
  const prepPets = f.prep.flatMap((p) => petsIn(p.term + p.text));
  const stepPets = f.steps.flatMap((s) => petsIn(s.text));
  const allPets = [...new Map([...prepPets, ...stepPets].map((p) => [p.name, p])).values()];
  const rewardCount = f.steps.filter((s) => s.text.includes("行令")).length;
  return {
    prepCount: f.prep.length,
    stepCount: f.steps.length,
    rewardLabel: props.flow === "water" ? "水行令" : "火行令",
    rewardCount,
    pets: allPets,
  };
});
</script>

<template>
  <div v-if="flow && stats" class="qf">
    <!-- ── 总况 ── -->
    <section class="qf-overview">
      <div class="qf-stat">
        <b>{{ stats.prepCount }}</b>
        <span>准备项</span>
      </div>
      <div class="qf-stat">
        <b>{{ stats.stepCount }}</b>
        <span>任务步骤</span>
      </div>
      <div class="qf-stat">
        <b>{{ stats.rewardCount }}</b>
        <span>{{ stats.rewardLabel }}</span>
      </div>
      <div class="qf-stat is-pets">
        <b>{{ stats.pets.length }}</b>
        <span>出场宠物</span>
      </div>
      <div v-if="stats.pets.length" class="qf-pets">
        <a v-for="p in stats.pets" :key="p.name" :href="`/pets/${p.id}`" class="qf-pet" :title="`查看 ${p.name} 图鉴`">
          <img v-if="p.img" :src="`/hl-assets/hl/pets/${p.img}`" :alt="p.name" loading="lazy" />
          <i v-else :style="{ background: p.color }">{{ EL[p.element]?.label ?? "宠" }}</i>
          <b>{{ p.name }}</b>
        </a>
      </div>
    </section>

    <p v-if="flow.lead" class="qf-lead">{{ flow.lead.replace(/\/+$/, "").trim() }}</p>

    <!-- ── 准备清单 ── -->
    <section class="qf-sec">
      <h3 class="qf-title">出发前准备 · {{ flow.prep.length }} 项</h3>
      <div class="qf-prep">
        <div v-for="p in flow.prep" :key="p.term" class="qf-prep-card">
          <b class="qf-prep-term">{{ p.term }}</b>
          <p class="qf-prep-text" v-html="richText(p.text || '见步骤内说明')"></p>
        </div>
      </div>
    </section>

    <!-- ── 步骤流 ── -->
    <section class="qf-sec">
      <h3 class="qf-title">任务流程 · {{ flow.steps.length }} 步</h3>
      <ol class="qf-steps">
        <li v-for="s in flow.steps" :key="s.n">
          <span class="qf-num">{{ s.n }}</span>
          <div class="qf-step-body">
            <p class="qf-step-text" v-html="richText(s.text)"></p>
            <p v-if="s.note" class="qf-step-note" v-html="richText(s.note)"></p>
          </div>
        </li>
      </ol>
    </section>
  </div>
</template>

<style scoped>
.qf {
  margin: 20px 0 30px;
}

/* ── 总况 ── */
.qf-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
  gap: 10px;
  padding: 16px 20px;
  border: 1px solid var(--vp-c-brand-soft);
  background: var(--vp-c-brand-soft);
  border-radius: 14px;
  margin-bottom: 8px;
}

.qf-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 6px 4px;
}

.qf-stat {
  animation: hl-pop 0.5s ease both;
}

.qf-stat:nth-child(1) { animation-delay: 0.03s; }
.qf-stat:nth-child(2) { animation-delay: 0.09s; }
.qf-stat:nth-child(3) { animation-delay: 0.15s; }
.qf-stat:nth-child(4) { animation-delay: 0.21s; }

@media (prefers-reduced-motion: reduce) {
  .qf-stat { animation: none; }
}

.qf-stat b {
  font-size: 26px;
  font-weight: 800;
  line-height: 1.1;
  color: var(--vp-c-brand-1);
  font-variant-numeric: tabular-nums;
}

.qf-stat span {
  font-size: 12px;
  color: var(--vp-c-text-3);
}

.qf-stat.is-pets {
  grid-column: span 1;
}

.qf-pets {
  grid-column: 1 / -1;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding-top: 10px;
  margin-top: 6px;
  border-top: 1px dashed var(--vp-c-divider);
}

.qf-pet {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px 4px 5px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  background: var(--vp-c-bg);
  text-decoration: none;
  transition: border-color 0.15s, transform 0.15s;
}

.qf-pet:hover {
  border-color: var(--vp-c-brand-1);
  transform: translateY(-1px);
}

.qf-pet img {
  width: 26px;
  height: 26px;
  object-fit: contain;
  border-radius: 50%;
  background: #fff;
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.05);
}

.qf-pet i {
  width: 26px;
  height: 26px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: #fff;
  font-style: normal;
  font-size: 12px;
  font-weight: 800;
}

.qf-pet b {
  font-size: 13px;
  color: var(--vp-c-text-1);
}

.qf-lead {
  margin: 14px 2px 4px;
  font-size: 14px;
  line-height: 1.9;
  color: var(--vp-c-text-2);
}

/* ── 小节 ── */
.qf-sec {
  margin-top: 24px;
}

.qf-title {
  margin: 0 0 12px;
  font-size: 16px;
  font-weight: 800;
  color: var(--vp-c-text-1);
  padding-left: 10px;
  border-left: 3px solid var(--vp-c-brand-1);
}

/* ── 准备清单 ── */
.qf-prep {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 10px;
}

.qf-prep-card {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 12px 14px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
}

.qf-prep-term {
  font-size: 14px;
  color: var(--vp-c-brand-1);
}

.qf-prep-text {
  margin: 0;
  font-size: 13px;
  line-height: 1.75;
  color: var(--vp-c-text-2);
}

/* ── 步骤流 ── */
.qf-steps {
  margin: 0;
  padding: 0;
  list-style: none;
  counter-reset: qs;
}

.qf-steps li {
  position: relative;
  display: flex;
  gap: 14px;
  padding: 0 0 16px 0;
}

.qf-steps li::before {
  content: "";
  position: absolute;
  left: 17px;
  top: 38px;
  bottom: 0;
  width: 2px;
  border-radius: 2px;
  background: var(--vp-c-brand-soft);
  /* 竖线永远垫在内容之下 */
  z-index: 0;
}

.qf-steps li:last-child::before {
  display: none;
}

.qf-num {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 14px;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  background: var(--vp-c-bg);
  border: 2px solid var(--vp-c-brand-soft);
  font-variant-numeric: tabular-nums;
  z-index: 1;
}

.qf-step-body {
  flex: 1;
  min-width: 0;
  padding-top: 4px;
  position: relative;
  z-index: 1;
  animation: hl-fade-up 0.4s ease both;
}

.qf-steps li:nth-child(1) .qf-step-body { animation-delay: 0.03s; }
.qf-steps li:nth-child(2) .qf-step-body { animation-delay: 0.07s; }
.qf-steps li:nth-child(3) .qf-step-body { animation-delay: 0.11s; }
.qf-steps li:nth-child(4) .qf-step-body { animation-delay: 0.15s; }
.qf-steps li:nth-child(5) .qf-step-body { animation-delay: 0.19s; }
.qf-steps li:nth-child(n+6) .qf-step-body { animation-delay: 0.23s; }

@media (prefers-reduced-motion: reduce) {
  .qf-step-body { animation: none; }
}

.qf-step-text {
  margin: 0;
  font-size: 14px;
  line-height: 1.9;
  color: var(--vp-c-text-2);
}

.qf-step-note {
  margin: 6px 0 0;
  padding: 7px 10px;
  border-left: 3px solid #c08a3e;
  background: rgba(192, 138, 62, 0.08);
  border-radius: 0 8px 8px 0;
  font-size: 12.5px;
  line-height: 1.75;
  color: var(--vp-c-text-3);
}

/* 正文内联宠物 chip */
.qf-step-text :deep(.qf-chip),
.qf-prep-text :deep(.qf-chip),
.qf-step-note :deep(.qf-chip) {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin: 0 2px;
  padding: 1px 9px 1px 2px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  background: var(--vp-c-bg);
  text-decoration: none;
  vertical-align: middle;
  white-space: nowrap;
  transition: border-color 0.15s;
}

.qf-chip:hover {
  border-color: var(--vp-c-brand-1);
}

.qf-chip img {
  width: 20px;
  height: 20px;
  object-fit: contain;
  border-radius: 50%;
  background: #fff;
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.05);
}

.qf-chip i {
  width: 20px;
  height: 20px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: #fff;
  font-style: normal;
  font-size: 11px;
}

.qf-chip b {
  font-size: 12.5px;
  color: var(--vp-c-text-1);
}

@media (max-width: 560px) {
  .qf-steps li {
    gap: 10px;
  }

  .qf-num {
    width: 30px;
    height: 30px;
    font-size: 12.5px;
  }

  .qf-steps li::before {
    left: 14px;
  }
}
</style>
