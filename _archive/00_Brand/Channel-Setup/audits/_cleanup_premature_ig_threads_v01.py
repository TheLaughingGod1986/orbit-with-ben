#!/usr/bin/env python3
"""Delete premature IG reels + Threads posts for aliens shorts 01–03 (YT not live yet)."""
from __future__ import annotations

import json
import re
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "premature_social_cleanup_2026-08-03"
OUT.mkdir(parents=True, exist_ok=True)
CDP = "http://127.0.0.1:9222"
LONDON = ZoneInfo("Europe/London")

# Morning-funnel IG reels (aliases 01–03) — remove until YT go-live
IG_REELS = [
    ("/orbitwithben/reel/Dbkjz74gTje/", "Where Is Everybody?", "1HuV8o3gOss"),
    ("/orbitwithben/reel/DbkkMoxjwpt/", "Space Is Rude About Distance", "dPMJQp2gMNc"),
    ("/orbitwithben/reel/DbkkmlLEwbH/", "What If Aliens Are Watching Us?", "rFJoOdQAc9c"),
]

THREADS_NEEDLES = [
    ("Where Is Everybody", "1HuV8o3gOss"),
    ("Space Is Rude About Distance", "dPMJQp2gMNc"),
    ("What If Aliens Are Watching Us", "rFJoOdQAc9c"),
    ("Watching Us", "rFJoOdQAc9c"),
]


def shot(page, name: str) -> None:
    try:
        page.screenshot(path=str(OUT / name), timeout=12000)
    except Exception as e:
        print("shot", name, type(e).__name__, flush=True)


def delete_ig(page, href: str, title: str) -> dict:
    url = "https://www.instagram.com" + href
    page.goto(url, wait_until="domcontentloaded", timeout=90000)
    time.sleep(2)
    body = page.evaluate("() => (document.body && document.body.innerText) || ''")
    if "isn't available" in body.lower() or "page isn't available" in body.lower():
        return {"href": href, "title": title, "status": "already_gone"}

    opened = False
    for sel in ('svg[aria-label="More Options"]', '[aria-label="More Options"]', '[aria-label="More options"]'):
        try:
            page.locator(sel).first.click(timeout=2500)
            opened = True
            break
        except Exception:
            continue
    if not opened:
        try:
            page.get_by_role("button", name=re.compile(r"More", re.I)).first.click(timeout=2000)
            opened = True
        except Exception:
            shot(page, f"ig_no_more_{href.split('/')[-2]}.png")
            return {"href": href, "title": title, "status": "no_more"}
    time.sleep(0.8)

    try:
        page.get_by_role("button", name=re.compile(r"^Delete$", re.I)).first.click(timeout=3000)
    except Exception:
        try:
            page.get_by_text("Delete", exact=True).first.click(timeout=2500)
        except Exception:
            shot(page, f"ig_no_delete_{href.split('/')[-2]}.png")
            return {"href": href, "title": title, "status": "no_delete_menu"}
    time.sleep(0.9)

    confirmed = False
    for _ in range(4):
        try:
            page.get_by_role("button", name=re.compile(r"^Delete$", re.I)).last.click(timeout=1500)
            confirmed = True
            time.sleep(0.7)
        except Exception:
            break
    time.sleep(2)
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    time.sleep(1.5)
    body2 = page.evaluate("() => (document.body && document.body.innerText) || ''")
    gone = "isn't available" in body2.lower() or "page isn't available" in body2.lower()
    shot(page, f"ig_after_{href.split('/')[-2]}.png")
    return {
        "href": href,
        "title": title,
        "status": "ok" if gone or confirmed else "unconfirmed",
        "confirmed": confirmed,
        "gone": gone,
    }


def delete_threads(page) -> list[dict]:
    results: list[dict] = []
    page.goto("https://www.threads.com/@orbitwithben", wait_until="domcontentloaded", timeout=90000)
    time.sleep(4)
    shot(page, "threads_before.png")

    for round_i in range(8):
        # Find a post card matching needles
        found = page.evaluate(
            """(needles) => {
              const arts=[...document.querySelectorAll('div[data-pressable-container], article, div[role=article], div')]
                .filter(el => {
                  const t=(el.innerText||'');
                  if (t.length<20 || t.length>2500) return false;
                  return needles.some(n => t.includes(n));
                });
              // pick smallest matching container that has a menu button nearby
              const scored=arts.map(el => {
                const r=el.getBoundingClientRect();
                return {t:(el.innerText||'').slice(0,120), w:r.width, h:r.height, x:r.x, y:r.y, top:r.top};
              }).filter(o => o.w>200 && o.h>80 && o.y>80 && o.y<900)
               .sort((a,b)=>a.h-b.h);
              return scored[0] || null;
            }""",
            [n[0] for n in THREADS_NEEDLES],
        )
        if not found:
            print("threads no more matches", flush=True)
            break
        print("threads found", found, flush=True)

        # Click the three-dot / More on that card (top-right of card)
        menu = page.evaluate(
            """(yApprox) => {
              const btns=[...document.querySelectorAll('div[role=button],button,[aria-label]')]
                .map(el => {
                  const r=el.getBoundingClientRect();
                  const al=(el.getAttribute('aria-label')||'')+(el.innerText||'');
                  return {al, x:r.x, y:r.y, w:r.width, h:r.height};
                })
                .filter(o => o.y>yApprox-40 && o.y<yApprox+120 && o.x>500 && o.w<80 && o.h<80
                  && /more|menu|option/i.test(o.al));
              if (!btns.length) {
                // fallback: unlabeled small buttons on right
                const small=[...document.querySelectorAll('div[role=button],button')]
                  .map(el => {
                    const r=el.getBoundingClientRect();
                    return {x:r.x,y:r.y,w:r.width,h:r.height,al:el.getAttribute('aria-label')||''};
                  })
                  .filter(o => o.y>yApprox-20 && o.y<yApprox+80 && o.x>700 && o.w>=24 && o.w<=60 && o.h>=24 && o.h<=60);
                return small.sort((a,b)=>b.x-a.x)[0] || null;
              }
              return btns.sort((a,b)=>b.x-a.x)[0];
            }""",
            found["y"],
        )
        if not menu:
            results.append({"status": "no_menu", "found": found})
            # scroll past
            page.mouse.wheel(0, 400)
            time.sleep(1)
            continue
        page.mouse.click(menu["x"] + menu["w"] / 2, menu["y"] + menu["h"] / 2)
        time.sleep(1.2)
        shot(page, f"threads_menu_{round_i}.png")

        items = page.evaluate(
            """() => [...document.querySelectorAll('[role=menuitem], div[role=dialog] div[role=button], span')]
              .map(e => (e.innerText||'').trim()).filter(Boolean).slice(0,30)"""
        )
        print("menu items", items, flush=True)
        deleted = page.evaluate(
            """() => {
              const el=[...document.querySelectorAll('[role=menuitem],div[role=button],button,span')]
                .find(e => /^(Delete|Delete post|Remove)$/i.test((e.innerText||'').trim()));
              if (!el) return null;
              el.click();
              return (el.innerText||'').trim();
            }"""
        )
        time.sleep(1)
        confirmed = page.evaluate(
            """() => {
              const els=[...document.querySelectorAll('div[role=button],button')]
                .filter(e => /^(Delete|Confirm|Delete post)$/i.test((e.innerText||'').trim()));
              if (!els.length) return null;
              els[els.length-1].click();
              return els[els.length-1].innerText.trim();
            }"""
        )
        entry = {"round": round_i, "found": found, "delete": deleted, "confirm": confirmed, "items": items}
        results.append(entry)
        print(entry, flush=True)
        time.sleep(3)
        page.goto("https://www.threads.com/@orbitwithben", wait_until="domcontentloaded", timeout=90000)
        time.sleep(3)

    shot(page, "threads_after.png")
    body = page.evaluate("() => (document.body && document.body.innerText) || ''")
    remaining = {
        n[0]: (n[0].lower() in body.lower() or n[0].split()[0].lower() in body.lower())
        for n in THREADS_NEEDLES[:3]
    }
    return results, remaining, re.sub(r"\s+", " ", body)[:800]


def main() -> None:
    results: dict = {
        "at": datetime.now(LONDON).isoformat(),
        "ig": [],
        "threads": [],
        "threads_remaining": None,
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = next((pg for pg in ctx.pages if not pg.is_closed()), None) or ctx.new_page()
        page.bring_to_front()

        print("=== IG ===", flush=True)
        for href, title, ytid in IG_REELS:
            print(f"deleting IG {title}", flush=True)
            try:
                entry = delete_ig(page, href, title)
            except Exception as e:
                entry = {"href": href, "title": title, "status": "error", "error": str(e)[:200]}
            entry["youtube_id"] = ytid
            results["ig"].append(entry)
            print(entry, flush=True)
            time.sleep(1)

        print("=== Threads ===", flush=True)
        try:
            thr, rem, snip = delete_threads(page)
            results["threads"] = thr
            results["threads_remaining"] = rem
            results["threads_snip"] = snip
        except Exception as e:
            results["threads_error"] = str(e)[:240]
            shot(page, "threads_err.png")

        # Verify IG profile grid
        page.goto("https://www.instagram.com/orbitwithben/", wait_until="domcontentloaded", timeout=90000)
        time.sleep(3)
        shot(page, "ig_profile_after.png")
        hrefs = page.evaluate(
            """() => [...document.querySelectorAll('a[href*="/reel/"],a[href*="/p/"]')]
              .map(a => a.getAttribute('href')||'')
              .filter(Boolean).slice(0,20)"""
        )
        results["ig_profile_hrefs"] = hrefs
        results["ig_still_has_targets"] = any(
            any(t[0].rstrip("/") in (h or "") for t in IG_REELS) for h in hrefs
        )

    (OUT / "CLEANUP_RESULT.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2), flush=True)


if __name__ == "__main__":
    main()
