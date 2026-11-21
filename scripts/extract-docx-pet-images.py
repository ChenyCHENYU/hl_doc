#!/usr/bin/env python3
"""【2026五系图鉴大全】docx 内嵌立绘 -> 图鉴补图

五个 docx（金木水火土）每行 = 宠物名 + 类型 + 属性 + 立绘图（word/media）。
按行文本锚定宠物名，图片按内容 hash 落盘 assets/hl/pets/{element}/，
输出 data/pet-images-2026.json，并把 pet-codex.json 中缺图的宠物补上 image
（同时为所有命中宠物记录 image2026 字段，供后续做"新版立绘"切换）。

管线顺序：extract-pet-codex.py 之后运行（本脚本在其产物上打补丁）。
docx 为只读输入，输出仅写入本项目。
"""

import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path("/Users/cheny/play/▲幻灵游侠优化资源▲/▲幻灵游侠优化资源▲/【2026五系图鉴大全】")
OUT_DIR = ROOT / "assets" / "hl" / "pets"
DATA = ROOT / "docs" / ".vitepress" / "data"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"

DOCX = [
    ("【金】宠物图鉴.docx", "metal"),
    ("【木】宠物图鉴.docx", "wood"),
    ("【水】宠物图鉴.docx", "water"),
    ("【火】宠物图鉴.docx", "fire"),
    ("【土】宠物图鉴.docx", "earth"),
]

OSS_BASE = "https://cheny-chenyu.oss-cn-chengdu.aliyuncs.com/hl/pets"

# 行首名字终止于类型词 / 颜色变体词 / 属性数字
NAME_RE = re.compile(
    r"^[-、．·，,\s\u3000\uff0d\xa0]*(.{1,12}?)\s*(?:防御型|敏攻型|攻击型|平均型|攻血型|攻防型|"
    r"血防型|防敏型|血攻型|攻敏型|防攻型|？？？|白色|黑色|金色|红色|蓝色|绿色|紫色|银色|\d)"
)

# 两代资料用字不同但为同一只宠（类型/系别一致），docx 名 -> codex 名
ALIAS = {"傲云兽": "傲雪兽"}


def pet_name(row_text: str) -> str | None:
    m = NAME_RE.match(row_text)
    if not m:
        return None
    name = re.sub(r"[\s\u3000\xa0]+", "", m.group(1))
    if len(name) < 2 or name.startswith(("=", "宠物", "金系", "木系", "水系", "火系", "土系")):
        return None
    return name


def to_png_if_gif(data: bytes, ext: str) -> tuple[bytes, str]:
    if ext.lower() != ".gif":
        return data, ext
    with tempfile.TemporaryDirectory() as tmp:
        gif_path = Path(tmp) / "in.gif"
        png_path = Path(tmp) / "out.png"
        gif_path.write_bytes(data)
        subprocess.run(
            ["sips", "-s", "format", "png", str(gif_path), "--out", str(png_path)],
            capture_output=True,
            check=True,
        )
        return png_path.read_bytes(), ".png"


def main():
    codex = json.load(open(DATA / "pet-codex.json"))
    by_name = {p["name"]: p for p in codex}

    records = []
    saved_hashes = set()
    for docx_name, element_dir in DOCX:
        path = SRC / docx_name
        if not path.exists():
            print(f"缺文件：{path}")
            continue
        z = zipfile.ZipFile(path)
        rels = {
            r.get("Id"): r.get("Target")
            for r in ET.fromstring(z.read("word/_rels/document.xml.rels")).iter(f"{{{PR}}}Relationship")
        }
        root = ET.fromstring(z.read("word/document.xml"))
        n_rows = n_kept = 0
        for tr in root.iter(f"{{{W}}}tr"):
            n_rows += 1
            text = "".join(t.text or "" for t in tr.iter(f"{{{W}}}t"))
            blips = [b.get(f"{{{R}}}embed") for b in tr.iter(f"{{{A}}}blip")]
            if not blips:
                continue
            name = pet_name(text)
            if not name:
                continue
            target = rels.get(blips[0])
            if not target or "media" not in target:
                continue
            media = "word/" + target.lstrip("/")
            try:
                data = z.read(media)
            except KeyError:
                continue
            data, ext = to_png_if_gif(data, Path(media).suffix)
            digest = hashlib.sha1(data).hexdigest()[:10]
            file_rel = f"{element_dir}/d{digest}{ext}"
            if digest not in saved_hashes:
                out = OUT_DIR / file_rel
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(data)
                saved_hashes.add(digest)
            rec = {
                "element": element_dir,
                "dir": element_dir,
                "name": name,
                "file": file_rel,
                "ossKey": f"hl/pets/{file_rel}",
                "url": f"{OSS_BASE}/{file_rel}",
            }
            records.append(rec)
            n_kept += 1
        print(f"{docx_name}: 行 {n_rows} → 锚定 {n_kept} 只")

    # 去重：同名取首个；别名归一到 codex 名
    best: dict[str, dict] = {}
    for r in records:
        key = ALIAS.get(r["name"], r["name"])
        r["name"] = key
        best.setdefault(key, r)

    (DATA / "pet-images-2026.json").write_text(
        json.dumps(list(best.values()), ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )

    # 补丁 codex：缺图补 image，全部命中记 image2026；顺带用 2026 图鉴补齐"？？"类型
    try:
        stats_by_name = {st["name"]: st for st in json.load(open(DATA / "pet-stats-2026.json"))}
    except Exception:
        stats_by_name = {}
    filled = marked = typed = 0
    for p in codex:
        if (not p.get("type") or set(p["type"]) <= {"？", "?"}) and p["name"] in stats_by_name:
            st_type = stats_by_name[p["name"]].get("type") or ""
            if st_type and not set(st_type) <= {"？", "?"}:
                p["type"] = st_type
                typed += 1
        rec = best.get(p["name"])
        if not rec:
            continue
        img = {"file": rec["file"], "ossKey": rec["ossKey"], "url": rec["url"]}
        p["image2026"] = img
        marked += 1
        if not p.get("image"):
            p["image"] = img
            filled += 1
    (DATA / "pet-codex.json").write_text(
        json.dumps(codex, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )

    no_img = [p["name"] for p in codex if not p.get("image")]
    print(f"锚定宠物 {len(best)} 只；codex 补图 {filled} 只、记 2026 立绘 {marked} 只、补类型 {typed} 只；仍缺图 {no_img}")


if __name__ == "__main__":
    main()
