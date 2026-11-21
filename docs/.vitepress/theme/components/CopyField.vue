<script setup lang="ts">
import { ref } from "vue";
const props = defineProps<{ value: string }>();
const status = ref("");

async function copy() {
  try {
    await navigator.clipboard.writeText(props.value);
    status.value = "已复制";
  } catch {
    status.value = "请手动复制";
  }
}
</script>

<template>
  <span class="copy-field">
    <b>{{ value }}</b>
    <button type="button" :aria-label="`复制坐标 ${value}`" @click="copy">{{ status || "复制" }}</button>
    <span class="visually-hidden" role="status">{{ status }}</span>
  </span>
</template>

<style scoped>
.copy-field { display: inline-flex; align-items: center; flex-wrap: wrap; gap: 6px; white-space: nowrap; min-width: 0; }
.copy-field b { font-variant-numeric: tabular-nums; }
.copy-field button { border: 1px solid var(--field-line); padding: 2px 8px; min-height: 30px; border-radius: 6px; font-size: 12px; font-weight: 650; color: var(--field-accent); background: var(--field-paper); }
.copy-field button:hover { border-color: var(--field-accent); }
.visually-hidden { position: absolute; width: 1px; height: 1px; padding: 0; overflow: hidden; white-space: nowrap; clip-path: inset(50%); }
</style>
