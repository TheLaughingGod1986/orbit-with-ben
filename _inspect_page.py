import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9223")
        context = browser.contexts[0]
        page = context.pages[0]
        
        # Go to Reels composer
        await page.goto("https://business.facebook.com/latest/reels_composer?asset_id=1285932871266399&business_id=1352434763139246")
        await page.wait_for_load_state("networkidle", timeout=15000)
        await asyncio.sleep(3)
        
        # Take screenshot
        await page.screenshot(path="/tmp/reels_composer.png", full_page=True)
        print("Screenshot saved to /tmp/reels_composer.png")
        
        # List all visible buttons and inputs
        print("\n=== Buttons on page ===")
        buttons = await page.locator('button, div[role="button"]').all()
        for i, btn in enumerate(buttons[:20]):
            try:
                if await btn.is_visible():
                    text = await btn.inner_text()
                    aria = await btn.get_attribute("aria-label")
                    print(f"{i}: text='{text[:50]}' aria-label='{aria}'")
            except:
                pass
        
        print("\n=== File inputs on page ===")
        inputs = await page.locator('input[type="file"]').all()
        print(f"Found {len(inputs)} file inputs")
        for i, inp in enumerate(inputs):
            try:
                visible = await inp.is_visible()
                name = await inp.get_attribute("name")
                accept = await inp.get_attribute("accept")
                print(f"{i}: visible={visible} name='{name}' accept='{accept}'")
            except:
                pass

asyncio.run(main())
