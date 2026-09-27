#!/usr/bin/env python3
"""Delete leftover TikTok v01 / duplicate scheduled posts after v02 replace.

Matches content-list rows by needle (title fragment) and removes posts that are
NOT the latest Orbit v02 upload for that needle. Uses Chrome CDP :9222.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

ROOT = Path("/Users/ben/code/Orbit-YouTube")
SETUP = ROOT / "00_Brand/Channel-Setup/TikTok"
RESULT = SETUP / "TIKTOK_DELETE_DUPES_RESULT.json"
AUDIT = SETUP / "audit" / "tt_delete_dupes"
CONTENT = "https://www.tiktok.com/tiktokstudio/content"
LONDON = ZoneInfo("Europe/London")
CDP = "http://127.0.0.1:9222"

# Keep newest matching row; delete older duplicates for these needles.
NEEDLES = [
    "Fermi Paradox",
    "rude about distance",
    "zoo hypothesis",
    "first alien clue",
    "never come back",
    "wouldn't feel like falling",
    "Time stops",
    "look back",
    "eyes would see",
    "point of no return",
    "glass",
    "diamond",
    "three suns",
    "hottest nights",
    "eyeball",
    "host life",
]


def list_rows(page) -> list[dict]:
    return page.evaluate(
        """() => {
          const rows=[];
          const nodes=[...document.querySelectorAll('[class*="content"], tr, [role="row"], div')];
          const seen=new Set();
          for (const n of nodes) {
            const t=(n.innerText||'').trim();
            if (!t || t.length<8 || t.length>500) continue;
            // Likely a content card/row with a title-ish first line
            const first=t.split('\\n')[0].trim();
            if (first.length<6 || first.length>120) continue;
            const key=first.toLowerCase();
            if (seen.has(key)) continue;
            const r=n.getBoundingClientRect();
            if (r.width<180 || r.height<28 || r.height>420) continue;
            seen.add(key);
            rows.push({title:first, text:t.slice(0,240), y:Math.round(r.y)});
          }
          return rows.slice(0,80);
        }"""
    )


def delete_row_containing(page, needle: str, *, keep_first: bool = True) -> dict:
    """Delete matching rows. If keep_first, skip the topmost match (newest)."""
    out = {"needle": needle, "deleted": [], "kept": None}
    matches = page.evaluate(
        """(needle) => {
          const n=needle.toLowerCase();
          const hits=[];
          const nodes=[...document.querySelectorAll('div, tr, [role="row"]')];
          for (const el of nodes) {
            const t=(el.innerText||'');
            if (!t.toLowerCase().includes(n)) continue;
            const r=el.getBoundingClientRect();
            if (r.width<200 || r.height<40 || r.height>360) continue;
            // Prefer rows that look like content items (have Delete/More)
            const hasMenu=[...el.querySelectorAll('button,[aria-label]')].some(b=>{
              const al=(b.getAttribute('aria-label')||'')+(b.innerText||'');
              return /more|menu|option|delete/i.test(al);
            });
            if (!hasMenu && r.height<60) continue;
            hits.push({
              y: Math.round(r.y),
              h: Math.round(r.height),
              preview: t.slice(0,120).replace(/\\s+/g,' ')
            });
          }
          hits.sort((a,b)=>a.y-b.y);
          // Dedupe near-identical y
          const uniq=[];
          for (const h of hits) {
            if (uniq.some(u=>Math.abs(u.y-h.y)<20)) continue;
            uniq.push(h);
          }
          return uniq;
        }""",
        needle,
    )
    if not matches:
        out["status"] = "no_match"
        return out

    # keep topmost (usually newest scheduled / posted)
    start_i = 1 if keep_first and len(matches) > 1 else (0 if not keep_first else 1)
    if keep_first and len(matches) >= 1:
        out["kept"] = matches[0]
    if len(matches) <= 1 and keep_first:
        out["status"] = "only_one_keep"
        return out

    for hit in matches[start_i:]:
        deleted = page.evaluate(
            """(args) => {
              const needle=args.needle.toLowerCase();
              const y=args.y;
              const nodes=[...document.querySelectorAll('div, tr, [role="row"]')];
              let target=null;
              for (const el of nodes) {
                const t=(el.innerText||'');
                if (!t.toLowerCase().includes(needle)) continue;
                const r=el.getBoundingClientRect();
                if (Math.abs(r.y-y)>24) continue;
                if (r.width<200 || r.height<40) continue;
                target=el; break;
              }
              if (!target) return 'no_target';
              // Open more menu
              const buttons=[...target.querySelectorAll('button,[aria-label],div[role="button"]')];
              let opened=false;
              for (const b of buttons) {
                const al=(b.getAttribute('aria-label')||'')+(b.getAttribute('title')||'')+(b.innerText||'');
                if (/more|menu|option/i.test(al)) { b.click(); opened=true; break; }
              }
              if (!opened) {
                // last icon-ish button in row
                const last=buttons[buttons.length-1];
                if (last) { last.click(); opened=true; }
              }
              return opened ? 'menu' : 'no_menu';
            }""",
            {"needle": needle, "y": hit["y"]},
        )
        page.wait_for_timeout(600)
        clicked = page.evaluate(
            """() => {
              for (const n of document.querySelectorAll('div,button,span,li,[role="menuitem"]')) {
                const t=(n.innerText||'').trim();
                if (/^Delete$/i.test(t) || /^Delete post$/i.test(t)) {
                  const r=n.getBoundingClientRect();
                  if (r.width>20 && r.height>10 && r.height<80) { n.click(); return t; }
                }
              }
              return null;
            }"""
        )
        page.wait_for_timeout(500)
        if clicked:
            page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button,div[role="button"]')) {
                    const t=(b.innerText||'').trim();
                    if (/^Delete$/i.test(t) || /^Confirm$/i.test(t) || /^OK$/i.test(t)) {
                      b.click(); return t;
                    }
                  }
                }"""
            )
            page.wait_for_timeout(1500)
            out["deleted"].append({**hit, "menu": deleted, "click": clicked})
        else:
            # Escape any open menu
            page.keyboard.press("Escape")
            out["deleted"].append({**hit, "menu": deleted, "click": None, "failed": True})
    out["status"] = "done"
    return out


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    report: dict = {"ran_at": datetime.now(LONDON).isoformat(), "results": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(CONTENT, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(4000)
        # Prefer Scheduled tab if present
        try:
            page.get_by_text(re.compile(r"Scheduled", re.I)).first.click(timeout=2500)
            page.wait_for_timeout(2500)
        except Exception:
            pass
        page.screenshot(path=str(AUDIT / "content_before.png"), full_page=False)
        report["rows_sample"] = list_rows(page)[:20]

        for needle in NEEDLES:
            print(f"dupes: {needle}", flush=True)
            res = delete_row_containing(page, needle, keep_first=True)
            report["results"].append(res)
            print(f"  → {res.get('status')} deleted={len(res.get('deleted') or [])}", flush=True)
            page.wait_for_timeout(800)

        # Also scan Posted for obvious v01 leftovers with same needles (keep newest)
        try:
            page.get_by_text(re.compile(r"^Posted$|Posts", re.I)).first.click(timeout=2500)
            page.wait_for_timeout(2500)
        except Exception:
            pass
        for needle in NEEDLES:
            res = delete_row_containing(page, needle, keep_first=True)
            res["tab"] = "posted"
            report["results"].append(res)

        page.screenshot(path=str(AUDIT / "content_after.png"), full_page=False)

    report["deleted_total"] = sum(len(r.get("deleted") or []) for r in report["results"])
    RESULT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"deleted_total": report["deleted_total"]}, indent=2))


if __name__ == "__main__":
    main()
