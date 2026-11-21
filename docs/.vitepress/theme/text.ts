export function escapeHtml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

const KEY_PATTERNS: RegExp[] = [
  /(?:\d+(?:\.\d+)?(?:[-~到]\d+(?:\.\d+)?)?\s*(?:级|点|次|个|倍|只|小时|分钟|万|亿|%))/g,
  /每[^，。；,.\s]{0,8}?(?:级|次|点|只|天|日)/g,
  /忠诚(?:度)?(?:100|下降|达到|为)?/g,
  /(?:才能|必须)[^，。；,.]{0,12}/g,
];

// 负面/警示词单独标红，与金色重点区分
const WARN_PATTERNS: RegExp[] = [/(?:不可|无法|请勿|不要|注意|千万|禁止|删号|封号|丢失|无法挽回)[^，。；,.]{0,10}/g];

type Mark = { st: number; en: number; warn: boolean };

export function highlight(s: string): string {
  let html = escapeHtml(s);
  const marks: Mark[] = [];
  for (const re of KEY_PATTERNS) {
    for (const m of s.matchAll(re)) {
      if (m.index !== undefined) marks.push({ st: m.index, en: m.index + m[0].length, warn: false });
    }
  }
  for (const re of WARN_PATTERNS) {
    for (const m of s.matchAll(re)) {
      if (m.index !== undefined) marks.push({ st: m.index, en: m.index + m[0].length, warn: true });
    }
  }
  if (!marks.length) return html;
  marks.sort((a, b) => a.st - b.st);
  const merged: Mark[] = [];
  for (const mk of marks) {
    const last = merged[merged.length - 1];
    if (merged.length && mk.st <= last.en) {
      last.en = Math.max(last.en, mk.en);
      last.warn = last.warn || mk.warn;
    } else {
      merged.push({ ...mk });
    }
  }
  let out = "";
  let pos = 0;
  for (const { st, en, warn } of merged) {
    out += escapeHtml(s.slice(pos, st));
    out += `<b class="${warn ? "hl-warn" : "hl-key"}">${escapeHtml(s.slice(st, en))}</b>`;
    pos = en;
  }
  out += escapeHtml(s.slice(pos));
  return out;
}
