export interface EvolutionChain {
  tier: string;
  examples: string[];
}

export interface PetRule {
  title: string;
  detail: string;
}

export const evolutionChains: EvolutionChain[] = [
  { tier: "一级进化宠", examples: ["小狗匆匆"] },
  { tier: "二级进化宠", examples: ["敖日犬"] },
  { tier: "三级进化宠", examples: ["奇变天狼"] },
  { tier: "终级宠物", examples: ["火妖精"] },
];

export const petRules: PetRule[] = [
  {
    title: "进化条件",
    detail: "宠物达到 500 级以上且忠诚度 100，二、三级进化宠由相应低一级宠物进化而来。",
  },
  {
    title: "终级宠物",
    detail: "由两只 1000 级以上、幻化过两次的三级进化宠幻化得到，过程十分复杂。",
  },
  {
    title: "变异与五行",
    detail: "进化过程可能变异为另一颜色的同族宠物；想避免变异，需选择与宠物五行属性相同的地图进化。",
  },
  {
    title: "勋章继承",
    detail: "进化得到的是一级新宠，可继承旧宠所有勋章；旧宠等级高且养护好还有机会获得勋章奖励。",
  },
];
