<script setup lang="ts">
import { computed, ref } from "vue";
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

const STATUS_TABS = ["全部", "已上线", "仅编目", "不收录"];
const activeStatus = ref("全部");
const keyword = ref("");
const lightbox = ref<GalleryItem | null>(null);

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
  <div class="pc-wrap">
    <div class="hero-stats res-stats">
      <div class="stat-item"><span class="stat-num">{{ entries.length }}</span><span class="stat-lbl">编目条目</span></div>
      <div class="stat-item"><span class="stat-num">{{ onlineCount }}</span><span class="stat-lbl">已上线</span></div>
      <div class="stat-item"><span class="stat-num">{{ catalogOnlyCount }}</span><span class="stat-lbl">仅编目</span></div>
      <div class="stat-item"><span class="stat-num">{{ excludedCount }}</span><span class="stat-lbl">不收录</span></div>
      <div class="stat-item"><span class="stat-num">{{ items.length }}</span><span class="stat-lbl">画廊图片</span></div>
    </div>

    <div class="pc-toolbar">
      <div class="pc-tabs">
        <button
          v-for="s in STATUS_TABS"
          :key="s"
          class="pc-tab"
          :class="{ active: activeStatus === s }"
          @click="activeStatus = s"
        >
          {{ s }}
        </button>
      </div>
      <input v-model="keyword" class="item-search pc-search" type="search" placeholder="搜索资源名 / 说明" />
    </div>

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

    <h2 class="gal-title">幻灵画廊 · 高清壁纸</h2>
    <p class="item-count">来自《▲幻灵游侠优化资源▲》壁纸包，点击看大图；正式环境经 OSS 分发。</p>
    <div class="gal-grid">
      <figure v-for="g in items" :key="g.file" class="gal-item" @click="lightbox = g">
        <div class="gal-frame">
          <img :src="src(g)" :alt="g.title" loading="lazy" @error="onImgError" />
        </div>
        <figcaption>{{ g.title }}</figcaption>
      </figure>
    </div>

    <Teleport to="body">
      <Transition name="pc-modal">
        <div v-if="lightbox" class="pc-overlay" @click.self="lightbox = null">
          <div class="pc-modal gal-modal" style="--el: var(--vp-c-brand-1)">
            <button class="pc-close" @click="lightbox = null">&#215;</button>
            <div class="gal-lightbox">
              <img :src="src(lightbox)" :alt="lightbox.title" />
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.res-stats {
  margin: 0 0 22px;
  display: inline-flex;
}

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

.gal-modal {
  display: block;
  max-width: 900px;
}

.gal-lightbox {
  padding: 14px;
}

.gal-lightbox img {
  width: 100%;
  height: auto;
  border-radius: 10px;
  display: block;
}
</style>
