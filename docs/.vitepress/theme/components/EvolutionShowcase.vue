<script setup lang="ts">
import { computed, ref } from "vue";
import { data } from "../home/catalog.data";
import { EVO_ELEMENTS } from "../evolution";
import { assetUrl } from "../assets";

const emit = defineEmits<{ preview: [event: MouseEvent, id: number, orderedIds: number[]] }>();
const index = ref(0);
const active = computed(() => data.lineages[index.value]);
const orderedIds = computed(() => active.value?.chain.map(pet => pet.id) ?? []);
const missingArt = ref(new Set<number>());

const rules = [
  { name: "进化条件", value: "500 级，忠诚 100" },
  { name: "防止变异", value: "在同属性地图进化" },
  { name: "终级宠获取", value: "两只 1000 级双幻化三级宠" },
  { name: "勋章继承", value: "进化后全额继承" },
];
</script>

<template>
  <div v-if="active" class="evolution-preview">
    <div class="element-options" role="group" aria-label="按五行查看示例系谱">
      <button
        v-for="(lineage, i) in data.lineages"
        :key="lineage.element"
        type="button"
        :aria-pressed="i === index"
        :style="{ '--element-accent': EVO_ELEMENTS[lineage.element].color }"
        @click="index = i"
      >
        <span></span>{{ EVO_ELEMENTS[lineage.element].label }}系
      </button>
    </div>

    <ol :aria-label="`${EVO_ELEMENTS[active.element].label}系进化顺序`" class="lineage">
      <li v-for="(pet, i) in active.chain" :key="pet.id">
        <a :href="`/pets/?pet=${pet.id}`" class="lineage-pet vp-raw" aria-haspopup="dialog" @click="emit('preview', $event, pet.id, orderedIds)">
          <span class="lineage-art">
            <img
              v-if="pet.image && !missingArt.has(pet.id)"
              :src="assetUrl(pet.image)"
              width="72"
              height="72"
              alt=""
              loading="lazy"
              @error="missingArt.add(pet.id)"
            />
            <b v-else aria-hidden="true">{{ EVO_ELEMENTS[pet.element]?.label ?? "宠" }}</b>
          </span>
          <strong>{{ pet.name }}</strong>
          <small>{{ i === 0 ? "起点" : (i === active.chain.length - 1 ? "链尾" : `进化 ${i}`) }}</small>
        </a>
        <span v-if="pet.evolveIllegal" class="lineage-branch">变异分支：{{ pet.evolveIllegal }}</span>
      </li>
    </ol>

    <dl class="lineage-rules">
      <div v-for="rule in rules" :key="rule.name">
        <dt>{{ rule.name }}</dt>
        <dd>{{ rule.value }}</dd>
      </div>
    </dl>

    <div class="lineage-links" aria-label="进化资料">
      <a href="/guide/library/lib-011">进化幻化全攻略</a>
      <a href="/guide/library/lib-012">五转飞养宠与宠物技能</a>
      <a href="/advanced/charts">2026 宠物进化表</a>
    </div>
  </div>
</template>

<style scoped>
.evolution-preview { padding: 15px; border: 1px solid var(--field-line); border-radius: 10px; background: var(--field-paper); }
.element-options { display: flex; flex-wrap: wrap; gap: 7px; padding-bottom: 13px; border-bottom: 1px solid var(--field-line); }
.element-options button { display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; border: 1px solid var(--field-line); border-radius: 6px; color: var(--field-muted); background: var(--field-bg); font-size: 13px; min-height: 38px; }
.element-options button:hover, .element-options button[aria-pressed="true"] { border-color: var(--field-accent); color: var(--field-ink); }
.element-options button[aria-pressed="true"] { background: var(--field-tint); font-weight: 750; }
.element-options button span { width: 8px; height: 8px; border-radius: 50%; background: var(--element-accent); }
.lineage { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(0, 1fr); align-items: start; gap: 18px; padding: 0; margin: 14px 0; list-style: none; }
.lineage li { position: relative; display: grid; gap: 4px; min-width: 0; }
.lineage li:not(:last-child)::after { content: "→"; position: absolute; inset-block-start: 27px; inset-inline-end: -16px; color: var(--field-accent); }
.lineage-pet { display: grid; grid-template-columns: minmax(0, 62px) minmax(0, 1fr); grid-template-areas: "art name" "art tier"; align-items: end; gap: 1px 8px; padding: 6px 8px; min-height: 72px; border: 1px solid var(--field-line); border-radius: 8px; }
.lineage-pet:hover { border-color: var(--field-accent); }
.lineage-art { grid-area: art; align-self: center; width: 100%; height: 56px; display: grid; place-items: center; border-radius: 6px; background: var(--field-bg); overflow: hidden; }
.lineage-art img { width: 100%; height: 100%; object-fit: contain; }
.lineage-art b { color: var(--field-accent); font-family: var(--field-serif); font-size: 20px; }
.lineage-pet strong { grid-area: name; color: var(--field-ink); font-size: 14px; line-height: 1.4; overflow-wrap: anywhere; }
.lineage-pet small { grid-area: tier; align-self: start; color: var(--field-muted); font-size: 12px; }
.lineage-branch { color: var(--field-muted); font-size: 12px; line-height: 1.4; padding-inline-start: 3px; overflow-wrap: anywhere; }
.lineage-rules { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); margin: 0; padding: 10px 0; border-block: 1px solid var(--field-line); gap: 8px 12px; }
.lineage-rules dt { color: var(--field-accent); font-weight: 700; font-size: 12px; }
.lineage-rules dd { margin: 0; color: var(--field-ink); font-size: 13px; line-height: 1.6; }
.lineage-links { display: flex; gap: 6px 15px; flex-wrap: wrap; padding-top: 10px; color: var(--field-accent); font-size: 13px; }
.lineage-links a:hover { text-decoration: underline; text-underline-offset: 3px; }
@media (max-width: 760px) {
  .evolution-preview { padding: 11px; }
  .lineage { grid-auto-flow: row; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px 14px; }
  .lineage li:not(:last-child)::after { inset-inline-end: -13px; }
  .lineage li:nth-child(even)::after { display: none; }
  .lineage-pet { grid-template-columns: minmax(0, 46px) minmax(0, 1fr); gap: 1px 5px; padding: 5px; min-height: 58px; }
  .lineage-art { height: 46px; }
  .lineage-rules { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
</style>
