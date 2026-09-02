#!/usr/bin/env python3
"""Set FbRFvSApfOQ time to 20:00 on 3 Sep without reopening the calendar."""
import json
import re
from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
VID = "FbRFvSApfOQ"


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
        # Click the time input by coordinates
        pos = page.evaluate(
            """() => {
              const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]');
              const walk=(root)=>{
                for (const el of root.querySelectorAll('input')) {
                  const r=el.getBoundingClientRect();
                  if (r.width>40 && r.width<160 && /^\\d{1,2}:\\d{2}$/.test(el.value||'')) {
                    el.click();
                    return {x:r.x+r.width/2, y:r.y+r.height/2, v:el.value};
                  }
                }
                for (const el of root.querySelectorAll('*')) {
                  if (el.shadowRoot) { const x=walk(el.shadowRoot); if (x) return x; }
                }
                return null;
              };
              return walk(dlg||document);
            }"""
        )
        print("time pos", pos)
        page.wait_for_timeout(300)
        page.keyboard.press("Meta+a")
        page.wait_for_timeout(150)
        page.keyboard.press("Backspace")
        page.wait_for_timeout(150)
        page.keyboard.type("20:00", delay=80)
        page.wait_for_timeout(500)
        hit = page.evaluate(
            """() => {
              const hits=[];
              const walk=(root)=>{
                for (const el of root.querySelectorAll('tp-yt-paper-item,[role=option],ytcp-ve,div,span')) {
                  const t=(el.innerText||'').trim();
                  if (t==='20:00' || t==='8:00 PM' || t==='20.00') {
                    const r=el.getBoundingClientRect();
                    if (r.width>20 && r.height>8 && r.height<50) hits.push({t, x:r.x+r.width/2, y:r.y+r.height/2, w:r.width, h:r.height});
                  }
                }
                for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
              };
              walk(document);
              return hits;
            }"""
        )
        print("hits", hit)
        if hit:
            page.mouse.click(hit[0]["x"], hit[0]["y"])
            page.wait_for_timeout(400)
        page.keyboard.press("Enter")
        page.wait_for_timeout(400)
        try:
            page.get_by_text("Schedule as public", exact=True).first.click(force=True, timeout=800)
        except Exception:
            pass
        mid = fields(page)
        print("mid", mid)
        page.screenshot(path="/tmp/fbrf_time_filled.png")
        ok = (mid.get("date") or "").startswith("3") and "Sep" in (mid.get("date") or "") and (mid.get("time") or "").startswith("20:00")
        result = {"before": before, "mid": mid, "ok": ok, "saved": False}
        if ok:
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
            page.screenshot(path="/tmp/fbrf_time_verify.png")
        else:
            page.keyboard.press("Escape")
        page.close()
        print(json.dumps(result, indent=2))
        return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
