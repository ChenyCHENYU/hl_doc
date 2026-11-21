<script setup lang="ts">
import { computed, nextTick, ref } from "vue";
import { assetUrl } from "../assets";
import catalog from "../../data/resource-catalog.json";
import gallery from "../../data/gallery.json";

interface CatalogEntry {
  name: string;
  type: string;
  status: string;
  note: string;
}

interface GalleryItem {
  file: string;
  title: string;
}

const entries = catalog as CatalogEntry[];
const items = gallery as GalleryItem[];

const STATUS_TABS = ["全部", "已上线", "仅编目", "史料收录", "不收录"];
const activeStatus = ref("全部");
const keyword = ref("");
const lightbox = ref<GalleryItem | null>(null);
const galleryDialog = ref<HTMLDialogElement | null>(null);
const galleryError = ref(false);
let galleryTrigger: HTMLElement | null = null;

async function openImage(item: GalleryItem, event: MouseEvent) {
  galleryTrigger = event.currentTarget as HTMLElement;
  galleryError.value = false;
  lightbox.value = item;
  await nextTick();
  galleryDialog.value?.showModal();
}
function afterClose() {
  lightbox.value = null;
  galleryTrigger?.focus({ preventScroll: true });
  galleryTrigger = null;
}

const filtered = computed(() => {
  const k = keyword.value.trim();
  return entries.filter((e) => {
    if (activeStatus.value !== "全部" && e.status !== activeStatus.value) return false;
    if (!k) return true;
    return e.name.includes(k) || e.note.includes(k) || e.type.includes(k);
  });
});

const onlineCount = entries.filter((e) => e.status === "已上线").length;
const catalogOnlyCount = entries.filter((e) => e.status === "仅编目").length;
const excludedCount = entries.filter((e) => e.status === "不收录").length;

function src(item: GalleryItem): string {
  return assetUrl(item.file);
}

function onImgError(e: Event) {
  const el = e.target as HTMLElement;
  const wrap = el.closest(".gal-item");
  if (wrap) wrap.classList.add("img-failed");
  el.remove();
}
</script>

<template>
  <div class="pc-wrap field-ui">
    <div class="hero-stats res-stats">
      <div class="stat-item"><span class="stat-num">{{ entries.length }}</span><span class="stat-lbl">编目条目</span></div>
      <div class="stat-item"><span class="stat-num">{{ onlineCount }}</span><span class="stat-lbl">已上线</span></div>
      <div class="stat-item"><span class="stat-num">{{ catalogOnlyCount }}</span><span class="stat-lbl">仅编目</span></div>
      <div class="stat-item"><span class="stat-num">{{ excludedCount }}</span><span class="stat-lbl">不收录</span></div>
      <div class="stat-item"><span class="stat-num">{{ items.length }}</span><span class="stat-lbl">画廊图片</span></div>
    </div>
    <nav class="res-jump" aria-label="资源库入口">
      <a href="#resource-index">查看资料编目</a>
      <a href="#resource-gallery">查看壁纸画廊</a>
      <a href="/guide/catalog">全部栏目</a>
    </nav>

    <h2 id="resource-index" class="gal-title">资料编目</h2>
    <div class="pc-toolbar">
      <div class="pc-tabs">
        <button
          v-for="s in STATUS_TABS"
          :key="s"
          class="pc-tab"
          :class="{ active: activeStatus === s }"
          :aria-pressed="activeStatus === s"
          @click="activeStatus = s"
        >
          {{ s }}
        </button>
      </div>
      <input v-model="keyword" class="item-search pc-search" type="search" placeholder="搜索资源名 / 说明" aria-label="搜索资源名称或说明" />
    </div>

    <div v-if="filtered.length" class="lookup-scroll" role="region" aria-label="资源编目" tabindex="0">
    <table>
      <thead>
        <tr>
          <th>资源</th>
          <th>类别</th>
          <th>状态</th>
          <th>说明</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="e in filtered" :key="e.name">
          <td class="pp-name">{{ e.name }}</td>
          <td class="pp-sys">{{ e.type }}</td>
          <td>
            <span class="res-tag" :class="'st-' + e.status">{{ e.status }}</span>
          </td>
          <td>{{ e.note }}</td>
        </tr>
      </tbody>
    </table>
    </div>
    <p v-else role="status">这个分类没有匹配的资源。</p>

    <h2 id="resource-gallery" class="gal-title">幻灵画廊 · 高清壁纸</h2>
    <p class="item-count">来自《▲幻灵游侠优化资源▲》壁纸包，点击看大图；正式环境经 OSS 分发。</p>
    <div class="gal-grid">
      <figure v-for="g in items" :key="g.file" class="gal-item">
        <button class="gal-frame" type="button" :aria-label="`查看大图：${g.title}`" aria-haspopup="dialog" @click="openImage(g, $event)">
          <img :src="src(g)" alt="" loading="lazy" @error="onImgError" />
        </button>
        <figcaption>{{ g.title }}</figcaption>
      </figure>
    </div>

    <dialog ref="galleryDialog" class="gallery-dialog" aria-labelledby="gallery-title" @close="afterClose" @click.self="galleryDialog?.close()">
      <div v-if="lightbox" class="gallery-dialog-inner">
        <header><h2 id="gallery-title">{{ lightbox.title }}</h2><button autofocus type="button" @click="galleryDialog?.close()">关闭</button></header>
        <img v-if="!galleryError" :src="src(lightbox)" :alt="lightbox.title" @error="galleryError = true" />
        <p v-else>这张图暂时无法加载。</p>
      </div>
    </dialog>
  </div>
</template>

<style scoped>
.res-stats {
  margin: 0 0 22px;
  display: flex;
  flex-wrap: wrap;
}
.res-jump { display: flex; flex-wrap: wrap; gap: 8px 15px; }

.res-tag {
  font-size: 12px;
  border-radius: 999px;
  padding: 1px 10px;
  border: 1px solid;
  white-space: nowrap;
}

.res-tag.st-已上线 {
  color: #2e7d32;
  border-color: rgba(46, 125, 50, 0.4);
  background: rgba(46, 125, 50, 0.1);
}

.dark .res-tag.st-已上线 {
  color: #7bd47f;
}

.res-tag.st-仅编目 {
  color: #9a7410;
  border-color: rgba(184, 134, 11, 0.4);
  background: rgba(184, 134, 11, 0.08);
}

.res-tag.st-不收录 {
  color: var(--vp-c-text-3);
  border-color: var(--vp-c-divider);
}

.gal-title {
  margin: 34px 0 4px;
  font-size: 22px;
  font-weight: 700;
}

.gal-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 14px;
  margin: 16px 0 28px;
}

.gal-item {
  margin: 0;
  cursor: zoom-in;
}

.gal-frame {
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
  aspect-ratio: 16 / 10;
  width: 100%;
  cursor: zoom-in;
  background: var(--vp-c-bg-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-color 0.15s, transform 0.15s, box-shadow 0.15s;
}

.gal-item:hover .gal-frame {
  border-color: rgba(184, 134, 11, 0.45);
  transform: translateY(-3px);
  box-shadow: 0 10px 26px rgba(184, 134, 11, 0.14);
}

.gal-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.gal-item.img-failed .gal-frame::after {
  content: "图片待 OSS 上线";
  font-size: 12px;
  color: var(--vp-c-text-3);
}

figcaption {
  margin-top: 8px;
  text-align: center;
  font-size: 12.5px;
  color: var(--vp-c-text-2);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.gallery-dialog { position: fixed; inset: 0; margin: auto; width: min(940px, 100% - 24px); max-height: 90dvh; overflow: auto; color: var(--field-ink); background: var(--field-paper); border-radius: 14px; border: 1px solid var(--field-line); padding: 0; }
.gallery-dialog::backdrop { background: rgb(10 16 13 / 75%); }
.gallery-dialog-inner { padding: 12px; }
.gallery-dialog header { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 8px; }
.gallery-dialog header h2 { font-size: 17px; border: 0; margin: 0; padding: 0; }
.gallery-dialog header button { min-height: 36px; padding: 0 10px; border-radius: 6px; background: var(--field-tint); }
.gallery-dialog img { display: block; margin: auto; max-height: 75dvh; width: auto; object-fit: contain; }
:global(html:has(.gallery-dialog[open])) { overflow: hidden; }
</style>
