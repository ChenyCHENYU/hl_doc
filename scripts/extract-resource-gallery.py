#!/usr/bin/env python3
"""优化资源 -> 站点资产：
1. 图表图片 -> assets/hl/charts/（养成进阶·玩法图表）
2. 高清壁纸 -> assets/hl/gallery/（资源库画廊）
3. 全目录编目 -> data/resource-catalog.json（资源库页渲染）
"""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = Path("/Users/cheny/play/▲幻灵游侠优化资源▲/▲幻灵游侠优化资源▲")
ASSETS = ROOT / "assets" / "hl"
DATA = ROOT / "docs" / ".vitepress" / "data"

CHARTS = [
    ("宠物进化表2026.png", "pet-evolution-2026.jpg", "宠物进化表（2026 版）"),
    ("招系数排名.png", "zhao-coeff-rank.jpg", "武功招式系数排名"),
    ("开荒装备.png", "kaikuang-gear.jpg", "开荒装备指南"),
    ("乾坤五行炉.png", "qiankun-furnace.jpg", "乾坤五行炉（五行炼化）"),
    ("八卦炉.jpg", "bagua-furnace.jpg", "八卦炉"),
    ("火任务.jpg", "fire-quest.jpg", "火属性任务流程图"),
]

gallery_files = []
GALLERY_SRC = RES / "幻灵高清壁纸"
gallery_out = ASSETS / "gallery"
gallery_out.mkdir(parents=True, exist_ok=True)
for f in sorted(GALLERY_SRC.iterdir()):
    if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
        target = f"{f.stem}-{hash(str(f.stat().st_mtime)) & 0xffff:x}{f.suffix.lower()}"
        shutil.copy2(f, gallery_out / target)
        gallery_files.append(
            {
                "file": f"hl/gallery/{target}",
                "title": f.stem,
            }
        )

charts_out = ASSETS / "charts"
charts_out.mkdir(parents=True, exist_ok=True)
charts_data = []
for src, dst, title in CHARTS:
    if (RES / src).exists():
        shutil.copy2(RES / src, charts_out / dst)
        charts_data.append({"img": f"/hl-assets/hl/charts/{dst}", "title": title})

(DATA / "gallery.json").write_text(json.dumps(gallery_files, ensure_ascii=False, indent=1), "utf-8")

CATALOG = [
    ("幻灵7大宝典/", "宝典合集", "已上线", "玩家文库 483 篇：玩家宝典.exe 139 + 六份 Mission.txt 宝典 344（extract-mission-baodian.py）"),
    ("【2026五系图鉴大全】/", "图鉴数据", "已上线", "173 只宠物标准属性，已接入宠物图鉴详情"),
    ("天关防御参数.xlsx", "数据表格", "已上线", "82 关防御参数表，怪物手册可筛选查询"),
    ("重塑宠物价格.xlsx", "数据表格", "已上线", "重塑价格表（与既有版本微差，修订时合并）"),
    ("宠物进化表2026.png", "图表", "已上线", "玩法图表页"),
    ("招系数排名.png", "图表", "已上线", "玩法图表页"),
    ("开荒装备.png", "图表", "已上线", "玩法图表页"),
    ("乾坤五行炉.jpg / 八卦炉.jpg", "图表", "已上线", "玩法图表页"),
    ("火任务.jpg", "图表", "已上线", "任务攻略·火属性任务"),
    ("水任务/全部飞升/新宠规则/公式/回归 6 篇 txt", "攻略文档", "已上线", "任务攻略栏目"),
    ("进化幻化公式及装备介绍.txt", "攻略文档", "已上线", "任务攻略栏目"),
    ("幻灵高清壁纸/", "壁纸画廊", "已上线", f"资源库画廊 {len(gallery_files)} 张"),
    ("好视力战斗地图（4）/", "游戏美化", "仅编目", "8 张战斗背景清晰化补丁（ini），不提供下载"),
    ("幻灵游侠界面皮肤/", "游戏美化", "仅编目", "界面皮肤资源（GUI 文件）"),
    ("原始战斗背景/", "游戏美化", "仅编目", "原始战斗背景配置"),
    ("绝版新宠补丁 / 绝版免动作宠怪补丁（1）（2）（3）", "游戏补丁", "仅编目", "绝版宠物/免动作外观补丁，不提供下载"),
    ("字体包/", "游戏美化", "仅编目", "227 个字体文件"),
    ("装备锻造脚本/", "辅助脚本", "不收录", "13 个锻造自动脚本（辅助类边界）"),
    ("▲自动练级▲/▲自动摆摊▲/▲五系练宠▲/▲自动吃书▲/▲自动逛街▲/▲五类极限/▲兵解药2.0", "辅助脚本", "不收录", "挂机/自动化脚本"),
    ("▲闯天关1-100(快速端).ini", "辅助脚本", "不收录", "闯天关自动脚本"),
    ("宠物成长计算器 / 装备纯点计算 / 4锻宠计算器（exe）", "工具", "仅编目", "本地计算器工具，站内记录用途"),
    ("快照版五系91宠全自动托管0.99 / 快速端1550斗宠版", "客户端", "不收录", "托管/快速端变体客户端"),
    ("▲超级.欢乐幻灵 / ▲宠爱精灵拖鞋终结版", "辅助工具", "史料收录", "见 /museum/ 历史陈列馆（仅史料，不提供下载）"),
    ("创建改色人物（纯色人物.exe）", "工具", "仅编目", "改色人物生成工具"),
    ("去神魔光（显存不够使用）", "游戏美化", "仅编目", "低配优化补丁"),
    ("虚拟机小精灵问题大全.txt / 小精灵辅助功能介绍.png / 业务介绍.png", "辅助文档", "史料收录", "见 /museum/ 历史陈列馆"),
    ("封IP的原因.png", "社区信息", "史料收录", "见 /museum/ 历史陈列馆"),
    ("四色排骨.png / 女角色.png", "画廊素材", "已上线", "画廊收录"),
    ("手机玩幻灵的方法及回归的切入点.txt", "攻略文档", "已上线", "任务攻略·回归指引"),
]

(DATA / "resource-catalog.json").write_text(
    json.dumps(
        [{"name": n, "type": t, "status": s, "note": note} for n, t, s, note in CATALOG],
        ensure_ascii=False,
        indent=1,
    ),
    "utf-8",
)

print(f"gallery: {len(gallery_files)} images -> {gallery_out}")
print(f"charts: {len(charts_data)} -> {charts_out}")
print(f"catalog: {len(CATALOG)} entries")
