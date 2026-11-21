#!/usr/bin/env python3
"""游戏内宝典 77 页（help/*.htm，GBK）→ docs/guide/topics/helpNN.md
并生成 data/help-sidebar.json 供 config.ts 组装侧边栏。

分类与专题映射来自 help/guide.js；未在导航出现的页码仍提取，归入「更多条目」。
"""

import json
import re
import subprocess
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HELP = Path("/Users/cheny/play/幻灵游侠2.5（快速端）/幻灵游侠2.5（快速端）/help")
OUT = ROOT / "docs" / "guide" / "topics"
SIDEBAR_OUT = ROOT / "docs" / ".vitepress" / "data" / "help-sidebar.json"

CATEGORIES = [
    ("人物相关", [("创建", 29), ("属性", 43), ("装备", 42), ("兵解", 4)]),
    ("宠物相关", [("综述", 6), ("属性", 13), ("进化", 10), ("幻化", 28), ("技能", 9), ("摆摊", 7), ("斗宠", 21)]),
    ("战斗相关", [("回合战斗", 53), ("即时战斗", 57), ("自创武功", 47), ("修练武功", 46), ("捕捉宠物", 55)]),
    ("帮派相关", [("创建帮派", 15), ("帮派功能", 2), ("设立总坛", 61), ("帮派传送", 62)]),
    ("其他帮助", [("锻造", 23), ("婚姻", 30), ("建筑", 31), ("界面", 60), ("银行", 18), ("交易", 33), ("赌场", 22)]),
]

# 已被站内结构化页面取代、不再单独生成的专题：
#   help19 称号 → /guide/titles（称号阶梯与飞升路线）
SUPERSEDED = {19}

# 侧栏分组显示名（与卡片页 cat 解耦，让导航语义更直白）
SIDEBAR_LABEL = {
    "人物相关": "人物与称号",
    "宠物相关": "宠物系统",
    "战斗相关": "战斗与武功",
    "帮派相关": "帮派",
    "其他帮助": "日常玩法",
}

# 「更多条目」按标题关键词归入更贴切的分组（顺序即优先级）
EXTRA_RULES = [
    ("新手入门", ["新手", "入门", "创建", "游戏帮助", "塑造", "人的特点"]),
    ("宠物专题", ["宠物", "养宠", "幻化", "勋章"]),
    ("界面与操作", ["面板", "命令", "快捷键", "指令", "动作", "交互", "按键", "环境", "左下", "保护锁"]),
    ("玩法与世界", ["世界", "建筑", "经济", "社会", "安家", "房屋", "劫富", "投胎", "五行", "乾坤", "武功传授", "队伍", "聊天", "黑名单", "服务器", "驿站", "阵型", "领奖"]),
]


def extra_group(title: str) -> str:
    for group, kws in EXTRA_RULES:
        if any(kw in title for kw in kws):
            return group
    return "界面与操作"

KNOWN = {n for _, topics in CATEGORIES for _, n in topics}


class TextExtract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts: list[tuple[str, str]] = []
        self._buf: list[str] = []
        self._skip = 0
        self._in_title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        if tag == "title":
            self._in_title = True
        if tag in ("p", "div", "tr", "li", "br", "table", "h1", "h2", "h3", "h4"):
            self._flush()
        if tag in ("td", "th"):
            self._flush()

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
        if tag == "title":
            self._in_title = False
            self.title = "".join(self._buf).strip()
            self._buf = []
        if tag in ("p", "div", "tr", "li", "table", "h1", "h2", "h3", "h4", "td", "th", "body", "html"):
            self._flush()

    def handle_data(self, data):
        if self._skip:
            return
        if self._in_title:
            self._buf.append(data)
            return
        self._buf.append(data)

    def _flush(self):
        text = re.sub(r"[ \t\u3000]+", " ", "".join(self._buf)).strip()
        self._buf = []
        if text:
            self.parts.append(text)

    def result(self):
        self._flush()
        return [t for t in self.parts if t not in ("返回顶部", ".", "　", "返回")]


def slug_link(n: int) -> str:
    return f"/guide/topics/help{n:02d}"


SHORT_MAX = 16


def analyze(body: list[str]):
    segs = [s for s in body if s not in ("宠物相关", "人物相关", "战斗相关", "帮派相关", "其他帮助")]
    intro: list[str] = []
    sections: list[dict] = []
    tips: list[str] = []
    cur = {"title": None, "terms": [], "paras": []}
    sections.append(cur)
    last_term = None
    intro_done = False
    i = 0
    n = len(segs)
    while i < n:
        seg = segs[i]
        m = re.match(r"^([^：，。]{2,12})[：:](.{1,200})$", seg)
        sec_m = re.match(r"^([一二三四五六七八九十]．.{2,14})[：:]?$", seg)
        if re.match(r"^(提示|注意|小提示|心得)[：:]", seg) or re.match(r"^(p\.s\.|P\.S\.|ps)\b", seg, re.I):
            tips.append(seg)
            last_term = None
            i += 1
            continue
        if sec_m:
            cur = {"title": sec_m.group(1), "terms": [], "paras": []}
            sections.append(cur)
            intro_done = True
            last_term = None
            i += 1
            continue
        if m:
            cur["terms"].append({"term": m.group(1), "def": m.group(2)})
            last_term = cur["terms"][-1]
            intro_done = True
            i += 1
            continue
        if len(seg) <= 12 and seg.endswith("：") and i + 1 < n and len(segs[i + 1]) >= 4:
            nxt = segs[i + 1]
            if not nxt.endswith("：") and len(nxt) <= 200:
                cur["terms"].append({"term": seg.rstrip("："), "def": nxt})
                last_term = cur["terms"][-1]
                intro_done = True
                i += 2
                continue
        if last_term is not None and len(seg) <= 60 and not seg.endswith("："):
            last_term["def"] += seg
            i += 1
            continue
        if re.fullmatch(r"[\u4e00-\u9fff]{1,4}|\d{1,3}层?", seg) and i + 2 < n and re.fullmatch(r"[\u4e00-\u9fff]{1,4}", segs[i + 1]):
            run = [seg]
            j = i + 1
            while j < n and re.fullmatch(r"[\u4e00-\u9fff]{1,4}|\d{1,3}层?", segs[j]):
                run.append(segs[j])
                j += 1
            if len(run) >= 3:
                (intro if not intro_done and len(intro) < 2 else cur["paras"]).append(" · ".join(run))
                i = j
                continue
        last_term = None
        if not intro_done and len(intro) < 2:
            intro.append(seg)
        else:
            cur["paras"].append(seg)
            intro_done = True
        i += 1
    flat_terms = [t for sc in sections for t in sc["terms"]]
    flat_paras = [q for sc in sections for q in sc["paras"]]
    return intro, sections, flat_terms, flat_paras, tips


def js_attr(s: str) -> str:
    return (
        s.replace("\r", "")
        .replace("\n", " ")
        .replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace('"', "&quot;")
    )


def render_body(body: list[str]) -> str:
    intro, sections, flat_terms, flat_paras, tips = analyze(body)
    out: list[str] = []

    def emit_pairs(pairs: list[dict]):
        if len(pairs) == 1:
            t = pairs[0]
            out.append(f"**{t['term']}**：{t['def']}")
            out.append("")
        elif pairs:
            items = ",".join(f"{{term:'{js_attr(t['term'])}',def:'{js_attr(t['def'])}'}}" for t in pairs)
            out.append(f'<TermDefs :items="[{items}]" />')
            out.append("")

    for seg in intro:
        if len(seg) <= 14 and seg.endswith("："):
            out.append(f"## {seg.rstrip('：')}")
            out.append("")
            continue
        out.append(seg)
        out.append("")

    for sc in sections:
        if sc["title"]:
            out.append(f"## {sc['title']}")
            out.append("")
        for k in range(0, len(sc["terms"]), 6):
            emit_pairs(sc["terms"][k : k + 6])
        for q in sc["paras"]:
            if len(q) <= 14 and q.endswith("："):
                out.append(f"## {q.rstrip('：')}")
                out.append("")
                continue
            if re.match(r"^\d{1,2}[.、．)）]", q):
                out.append(q)
                continue
            out.append(q)
            out.append("")

    for seg in tips:
        out.append("::: tip 玩家提示")
        out.append(seg)
        out.append(":::")
        out.append("")
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


OUT.mkdir(parents=True, exist_ok=True)
CARDS_OUT = ROOT / "docs" / "guide" / "cards"
CARDS_OUT.mkdir(parents=True, exist_ok=True)
for old in OUT.glob("help*.md"):
    old.unlink()
pages = {}
cards: dict[str, list] = {}
long_topics: dict[str, list] = {}
used = set()

for cat_name, topics in CATEGORIES:
    for topic, n in topics:
        src = HELP / f"help{n:02d}.htm"
        if not src.exists():
            continue
        parser = TextExtract()
        parser.feed(src.read_bytes().decode("gb18030", "replace").replace("\uFFFD", ""))
        body = parser.result()
        if n == 29:
            body = [
                ln
                for ln in body
                if not re.search(r"充值|注册新帐号|游戏登入界面|申请帐号|充值卡|官方网站申请", ln)
                and ln not in ("如何给帐号充值：", "如何获得游戏帐号：")
            ]
            body = [re.sub(r"2\.0版里有男女各8个人物可供大家选择。?", "", ln) for ln in body]
            body = [ln for ln in body if ln.strip()]
            body.insert(1, "现行服直接注册账号即可进入游戏（2.5 版），已无点卡充值流程。")
        used.add(n)
        intro, _sections, terms, plain, tips = analyze(body)
        if len(intro) + len(plain) + len(tips) <= SHORT_MAX:
            cards.setdefault(cat_name, []).append(
                {
                    "topic": topic,
                    "src": f"help{n:02d}.htm",
                    "intro": intro,
                    "terms": terms,
                    "plain": plain,
                    "tips": tips,
                    "sections": [
                        {"title": sc["title"], "terms": sc["terms"], "paras": sc["paras"]}
                        for sc in _sections
                        if sc["title"] or sc["terms"] or sc["paras"]
                    ],
                }
            )
            continue
        long_topics.setdefault(cat_name, []).append((topic, n))
        body_md_pre = render_body(body)
        head = (
            f"---\ntitle: {topic} - 幻灵宝典指南"
            + ("\naside: false" if sum(1 for ln in body_md_pre.split("\n") if ln.startswith(("## ", "### "))) < 2 else "")
            + f"\n---\n\n"
            f"# {topic}\n\n"
            f'<TopicHeader cat="{cat_name}" src="help{n:02d}.htm" />\n\n'
        )
        forge = ""
        if n == 23:
            # 锻造：概念部分（装备五行/生克环/流程/规则）由 ForgeGuide 组件可视化，正文从"三、"起
            forge = "<ForgeGuide />\n\n"
            try:
                i3 = next(i for i, ln in enumerate(body) if ln.startswith("三、"))
                body = body[:1] + body[i3:]
            except StopIteration:
                pass
        md = head + forge + render_body(body) + f'\n<TopicRelated cat="{cat_name}" topic="{topic}" />\n' 
        (OUT / f"help{n:02d}.md").write_text(md, "utf-8")
        pages[n] = {"title": topic, "cat": cat_name, "link": slug_link(n)}

extra = []
for src in sorted(HELP.glob("help*.htm")):
    m = re.match(r"help(\d+)\.htm", src.name)
    if not m or int(m.group(1)) in used:
        continue
    n = int(m.group(1))
    if n in SUPERSEDED:
        continue
    parser = TextExtract()
    parser.feed(src.read_bytes().decode("gb18030", "replace").replace("\uFFFD", ""))
    body = parser.result()
    title = body[0][:12] if body else f"help{n:02d}"
    group = extra_group(title)
    structured_md = render_body(body[1:]) if len(body) > 1 else ""
    n_heads = sum(1 for ln in structured_md.split("\n") if ln.startswith(("## ", "### ")))
    lines = [f"---\ntitle: {title} - 幻灵宝典指南"
             + ("\naside: false" if n_heads < 2 else "")
             + f"\n---\n\n# {title}\n"]
    lines.append(f'<TopicHeader cat="{group} · 游戏帮助" src="help{n:02d}.htm" />\n')
    lines.append(f"> 原文：help{n:02d}.htm（游戏内宝典，未在官方导航目录中），结构化整理保留原意。\n")
    if n == 23:
        # 锻造：概念部分（五行/装备/流程/生克规则）由 ForgeGuide 组件可视化呈现
        lines.append("<ForgeGuide />\n")
        try:
            i3 = next(i for i, ln in enumerate(body) if ln.startswith("三、"))
            body = body[:1] + body[i3:]
        except StopIteration:
            pass
    # 与长专题同款结构化渲染（小节/词条/要点/提示）；正文去掉与 h1 重复的首行
    structured = structured_md
    if structured.strip():
        lines.append(structured)
    else:
        lines.extend(body[1:])
    md = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"
    (OUT / f"help{n:02d}.md").write_text(md, "utf-8")
    extra.append({"text": title, "cat": group, "link": slug_link(n)})

CARD_KEYS = {"人物相关": "gr", "宠物相关": "cw", "战斗相关": "xx", "帮派相关": "wh", "其他帮助": "gl"}
cards_data = []
for cat_name, items in cards.items():
    key = CARD_KEYS.get(cat_name, cat_name)
    cards_data.extend({"cat": cat_name, **it} for it in items)
    page = f"---\ntitle: {cat_name} - 幻灵宝典指南\naside: false\n---\n\n# {cat_name} · 专题宝典\n\n<p class=\"hc-page-intro\">按玩家问题组织的专题合集：上方页签切换专题，核心要点、操作步骤、词条解释一屏读完。</p>\n\n<HelpCards cat=\"{cat_name}\" />\n"
    (CARDS_OUT / f"{key}.md").write_text(page, "utf-8")

CARDS_JSON = ROOT / "docs" / ".vitepress" / "data" / "help-cards.json"
CARDS_JSON.write_text(json.dumps(cards_data, ensure_ascii=False, indent=1), "utf-8")

sidebar = []
for cat_name, topics in CATEGORIES:
    items = []
    if cat_name == "人物相关":
        items.append({"text": "称号阶梯与飞升路线", "link": "/guide/titles"})
    if cat_name == "战斗相关":
        items.append({"text": "自创武功 · 创招全流程", "link": "/guide/wugong"})
    if cat_name in cards:
        key = CARD_KEYS.get(cat_name, cat_name)
        items.append({"text": "专题宝典（页签阅读）", "link": f"/guide/cards/{key}"})
    for topic, n in topics:
        if n in pages:
            items.append({"text": topic, "link": slug_link(n)})
    # 宠物类额外条目并入宠物分组，避免分组碎片化
    if cat_name == "宠物相关":
        items.extend({"text": e["text"], "link": e["link"]} for e in extra if e["cat"] == "宠物专题")
    if items:
        sidebar.append({"text": SIDEBAR_LABEL.get(cat_name, cat_name), "collapsed": False, "items": items})

for group, _kws in EXTRA_RULES:
    if group == "宠物专题":
        continue  # 已并入宠物系统分组
    items = [{"text": e["text"], "link": e["link"]} for e in extra if e["cat"] == group]
    if items:
        sidebar.append({"text": group, "collapsed": True, "items": items})

SIDEBAR_OUT.write_text(json.dumps(sidebar, ensure_ascii=False, indent=1), "utf-8")
print(f"help: {len(pages)} topic pages, cards {sum(len(v) for v in cards.values())} in {list(cards)}")
print(f"sidebar groups: {[g['text'] for g in sidebar]}")
