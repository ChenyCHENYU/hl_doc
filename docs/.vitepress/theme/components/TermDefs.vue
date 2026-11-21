<script setup lang="ts">
import { highlight } from "../text";

interface TermDef {
  term: string;
  def: string;
}

defineProps<{ items: TermDef[] }>();
</script>

<template>
  <div class="td-grid">
    <div v-for="t in items" :key="t.term" class="td-card">
      <div class="td-term">{{ t.term }}</div>
      <div class="td-def" v-html="highlight(t.def)"></div>
    </div>
  </div>
</template>

<style scoped>
.td-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 12px;
  margin: 14px 0 22px;
}

.td-card {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  padding: 14px 16px;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.td-card:hover {
  border-color: rgba(184, 134, 11, 0.4);
  box-shadow: 0 6px 18px rgba(184, 134, 11, 0.1);
}

.dark .td-card:hover {
  border-color: rgba(240, 201, 78, 0.4);
  box-shadow: 0 6px 18px rgba(240, 201, 78, 0.14);
}

.td-term {
  font-size: 14px;
  font-weight: 700;
  color: var(--vp-c-brand-1);
  margin-bottom: 6px;
}

.td-def {
  font-size: 13.5px;
  line-height: 1.75;
  color: var(--vp-c-text-2);
}
</style>

<style>
.td-def .hl-key {
  color: var(--vp-c-brand-1);
  font-weight: 700;
}
</style>
