// Renders the capability statement PDF, the share image and the touch icon.
// Usage: serve the repo root on port 8000 (python3 -m http.server 8000), then: node scripts/render.js
const { chromium } = require('playwright');
const fs = require('fs');
const BASE = process.env.BASE || 'http://localhost:8000';
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`${BASE}/capability-statement.html`, { waitUntil: 'networkidle' });
  await page.emulateMedia({ media: 'print' });
  await page.pdf({ path: 'manifold-capability-statement.pdf', format: 'Letter', printBackground: true, preferCSSPageSize: true, tagged: true });
  const pdf = fs.readFileSync('manifold-capability-statement.pdf', 'latin1');
  const m = pdf.match(/\/Count (\d+)/);
  if (!m || m[1] !== '1') { console.error(`PDF has ${m ? m[1] : '?'} pages; it must be one.`); process.exit(1); }
  const og = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await og.goto(`${BASE}/scripts/og.html`, { waitUntil: 'networkidle' });
  await og.screenshot({ path: 'assets/img/og.png' });
  const icon = await browser.newPage({ viewport: { width: 180, height: 180 }, deviceScaleFactor: 1 });
  await icon.goto(`${BASE}/scripts/icon.html`, { waitUntil: 'networkidle' });
  await icon.screenshot({ path: 'apple-touch-icon.png' });
  await browser.close();
  console.log('rendered: manifold-capability-statement.pdf (1 page), assets/img/og.png, apple-touch-icon.png');
})();
