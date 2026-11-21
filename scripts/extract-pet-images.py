#!/usr/bin/env python3
"""从 宠物图鉴.xlsx 提取全部内嵌图片，按 sheet 分类落盘并生成映射表。

只读 /Users/cheny/play 原件；输出：
  assets/hl/pets/{metal,wood,water,fire,earth,shop,forge}/{hash10}.{ext}
  docs/.vitepress/data/pet-images.json  [{sheet, dir, name, row, file, ossKey, url}]

图片按内容 hash 命名（同图自动去重），宠物名与图片的锚定关系来自
xl/drawings 的行锚点；取锚点所在行第一个字符串单元格作为宠物名。
"""

import json
import hashlib
import posixpath
import re
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

SRC = Path(
    "/Users/cheny/play/EXCEL文件/宠物图鉴.xlsx"
)
OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "hl" / "pets"
DATA_OUT = Path(__file__).resolve().parent.parent / "docs" / ".vitepress" / "data" / "pet-images.json"

NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "xdr": "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}

SHEET_DIRS = {
    "金属性宠物": "metal",
    "木属性宠物": "wood",
    "水属性宠物": "water",
    "火属性宠物": "fire",
    "土属性宠物": "earth",
    "新山宠店宠物": "shop",
    "任务物品锻造": "forge",
}

OSS_BASE = "https://cheny-chenyu.oss-cn-chengdu.aliyuncs.com/hl/pets"


def load_shared(z):
    shared = []
    if "xl/sharedStrings.xml" not in z.namelist():
        return shared
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    for si in root.findall("m:si", NS):
        shared.append("".join(t.text or "" for t in si.iter(f"{{{NS['m']}}}t")))
    return shared


def cell_rows(z, sheet_xml):
    root = ET.fromstring(z.read(sheet_xml))
    rows = {}
    for row in root.iter(f"{{{NS['m']}}}row"):
        r = int(row.get("r"))
        values = []
        for c in row.iter(f"{{{NS['m']}}}c"):
            v = c.find(f"{{{NS['m']}}}v")
            if v is None or v.text is None:
                continue
            text = shared[int(v.text)] if c.get("t") == "s" else v.text
            text = (text or "").strip()
            if text:
                values.append(text)
        if values:
            rows[r] = values
    return rows


def qn(prefix, tag):
    return f"{{{NS[prefix]}}}{tag}"


z = zipfile.ZipFile(SRC)
shared = load_shared(z)

# sheet 名 → sheetN.xml
wb = ET.fromstring(z.read("xl/workbook.xml"))
wb_rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
rel_map = {rel.get("Id"): rel.get("Target") for rel in wb_rels.findall("pr:Relationship", NS)}
sheet_files = {}
for sh in wb.iter(qn("m", "sheet")):
    target = rel_map[sh.get(qn("r", "id"))].lstrip("/")
    if not target.startswith("xl/"):
        target = posixpath.join("xl", target)
    sheet_files[sh.get("name")] = target

entries = []
written = {}
for sheet_name, sheet_xml in sheet_files.items():
    dir_name = SHEET_DIRS.get(sheet_name)
    if not dir_name:
        continue
    rows = cell_rows(z, sheet_xml)

    rels_path = sheet_xml.replace("worksheets/", "worksheets/_rels/") + ".rels"
    if rels_path not in z.namelist():
        continue
    sheet_rels = ET.fromstring(z.read(rels_path))
    drawing_target = None
    for rel in sheet_rels.findall("pr:Relationship", NS):
        if rel.get("Type", "").endswith("/drawing"):
            drawing_target = rel.get("Target").replace("../", "xl/")
    if not drawing_target:
        continue

    drawing_rels = ET.fromstring(z.read(drawing_target.replace("drawings/", "drawings/_rels/") + ".rels"))
    img_by_rid = {
        rel.get("Id"): rel.get("Target").replace("../", "xl/")
        for rel in drawing_rels.findall("pr:Relationship", NS)
    }

    drawing = ET.fromstring(z.read(drawing_target))
    for anchor in list(drawing):
        blip = anchor.find(f".//{qn('a','blip')}")
        frm = anchor.find(f".//{qn('xdr','from')}")
        if blip is None or frm is None:
            continue
        rid = blip.get(qn("r", "embed"))
        media = img_by_rid.get(rid)
        if not media:
            continue
        row_num = int(frm.find(qn("xdr", "row")).text) + 1

        name = ""
        for probe in (row_num, row_num - 1, row_num + 1, row_num + 2):
            if probe in rows:
                name = rows[probe][0]
                if name not in ("宠物图解", "宠物名称"):
                    break
                name = rows[probe][1] if len(rows[probe]) > 1 else ""
                break
        name = re.sub(r"[\s/\\:*?\"<>|]", "", name)[:24]

        data = z.read(media)
        if media.lower().endswith(".gif"):
            import subprocess
            import tempfile

            with tempfile.TemporaryDirectory() as tmp:
                gif_path = Path(tmp) / "in.gif"
                png_path = Path(tmp) / "out.png"
                gif_path.write_bytes(data)
                subprocess.run(
                    ["sips", "-s", "format", "png", str(gif_path), "--out", str(png_path)],
                    capture_output=True,
                    check=True,
                )
                data = png_path.read_bytes()
            media = media[:-4] + ".png"
        digest = hashlib.sha1(data).hexdigest()[:10]
        ext = Path(media).suffix.lower()
        out_file = f"{digest}{ext}"
        out_path = OUT_DIR / dir_name / out_file
        if out_file not in written:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(data)
            written[out_file] = len(data)

        rel_path = f"{dir_name}/{out_file}"
        entries.append(
            {
                "sheet": sheet_name,
                "dir": dir_name,
                "name": name,
                "row": row_num,
                "file": rel_path,
                "ossKey": f"hl/pets/{rel_path}",
                "url": f"{OSS_BASE}/{rel_path}",
            }
        )

DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
DATA_OUT.write_text(json.dumps(entries, ensure_ascii=False, indent=2), "utf-8")

total_kb = sum(written.values()) / 1024
print(f"sheets: {len(sheet_files)} 提取 {len(entries)} 个锚点图, 去重后 {len(written)} 个文件, 共 {total_kb:.0f}KB")
print(f"落盘: {OUT_DIR}")
print(f"映射: {DATA_OUT}")
