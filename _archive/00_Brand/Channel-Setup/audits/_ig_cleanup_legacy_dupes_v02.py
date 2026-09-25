#!/usr/bin/env python3
"""Continue IG cleanup — fast delete remaining legacy /p/ + no-caption reel dupes."""
from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9223"
OUT = Path(__file__).resolve().parent / "ig_cleanup_2026-08-03"
OUT.mkdir(parents=True, exist_ok=True)

KEEP = {
    "/orbitwithben/reel/DbkkmlLEwbH/",
    "/orbitwithben/reel/DbkkMoxjwpt/",
    "/orbitwithben/reel/Dbkjz74gTje/",
}


def collect_hrefs(page) -> list[str]:
    page.goto("https://www.instagram.com/orbitwithben/", wait_until="domcontentloaded", timeout=90000)
    time.sleep(3.5)
    hrefs: list[str] = []
    stagnant = 0
    for _ in range(35):
        before = len(hrefs)
        for a in page.locator('a[href*="/p/"], a[href*="/reel/"]').all():
            try:
                h = a.get_attribute("href") or ""
            except Exception:
                continue
            m = re.search(r"(/orbitwithben/(?:p|reel)/[^/?#]+/?)", h) or re.search(
                r"(/(?:p|reel)/[^/?#]+/?)", h
            )
            if not m:
                continue
            h = m.group(1)
            if not h.startswith("/orbitwithben"):
                h = "/orbitwithben" + h
            if not h.endswith("/"):
                h += "/"
            if h not in hrefs:
                hrefs.append(h)
        page.mouse.wheel(0, 3200)
        time.sleep(0.9)
        if len(hrefs) == before:
            stagnant += 1
            if stagnant >= 4:
                break
        else:
            stagnant = 0
    return hrefs


def delete_one(page, href: str) -> dict:
    url = "https://www.instagram.com" + href
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        time.sleep(1.4)
    except Exception as e:
        return {"href": href, "status": "nav_fail", "error": str(e)[:120]}

    body = ""
    try:
        body = page.inner_text("body")[:900]
    except Exception:
        pass
    if "isn't available" in body.lower():
        return {"href": href, "status": "already_gone"}

    # Open More Options
    opened = False
    for sel in ('svg[aria-label="More Options"]', '[aria-label="More Options"]'):
        try:
            page.locator(sel).first.click(timeout=2000)
            opened = True
            break
        except Exception:
            continue
    if not opened:
        try:
            page.mouse.click(1160, 75)
            opened = True
        except Exception:
            return {"href": href, "status": "no_more"}
    time.sleep(0.55)

    # Menu Delete
    try:
        page.locator('div[role="button"]', has_text=re.compile(r"^Delete$")).first.click(timeout=2500)
    except Exception:
        try:
            page.get_by_text("Delete", exact=True).first.click(timeout=2000)
        except Exception:
            page.screenshot(path=str(OUT / f"v02_fail_menu_{href.split('/')[-2]}.png"))
            return {"href": href, "status": "no_delete_menu"}
    time.sleep(0.7)

    # Confirm dialog Delete
    confirmed = False
    for _ in range(4):
        try:
            page.get_by_role("button", name=re.compile(r"^Delete$", re.I)).click(timeout=1200)
            confirmed = True
            time.sleep(0.6)
        except Exception:
            try:
                # dialog often uses button with red Delete
                btns = page.locator('button:has-text("Delete"), div[role="button"]:has-text("Delete")')
                if btns.count():
                    btns.last.click(timeout=1200)
                    confirmed = True
                    time.sleep(0.6)
                else:
                    break
            except Exception:
                break
    time.sleep(0.8)
    return {"href": href, "status": "deleted" if confirmed else "maybe_deleted"}


def posts_count(page) -> int | None:
    page.goto("https://www.instagram.com/orbitwithben/", wait_until="domcontentloaded", timeout=90000)
    time.sleep(3.5)
    body = page.inner_text("body")
    page.screenshot(path=str(OUT / "v02_profile.png"), full_page=True)
    m = re.search(r"(\d+)\s+posts", body, re.I)
    return int(m.group(1)) if m else None


def profile_funnel(page) -> dict:
    page.goto("https://www.instagram.com/orbitwithben/", wait_until="domcontentloaded", timeout=90000)
    time.sleep(3.5)
    body = page.inner_text("body")
    return {
        "bio_youtube_link": "youtube.com/@orbitwithben" in body.lower(),
        "bio_full_films": "full films on youtube" in body.lower(),
        "snip": re.sub(r"\s+", " ", body)[:400],
    }


def main() -> None:
    results = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "deleted": [],
        "kept": list(KEEP),
        "errors": [],
    }
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(CDP)
        page = next(x for x in b.contexts[0].pages if not x.is_closed())
        page.bring_to_front()
        before = posts_count(page)
        results["posts_before"] = before
        hrefs = collect_hrefs(page)
        results["hrefs"] = hrefs
        targets = [h for h in hrefs if h not in KEEP]
        # Prefer deleting /p/ first, then extra reels
        targets = sorted(targets, key=lambda h: (0 if "/p/" in h else 1, h))
        print(f"before={before} hrefs={len(hrefs)} targets={len(targets)}", flush=True)

        for i, href in enumerate(targets):
            r = delete_one(page, href)
            results["deleted"].append(r)
            print(f"[{i+1}/{len(targets)}] {r['status']} {href}", flush=True)
            if (i + 1) % 15 == 0:
                (OUT / "V02_PARTIAL.json").write_text(json.dumps(results, indent=2))
                # soft progress count
                try:
                    n = posts_count(page)
                    print(f"  progress posts≈{n}", flush=True)
                except Exception:
                    pass

        results["posts_after"] = posts_count(page)
        results["funnel"] = profile_funnel(page)
        # final grid hrefs
        results["hrefs_after"] = collect_hrefs(page)
        results["finished_at"] = datetime.now(timezone.utc).isoformat()
        (OUT / "V02_RESULT.json").write_text(json.dumps(results, indent=2))
        print(
            json.dumps(
                {
                    "before": results["posts_before"],
                    "after": results["posts_after"],
                    "deleted_attempts": len(results["deleted"]),
                    "ok": sum(1 for d in results["deleted"] if d["status"] in ("deleted", "already_gone", "maybe_deleted")),
                    "remaining_hrefs": len(results["hrefs_after"]),
                    "funnel": results["funnel"],
                    "kept_still_present": [h for h in KEEP if h in results["hrefs_after"]],
                },
                indent=2,
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
