#!/usr/bin/env python3
"""Pin Full Film CTA comments via YouTube Studio (CDP :9222).

Uses Studio comments UI — more reliable than watch-page Shorts layout.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

ROOT = Path("/Users/ben/code/Orbit-YouTube")
OUT = ROOT / "00_Brand/Channel-Setup/audits/PIN_ALL_SHORTS_FULLFILM_CTA.json"
AUDIT = ROOT / "00_Brand/Channel-Setup/audits/pin_fullfilm_cta"
LONDON = ZoneInfo("Europe/London")
NEEDLE = "Full film here"
CDP = "http://127.0.0.1:9222"

INDEXES = [
    ROOT / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/SHORTS_UPLOAD_INDEX.json",
    ROOT
    / "02_Video-Projects/002_What-Happens-If-You-Fall-Into-A-Black-Hole/10_Shorts/SHORTS_UPLOAD_INDEX.json",
    ROOT
    / "02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds/10_Shorts/SHORTS_UPLOAD_INDEX.json",
]


def long_meta(index: dict) -> tuple[str, str]:
    long_id = (
        index.get("long_id")
        or index.get("related_to_long")
        or (index.get("shorts") or [{}])[0].get("related")
        or ""
    )
    long_url = index.get("long_url") or index.get("long_placeholder") or ""
    if not long_url and long_id:
        long_url = f"https://youtu.be/{long_id}"
    title = index.get("long_title") or "the full documentary"
    return long_url, title


def load_targets() -> list[dict]:
    targets: list[dict] = []
    for path in INDEXES:
        index = json.loads(path.read_text())
        long_url, long_title = long_meta(index)
        for short in index.get("shorts") or []:
            vid = (short.get("video_id") or "").strip()
            if not vid:
                continue
            targets.append(
                {
                    "video_id": vid,
                    "title": short.get("title"),
                    "short_id": short.get("id"),
                    "comment": (
                        f"Full film here → {long_title}\n"
                        f"{long_url}\n\n"
                        "Orbit's Cosmic Journey 🚀"
                    ),
                    "long_url": long_url,
                }
            )
    return targets


def mark_index(video_id: str, pinned: bool) -> None:
    for path in INDEXES:
        data = json.loads(path.read_text())
        changed = False
        for short in data.get("shorts") or []:
            if short.get("video_id") == video_id:
                short["pinned_fullfilm_cta"] = bool(pinned)
                short["pinned_fullfilm_cta_at"] = datetime.now(LONDON).isoformat()
                changed = True
        if changed:
            path.write_text(json.dumps(data, indent=2) + "\n")


def ensure_orbit_studio(page) -> str | None:
    page.goto("https://studio.youtube.com/", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3500)
    # Switch entity if needed
    try:
        page.locator("button#avatar-btn, #avatar-btn, ytcp-avatar").first.click(timeout=3000)
        page.wait_for_timeout(800)
    except Exception:
        pass
    chose = page.evaluate(
        """() => {
          const nodes=[...document.querySelectorAll('*')];
          for (const n of nodes) {
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
    body = page.locator("body").inner_text()[:500]
    return chose or ("orbit" if "Orbit" in body else None)


def post_and_pin_studio(page, video_id: str, comment: str) -> dict:
    out: dict = {"video_id": video_id}
    # Prefer public watch as channel (owner comment), then Studio pin
    page.goto(
        f"https://www.youtube.com/watch?v={video_id}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    # Dismiss dialogs
        try:
        page.keyboard.press("Escape")
    except Exception:
        pass

    # Expand description / scroll to comments
    page.evaluate("window.scrollTo(0, Math.min(document.body.scrollHeight, 1400))")
    page.wait_for_timeout(1500)

    body0 = page.locator("body").inner_text()
    out["has_comment_already"] = NEEDLE in body0

    if not out["has_comment_already"]:
        # Switch account to Orbit on watch page
        try:
            page.locator("#avatar-btn").first.click(force=True, timeout=2500)
            page.wait_for_timeout(700)
            page.get_by_text("Switch account", exact=False).first.click(force=True, timeout=2000)
            page.wait_for_timeout(700)
            page.evaluate(
                """() => {
                  for (const n of document.querySelectorAll('*')) {
                    const t=n.innerText||'';
                    if (t.includes('Orbit with Ben') && t.length<100) {
                      const r=n.getBoundingClientRect();
                      if (r.width>50 && r.height>12) { n.click(); return; }
                    }
                  }
                }"""
            )
            page.wait_for_timeout(2500)
            page.goto(
                f"https://www.youtube.com/watch?v={video_id}",
                wait_until="domcontentloaded",
            )
            page.wait_for_timeout(3500)
            page.evaluate("window.scrollTo(0, 1200)")
            page.wait_for_timeout(1200)
        except Exception as e:
            out["switch_err"] = str(e)[:160]

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
            page.keyboard.type(comment, delay=10)
            page.wait_for_timeout(400)
            clicked = page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button, yt-button-shape button')) {
                    const t=(b.innerText||'').trim();
                    if (/^Comment$/i.test(t)) { b.click(); return t; }
                  }
                  return null;
                }"""
            )
            out["comment_click"] = clicked
            page.wait_for_timeout(3000)

    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(3500)
    page.evaluate("window.scrollTo(0, 1200)")
    page.wait_for_timeout(1200)
    body = page.locator("body").inner_text()
    out["has_comment"] = NEEDLE in body

    # Pin via Studio comments (works for scheduled too)
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/comments",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    page.screenshot(path=str(AUDIT / f"{video_id}_studio.png"), full_page=False)

    studio_text = page.locator("body").inner_text()
    out["studio_has_needle"] = NEEDLE in studio_text

    # If no comment yet, try leaving one from studio "Add a comment" if present
    if not out.get("has_comment") and not out.get("studio_has_needle"):
        try:
            page.get_by_text(re.compile(r"Add a comment|Comment as", re.I)).first.click(
                timeout=2500
            )
            page.wait_for_timeout(500)
            page.keyboard.type(comment, delay=10)
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
            out["studio_post_err"] = str(e)[:160]

    if out.get("has_comment") or out.get("studio_has_needle"):
        # Open menu on matching comment
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

    out["ok"] = bool(out.get("has_comment") or out.get("studio_has_needle"))
    return out


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    targets = load_targets()
    report: dict = {
        "ran_at": datetime.now(LONDON).isoformat(),
        "cdp": CDP,
        "count": len(targets),
        "results": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
                report["orbit"] = ensure_orbit_studio(page)

        for i, t in enumerate(targets):
            print(f"[{i+1}/{len(targets)}] {t['video_id']} · {t['title']}", flush=True)
            try:
                row = post_and_pin_studio(page, t["video_id"], t["comment"])
                row["title"] = t["title"]
                mark_index(t["video_id"], bool(row.get("pinned") or row.get("ok")))
            except Exception as e:
                row = {"video_id": t["video_id"], "ok": False, "error": str(e)[:400]}
            report["results"].append(row)
            print(
                f"  → ok={row.get('ok')} pinned={row.get('pinned')} studio={row.get('studio_has_needle')}",
                flush=True,
            )
        try:
            page.close()
        except Exception:
            pass

    report["ok_count"] = sum(1 for r in report["results"] if r.get("ok"))
    report["pinned_count"] = sum(1 for r in report["results"] if r.get("pinned"))
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"ok": report["ok_count"], "pinned": report["pinned_count"]}, indent=2))
    raise SystemExit(0 if report["ok_count"] else 1)


if __name__ == "__main__":
    main()
