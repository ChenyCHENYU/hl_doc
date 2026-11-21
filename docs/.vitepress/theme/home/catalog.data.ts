import { defineLoader } from "vitepress";
import codex from "../../data/pet-codex.json" with { type: "json" };
import library from "../../data/library.json" with { type: "json" };
import tower from "../../data/tower-defense.json" with { type: "json" };
import attributes from "../../data/pet-stats-2026.json" with { type: "json" };
import gallery from "../../data/gallery.json" with { type: "json" };
import { items } from "../../data/items.ts";
import { computeLineages, type EvoPet } from "../evolution.ts";

const featured = [
  "苦行龟", "雪凤凰", "霹雳虎", "裁决精灵", "幻晶刚", "冰晶刚",
  "寿眉", "白骨战士", "小法师", "考拉熊", "白骨魅姬", "斑斑虎",
];
const elements = ["metal", "wood", "water", "fire", "earth"] as const;

function petPreview(pet: EvoPet) {
  return {
    id: pet.id,
    name: pet.name,
    element: pet.element,
    image: pet.image?.ossKey || null,
    evolveIllegal: pet.evolveIllegal,
  };
}

function readHomeCatalog() {
  const allLineages = computeLineages(codex);
  const petsByName = new Map(codex.map(pet => [pet.name, pet]));
  return {
    stats: [
      { count: codex.length, name: "宠物档案", url: "/pets/" },
      { count: library.length, name: "文库文章", url: "/guide/library/" },
      { count: items.length, name: "物品条目", url: "/items/" },
      { count: tower.length, name: "天关关卡", url: "/monsters/" },
      { count: attributes.length, name: "2026 属性条目", url: "/pets/" },
      { count: gallery.length, name: "画廊藏图", url: "/resources/" },
    ],
    pets: featured.flatMap((name) => {
      const pet = petsByName.get(name);
      return pet ? [petPreview(pet)] : [];
    }),
    evolutionCount: allLineages.length,
    lineages: elements.flatMap((element) => {
      const sample = allLineages.filter(lineage => lineage.element === element)
        .sort((a, b) => b.chain.length - a.chain.length)[0];
      return sample ? [{ element, chain: sample.chain.map(petPreview) }] : [];
    }),
  };
}

export declare const data: ReturnType<typeof readHomeCatalog>;

export default defineLoader({
  load: readHomeCatalog,
});
