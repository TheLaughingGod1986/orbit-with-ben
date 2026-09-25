#!/usr/bin/env python3
"""Move eVp9 to Thu 3 Sep 20:00 launch. Leave FbRF at 11:30 upcoming."""
import json
from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
VID = "eVp9a7f4rWg"


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


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.goto(f"https://studio.youtube.com/video/{VID}/edit", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(3200)
        page.evaluate("() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())")
        page.locator("ytcp-video-metadata-visibility").first.click(force=True)
        page.wait_for_timeout(1300)
        before = fields(page)
        print("before", before)
        page.evaluate(
            """() => {
              const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]');
              const walk=(root)=>{
                for (const el of root.querySelectorAll('input')) {
                  const r=el.getBoundingClientRect();
                  if (r.width>40 && r.width<160 && /^\\d{1,2}:\\d{2}$/.test(el.value||'')) {
                    el.click(); return true;
                  }
                }
                for (const el of root.querySelectorAll('*')) if (el.shadowRoot && walk(el.shadowRoot)) return true;
                return false;
              };
              walk(dlg||document);
            }"""
        )
        page.wait_for_timeout(250)
        loc = page.get_by_text("20:00", exact=True)
        n = loc.count()
        print("20:00 count", n)
        clicked = False
        for i in range(n):
            try:
                loc.nth(i).scroll_into_view_if_needed(timeout=1500)
                if loc.nth(i).is_visible():
                    loc.nth(i).click(force=True, timeout=2000)
                    clicked = True
                    break
            except Exception as e:
                print("skip", i, e)
        print("clicked", clicked)
        page.wait_for_timeout(400)
        try:
            page.get_by_text("Schedule as public", exact=True).first.click(force=True, timeout=800)
        except Exception:
            pass
        mid = fields(page)
        print("mid", mid)
        page.screenshot(path="/tmp/evp9_2000_filled.png")
        ok = "3" in (mid.get("date") or "") and "Sep" in (mid.get("date") or "") and (mid.get("time") or "").startswith("20:00")
        result = {"before": before, "mid": mid, "ok": ok, "saved": False}
        if not ok:
            page.keyboard.press("Escape")
            print(json.dumps(result, indent=2))
            page.close()
            return 1
        btn = page.get_by_role("button", name="Done", exact=True)
        if btn.count():
            (btn.last if btn.count() > 1 else btn.first).click(force=True)
            page.wait_for_timeout(1200)
        sb = page.get_by_role("button", name="Save", exact=True)
        if sb.count() and sb.first.is_enabled():
            sb.first.click(force=True)
            page.wait_for_timeout(3200)
            result["saved"] = True
        page.goto(f"https://studio.youtube.com/video/{VID}/edit", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(3000)
        page.locator("ytcp-video-metadata-visibility").first.click(force=True)
        page.wait_for_timeout(1300)
        result["verify"] = fields(page)
        result["ok"] = (result["verify"].get("time") or "").startswith("20:00") and "3" in (result["verify"].get("date") or "")
        page.screenshot(path="/tmp/evp9_2000_verify.png")
        page.close()
        print(json.dumps(result, indent=2))
        return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
