# 幻灵宝典 · Vercel 部署清单

> 站点：VitePress 2.0-alpha.20 · 构建命令 `pnpm build` · 输出目录 `docs/.vitepress/dist`

## 一、部署站点本体（Vercel）

1. 仓库推到 GitHub（本目录 `huanling-wiki` 作为仓库根；若放在 monorepo 子目录，Vercel 项目里把 **Root Directory** 设为 `huanling-wiki`）
2. Vercel → New Project → 导入仓库，设置：
   - Framework Preset: **VitePress**（或 Other）
   - Build Command: `pnpm build`
   - Output Directory: `docs/.vitepress/dist`
   - Install Command: `pnpm install --frozen-lockfile`
3. 环境变量（Project → Settings → Environment Variables）：

   | 变量 | 说明 |
   |---|---|
   | `TWIKOO_ENV_ID` | Twikoo 服务端地址（见下），如 `https://hl-twikoo-xxx.vercel.app` |
   | `DEPLOY_URL` | 正式域名，用于生成 sitemap。未配置时不生成 sitemap |

4. 部署后绑定自定义域名（Settings → Domains）

## 二、评论后端（Twikoo on Vercel，免费）

1. 打开 <https://twikoo.js.org/quick-start.html> → 「Vercel 部署」按钮，一键 Fork 部署 Twikoo Server
2. 免费 MongoDB：注册 <https://www.mongodb.com/atlas> → 建免费集群 → Database Access 建用户 → Network Access 允许 `0.0.0.0/0` → 拿到连接串 `mongodb+srv://user:pass@xxx.mongodb.net/twikoo`
3. Twikoo Server 的 Vercel 项目里设置环境变量 `MONGODB_URI` = 上面的连接串，Redeploy
4. 访问 `https://你的-twikoo-项目.vercel.app` 出现"Twikoo 云端运行正常"即成功
5. 把该地址填入站点项目的 `TWIKOO_ENV_ID` 环境变量，重新部署站点
6. 首次在任意文章页评论框里（昵称/邮箱框）输入你的管理员昵称+邮箱评论后，访问 `https://你的-twikoo-项目.vercel.app` 按提示设置管理密码，即可后台管理（删评论/反垃圾/邮件提醒）

> QQ 玩家体验：评论时邮箱填 QQ 号（如 `123456@qq.com` 或直接数字），头像自动显示 QQ 头像；游客只填昵称即可评论。
> 真·QQ 授权登录（OAuth）需要域名备案 + QQ 互联申请，拿到 appid 后可在 Twikoo 侧扩展，当前方案已覆盖"QQ 身份评论"的实际体验。

## 三、图片 OSS（生产环境必做）

生产环境图片走阿里云 OSS（bucket `cheny-chenyu`，成都区域）：

```bash
OSS_AK_ID=.. OSS_AK_SECRET=.. node scripts/upload-oss.mjs --source assets/hl/pets --target hl/pets
# charts / gallery / misc 同理，先 --dry-run 预览
```

本地 `assets/hl/` 的图片只在 dev/preview 生效；未上传前生产环境为占位提示，不留死图。

## 四、部署前检查

- [ ] `pnpm build` 通过
- [ ] 已为正式部署配置 `DEPLOY_URL`，并核对 sitemap 中的域名
- [ ] Twikoo Server 正常、`TWIKOO_ENV_ID` 已配置（评论区左上角不再显示"本地试用模式"）
- [ ] OSS 三目录（pets/charts/gallery + misc）已上传
- [ ] 关于页联系方式已换成真实邮箱
