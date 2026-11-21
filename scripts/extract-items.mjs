import { readFileSync, writeFileSync } from "node:fs";

const SRC = process.argv[2] ?? "/Users/cheny/play/幻灵游侠2.5（快速端）/幻灵游侠2.5（快速端）/ini/ItemNote.ini";
const OUT = new URL("../docs/.vitepress/data/items.ts", import.meta.url);

const text = new TextDecoder("gbk").decode(readFileSync(SRC));
const items = [];
let current = null;
for (const line of text.split(/\r?\n/)) {
  const section = line.match(/^\[Item(\d+)\]$/);
  if (section) {
    if (current) items.push(current);
    current = { id: Number(section[1]) };
    continue;
  }
  const kv = line.match(/^(Name|Inventer|Note)=(.*)$/);
  if (kv && current) current[kv[1] === "Name" ? "name" : kv[1] === "Inventer" ? "inventer" : "note"] = kv[2];
}
if (current) items.push(current);

const body = `export interface ItemNote {
  id: number;
  name: string;
  inventer: string;
  note: string;
}

export const totalAmount = ${text.match(/^ItemAmount=(\d+)$/m)?.[1] ?? items.length};

export const items: ItemNote[] = ${JSON.stringify(items, null, 2)};
`;

writeFileSync(OUT, body);
console.log(`extracted ${items.length} items -> ${OUT.pathname}`);
