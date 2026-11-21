#!/usr/bin/env python3
"""生成养成进阶板块：
1. 云狐/AD 满属性 docx -> docs/advanced/manxing-*.md（含图位标记）
2. 剑雨理论 .doc -> textutil 转 txt 再转 md
3. 小技巧 txt(GBK) -> docs/advanced/tips.md
4. 玩法图表 jpg 归档到 assets/hl/charts/ + 生成 charts.md
"""

import re
import subprocess
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES_ROOT = Path("/Users/cheny/play/▲幻灵游侠优化资源▲/▲幻灵游侠优化资源▲")
SRC = Path("/Users/cheny/play/EXCEL文件")
DGE = Path("/Users/cheny/play/东哥定制全套服务/东哥定制全套服务")
OUT = ROOT / "docs" / "advanced"
CHARTS = ROOT / "assets" / "hl" / "charts"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"



# ── 结构化后处理：小节 / 情况列表 / 公式行 / 概率数据表 / 数值加粗 ──
HEAD_RE = re.compile(r"^[^，。：:；=＋+\-×*/（）()\d\s]{2,10}[：:]?$")
CASE_RE = re.compile(r"^(第[一二三四五六七八九十]种情况|情况[一二三四五六七八九十])[：:]")
SUB_RE = re.compile(r"^[（(]\d[）)]")
PROB_RE = re.compile(r"^((?:全|[金木水火土])系)[：:]\s*(.+)$")


def bold_nums(t: str) -> str:
    # 乘号统一为 ×，避免与 markdown 加粗星号冲突
    t = re.sub(r"(?<=[\d）)\u4e00-\u9fff])\*(?=\d)", "×", t)
    t = re.sub(r"(\d{1,3}\.\d{1,2})", r"**\1**", t)
    t = re.sub(r"(\d{2,4}\s*级)", r"**\1**", t)
    t = re.sub(r"(?<![\d.*])((?:\d{1,2}[-－]){2}\d{1,2})(?![\d.])", r"**\1**", t)  # 三围 38-31-31
    t = re.sub(r"(?<![\d.*])(\d{4})(?![\d.%])", r"**\1**", t)  # 裸数值 3097
    t = re.sub(r"(\*1\.1[456])", r"**\1**", t)
    return t


def structureize(lines):
    out = []
    prob_start = None
    prob_rows = []
    for raw in lines:
        t = raw.rstrip()
        if not t:
            out.append("")
            continue
        if t.startswith(("> 图", "#", "---")):
            out.append(t)
            continue
        m = PROB_RE.match(t)
        if m:
            if prob_start is None:
                prob_start = len(out)
                out.append("@@PROB_TABLE@@")
            body = m.group(2)
            for pm in re.finditer(r"([\u4e00-\u9fff（）]{2,12}?)(\d{1,3}\.\d{1,2})", body):
                prob_rows.append((m.group(1), pm.group(1), pm.group(2)))
            rest = re.sub(r"[\u4e00-\u9fff（）]{2,12}?\d{1,3}\.\d{1,2}\s*", "", body).strip()
            if rest:
                prob_rows.append((m.group(1), rest, "—"))
            continue
        if CASE_RE.match(t):
            head, _, tail = t.partition("：")
            out.append(f"- **{head}**：{bold_nums(tail)}")
            continue
        if SUB_RE.match(t):
            out.append(f"- **{t}**")
            continue
        if "=" in t and len(t) <= 80 and not t.startswith("http"):
            out.append(f"`{t}`")
            out.append("")
            continue
        if HEAD_RE.match(t):
            out.append(f"## {t.rstrip('：:')}")
            out.append("")
            continue
        out.append(bold_nums(t))
        out.append("")
    if prob_start is not None and prob_rows:
        table = ["| 系 | 地点 | 出双概率 |", "| --- | --- | --- |"]
        table += [f"| {a} | {b} | {c} |" for a, b, c in prob_rows]
        out[prob_start] = "\n".join(table)
    body = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    return body.split("\n")


MANXING_DIR = ROOT / "assets" / "hl" / "manxing"


def docx_to_md(path: Path, title: str, out_name: str, key: str, author: str = ""):
    """docx -> md；word/media 按文档顺序落盘 assets/hl/manxing/{key}-NN.png，
    段落中的图以内联 md 图片接入（dev/preview 直读，生产走 OSS 同名路径）。"""
    import hashlib

    z = zipfile.ZipFile(path)
    MANXING_DIR.mkdir(parents=True, exist_ok=True)
    rels = {}
    PR = "http://schemas.openxmlformats.org/package/2006/relationships"
    R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    A = "http://schemas.openxmlformats.org/drawingml/2006/main"
    for r in ET.fromstring(z.read("word/_rels/document.xml.rels")).iter(f"{{{PR}}}Relationship"):
        rels[r.get("Id")] = r.get("Target")

    body = ET.fromstring(z.read("word/document.xml")).find(f"{{{W}}}body")
    lines = []
    img_seq = 0
    for el in body:
        tag = el.tag.split("}")[1]
        if tag == "p":
            blips = [b.get(f"{{{R}}}embed") for b in el.iter(f"{{{A}}}blip")]
            text = "".join(t.text or "" for t in el.iter(f"{{{W}}}t")).strip()
            if blips:
                for rid in blips:
                    target = rels.get(rid)
                    if not target or "media" not in target:
                        continue
                    img_seq += 1
                    media = "word/" + target.lstrip("/")
                    data = z.read(media)
                    ext = media.rsplit(".", 1)[-1].lower()
                    digest = hashlib.sha1(data).hexdigest()[:8]
                    name = f"{key}-{img_seq:02d}-{digest}.{ext}"
                    (MANXING_DIR / name).write_bytes(data)
                    lines.append(f'<AdvChart img="/hl-assets/hl/manxing/{name}" title="图 {img_seq} · {title} 配图" />')
                    lines.append("")
            if text:
                style = el.find(f"{{{W}}}pPr/{{{W}}}pStyle")
                if style is not None and "Heading" in (style.get(f"{{{W}}}val") or ""):
                    lines.append(f"## {text}")
                else:
                    lines.append(text)
                    lines.append("")
    lines = structureize(lines)
    content = f"---\ntitle: {title}\n---\n\n# {title}\n\n" + "\n".join(lines)
    content = re.sub(r"\n{3,}", "\n\n", content).strip() + "\n"
    if author:
        content += f"\n<AuthorCard author=\"{author}\" />\n"
    (OUT / out_name).write_text(content, "utf-8")
    return img_seq


def doc_to_md(path: Path, title: str, out_name: str, author: str = ""):
    r = subprocess.run(
        ["textutil", "-convert", "txt", "-stdout", str(path)],
        capture_output=True,
    )
    text = r.stdout.decode("utf-8", "ignore").strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = "\n".join(structureize(text.split("\n")))
    content = f"---\ntitle: {title}\n---\n\n# {title}\n\n{text}\n"
    if author:
        content += f"\n<AuthorCard author=\"{author}\" />\n"
    (OUT / out_name).write_text(content, "utf-8")
    return len(text)


def txt_to_md(path: Path, title: str, out_name: str):
    text = path.read_bytes().decode("gbk", "ignore").strip()
    raw_lines = [l for l in text.split("\n") if l.strip()]
    short_ratio = sum(1 for l in raw_lines if len(l.strip()) <= 4) / max(len(raw_lines), 1)
    if short_ratio > 0.5:
        body = "```\n" + text + "\n```"
    else:
        body = text
    content = f"---\ntitle: {title}\n---\n\n# {title}\n\n{body}\n"
    (OUT / out_name).write_text(content, "utf-8")


OUT.mkdir(parents=True, exist_ok=True)
CHARTS.mkdir(parents=True, exist_ok=True)

n1 = docx_to_md(SRC / "云狐满属性文字图片文稿.docx", "满属性实操：云狐", "manxing-yunhu.md", key="yunhu", author="hentian")
n2 = docx_to_md(SRC / "AD满属性文字图片文稿.docx", "满属性实操：AD（攻防宠）", "manxing-ad.md", key="ad", author="jianyu")
n3 = doc_to_md(SRC / "剑雨满属性理论基础 (4).doc", "满属性理论基础：剑雨", "manxing-jianyu.md", author="jianyu")
txt_to_md(SRC / "人或宠把名字竖起的方法(1).txt", "小技巧合集", "tips.md")

charts = [
    (DGE / "东哥编写-关于锻造相生相克及五行位置图.jpg", "forging-wuxing.jpg", "锻造相生相克及五行位置图"),
    (DGE / "各宠物进化次序及形态方法.jpg", "pet-evolution.jpg", "各宠物进化次序及形态方法"),
    (RES_ROOT / "宠物进化表2026.png", "pet-evolution-2026.jpg", "宠物进化表（2026 版）"),
    (RES_ROOT / "招系数排名.png", "zhao-coeff-rank.jpg", "武功招式系数排名"),
    (RES_ROOT / "开荒装备.png", "kaikuang-gear.jpg", "开荒装备指南"),
    (RES_ROOT / "乾坤五行炉.png", "qiankun-furnace.jpg", "乾坤五行炉（五行炼化）"),
    (RES_ROOT / "八卦炉.jpg", "bagua-furnace.jpg", "八卦炉"),
]
chart_lines = []
for src, name, title in charts:
    if src.exists():
        (CHARTS / name).write_bytes(src.read_bytes())
    chart_lines.append(f"## {title}\n\n<AdvChart img=\"/hl-assets/hl/charts/{name}\" title=\"{title}\" />\n")

(OUT / "charts.md").write_text(
    "---\ntitle: 玩法图表\n---\n\n# 玩法图表\n\n高分辨率大图已归档，正式环境经 OSS 图床（`hl/charts/`）分发。\n\n" + "\n".join(chart_lines) + "\n<AuthorCard author=\"dongge\" />\n",
    "utf-8",
)

index = """---
title: 养成进阶
---

# 养成进阶

面向进阶玩家的深度养成资料：满属性宠物打造、锻造五行、玩法图表与小技巧。

<div class="adv-grid">
  <a href="/advanced/manxing-jianyu" class="adv-card">
    <span class="adv-icon">理</span>
    <div><b>满属性理论基础 · 剑雨</b><p>三围比例、幻化固定、锻造调平的核心公式与思路。</p></div>
  </a>
  <a href="/advanced/manxing-yunhu" class="adv-card">
    <span class="adv-icon">狐</span>
    <div><b>满属性实操 · 云狐</b><p>1550 后锻造减属性、幻化固定三围全流程（含 %d 张配图位）。</p></div>
  </a>
  <a href="/advanced/manxing-ad" class="adv-card">
    <span class="adv-icon">炼</span>
    <div><b>满属性实操 · AD 攻防宠</b><p>攻防宠三围 38-31-31 路线、内带制作与减属性阈值（含 %d 张配图位）。</p></div>
  </a>
  <a href="/advanced/charts" class="adv-card">
    <span class="adv-icon">图</span>
    <div><b>玩法图表</b><p>锻造相生相克五行位置图、宠物进化次序及形态方法。</p></div>
  </a>
  <a href="/advanced/tips" class="adv-card">
    <span class="adv-icon">技</span>
    <div><b>小技巧合集</b><p>名字竖排等游戏内实用小技巧，持续补充。</p></div>
  </a>
</div>

> 满属性系列文稿来自玩家整理（云狐篇感谢玩家「恨天」提供素材），原文配图将随 OSS 图床上线逐步接入。
""" % (n1, n2)
(OUT / "index.md").write_text(index, "utf-8")
print(f"advanced: jianyu {n3} chars, yunhu {n1} imgs, ad {n2} imgs, charts {len(charts)}")
