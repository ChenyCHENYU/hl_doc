<script setup lang="ts">
import CopyField from "./CopyField.vue";

const areas = [
  {
    id: "new-mountain-1", tier: "一层", name: "九曲回廊（1）", mapId: "131006",
    mobs: "红锦宝、呆刺头、衰呆象、欢欢熊", points: ["5,15", "33,41"],
    evidence: "练级资料里，（5,15）附近的参考值约为 4000 人防。另一份宠物路线在（33,41）记录了衰呆象和欢欢熊。",
    note: "低防时优先试一层。换点可能遇到不同怪组，观察掉血和经验后再决定是否上楼。",
  },
  {
    id: "new-mountain-2", tier: "二层", name: "九曲回廊（2）", mapId: "131007",
    mobs: "楞头青、跷跷鼠、酷刺头、小妖", points: ["33,37", "15,21"],
    evidence: "（33,37）的两份练级记录分别写了 4200 和 4500 人防。（15,21）的旧攻略记录的是酷刺头、小妖，且同时给出了敏捷要求。",
    note: "从一层转来可优先试（33,37）。4500 是一份参考值，不代表所有怪组都能稳定打。",
  },
  {
    id: "new-mountain-3", tier: "三层", name: "九曲回廊（3）", mapId: "131008",
    mobs: "草莽兔、铁甲龟、淘淘、努努鸟", points: ["29,30", "29,40"],
    evidence: "同在（29,30），两份练级记录分别标 4600 和 5000 人防。另一份攻略的（29,40）用较低防御，但同时要求约 3500 敏捷，并以战斗宠能秒怪为前提。",
    note: "有玩家在 4500 防时被带阵怪物击倒。阵型、怪物数量、出手顺序和当前血量都会影响结果；先在同一点试打，包括带阵的场次。",
  },
  {
    id: "new-mountain-4", tier: "四层", name: "清幽古洞", mapId: "131009",
    mobs: "珍珍、西皮、露露鸟、纹地龙", points: ["31,46", "45,21"],
    evidence: "不同练级记录给出的参考值约为 5100 至 5800 人防，且涉及不同坐标、怪组和敏捷条件。",
    note: "按实际准备和同坐标试打选择。旧攻略里的最低数字不能用作挂机保证。",
  },
];
</script>

<template>
  <div class="field-ui field-reading map-guide">
    <p class="map-lead">查地图编号、常见练级坐标和怪物组合。不同站位遇到的怪可能不同，防御数字要连同出手顺序、宠物和阵型一起看。</p>
    <nav class="map-nav" aria-label="本页地图">
      <a v-for="area in areas" :key="area.id" :href="`#${area.id}`">新山{{ area.tier }}</a>
      <a href="#ice-crystal">玉洁桥</a>
      <a href="/monsters/#天关防御参数表">天关防御表 ↗</a>
    </nav>

    <section v-for="area in areas" :id="area.id" :key="area.id" class="map-area">
      <div class="map-heading">
        <span>新山城 · {{ area.tier }}</span>
        <h2>{{ area.name }}</h2>
        <p>地图编号 {{ area.mapId }}</p>
      </div>
      <dl class="map-fields">
        <div><dt>常见怪物</dt><dd>{{ area.mobs }}</dd></div>
        <div><dt>资料坐标</dt><dd class="map-points"><CopyField v-for="point in area.points" :key="point" :value="point" /></dd></div>
        <div><dt>防御参考</dt><dd>{{ area.evidence }}</dd></div>
      </dl>
      <p class="map-risk">{{ area.note }}</p>
    </section>

    <section id="ice-crystal" class="map-area">
      <div class="map-heading"><span>雪城 · 任务地点</span><h2>玉洁桥</h2></div>
      <dl class="map-fields">
        <div><dt>任务 NPC</dt><dd>常枫 <CopyField value="40,20" /></dd></div>
        <div><dt>出现时段</dt><dd>每天 20:00–21:00，按游戏内时间确认。</dd></div>
        <div><dt>所需材料</dt><dd>先在玉洁桥打到 6 个冰石，再找常枫换冰晶。</dd></div>
      </dl>
      <a href="/quests/fire#fire-step-10">返回火任务 · 第 10 步 →</a>
    </section>

    <aside class="map-source">
      <h2>资料依据</h2>
      <ul>
        <li><a href="/guide/library/lib-009">宠物分布与怪物属性旧表</a></li>
        <li><a href="/guide/library/bd-151">地图名称与编号对照</a></li>
        <li><a href="/guide/library/bd-003">玩家练级路线及配装条件</a></li>
      </ul>
      <p>参考防御为旧资料及本地玩家记录对照。缺少区服或完整配装的数据用作试打线索。</p>
    </aside>
  </div>
</template>

<style scoped>
.map-lead { margin: 14px 0 21px; color: var(--field-muted); }
.map-nav { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 22px; }
.map-nav a { padding: 5px 10px; border: 1px solid var(--field-line); border-radius: 8px; text-decoration: none; font-size: 14px; color: var(--field-accent); background: var(--field-paper); }
.map-nav a:hover { border-color: var(--field-accent); }
.map-area { margin: 0 0 18px; border: 1px solid var(--field-line); background: var(--field-paper); border-radius: 14px; padding: 18px 22px; scroll-margin-top: 110px; }
.map-heading { display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap; }
.map-heading span, .map-heading p { color: var(--field-muted); font-size: 13px; margin: 0; }
.map-heading h2 { margin: 0; padding: 0; border: 0; font-size: clamp(21px, 4vw, 27px); }
.map-fields { margin: 12px 0; }
.map-fields > div { display: grid; grid-template-columns: 5em minmax(0, 1fr); gap: 10px; border-top: 1px solid var(--field-line); padding: 7px 0; }
.map-fields dt { color: var(--field-accent); font-weight: 700; }
.map-fields dd { margin: 0; }
.map-points { display: flex; flex-wrap: wrap; gap: 10px; }
.map-risk { padding: 9px 13px; margin: 0; background: var(--field-tint); border-radius: 8px; }
.map-source { color: var(--field-muted); font-size: 14px; }
.map-source h2 { font-size: 20px; }
@media (max-width: 550px) {
  .map-area { padding: 14px; }
  .map-fields > div { grid-template-columns: 1fr; gap: 1px; }
}
</style>
