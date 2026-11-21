export type Tier = "legend" | "epic" | "elite";

export interface Hero {
  name: string;
  qq: string;
  glyph: string;
  tier: Tier;
  quote: string;
  contribution: string;
  tags: string[];
  featured?: boolean;
  placeholder?: boolean;
}

export const tierMeta: Record<Tier, { label: string }> = {
  legend: { label: "传说" },
  epic: { label: "史诗" },
  elite: { label: "精英" },
};

export const heroes: Hero[] = [
  {
    name: "虚位以待",
    qq: "",
    glyph: "侠",
    tier: "legend",
    quote: "这一格留给第一个投稿的你。",
    contribution: "投稿方式：截图 + 游戏名 + QQ + 一句话事迹，联系站长即可上墙。",
    tags: ["待投稿"],
    placeholder: true,
  },
  {
    name: "虚位以待",
    qq: "",
    glyph: "灵",
    tier: "epic",
    quote: "养宠大神的位置空着。",
    contribution: "满属性宠晒图、稀有宠收藏、成长截图皆可投稿。",
    tags: ["养宠大神", "待投稿"],
    placeholder: true,
  },
  {
    name: "虚位以待",
    qq: "",
    glyph: "战",
    tier: "elite",
    quote: "帮战之魂，等你落座。",
    contribution: "帮战战绩、跨服征伐、名场面截图皆可投稿。",
    tags: ["战斗达人", "待投稿"],
    placeholder: true,
  },
  {
    name: "虚位以待",
    qq: "",
    glyph: "匠",
    tier: "elite",
    quote: "锻造台前的身影。",
    contribution: "极品锻造记录、锻造数据整理皆可投稿。",
    tags: ["锻造达人", "待投稿"],
    placeholder: true,
  },
  {
    name: "虚位以待",
    qq: "",
    glyph: "贤",
    tier: "elite",
    quote: "写攻略的手。",
    contribution: "攻略投稿一经收录，将同步挂在对应板块的作者卡上。",
    tags: ["攻略作者", "待投稿"],
    placeholder: true,
  },
  {
    name: "虚位以待",
    qq: "",
    glyph: "侠",
    tier: "elite",
    quote: "下一个传说是谁？",
    contribution: "任何值得铭记的幻灵时刻，都欢迎上墙。",
    tags: ["待投稿"],
    placeholder: true,
  },
];
