// 评论区配置
// 正式模式：设置环境变量 TWIKOO_ENV_ID（Twikoo on Vercel 部署后的地址，如 https://xxx.vercel.app）
// 本地/未配置时自动回退"本地试用模式"
// 部署步骤见项目根 DEPLOY.md
export const TWIKOO_ENV_ID: string = (import.meta.env.TWIKOO_ENV_ID as string) || "";
