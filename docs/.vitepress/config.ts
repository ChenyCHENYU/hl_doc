import { defineConfig } from "vitepress";
import type { Plugin } from "vite";
import { readFileSync, statSync } from "node:fs";
import { resolve, extname, relative, isAbsolute } from "node:path";
import { fileURLToPath } from "node:url";
const CONFIG_DIR = fileURLToPath(new URL(".", import.meta.url));
const ASSETS_BASE = resolve(CONFIG_DIR, "../../assets");
type SidebarGroup = { text: string; collapsed: boolean; items: { text: string; link: string }[] };
function readData(name: string) {
  return JSON.parse(readFileSync(resolve(CONFIG_DIR, "data", name), "utf-8"));
}
const helpSidebarGroups: SidebarGroup[] = readData("help-sidebar.json");
const librarySidebar: SidebarGroup[] = readData("library-sidebar.json");

const MIME: Record<string, string> = {
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
};

function hlLocalAssets(): Plugin {
  const handler = (req: any, res: any, next: () => void) => {
    if (!req.url || !req.url.startsWith("/hl-assets/")) return next();
    let rel: string;
    try {
      rel = decodeURIComponent(req.url.slice("/hl-assets/".length).split("?")[0]);
    } catch {
      res.statusCode = 400;
      return res.end();
    }
    const file = resolve(ASSETS_BASE, rel);
    const fromBase = relative(ASSETS_BASE, file);
    if (isAbsolute(fromBase) || /^\.\.(?:[\\/]|$)/.test(fromBase)) {
      res.statusCode = 403;
      return res.end();
    }
    try {
      const data = readFileSync(file);
      res.setHeader("Content-Type", MIME[extname(file).toLowerCase()] || "application/octet-stream");
      res.setHeader("Cache-Control", "no-store");
      res.end(data);
    } catch {
      res.statusCode = 404;
      res.end();
    }
  };
  return {
    name: "hl-local-assets",
    configureServer(server) {
      server.middlewares.use(handler);
    },
    configurePreviewServer(server) {
      server.middlewares.use(handler);
    },
  };
}

const petCodex: { id: number; name: string }[] = readData("pet-codex.json");
const libraryCount = readData("library.json").length;
const petNameById = new Map(petCodex.map((p: { id: number; name: string }) => [String(p.id), p.name]));

export default defineConfig({
  transformPageData(pageData) {
    const m = pageData.relativePath?.match(/^pets\/(\d+)\.md$/);
    if (m) {
      const name = petNameById.get(m[1]);
      if (name) {
        pageData.title = `${name} - 宠物图鉴`;
        pageData.description = `${name}的档案：一级属性、2026标准成长、进化系谱、抓取出处与重塑价格。`;
      }
    }
  },
  title: "幻灵宝典",
  description: "幻灵游侠 2.5 非官方玩家资料站 — 游戏内宝典 · 宠物图鉴 · 物品大全 · 新手指引线上化",
  lang: "zh-CN",
  head: [
    ["link", { rel: "icon", href: "/logo.png" }],
    ["meta", { name: "theme-color", content: "#263d33" }],
    ["meta", { property: "og:site_name", content: "幻灵宝典" }],
    ["meta", { property: "og:type", content: "website" }],
    ["meta", { property: "og:description", content: `幻灵游侠 2.5 玩家资料站：${petCodex.length} 只宠物档案、${libraryCount} 篇玩家文库，以及任务和练级地图。` }],
  ],
  sitemap: process.env.DEPLOY_URL ? { hostname: process.env.DEPLOY_URL } : undefined,
  ignoreDeadLinks: [/^\/pets\/\d+$/],
  markdown: {
    config(md) {
      md.renderer.rules.table_open = (tokens, index, options, _env, renderer) => {
        tokens[index].attrJoin("class", "wiki-text-table");
        return renderer.renderToken(tokens, index, options);
      };
    },
  },
  vite: {
    plugins: [hlLocalAssets()],
    // 允许 TWIKOO_ENV_ID 等业务变量进入客户端（默认仅 VITE_ 前缀）
    envPrefix: ["VITE_", "TWIKOO_", "DEPLOY_"],
    server: {
      watch: {
        ignored: ["**/dist/**"],
      },
    },
  },
  themeConfig: {
    logo: "/logo.png",
    nav: [
      { text: "攻略", activeMatch: "^/(quests|advanced)/", items: [
        { text: "任务攻略", link: "/quests/" }, { text: "飞升指南", link: "/quests/ascension" },
        { text: "养成进阶", link: "/advanced/" }, { text: "宝典指南", link: "/guide/" },
      ] },
      { text: "图鉴", activeMatch: "^/(pets|items)/", items: [
        { text: "宠物图鉴", link: "/pets/" }, { text: "物品大全", link: "/items/" },
        { text: "进化系谱", link: "/pets/evolutions" },
      ] },
      { text: "地图与天关", activeMatch: "^/(maps|monsters)/", items: [
        { text: "地图与练级", link: "/maps/" }, { text: "天关防御表", link: "/monsters/" },
      ] },
      { text: "查资料", link: "/search/" },
      { text: "更多", items: [
        { text: "全部栏目", link: "/guide/catalog" },
        { text: "玩家文库", link: "/guide/library/" }, { text: "资源与画廊", link: "/resources/" },
        { text: "英雄墙", link: "/heroes/" }, { text: "历史陈列馆", link: "/museum/" },
        { text: "关于本站", link: "/about/" },
      ] },
    ],
    sidebar: {
      "/guide/": [
        { text: "总览", items: [{ text: "分类总览", link: "/guide/" }, { text: "全部栏目", link: "/guide/catalog" }] },
        ...helpSidebarGroups,
        { text: "玩家文库", collapsed: false, items: [{ text: "文库总览", link: "/guide/library/" }] },
        ...librarySidebar,
      ],
      "/pets/": [
        {
          text: "宠物图鉴",
          items: [
            { text: "图鉴总览", link: "/pets/" },
            { text: "进化系谱大全", link: "/pets/evolutions" },
            { text: "重塑价格表", link: "/pets/prices" },
          ],
        },
      ],
      "/items/": [
        {
          text: "物品大全",
          items: [{ text: "物品条目", link: "/items/" }],
        },
      ],
      "/monsters/": [
        {
          text: "怪物手册",
          items: [
            { text: "总览", link: "/monsters/" },
            { text: "天关防御参数", link: "/monsters/#天关防御参数表" },
          ],
        },
      ],
      "/quests/": [
        {
          text: "任务攻略",
          items: [
            { text: "总览", link: "/quests/" },
            { text: "飞升全指南（0-5 转）", link: "/quests/ascension" },
            { text: "水属性任务", link: "/quests/water" },
            { text: "火属性任务", link: "/quests/fire" },
            { text: "全部飞升攻略", link: "/quests/ascend" },
            { text: "2025 新宠终极规则", link: "/quests/rules2025" },
            { text: "进化幻化公式", link: "/quests/formula" },
            { text: "手机玩与回归", link: "/quests/return" },
          ],
        },
      ],
      "/advanced/": [
        {
          text: "养成进阶",
          items: [
            { text: "总览", link: "/advanced/" },
            { text: "满属性理论（剑雨）", link: "/advanced/manxing-jianyu" },
            { text: "满属性实操（云狐）", link: "/advanced/manxing-yunhu" },
            { text: "满属性实操（AD）", link: "/advanced/manxing-ad" },
            { text: "玩法图表", link: "/advanced/charts" },
            { text: "小技巧合集", link: "/advanced/tips" },
          ],
        },
      ],
      "/heroes/": [
        {
          text: "幻灵英雄墙",
          items: [{ text: "玩家风采", link: "/heroes/" }],
        },
      ],
      "/resources/": [
        {
          text: "资源库",
          items: [
            { text: "总览与画廊", link: "/resources/" },
          ],
        },
      ],
      "/museum/": [
        {
          text: "历史陈列馆",
          items: [
            { text: "32 位工具生态", link: "/museum/" },
          ],
        },
      ],
      "/about/": [
        {
          text: "关于本站",
          items: [{ text: "关于本站", link: "/about/" }],
        },
      ],
    },
    search: {
      provider: "local",
      options: {
        translations: {
          button: { buttonText: "搜索", buttonAriaLabel: "搜索" },
          modal: {
            noResultsText: "未找到相关结果",
            resetButtonTitle: "清除查询",
            footer: { selectText: "选择", navigateText: "切换", closeText: "关闭" },
          },
        },
      },
    },
    outline: { label: "页面导航", level: [2, 3] },
    sidebarMenuLabel: "目录",
    docFooter: { prev: "上一页", next: "下一页" },
    returnToTopLabel: "返回顶部",
    footer: {
      message: "非官方粉丝资料站，游戏内容及版权归 网龙/天晴数码 所有，资料来源见关于本站。",
      copyright: "如有异议请联系站长撤除",
    },
  },
});
