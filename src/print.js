// Prints the HTML to an A4 PDF with headless Chromium and runs layout checks.
// usage: node print.js <in.html> <out.pdf>
const path = require('path');
const { chromium } = require(process.env.PW_PATH || '/opt/node22/lib/node_modules/playwright');

(async () => {
  const [inFile, outFile] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(inFile), { waitUntil: 'load' });
  await page.emulateMedia({ media: 'print' });
  await page.evaluate(() => document.fonts.ready);

  // ---- QA: fonts, horizontal overflow, clipped or overlapping text
  const report = await page.evaluate(() => {
    const issues = [];
    const fontOk = document.fonts.check('13pt "Atkinson Hyperlegible"');
    if (!fontOk) issues.push('font not loaded');
    const pageW = document.documentElement.clientWidth;
    document.querySelectorAll('body *').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.width && r.right > pageW + 1) issues.push('overflow-x: ' + el.className + ' ' + (el.textContent || '').slice(0, 40));
      if (el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).overflow !== 'visible')
        issues.push('clipped: ' + el.className);
    });
    // overlapping text lines between sibling cues / captions
    const boxes = [...document.querySelectorAll('.say p, .tag, .pname, .fcap, .scap, .sb, .badge, .nl li, .cmpt td')]
      .map(e => ({ e, r: e.getBoundingClientRect() }));
    for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
      const a = boxes[i].r, b = boxes[j].r;
      if (boxes[i].e.contains(boxes[j].e) || boxes[j].e.contains(boxes[i].e)) continue;
      const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left);
      const oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (ox > 1 && oy > 1) issues.push('overlap: ' + boxes[i].e.textContent.slice(0, 30) + ' | ' + boxes[j].e.textContent.slice(0, 30));
    }
    // svgs overlapping text in strips
    return { fontOk, issues };
  });
  console.log(JSON.stringify(report, null, 1));
  await page.pdf({ path: outFile, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await browser.close();
})();
