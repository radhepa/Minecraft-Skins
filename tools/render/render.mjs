// Render preview shots of a skin from the pack using headless Chromium.
//
//   node tools/render/render.mjs <identifier> <texture.png> <outDir> [shots.json] [geometry.json]
//
// Each shot is saved as <outDir>/<name>.png with a transparent background.

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch {
  ({ chromium } = require('/opt/node22/lib/node_modules/playwright'));
}

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..');
const [identifier, texture, outDir, shotsFile, geometryFile] = process.argv.slice(2);

const DEFAULT_SHOTS = [
  { name: 'hero', yaw: 28, pitch: 8, poseName: 'idle' },
  { name: 'front', yaw: 0, pitch: 4, poseName: 'idle' },
  { name: 'right', yaw: 90, pitch: 4, poseName: 'idle' },
  { name: 'back', yaw: 180, pitch: 4, poseName: 'idle' },
  { name: 'left', yaw: 270, pitch: 4, poseName: 'idle' },
  { name: 'back34', yaw: 210, pitch: 12, poseName: 'idle' },
  { name: 'walk', yaw: -32, pitch: 6, poseName: 'walk' },
  { name: 'wave', yaw: 20, pitch: 6, poseName: 'wave' },
  { name: 'top', yaw: 25, pitch: 55, poseName: 'idle', dist: 100 },
  { name: 'shoes', yaw: 35, pitch: 18, poseName: 'idle', dist: 34, target: 4, fov: 30 },
  { name: 'face', yaw: 22, pitch: 10, poseName: 'idle', dist: 40, target: 27, fov: 30 },
];
const shots = shotsFile && shotsFile !== '-' ? JSON.parse(fs.readFileSync(shotsFile, 'utf8')) : DEFAULT_SHOTS;

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png' };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  const file = p.startsWith('/node_modules/') ? path.join(HERE, p) : path.join(ROOT, p);
  if (!file.startsWith(ROOT) || !fs.existsSync(file)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}`;

const W = 900, H = 1200;
const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await browser.newPage({ viewport: { width: W, height: H } });
page.on('console', m => { if (m.type() === 'error') console.error('page:', m.text()); });
await page.goto(`${base}/tools/render/viewer.html`);
await page.waitForFunction(() => window.ready === true);
const texRel = '/' + path.relative(ROOT, path.resolve(texture)).split(path.sep).join('/');
const geoRel = '/' + path.relative(ROOT, path.resolve(geometryFile || 'MidnightMischief/geometry.json'))
  .split(path.sep).join('/');
await page.evaluate(([w, h, g, t, id]) => window.preview.init(w, h, g, t, id),
  [W, H, geoRel, texRel, identifier]);

fs.mkdirSync(outDir, { recursive: true });
for (const shot of shots) {
  const url = await page.evaluate(s => window.preview.render(s), shot);
  fs.writeFileSync(path.join(outDir, `${shot.name}.png`), Buffer.from(url.split(',')[1], 'base64'));
  console.log('rendered', shot.name);
}
await browser.close();
server.close();
