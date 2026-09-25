#!/usr/bin/env python3
"""Post + pin Full Film CTA on one Short via Chrome CDP (:9222).

Usage:
  /tmp/pwvenv/bin/python 00_Brand/Channel-Setup/audits/_pin_one_short_fullfilm_cta.py \\
    --video-id DN4L1DkerMM \\
    --long-id REXYxuLOBoI \\
    --long-title "What Happens When the Last Star Dies?"
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / "00_Brand/Channel-Setup/audits/pin_fullfilm_cta"
LONDON = ZoneInfo("Europe/London")
NEEDLE = "Full film here"
CDP = "http://127.0.0.1:9222"


def build_comment(long_title: str, long_id: str) -> str:
    return (
        f"Full film here → {long_title}\n"
        f"https://youtu.be/{long_id}\n\n"
        "Orbit's Cosmic Journey"
    )


def ensure_orbit_studio(page) -> str | None:
    page.goto("https://studio.youtube.com/", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(2500)
    body = page.locator("body").inner_text()[:800]
    if "Orbit with Ben" in body:
        return "already"
    try:
        page.locator("button#avatar-btn, #avatar-btn, ytcp-avatar").first.click(timeout=3000)
        page.wait_for_timeout(800)
        page.evaluate(
            """() => {
              for (const n of document.querySelectorAll('*')) {
                const t=(n.innerText||'');
                if (t.includes('Orbit with Ben') && t.length<120) {
                  const r=n.getBoundingClientRect();
                  if (r.width>40 && r.height>10 && r.height<100) { n.click(); return t.slice(0,80); }
                }
              }
              return null;
            }"""
        )
        page.wait_for_timeout(2500)
    except Exception:
        pass
    return "switched" if "Orbit" in page.locator("body").inner_text()[:500] else None


def post_and_pin(page, video_id: str, comment: str) -> dict:
    out: dict = {"video_id": video_id}
    page.goto(
        f"https://www.youtube.com/watch?v={video_id}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.evaluate("window.scrollTo(0, Math.min(document.body.scrollHeight, 1400))")
    page.wait_for_timeout(1200)
    body0 = page.locator("body").inner_text()
    out["has_comment_already"] = NEEDLE in body0

    if not out["has_comment_already"]:
        placed = False
        for sel in (
            "#simplebox-placeholder",
            "#placeholder-area",
            "ytd-commentbox #simplebox-placeholder",
            "#contenteditable-root",
        ):
            try:
                loc = page.locator(sel).first
                if loc.count():
                    loc.click(force=True, timeout=2000)
                    page.wait_for_timeout(400)
                    placed = True
                    break
            except Exception:
                continue
        out["box"] = placed
        if placed:
            page.keyboard.type(comment, delay=8)
            page.wait_for_timeout(400)
            out["comment_click"] = page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button, yt-button-shape button')) {
                    const t=(b.innerText||'').trim();
                    if (/^Comment$/i.test(t)) { b.click(); return t; }
                  }
                  return null;
                }"""
            )
            page.wait_for_timeout(2800)

    page.goto(
        f"https://studio.youtube.com/video/{video_id}/comments",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"{video_id}_studio.png"), full_page=False)
    studio_text = page.locator("body").inner_text()
    out["studio_has_needle"] = NEEDLE in studio_text

    if not out.get("has_comment_already") and not out.get("studio_has_needle"):
        try:
            page.get_by_text(re.compile(r"Add a comment|Comment as", re.I)).first.click(timeout=3000)
            page.wait_for_timeout(500)
            page.keyboard.type(comment, delay=8)
            page.wait_for_timeout(300)
            page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button, ytcp-button')) {
                    const t=(b.innerText||'').trim();
                    if (/^Comment$/i.test(t)) { b.click(); return t; }
                  }
                }"""
            )
            page.wait_for_timeout(2500)
            studio_text = page.locator("body").inner_text()
            out["studio_has_needle"] = NEEDLE in studio_text
        except Exception as e:
            out["studio_post_err"] = str(e)[:200]

    if out.get("has_comment_already") or out.get("studio_has_needle"):
        page.evaluate(
            """(needle) => {
              const all=[...document.querySelectorAll('*')];
              let target=null;
              for (const el of all) {
                const t=(el.innerText||'');
                if (t.includes(needle) && t.length<900) {
                  const r=el.getBoundingClientRect();
                  if (r.width>80 && r.height>18) { target=el; break; }
                }
              }
              if (!target) return 'no';
              let row=target;
              for (let i=0;i<10 && row;i++) {
                for (const b of row.querySelectorAll('button, ytcp-icon-button, [aria-label]')) {
                  const al=(b.getAttribute('aria-label')||'')+(b.innerText||'');
                  if (/more|action|options|menu/i.test(al)) { b.click(); return 'menu'; }
                }
                row=row.parentElement;
              }
              return 'fail';
            }""",
            NEEDLE,
        )
        page.wait_for_timeout(700)
        pinned = page.evaluate(
            """() => {
              for (const n of document.querySelectorAll('*')) {
                const t=(n.innerText||'').trim();
                if (/^Pin( comment)?$/i.test(t)) {
                  const r=n.getBoundingClientRect();
                  if (r.width>10 && r.height>8 && r.height<90) { n.click(); return t; }
                }
              }
              return null;
            }"""
        )
        out["pin_click"] = pinned
        if pinned:
            page.wait_for_timeout(500)
            page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button, ytcp-button')) {
                    const t=(b.innerText||'').trim();
                    if (/^Pin$/i.test(t) || /^Confirm$/i.test(t)) { b.click(); return t; }
                  }
                }"""
            )
            page.wait_for_timeout(1800)
            out["pinned"] = True

    out["ok"] = bool(out.get("pinned") or out.get("studio_has_needle") or out.get("has_comment_already"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video-id", required=True)
    ap.add_argument("--long-id", required=True)
    ap.add_argument("--long-title", required=True)
    ap.add_argument("--cdp", default=CDP)
    args = ap.parse_args()
    comment = build_comment(args.long_title, args.long_id)
    report = {
        "ran_at": datetime.now(LONDON).isoformat(),
        "video_id": args.video_id,
        "long_id": args.long_id,
        "comment": comment,
        "cdp": args.cdp,
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(args.cdp)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        report["orbit"] = ensure_orbit_studio(page)
        report["result"] = post_and_pin(page, args.video_id, comment)
        page.close()
    out_path = AUDIT / f"{args.video_id}_pin_result.json"
    AUDIT.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["result"].get("pinned") or report["result"].get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
