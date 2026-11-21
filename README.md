# 幻灵宝典 — 幻灵游侠 2.5 玩家资料站

基于 VitePress 2 的非官方粉丝资料站，目标：游戏内宝典、宠物、物品资料线上化、结构化。

## 本地开发

```bash
pnpm install
pnpm dev        # http://localhost:8877
pnpm build      # 构建校验
pnpm preview
```

首页可按宠物、地图、任务、物品和天关关数查资料。`/quests/fire` 提供任务清单，勾选进度只保存在当前浏览器。`/maps/` 区分地图坐标、历史防御参考与玩家实测。火任务的逐步摘要维护在 `docs/.vitepress/data/fire-checklist.ts`，原攻略仍由提取脚本生成。

## 数据管线

| 数据 | 事实源 | 更新方式 |
| --- | --- | --- |
| 物品条目 | 游戏客户端 `ini/ItemNote.ini`（GBK） | `pnpm extract:items` 重建 `docs/.vitepress/data/items.ts` |
| 帮助目录 | 客户端 `help/guide.js` | 手工维护 `docs/.vitepress/data/helpToc.ts` |
| 宠物规则 | 客户端 `help/help06/10.htm` | 手工维护 `docs/.vitepress/data/pets.ts` |
| 宠物图片 | `EXCEL文件/宠物图鉴.xlsx` 内嵌 310 图 | `python3 scripts/extract-pet-images.py` 重建 `assets/hl/pets/` + `data/pet-images.json` |

## 图片 OSS 管线

游戏实体图存阿里云 OSS（bucket `cheny-chenyu` / 成都，与 jh-agileteam-doc 共用），专目录 `hl/`：

```
hl/pets/{metal,wood,water,fire,earth,shop,forge}   # 宠物图鉴（按五行等 sheet 分类）
hl/monsters  hl/items  hl/charts  hl/heroes  hl/misc
```

```bash
node scripts/upload-oss.mjs --source assets/hl/pets --target hl/pets --dry-run   # 预览
OSS_AK_ID=.. OSS_AK_SECRET=.. node scripts/upload-oss.mjs --source assets/hl/pets --target hl/pets
```

文件按内容 hash 命名（同图去重、URL 永久缓存），宠物名 → URL 在 `data/pet-images.json`；
本地 `assets/` 暂存目录不入仓库。

客户端目录 `/Users/cheny/play` 为只读参考，任何提取脚本不得写回原件。
生成的 `data/items.ts` 可重复构建，不要手工编辑。

## 内容边界

- 不放挂机脚本、辅助工具、私服相关内容（相关工程在 huanling-assistant，独立维护）
- 版权素材（宠物图、地图图）后续统一走 OSS 图床 + manifest 映射，不引用官方站热链
- 撤除政策与来源声明见 `docs/about.md`

## 目录结构

```
docs/
├── index.md                  # 首页（home 布局 + 组件区块）
├── guide/  pets/  items/     # 内容栏目
├── about.md                  # 版权与联系
└── .vitepress/
    ├── config.ts
    ├── data/                 # 单一数据源（items 生成 / pets、helpToc 手工）
    └── theme/                # 默认主题扩展 + 自定义组件与样式
scripts/extract-items.mjs     # GBK ini → items.ts 提取脚本
```
