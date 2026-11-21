#!/usr/bin/env python3
"""提取 优化资源 里的新数据：
1. 天关防御参数.xlsx(3 sheets) -> data/tower-defense.json
2. 【2026五系图鉴大全】5 个 docx 的 w:tbl -> data/pet-stats-2026.json
"""

import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = Path("/Users/cheny/play/▲幻灵游侠优化资源▲/▲幻灵游侠优化资源▲")
DATA = ROOT / "docs" / ".vitepress" / "data"

M = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def load_xlsx_sheet(z, sheet_xml, shared):
    rows = []
    for row in ET.fromstring(z.read(sheet_xml)).iter(f"{{{M}}}row"):
        cells = {}
        for c in row.iter(f"{{{M}}}c"):
            ref = re.match(r"([A-Z]+)", c.get("r") or "").group(1)
            v = c.find(f"{{{M}}}v")
            cells[ref] = shared[int(v.text)] if (v is not None and c.get("t") == "s" and v.text) else (v.text if v is not None else "")
        rows.append(cells)
    return rows


# ---- 1. 天关防御参数 ----
z = zipfile.ZipFile(RES / "天关防御参数.xlsx")
shared = []
if "xl/sharedStrings.xml" in z.namelist():
    for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(f"{{{M}}}si"):
        shared.append("".join(t.text or "" for t in si.iter(f"{{{M}}}t")))

tower = []
for sheet_xml in sorted(n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml", n)):
    rows = load_xlsx_sheet(z, sheet_xml, shared)
    if not rows or not any(rows[0].values()):
        continue
    header = {v: k for k, v in rows[0].items() if v}
    col_floor = next((k for k, v in rows[0].items() if "关数" in (v or "")), None)
    if not col_floor:
        continue
    mode = "兄弟" if any("兄弟" in (r.get(col_floor) or "") for r in rows[1:20]) else ("夫妻" if any("夫妻" in (r.get(col_floor) or "") for r in rows[1:20]) else "普通")
    for r in rows[1:]:
        if not (r.get(col_floor) or "").strip():
            continue
        entry = {"mode": mode}
        for key, col in (("floor", "关数"), ("level", "等级"), ("monster", "怪物"), ("element", "属性")):
            c = next((k for k, v in rows[0].items() if key != "x" and v and col in v), None)
            if c:
                entry[key] = r.get(c, "")
        for key, col in (
            ("maxAtk", "最大攻击"),
            ("defHuman", "人防"),
            ("defEarth", "土系"),
            ("defFire", "火系"),
            ("defWater", "水系"),
            ("defWood", "木系"),
            ("defMetal", "金系"),
            ("agi", "敏"),
        ):
            c = next((k for k, v in rows[0].items() if v and col in v), None)
            if c:
                entry[key] = r.get(c, "")
        tower.append(entry)

(DATA / "tower-defense.json").write_text(json.dumps(tower, ensure_ascii=False, indent=1), "utf-8")
print(f"tower-defense: {len(tower)} rows, modes={set(t['mode'] for t in tower)}")

# ---- 2. 2026 五系图鉴 docx（段落流结构）----
stats = []
ELEMENTS = {"金": "metal", "木": "wood", "水": "water", "火": "fire", "土": "earth"}
TYPE_WORDS = "攻击型|防御型|防血型|敏攻型|攻防型|防攻型|血攻型|血防型|敏防型"
ENTRY_RE = re.compile(
    rf"([一-龥]{{1,6}}[一-龥A-Za-z]?)\s*({TYPE_WORDS})\s*"
    r"([\d.]+\s*/\s*[\d.]+\s*/\s*[\d.]+\s*/\s*[\d.]+)\s*"
    r"([\d.]+)\s*([\d.]+)\s*"
    r"(\d+%\s*/\s*\d+%\s*/\s*\d+%)"
)
for docx in sorted((RES / "【2026五系图鉴大全】").glob("*.docx")):
    el_code = next((v for k, v in ELEMENTS.items() if k in docx.name), "misc")
    dz = zipfile.ZipFile(docx)
    doc = ET.fromstring(dz.read("word/document.xml"))
    parts = []
    for p in doc.iter(f"{{{W}}}p"):
        t = "".join(x.text or "" for x in p.iter(f"{{{W}}}t"))
        if t.strip():
            parts.append(t)
    text = "".join(parts)
    group = ""
    for m in ENTRY_RE.finditer(text):
        name, ptype, attrs, g3, ghp, dist = m.groups()
        if name in ("宠物名", "宠物名称"):
            continue
        atk = dfs = agi = hp = ""
        tail = ""
        am = re.match(r"^(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)\s*/\s*(.+)$", attrs)
        if am:
            atk, dfs, agi = am.group(1), am.group(2), am.group(3)
            tail = am.group(4).replace(" ", "")
            tm = re.match(r"^(\d{2})(\d\.\d)(\d(?:\.\d)?)", tail)
            if tm:
                hp, g3, ghp = tm.group(1), tm.group(2), tm.group(3)
            else:
                tm2 = re.match(r"^(\d{2})(\d\.\d?)$", tail)
                if tm2:
                    hp, g3 = tm2.group(1), tm2.group(2)
        parsed = bool(am and hp)
        section_idx = text.rfind("不可进化", 0, m.start())
        evolve_idx = text.rfind("可进化", 0, m.start())
        group = "不可进化" if section_idx > evolve_idx else "可进化"
        entry = {
            "name": name.strip(),
            "element": el_code,
            "group": group,
            "type": ptype,
            "attrs": re.sub(r"\s+", "", attrs),
            "dist": re.sub(r"\s+", "", dist),
        }
        if parsed:
            entry.update({"atk": atk, "def": dfs, "agi": agi, "hp": hp, "growth3": g3, "growthHp": ghp})
        else:
            entry.update({"growth3": g3, "growthHp": ghp})
        stats.append(entry)

(DATA / "pet-stats-2026.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1), "utf-8")
by_el = {}
for s in stats:
    by_el[s["element"]] = by_el.get(s["element"], 0) + 1
print(f"pet-stats-2026: {len(stats)} rows, {by_el}")
