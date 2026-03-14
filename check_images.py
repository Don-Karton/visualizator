import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Start server
        os.system("python3 -m http.server 8000 > server.log 2>&1 &")
        await asyncio.sleep(2)

        # Open the page
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"PAGE ERROR: {exc}"))
        page.on("requestfailed", lambda req: print(f"REQUEST FAILED: {req.url} {req.failure.error_text}"))

        await page.goto("http://localhost:8000/")
        await asyncio.sleep(5) # Wait for assets to load

        # Check if media items are present in mediaQueue
        queue_count = await page.evaluate("() => { try { return document.querySelectorAll('.space-y-2 .flex.items-center.justify-between').length; } catch(e) { return 0; } }")
        print(f"Media queue count: {queue_count}")

        # Check if images are loading (naturalWidth > 0)
        img_stats = await page.evaluate("""() => {
            const imgs = Array.from(document.querySelectorAll('img'));
            return imgs.map(img => ({
                src: img.src,
                loaded: img.naturalWidth > 0,
                visible: img.offsetParent !== null
            }));
        }""")
        print(f"Image stats: {img_stats}")

        # Check for 404s in logs is already handled by requestfailed

        await browser.close()
        os.system("kill $(lsof -t -i :8000)")

asyncio.run(run())
