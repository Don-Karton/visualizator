const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`file://${path.join(process.cwd(), 'index.html')}`);
  await page.click('button:has-text("Запустить")');
  await page.keyboard.press('q');

  // Go to Effects
  await page.click('button:has-text("Эффекты")');

  // Verify new Starry Sky labels
  const labels = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('label')).map(l => l.innerText);
  });
  console.log('Labels in Effects tab:', labels);

  const hasGlow = labels.some(l => l.includes('Интенсивность свечения'));
  console.log('Has glow setting:', hasGlow);

  await page.screenshot({ path: '/home/jules/verification/starry_sky_glow.png' });

  // Close and cleanup
  await browser.close();
})();
