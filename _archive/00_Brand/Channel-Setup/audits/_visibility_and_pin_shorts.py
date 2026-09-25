#!/usr/bin/env python3
"""Set Orbit Shorts visibility (Public / Scheduled) then pin Full Film CTAs.

Private videos block comments — publish/schedule first, then comment+pin.
Uses CDP :9222 (Orbit Studio session).
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

ROOT = Path("/Users/ben/code/Orbit-YouTube")
OUT = ROOT / "00_Brand/Channel-Setup/audits/VISIBILITY_AND_PIN_SHORTS.json"
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


def load_targets() -> list[dict]:
    out = []
    for path in INDEXES:
        data = json.loads(path.read_text())
        long_url = data.get("long_url") or data.get("long_placeholder") or ""
        long_title = data.get("long_title") or "the full documentary"
        if not long_url:
            rid = (data.get("shorts") or [{}])[0].get("related")
            if rid:
                long_url = f"https://youtu.be/{rid}"
        for s in data.get("shorts") or []:
            vid = s.get("video_id")
            if not vid:
                continue
            out.append(
                {
                    "video_id": vid,
                    "title": s.get("title"),
                    "visibility": s.get("visibility") or "scheduled",
                    "schedule_iso": s.get("schedule_iso"),
                    "comment": (
                        f"Full film here → {long_title}\n{long_url}\n\n"
                        "Orbit's Cosmic Journey 🚀"
                    ),
                }
            )
    return out


def mark(video_id: str, **fields) -> None:
    for path in INDEXES:
        data = json.loads(path.read_text())
        changed = False
        for s in data.get("shorts") or []:
            if s.get("video_id") == video_id:
                s.update(fields)
                changed = True
        if changed:
            path.write_text(json.dumps(data, indent=2) + "\n")


def set_visibility(page, video_id: str, visibility: str, schedule_iso: str | None) -> dict:
    """Open Studio editor visibility and set Public or keep Scheduled."""
    out = {"visibility_target": visibility}
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    # Click Visibility radio / dropdown
    body = page.locator("body").inner_text()
    out["before_private"] = "Private" in body and "Public" in body

    if visibility == "public":
        clicked = page.evaluate(
            """() => {
              // Prefer radio / tip option labeled Public
              for (const el of document.querySelectorAll('tp-yt-paper-radio-button, yt-radio, [role="radio"], label, div')) {
                const t=(el.innerText||'').trim();
                if (/^Public$/i.test(t) || t.startsWith('Public\\n')) {
                  const r=el.getBoundingClientRect();
                  if (r.width>20 && r.height>10 && r.height<80) { el.click(); return t.slice(0,40); }
                }
              }
              return null;
            }"""
        )
        out["public_click"] = clicked
    else:
        # Scheduled — click Schedule if currently Private
        clicked = page.evaluate(
            """() => {
              for (const el of document.querySelectorAll('tp-yt-paper-radio-button, [role="radio"], label, div, button')) {
                const t=(el.innerText||'').trim();
                if (/^Schedule$/i.test(t) || t.startsWith('Schedule\\n')) {
                  const r=el.getBoundingClientRect();
                  if (r.width>20 && r.height>10 && r.height<90) { el.click(); return t.slice(0,40); }
                }
              }
              return null;
            }"""
        )
        out["schedule_click"] = clicked

    page.wait_for_timeout(800)
    # Save
    saved = page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button, ytcp-button')) {
            const t=(b.innerText||'').trim();
            if (/^Save$/i.test(t) || /^Publish$/i.test(t)) {
              if (!b.disabled) { b.click(); return t; }
            }
          }
          return null;
        }"""
    )
    out["save"] = saved
    page.wait_for_timeout(2500)
    page.screenshot(path=str(AUDIT / f"{video_id}_visibility.png"), full_page=False)
    return out


def post_pin(page, video_id: str, comment: str) -> dict:
    out: dict = {}
    page.goto(f"https://www.youtube.com/shorts/{video_id}", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3500)
    body = page.locator("body").inner_text()
    if "Comments are not supported on private" in body or re.search(
        r"\bPrivate\b", body[:1500]
    ):
        out["blocked_private"] = True
        # Still try watch page after visibility fix may need refresh
    # Open comments
    page.evaluate(
        """() => {
          for (const el of document.querySelectorAll('button,[role="button"]')) {
            const al=(el.getAttribute('aria-label')||'')+(el.innerText||'');
            if (/view comments/i.test(al)) { el.click(); return al; }
          }
        }"""
    )
    page.wait_for_timeout(2000)
    body2 = page.locator("body").inner_text()
    if "not supported on private" in body2:
        out["blocked_private"] = True
        out["ok"] = False
        return out

    if NEEDLE not in body2:
        placed = False
        for sel in ("#simplebox-placeholder", "#placeholder-area", "#contenteditable-root"):
            try:
                loc = page.locator(sel).first
                if loc.count():
                    loc.click(force=True, timeout=2000)
                    placed = True
                    break
            except Exception:
                continue
        out["box"] = placed
        if placed:
            page.keyboard.type(comment, delay=10)
            page.wait_for_timeout(400)
            page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button')) {
                    const t=(b.innerText||'').trim();
                    if (/^Comment$/i.test(t)) { b.click(); return t; }
                  }
                }"""
            )
            page.wait_for_timeout(2800)

    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    page.evaluate(
        """() => {
          for (const el of document.querySelectorAll('button,[role="button"]')) {
            const al=(el.getAttribute('aria-label')||'')+(el.innerText||'');
            if (/view comments/i.test(al)) { el.click(); return; }
          }
        }"""
    )
    page.wait_for_timeout(1500)
    out["has_comment"] = NEEDLE in page.locator("body").inner_text()

    # Pin via Studio
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/comments",
        wait_until="domcontentloaded",
    )
    page.wait_for_timeout(3500)
    # Clear Unresponded filter
    page.evaluate(
        """() => {
          for (const el of document.querySelectorAll('button, [aria-label], yt-chip-cloud-chip-renderer')) {
            const t=(el.innerText||'')+(el.getAttribute('aria-label')||'');
            if (/unresponded/i.test(t)) { el.click(); }
          }
        }"""
    )
    page.wait_for_timeout(800)
    page.evaluate(
        """() => {
          // uncheck Unresponded in any open menu
          for (const el of document.querySelectorAll('tp-yt-paper-checkbox, [role="checkbox"], label')) {
            const t=(el.innerText||'').trim();
            if (/^Unresponded$/i.test(t)) { el.click(); }
          }
        }"""
    )
    page.wait_for_timeout(1200)
    out["studio_has"] = NEEDLE in page.locator("body").inner_text()
    if out.get("has_comment") or out.get("studio_has"):
        page.evaluate(
            """(needle) => {
              const all=[...document.querySelectorAll('*')];
              let target=null;
              for (const el of all) {
                const t=el.innerText||'';
                if (t.includes(needle) && t.length<900) {
                  const r=el.getBoundingClientRect();
                  if (r.width>80 && r.height>18) { target=el; break; }
                }
              }
              if (!target) return;
              let row=target;
              for (let i=0;i<10 && row;i++) {
                for (const b of row.querySelectorAll('button, ytcp-icon-button, [aria-label]')) {
                  const al=(b.getAttribute('aria-label')||'');
                  if (/more|action|options|menu/i.test(al)) { b.click(); return; }
                }
                row=row.parentElement;
              }
            }""",
            NEEDLE,
        )
        page.wait_for_timeout(600)
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
            page.wait_for_timeout(400)
            page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button, ytcp-button')) {
                    const t=(b.innerText||'').trim();
                    if (/^Pin$/i.test(t) || /^Confirm$/i.test(t)) { b.click(); return t; }
                  }
                }"""
            )
            page.wait_for_timeout(1600)
            out["pinned"] = True
    out["ok"] = bool(out.get("has_comment") or out.get("studio_has"))
    page.screenshot(path=str(AUDIT / f"{video_id}_pin_final.png"), full_page=False)
    return out


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    targets = load_targets()
    report = {"ran_at": datetime.now(LONDON).isoformat(), "results": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
                page.goto("https://studio.youtube.com/", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(3000)

        for i, t in enumerate(targets):
            print(f"[{i+1}/{len(targets)}] {t['video_id']} vis={t['visibility']}", flush=True)
            row = {"video_id": t["video_id"], "title": t["title"]}
            try:
                row["visibility"] = set_visibility(
                    page, t["video_id"], t["visibility"], t.get("schedule_iso")
                )
                row["pin"] = post_pin(page, t["video_id"], t["comment"])
                row["ok"] = bool(row["pin"].get("ok"))
                mark(
                    t["video_id"],
                    pinned_fullfilm_cta=bool(row["pin"].get("pinned") or row["pin"].get("ok")),
                    pinned_fullfilm_cta_at=datetime.now(LONDON).isoformat(),
                    visibility_fixed_at=datetime.now(LONDON).isoformat(),
                )
            except Exception as e:
                row["ok"] = False
                row["error"] = str(e)[:400]
            report["results"].append(row)
            print(
                f"  → ok={row.get('ok')} pinned={row.get('pin',{}).get('pinned')} private_block={row.get('pin',{}).get('blocked_private')}",
                flush=True,
            )
        try:
            page.close()
        except Exception:
            pass
    report["ok_count"] = sum(1 for r in report["results"] if r.get("ok"))
    report["pinned_count"] = sum(
        1 for r in report["results"] if (r.get("pin") or {}).get("pinned")
    )
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"ok": report["ok_count"], "pinned": report["pinned_count"]}, indent=2))


if __name__ == "__main__":
    main()
