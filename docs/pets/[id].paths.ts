import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const codex = JSON.parse(
  readFileSync(resolve(process.cwd(), "docs/.vitepress/data/pet-codex.json"), "utf-8")
);

export default {
  paths: () => codex.map((p: { id: number }) => ({ params: { id: String(p.id) } })),
};
