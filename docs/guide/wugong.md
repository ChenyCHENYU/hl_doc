---
title: 自创武功 · 创招全流程
---

# 自创武功 · 创招全流程

武功自创是幻灵游侠的招牌系统：招式名、内力配比、攻击系数、特效全部由玩家定义，
创招成功全服通告。本页把 help47（自创武功）+ help46（修练武功）拆成流程与公式卡，
配《招系数排名》大图。

<div class="wg-steps">
  <div class="wg-step">
    <span class="wg-num">1</span>
    <b>确认资格</b>
    <p>凡人 300 级以上，或飞升后的散仙 100 级以上；内力属性 ≥ 100 点。</p>
  </div>
  <div class="wg-step">
    <span class="wg-num">2</span>
    <b>打开创招面板</b>
    <p>游戏菜单 → 武功自创面板；此时会校验等级与内力门槛。</p>
  </div>
  <div class="wg-step">
    <span class="wg-num">3</span>
    <b>命名与调参</b>
    <p>取一个响亮的名字；设定使用内力（≤ 你的内力属性点）与攻击系数，选择特效动画。</p>
  </div>
  <div class="wg-step">
    <span class="wg-num">4</span>
    <b>确认成功率</b>
    <p>界面上的成功率估测相当准确；系数越低成功率越高，追求高系数要做好失败准备。</p>
  </div>
  <div class="wg-step">
    <span class="wg-num">5</span>
    <b>创招成功</b>
    <p>系统全服通告；招式可自用，也可传授给队友分享。</p>
  </div>
</div>

<h2 class="wg-h">核心公式</h2>

<div class="wg-formulas">
  <div class="wg-f">
    <span class="wg-f-name">攻击效果</span>
    <code>攻击效果 = 攻击系数 × 所用内力</code>
  </div>
  <div class="wg-f">
    <span class="wg-f-name">系数上限</span>
    <code>攻击系数上限 = [150 + (攻击点数 − 600) × 5 / 140] / 100</code>
  </div>
  <div class="wg-f">
    <span class="wg-f-name">内力上限</span>
    <code>可用内力 ≤ 内力属性点（如 180 点 → 招式内力 ≤ 180）</code>
  </div>
</div>

> 界面会自动控制数值范围，公式用于估算收益；修练层面的进阶说明见宝典专题
> 专题卡片（[战斗相关 · 专题卡片](/guide/cards/xx) 内《自创武功》《修练武功》）。

<AdvChart img="/hl-assets/hl/charts/zhao-coeff-rank.jpg" title="武功招式系数排名（全服招式参考）" />

<TopicRelated cat="战斗相关" topic="武功" />

<style>
.wg-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 12px;
  margin: 20px 0 26px;
  counter-reset: wg;
}

.wg-step {
  position: relative;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  padding: 16px 16px 14px;
  transition: border-color 0.15s, transform 0.15s;
}

.wg-step:hover {
  border-color: rgba(184, 134, 11, 0.45);
  transform: translateY(-2px);
}

.wg-num {
  display: inline-flex;
  width: 30px;
  height: 30px;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 14px;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  border: 1.5px solid var(--vp-c-brand-soft);
  background: var(--vp-c-brand-soft);
  margin-bottom: 10px;
}

.wg-step b {
  display: block;
  font-size: 14.5px;
  color: var(--vp-c-text-1);
  margin-bottom: 6px;
}

.wg-step p {
  margin: 0;
  font-size: 12.5px;
  line-height: 1.7;
  color: var(--vp-c-text-2);
}

.wg-h {
  font-size: 19px;
  font-weight: 700;
  margin: 26px 0 12px;
}

.wg-formulas {
  display: grid;
  gap: 10px;
  margin-bottom: 22px;
}

.wg-f {
  display: flex;
  align-items: center;
  gap: 14px;
  border: 1px dashed var(--vp-c-divider);
  border-radius: 10px;
  padding: 12px 16px;
  background: var(--vp-c-bg-soft);
}

.wg-f-name {
  flex-shrink: 0;
  font-size: 12.5px;
  font-weight: 700;
  color: var(--vp-c-brand-1);
  width: 5em;
}

.wg-f code {
  font-size: 13.5px;
  color: var(--vp-c-text-1);
  background: transparent;
  padding: 0;
}
</style>
