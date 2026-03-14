import asyncio
from playwright.async_api import async_playwright
import os
import subprocess
import time

async def run():
    # Start server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8001"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 720})

        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"PAGE ERROR: {exc}"))

        await page.goto("http://localhost:8001/")

        # Wait for the app to load and discover assets
        await asyncio.sleep(5)

        # 1. Media Tab Screenshot
        await page.screenshot(path="media_tab_verify.png")
        print("Captured media_tab_verify.png")

        # 2. Switch to Timeline Tab
        await page.get_by_role("button", name="Таймлайн").click()
        await asyncio.sleep(1)
        await page.screenshot(path="timeline_tab_verify.png")
        print("Captured timeline_tab_verify.png")

        # 3. Switch to Logo Tab
        await page.get_by_role("button", name="Лого (Z)").click()
        await asyncio.sleep(1)
        await page.screenshot(path="logo_tab_verify.png")
        print("Captured logo_tab_verify.png")

        # 4. Hide Settings to see Canvas
        await page.keyboard.press("q")
        await asyncio.sleep(2)
        await page.screenshot(path="canvas_content_verify.png")
        print("Captured canvas_content_verify.png")

        # 5. Check for 404s or errors in discovered assets
        images = await page.evaluate("""() => {
            return Array.from(document.querySelectorAll('img')).map(img => ({
                src: img.src,
                naturalWidth: img.naturalWidth,
                complete: img.complete
            }));
        }""")
        for img in images:
            if img['complete'] and img['naturalWidth'] == 0:
                print(f"ERROR: Image failed to load: {img['src']}")

        await browser.close()

    server_process.terminate()

if __name__ == "__main__":
    asyncio.run(run())
