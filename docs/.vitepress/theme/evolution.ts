import type { App } from "vue";

export interface EvoPet {
  id: number;
  name: string;
  element: string;
  type: string;
  evolveIllegal: string;
  evolveNormal: string;
  image: { file: string; ossKey: string; url: string } | null;
}

export interface Lineage {
  element: string;
  chain: EvoPet[];
}

export function computeLineages(pets: EvoPet[], element?: string): Lineage[] {
  const byName = new Map(pets.map((p) => [p.name, p]));
  const evolvedInto = new Set<string>();
  for (const p of pets) {
    if (p.evolveNormal) evolvedInto.add(p.evolveNormal);
    if (p.evolveIllegal) evolvedInto.add(p.evolveIllegal);
  }
  const roots = pets.filter(
    (p) => (!element || p.element === element) && p.evolveNormal && !evolvedInto.has(p.name)
  );
  const lineages: Lineage[] = [];
  for (const r of roots) {
    const chain: EvoPet[] = [];
    const seen = new Set<string>();
    let cur: EvoPet | undefined = r;
    while (cur && !seen.has(cur.name)) {
      chain.push(cur);
      seen.add(cur.name);
      cur = cur.evolveNormal ? byName.get(cur.evolveNormal) : undefined;
    }
    if (chain.length >= 2) lineages.push({ element: r.element, chain });
  }
  return lineages;
}

export function evoImgUrl(p: EvoPet): string | null {
  if (!p.image) return null;
  return import.meta.env.DEV ? `/hl-assets/${p.image.ossKey}` : p.image.url;
}

export const EVO_ELEMENTS: Record<string, { label: string; color: string }> = {
  metal: { label: "金", color: "#d4af37" },
  wood: { label: "木", color: "#5cae7d" },
  water: { label: "水", color: "#5b9bd5" },
  fire: { label: "火", color: "#e0664f" },
  earth: { label: "土", color: "#c4875a" },
};

export function install(app: App, _opts?: unknown) {
  void app;
}
