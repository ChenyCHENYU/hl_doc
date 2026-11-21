export interface HelpTopic {
  title: string;
  source: string;
  status: "recorded" | "pending";
}

export interface HelpCategory {
  key: string;
  title: string;
  topics: HelpTopic[];
}

export const helpCategories: HelpCategory[] = [
  {
    key: "gr",
    title: "人物相关",
    topics: [
      { title: "创建", source: "help29.htm", status: "pending" },
      { title: "属性", source: "help43.htm", status: "pending" },
      { title: "称号", source: "help19.htm", status: "pending" },
      { title: "装备", source: "help42.htm", status: "pending" },
      { title: "兵解", source: "help04.htm", status: "pending" },
    ],
  },
  {
    key: "cw",
    title: "宠物相关",
    topics: [
      { title: "综述", source: "help06.htm", status: "recorded" },
      { title: "属性", source: "help13.htm", status: "pending" },
      { title: "进化", source: "help10.htm", status: "recorded" },
      { title: "幻化", source: "help28.htm", status: "pending" },
      { title: "技能", source: "help09.htm", status: "pending" },
      { title: "摆摊", source: "help07.htm", status: "pending" },
      { title: "斗宠", source: "help21.htm", status: "pending" },
    ],
  },
  {
    key: "xx",
    title: "战斗相关",
    topics: [
      { title: "回合战斗", source: "help53.htm", status: "pending" },
      { title: "即时战斗", source: "help57.htm", status: "pending" },
      { title: "自创武功", source: "help47.htm", status: "pending" },
      { title: "修练武功", source: "help46.htm", status: "pending" },
      { title: "捕捉宠物", source: "help55.htm", status: "pending" },
    ],
  },
  {
    key: "wh",
    title: "帮派相关",
    topics: [
      { title: "创建帮派", source: "help15.htm", status: "pending" },
      { title: "帮派功能", source: "help02.htm", status: "pending" },
      { title: "设立总坛", source: "help61.htm", status: "pending" },
      { title: "帮派传送", source: "help62.htm", status: "pending" },
    ],
  },
  {
    key: "gl",
    title: "其他帮助",
    topics: [
      { title: "锻造", source: "help23.htm", status: "pending" },
      { title: "婚姻", source: "help30.htm", status: "pending" },
      { title: "建筑", source: "help31.htm", status: "pending" },
      { title: "界面", source: "help60.htm", status: "pending" },
      { title: "银行", source: "help18.htm", status: "pending" },
      { title: "交易", source: "help33.htm", status: "pending" },
      { title: "赌场", source: "help22.htm", status: "pending" },
    ],
  },
];
