const assetHost = 'https://cheny-chenyu.oss-cn-chengdu.aliyuncs.com';

export function assetUrl(path: string): string {
  const key = path.replace(/^\/hl-assets\//, '');
  if (!key.startsWith('hl/')) return path;
  const encoded = key.split('/').map(encodeURIComponent).join('/');
  return import.meta.env.DEV ? `/hl-assets/${encoded}` : `${assetHost}/${encoded}`;
}
