export interface MortalTitle {
  range: string;
  title: string;
}

export interface Ascension {
  turn: string;
  good: { title: string; req: string };
  evil: { title: string; req: string };
}

export const mortalTitles: MortalTitle[] = [
  { range: "1 – 50 级", title: "见习武士" },
  { range: "50 – 150 级", title: "初级武士" },
  { range: "150 – 300 级", title: "高级武士" },
  { range: "300 – 500 级", title: "侠客" },
  { range: "500 – 700 级", title: "豪侠" },
  { range: "700 – 900 级", title: "隐侠" },
  { range: "900 – 1100 级", title: "宗师" },
  { range: "1100 – 1200 级", title: "武神" },
];

export const ascensions: Ascension[] = [
  {
    turn: "一转",
    good: { title: "散仙", req: "800 – 1200 级飞升" },
    evil: { title: "散仙", req: "800 – 1200 级飞升（正邪同源）" },
  },
  {
    turn: "二转",
    good: { title: "地仙", req: "散仙入仙" },
    evil: { title: "夜叉", req: "散仙入魔" },
  },
  {
    turn: "三转",
    good: { title: "天仙", req: "1000 级 + 800-1250 级忠诚 100 绿衣仙子（玉露丹 → 青云仙子）" },
    evil: { title: "阿修罗", req: "1000 级 + 800-1250 级忠诚 100 黄龙使（天魔散 → 地狱飞龙）" },
  },
  {
    turn: "四转",
    good: { title: "大罗金仙", req: "完成某一系宠物图鉴" },
    evil: { title: "魔神", req: "完成某一系宠物图鉴" },
  },
  {
    turn: "五转",
    good: { title: "天神", req: "完成一种属性任务，按七种职业要求飞升" },
    evil: { title: "魔尊", req: "完成一种属性任务，按七种职业要求飞升" },
  },
];

export interface GodJob {
  name: string;
  domain: string;
}

export const godJobs: GodJob[] = [
  { name: "火淬天神", domain: "锻造" },
  { name: "尚武天神", domain: "创招" },
  { name: "巡游天神", domain: "修行" },
  { name: "通灵天神", domain: "养宠" },
  { name: "功德天神", domain: "功德" },
];

export const demonJobs: GodJob[] = [
  { name: "幻变魔尊", domain: "偷窃" },
  { name: "嗜血魔尊", domain: "声望" },
  { name: "堕天魔尊", domain: "修行" },
  { name: "摄魂魔尊", domain: "养宠" },
  { name: "泯灭魔尊", domain: "功德" },
];
