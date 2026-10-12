import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9223")
        context = browser.contexts[0]
        page = context.pages[0]
        
        # Go to composer
        await page.goto("https://business.facebook.com/latest/reels_composer?asset_id=1285932871266399&business_id=1352434763139246", wait_until="networkidle")
        await asyncio.sleep(3)
        
        # Get page title
        title = await page.title()
        print(f"Page title: {title}")
        
        # Try to get the Add video button using different methods
        print("\n=== Searching for Add video button ===")
        
        # Method 1: Text content
        result1 = await page.evaluate("""
            () => {
                const elements = Array.from(document.querySelectorAll('*'));
                const found = elements.filter(el => 
                    el.textContent && el.textContent.trim() === 'Add video'
                );
                return found.map(el => ({
                    tag: el.tagName,
                    role: el.getAttribute('role'),
                    ariaLabel: el.getAttribute('aria-label'),
                    className: el.className
                }));
            }
        """)
        print(f"Method 1 (exact text): Found {len(result1)} elements")
        for item in result1:
            print(f"  {item}")
        
        # Method 2: Contains "video"
        result2 = await page.evaluate("""
            () => {
                const elements = Array.from(document.querySelectorAll('button, div[role="button"]'));
                const found = elements.filter(el => 
                    el.textContent && el.textContent.toLowerCase().includes('video')
                );
                return found.slice(0, 5).map(el => ({
                    text: el.textContent.trim().substring(0, 50),
                    tag: el.tagName,
                    role: el.getAttribute('role'),
                    visible: el.offsetParent !== null
                }));
            }
        """)
        print(f"\nMethod 2 (contains 'video'): Found {len(result2)} elements")
        for item in result2:
            print(f"  {item}")
        
        # Check for any modals or overlays
        print("\n=== Checking for modals/overlays ===")
        modals = await page.evaluate("""
            () => {
                const overlays = document.querySelectorAll('[role="dialog"], .modal, [aria-modal="true"]');
                return Array.from(overlays).map(el => ({
                    text: el.textContent.substring(0, 100),
                    visible: el.offsetParent !== null
                }));
            }
        """)
        print(f"Found {len(modals)} modals")
        for m in modals:
            print(f"  {m}")
        
        # Take screenshot
        await page.screenshot(path="/tmp/debug_composer.png", full_page=True)
        print("\n📸 Screenshot saved: /tmp/debug_composer.png")

asyncio.run(main())
