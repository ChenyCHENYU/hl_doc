<script setup lang="ts">
// 历史陈列馆 —— 32 位时代的幻灵工具生态
// 仅作史料陈列：不提供下载、不含操作指引。

interface Exhibit {
  name: string;
  era: string;
  kind: string;
  desc: string;
  fate?: string;
}

interface Section {
  key: string;
  icon: string;
  title: string;
  intro: string;
  items: Exhibit[];
}

const SECTIONS: Section[] = [
  {
    key: "engine",
    icon: "擎",
    title: "按键脚本引擎",
    intro: "一切脚本工具的地基：把键盘鼠标动作录制成可回放的脚本，在游戏前台重复执行。",
    items: [
      {
        name: "A+（AMANI PLUS）",
        era: "2015-08-13 终极版",
        kind: "按键引擎",
        desc: "功能最全的一代脚本引擎，附 CHM 命令大全与整套 JB 脚本体系，SJ 目录里还留有 NPCCODE / PETCODE / ITEMCODE 三份游戏码表——如今反而成了资料站的珍贵数据源。",
        fate: "32 位进程，随系统退役",
      },
      {
        name: "欢乐幻灵（HLHL 0.925）",
        era: "约 2008-2012",
        kind: "脚本引擎",
        desc: "以 HLHL 为名的脚本引擎，带 Info / Scripts / Users 三层目录，玩家自写脚本在此流转，是当年最流行的自动化入口之一。",
        fate: "已停更",
      },
      {
        name: "新 HLHL（0.927）",
        era: "末代版本",
        kind: "脚本引擎",
        desc: "HLHL 系列的最后一次升级，随幻灵热度退潮而终结。同目录留存的账号信息文件属于他人隐私，本站明确拒绝收录。",
        fate: "已停更",
      },
    ],
  },
  {
    key: "sprite",
    icon: "灵",
    title: "小精灵家族",
    intro: "在引擎之上封装出的『一键托管』成品：登录、买药、战斗、修复，各有专职。",
    items: [
      {
        name: "登号小精灵",
        era: "年代不详",
        kind: "自动登录",
        desc: "负责排队登号与掉线重连，并附带冰解刷修功能，是挂机链路的第一环。",
        fate: "32 位退役",
      },
      {
        name: "宠爱精灵（拖鞋终结版）",
        era: "2008 年改版 · 2025-10 存档",
        kind: "原地挂机",
        desc: "2008 年出现的原地买药版本，配合虚拟机快照可实现长时间闯天关挂机。『绝版的拖鞋』在 2025 年 10 月仍为其写下快照内使用存档，是这套生态最后的手工业者之一。",
        fate: "快照工艺随 32 位失效",
      },
      {
        name: "云机小精灵",
        era: "云机时代",
        kind: "虚拟机托管",
        desc: "把整套『客户端 + 小精灵』搬进虚拟机托管运行，用快照对抗崩溃与内存溢出——问题大全.txt 里详细记录了这套体系的 CPU / 内存排障经验。",
        fate: "随 32 位失效",
      },
      {
        name: "快照版五系 91 宠全自动托管 0.99",
        era: "2025 年前后",
        kind: "全托管",
        desc: "小精灵生态的集大成者：五系宠物全流程自动练养，版本号停在 0.99，永远没有 1.0。",
        fate: "绝版",
      },
    ],
  },
  {
    key: "offline",
    icon: "脱",
    title: "脱机形态",
    intro: "不开游戏客户端、直接与服务器对话的形态，风险与效率都最高，也是官方封禁的主要对象。",
    items: [
      {
        name: "西瓜",
        era: "年代不详",
        kind: "脱机辅助",
        desc: "经典脱机工具，目录里同样留有一份 MAPCODE.ini 地图码表（664 张地图），本站怪物分布数据亦有引用。",
        fate: "已淘汰",
      },
    ],
  },
  {
    key: "script",
    icon: "脚",
    title: "配套脚本与补丁",
    intro: "围绕引擎与精灵流转的 ini 脚本与客户端补丁，按用途各自成包。",
    items: [
      { name: "自动摆摊 / 自动吃书 / 自动逛街", era: "脚本包", kind: "日常自动化", desc: "挂摊收钱、吃书涨技能、逛街扫货三类日常杂务的成品脚本。" },
      { name: "五类极限 · 闯天关 1-100", era: "脚本包", kind: "战斗脚本", desc: "按怪物种族与天关层数调度的战斗自动化配置。" },
      { name: "兵解药 2.0 · 装备锻造脚本", era: "脚本包", kind: "专项脚本", desc: "兵解药补给与锻造流程的专用自动化。" },
      { name: "快速端 1550 斗宠版 · 五系练宠 · 自动练级", era: "快速端系列", kind: "定制客户端", desc: "基于快速端客户端的定制发行，内置对应练级/斗宠脚本，是『改客户端』路线的代表。" },
      { name: "去神魔光 · 界面皮肤 · 好视力地图 · 绝版免动作补丁", era: "美化/性能", kind: "客户端补丁", desc: "去掉技能光效省显存、换界面皮肤、清晰战斗地图、免动作动画补丁——不改变玩法，只改变体验。" },
    ],
  },
  {
    key: "eco",
    icon: "圈",
    title: "周边生态",
    intro: "工具之外，围绕挂机形成的服务业与知识沉淀。",
    items: [
      {
        name: "东哥定制全套服务",
        era: "服务包",
        kind: "代练服务",
        desc: "一整套按需定制的代练交付物：脚本、天关/刷玉/练宠/锻造配置与服务说明。整套服务包如今静静躺在资源文件夹里，成为时代的注脚。",
      },
      {
        name: "《虚拟机小精灵问题大全》",
        era: "2025-12-29 · 绝版的拖鞋",
        kind: "运维笔记",
        desc: "最后一份系统性排障笔记：CPU 打满、内存溢出、快照回滚……把一套将死的工艺写得明明白白，堪称小精灵生态的『墓志铭』。",
      },
    ],
  },
];

const TIMELINE: { year: string; text: string }[] = [
  { year: "2003", text: "幻灵游侠开服，手动时代" },
  { year: "2008", text: "宠爱精灵原地买药版出现，脚本时代成形" },
  { year: "2015", text: "A+（AMANI PLUS）终极版定稿" },
  { year: "2025", text: "最后的维护者仍在写快照笔记与存档" },
  { year: "2026", text: "社区 64 位适配推进，32 位工具链整体退场" },
];

function img(file: string): string {
  return `/hl-assets/hl/misc/${file}`;
}
</script>

<template>
  <div class="mu">
    <div class="mu-hero">
      <div class="mu-kicker">HISTORY MUSEUM</div>
      <h1 class="mu-title">历史陈列馆</h1>
      <p class="mu-desc">
        宠爱、欢乐幻灵、A 挂、小精灵——这些名字撑起了幻灵游侠二十年的"第三方工具史"。
        它们全部运行在 32 位 Windows 之上，依附于虚拟机快照与老客户端存活；
        随着新 64 位架构落地，它们将整体退出历史舞台。本馆只做史料陈列，不提供下载与使用协助。
      </p>
    </div>

    <div class="mu-timeline">
      <div v-for="t in TIMELINE" :key="t.year" class="mu-tl-item">
        <span class="mu-tl-year">{{ t.year }}</span>
        <span class="mu-tl-dot"></span>
        <span class="mu-tl-text">{{ t.text }}</span>
      </div>
    </div>

    <section v-for="s in SECTIONS" :key="s.key" class="mu-sec">
      <h2 class="mu-sec-title">
        <span class="mu-sec-icon">{{ s.icon }}</span>
        {{ s.title }}
      </h2>
      <p class="mu-sec-intro">{{ s.intro }}</p>
      <div class="mu-grid">
        <article v-for="e in s.items" :key="e.name" class="mu-card">
          <div class="mu-card-head">
            <b class="mu-card-name">{{ e.name }}</b>
            <span class="mu-card-kind">{{ e.kind }}</span>
          </div>
          <div class="mu-card-era">{{ e.era }}</div>
          <p class="mu-card-desc">{{ e.desc }}</p>
          <div v-if="e.fate" class="mu-card-fate">已退役 · {{ e.fate }}</div>
        </article>
      </div>
    </section>

    <section class="mu-sec">
      <h2 class="mu-sec-title"><span class="mu-sec-icon">证</span>纸面证据</h2>
      <p class="mu-sec-intro">来自优化资源包的两张说明图与一份官方机制图，正式环境经 OSS 分发。</p>
      <div class="mu-figures">
        <figure class="mu-fig">
          <img :src="img('xiaojingling-intro.png')" alt="小精灵辅助功能介绍" />
          <figcaption>小精灵功能介绍（业务传单）</figcaption>
        </figure>
        <figure class="mu-fig">
          <img :src="img('business-intro.png')" alt="工具业务介绍" />
          <figcaption>定制服务业务介绍</figcaption>
        </figure>
        <figure class="mu-fig">
          <img :src="img('ban-ip-reason.png')" alt="封IP的原因" />
          <figcaption>官方封禁机制说明（封 IP 的原因）</figcaption>
        </figure>
      </div>
    </section>

    <p class="mu-note">
      本页仅作历史记录：游戏内容与版权归 网龙/天晴数码 所有；工具截图与说明仅存档展示；
      涉及他人隐私的文件（如账号信息）本站明确拒绝收录。
    </p>
  </div>
</template>

<style scoped>
.mu {
  margin: 18px 0 40px;
}

.mu-hero {
  max-width: 720px;
  margin-bottom: 26px;
}

.mu-kicker {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.22em;
  color: var(--vp-c-brand-1);
  margin-bottom: 8px;
}

.mu-title {
  margin: 0 0 12px;
  font-size: 30px;
  font-weight: 800;
  color: var(--vp-c-text-1);
  letter-spacing: 0.02em;
}

.mu-desc {
  margin: 0;
  font-size: 14.5px;
  line-height: 1.95;
  color: var(--vp-c-text-2);
}

.mu-timeline {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 22px;
  padding: 14px 18px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  margin-bottom: 30px;
}

.mu-tl-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mu-tl-year {
  font-size: 13px;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  font-variant-numeric: tabular-nums;
}

.mu-tl-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--vp-c-brand-1);
  opacity: 0.55;
}

.mu-tl-text {
  font-size: 12.5px;
  color: var(--vp-c-text-2);
}

.mu-sec {
  margin-bottom: 30px;
}

.mu-sec-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 19px;
  font-weight: 700;
  color: var(--vp-c-text-1);
  margin: 0 0 6px;
}

.mu-sec-icon {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  background: rgba(184, 134, 11, 0.08);
  border: 1px solid rgba(184, 134, 11, 0.22);
  border-radius: 8px;
}

.dark .mu-sec-icon {
  background: rgba(240, 201, 78, 0.1);
  border-color: rgba(240, 201, 78, 0.28);
}

.mu-sec-intro {
  margin: 0 0 14px;
  font-size: 13.5px;
  line-height: 1.8;
  color: var(--vp-c-text-3);
}

.mu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 12px;
}

.mu-card {
  display: flex;
  flex-direction: column;
  gap: 7px;
  padding: 16px 18px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  transition: border-color 0.15s, transform 0.15s, box-shadow 0.15s;
}

.mu-card:hover {
  border-color: rgba(184, 134, 11, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 22px rgba(184, 134, 11, 0.12);
}

.mu-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  flex-wrap: wrap;
}

.mu-card-name {
  font-size: 15px;
  font-weight: 700;
  color: var(--vp-c-text-1);
}

.mu-card-kind {
  font-size: 11.5px;
  color: var(--vp-c-brand-1);
  border: 1px solid var(--vp-c-brand-soft);
  border-radius: 999px;
  padding: 1px 10px;
  white-space: nowrap;
}

.mu-card-era {
  font-size: 12px;
  color: var(--vp-c-text-3);
  font-variant-numeric: tabular-nums;
}

.mu-card-desc {
  margin: 0;
  font-size: 13.5px;
  line-height: 1.85;
  color: var(--vp-c-text-2);
}

.mu-card-fate {
  margin-top: auto;
  padding-top: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #a05a2c;
  border-top: 1px dashed var(--vp-c-divider);
}

.dark .mu-card-fate {
  color: #e8a56a;
}

.mu-figures {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 14px;
}

.mu-fig {
  margin: 0;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  overflow: hidden;
}

.mu-fig img {
  display: block;
  width: 100%;
}

.mu-fig figcaption {
  padding: 9px 14px;
  font-size: 12.5px;
  color: var(--vp-c-text-3);
  border-top: 1px solid var(--vp-c-divider);
}

.mu-note {
  margin-top: 26px;
  padding: 12px 16px;
  border-left: 3px solid var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
  border-radius: 0 10px 10px 0;
  font-size: 12.5px;
  line-height: 1.8;
  color: var(--vp-c-text-2);
}

@media (max-width: 560px) {
  .mu-title {
    font-size: 24px;
  }

  .mu-timeline {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
