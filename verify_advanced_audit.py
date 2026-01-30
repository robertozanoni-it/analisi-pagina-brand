
import asyncio
from playwright.async_api import async_playwright
import os

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load the local index.html
        path = os.path.abspath("index.html")
        await page.goto(f"file://{path}")

        # 1. Check if the initial UI is correct
        await page.wait_for_selector("#brandName")
        print("Page loaded successfully.")

        # 2. Switch to HTML/Text mode
        await page.click("label[for='modeHtml']")
        await page.fill("#brandText", "Siamo i leader dell'innovazione. Contattaci subito per una consulenza professionale. Testimonianze: il 99% dei clienti è soddisfatto.")
        await page.fill("#posStatement", "E-commerce fashion che vogliono crescere.")
        await page.fill("#values", "Trasparenza, Performance")

        # 3. Run Audit
        await page.click("#runHtml")

        # 4. Verify Report Sections
        await page.wait_for_selector("#sections .item")
        sections = await page.query_selector_all("#sections .item")
        print(f"Found {len(sections)} sections in report.")

        if len(sections) == 13:
            print("SUCCESS: Found exactly 13 sections.")
        else:
            print(f"FAILURE: Found {len(sections)} sections instead of 13.")

        # 5. Check Section Content structure
        first_section = sections[0]
        title = await first_section.query_selector("b")
        title_text = await title.inner_text()
        print(f"First section title: {title_text}")

        analysis_header = await first_section.query_selector("text='Analisi (Cosa c’è e cosa manca)'")
        if analysis_header:
            print("SUCCESS: 'Analisi' header found.")
        else:
            print("FAILURE: 'Analisi' header NOT found.")

        # 6. Check if 'Copia Prompt AI' button is visible
        copy_btn = await page.query_selector("#btnCopyPrompt")
        is_visible = await copy_btn.is_visible()
        if is_visible:
            print("SUCCESS: 'Copia Prompt AI' button is visible.")
        else:
            print("FAILURE: 'Copia Prompt AI' button is NOT visible.")

        # Take a screenshot
        await page.screenshot(path="verification_advanced.png", full_page=True)
        print("Screenshot saved to verification_advanced.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
