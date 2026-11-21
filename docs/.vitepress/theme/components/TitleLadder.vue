<script setup lang="ts">
import { mortalTitles, ascensions, godJobs, demonJobs } from "../../data/titles";
</script>

<template>
  <div class="tv">
    <!-- 凡人阶梯 -->
    <section class="tv-block">
      <h2 class="tv-h">
        <span class="tv-kicker">STAGE 1</span>凡人称号 · 八阶
      </h2>
      <div class="tv-stairs">
        <div
          v-for="(m, i) in mortalTitles"
          :key="m.title"
          class="tv-stair"
          :class="{ top: i === mortalTitles.length - 1 }"
        >
          <span class="tv-stair-title">{{ m.title }}</span>
          <span class="tv-stair-range">{{ m.range }}</span>
          <i class="tv-stair-bar" :style="{ height: 18 + i * 8 + 'px' }"></i>
        </div>
      </div>
    </section>

    <!-- 正邪转世双线 -->
    <section class="tv-block">
      <h2 class="tv-h">
        <span class="tv-kicker">STAGE 2</span>五转飞升 · 正邪双线
      </h2>
      <div class="tv-path">
        <div class="tv-col tv-good">
          <div class="tv-col-head gold">正道 · 入仙</div>
          <div v-for="(a, i) in ascensions" :key="'g' + i" class="tv-node gold">
            <b>{{ a.good.title }}</b>
            <p>{{ a.good.req }}</p>
          </div>
        </div>

        <div class="tv-mid">
          <div v-for="(a, i) in ascensions" :key="'m' + i" class="tv-turn">
            <span class="tv-turn-dot"></span>
            <span class="tv-turn-label">{{ a.turn }}</span>
          </div>
          <div class="tv-merge">殊归同途</div>
        </div>

        <div class="tv-col tv-evil">
          <div class="tv-col-head jade">邪道 · 入魔</div>
          <div v-for="(a, i) in ascensions" :key="'e' + i" class="tv-node jade">
            <b>{{ a.evil.title }}</b>
            <p>{{ a.evil.req }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 五转职业分支 -->
    <section class="tv-block">
      <h2 class="tv-h">
        <span class="tv-kicker">STAGE 3</span>五转分支 · 十种神尊
      </h2>
      <div class="tv-jobs">
        <div class="tv-jobs-col">
          <div class="tv-jobs-title gold">天神 · 五职</div>
          <div class="tv-job gold" v-for="j in godJobs" :key="j.name">
            <b>{{ j.name }}</b><span>{{ j.domain }}</span>
          </div>
        </div>
        <div class="tv-jobs-col">
          <div class="tv-jobs-title jade">魔尊 · 五职</div>
          <div class="tv-job jade" v-for="j in demonJobs" :key="j.name">
            <b>{{ j.name }}</b><span>{{ j.domain }}</span>
          </div>
        </div>
      </div>
      <p class="tv-jobs-note">完成一种五行属性任务后，按七种职业要求分别飞升；锻造/创招/修行/养宠/功德为仙线五职，偷窃/声望/修行/养宠/功德为魔线五职。</p>
    </section>

    <div class="tv-foot">
      <span>入仙入魔不满意？<b>仙魔互转任务</b>可降一层次换阵营</span>
      <a href="/quests/ascension">完整飞升流程（0 → 五转）&#8250;</a>
      <a href="/quests/ascend">历史版简易攻略 &#8250;</a>
    </div>
  </div>
</template>

<style scoped>
.tv {
  margin: 22px 0 34px;
}

.tv-block {
  margin-bottom: 38px;
}

.tv-h {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: 800;
  color: var(--vp-c-text-1);
  margin: 0 0 16px;
}

.tv-kicker {
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.18em;
  color: var(--vp-c-brand-1);
  border: 1px solid var(--vp-c-brand-soft);
  background: var(--vp-c-brand-soft);
  border-radius: 6px;
  padding: 2px 8px;
}

/* ---- 凡人阶梯（横向柱状梯） ---- */
.tv-stairs {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  padding: 0 4px;
}

.tv-stair {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  min-width: 0;
}

.tv-stair-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--vp-c-text-1);
  white-space: nowrap;
}

.tv-stair-range {
  font-size: 12px;
  color: var(--vp-c-text-3);
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.tv-stair-bar {
  width: 100%;
  max-width: 92px;
  border-radius: 6px 6px 0 0;
  background: linear-gradient(180deg, rgba(184, 134, 11, 0.55), rgba(184, 134, 11, 0.16));
  border: 1px solid rgba(184, 134, 11, 0.3);
  border-bottom: none;
  transition: filter 0.15s;
  transform-origin: bottom;
  animation: hl-grow-y 0.6s cubic-bezier(0.34, 1.3, 0.5, 1) both;
}

.tv-stair:nth-child(1) .tv-stair-bar { animation-delay: 0.05s; }
.tv-stair:nth-child(2) .tv-stair-bar { animation-delay: 0.12s; }
.tv-stair:nth-child(3) .tv-stair-bar { animation-delay: 0.19s; }
.tv-stair:nth-child(4) .tv-stair-bar { animation-delay: 0.26s; }
.tv-stair:nth-child(5) .tv-stair-bar { animation-delay: 0.33s; }
.tv-stair:nth-child(6) .tv-stair-bar { animation-delay: 0.40s; }
.tv-stair:nth-child(7) .tv-stair-bar { animation-delay: 0.47s; }
.tv-stair:nth-child(8) .tv-stair-bar { animation-delay: 0.54s; }

@media (prefers-reduced-motion: reduce) {
  .tv-stair-bar { animation: none; }
}

.tv-stair:hover .tv-stair-bar {
  filter: brightness(1.25);
}

.tv-stair.top .tv-stair-bar {
  background: linear-gradient(180deg, #d4af37, rgba(184, 134, 11, 0.5));
  box-shadow: 0 0 18px rgba(212, 175, 55, 0.35);
}

.tv-stair.top .tv-stair-title {
  color: var(--vp-c-brand-1);
}

/* ---- 正邪双线 ---- */
.tv-path {
  display: grid;
  grid-template-columns: 1fr 96px 1fr;
  gap: 14px;
}

.tv-col-head {
  text-align: center;
  font-size: 13.5px;
  font-weight: 800;
  padding: 8px 0;
  border-radius: 10px;
  margin-bottom: 10px;
}

.tv-col-head.gold {
  color: #b8860b;
  background: rgba(184, 134, 11, 0.1);
  border: 1px solid rgba(184, 134, 11, 0.35);
}

.dark .tv-col-head.gold {
  color: #f0c94e;
}

.tv-col-head.jade {
  color: #2e9e6f;
  background: rgba(46, 158, 111, 0.1);
  border: 1px solid rgba(46, 158, 111, 0.35);
}

.dark .tv-col-head.jade {
  color: #6fd0a5;
}

.tv-node {
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
  padding: 9px 12px;
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  transition: transform 0.15s, border-color 0.15s;
}

.tv-node:hover {
  transform: translateX(2px);
}

.tv-node.gold {
  border-left: 3px solid #b8860b;
}

.tv-node.jade {
  border-left: 3px solid #2e9e6f;
}

.tv-node b {
  font-size: 14.5px;
  color: var(--vp-c-text-1);
}

.tv-node p {
  margin: 0;
  font-size: 12px;
  line-height: 1.6;
  color: var(--vp-c-text-3);
}

.tv-mid {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 34px 0 8px;
  position: relative;
}

.tv-mid::before {
  content: "";
  position: absolute;
  top: 44px;
  bottom: 26px;
  width: 2px;
  background: linear-gradient(180deg, var(--vp-c-divider), var(--vp-c-brand-1), var(--vp-c-divider));
}

.tv-turn {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  margin: 6px 0;
}

.tv-turn-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--vp-c-brand-1);
  box-shadow: 0 0 0 4px var(--vp-c-brand-soft);
}

.tv-turn-label {
  font-size: 12px;
  font-weight: 800;
  color: var(--vp-c-text-3);
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  padding: 1px 9px;
}

.tv-merge {
  position: relative;
  z-index: 1;
  font-size: 12px;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-brand-soft);
  border-radius: 999px;
  padding: 2px 10px;
  margin-top: 8px;
}

/* ---- 五转职业 ---- */
.tv-jobs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.tv-jobs-title {
  text-align: center;
  font-size: 13px;
  font-weight: 800;
  margin-bottom: 10px;
}

.tv-jobs-title.gold { color: #b8860b; }
.dark .tv-jobs-title.gold { color: #f0c94e; }
.tv-jobs-title.jade { color: #2e9e6f; }
.dark .tv-jobs-title.jade { color: #6fd0a5; }

.tv-jobs-col {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 8px;
}

.tv-job {
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
  padding: 9px 12px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 5px;
  transition: transform 0.15s, border-color 0.15s, box-shadow 0.15s;
}

.tv-job:hover {
  transform: translateY(-2px);
}

.tv-job.gold:hover {
  border-color: rgba(184, 134, 11, 0.5);
  box-shadow: 0 8px 20px -8px rgba(184, 134, 11, 0.35);
}

.tv-job.jade:hover {
  border-color: rgba(46, 158, 111, 0.5);
  box-shadow: 0 8px 20px -8px rgba(46, 158, 111, 0.35);
}

.tv-job b {
  font-size: 13.5px;
  line-height: 1.3;
  white-space: nowrap;
  color: var(--vp-c-text-1);
}

.tv-job span {
  font-size: 12px;
  color: var(--vp-c-text-3);
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  padding: 0 8px;
}

.tv-jobs-note {
  margin: 12px 0 0;
  font-size: 12px;
  line-height: 1.7;
  color: var(--vp-c-text-3);
}

.tv-foot {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 16px;
  border-top: 1px dashed var(--vp-c-divider);
  padding-top: 14px;
  font-size: 12.5px;
  color: var(--vp-c-text-3);
}

.tv-foot b {
  color: var(--vp-c-text-2);
}

.tv-foot a {
  color: var(--vp-c-brand-1);
  font-weight: 700;
  text-decoration: none;
}

@media (max-width: 760px) {
  .tv-stairs {
    flex-wrap: wrap;
    align-items: flex-start;
  }

  .tv-stair {
    flex: 1 1 22%;
  }

  .tv-path {
    grid-template-columns: 1fr;
  }

  .tv-mid {
    flex-direction: row;
    padding: 6px 0;
    gap: 8px;
  }

  .tv-mid::before {
    display: none;
  }

  .tv-jobs {
    grid-template-columns: 1fr;
  }
}
</style>
