/** Rates transcribed from columns J and K of 重塑宠物价格.xlsx, 幻兽价格. */
export const petRechargeTiers = [
  { amount: 50, yuanPerStone: 0.03623 },
  { amount: 10, yuanPerStone: 1 / 27 },
] as const;

const yuanFormat = new Intl.NumberFormat("zh-CN", {
  style: "currency",
  currency: "CNY",
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

export function readPetPrice(value: string | number | null | undefined): number | null {
  if (value == null || (typeof value === "string" && value.trim() === "")) return null;
  const amount = Number(value);
  return Number.isFinite(amount) && amount >= 0 ? amount : null;
}

export function formatPetPriceYuan(value: string | number | null | undefined): string {
  const amount = readPetPrice(value);
  return amount == null ? "—" : yuanFormat.format(amount);
}
