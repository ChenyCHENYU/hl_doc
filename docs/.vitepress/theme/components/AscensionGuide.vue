<script setup lang="ts">
import { stages, extraRules } from "../../data/ascension";
</script>

<template>
  <div class="field-ui asc-guide">
    <nav class="asc-guide-nav" aria-label="跳到对应飞升阶段">
      <a v-for="s in stages" :key="s.key" :href="`#asc-stage-${s.key}`">{{ s.turn }}</a>
      <a href="#asc-rules">周边规则</a>
    </nav>

    <ol class="asc-guide-stages">
      <li v-for="s in stages" :id="`asc-stage-${s.key}`" :key="s.key" class="asc-guide-stage">
        <div class="asc-stage-card">
          <header class="asc-stage-heading">
            <span class="asc-stage-label">{{ s.turn }}</span>
            <h2>{{ s.name }}</h2>
          </header>
          <p class="asc-stage-description">{{ s.desc }}</p>

          <div v-if="s.good || s.evil" class="asc-stage-paths" :class="{ 'has-two': s.good && s.evil }">
            <section v-for="(branch, index) in [s.good, s.evil]" v-show="branch" :key="index" class="asc-stage-path" :data-path="index === 0 ? 'good' : 'evil'">
              <template v-if="branch">
                <h3>{{ branch.title }}</h3>
                <dl>
                  <div><dt>地点</dt><dd>{{ branch.place }}</dd></div>
                  <div v-if="branch.item && branch.item !== '—'"><dt>道具</dt><dd>{{ branch.item }}</dd></div>
                  <div><dt>条件</dt><dd>{{ branch.req }}</dd></div>
                </dl>
              </template>
            </section>
          </div>

          <div class="asc-stage-reward"><b>获得</b><span>{{ s.reward }}</span></div>
          <ul v-if="s.notes.length" class="asc-stage-notes">
            <li v-for="note in s.notes" :key="note">{{ note }}</li>
          </ul>
        </div>
      </li>
    </ol>

    <section id="asc-rules" class="asc-rules">
      <h2>飞升周边规则</h2>
      <dl class="asc-rule-list">
        <div v-for="rule in extraRules" :key="rule.k"><dt>{{ rule.k }}</dt><dd>{{ rule.v }}</dd></div>
      </dl>
    </section>
  </div>
</template>

<style scoped>
.asc-guide { color: var(--field-ink); margin-top: 20px; }
.asc-guide-nav { display: flex; gap: 7px; flex-wrap: wrap; margin: 0 0 17px; }
.asc-guide-nav a {
  display: inline-flex; align-items: center; min-height: 36px; padding: 4px 11px;
  border: 1px solid var(--field-line); border-radius: 7px; color: var(--field-accent); text-decoration: none;
  background: var(--field-bg); font-size: 14px; font-weight: 650;
}
.asc-guide-nav a:hover { border-color: var(--field-accent); }
.asc-guide-stages, .asc-stage-notes { padding: 0; list-style: none; }
.asc-guide-stages { display: grid; gap: 13px; margin: 0; }
.asc-guide-stage { position: relative; margin: 0; padding-inline-start: 23px; min-width: 0; scroll-margin-top: 106px; }
.asc-guide-stage::before {
  content: ""; position: absolute; top: 24px; inset-inline-start: 2px; width: 9px; height: 9px;
  border: 2px solid var(--field-accent); background: var(--field-paper); border-radius: 50%;
}
.asc-guide-stage:not(:last-child)::after {
  content: ""; position: absolute; top: 39px; bottom: -30px; inset-inline-start: 6px; width: 1px; background: var(--field-line);
}
.asc-stage-card { min-width: 0; border: 1px solid var(--field-line); padding: 17px 19px; border-radius: 12px; }
.asc-stage-heading { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 10px; }
.asc-stage-heading h2, .asc-rules h2 { font-family: var(--field-serif); color: var(--field-ink); border: 0; padding: 0; margin: 0; font-size: 23px; line-height: 1.4; }
.asc-stage-label { color: var(--field-accent); background: var(--field-tint); border-radius: 6px; padding: 2px 8px; font-size: 13px; font-weight: 700; }
.asc-stage-description { margin: 8px 0 13px; color: var(--field-muted); line-height: 1.75; }
.asc-stage-paths { display: grid; gap: 9px; margin-bottom: 11px; }
.asc-stage-paths.has-two { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.asc-stage-path { border: 1px solid var(--field-line); background: var(--field-bg); border-radius: 9px; padding: 10px 12px; min-width: 0; }
.asc-stage-path h3 { margin: 0 0 5px; color: var(--field-wood); font-size: 16px; }
.asc-stage-path[data-path="evil"] h3 { color: var(--field-fire); }
.asc-stage-path dl, .asc-rule-list { margin: 0; }
.asc-stage-path dl > div, .asc-stage-reward { display: grid; grid-template-columns: 3em minmax(0, 1fr); align-items: baseline; gap: 6px; }
.asc-stage-path dl > div { font-size: 14px; line-height: 1.65; margin-top: 3px; }
.asc-stage-path dt, .asc-stage-reward b { font-weight: 700; color: var(--field-accent); }
.asc-stage-path dd, .asc-rule-list dd { margin: 0; overflow-wrap: anywhere; }
.asc-stage-reward { background: var(--field-tint); border-radius: 7px; padding: 5px 9px; font-size: 14px; }
.asc-stage-notes { margin: 9px 0 0; color: var(--field-muted); font-size: 14px; line-height: 1.72; }
.asc-stage-notes li { position: relative; padding-inline-start: 13px; margin-top: 3px; }
.asc-stage-notes li::before { content: "·"; position: absolute; inset-inline-start: 2px; color: var(--field-accent); font-weight: 800; }
.asc-rules { margin-top: 28px; scroll-margin-top: 104px; }
.asc-rule-list { margin-top: 12px; border-block-start: 1px solid var(--field-line); }
.asc-rule-list > div { display: grid; grid-template-columns: 8em minmax(0, 1fr); gap: 9px; padding: 11px 2px; border-block-end: 1px solid var(--field-line); }
.asc-rule-list dt { color: var(--field-accent); font-weight: 700; }
.asc-rule-list dd { color: var(--field-muted); }
@media (max-width: 660px) {
  .asc-stage-paths.has-two, .asc-rule-list > div { grid-template-columns: 1fr; }
  .asc-stage-card { padding: 12px; }
  .asc-guide-stage { padding-inline-start: 17px; }
  .asc-stage-heading h2 { font-size: 20px; }
}
</style>
