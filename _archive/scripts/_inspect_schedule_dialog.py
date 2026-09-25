#!/usr/bin/env python3
"""Inspect Studio visibility dialog controls for an already-scheduled Short."""
from playwright.sync_api import sync_playwright

VID = "92vmMxSNmlk"
CDP = "http://127.0.0.1:9222"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.goto(f"https://studio.youtube.com/video/{VID}/edit", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(3500)
        page.evaluate("() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())")
        vis = page.locator("ytcp-video-metadata-visibility")
        print("vis count", vis.count())
        vis.first.scroll_into_view_if_needed()
        vis.first.click(force=True)
        page.wait_for_timeout(1500)
        page.screenshot(path="/tmp/orbit_sched_inspect_01.png")
        info = page.evaluate(
            """() => {
              const out = {dialogs: [], triggers: [], inputs: [], labels: []};
              const walk=(root, depth=0)=>{
                if (depth>25) return;
                for (const el of root.querySelectorAll('*')) {
                  const tag=(el.tagName||'').toLowerCase();
                  const al=el.getAttribute('aria-label')||'';
                  const t=(el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,80);
                  if (tag.includes('dialog') || tag.includes('paper-dialog')) {
                    const r=el.getBoundingClientRect();
                    out.dialogs.push({tag, al, t, w:r.width, h:r.height, vis:r.width>0});
                  }
                  if (tag.includes('dropdown') || tag.includes('date')) {
                    const r=el.getBoundingClientRect();
                    if (r.width>5) out.triggers.push({tag, al, t:t.slice(0,60), w:r.width, h:r.height});
                  }
                  if (tag==='input') {
                    const r=el.getBoundingClientRect();
                    out.inputs.push({al, type:el.type, value:el.value, w:r.width, vis:r.width>0});
                  }
                  if (al && /2026|schedule|date|time|expand|sept|sep/i.test(al) && out.labels.length<40) {
                    const r=el.getBoundingClientRect();
                    if (r.width>4) out.labels.push({al:al.slice(0,120), tag, w:r.width, h:r.height});
                  }
                  if (el.shadowRoot) walk(el.shadowRoot, depth+1);
                }
              };
              walk(document);
              return out;
            }"""
        )
        import json
        print(json.dumps(info, indent=2)[:8000])
        # click expand if present
        page.evaluate(
            """() => {
              const walk=(root)=>{
                for (const el of root.querySelectorAll('*')) {
                  const al=el.getAttribute('aria-label')||'';
                  if (/click to expand/i.test(al) || el.id==='first-container-expand-button') {
                    el.click(); return al||el.id;
                  }
                  if (el.shadowRoot) {
                    const x=walk(el.shadowRoot);
                    if (x) return x;
                  }
                }
                return null;
              };
              return walk(document);
            }"""
        )
        page.wait_for_timeout(1000)
        page.screenshot(path="/tmp/orbit_sched_inspect_02.png")
        info2 = page.evaluate(
            """() => {
              const inputs=[];
              const labels=[];
              const walk=(root)=>{
                for (const el of root.querySelectorAll('*')) {
                  if (el.tagName==='INPUT') {
                    const r=el.getBoundingClientRect();
                    inputs.push({al:el.getAttribute('aria-label'), type:el.type, value:el.value, w:r.width, x:r.x, y:r.y});
                  }
                  const al=el.getAttribute('aria-label')||'';
                  if (al && /2026|September|Sept|October|time|date/i.test(al) && labels.length<50) {
                    const r=el.getBoundingClientRect();
                    if (r.width>5) labels.push({al:al.slice(0,140), w:r.width, h:r.height, x:r.x, y:r.y});
                  }
                  if (el.shadowRoot) walk(el.shadowRoot);
                }
              };
              walk(document);
              return {inputs, labels};
            }"""
        )
        print("AFTER EXPAND")
        print(json.dumps(info2, indent=2)[:9000])
        page.close()


if __name__ == "__main__":
    main()
