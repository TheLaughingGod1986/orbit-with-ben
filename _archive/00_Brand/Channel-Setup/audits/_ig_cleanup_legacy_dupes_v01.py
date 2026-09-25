#!/usr/bin/env python3
"""Clean Instagram @orbitwithben: delete legacy merch/animal posts + duplicate reels.

Keeps one copy of each live Orbit short that has 'Full film on YouTube' in the caption.
Verifies profile bio + YouTube link.
"""
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

KEEP_CAPTION_MARKERS = [
    "where is everybody",
    "space is rude about distance",
    "what if aliens are watching",
]
FULL_FILM = "full film on youtube"
YT_LINK = "youtube.com/@orbitwithben"

# Soft caps so a hung run does not wipe forever; re-run to continue.
MAX_LEGACY_DELETES = 120
MAX_DUPE_DELETES = 40


def _goto(page, url: str, wait: float = 2.5) -> None:
    page.goto(url, wait_until="domcontentloaded", timeout=90000)
    time.sleep(wait)


def _dismiss_noise(page) -> None:
    for label in (
        "Not Now",
        "Not now",
        "Allow all cookies",
        "Allow all",
        "Decline optional cookies",
        "Turn on Notifications",
    ):
        try:
            page.get_by_role("button", name=re.compile(rf"^{re.escape(label)}$", re.I)).click(
                timeout=800
            )
            time.sleep(0.4)
        except Exception:
            pass


def collect_hrefs(page) -> list[str]:
    _goto(page, "https://www.instagram.com/orbitwithben/", wait=4)
    _dismiss_noise(page)
    hrefs: list[str] = []
    stagnant = 0
    for _ in range(40):
        before = len(hrefs)
        for a in page.locator('a[href*="/p/"], a[href*="/reel/"]').all():
            try:
                h = a.get_attribute("href") or ""
            except Exception:
                continue
            if not h:
                continue
            # normalize
            m = re.search(r"(/orbitwithben/(?:p|reel)/[^/?#]+/?)", h)
            if not m:
                m = re.search(r"(/(?:p|reel)/[^/?#]+/?)", h)
                if m:
                    h = "/orbitwithben" + m.group(1)
                else:
                    continue
            else:
                h = m.group(1)
            if not h.endswith("/"):
                h += "/"
            if h not in hrefs:
                hrefs.append(h)
        page.mouse.wheel(0, 3200)
        time.sleep(1.1)
        if len(hrefs) == before:
            stagnant += 1
            if stagnant >= 4:
                break
        else:
            stagnant = 0
    return hrefs


def read_caption(page) -> str:
    """Caption for the opened post only — strip 'More posts from' carousels."""
    try:
        art = page.locator("article").first
        body = art.inner_text(timeout=4000)
    except Exception:
        try:
            body = page.inner_text("body")
        except Exception:
            body = ""
    # Drop suggestions grid that pollutes classification
    for cut in ("More posts from", "More posts", "Suggested for you"):
        idx = body.find(cut)
        if idx > 0:
            body = body[:idx]
    # First meaningful img alt inside article header/media (not profile pic)
    alts = []
    try:
        for img in page.locator("article img").all()[:6]:
            al = (img.get_attribute("alt") or "").strip()
            if not al or "profile picture" in al.lower():
                continue
            if len(al) > 8:
                alts.append(al)
                break  # primary media alt only
    except Exception:
        pass
    return "\n".join(alts + [body])


def classify(href: str, caption: str) -> str:
    low = caption.lower()
    # Feed photo posts on this account are pre-Orbit merch/art — always remove.
    if "/p/" in href:
        if FULL_FILM in low and any(m in low for m in KEEP_CAPTION_MARKERS):
            return "keep_orbit"  # rare: reel shared as /p/
        if any(k in low for k in ("tshirt", "t-shirt", "hoodie", "#shirt", "merch", "unisex", "#tshirt")):
            return "legacy_merch"
        if any(
            k in low
            for k in (
                "cat ",
                "cat mum",
                "dog",
                "sloth",
                "bunny",
                "animal",
                "puppy",
                "kitten",
                "fox",
                "pluto never",
                "metal never",
            )
        ):
            return "legacy_animal"
        return "legacy_other"

    if "/reel/" in href:
        if FULL_FILM in low and any(m in low for m in KEEP_CAPTION_MARKERS):
            return "keep_orbit"
        if FULL_FILM in low:
            return "orbit_other"
        # Today's retries often show "This post has no text" only in Suite;
        # on IG the caption may be empty → treat unknown recent reels as dupes
        # when they lack Full film CTA.
        return "orbit_dupe_candidate"
    return "unknown"


def open_more_menu(page) -> bool:
    for sel in ('svg[aria-label="More Options"]', '[aria-label="More Options"]'):
        try:
            page.locator(sel).first.click(timeout=2500)
            time.sleep(0.8)
            return True
        except Exception:
            continue
    # coordinate fallback from prior probe
    try:
        page.mouse.click(1160, 75)
        time.sleep(0.8)
        return True
    except Exception:
        return False


def confirm_delete(page) -> bool:
    # Click Delete in menu
    clicked = False
    for sel in (
        'div[role="button"]:has-text("Delete")',
        'button:has-text("Delete")',
        'div:text-is("Delete")',
    ):
        try:
            page.locator(sel).first.click(timeout=2000)
            clicked = True
            break
        except Exception:
            continue
    if not clicked:
        # mouse on known Delete row
        try:
            page.get_by_text("Delete", exact=True).first.click(timeout=2000)
            clicked = True
        except Exception:
            return False
    time.sleep(1.0)
    # Confirm dialog — often another Delete
    for _ in range(3):
        try:
            page.get_by_role("button", name=re.compile(r"^Delete$", re.I)).click(timeout=1500)
            time.sleep(0.8)
        except Exception:
            try:
                page.get_by_text("Delete", exact=True).last.click(timeout=1500)
                time.sleep(0.8)
            except Exception:
                break
    time.sleep(1.2)
    return True


def delete_post(page, href: str) -> dict:
    url = "https://www.instagram.com" + href
    try:
        _goto(page, url, wait=2.2)
    except Exception as e:
        return {"href": href, "status": "nav_fail", "error": str(e)[:160]}
    _dismiss_noise(page)
    if page.url.rstrip("/").endswith("orbitwithben") or "/accounts/login" in page.url:
        return {"href": href, "status": "gone_or_login"}
    # already deleted?
    body = ""
    try:
        body = page.inner_text("body")[:1500]
    except Exception:
        pass
    if "Sorry, this page isn't available" in body or "page isn't available" in body.lower():
        return {"href": href, "status": "already_gone"}
    if not open_more_menu(page):
        page.screenshot(path=str(OUT / f"fail_more_{href.split('/')[-2]}.png"))
        return {"href": href, "status": "no_more_menu"}
    if not confirm_delete(page):
        page.screenshot(path=str(OUT / f"fail_del_{href.split('/')[-2]}.png"))
        return {"href": href, "status": "delete_click_fail"}
    # verify
    time.sleep(1.0)
    try:
        _goto(page, url, wait=1.5)
        body2 = page.inner_text("body")[:800]
        gone = "isn't available" in body2.lower() or "/orbitwithben/" == page.url.rstrip("/")[-15:]
    except Exception:
        gone = True
    return {"href": href, "status": "deleted" if gone else "deleted_unverified"}


def verify_profile(page) -> dict:
    _goto(page, "https://www.instagram.com/orbitwithben/", wait=4)
    _dismiss_noise(page)
    body = page.inner_text("body")
    page.screenshot(path=str(OUT / "ig_profile_after.png"), full_page=True)
    m = re.search(r"(\d+)\s+posts", body, re.I)
    return {
        "posts": int(m.group(1)) if m else None,
        "bio_youtube_link": YT_LINK in body.lower(),
        "bio_full_films": "full films on youtube" in body.lower() or "full film" in body.lower(),
        "snip": re.sub(r"\s+", " ", body)[:500],
    }


def main() -> None:
    results: dict = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "hrefs": [],
        "classified": [],
        "deleted": [],
        "kept": [],
        "skipped": [],
        "errors": [],
        "profile_before": None,
        "profile_after": None,
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = next(x for x in browser.contexts[0].pages if not x.is_closed())
        page.bring_to_front()

        results["profile_before"] = verify_profile(page)
        hrefs = collect_hrefs(page)
        results["hrefs"] = hrefs
        (OUT / "HREFS.json").write_text(json.dumps(hrefs, indent=2))
        print(f"collected {len(hrefs)} hrefs; posts_before={results['profile_before'].get('posts')}", flush=True)

        # Classify: all /p/ feed posts are pre-Orbit legacy → delete without opening.
        # Open /reel/ only to keep one Full-film copy of each live short.
        keep_slots: dict[str, str] = {}  # marker -> href
        to_delete: list[tuple[str, str]] = []

        legacy_hrefs = [h for h in hrefs if "/p/" in h]
        reel_hrefs = [h for h in hrefs if "/reel/" in h]
        for href in legacy_hrefs:
            entry = {"href": href, "kind": "legacy_other", "cap": "(feed post — delete)"}
            results["classified"].append(entry)
            to_delete.append((href, "legacy_other"))
        print(f"queued {len(legacy_hrefs)} legacy /p/ deletes; classifying {len(reel_hrefs)} reels", flush=True)

        for i, href in enumerate(reel_hrefs):
            try:
                _goto(page, "https://www.instagram.com" + href, wait=1.8)
            except Exception as e:
                results["errors"].append({href: str(e)[:120]})
                continue
            cap = read_caption(page)
            kind = classify(href, cap)
            entry = {"href": href, "kind": kind, "cap": re.sub(r"\s+", " ", cap)[:220]}
            results["classified"].append(entry)
            print(f"[reel {i+1}/{len(reel_hrefs)}] {kind} {href} :: {entry['cap'][:80]}", flush=True)

            if kind == "keep_orbit":
                low = cap.lower()
                marker = next((m for m in KEEP_CAPTION_MARKERS if m in low), "orbit")
                if marker not in keep_slots:
                    keep_slots[marker] = href
                    results["kept"].append(entry)
                else:
                    to_delete.append((href, "dupe_of_kept"))
            elif kind == "orbit_other":
                # Unique Full-film reel (e.g. clue) — keep
                results["kept"].append(entry)
            elif kind in ("orbit_dupe_candidate", "reel_unknown"):
                to_delete.append((href, kind))
            else:
                results["skipped"].append(entry)

            if i and i % 10 == 0:
                (OUT / "CLASSIFY_PARTIAL.json").write_text(json.dumps(results, indent=2))

        # Ensure we keep at most one per marker; if none classified keep yet, pin newest Full film later
        print(f"keep_slots={keep_slots}", flush=True)
        print(f"to_delete={len(to_delete)}", flush=True)

        legacy = [(h, k) for h, k in to_delete if k.startswith("legacy")]
        dupes = [(h, k) for h, k in to_delete if not k.startswith("legacy")]

        deleted_n = 0
        for href, reason in legacy:
            if deleted_n >= MAX_LEGACY_DELETES:
                results["skipped"].append({"href": href, "reason": "max_legacy"})
                continue
            r = delete_post(page, href)
            r["reason"] = reason
            results["deleted"].append(r)
            deleted_n += 1
            print("DEL", r["status"], href, reason, flush=True)
            if deleted_n % 10 == 0:
                (OUT / "DELETE_PARTIAL.json").write_text(json.dumps(results, indent=2))

        dupe_n = 0
        for href, reason in dupes:
            if dupe_n >= MAX_DUPE_DELETES:
                results["skipped"].append({"href": href, "reason": "max_dupe"})
                continue
            # never delete the keep_slots
            if href in keep_slots.values():
                continue
            r = delete_post(page, href)
            r["reason"] = reason
            results["deleted"].append(r)
            dupe_n += 1
            print("DEL", r["status"], href, reason, flush=True)

        results["profile_after"] = verify_profile(page)
        results["finished_at"] = datetime.now(timezone.utc).isoformat()
        results["keep_slots"] = keep_slots
        (OUT / "CLEANUP_RESULT.json").write_text(json.dumps(results, indent=2))
        print(json.dumps({
            "before": results["profile_before"].get("posts"),
            "after": results["profile_after"].get("posts"),
            "deleted": len(results["deleted"]),
            "kept": len(results["kept"]),
            "bio_yt": results["profile_after"].get("bio_youtube_link"),
            "keep_slots": keep_slots,
        }, indent=2), flush=True)


if __name__ == "__main__":
    main()
