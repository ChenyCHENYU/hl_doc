<script setup lang="ts">
import { stages, extraRules } from "../../data/ascension";
</script>

<template>
  <div class="ag">
    <div class="ag-stages">
      <div class="ag-line" aria-hidden="true"></div>

      <section v-for="(s, i) in stages" :key="s.key" class="ag-stage" :class="{ fork: s.good && s.evil }">
      <div class="ag-badge" :class="{ fork: s.good && s.evil }">{{ s.turn }}</div>
      <div class="ag-card">
        <h3 class="ag-name">
          {{ s.name }}
          <span v-if="s.good && s.evil" class="ag-fork-tag">仙魔分线</span>
        </h3>
        <p class="ag-desc">{{ s.desc }}</p>

        <div v-if="s.good && s.evil" class="ag-fork">
          <div class="ag-path ag-good">
            <div class="ag-path-title">{{ s.good.title }}</div>
            <dl>
              <div><dt>地点</dt><dd>{{ s.good.place }}</dd></div>
              <div><dt>道具</dt><dd>{{ s.good.item }}</dd></div>
              <div><dt>条件</dt><dd>{{ s.good.req }}</dd></div>
            </dl>
          </div>
          <div class="ag-path ag-evil">
            <div class="ag-path-title">{{ s.evil.title }}</div>
            <dl>
              <div><dt>地点</dt><dd>{{ s.evil.place }}</dd></div>
              <div><dt>道具</dt><dd>{{ s.evil.item }}</dd></div>
              <div><dt>条件</dt><dd>{{ s.evil.req }}</dd></div>
            </dl>
          </div>
        </div>

        <div v-else-if="s.good" class="ag-single ag-good">
          <dl>
            <div><dt>方式</dt><dd>{{ s.good.place }}</dd></div>
            <div><dt>条件</dt><dd>{{ s.good.req }}</dd></div>
          </dl>
        </div>

        <div class="ag-reward">获得：{{ s.reward }}</div>
        <ul class="ag-notes">
          <li v-for="n in s.notes" :key="n">{{ n }}</li>
        </ul>
      </div>
      <div v-if="i < stages.length - 1" class="ag-next">&#9660;</div>
      </section>
    </div>

    <h2 class="ag-extra-h">飞升周边规则</h2>
    <div class="ag-extra">
      <div v-for="r in extraRules" :key="r.k" class="ag-extra-card">
        <b>{{ r.k }}</b>
        <p>{{ r.v }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ag {
  position: relative;
  margin: 20px 0 32px;
}

/* 阶段区容器：竖轴只画到转生阶段为止，不再穿进底部“周边规则”卡片 */
.ag-stages {
  position: relative;
}

.ag-line {
  position: absolute;
  left: 38px;
  top: 30px;
  bottom: 44px;
  width: 2px;
  background: linear-gradient(180deg, var(--vp-c-brand-1), rgba(184, 134, 11, 0.15));
}

.ag-stage {
  position: relative;
  padding-left: 92px;
  margin-bottom: 8px;
}

.ag-badge {
  position: absolute;
  left: 0;
  top: 14px;
  width: 76px;
  height: 76px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  background: rgba(184, 134, 11, 0.08);
  border: 2px solid rgba(184, 134, 11, 0.4);
  z-index: 1;
}

.dark .ag-badge {
  background: rgba(240, 201, 78, 0.1);
  border-color: rgba(240, 201, 78, 0.45);
}

.ag-next {
  text-align: left;
  margin-left: 30px;
  color: var(--vp-c-brand-1);
  font-size: 13px;
  opacity: 0.7;
}

.ag-card {
  border: 1px solid var(--vp-c-divider);
  border-radius: 14px;
  background: var(--vp-c-bg-soft);
  padding: 18px 22px 16px;
  margin-bottom: 14px;
}

.ag-name {
  margin: 0 0 8px;
  font-size: 17px;
  font-weight: 700;
  color: var(--vp-c-text-1);
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.ag-fork-tag {
  font-size: 12px;
  color: var(--vp-c-brand-1);
  border: 1px solid var(--vp-c-brand-soft);
  border-radius: 999px;
  padding: 1px 10px;
}

.ag-desc {
  margin: 0 0 14px;
  font-size: 14px;
  line-height: 1.8;
  color: var(--vp-c-text-2);
}

.ag-fork {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 12px;
}

.ag-path {
  border-radius: 10px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  padding: 12px 14px;
}

.ag-path.ag-good {
  border-color: rgba(184, 134, 11, 0.45);
}

.ag-path.ag-evil {
  border-color: rgba(46, 158, 111, 0.45);
}

.ag-path-title {
  font-size: 15px;
  font-weight: 700;
  margin-bottom: 8px;
}

.ag-good .ag-path-title {
  color: #b8860b;
}

.dark .ag-good .ag-path-title {
  color: #f0c94e;
}

.ag-evil .ag-path-title {
  color: #2e9e6f;
}

.dark .ag-evil .ag-path-title {
  color: #6fd0a5;
}

.ag-path dl,
.ag-single dl {
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.ag-path dl > div,
.ag-single dl > div {
  display: flex;
  gap: 8px;
  font-size: 12.5px;
  line-height: 1.65;
}

.ag-path dt,
.ag-single dt {
  flex-shrink: 0;
  font-weight: 700;
  color: var(--vp-c-text-3);
  width: 3em;
}

.ag-path dd,
.ag-single dd {
  margin: 0;
  color: var(--vp-c-text-2);
}

.ag-single {
  margin-bottom: 12px;
}

.ag-reward {
  font-size: 12.5px;
  font-weight: 700;
  color: var(--vp-c-brand-1);
  margin-bottom: 8px;
}

.ag-notes {
  margin: 0;
  padding: 10px 0 0;
  border-top: 1px dashed var(--vp-c-divider);
  list-style: none;
}

.ag-notes li {
  font-size: 12.5px;
  color: var(--vp-c-text-3);
  line-height: 1.75;
  padding-left: 16px;
  position: relative;
}

.ag-notes li::before {
  content: "·";
  position: absolute;
  left: 4px;
  color: var(--vp-c-brand-1);
  font-weight: 800;
}

.ag-extra-h {
  margin: 30px 0 14px;
  font-size: 20px;
  font-weight: 700;
}

.ag-extra {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 10px;
}

.ag-extra-card {
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
  padding: 12px 16px;
}

.ag-extra-card b {
  font-size: 13.5px;
  color: var(--vp-c-brand-1);
}

.ag-extra-card p {
  margin: 6px 0 0;
  font-size: 12.5px;
  line-height: 1.7;
  color: var(--vp-c-text-2);
}

@media (max-width: 760px) {
  .ag-line {
    display: none;
  }

  .ag-stage {
    padding-left: 0;
  }

  .ag-badge {
    position: static;
    margin-bottom: 10px;
  }

  .ag-fork {
    grid-template-columns: 1fr;
  }
}
</style>
