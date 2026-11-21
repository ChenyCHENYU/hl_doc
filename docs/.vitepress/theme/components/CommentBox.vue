<script setup lang="ts">
// 文章底部评论区
// - 正式模式：Twikoo（Vercel Serverless），游客可评论，邮箱填 QQ 号即显示 QQ 头像
// - 回退模式：未配置 TWIKOO_ENV_ID 时使用本地试用（localStorage），便于本地预览
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vitepress";
import { TWIKOO_ENV_ID } from "../comments";

const route = useRoute();
const key = computed(() => `hl-comments:${route.path}`);

interface Comment {
  id: number;
  name: string;
  qq: string;
  content: string;
  time: number;
}

const list = ref<Comment[]>([]);
const name = ref("");
const qq = ref("");
const content = ref("");
const okFlash = ref(false);
const formErr = ref("");
const twikooEl = ref<HTMLElement | null>(null);
const twikooReady = ref(false);
const twikooErr = ref("");

const isLive = !!TWIKOO_ENV_ID;

function loadScript(src: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = src;
    s.onload = () => resolve();
    s.onerror = () => reject(new Error("twikoo 加载失败"));
    document.head.appendChild(s);
  });
}

async function mountTwikoo() {
  if (!twikooEl.value) return;
  try {
    await loadScript("https://cdn.jsdelivr.net/npm/twikoo@1.6.44/dist/twikoo.all.min.js");
    const tk = (window as any).twikoo;
    await tk.init({
      envId: TWIKOO_ENV_ID,
      el: twikoo.value,
      path: route.path,
      lang: "zh-CN",
    });
    twikooReady.value = true;
  } catch (e) {
    twikooErr.value = e instanceof Error ? e.message : String(e);
  }
}

onMounted(() => {
  if (isLive) {
    mountTwikoo();
    return;
  }
  try {
    const saved = localStorage.getItem(key.value);
    if (saved) list.value = JSON.parse(saved);
    const who = localStorage.getItem("hl-commenter");
    if (who) {
      const w = JSON.parse(who);
      name.value = w.name || "";
      qq.value = w.qq || "";
    }
  } catch {
    /* 忽略本地存储异常 */
  }
});

// 路由切换时重挂 Twikoo（path 变化）
watch(
  () => route.path,
  () => {
    if (isLive && twikooReady.value) {
      twikooReady.value = false;
      requestAnimationFrame(() => mountTwikoo());
    }
  }
);

function avatar(c: Comment): string {
  if (c.qq && /^\d{5,11}$/.test(c.qq)) {
    return `https://q1.qlogo.cn/g?b=qq&nk=${c.qq}&s=100`;
  }
  return "";
}

function avatarBg(c: Comment): string {
  const colors = ["#b8860b", "#2e9e6f", "#4d8fd1", "#d15a5a", "#8a6fd0"];
  let h = 0;
  for (const ch of c.name) h = (h * 31 + ch.charCodeAt(0)) % 997;
  return colors[h % colors.length];
}

function fmt(t: number): string {
  const d = new Date(t);
  const p = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`;
}

function save() {
  try {
    localStorage.setItem(key.value, JSON.stringify(list.value));
    formErr.value = "";
  } catch (e) {
    formErr.value = "保存失败：" + (e instanceof Error ? e.message : String(e));
  }
}

function submit() {
  const c = content.value.trim();
  const n = name.value.trim();
  if (!n || !c || c.length < 2) return;
  try {
    list.value.unshift({ id: Date.now(), name: n, qq: qq.value.trim(), content: c, time: Date.now() });
    localStorage.setItem("hl-commenter", JSON.stringify({ name: n, qq: qq.value.trim() }));
    save();
    content.value = "";
    okFlash.value = true;
    setTimeout(() => (okFlash.value = false), 1600);
  } catch (e) {
    formErr.value = "发布失败：" + (e instanceof Error ? e.message : String(e)) + "｜key=" + key.value;
  }
}

const canSubmit = computed(() => name.value.trim().length > 0 && content.value.trim().length >= 2);
</script>

<template>
  <section class="cb">
    <header class="cb-head">
      <h3 class="cb-title">评论<span v-if="!isLive && list.length" class="cb-count">{{ list.length }}</span></h3>
      <span v-if="!isLive" class="cb-mode" title="评论已可正常发布（本机保存）。部署 Vercel 并配置 TWIKOO_ENV_ID 后自动切换云端共享评论，三步见 DEPLOY.md">预览模式 · 部署后自动上云</span>
    </header>

    <!-- 正式模式：Twikoo 挂载点 -->
    <div v-if="isLive" ref="twikooEl" class="cb-twikoo"></div>
    <p v-if="isLive && twikooErr" class="cb-empty">评论服务暂时不可用：{{ twikooErr }}</p>

    <!-- 回退模式：本地 UI -->
    <template v-if="!isLive">
      <div class="cb-form" :data-err="formErr || null">
        <div class="cb-who">
          <input v-model="name" class="cb-input cb-name" type="text" maxlength="16" placeholder="昵称（必填）" />
          <input v-model="qq" class="cb-input cb-qq" type="text" maxlength="11" inputmode="numeric" placeholder="QQ 号（选填，自动带头像）" />
          <span class="cb-qq-login" title="正式模式由 Twikoo 提供：邮箱填 QQ 号即显示 QQ 头像；域名备案后可追加 QQ 互联回调">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M12 2C8 2 4.9 4.4 4.9 7.4c0 1.6.9 3 2.4 4-.2.8-.7 1.9-1.4 2.6 0 0 1.9-.2 3.3-1.1.9.3 1.8.4 2.8.4 4 0 7.1-2.4 7.1-5.4S16 2 12 2z" transform="translate(0 1.5)"/>
            </svg>
            QQ 用户直接评论
          </span>
        </div>
        <textarea
          v-model="content"
          class="cb-input cb-text"
          rows="3"
          maxlength="500"
          placeholder="说点什么吧……（游客可直接评论）"
        ></textarea>
        <div class="cb-actions">
          <span v-if="okFlash" class="cb-ok">✓ 已发布</span>
          <button class="cb-submit" :disabled="!canSubmit" @click="submit">发布评论</button>
        </div>
      </div>

      <ul v-if="list.length" class="cb-list">
        <li v-for="c in list" :key="c.id" class="cb-item">
          <img v-if="avatar(c)" class="cb-avatar" :src="avatar(c)" :alt="c.name" loading="lazy" />
          <span v-else class="cb-avatar cb-avatar-fallback" :style="{ background: avatarBg(c) }">{{ c.name.slice(0, 1) }}</span>
          <div class="cb-main">
            <div class="cb-meta">
              <b class="cb-name">{{ c.name }}</b>
              <span v-if="c.qq" class="cb-qqtag">QQ {{ c.qq }}</span>
              <time class="cb-time">{{ fmt(c.time) }}</time>
            </div>
            <p class="cb-content">{{ c.content }}</p>
          </div>
        </li>
      </ul>
      <p v-else class="cb-empty">还没有评论，来抢沙发吧。</p>
    </template>
  </section>
</template>

<style scoped>
.cb {
  margin: 34px 0 10px;
  padding-top: 22px;
  border-top: 1px solid var(--vp-c-divider);
}

.cb-head {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

.cb-title {
  margin: 0;
  font-size: 17px;
  font-weight: 800;
  color: var(--vp-c-text-1);
  display: flex;
  align-items: center;
  gap: 8px;
}

.cb-count {
  min-width: 22px;
  height: 22px;
  padding: 0 7px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-size: 12px;
  font-weight: 800;
}

.cb-mode {
  margin-left: auto;
  font-size: 11.5px;
  color: var(--vp-c-text-3);
  border: 1px dashed var(--vp-c-divider);
  border-radius: 999px;
  padding: 2px 10px;
  cursor: help;
}

.cb-twikoo {
  min-height: 120px;
}

.cb-form {
  border: 1px solid var(--vp-c-divider);
  border-radius: 14px;
  background: var(--vp-c-bg-soft);
  padding: 14px 16px;
}

.cb-who {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
}

.cb-input {
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 13.5px;
  padding: 8px 12px;
  outline: none;
  transition: border-color 0.15s;
}

.cb-input:focus {
  border-color: var(--vp-c-brand-1);
}

.cb-name {
  width: 150px;
}

.cb-qq {
  flex: 1;
  min-width: 200px;
}

.cb-qq-login {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 36px;
  padding: 0 14px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg);
  color: var(--vp-c-brand-1);
  font-size: 13px;
  font-weight: 600;
}

.cb-text {
  width: 100%;
  box-sizing: border-box;
  resize: vertical;
  min-height: 74px;
  line-height: 1.7;
  font-family: inherit;
}

.cb-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
  margin-top: 10px;
}

.cb-ok {
  font-size: 12.5px;
  color: #2e9e6f;
  font-weight: 700;
}

.cb-submit {
  min-height: 36px;
  padding: 7px 20px;
  border: none;
  border-radius: 10px;
  background: var(--vp-c-brand-1);
  color: var(--vp-c-bg);
  font-size: 13.5px;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.15s, transform 0.15s;
}

.cb-submit:hover:not(:disabled) {
  transform: translateY(-1px);
}

.cb-submit:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.cb-list {
  list-style: none;
  margin: 18px 0 0;
  padding: 0;
}

.cb-item {
  animation: hl-slide-in 0.35s ease both;
  display: flex;
  gap: 12px;
  padding: 13px 2px;
  border-bottom: 1px dashed var(--vp-c-divider);
}

.cb-item:last-child {
  border-bottom: none;
}

.cb-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  background: #fff;
}

.cb-avatar-fallback {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 16px;
  font-weight: 800;
}

.cb-main {
  flex: 1;
  min-width: 0;
}

.cb-meta {
  display: flex;
  align-items: baseline;
  gap: 8px;
  flex-wrap: wrap;
}

.cb-name {
  font-size: 13.5px;
  color: var(--vp-c-text-1);
}

.cb-qqtag {
  font-size: 11.5px;
  color: var(--vp-c-brand-1);
  border: 1px solid var(--vp-c-brand-soft);
  border-radius: 999px;
  padding: 0 8px;
}

.cb-time {
  font-size: 11.5px;
  color: var(--vp-c-text-3);
  font-variant-numeric: tabular-nums;
}

.cb-content {
  margin: 5px 0 0;
  font-size: 13.5px;
  line-height: 1.8;
  color: var(--vp-c-text-2);
  overflow-wrap: anywhere;
}

.cb-empty {
  margin: 18px 0 0;
  font-size: 13px;
  color: var(--vp-c-text-3);
  text-align: center;
  padding: 14px;
  border: 1px dashed var(--vp-c-divider);
  border-radius: 12px;
}

@media (max-width: 560px) {
  .cb-name {
    width: 120px;
  }

  .cb-qq {
    min-width: 140px;
  }
}
</style>

<style>
/* Twikoo 主题适配：对齐站点金色系 */
.cb-twikoo .tk-submit {
  background: var(--vp-c-brand-1) !important;
  border: none !important;
  color: var(--vp-c-bg) !important;
  border-radius: 10px !important;
  font-weight: 700 !important;
}

.cb-twikoo .tk-action-icon,
.cb-twikoo .tk-nick {
  color: var(--vp-c-brand-1);
}

.cb-twikoo .tk-comments-container {
  margin-top: 6px;
}
</style>
