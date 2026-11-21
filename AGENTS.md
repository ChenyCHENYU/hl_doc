# 幻灵宝典开发约定

本项目是独立的游戏资料文档站（VitePress），不适用工作区 PC Kit / wl-skills 路由。

- 改动后运行 `pnpm build` 确认通过；纯文档改动可用 `pnpm dev` 自查
- `/Users/cheny/play` 客户端目录只读，提取脚本只写本项目 `docs/.vitepress/data/` 与 `assets/`
- `data/items.ts`、`data/pet-images.json` 为生成物，分别通过 `pnpm extract:items`、`python3 scripts/extract-pet-images.py` 重建，禁止手工编辑
- 不收录挂机、辅助、私服内容；**唯一例外：`/museum/` 历史陈列馆**——仅以史料视角介绍 32 位时代工具生态（宠爱精灵/欢乐幻灵/A+/小精灵等），不提供下载、不含操作指引；其中涉及的账号信息等隐私文件任何情况下不得读取或入库
- 版权素材走本地归档 + OSS，不热链官方站

## 图片资产与 OSS

- 站点 UI 图放 `docs/public/`；游戏实体图一律走 OSS（bucket `cheny-chenyu` / 成都区域，与 jh-agileteam-doc 同一 bucket）
- OSS 专目录 `hl/`：`pets/{metal,wood,water,fire,earth,shop,forge}`、`monsters/`、`items/`、`charts/`、`gallery/`、`heroes/`、`misc/`
- 文件按内容 hash 命名（去重、可永久缓存），实体名 → URL 关系记录在 `data/*.json` 映射表
- 本地暂存 `assets/`（已 gitignore，不入仓库）；上传命令：
  `OSS_AK_ID=xx OSS_AK_SECRET=xx node scripts/upload-oss.mjs --source assets/hl/pets --target hl/pets`
  先 `--dry-run` 预览；上传是写操作，执行前与用户确认
- OSS 图片 URL 引用失败时站点自动降级为占位提示，不留死图

## 生成物清单（禁止手工编辑，脚本重建）

| 数据/页面 | 脚本 |
| --- | --- |
| `data/items.ts` | `pnpm extract:items` |
| `data/pet-images.json` + `assets/hl/pets/` | `python3 scripts/extract-pet-images.py`（GIF 自动转首帧 PNG） |
| `data/pet-codex.json`、`data/pet-prices.json` | `python3 scripts/extract-pet-codex.py` |
| `data/pet-images-2026.json` + codex 补图/立绘字段 | `python3 scripts/extract-docx-pet-images.py`（须在 extract-pet-codex.py 之后） |
| `docs/guide/topics/`、`cards/`、`data/help-*.json` | `python3 scripts/extract-help.py` |
| `docs/guide/library/`、`data/library*.json` | `python3 scripts/extract-baodian-exe.py` |
| `docs/advanced/*` | `python3 scripts/extract-advanced-docs.py` |
| `docs/quests/*` | `python3 scripts/extract-quest-guides.py` |
| `data/tower-defense.json`、`data/pet-stats-2026.json` | `python3 scripts/extract-optimize-res.py` |
| `docs/guide/library/bd-*.md` + library.json 合并 | `python3 scripts/extract-mission-baodian.py`（须在 extract-baodian-exe.py 之后运行） |
| `assets/hl/{charts,gallery}/`、`data/{gallery,resource-catalog}.json` | `python3 scripts/extract-resource-gallery.py` |

## 评论区（CommentBox）

- `docs/.vitepress/theme/components/CommentBox.vue`，经 Layout.vue 的 `#doc-after` 槽挂在文章类路由底部（文库/专题/任务/满属性/陈列馆；列表与首页不挂，正则见 Layout 内 COMMENT_ROUTES）
- 当前为**本地试用模式**：localStorage 按路径存储；游客昵称必填，QQ 号选填即得 QQ 头像直链（q1.qlogo.cn，无需授权）
- 正式接入：站点域名备案后 ① 在 `save()`/`onMounted` 处替换为 Waline 或 Twikoo API（serverURL 配置化）；② QQ 授权登录按钮去掉 disabled，接 QQ 互联回调
