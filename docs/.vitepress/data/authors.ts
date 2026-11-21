// 贡献者/作者档案 —— 内容板块署名用（AuthorCard）
// qq 为空时头像回退首字、不显示 QQ 徽章；投稿后补齐即可
export interface Author {
  key: string;
  name: string;
  qq: string;
  tags: string[];
  contribution: string;
  works?: { title: string; link: string }[];
}

export const authors: Author[] = [
  {
    key: "jianyu",
    name: "剑雨",
    qq: "",
    tags: ["满属性理论奠基人", "数据流大神"],
    contribution:
      "满属性宠理论体系的开创者：宠物代数、进化/幻化成长公式、幻化副宠五原则、出双概率与成长控制全套方法均出自其手稿，本站「满属性理论基础」全文收录。",
    works: [{ title: "满属性理论基础", link: "/advanced/manxing-jianyu" }],
  },
  {
    key: "hentian",
    name: "恨天",
    qq: "",
    tags: ["满属性实操", "养宠达人"],
    contribution:
      "云狐满属性全流程实操记录的提供者，1550 后锻造减属性、幻化固定三围的一手截图与步骤由其整理成稿。",
    works: [{ title: "满属性实操：云狐", link: "/advanced/manxing-yunhu" }],
  },
  {
    key: "tuoxie",
    name: "绝版的拖鞋",
    qq: "",
    tags: ["辅助大神", "工具考古"],
    contribution:
      "32 位时代小精灵生态的最后维护者：宠爱精灵终结版存档、《虚拟机小精灵问题大全》排障笔记（2025-12）皆出其手，是历史陈列馆最重要的史料来源。",
    works: [{ title: "历史陈列馆", link: "/museum/" }],
  },
  {
    key: "dongge",
    name: "东哥",
    qq: "",
    tags: ["锻造大神", "定制服务"],
    contribution:
      "锻造相生相克五行位置图、宠物进化次序图等经典图表的作者，当年按需定制天关/刷玉/练宠/锻造脚本全套服务，图表至今仍是本站玩法图表页的镇页之宝。",
    works: [{ title: "玩法图表", link: "/advanced/charts" }],
  },
  {
    key: "fengzhigu",
    name: "风之谷·极度",
    qq: "",
    tags: ["锻造数据整理"],
    contribution:
      "《幻灵锻造宝典》整理编辑者，搜集全部最新最全的锻造数据成册，本站锻造词条数据的重要源头之一。",
  },
  {
    key: "zhanzhang",
    name: "站长",
    qq: "",
    tags: ["站长", "全栈搬运工"],
    contribution:
      "本站搭建与维护：数据管线、页面设计与史料数字化。有资料要投稿、有错误要反馈，欢迎联系。",
  },
];

export const authorByKey: Record<string, Author> = Object.fromEntries(authors.map((a) => [a.key, a]));
