<template>
  <div class="nf">
    <div class="nf-code">404</div>
    <h1 class="nf-title">这里空空如也</h1>
    <p class="nf-desc">
      你要找的页面可能已被移动、改名，或从未存在过。按
      <kbd>Ctrl</kbd>+<kbd>K</kbd>（macOS 为 <kbd>⌘</kbd>+<kbd>K</kbd>）可以直接搜索全站。
    </p>
    <div class="nf-links">
      <a href="/" class="nf-link">首页</a>
      <a href="/pets/" class="nf-link">宠物图鉴</a>
      <a href="/guide/" class="nf-link">宝典指南</a>
      <a href="/items/" class="nf-link">物品大全</a>
      <a href="/monsters/" class="nf-link">怪物手册</a>
      <a href="/quests/ascension" class="nf-link">飞升指南</a>
    </div>
  </div>
</template>

<style scoped>
.nf {
  padding: 72px 24px 96px;
  text-align: center;
}

.nf-code {
  font-size: 88px;
  font-weight: 800;
  line-height: 1;
  letter-spacing: 0.04em;
  background: linear-gradient(135deg, var(--vp-c-brand-1), #d4af37);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.nf-title {
  margin: 18px 0 10px;
  font-size: 26px;
  font-weight: 700;
  color: var(--vp-c-text-1);
}

.nf-desc {
  max-width: 480px;
  margin: 0 auto 28px;
  font-size: 14.5px;
  line-height: 1.9;
  color: var(--vp-c-text-2);
}

.nf-desc kbd {
  padding: 1px 7px;
  border: 1px solid var(--vp-c-divider);
  border-bottom-width: 2px;
  border-radius: 6px;
  background: var(--vp-c-bg-soft);
  font-size: 12.5px;
  font-family: var(--vp-font-family-mono);
}

.nf-links {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.nf-link {
  display: inline-flex;
  align-items: center;
  min-height: 40px;
  padding: 8px 20px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: border-color 0.15s, transform 0.15s, box-shadow 0.15s;
}

.nf-link:hover {
  border-color: var(--vp-c-brand-1);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(184, 134, 11, 0.14);
}
</style>
