<script setup lang="ts">
import { computed, defineAsyncComponent, nextTick, onBeforeUnmount, ref, useId } from "vue";
import codex from "../../data/pet-codex.json";

const props = defineProps<{ petIds?: number[] }>();
const emit = defineEmits<{ close: [] }>();
const PetDetail = defineAsyncComponent(() => import("./PetDetail.vue"));

const titleId = useId();
const activePet = ref<(typeof codex)[number] | null>(null);
const dialog = ref<HTMLDialogElement | null>(null);
const scrollArea = ref<HTMLElement | null>(null);
const title = ref<HTMLElement | null>(null);
const activeIndex = computed(() => props.petIds?.indexOf(activePet.value?.id ?? NaN) ?? -1);
let opener: HTMLElement | null = null;

function supportsModal() {
  return typeof HTMLDialogElement !== "undefined" && typeof HTMLDialogElement.prototype.showModal === "function";
}

async function open(id: number, trigger?: HTMLElement) {
  if (!supportsModal()) return;
  const pet = codex.find((entry) => entry.id === id);
  if (!pet) return;
  opener = trigger ?? null;
  activePet.value = pet;
  await nextTick();
  if (!dialog.value || dialog.value.open) return;
  dialog.value.showModal();
  document.documentElement.classList.add("pet-preview-open");
}

function openFromLink(event: MouseEvent, id: number) {
  if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  if (!supportsModal() || !codex.some((entry) => entry.id === id)) return;
  event.preventDefault();
  void open(id, event.currentTarget as HTMLElement);
}

function dismiss() {
  dialog.value?.close();
}

function reset() {
  activePet.value = null;
  document.documentElement.classList.remove("pet-preview-open");
  if (opener?.isConnected) opener.focus({ preventScroll: true });
  opener = null;
  emit("close");
}

async function selectPet(id: number, focusTitle = false) {
  const pet = codex.find((entry) => entry.id === id);
  if (!pet || pet.id === activePet.value?.id) return;
  activePet.value = pet;
  scrollArea.value?.scrollTo({ top: 0 });
  if (focusTitle) {
    await nextTick();
    title.value?.focus({ preventScroll: true });
  }
}

function move(offset: number) {
  if (activeIndex.value < 0) return;
  const id = props.petIds?.[activeIndex.value + offset];
  if (id != null) void selectPet(id);
}

function dismissBackdrop(event: MouseEvent) {
  if (event.target === event.currentTarget) dismiss();
}

onBeforeUnmount(() => {
  if (dialog.value?.open) document.documentElement.classList.remove("pet-preview-open");
});

defineExpose({ open, openFromLink });
</script>

<template>
  <Teleport to="body">
    <dialog
      v-if="activePet"
      ref="dialog"
      class="pet-preview"
      :aria-labelledby="titleId"
      @close="reset"
      @click="dismissBackdrop"
    >
      <div class="pet-preview-shell">
        <header class="pet-preview-header">
          <div>
            <span>{{ activePet.sheet }}</span>
            <h2 :id="titleId" ref="title" tabindex="-1" aria-live="polite">{{ activePet.name }}</h2>
          </div>
          <button class="pet-preview-close" type="button" autofocus aria-label="关闭宠物详情" @click="dismiss">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="m5 5 10 10M15 5 5 15" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
          </button>
        </header>
        <div ref="scrollArea" class="pet-preview-content">
          <PetDetail :id="activePet.id" in-dialog @select="selectPet($event, true)" />
        </div>
        <footer class="pet-preview-footer">
          <div v-if="activeIndex >= 0" class="pet-preview-pagination">
            <button type="button" :disabled="activeIndex <= 0" @click="move(-1)">上一只</button>
            <span>{{ activeIndex + 1 }} / {{ petIds?.length }}</span>
            <button type="button" :disabled="activeIndex >= (petIds?.length ?? 0) - 1" @click="move(1)">下一只</button>
          </div>
          <a :href="`/pets/${activePet.id}`" target="_blank" rel="noopener">独立详情 <span aria-hidden="true">↗</span></a>
        </footer>
      </div>
    </dialog>
  </Teleport>
</template>

<style scoped>
.pet-preview { position: fixed; inset: 0; margin: auto; width: min(880px, calc(100% - 40px)); max-width: none; max-height: min(88dvh, 850px); padding: 0; overflow: hidden; border: 1px solid var(--field-line); border-radius: 16px; background: var(--field-paper); color: var(--field-ink); box-shadow: 0 22px 76px rgb(0 0 0 / 24%); }
.pet-preview::backdrop { background: rgb(12 15 13 / 65%); }
.pet-preview-shell { max-height: min(88dvh, 850px); display: flex; flex-direction: column; }
.pet-preview-header, .pet-preview-footer { display: flex; align-items: center; justify-content: space-between; gap: 8px 14px; flex: none; padding: 12px 18px; }
.pet-preview-header { align-items: flex-start; border-bottom: 1px solid var(--field-line); }
.pet-preview-header > div > span { font-size: 13px; font-weight: 600; color: var(--field-muted); }
.pet-preview-header h2 { margin: 1px 0 0; font-family: var(--field-serif); font-size: 26px; line-height: 1.2; font-weight: 800; color: var(--field-ink); }
.pet-preview-header h2:focus { outline: none; }
.pet-preview-close { display: grid; place-items: center; flex: 0 0 38px; height: 38px; border: 1px solid var(--field-line); border-radius: 8px; color: var(--field-ink); }
.pet-preview-content { min-height: 0; overflow-y: auto; overscroll-behavior: contain; padding: 14px 18px 0; }
.pet-preview-footer { background: var(--field-paper); border-top: 1px solid var(--field-line); font-size: 14px; flex-wrap: wrap; }
.pet-preview-footer a { margin-left: auto; color: var(--field-accent); font-weight: 650; }
.pet-preview-pagination { display: flex; align-items: center; gap: 8px; white-space: nowrap; color: var(--field-muted); }
.pet-preview-pagination button { border: 1px solid var(--field-line); border-radius: 8px; padding: 3px 10px; min-height: 32px; }
.pet-preview-pagination button:disabled { cursor: default; opacity: .52; }
.pet-preview-close:hover, .pet-preview-pagination button:not(:disabled):hover { background: var(--field-tint); border-color: var(--field-accent); }
.pet-preview :is(a, button):focus-visible { outline: 2px solid var(--field-accent); outline-offset: 3px; }
.pet-preview .pet-preview-close:focus-visible { border-color: transparent; outline-offset: 0; }
:global(html.pet-preview-open) { overflow: hidden; }
@media (max-width: 600px) {
  .pet-preview { inset: auto 0 0; width: 100%; max-height: 94dvh; border-radius: 16px 16px 0 0; }
  .pet-preview-shell { max-height: 94dvh; }
  .pet-preview-header, .pet-preview-footer { padding: 10px 12px; }
  .pet-preview-content { padding: 10px 12px 0; }
  .pet-preview-footer { padding-bottom: max(10px, env(safe-area-inset-bottom)); }
}
</style>
