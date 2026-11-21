<script setup lang="ts">
import { heroes, tierMeta } from "../../data/heroes";

function avatar(hero: { qq: string }): string {
  if (hero.qq && /^\d{5,11}$/.test(hero.qq)) {
    return `https://q1.qlogo.cn/g?b=qq&nk=${hero.qq}&s=100`;
  }
  return "";
}
</script>

<template>
  <div class="gwall">
    <article
      v-for="(hero, i) in heroes"
      :key="i"
      class="gcard"
      :class="[`tier-${hero.tier}`, { 'is-featured': hero.featured }]"
    >
      <div class="gcard-art">
        <div class="art-glyph">
          <span class="glyph-ring" />
          <span class="glyph-ring glyph-ring--outer" />
          <span class="glyph-text">{{ hero.glyph }}</span>
        </div>
        <span class="art-tier">{{ tierMeta[hero.tier].label }}</span>
      </div>
      <div class="gcard-body">
        <div class="gcard-head">
          <img v-if="avatar(hero)" class="gavatar" :src="avatar(hero)" :alt="hero.name" loading="lazy" />
          <div class="gcard-name-wrap">
            <div class="gcard-name">{{ hero.name }}</div>
            <span v-if="hero.qq" class="gqq">QQ {{ hero.qq }}</span>
          </div>
        </div>
        <p class="gcard-quote">「{{ hero.quote }}」</p>
        <p class="gcard-contrib">{{ hero.contribution }}</p>
        <div class="gcard-tags">
          <span v-for="t in hero.tags" :key="t" class="gtag">{{ t }}</span>
        </div>
      </div>
    </article>
  </div>
</template>

<style scoped>
.gwall {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 18px;
  margin: 24px 0 32px;
}

.gcard {
  position: relative;
  border-radius: 18px;
  overflow: hidden;
  text-decoration: none;
  background:
    linear-gradient(var(--vp-c-bg), var(--vp-c-bg)) padding-box,
    linear-gradient(160deg, var(--tier-1), var(--tier-2) 55%, var(--tier-3)) border-box;
  border: 1.5px solid transparent;
  box-shadow:
    0 0 0 1px rgba(0, 0, 0, 0.04),
    0 10px 34px -14px var(--tier-glow);
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.25s ease;
}

.gcard:hover {
  transform: translateY(-4px);
  box-shadow:
    0 0 0 1px rgba(0, 0, 0, 0.05),
    0 18px 44px -14px var(--tier-glow),
    0 0 60px -18px var(--tier-glow);
}

.gcard::after {
  content: "";
  position: absolute;
  top: -60%;
  left: -80%;
  width: 55%;
  height: 220%;
  background: linear-gradient(
    100deg,
    transparent 40%,
    rgba(255, 255, 255, 0.16) 47%,
    rgba(255, 255, 255, 0.05) 53%,
    transparent 60%
  );
  transform: rotate(0.001deg);
  transition: left 0.7s cubic-bezier(0.4, 0, 0.2, 1);
  pointer-events: none;
  z-index: 3;
}

.gcard:hover::after {
  left: 130%;
}

.gcard.tier-legend {
  --tier-1: #f5d67b;
  --tier-2: #b8860b;
  --tier-3: #7a5a0c;
  --tier-glow: rgba(212, 175, 55, 0.42);
}

.gcard.tier-epic {
  --tier-1: #6fd0a5;
  --tier-2: #2e9e6f;
  --tier-3: #1c6e4c;
  --tier-glow: rgba(59, 162, 114, 0.36);
}

.gcard.tier-elite {
  --tier-1: #d4d9e2;
  --tier-2: #97a0b0;
  --tier-3: #6b7382;
  --tier-glow: rgba(130, 140, 160, 0.3);
}

.gcard.is-featured {
  grid-column: span 2;
  display: grid;
  grid-template-columns: 240px 1fr;
}

.gcard-art {
  position: relative;
  min-height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
  background:
    radial-gradient(ellipse 90% 70% at 50% 115%, var(--tier-glow) 0%, transparent 62%),
    radial-gradient(ellipse 120% 90% at 50% -20%, color-mix(in srgb, var(--tier-2) 24%, transparent) 0%, transparent 60%),
    linear-gradient(180deg, color-mix(in srgb, var(--tier-1) 10%, var(--vp-c-bg)), color-mix(in srgb, var(--tier-3) 16%, var(--vp-c-bg)));
  overflow: hidden;
}

.gcard-art::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(color-mix(in srgb, var(--tier-1) 7%, transparent) 1px, transparent 1px),
    linear-gradient(90deg, color-mix(in srgb, var(--tier-1) 7%, transparent) 1px, transparent 1px);
  background-size: 26px 26px;
  mask-image: radial-gradient(ellipse 90% 80% at 50% 55%, black 0%, transparent 80%);
  -webkit-mask-image: radial-gradient(ellipse 90% 80% at 50% 55%, black 0%, transparent 80%);
}

.art-glyph {
  position: relative;
  width: 96px;
  height: 96px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: glyph-float 5s ease-in-out infinite;
}

@keyframes glyph-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.glyph-ring,
.glyph-ring--outer {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 1.5px solid color-mix(in srgb, var(--tier-1) 55%, transparent);
}

.glyph-ring--outer {
  inset: -12px;
  border-style: dashed;
  border-color: color-mix(in srgb, var(--tier-1) 32%, transparent);
  animation: ring-spin 26s linear infinite;
}

@keyframes ring-spin {
  to { transform: rotate(360deg); }
}

.glyph-text {
  font-size: 46px;
  font-weight: 800;
  line-height: 1;
  background: linear-gradient(160deg, var(--tier-1), var(--tier-2));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 40px var(--tier-glow);
}

.art-tier {
  position: absolute;
  bottom: 12px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.28em;
  color: color-mix(in srgb, var(--tier-1) 85%, var(--vp-c-text-2));
}

.gwall .gcard {
  animation: hl-fade-up 0.5s ease both;
}

.gwall .gcard:nth-child(1) { animation-delay: 0.05s; }
.gwall .gcard:nth-child(2) { animation-delay: 0.13s; }
.gwall .gcard:nth-child(3) { animation-delay: 0.21s; }
.gwall .gcard:nth-child(4) { animation-delay: 0.29s; }
.gwall .gcard:nth-child(5) { animation-delay: 0.37s; }
.gwall .gcard:nth-child(6) { animation-delay: 0.45s; }

@media (prefers-reduced-motion: reduce) {
  .gwall .gcard { animation: none; }
}

.gcard-body {
  padding: 18px 20px 20px;
  display: flex;
  flex-direction: column;
}

.gcard-head {
  display: flex;
  align-items: center;
  gap: 12px;
}

.gavatar {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  background: #fff;
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.05);
}

.gcard-name-wrap {
  min-width: 0;
}

.gcard-name {
  font-size: 19px;
  font-weight: 700;
  letter-spacing: 0.01em;
  color: var(--vp-c-text-1);
}

.gqq {
  display: inline-block;
  margin-top: 3px;
  font-size: 12px;
  font-weight: 600;
  color: var(--vp-c-brand-1);
  border: 1px solid var(--vp-c-brand-soft);
  border-radius: 999px;
  padding: 0 9px;
  font-variant-numeric: tabular-nums;
}

.gcard-quote {
  margin: 12px 0 8px;
  font-size: 13.5px;
  line-height: 1.7;
  color: var(--vp-c-text-2);
}

.gcard-contrib {
  margin: 0 0 12px;
  font-size: 12.5px;
  line-height: 1.75;
  color: var(--vp-c-text-3);
  flex: 1;
}

.gcard-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.gtag {
  font-size: 12px;
  color: var(--vp-c-text-3);
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  padding: 1px 11px;
}

.gtag--cta {
  color: var(--vp-c-brand-1);
  border-color: color-mix(in srgb, var(--tier-1) 45%, transparent);
  background: color-mix(in srgb, var(--tier-1) 9%, transparent);
  font-weight: 600;
}

@media (max-width: 960px) {
  .gcard.is-featured {
    grid-column: span 1;
    grid-template-columns: none;
  }
}

@media (max-width: 700px) {
  .gwall {
    grid-template-columns: 1fr;
  }
}
</style>
