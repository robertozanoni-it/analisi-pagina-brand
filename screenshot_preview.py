import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 2000})
        await page.goto('http://localhost:3000')
        await asyncio.sleep(1)

        # Switch to HTML mode first
        await page.click('label[for="modeHtml"]')
        await asyncio.sleep(0.5)

        # Now fill
        await page.fill('#brandName', 'Brand Test')
        await page.fill('#brandText', 'Questo è un testo di prova per il brand che parla di innovazione e qualità. Abbiamo recensioni ottime e siamo leader di mercato.')

        await page.click('#runHtml')
        await asyncio.sleep(1)
        await page.screenshot(path='preview.png', full_page=True)
        await browser.close()

asyncio.run(main())
