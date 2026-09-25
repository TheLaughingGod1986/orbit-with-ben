#!/usr/bin/env python3
"""Scrape Studio Shorts rows with date + visibility from ytcp-video-row."""
from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
OUT = Path("/tmp/studio_shorts_rows.json")
URL = "https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/videos/short"


JS = r"""() => {
  const rows = [];
  const walkRows = (root) => {
    const list = root.querySelectorAll ? root.querySelectorAll('ytcp-video-row') : [];
    for (const row of list) {
      const rec = {id: null, title: '', vis: '', date: '', raw: ''};
      const walk = (n) => {
        if (!n) return;
        if (n.shadowRoot) walk(n.shadowRoot);
        if (n.querySelectorAll) {
          for (const a of n.querySelectorAll('a[href*="/video/"]')) {
            const href = a.getAttribute('href') || '';
            const m = href.match(/\/video\/([\w-]{11})\//);
            if (m) rec.id = rec.id || m[1];
          }
        }
        if (n.children) for (const c of n.children) walk(c);
      };
      walk(row);
      try { rec.raw = (row.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 400); } catch (e) {}
      rows.push(rec);
    }
    for (const el of (root.querySelectorAll ? root.querySelectorAll('*') : [])) {
      if (el.shadowRoot) walkRows(el.shadowRoot);
    }
  };
  walkRows(document);
  // Dedup
  const seen = new Set();
  const out = [];
  for (const r of rows) {
    const k = r.id || r.raw.slice(0, 40);
    if (seen.has(k)) continue;
    seen.add(k);
    out.push(r);
  }
  return out;
}"""

JS2 = r"""() => {
  const out = [];
  const collect = (root) => {
    const nodes = root.querySelectorAll ? [...root.querySelectorAll('*')] : [];
    for (const el of nodes) {
      const tag = (el.tagName || '').toLowerCase();
      if (tag === 'ytcp-video-row') {
        let text = '';
        try { text = el.innerText || ''; } catch (e) {}
        out.push({tag, text: text.replace(/\s+/g, ' | ').slice(0, 500)});
      }
      if (el.shadowRoot) collect(el.shadowRoot);
    }
  };
  collect(document);
  return out;
}"""


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(4500)
        collected = []
        for i in range(8):
            batch = page.evaluate(JS2)
            collected.extend(batch)
            page.mouse.wheel(0, 1400)
            page.wait_for_timeout(600)
        # Search neutron unpublished
        page.goto(
            "https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/videos/search?query=neutron",
            wait_until="domcontentloaded",
            timeout=90000,
        )
        page.wait_for_timeout(4000)
        neutron = page.evaluate(JS2)
        page.goto(
            "https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/videos/search?query=fhJP",
            wait_until="domcontentloaded",
            timeout=90000,
        )
        page.wait_for_timeout(3000)
        fh = page.inner_text("body")[:1500]
        page.screenshot(path="/tmp/studio_search_fhjp.png")
        page.close()

    # unique by first 80 chars
    seen = set()
    uniq = []
    for r in collected:
        k = r.get("text", "")[:90]
        if k in seen:
            continue
        seen.add(k)
        uniq.append(r)
    payload = {"shorts_rows": uniq, "neutron_search": neutron, "fhjp_body": fh}
    OUT.write_text(json.dumps(payload, indent=2))
    print(json.dumps({"n_shorts": len(uniq), "n_neutron": len(neutron)}, indent=2))
    for r in uniq[:40]:
        print(r.get("text", "")[:220])
        print("---")


if __name__ == "__main__":
    main()
