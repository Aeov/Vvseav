// Shadow study renders: node shadow.js jobs.json   (jobs: [{out, v, L, T, az, alt}])
const { chromium } = require('playwright-core');
const path = require('path');
const fs = require('fs');

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--allow-file-access-from-files'],
  });
  const W = 1600, H = 1020;
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: W, height: H } });
    page.on('pageerror', e => console.log(j.out, 'pageerror:', e.message));
    const q = `?v=${j.v}&view=${j.view || 'plan'}&notrees=1&w=${W}&h=${H}&L=${j.L}` + (j.T ? `&T=${j.T}` : '') + `&sunaz=${j.az}&sunalt=${j.alt}` + (j.extra || '');
    await page.goto('file://' + path.resolve(__dirname, 'scene.html') + q);
    await page.waitForFunction('window.__done === true', null, { timeout: 180000 });
    fs.mkdirSync(path.dirname(j.out), { recursive: true });
    await page.screenshot({ path: j.out });
    console.log('wrote', j.out);
    await page.close();
  }
  await browser.close();
})();
