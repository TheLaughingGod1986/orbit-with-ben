#!/usr/bin/env python3
"""Open datepicker via JS click on #datepicker-trigger and dump cell labels."""
import json
from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
VID = "92vmMxSNmlk"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.goto(f"https://studio.youtube.com/video/{VID}/edit", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(3200)
        page.evaluate("() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())")
        page.locator("ytcp-video-metadata-visibility").first.click(force=True)
        page.wait_for_timeout(1400)
        page.screenshot(path="/tmp/cal_before.png")
        clicked = page.evaluate(
            """() => {
              const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]');
              const info={clicked:null, triggers:[]};
              const walk=(root)=>{
                for (const el of root.querySelectorAll('ytcp-text-dropdown-trigger, #datepicker-trigger')) {
                  const r=el.getBoundingClientRect();
                  const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                  info.triggers.push({id:el.id, t, w:Math.round(r.width), h:Math.round(r.height), x:Math.round(r.x), y:Math.round(r.y)});
                }
                for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
              };
              walk(dlg||document);
              const vis = info.triggers.filter(t => t.w>50 && t.h>20 && /\\d/.test(t.t));
              const tgt = vis[0] || info.triggers.find(t => t.id==='datepicker-trigger');
              if (!tgt) return info;
              const walk2=(root)=>{
                for (const el of root.querySelectorAll('ytcp-text-dropdown-trigger, #datepicker-trigger')) {
                  const r=el.getBoundingClientRect();
                  if (Math.round(r.x)===tgt.x && Math.round(r.y)===tgt.y) { el.click(); info.clicked=tgt; return true; }
                  if (el.id==='datepicker-trigger' && !info.clicked) { el.click(); info.clicked={id:el.id, via:'id'}; return true; }
                }
                for (const el of root.querySelectorAll('*')) if (el.shadowRoot && walk2(el.shadowRoot)) return true;
                return false;
              };
              walk2(dlg||document);
              return info;
            }"""
        )
        page.wait_for_timeout(900)
        page.screenshot(path="/tmp/cal_open.png")
        labels = page.evaluate(
            """() => {
              const labs=[];
              const walk=(root)=>{
                for (const el of root.querySelectorAll('[aria-label]')) {
                  const al=el.getAttribute('aria-label')||'';
                  const r=el.getBoundingClientRect();
                  if (r.width>8 && r.height>8 && /\\d/.test(al)) {
                    labs.push({al:al.slice(0,180), w:Math.round(r.width), h:Math.round(r.height), x:Math.round(r.x), y:Math.round(r.y)});
                  }
                }
                for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
              };
              walk(document);
              return labs.slice(0, 100);
            }"""
        )
        print(json.dumps({"clicked": clicked, "n_labels": len(labels), "labels": labels}, indent=2)[:14000])
        page.keyboard.press("Escape")
        page.keyboard.press("Escape")
        page.close()


if __name__ == "__main__":
    main()
