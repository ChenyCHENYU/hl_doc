/**
 * OSS 批量上传工具（零依赖，仅需 Node.js）
 * 与 jh-agileteam-doc 同一 bucket：cheny-chenyu / oss-cn-chengdu
 *
 * 用法:
 *   OSS_AK_ID=xxx OSS_AK_SECRET=xxx \
 *   node scripts/upload-oss.mjs \
 *     --source assets/hl/pets \
 *     --target hl/pets
 *
 * 参数:
 *   --source   本地图片目录（必需，相对路径基于项目根）
 *   --target   OSS 目标路径前缀，如 hl/pets（必需）
 *   --bucket   OSS Bucket 名（默认 cheny-chenyu）
 *   --region   OSS 区域（默认 oss-cn-chengdu）
 *   --domain   自定义域名前缀（可选）
 *   --dry-run  只输出计划不上传
 *
 * 环境变量:
 *   OSS_AK_ID / OSS_AK_SECRET   阿里云 AccessKey（必需，dry-run 除外）
 *
 * 输出: upload-result.json（相对路径→URL 映射表）
 * 目录约定（hl/ 专目录）:
 *   hl/pets/{metal,wood,water,fire,earth,shop,forge}  宠物图鉴图
 *   hl/monsters  怪物手册图    hl/items  物品图
 *   hl/charts    玩法图表      hl/heroes 玩家头像    hl/misc 其他
 */

import { readdirSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join, extname } from 'node:path';
import { createHmac } from 'node:crypto';
import { request } from 'node:https';

const args = process.argv.slice(2);
const get = (key, def) => {
  const i = args.indexOf(`--${key}`);
  return i >= 0 ? args[i + 1] : def;
};

const SOURCE = get('source');
const TARGET = get('target');
const BUCKET = get('bucket', 'cheny-chenyu');
const REGION = get('region', 'oss-cn-chengdu');
const DOMAIN = get('domain', '');
const DRY_RUN = args.includes('--dry-run');

const AK_ID = process.env.OSS_AK_ID;
const AK_SECRET = process.env.OSS_AK_SECRET;

if (!SOURCE || !TARGET) {
  console.error('用法: node scripts/upload-oss.mjs --source <目录> --target <hl/...前缀>');
  process.exit(1);
}
if (!DRY_RUN && (!AK_ID || !AK_SECRET)) {
  console.error('需要环境变量 OSS_AK_ID 和 OSS_AK_SECRET');
  process.exit(1);
}

const MIME = {
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
};

function uploadFile(key, filePath, contentType) {
  return new Promise((resolve, reject) => {
    const body = readFileSync(filePath);
    const date = new Date().toUTCString();

    const stringToSign = `PUT\n\n${contentType}\n${date}\n/${BUCKET}/${key}`;
    const signature = createHmac('sha1', AK_SECRET)
      .update(stringToSign)
      .digest('base64');

    const host = `${BUCKET}.${REGION}.aliyuncs.com`;
    const options = {
      hostname: host,
      path: '/' + encodeURI(key),
      method: 'PUT',
      headers: {
        'Content-Type': contentType,
        'Date': date,
        'Authorization': `OSS ${AK_ID}:${signature}`,
        'Content-Length': body.length,
      },
    };

    const req = request(options, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        if (res.statusCode === 200) {
          const url = DOMAIN
            ? `${DOMAIN.replace(/\/$/, '')}/${key}`
            : `https://${host}/${key}`;
          resolve({ ok: true, url, size: body.length });
        } else {
          reject(
            new Error(`HTTP ${res.statusCode}: ${Buffer.concat(chunks).toString().slice(0, 200)}`)
          );
        }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

function scanImages(dir, base = '') {
  const results = [];
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const rel = base ? `${base}/${entry}` : entry;
    if (statSync(full).isDirectory()) {
      results.push(...scanImages(full, rel));
    } else if (MIME[extname(entry).toLowerCase()]) {
      results.push({ local: full, rel });
    }
  }
  return results;
}

async function main() {
  const images = scanImages(SOURCE);
  console.log(`找到 ${images.length} 张图片`);
  console.log(`目标: ${BUCKET}/${TARGET}/`);
  console.log(DRY_RUN ? '（dry-run 模式，不上传）\n' : '\n');

  const result = {};

  for (let i = 0; i < images.length; i++) {
    const img = images[i];
    const key = `${TARGET}/${img.rel}`.replace(/\\/g, '/');
    const mime = MIME[extname(img.local).toLowerCase()];

    if (DRY_RUN) {
      const size = (statSync(img.local).size / 1024).toFixed(0);
      console.log(`  [${i + 1}/${images.length}] ${img.rel} (${size}KB) → ${key}`);
      result[img.rel] = `https://${BUCKET}.${REGION}.aliyuncs.com/${key}`;
      continue;
    }

    try {
      const res = await uploadFile(key, img.local, mime);
      result[img.rel] = res.url;
      const size = (res.size / 1024).toFixed(0);
      console.log(`  [${i + 1}/${images.length}] ✓ ${img.rel} (${size}KB)`);
    } catch (e) {
      console.error(`  [${i + 1}/${images.length}] ✗ ${img.rel}: ${e.message}`);
    }

    if (!DRY_RUN && i < images.length - 1) {
      await new Promise((r) => setTimeout(r, 50));
    }
  }

  const outPath = join(process.cwd(), 'upload-result.json');
  writeFileSync(outPath, JSON.stringify(result, null, 2), 'utf-8');
  console.log(`\n完成: ${Object.keys(result).length} 张处理成功`);
  console.log(`映射表: ${outPath}`);
}

main().catch((e) => {
  console.error('执行失败:', e);
  process.exit(1);
});
