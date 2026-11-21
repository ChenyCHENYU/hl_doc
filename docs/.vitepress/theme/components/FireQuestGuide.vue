<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import flows from "../../data/quest-flows.json";
import { fireStages } from "../../data/fire-checklist";
import CopyField from "./CopyField.vue";

const storageKey = "hl-fire-checklist-v1";
const materials = flows.fire.prep;
const sourceByStep = new Map(flows.fire.steps.map((step) => [step.n, step]));
const checkedPrep = ref<string[]>([]);
const checkedSteps = ref<number[]>([]);
const onlyRemaining = ref(false);
const openSteps = ref([1]);
const nextStep = computed(() => fireStages.find((step) => !checkedSteps.value.includes(step.n)));
const visible = computed(() => onlyRemaining.value ? fireStages.filter((step) => !checkedSteps.value.includes(step.n)) : fireStages);

function load() {
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) ?? "{}");
    if (Array.isArray(saved.prep)) checkedPrep.value = saved.prep.filter((name: string) => materials.some((material) => material.term === name));
    if (Array.isArray(saved.steps)) checkedSteps.value = saved.steps.filter((n: number) => fireStages.some((step) => step.n === n));
  } catch {
    // This view still works if storage is unavailable.
  }
}
function openStep(n: number) {
  if (!openSteps.value.includes(n)) openSteps.value = [...openSteps.value, n];
  if (checkedSteps.value.includes(n)) onlyRemaining.value = false;
}
function applyHash() {
  const n = Number(location.hash.match(/^#fire-step-(\d+)$/)?.[1]);
  if (fireStages.some((step) => step.n === n)) openStep(n);
}
function syncOpen(event: Event, n: number) {
  const isOpen = (event.currentTarget as HTMLDetailsElement).open;
  if (isOpen && !openSteps.value.includes(n)) openStep(n);
  if (!isOpen && openSteps.value.includes(n)) openSteps.value = openSteps.value.filter((value) => value !== n);
}
onMounted(() => {
  load();
  openSteps.value = nextStep.value ? [nextStep.value.n] : [];
  applyHash();
  window.addEventListener("hashchange", applyHash);
});
onUnmounted(() => window.removeEventListener("hashchange", applyHash));

watch([checkedPrep, checkedSteps], ([prep, steps]) => {
  try {
    localStorage.setItem(storageKey, JSON.stringify({ prep, steps }));
  } catch {
    // Progress can still be tracked for the current visit.
  }
});
</script>

<template>
  <div class="field-ui field-reading fire-guide">
    <div class="fire-summary">
      <div>
        <strong>收集 19 条火行令</strong>
        <p>先安排限时材料。出发前勾选已备物品，游戏里按步骤查 NPC 和坐标。</p>
      </div>
      <a v-if="nextStep" :href="`#fire-step-${nextStep.n}`" @click="openStep(nextStep.n)">继续第 {{ nextStep.n }} 步 <span aria-hidden="true">↓</span></a>
      <b v-else>全部完成</b>
    </div>

    <section aria-labelledby="fire-time">
      <h2 id="fire-time">先排时间</h2>
      <div class="fire-times">
        <a href="#fire-step-10" @click="openStep(10)"><b>20:00–21:00</b><span>玉洁桥 · 换冰晶</span></a>
        <a href="#fire-step-9" @click="openStep(9)"><b>21:00</b><span>沙城竞技场 · 换玉佩</span></a>
        <a href="#fire-step-15" @click="openStep(15)"><b>22:00–24:00</b><span>时间的伤口 · 换绣球花</span></a>
        <a href="#fire-step-7" @click="openStep(7)"><b>整点</b><span>水城宝洞 · 打钥匙</span></a>
      </div>
      <p class="fire-note">时段据玩家原攻略整理，请对照游戏内时间。第 11 步烟火购买时段仍需核对。</p>
    </section>

    <section aria-labelledby="fire-materials">
      <h2 id="fire-materials">出发前准备 <small>{{ checkedPrep.length }}/{{ materials.length }}</small></h2>
      <ul class="fire-materials">
        <li v-for="material in materials" :key="material.term">
          <label><input v-model="checkedPrep" :value="material.term" type="checkbox" /><span>{{ material.term }}</span></label>
          <details><summary>怎么获得</summary><p>{{ material.text }}</p><a v-if="material.term === '冰晶'" href="/maps/#ice-crystal">查玉洁桥坐标与时段 →</a></details>
        </li>
      </ul>
    </section>

    <section aria-labelledby="fire-route">
      <div class="fire-step-heading">
        <h2 id="fire-route">火行令路线 <small>{{ checkedSteps.length }}/{{ fireStages.length }}</small></h2>
        <label><input v-model="onlyRemaining" type="checkbox" /> 只看未完成</label>
      </div>
      <progress :value="checkedSteps.length" :max="fireStages.length" aria-label="火行令收集进度" />
      <p class="fire-note">勾选状态保存在当前浏览器。第 13、18、19 步前先核对宠物条件或战斗准备。</p>
      <ol v-if="visible.length" class="fire-steps">
        <li v-for="step in visible" :id="`fire-step-${step.n}`" :key="step.n">
          <details :open="openSteps.includes(step.n)" @toggle="syncOpen($event, step.n)">
            <summary>
              <span class="step-number">{{ String(step.n).padStart(2, "0") }}</span>
              <b>{{ step.title }}</b>
              <span v-if="checkedSteps.includes(step.n)" class="step-done">已完成</span>
            </summary>
            <div class="fire-step-body">
              <p v-if="step.before" class="fire-required"><b>先准备</b> {{ step.before }}</p>
              <ul class="fire-stops" aria-label="沿途地点">
                <li v-for="[place, npc, point] in step.stops" :key="`${place}-${npc}`">
                  <div><span>{{ place }}</span><strong>{{ npc }}</strong></div>
                  <CopyField v-if="point" :value="point" />
                </li>
              </ul>
              <p v-if="step.risk" class="fire-risk">{{ step.risk }}</p>
              <p class="step-reward"><b>本步拿到</b> 火行令 {{ step.n }}<span v-if="step.result && step.n !== 19"> · {{ step.result }}</span></p>
              <a v-if="step.n === 10" href="/maps/#ice-crystal">查玉洁桥位置 →</a>
              <details v-if="sourceByStep.get(step.n)" class="step-source">
                <summary>原攻略说明</summary>
                <p>{{ sourceByStep.get(step.n)?.text }}</p>
                <p v-if="sourceByStep.get(step.n)?.note">{{ sourceByStep.get(step.n)?.note }}</p>
              </details>
              <label class="step-check"><input v-model="checkedSteps" :value="step.n" type="checkbox" /> 已取得火行令 {{ step.n }}</label>
            </div>
          </details>
        </li>
      </ol>
      <p v-else role="status">19 步都已标记完成。</p>
    </section>
  </div>
</template>

<style scoped>
.fire-guide { margin: 16px auto 34px; }
.fire-summary { display: flex; align-items: center; justify-content: space-between; gap: 14px; padding: 17px 20px; border-radius: 13px; border: 1px solid var(--field-line); background: var(--field-tint); }
.fire-summary strong { font-family: var(--field-serif); font-size: 23px; color: var(--field-ink); }
.fire-summary p { color: var(--field-muted); margin: 2px 0 0; }
.fire-summary a { flex: none; background: var(--field-action); color: var(--field-action-text); border-radius: 8px; padding: 6px 11px; font-size: 14px; text-decoration: none; }
.fire-guide section { margin-top: 22px; }
.fire-guide h2 { margin: 0 0 12px; padding: 0; border: none; font-size: clamp(22px, 4vw, 28px); }
.fire-guide h2 small { margin-left: 4px; color: var(--field-muted); font: 650 14px/1.5 var(--vp-font-family-base); font-variant-numeric: tabular-nums; }
.fire-times { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; }
.fire-times a { display: grid; gap: 2px; padding: 9px 12px; border: 1px solid var(--field-line); border-radius: 10px; background: var(--field-paper); color: var(--field-fire); text-decoration: none; }
.fire-times a:hover { border-color: var(--field-fire); }
.fire-times span, .fire-note { font-size: 13px; color: var(--field-muted); }
.fire-note { margin: 8px 0; }
.fire-materials, .fire-steps, .fire-stops { padding: 0; list-style: none; }
.fire-materials { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 7px 11px; }
.fire-materials li { margin: 0; border: 1px solid var(--field-line); padding: 5px 10px; border-radius: 9px; background: var(--field-paper); }
.fire-materials label, .step-check { display: flex; align-items: center; gap: 8px; min-height: 34px; font-weight: 700; cursor: pointer; }
.fire-guide input { accent-color: var(--field-wood); width: 16px; height: 16px; flex: none; }
.fire-materials details, .step-source { font-size: 14px; color: var(--field-muted); }
.fire-materials details summary, .step-source summary { cursor: pointer; color: var(--field-accent); }
.fire-materials details p, .step-source p { margin: 4px 0; }
.fire-step-heading { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: baseline; gap: 4px 14px; }
.fire-step-heading label { font-size: 14px; color: var(--field-muted); display: inline-flex; align-items: center; gap: 5px; }
.fire-guide progress { width: 100%; height: 9px; accent-color: var(--field-wood); }
.fire-steps > li { margin: 0 0 7px; scroll-margin-top: 105px; }
.fire-steps > li > details { border: 1px solid var(--field-line); border-radius: 11px; background: var(--field-paper); }
.fire-steps > li > details > summary { display: flex; align-items: center; gap: 10px; padding: 9px 13px; cursor: pointer; min-height: 48px; }
.fire-steps > li > details > summary::after { content: "+"; margin-left: auto; color: var(--field-accent); }
.fire-steps > li > details[open] > summary::after { content: "−"; }
.step-number { font-variant-numeric: tabular-nums; min-width: 22px; color: var(--field-fire); font-weight: 770; }
.step-done { color: var(--field-wood); font-size: 13px; }
.fire-step-body { padding: 0 13px 9px; }
.fire-step-body p { margin: 6px 0; }
.fire-required b, .step-reward b { color: var(--field-accent); margin-right: 5px; }
.fire-stops { margin: 7px 0; }
.fire-stops li { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 2px 8px; padding: 5px 0; margin: 0; border-bottom: 1px solid var(--field-line); }
.fire-stops li > div { display: flex; align-items: baseline; gap: 7px; flex-wrap: wrap; }
.fire-stops li > div span { color: var(--field-muted); font-size: 13px; }
.fire-risk { padding: 6px 9px; border-radius: 6px; color: var(--field-fire); background: var(--field-tint); }
.step-check { margin-top: 7px; border-top: 1px solid var(--field-line); color: var(--field-wood); }
@media (max-width: 590px) {
  .fire-summary { align-items: flex-start; flex-direction: column; padding: 13px; }
  .fire-times { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .fire-materials { grid-template-columns: 1fr; }
}
</style>
