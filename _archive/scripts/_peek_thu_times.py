#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import json

CDP = "http://127.0.0.1:9222"
IDS = ["FbRFvSApfOQ", "eVp9a7f4rWg", "92vmMxSNmlk", "D3KSYrqip5A"]


def fields(page):
    return page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]');
          let date=''; let time='';
          const walk=(root)=>{
            for (const el of root.querySelectorAll('#datepicker-trigger, ytcp-text-dropdown-trigger')) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              const r=el.getBoundingClientRect();
              if (r.width>80 && /202\\d/.test(t)) date=t;
            }
            for (const el of root.querySelectorAll('input')) {
              if (/^\\d{1,2}:\\d{2}$/.test(el.value||'')) time=el.value;
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          walk(dlg||document);
          return {date, time};
        }"""
    )


def main():
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        for vid in IDS:
            page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=90000)
            page.wait_for_timeout(2800)
            page.evaluate("() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())")
            page.locator("ytcp-video-metadata-visibility").first.click(force=True)
            page.wait_for_timeout(1100)
            out[vid] = fields(page)
            page.keyboard.press("Escape")
        page.close()
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
