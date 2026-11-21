#!/usr/bin/env python3
"""合并 宠物图鉴.xlsx + 重塑宠物价格.xlsx + 已提取图片映射 -> data/pet-codex.json。

输出条目:
  {id, name, sheet, element, type, evolveIllegal, evolveNormal, source, note,
   image: {file, ossKey, url} | null,
   price: {original, discount, special} | null}
"""

import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_PET = Path("/Users/cheny/play/EXCEL文件/宠物图鉴.xlsx")
SRC_PRICE = Path("/Users/cheny/play/EXCEL文件/重塑宠物价格.xlsx")
IMG_MAP = ROOT / "docs" / ".vitepress" / "data" / "pet-images.json"
OUT = ROOT / "docs" / ".vitepress" / "data" / "pet-codex.json"

M = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def col_of(ref):
    return re.match(r"([A-Z]+)", ref).group(1)


def load_sheet(path, wanted=None):
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(f"{{{M}}}si"):
            shared.append("".join(t.text or "" for t in si.iter(f"{{{M}}}t")))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    R = "http://schemas.openxmlformats.org/package/2006/relationships"
    rel_map = {r.get("Id"): r.get("Target") for r in rels.findall(f"{{{R}}}Relationship")}
    sheets = {}
    for sh in wb.iter(f"{{{M}}}sheet"):
        name = sh.get("name")
        if wanted and name not in wanted:
            continue
        target = rel_map[sh.get(f"{{http://schemas.openxmlformats.org/officeDocument/2006/relationships}}id")]
        target = target.lstrip("/")
        if not target.startswith("xl/"):
            target = "xl/" + target
        rows = {}
        for row in ET.fromstring(z.read(target)).iter(f"{{{M}}}row"):
            cells = {}
            for c in row.iter(f"{{{M}}}c"):
                v = c.find(f"{{{M}}}v")
                if v is None or v.text is None:
                    continue
                text = shared[int(v.text)] if c.get("t") == "s" else v.text
                text = (text or "").strip()
                if text:
                    cells[col_of(c.get("r"))] = text
            rows[int(row.get("r"))] = cells
        sheets[name] = rows
    return sheets


ELEMENTS = {
    "金属性宠物": "metal",
    "木属性宠物": "wood",
    "水属性宠物": "water",
    "火属性宠物": "fire",
    "土属性宠物": "earth",
    "新山宠店宠物": "shop",
    "任务物品锻造": "forge",
}

images = json.loads(IMG_MAP.read_text())
img_by_key = {}
for e in images:
    img_by_key.setdefault((e["sheet"], e["row"]), e)
    if not e["name"]:
        continue
    img_by_key.setdefault((e["sheet"], e["name"]), e)

prices = {}
price_rows = []
rows = load_sheet(SRC_PRICE)["幻兽价格"]
header = rows.get(1, {})
col_pname = next((c for c, h in header.items() if "名字" in h), None)
col_psys = next((c for c, h in header.items() if "系别" in h), None)
col_orig = next((c for c, h in header.items() if "原价" in h), None)
col_disc = next((c for c, h in header.items() if "折扣" in h), None)
col_spec = next((c for c, h in header.items() if "特惠" in h), None)
col_c50 = next((c for c, h in header.items() if "50元" in h), None)
col_c10 = next((c for c, h in header.items() if "10元" in h), None)
for r, cells in rows.items():
    if r == 1 or col_pname is None or cells.get(col_pname) is None:
        continue
    p = {
        "sys": cells.get(col_psys, ""),
        "name": cells[col_pname],
        "original": cells.get(col_orig, ""),
        "discount": cells.get(col_disc, ""),
        "special": cells.get(col_spec, ""),
        "charge50": cells.get(col_c50, ""),
        "charge10": cells.get(col_c10, ""),
    }
    prices[p["name"]] = p
    price_rows.append(p)

PRICE_OUT = ROOT / "docs" / ".vitepress" / "data" / "pet-prices.json"
PRICE_OUT.write_text(json.dumps(price_rows, ensure_ascii=False, indent=1), "utf-8")

pet_sheets = load_sheet(SRC_PET, set(ELEMENTS))
entries = []
seq = 0
for sheet, rows in pet_sheets.items():
    element = ELEMENTS[sheet]
    header = rows.get(1, {})
    col_name = next((c for c in ("A", "B") if header.get(c) in ("宠物图解", "宠物名称")), "A")
    col_type = next((c for c, h in header.items() if h == "宠物类型"), "C")
    col_illegal = next((c for c, h in header.items() if "非法" in h), "D")
    col_normal = next((c for c, h in header.items() if "正常" in h), "E")
    col_source = next((c for c, h in header.items() if "出处" in h), "F")
    note_cols = [c for c, h in header.items() if "绝版" in h or "没有填出处" in h]
    col_note = note_cols[0] if note_cols else None

    for r in sorted(rows):
        if r == 1:
            continue
        cells = rows[r]
        name = cells.get(col_name) or next(iter(cells.values()), "")
        if not name or name in ("宠物图解", "宠物名称"):
            continue
        # 数据清洗：统计行 / 锻造物品行 / 客栈价目行不是宠物
        if name.startswith(("合计", "合击")):
            continue
        if sheet == "任务物品锻造":
            continue
        if "客栈" in name or len(name) > 12:
            continue
        img = img_by_key.get((sheet, r)) or img_by_key.get((sheet, name))
        price = prices.get(name)
        seq += 1
        entries.append(
            {
                "id": seq,
                "name": name,
                "sheet": sheet,
                "element": element,
                "type": cells.get(col_type, ""),
                "evolveIllegal": cells.get(col_illegal, ""),
                "evolveNormal": cells.get(col_normal, ""),
                "source": cells.get(col_source, ""),
                "note": cells.get(col_note, "") if col_note else "",
                "image": {"file": img["file"], "ossKey": img["ossKey"], "url": img["url"]} if img else None,
                "price": price,
            }
        )

OUT.write_text(json.dumps(entries, ensure_ascii=False, indent=1), "utf-8")
with_img = sum(1 for e in entries if e["image"])
with_price = sum(1 for e in entries if e["price"])
print(f"pets: {len(entries)} entries, with image {with_img}, with price {with_price}")
print(f"elements:", {v: sum(1 for e in entries if e['element'] == v) for v in set(ELEMENTS.values())})
