# 幻灵宝典 · 页面清单（交接用）

> 生成时间：2026-11-17 · 共 24 类页面路由 · 数据管线 9 条（scripts/extract-*.py|js）· 构建命令 pnpm build · 本地服务 :8877（常驻）

| 路由 | 页面 | 数据来源 | 模板/组件 | 状态 | 已知问题/待优化 |
| --- | --- | --- | --- | --- | --- |
| `/` | 首页（叙事式） | codex/library/tower/stats2026/gallery 数据汇聚 | home/index.vue + SCSS 4分册 | 已改版 | 英雄区背景仍是登录图压暗待换主视觉；明星宠物带无轮播；移动端首屏弱 |
| `/pets/` | 宠物图鉴总览 | pet-codex.json（323只，垃圾行已清洗） | PetCodex.vue（Tab+搜索+卡墙） | 已改版 | 卡片信息密度可再加（无元素背景色区分）；无虚拟滚动 |
| `/pets/{id} ×323` | 宠物详情页 | codex+stats2026+prices+2026立绘 join | PetDetail.vue（五维雷达+系谱上下文） | 已上线 | 仅竟光犬1只缺图；2026属性59条未结构化；出处未链地图文章 |
| `/pets/evolutions` | 进化系谱大全 | evolveNormal 推导（32链） | EvolutionExplorer.vue | 已上线 | 同系谱内节点无可点击详情提示 |
| `/pets/prices` | 重塑价格表 | pet-prices.json（290条） | PetPrices.vue（Tab+条形图） | 已上线 | 表内名字未链宠物详情页 |
| `/guide/` | 宝典总览 | helpToc（5类25专题） | GuideCategories.vue（分类色卡） | 已上线 | 仅列出25官方专题，49条目扩展页无入口（仅侧边栏） |
| `/guide/cards/{gr,cw,xx,wh,gl}` | 专题宝典 ×5页 | help-cards.json（24卡） | HelpCards.vue（页签式一屏阅读：步骤+要点+词条+警示，无弹窗） | 已改版 | 吸顶页签条；底部上/下一篇翻页 |
| `/guide/topics/helpNN ×3+49` | 长专题+扩展帮助 | 客户端 help/*.htm | TopicHeader+TermDefs+tip/warning | 已上线 | help19称号已下线（并入/guide/titles）；更多条目已按 新手入门/界面与操作/玩法与世界 归组 |
| `/guide/library/` | 玩家文库总览 | library.json（483篇=玩家宝典139+Mission宝典344） | LibraryList.vue（分类色条+Tab） | 已上线 | 卡片无摘要（仅段数） |
| `/guide/library/{lib,bd}-NNN ×483` | 文库文章 | 宝典exe解压 + 六份Mission.txt宝典条目化 | 阅读模式（进度条+上下一篇+互链+表格/步骤转换） | 已上线 | bd-*为宝典合集条目（宠物自动互链）；综合其他待人工重分类 |
| `/items/` | 物品大全 | ItemNote.ini（343条） | ItemTable.vue（统计卡+搜索） | 已上线 | 无分类维度（类型/用途）；名字未链图鉴同名宠物装备 |
| `/monsters/` | 怪物手册·天关 | tower-defense.json（82关） | TowerTable.vue（看板+折线+表格） | 已上线 | 地图怪物分布/掉落查询仍为规划态 |
| `/quests/` | 任务攻略总览 | 6篇txt | adv-grid 卡片 | 简单 | 卡片样式与养成进阶总览同构（重复感）；无进度/完成度 |
| `/quests/ascension` | 飞升全指南（0-5转） | ascension.ts 人工整理 | AscensionGuide.vue（时间轴+仙魔分线） | 已上线 | 一转凡人801级条件未与新编宝典3.0规则(100级)交叉注 |
| `/quests/{water,fire,rules2025,formula,return}` | 任务攻略 ×5 | 优化资源txt | TopicHeader+结构化+AdvChart | 原文档平铺 | 除fire外无配图；water/return内容极短（<40行） |
| `/quests/ascend` | 历史版飞升攻略 | 旧txt（含勘误横幅） | 原文+###锚点 | 保留作史料 | 数据陈旧（120级等），仅靠横幅提醒 |
| `/advanced/` | 养成进阶总览 | 5入口 | adv-grid 卡片 | 简单 | 同 quests 总览同构；无内容量统计 |
| `/advanced/manxing-{jianyu,yunhu,ad}` | 满属性三部曲 | doc/docx 转文本 | TopicHeader+正文 | 图位待接 | 云狐20图/AD21图未提取（图位标记占位）；剑雨理论为纯文本 |
| `/advanced/charts` | 玩法图表 | 7张（OSS staging） | AdvChart（开发态本地图） | 待OSS | 生产环境图为占位符（OSS未上传） |
| `/advanced/tips` | 小技巧 | 竖排字符画txt | 代码块 | 已上线 | 仅1篇内容 |
| `/heroes/` | 幻灵英雄墙 | heroes.ts 占位 | HeroWall.vue（稀有度游戏卡） | 占位 | 无真实玩家数据；投稿流程文字化 |
| `/resources/` | 资源库+画廊 | resource-catalog.json + gallery.json | ResourcesPage.vue（编目表+灯箱） | 已上线 | 画廊无分类筛选/瀑布流；编目29条可再细化 |
| `/museum/` | 历史陈列馆（32位工具生态） | 优化资源包史料（手写整理） | MuseumHall.vue（时间轴+展品卡+纸面证据） | 已上线 | 仅史料不提供下载；3张说明图待OSS |
| `/about/` | 关于本站 | 手写 | 统计卡+来源表 | 已上线 | 联系方式占位邮箱 |
| `/guide/titles` | 称号阶梯与飞升路线 | titles.ts（凡人8阶+5转双线+10神尊） | TitleLadder.vue（阶梯+双线+职业） | 已改版 | 投胎后称号未覆盖 |
| `/guide/wugong` | 自创武功专页 | help47/46 整理 | stepper+公式卡+图表 | 已上线 | 招式类型九宫未做 |

## 全局待办

1. **OSS 上传**（阻塞所有生产环境图片）：`OSS_AK_ID=.. OSS_AK_SECRET=.. node scripts/upload-oss.mjs --source assets/hl/pets --target hl/pets`（charts/gallery 同理，先 --dry-run）
2. P2 交互：Ctrl+K 命令面板、画廊/图表统一灯箱、移动端手风琴
3. sitemap hostname 占位 hl.example.com 待部署域名
4. 2026 属性 59 条未结构化；文库综合其他 54 篇待重分类
5. 首页主视觉素材待用户提供（替换登录图背景）

## 数据事实源

| 数据 | 文件 | 重建 |
| --- | --- | --- |
| 物品 343 | data/items.ts | pnpm extract:items |
| 宠物 333 + 图310 | data/pet-codex.json / pet-images.json | python3 scripts/extract-pet-{images,codex}.py |
| 2026属性 173 | data/pet-stats-2026.json | python3 scripts/extract-optimize-res.py |
| 天关 82 | data/tower-defense.json | 同上 |
| 帮助 78页+卡片 | docs/guide/{topics,cards}/ + data/help-*.json | python3 scripts/extract-help.py |
| 文库 483（139 玩家宝典 + 344 Mission宝典） | docs/guide/library/ + data/library*.json | python3 scripts/extract-baodian-exe.py && python3 scripts/extract-mission-baodian.py（顺序执行） |
| 任务/养成 | docs/quests/ docs/advanced/ | extract-quest-guides.py / extract-advanced-docs.py |
| 编目+画廊 | data/{resource-catalog,gallery}.json | extract-resource-gallery.py |