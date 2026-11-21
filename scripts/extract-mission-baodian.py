#!/usr/bin/env python3
"""幻灵7大宝典 Mission.txt -> 玩家文库（宝典合集）

优化资源包"幻灵7大宝典"目录 = 同一阅读器 exe（183296B）+ 各自 Mission.txt 数据包。
本脚本解析 6 份 Mission.txt（《幻灵资料查询》与《幻灵宝典》内容相同，仅取其一），
按 标题+正文归一化哈希 跨源去重、并与现有文库（幻灵玩家宝典.exe 139 篇）去重，
生成 docs/guide/library/bd-NNN.md，并把条目合并进 library.json / library-sidebar.json。

管线顺序：先跑 extract-baodian-exe.py（重建 lib-*.md + 基础 json），再跑本脚本（追加 bd-*）。
源文件只读，输出仅写入本项目。
"""

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAY = Path("/Users/cheny/play/▲幻灵游侠优化资源▲/▲幻灵游侠优化资源▲/幻灵7大宝典")
OUT = ROOT / "docs" / "guide" / "library"
DATA = ROOT / "docs" / ".vitepress" / "data"

# 顺序即去重优先级：版本越新/内容越全的排前面
SOURCES = [
    ("新编幻灵宝典", "新编幻灵宝典/Mission.txt", "奇幻侠客的葵花宝典.exe"),
    ("幻灵资料查询", "《幻灵资料查询》/Mission.txt", "《幻灵游侠浏览器》.exe"),
    ("幻灵宝典2011", "幻灵宝典2011/Mission.txt", "幻灵游侠宝典.exe"),
    ("幻灵游侠宝典2009修改版", "幻灵游侠宝典2009修改版/Mission.txt", "幻灵游侠宝典2009版.exe"),
    ("幻灵官服宝典", "幻灵官服宝典/Mission.txt", "幻灵宝典.exe"),
    ("幻灵锻造宝典", "幻灵锻造宝典/Mission.txt", "幻灵锻造宝典.exe"),
]

CATEGORIES = [
    ("宠物练级", ["练级", "升级路线", "路线", "极速练宠"]),
    ("宠物养成", ["幻化", "变异", "进化", "养宠", "忠诚", "宠物技能", "受伤", "宠物资料", "宠物", "宠"]),
    ("宠物分布", ["分布", "坐标", "抓宠", "捕捉"]),
    ("锻造-武器", ["武器", "炼化", "刀", "剑", "彪武器"]),
    ("锻造-防具", ["战衣", "防衣", "敏衣", "血衣", "内衣", "甲", "鞋", "内带", "标衣", "彪衣"]),
    ("锻造-饰品", ["右饰", "左饰", "钗", "珠", "锁", "佩", "饰"]),
    ("锻造-其他", ["锻造", "煅造", "炼化", "制作", "数据", "材料"]),
    ("战斗与PK", ["PK", "战斗", "克与被克", "伤血公式"]),
    ("任务与飞升", ["任务", "飞升", "转生", "兵解", "投胎"]),
]

DECOR = re.compile(r"^[\s━─═◆◇★☆*·.。,'\-—﹏′\u3000]+$")


def norm_title(s: str) -> str:
    return re.sub(r"[◆◇★\s。，.\d！!?？:：;；,、()\[\]（）-]+", "", s)


def parse_mission(path: Path):
    text = path.read_bytes().decode("gb18030", "replace")
    entries, cur, buf = [], None, []
    for ln in text.split("\n"):
        ln = ln.rstrip("\r")
        if ln.startswith("PATH="):
            if cur is not None:
                entries.append((cur, buf))
            cur, buf = ln[5:].strip(), []
        elif ln == "END;":
            continue
        else:
            buf.append(ln)
    if cur is not None:
        entries.append((cur, buf))
    return entries


def is_char_art(line: str) -> bool:
    """单字符重复为主的字符画（如 logo 的『幻幻幻…』）。"""
    if len(line) < 8:
        return False
    freq = {}
    for ch in line:
        if ch.strip():
            freq[ch] = freq.get(ch, 0) + 1
    if not freq:
        return True
    top = max(freq.values())
    return top / sum(freq.values()) > 0.6 and len(freq) <= 4


def clean_lines(lines: list[str]) -> list[str]:
    out = []
    for l in lines:
        if l.strip() == "DATA=":
            continue
        l = re.sub(r"[\u3000 ]+", " ", l).strip()
        if not l or DECOR.match(l):
            continue
        if not re.search(r"[\u4e00-\u9fffA-Za-z0-9]", l):
            continue
        if is_char_art(l):
            continue
        out.append(l)
    return out



# ── 正文精修：词条加粗 / 数值加粗 / 编号成列 / 提示容器 / 超长段拆句 ──
TERM_RE = re.compile(r"^([^，。；：:！？\s]{1,8})[：:]\s*(.{4,})$")
NUM_ITEM_RE = re.compile(r"^(\d{1,2})[、.．)）]\s*(.+)$")
TIP_RE = re.compile(r"^(PS|ps|注意|提示|提醒|切记)")


def bold_nums(t: str) -> str:
    t = re.sub(r"(?<=[\d）)\u4e00-\u9fff])\*(?=\d)", "×", t)
    t = re.sub(r"(\d{2,4}\s*级)", r"**\1**", t)
    t = re.sub(r"(忠诚\s*100)", r"**\1**", t)
    t = re.sub(r"(\d{1,3}\.\d{1,2})", r"**\1**", t)
    return t


def enrich_bd(lines):
    out, tips = [], []
    ol = []

    def flush_ol():
        nonlocal ol
        if ol:
            out.append("\n".join(f"{i}. {t}" for i, t in enumerate(ol, 1)))
            ol = []

    for raw in lines:
        t = raw.strip()
        if not t:
            flush_ol()
            continue
        if TIP_RE.match(t):
            flush_ol()
            tips.append(bold_nums(t))
            continue
        m = NUM_ITEM_RE.match(t)
        if m:
            ol.append(bold_nums(m.group(2)))
            continue
        flush_ol()
        tm = TERM_RE.match(t)
        if tm:
            tail = tm.group(2)
            if len(tail) > 150:
                import re as _re
                parts = [q for q in _re.split(r"(?<=[。！？；])", tail) if q.strip()]
                buf = ""
                for q in parts:
                    if len(buf) + len(q) > 110 and buf:
                        out.append(f"**{tm.group(1)}**：{bold_nums(buf)}" if buf is parts[0] else bold_nums(buf))
                        buf = q
                    else:
                        buf += q
                if buf:
                    out.append(bold_nums(buf))
            else:
                out.append(f"**{tm.group(1)}**：{bold_nums(tail)}")
            continue
        # 数值流水（锻造记录等：数字密、句读少）→ 等宽代码块
        if len(t) > 120 and len(re.findall(r"\d{2,5}", t)) >= 6 and t.count("。") <= 1:
            out.append("```\n" + t + "\n```")
            continue
        # 超长段按句拆分（150 字以上）
        if len(t) > 150:
            import re as _re
            parts = [p for p in _re.split(r"(?<=[。！？；])", t) if p.strip()]
            buf = ""
            for p in parts:
                if len(buf) + len(p) > 110 and buf:
                    out.append(bold_nums(buf))
                    buf = p
                else:
                    buf += p
            if buf:
                out.append(bold_nums(buf))
            continue
        out.append(bold_nums(t))
    flush_ol()
    if tips:
        out.append("::: info 玩家提示\n" + "\n".join(f"- {t}" for t in tips) + "\n:::")
    return out


def merge_short(paras: list[str]) -> list[str]:
    """过短行并入前段，避免碎片段落。"""
    out: list[str] = []
    for p in paras:
        if out and len(p) < 8:
            out[-1] += p
        else:
            out.append(p)
    return out


def escape_md(line: str) -> str:
    if re.match(r"^[#*`|>\-+]", line):
        return "\\" + line
    return line


def categorize(title: str, first_line: str) -> str:
    for cat, kws in CATEGORIES:
        for kw in kws:
            if kw in title or kw in first_line:
                return cat
    return "综合其他"


def main():
    codex_names = {}
    try:
        codex = json.load(open(DATA / "pet-codex.json"))
        codex_names = {e["name"]: e["id"] for e in codex if len(e["name"]) >= 2}
    except Exception:
        pass

    # ── 现有文库的去重集（只认基础 lib-*，bd-* 是本脚本自身产物会重建）──
    existing = json.load(open(DATA / "library.json"))
    exist_titles = {norm_title(e["title"]) for e in existing if not e["slug"].startswith("bd-")}
    exist_hashes = set()
    for f in OUT.glob("lib-*.md"):
        body = f.read_text(encoding="utf-8").split("> 来源：", 1)[-1]
        h = hashlib.md5("".join(body.split()).encode()).hexdigest()
        exist_hashes.add(h)

    seen_titles, seen_hashes = set(exist_titles), set(exist_hashes)
    stats, kept = [], []

    for name, rel, exe in SOURCES:
        path = PLAY / rel
        if not path.exists():
            stats.append(f"{name}: 源缺失，跳过")
            continue
        n_raw = n_kept = 0
        for title, lines in parse_mission(path):
            n_raw += 1
            content = clean_lines(lines)
            if len(content) < 2:
                continue
            # 标题取层级最后一段，去掉装饰符
            short = re.sub(r"[◆◇★\s]+", "", title.split("->")[-1]).replace("2。5", "2.5")
            if len(short) < 2:
                continue
            nt = norm_title(short)
            body_norm = "".join("".join(content).split())
            h = hashlib.md5(body_norm.encode()).hexdigest()
            if nt in seen_titles or h in seen_hashes:
                continue
            seen_titles.add(nt)
            seen_hashes.add(h)
            cat = categorize(short, content[0])
            kept.append({"title": short, "cat": cat, "src": name, "exe": exe, "content": content})
            n_kept += 1
        stats.append(f"{name}: 解析 {n_raw} 条 → 收 {n_kept} 条")

    # ── 写 bd-NNN.md ──
    for old in OUT.glob("bd-*.md"):
        old.unlink()
    entries_json = []
    for idx, e in enumerate(kept, start=1):
        slug = f"bd-{idx:03d}"
        paras = enrich_bd([escape_md(l) for l in e["content"]])
        body_md = "\n\n".join(paras)

        linked = set()
        lines = body_md.split("\n")
        for i, ln in enumerate(lines):
            if len(linked) >= 120:
                break
            if ln.startswith(("\\", "#", "|", "<", ">", "`", "[")):
                continue
            for pname, pid in codex_names.items():
                if pname in linked or pname not in ln:
                    continue
                lines[i] = ln = ln.replace(pname, f"[{pname}](/pets/{pid})", 1)
                linked.add(pname)
        body_md = "\n".join(lines)

        md = (
            f"---\ntitle: {json.dumps(e['title'], ensure_ascii=False)}"
            + ("\naside: false" if body_md.count("\n## ") + body_md.count("\n### ") + body_md.count("\n- **") < 2 else "")
            + f"\n---\n\n"
            f"# {e['title']}\n\n"
            f"<TopicHeader cat=\"玩家文库 · {e['cat']}\" src=\"{e['exe']}\" />\n\n"
            f"> 来源：《{e['src']}》（游戏内资料查询器，Mission.txt 数据包），条目化整理保留原意。\n\n"
            f"{body_md}\n"
        )
        (OUT / f"{slug}.md").write_text(md, encoding="utf-8")
        entries_json.append({"slug": slug, "title": e["title"], "cat": e["cat"], "paras": len(paras)})

    # ── 合并 json（基础 lib-* 由 extract-baodian-exe.py 生成，本脚本只追加 bd-*）──
    merged = [e for e in existing if not e["slug"].startswith("bd-")] + entries_json
    (DATA / "library.json").write_text(
        json.dumps(merged, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )

    # sidebar 先剔除旧 bd 条目（本脚本产物，重建），再合并本次结果，避免跨运行累积死链
    sidebar = json.load(open(DATA / "library-sidebar.json"))
    for g in sidebar:
        g["items"] = [it for it in g.get("items", []) if "/guide/library/bd-" not in it.get("link", "")]
    sidebar = [g for g in sidebar if g.get("items")]
    by_cat: dict[str, list] = {}
    for e in entries_json:
        by_cat.setdefault(e["cat"], []).append({"text": e["title"], "link": f"/guide/library/{e['slug']}"})
    groups = {g["text"]: g for g in sidebar}
    for cat, items in by_cat.items():
        if cat in groups:
            groups[cat]["items"].extend(items)
        else:
            newg = {"text": cat, "collapsed": True, "items": items}
            if "综合其他" in groups:
                sidebar.insert(list(groups).index("综合其他") + 1, newg)
                groups[cat] = newg
            else:
                sidebar.append(newg)
                groups[cat] = newg
    (DATA / "library-sidebar.json").write_text(
        json.dumps(sidebar, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )

    for s in stats:
        print(s)
    print(f"library.json: {len(existing)} → {len(merged)} 条（新增 {len(entries_json)}）")


if __name__ == "__main__":
    main()
