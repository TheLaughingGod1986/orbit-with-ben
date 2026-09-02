#!/usr/bin/env python3
"""Read-only Studio check: title, description start, Related, no Save."""
from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
PACK = Path(__file__).resolve().parents[1] / (
    "00_Brand/Channel-Setup/audits/vidiq_optimize_2026-09-03/SHORTS_LISTING_UPDATES.json"
)
OUT = Path("/tmp/orbit_shorts_seo_verify.json")
RELATED_WANT = {
    "FbRFvSApfOQ": "NbW5G1BpPY0",
    "eVp9a7f4rWg": "NbW5G1BpPY0",
    "8Bym-yrYhGc": "NbW5G1BpPY0",
    "1glQuYFSaYQ": "NbW5G1BpPY0",
    "Xza_jSHD4qw": "NbW5G1BpPY0",
    "VE0f186WQZo": "NbW5G1BpPY0",
    "D3KSYrqip5A": "NbW5G1BpPY0",
    "TE_HDKAnqms": "NbW5G1BpPY0",
    "92vmMxSNmlk": "Yk1tLh23rko",
    "vCxXTYXSSqY": "Yk1tLh23rko",
    "va5ATScn3rs": "Yk1tLh23rko",
    "o7ykyTDZKiE": "Yk1tLh23rko",
    "Rp_8J6_6IIk": "Yk1tLh23rko",
    "0j_pgYbCe5E": "REXYxuLOBoI",
}


def read_fields(page) -> dict:
    return page.evaluate(
        """() => {
          const grab = (sel) => {
            const el = document.querySelector(sel);
            return el ? (el.innerText || el.textContent || '').trim() : '';
          };
          let title = '';
          let desc = '';
          const walk = (root) => {
            if (!root) return;
            for (const el of root.querySelectorAll('div[contenteditable=true],#textbox,ytcp-social-suggestions-textbox,ytcp-mention-textbox')) {
              const al = (el.getAttribute('aria-label') || '').toLowerCase();
              const t = (el.innerText || el.textContent || '').trim();
              if (!t) continue;
              if (al.includes('title') && !title) title = t.split('\\n')[0];
              if ((al.includes('tell viewers') || al.includes('description')) && !desc) desc = t.slice(0, 220);
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          walk(document);
          const body = (document.body && document.body.innerText) ? document.body.innerText : '';
          const compact = body.replace(/\\s+/g, ' ');
          return {
            title,
            desc,
            has_related_label: /Related video/i.test(compact),
            mentions_europa_long: /Could Life Exist Under The Ice Of Europa/i.test(compact),
            mentions_neutron_long: /What Happens to Your Body Near a Neutron Star/i.test(compact),
            mentions_last_star: /When the Last Star Dies|Last Star/i.test(compact),
            has_go_link: /\\/go\\//.test(compact),
            made_for_kids_no: /not made for kids/i.test(compact),
          };
        }"""
    )


def main() -> int:
    pack = json.loads(PACK.read_text())
    rows = {s["id"]: s for s in pack["shorts"]}
    report = {"videos": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        for vid, want in RELATED_WANT.items():
            page = ctx.new_page()
            page.goto(
                f"https://studio.youtube.com/video/{vid}/edit",
                wait_until="domcontentloaded",
                timeout=90000,
            )
            page.wait_for_timeout(2600)
            fields = read_fields(page)
            expected = rows[vid]["title"]
            title_ok = expected.lower() in (fields.get("title") or "").lower()
            desc_ok = (rows[vid]["description"].split("\n")[0][:40].lower() in (fields.get("desc") or "").lower())
            related_ok = False
            if want == "NbW5G1BpPY0":
                related_ok = bool(fields.get("mentions_europa_long"))
            elif want == "Yk1tLh23rko":
                related_ok = bool(fields.get("mentions_neutron_long"))
            elif want == "REXYxuLOBoI":
                related_ok = bool(fields.get("mentions_last_star"))
            item = {
                "id": vid,
                "expected_title": expected,
                "title_ok": title_ok,
                "desc_ok": desc_ok,
                "related_ok": related_ok,
                "has_go_link": fields.get("has_go_link"),
                "fields": fields,
            }
            report["videos"].append(item)
            print(
                json.dumps(
                    {
                        "id": vid,
                        "title_ok": title_ok,
                        "desc_ok": desc_ok,
                        "related_ok": related_ok,
                        "title": (fields.get("title") or "")[:80],
                    }
                ),
                flush=True,
            )
            page.close()
    report["all_titles"] = all(v["title_ok"] for v in report["videos"])
    report["all_desc"] = all(v["desc_ok"] for v in report["videos"])
    report["all_related"] = all(v["related_ok"] for v in report["videos"])
    report["any_go"] = any(v["has_go_link"] for v in report["videos"])
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report[k] for k in ("all_titles", "all_desc", "all_related", "any_go")}, indent=2))
    return 0 if report["all_titles"] and report["all_desc"] and report["all_related"] and not report["any_go"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
