#!/usr/bin/env python3
"""任务攻略板块：优化资源 + 7大宝典 目录下的 txt 攻略 -> docs/quests/*.md"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = Path("/Users/cheny/play/▲幻灵游侠优化资源▲/▲幻灵游侠优化资源▲")
BAODIAN = RES / "幻灵7大宝典"
OUT = ROOT / "docs" / "quests"
OUT.mkdir(parents=True, exist_ok=True)

GUIDES = [
    (BAODIAN / "水任务简易步骤.txt", "水属性任务（简易步骤）", "water"),
    (BAODIAN / "火属性任务步骤.txt", "火属性任务（步骤）", "fire"),
    (BAODIAN / "全部飞升简易攻略.txt", "全部飞升简易攻略", "ascend"),
    (RES / "手机玩幻灵的方法及回归的切入点.txt", "手机玩幻灵与回归指引", "return"),
    (RES / "2025【新宠终极规则】.txt", "2025 新宠终极规则", "rules2025"),
    (RES / "进化幻化公式及装备介绍.txt", "进化幻化公式与装备介绍", "formula"),
]



TURN_RE = re.compile(r"===\s*(\d+)转飞升攻略\s*===")
ROUTE_RE = re.compile(r"^([^，。；！？：:]{2,16})[：:]$")
SECTION_RE = re.compile(r"===\s*(.+?)\s*===")
BIGTITLE_RE = re.compile(r"^[■□]+\s*(.+)$")
BRANCH_RE = re.compile(r"^(\d)：(.+?)（(.+?)）$")
CAMP_RE = re.compile(r"^(仙道|魔道)$")
CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩"


def ascend_md(text: str) -> str:
    """全部飞升攻略 -> 状态机结构化 md（分节/阵营/支线卡/门槛/步骤/警示）"""
    out: list[str] = []
    nav: list[str] = []
    sec = 0
    steps: list[str] = []
    warn: list[str] = []
    mode = None  # None | 'quest' | 'warn'

    def flush_steps():
        nonlocal steps
        if steps:
            out.extend(f"{i}. {t}" for i, t in enumerate(steps, 1))
            out.append("")
            steps = []

    def flush_warn():
        nonlocal warn
        if warn:
            out.append("::: warning 注意事项")
            out.extend(f"- {t}" for t in warn)
            out.append(":::")
            out.append("")
            warn = []

    def add_sec(title: str, anchor: str, label: str = None):
        nonlocal sec
        sec += 1
        out.append(f"## {title} {{#{anchor}}}")
        out.append("")
        nav.append(f'<a href="#{anchor}">{label or title}</a>')

    for raw in text.split("\n"):
        t = raw.strip()
        lead_sp = raw[:1] in (" ", "\u3000")
        if not t or set(t) <= {"=", " ", "■", "□"}:
            if set(t) <= {"=", " "} and t.count("=") >= 6:
                continue
            if not t:
                flush_steps()
                flush_warn()
                mode = None if mode != "quest" else mode
                continue
        m = SECTION_RE.search(t)
        if t.count("=") >= 6 and m and re.search(r"[^\s=]", m.group(1)):
            flush_steps(); flush_warn(); mode = None
            name = m.group(1)
            if TURN_RE.search(t):
                n = TURN_RE.search(t).group(1)
                add_sec(f"{n}转 · 飞升攻略", f"turn-{n}", f"{n}转")
            else:
                add_sec(name, f"sec-{sec}")
            continue
        mb = BIGTITLE_RE.match(t)
        if mb:
            flush_steps(); flush_warn(); mode = None
            add_sec(mb.group(1), f"sec-{sec}")
            continue
        if CAMP_RE.match(t):
            flush_steps(); flush_warn(); mode = None
            out.append(f"### {t}五职")
            out.append("")
            continue
        if t[0] in CIRCLED:
            flush_steps()
            out.append(f"- **{t}**")
            continue
        mq = BRANCH_RE.match(t)
        if mq:
            flush_steps(); flush_warn()
            out.append(f"### {mq.group(2)} · {mq.group(3)}")
            out.append("")
            mode = "quest"
            continue
        if re.match(r"^注意事项", t):
            flush_steps()
            mode = "warn"
            continue
        if mode == "warn" and re.match(r"^[一二三四五六七八九十]、", t):
            warn.append(t)
            continue
        if mode == "warn" and not re.match(r"^[一二三四五六七八九十]、", t):
            flush_warn()
            mode = None
        if re.match(r"^(PS|ps|友情提醒)", t):
            flush_steps()
            out.append("::: info 玩家提醒")
            out.append(t)
            out.append(":::")
            out.append("")
            continue
        if mode == "quest":
            if lead_sp and steps:
                steps[-1] += t
                continue
            if t.startswith("如果"):
                out.append(f"**门槛**：{asc_line(t)}")
                out.append("")
                continue
            steps.append(asc_line(t))
            continue
        # 路线行（X飞Y：）
        rm = ROUTE_RE.match(t)
        if rm and ("飞" in t or "条件" in t):
            flush_steps()
            out.append(f"### {rm.group(1)}")
            out.append("")
            continue
        out.append(asc_line(t))
        out.append("")
    flush_steps()
    flush_warn()
    nav_html = '<p class="asc-nav">跳转：' + " ".join(nav) + "</p>"
    body = "\n".join(out)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return nav_html + "\n\n" + body


def asc_line(ln: str) -> str:
    ln = re.sub(r"(\d{2,4}\s*级)", r"**\1**", ln)
    ln = re.sub(r"(忠诚\s*100)", r"**\1**", ln)
    ln = re.sub(r"(满血满内|内力和血全满)", r"**\1**", ln)
    return ln


def enrich(md: str) -> str:
    """长文页面文字精修：PS/注意行归入提示容器，关键数值加粗。"""
    out = []
    tips = []
    in_code = False

    def flush():
        if tips:
            out.append("::: info 玩家提示")
            out.extend(tips)
            out.append(":::")
            tips.clear()

    for ln in md.split("\n"):
        if ln.startswith("```"):
            in_code = not in_code
        if not in_code and re.match(r"^(PS|ps[:：]|注[:：]|提示[:：]|注意)", ln.strip()):
            tips.append(ln.strip())
            continue
        flush()
        if in_code or ln.startswith(("#", "|", "<", ">", "**", "[", ":::", "-", "1.", "2.", "3.")):
            out.append(ln)
            continue
        ln = re.sub(r"(\d{2,4}\s*级)", r"**\1**", ln)
        ln = re.sub(r"(忠诚\s*100)", r"**\1**", ln)
        ln = re.sub(r"((?:水|火|金|木|土)行令\s?\d{0,2})", r"**\1**", ln)
        ln = re.sub(r"(\d{3,6}\s*两)", r"**\1**", ln)
        out.append(ln)
    flush()
    return "\n".join(out)


def to_md(text: str) -> str:
    lines = []
    for raw in text.split("\n"):
        ln = raw.rstrip()
        if not ln.strip():
            lines.append("")
            continue
        if re.match(r"^(一|二|三|四|五|六|七|八|九|十)[、.．]", ln.strip()):
            lines.append(f"## {ln.strip()}")
        elif re.fullmatch(r"[^：]{2,14}[：:]", ln.strip()):
            lines.append(f"### {ln.strip().rstrip('：:')}")
        elif re.match(r"^\d{1,2}[、.．)）]\s*", ln.strip()) and len(ln.strip()) <= 30:
            lines.append(f"### {ln.strip()}")
        else:
            lines.append(ln.strip())
    body = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    return body


STEP_RE = re.compile(r"^(\d{1,2})[.、)）]\s*")
# 术语行：短、无标点顿逗、以冒号结尾（如「1级乒乓鱼：」「超强毒药：」）
NAME_LINE = re.compile(r"^[^：:。，,、；！？\[\]()（）]{1,20}[：:]$")


def parse_flow(text: str) -> dict:
    """任务 txt -> {lead, prep:[{term,text}], steps:[{n,text,note}]}"""
    lines = [ln.rstrip() for ln in text.split("\n")]
    # 找到第一步的位置
    first_step = None
    for i, ln in enumerate(lines):
        if STEP_RE.match(ln.strip()) and int(STEP_RE.match(ln.strip()).group(1)) <= 2:
            first_step = i
            break
    head = lines[: first_step or len(lines)]
    tail = lines[first_step:] if first_step is not None else []

    # 准备区：短名行开启一个块
    lead, prep = [], []
    cur = None
    for ln in head:
        t = ln.strip()
        if not t or set(t) <= {"/"}:
            if cur:
                prep.append(cur)
                cur = None
            continue
        if NAME_LINE.match(t) and not re.search(r"需要|如下", t):
            if cur:
                prep.append(cur)
            cur = {"term": t.rstrip("：:"), "text": ""}
        elif cur:
            cur["text"] += t
        else:
            lead.append(t)
    if cur:
        prep.append(cur)

    # 步骤区：编号行开新步，PS/注 行并入当前步
    steps = []
    for ln in tail:
        t = ln.strip()
        if not t:
            continue
        m = STEP_RE.match(t)
        if m:
            steps.append({"n": int(m.group(1)), "text": t[m.end():], "note": ""})
        elif t.startswith(("PS", "ps", "注", "提示")) and steps:
            steps[-1]["note"] += t
        elif steps:
            steps[-1]["text"] += t
    return {
        "lead": " ".join(lead),
        "prep": [p for p in prep if p["text"] or p["term"]],
        "steps": steps,
    }


flows = {}
for src, title, slug in GUIDES:
    if not src.exists():
        continue
    text = src.read_bytes().decode("gbk", "replace")
    extra = ""
    if slug == "ascend":
        extra = '\n> **现行服勘误**：凡人飞散仙的出征宠物要求已更新为 **301 级以上苦行龟**（本文 120 级为旧版数据）；结构化最新版见 [从 0 到五转 · 仙魔飞升全指南](/quests/ascension)。\n'
    if slug == "fire":
        extra = '\n<AdvChart img="/hl-assets/hl/charts/fire-quest.jpg" title="火属性任务流程图" />\n'
    body_md = to_md(text)
    if slug == "ascend":
        body_md = ascend_md(text)
    if slug in ("water", "fire"):
        flows[slug] = {"title": title, **parse_flow(text)}
        component = '<FireQuestGuide />' if slug == "fire" else f'<QuestFlow flow="{slug}" />'
        source = "> 来源：《▲幻灵游侠优化资源▲》玩家资料包，原文GBK文本整理。\n\n"
        opening = "" if slug == "fire" else f'<TopicHeader cat="任务攻略" src="{src.name}" />\n\n' + source
        md = (
            f"---\ntitle: {title} - 幻灵宝典任务攻略\naside: false\n---\n\n"
            f"# {'火属性任务' if slug == 'fire' else title}\n\n"
            + opening
            + f"{component}\n"
            + extra
            + "\n<details>\n<summary>原文参考（纯文本）</summary>\n\n"
            + (source if slug == "fire" else "")
            + body_md
            + "\n</details>\n"
            + f'\n<TopicRelated cat="任务攻略" topic="{title}" />\n'
        )
    else:
        aside = "\naside: false" if slug in ("return", "rules2025") else ""
        md = (
            f"---\ntitle: {title} - 幻灵宝典任务攻略{aside}\n---\n\n"
            f"# {title}\n\n"
            f'<TopicHeader cat="任务攻略" src="{src.name}" />\n\n'
            f"> 来源：《▲幻灵游侠优化资源▲》玩家资料包，原文GBK文本整理。\n\n"
            + (body_md if slug == "ascend" else enrich(body_md))
            + extra
            + f'\n<TopicRelated cat="任务攻略" topic="{title}" />\n' 
        )
    (OUT / f"{slug}.md").write_text(md, "utf-8")
    print(f"{slug}: {len(text)} chars")

if flows:
    (ROOT / "docs" / ".vitepress" / "data" / "quest-flows.json").write_text(
        json.dumps(flows, ensure_ascii=False, indent=1), "utf-8"
    )
    print("quest-flows.json:", {k: (len(v["prep"]), len(v["steps"])) for k, v in flows.items()})

index = """---
title: 任务攻略
aside: false
---

# 任务攻略

先选你要做的任务。飞升条件看新版指南，旧版攻略保留原文供对照。

<div class="adv-grid">
  <a href="/quests/fire" class="adv-card"><span class="adv-icon">火</span><div><b>火属性任务</b><p>备料、限时事项、19 条火行令路线。</p></div></a>
  <a href="/quests/water" class="adv-card"><span class="adv-icon">水</span><div><b>水属性任务</b><p>水行令路线、苦行龟、毒药与兽玉。</p></div></a>
  <a href="/quests/ascension" class="adv-card"><span class="adv-icon">飞</span><div><b>仙魔飞升全指南</b><p>按称号查下一阶的人物、出征宠和药品条件。</p></div></a>
  <a href="/quests/rules2025" class="adv-card"><span class="adv-icon">规</span><div><b>2025 新宠终极规则</b><p>最新版宠物终极规则说明。</p></div></a>
  <a href="/quests/formula" class="adv-card"><span class="adv-icon">式</span><div><b>进化幻化公式与装备介绍</b><p>进化幻化核心公式与装备体系介绍。</p></div></a>
  <a href="/quests/return" class="adv-card"><span class="adv-icon">归</span><div><b>手机玩幻灵与回归指引</b><p>移动端游玩方案与老玩家回归切入点。</p></div></a>
</div>

[旧版飞升攻略与勘误](/quests/ascend)
"""
(OUT / "index.md").write_text(index, "utf-8")
print("quests index done")
