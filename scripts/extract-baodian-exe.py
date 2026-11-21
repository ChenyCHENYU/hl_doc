#!/usr/bin/env python3
"""幻灵玩家宝典.exe -> 玩家文库

从 exe overlay 解出全部 zlib HTML 文章（天下网游论坛精华合集），
剥离论坛模板行（跨文档高频行 + 关键词黑名单），按标题自动分类，
生成 docs/guide/library/lib-NNN.md + data/library.json + data/library-sidebar.json。
exe 为只读输入，输出仅写入本项目。
"""

import json
import re
import struct
import zlib
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXE = Path("/Users/cheny/play/东哥定制全套服务/东哥定制全套服务/幻灵玩家宝典.exe")
OUT = ROOT / "docs" / "guide" / "library"
DATA = ROOT / "docs" / ".vitepress" / "data"

CATEGORIES = [
    ("宠物练级", ["练级", "升级路线", "路线"]),
    ("宠物养成", ["幻化", "变异", "进化", "养宠", "忠诚", "宠物技能", "受伤", "宠物资料", "宠物"]),
    ("宠物分布", ["分布", "坐标", "抓宠", "捕捉"]),
    ("锻造-武器", ["武器", "炼化", "刀", "剑"]),
    ("锻造-防具", ["战衣", "防衣", "敏衣", "血衣", "内衣", "甲", "鞋", "内带", "标衣"]),
    ("锻造-饰品", ["右饰", "左饰", "钗", "珠", "锁", "佩", "饰"]),
    ("锻造-其他", ["锻造", "煅造", "炼化", "制作", "数据"]),
    ("战斗与PK", ["PK", "战斗", "克与被克", "伤血公式"]),
]

BLACKLIST = re.compile(
    r"论坛|搜索|注册|登录|积分|头像|短消息|加为好友|查看资料|引用|回复|编辑|删除|评分|"
    r"Copyright|版权|站长|统计|在线|游客|会员|发帖|帖数|注册时间|最后登录|精华|贡献|威望|金钱|"
    r"快速跳转|论坛模式|浏览次数|字体|打印|订阅|收藏|推荐|楼|#\d+|返回列表|本页|主题|"
    r"天下网游|幻灵之路|只读"
)


class H2T(HTMLParser):
    BLOCKS = ("p", "div", "tr", "li", "br", "table", "h1", "h2", "h3", "h4", "td", "th", "center")

    def __init__(self):
        super().__init__()
        self.parts: list[str] = []
        self._buf: list[str] = []
        self._skip = 0
        self._skip_fmt = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self._skip += 1
        if tag == "font":
            self._skip_fmt += 1
        if tag in self.BLOCKS:
            self._flush()

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self._skip:
            self._skip -= 1
        if tag == "font" and self._skip_fmt:
            self._skip_fmt -= 1
        if tag in self.BLOCKS:
            self._flush()

    def handle_data(self, data):
        if self._skip:
            return
        self._buf.append(data)

    def _flush(self):
        t = re.sub(r"[ \t\u3000\xa0]+", " ", "".join(self._buf)).strip()
        self._buf = []
        if t:
            self.parts.append(t)

    def result(self):
        self._flush()
        return self.parts


def html_text(html: bytes) -> list[str]:
    parser = H2T()
    parser.feed(html.decode("gbk", "replace"))
    return parser.result()


def clean_title(raw: str) -> str:
    t = raw
    if " - " in t:
        t = t.split(" - ")[-1]
    t = re.sub(r"^\[[^\]]{1,6}\]", "", t.strip())
    t = re.sub(r"\s+", " ", t).strip()
    return t[:50]


def html_to_blocks(html: str) -> list[str]:
    h = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", "", html)
    tables: list[str] = []

    def table_repl(m):
        rows = []
        for tr in re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", m.group(0)):
            cells = []
            for cell in re.findall(r"(?is)<t[dh][^>]*>(.*?)</t[dh]>", tr):
                text = re.sub(r"(?is)<br\s*/?>", " ", cell)
                text = re.sub(r"<[^>]+>", "", text)
                text = unescape(re.sub(r"\s+", " ", text)).strip()
                cells.append(text.replace("|", "\\|"))
            if any(cells):
                rows.append(cells)
        if not rows:
            return ""
        width = max(len(r) for r in rows)
        norm = [r + [""] * (width - len(r)) for r in rows]
        md = "| " + " | ".join(norm[0]) + " |\n"
        md += "| " + " | ".join(["---"] * width) + " |\n"
        for r in norm[1:]:
            md += "| " + " | ".join(r) + " |\n"
        tables.append(md)
        return f"\n\x02TABLE{len(tables) - 1}\x03\n"

    h = re.sub(r"(?is)<table[^>]*>.*?</table>", table_repl, h)
    h = re.sub(r"(?is)</?font[^>]*>", "", h)
    h = re.sub(r"(?is)<li[^>]*>", "\n- ", h)
    h = re.sub(r"(?is)</li>", "\n", h)
    h = re.sub(
        r"(?is)<(b|strong)[^>]*>(.*?)</\1>",
        lambda m: "**" + re.sub(r"<[^>]+>", "", m.group(2)).strip() + "**",
        h,
    )
    h = re.sub(r"\*\*\s*\*\*", "", h)
    h = re.sub(r"\*\*\s*(.+?)\s*\*\*", r"**\1**", h)
    h = re.sub(r"(?is)<br\s*/?>", "\n", h)
    h = re.sub(r"(?is)</?(p|div|tr|td|th|h[1-6]|center|blockquote|ul|ol|table)[^>]*>", "\n\n", h)
    h = re.sub(r"<[^>]+>", "", h)
    h = unescape(h)

    blocks: list[str] = []
    for para in re.split(r"\n\s*\n", h):
        lines = []
        for ln in para.split("\n"):
            ln = re.sub(r"[ \t\u3000\xa0]{2,}", "\t", ln)
            ln = re.sub(r"[ \t\u3000\xa0]", " ", ln).strip()
            if ln:
                lines.append(ln)
        if not lines:
            continue
        if len(lines) == 1 and re.fullmatch(r"\x02TABLE\d+\x03", lines[0]):
            blocks.append(tables[int(lines[0][6:-1])].strip())
            continue

        tab_rows = [ln for ln in lines if "\t" in ln]
        if len(tab_rows) < 3:
            def is_data_row(ln: str) -> bool:
                toks = ln.split(" ")
                if len(toks) < 3 or len(toks) > 12 or "\t" in ln:
                    return False
                nums = sum(
                    1
                    for t in toks
                    if re.fullmatch(r"[\d.]+%?", t) or re.fullmatch(r"\(\d+,\d+\)", t) or re.fullmatch(r"\d+-\d+", t)
                )
                return nums >= 2 and bool(re.search(r"[\u4e00-\u9fffA-Za-z]", toks[0]))

            run = [ln for ln in lines if is_data_row(ln) or "\t" in ln]
            if len(run) >= 4:
                tab_rows = run
                lines = [ln for ln in lines if ln not in run]
        if len(tab_rows) >= 3:
            header = None
            for ln in lines:
                if "\t" not in ln and ln.count("/") >= 2 and len(ln) < 80:
                    header = [c.strip() for c in ln.split("/")]
                    break
            rows = [[c.strip() for c in (ln.split("\t") if "\t" in ln else ln.split(" ")) if c.strip() != ""] for ln in tab_rows]
            width = max(len(r) for r in rows)
            if not header or len(header) > width + 1:
                header = rows[0]
                rows = rows[1:]
            header = (header + [""] * width)[:width]
            if rows:
                norm = [r + [""] * (width - len(r)) for r in rows]
                tbl = "| " + " | ".join(header[:width]) + " |\n"
                tbl += "| " + " | ".join(["---"] * width) + " |\n"
                for r in norm:
                    tbl += "| " + " | ".join(r) + " |\n"
                blocks.append(tbl.strip())
                lines = [ln for ln in lines if "\t" not in ln and ln not in ("/".join(header),)]
                if not lines:
                    continue
        md_lines = []
        short_run: list[str] = []

        def flush_run():
            nonlocal short_run
            if len(short_run) >= 3:
                md_lines.append(" · ".join(short_run))
            else:
                md_lines.extend(short_run)
            short_run = []

        for ln in lines:
            if not ln.strip("*#-|: "):
                continue
            if "\ufffd" in ln:
                continue
            if re.fullmatch(r"[\u4e00-\u9fff]{1,4}|\d{1,3}层?", ln):
                short_run.append(ln)
                continue
            flush_run()
            if md_lines and len(ln) <= 3 and not md_lines[-1].startswith(("#", ":::", "|")):
                md_lines[-1] = md_lines[-1] + " " + ln
                continue
            if re.fullmatch(r"\*\*.{1,22}\*\*", ln):
                md_lines.append(f"### {ln[2:-2].strip()}")
            elif re.match(r"^\d{1,2}[.、．)）]\s*.{1,16}$", ln) and re.search(r"[\u4e00-\u9fff]", ln) and not ln.startswith("**"):
                md_lines.append(f"### {ln}")
            elif re.match(r"^(p\.s\.|P\.S\.|ps)\b", ln, re.I) or re.match(r"^(提示|注意|说明)[：:]", ln):
                md_lines.append("::: tip 玩家提示\n" + ln + "\n:::")
            elif any(k in ln for k in ("千万", "切记", "一定不要", "务必", "小心")) and len(ln) <= 90:
                md_lines.append("::: warning 注意\n" + ln + "\n:::")
            elif re.match(r"^[^：，。\d]{2,12}[：:](.{1,90})$", ln) and "**" not in ln:
                m2 = re.match(r"^([^：，。]{2,12})[：:](.+)$", ln)
                md_lines.append(f"**{m2.group(1)}**：{m2.group(2)}")
            else:
                md_lines.append(ln)
        flush_run()
        blocks.append("  \n".join(md_lines))
    return blocks


def unescape(s: str) -> str:
    return (
        s.replace("&nbsp;", " ")
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
    )


def is_clean_line(ln: str) -> bool:
    if "\ufffd" in ln:
        return False
    bad = sum(1 for c in ln if not ("\u4e00" <= c <= "\u9fff") and not c.isprintable())
    return bad <= len(ln) * 0.1


def categorize(title: str) -> str:
    for cat, kws in CATEGORIES:
        if any(k in title for k in kws):
            return cat
    return "综合其他"


data = EXE.read_bytes()
overlay = data[data.index(b"[Info]"):]
overlay = overlay[overlay[0x7b000 - data.index(b"[Info]"):] if False else 0:]

raw_pages = []
for m in re.finditer(rb"\x78[\x01\x5e\x9c\xda]", overlay):
    s = m.start()
    try:
        out = zlib.decompressobj().decompress(overlay[s:s + 900000])
    except Exception:
        continue
    if len(out) < 300 or b"<HTML" not in out[:600].upper():
        continue
    nl = struct.unpack_from("<I", out, 8)[0]
    html = out[12 + nl:]
    m_end = re.search(rb"</html\s*>", html, re.I)
    if m_end:
        html = html[: m_end.end()]
    else:
        cut = len(html)
        for sig in (b"GIF89a", b"GIF87a", b"\xff\xd8\xff\xe0", b"\x89PNG"):
            pos = html.find(sig)
            if 0 < pos < cut:
                cut = pos
        html = html[:cut]
    mt = re.search(rb"<TITLE>(.*?)</TITLE>", html[:3000], re.S | re.I)
    title = clean_title(mt.group(1).decode("gbk", "replace")) if mt else ""
    if not title or len(html) < 1200:
        continue
    raw_pages.append((title, html))

line_freq: dict[str, int] = {}
all_blocks = []
for title, html in raw_pages:
    blocks = [b for b in html_to_blocks(html.decode("gbk", "replace")) if b.strip()]
    all_blocks.append(blocks)
    for b in dict.fromkeys(blocks):
        first = b.split("\n")[0].strip("*# |:-")
        if 2 <= len(first) <= 60:
            line_freq[first] = line_freq.get(first, 0) + 1


# ── 纯文本块精修：数值加粗 + 超长段拆句（结构块表格/步骤不动）──
def bold_nums(t: str) -> str:
    t = re.sub(r"(?<=[\d\u4e00-\u9fff])\*(?=\d)", "×", t)
    t = re.sub(r"(\d{2,4}\s*级)", r"**\1**", t)
    t = re.sub(r"(忠诚\s*100)", r"**\1**", t)
    t = re.sub(r"(\d{1,3}\.\d{1,2})", r"**\1**", t)
    return t


def enrich_block(b: str) -> str:
    lines = b.split("\n")
    out = []
    for ln in lines:
        if len(ln) > 150:
            import re as _re
            parts = [q for q in _re.split(r"(?<=[。！？；])", ln) if q.strip()]
            buf = ""
            for q in parts:
                if len(buf) + len(q) > 110 and buf:
                    out.append(bold_nums(buf))
                    buf = q
                else:
                    buf += q
            if buf:
                out.append(bold_nums(buf))
        else:
            out.append(bold_nums(ln))
    return "\n".join(out)


THRESHOLD = max(8, len(raw_pages) // 8)
OUT.mkdir(parents=True, exist_ok=True)
for old in OUT.glob("lib-*.md"):
    old.unlink()

entries = []
for idx, ((title, html), blocks) in enumerate(zip(raw_pages, all_blocks), start=1):
    body = []
    for b in blocks:
        first = b.split("\n")[0].strip()
        structured = b.startswith(("#", "|", ":::", "**", "-", "1.", "2.", "3."))
        plain = first.strip("*# |:-")
        if not structured:
            if line_freq.get(plain, 0) >= THRESHOLD and len(plain) < 40:
                continue
            if BLACKLIST.search(plain):
                continue
            if len(plain) < 2 or not is_clean_line(plain):
                continue
        body.append(enrich_block(b) if not structured else b)
    if len(body) < 3:
        continue
    if title and body and title[:10] in body[0]:
        body = body[1:]
    cat = categorize(title)
    slug = f"lib-{idx:03d}"
    md = [
        f"---\ntitle: {json.dumps(title, ensure_ascii=False)}"
        + ("\naside: false" if sum(b.startswith(("## ", "### ")) for b in body) < 2 else "")
        + f"\n---\n\n# {title}\n",
        f'<TopicHeader cat="玩家文库 · {cat}" src="幻灵玩家宝典.exe" />\n',
        "> 来源：《幻灵玩家宝典 V1.0》玩家自制电子书（天下网游论坛精华合集），文字整理保留原意。\n",
    ]
    body_md = "\n\n".join(body)

    import json as _json
    codex_names = None
    try:
        codex_names = {e["name"]: e["id"] for e in _json.load(open(DATA / "pet-codex.json"))}
    except Exception:
        codex_names = {}

    def autolink(text: str) -> str:
        linked = set()
        lines = text.split("\n")
        for idx, ln in enumerate(lines):
            if ln.startswith(("#", "|", "<", ">", ":::", "```", "[")):
                continue
            for name, pid in codex_names.items():
                if name in linked or len(name) < 2 or name not in ln:
                    continue
                if f"]({name})" in ln or f"[{name}]" in ln:
                    linked.add(name)
                    continue
                lines[idx] = ln = ln.replace(name, f"[{name}](/pets/{pid})", 1)
                linked.add(name)
                if len(linked) >= 40:
                    break
        return "\n".join(lines)

    body_md = autolink(body_md)
    md.append(body_md)

    md.append('\n<div class="lib-nav">\n  <span class="lib-prev-slot"></span>\n  <a href="/guide/library/" class="lib-nav-home">返回文库</a>\n  <span class="lib-next-slot"></span>\n</div>\n')
    content = re.sub(r"\n{3,}", "\n\n", "\n".join(md)).strip() + "\n"
    content = re.sub(r"(?m)^\*{2,}\s*$\n?", "", content)
    content = content.replace("****", "")
    (OUT / f"{slug}.md").write_text(content, "utf-8")
    entries.append({"slug": slug, "title": title, "cat": cat, "paras": len(body)})

groups: dict[str, list] = {}
for e in entries:
    groups.setdefault(e["cat"], []).append(e)

for cat, items in groups.items():
    for idx, e in enumerate(items):
        fpath = OUT / f"{e['slug']}.md"
        if not fpath.exists():
            continue
        content = fpath.read_text("utf-8")
        prev_html = next_html = '<span class="lib-nav-dim">—</span>'
        if idx > 0:
            p = items[idx - 1]
            prev_html = f'<a href="/guide/library/{p["slug"]}">&#8249; 上一篇 · {p["title"][:18]}</a>'
        if idx + 1 < len(items):
            nx = items[idx + 1]
            next_html = f'<a href="/guide/library/{nx["slug"]}">下一篇 · {nx["title"][:18]} &#8250;</a>'
        content = content.replace('<span class="lib-prev-slot"></span>', prev_html)
        content = content.replace('<span class="lib-next-slot"></span>', next_html)
        fpath.write_text(content, "utf-8")

sidebar = [
    {"text": cat, "collapsed": True, "items": [{"text": e["title"][:12], "link": f"/guide/library/{e['slug']}"} for e in items]}
    for cat, items in groups.items()
]
(DATA / "library-sidebar.json").write_text(json.dumps(sidebar, ensure_ascii=False, indent=1), "utf-8")
(DATA / "library.json").write_text(json.dumps(entries, ensure_ascii=False, indent=1), "utf-8")
print(f"library: {len(entries)} articles, categories: {[(g, len(v)) for g, v in groups.items()]}")
