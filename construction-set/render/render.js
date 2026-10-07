// Render the courtyard roof scene (scene.html) with headless Chromium (software WebGL) to PNGs.
// usage: node render.js [outDir] [versions...]
const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

(async () => {
  const out = path.resolve(process.argv[2] || '../output/Render_C09');
  const versions = process.argv.slice(3).length ? process.argv.slice(3) : ['V1', 'V2', 'V1T', 'V2T'];
  const views = (process.env.VIEWS || 'eye,aerial,under').split(',');
  const lights = (process.env.LIGHTS || 'day').split(',');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--allow-file-access-from-files'],
  });
  const W = 1800, H = 1200;
  for (const v of versions) for (const view of views) for (const light of lights) {
    const page = await browser.newPage({ viewport: { width: W, height: H } });
    page.on('console', m => { if (m.type() === 'error') console.log(v, view, 'console:', m.text()); });
    page.on('pageerror', e => console.log(v, view, 'pageerror:', e.message));
    const url = 'file://' + path.resolve(__dirname, 'scene.html') + `?v=${v}&view=${view}&light=${light}&w=${W}&h=${H}`;
    await page.goto(url);
    await page.waitForFunction('window.__done === true', null, { timeout: 180000 });
    const f = path.join(out, `${v}_${view}_${light}.png`);
    await page.screenshot({ path: f });
    console.log('wrote', f);
    await page.close();
  }
  await browser.close();
})();
