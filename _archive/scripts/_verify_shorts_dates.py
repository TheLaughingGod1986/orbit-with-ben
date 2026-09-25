#!/usr/bin/env python3
"""Verify live Shorts dates after thumb apply. Read-only."""
import json
import re
from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
URL = "https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/videos/short"
WANT = {
    "FbRFvSApfOQ", "eVp9a7f4rWg", "8Bym-yrYhGc", "1glQuYFSaYQ", "Xza_jSHD4qw",
    "VE0f186WQZo", "D3KSYrqip5A", "TE_HDKAnqms", "92vmMxSNmlk", "vCxXTYXSSqY",
    "va5ATScn3rs", "o7ykyTDZKiE", "Rp_8J6_6IIk", "0j_pgYbCe5E",
}


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(4500)
        collected = []
        for _ in range(10):
            batch = page.evaluate(
                """() => {
                  const out=[];
                  const walk=(root)=>{
                    for (const el of root.querySelectorAll('ytcp-video-row')) {
                      let text='';
                      try { text = el.innerText || ''; } catch(e) {}
                      let id=null;
                      const find=(n)=>{
                        if (!n) return;
                        if (n.getAttribute) {
                          const href=n.getAttribute('href')||'';
                          const m=href.match(/\\/video\\/([\\w-]{11})\\//);
                          if (m) id=id||m[1];
                        }
                        if (n.shadowRoot) find(n.shadowRoot);
                        if (n.children) for (const c of n.children) find(c);
                      };
                      find(el);
                      out.push({id, text: text.replace(/\\s+/g,' ').trim()});
                    }
                    for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
                  };
                  walk(document);
                  return out;
                }"""
            )
            collected.extend(batch)
            page.mouse.wheel(0, 1600)
            page.wait_for_timeout(500)
        page.screenshot(path="/tmp/studio_shorts_after_v02.png")
        page.close()
    seen = {}
    for r in collected:
        if r.get("id") in WANT and r["id"] not in seen:
            t = r["text"]
            dm = re.search(r"(\d{1,2}\s+\w+\s+2026)", t)
            vis = "Scheduled" if "Scheduled" in t else ("Private" if "Private" in t else None)
            title = t.split("—")[0][:80]
            seen[r["id"]] = {"title": title, "date": dm.group(1) if dm else None, "vis": vis, "raw_tail": t[-80:]}
    print(json.dumps(seen, indent=2))


if __name__ == "__main__":
    main()
