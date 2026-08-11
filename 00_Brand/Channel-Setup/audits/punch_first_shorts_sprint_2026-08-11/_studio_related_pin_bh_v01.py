#!/usr/bin/env python3
"""Studio finish: Related → 3xrxdmaOwJI + pin full-film CTA on live BH Shorts.

Uses CDP :9222. Does not upload or change visibility/privacy.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"
LONG_ID = "3xrxdmaOwJI"
LONG_TITLE = "What Happens If You Fall Into a Black Hole"
# Live / go-live BH Shorts that should funnel to the BH long
SHORTS = [
    "JRfhE6yWom4",
    "L2OFjL4neOo",
    "tUAdhOnMW2g",
    "svYOx07OrIM",  # may still be scheduled — skip if not editable public/scheduled details ok
]
COMMENT = (
    "Want to see the full journey into a black hole? "
    "Watch the complete episode using the related video link 👇"
)
NEEDLE = "full journey into a black hole"
OUT_DIR = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/audits/"
    "punch_first_shorts_sprint_2026-08-11"
)
OUT = OUT_DIR / "STUDIO_RELATED_PIN_RESULT.json"
SHOTS = OUT_DIR / "studio_finish_shots"
SHOTS.mkdir(parents=True, exist_ok=True)


def dismiss(page) -> None:
    for name in ("Done", "Got it", "Close", "Not now", "Dismiss"):
        try:
            page.get_by_role("button", name=name, exact=True).first.click(timeout=400)
            page.wait_for_timeout(150)
        except Exception:
            pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def save_edit(page) -> bool:
    try:
        b = page.get_by_role("button", name="Save", exact=True).first
        if b.count() and b.is_enabled():
            b.click(force=True, timeout=2000)
            page.wait_for_timeout(2200)
            return True
    except Exception:
        pass
    return False


def set_related(page, vid: str) -> dict:
    r: dict = {"id": vid, "step": "related"}
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    try:
        page.evaluate("()=>{window.onbeforeunload=null}")
    except Exception:
        pass
    dismiss(page)

    body0 = page.locator("body").inner_text()
    if "don't have permission" in body0.lower() or "Oops" in page.title():
        r["error"] = "no_permission"
        return r
    if "Video unavailable" in body0 or "isn't available" in body0.lower():
        r["error"] = "unavailable"
        return r

    # Already set?
    if "Related video" in body0:
        chunk0 = body0.split("Related video", 1)[-1][:220]
        if ("Black Hole" in chunk0 or "Fall Into" in chunk0) and "None" not in chunk0[:40]:
            r["already_set"] = True
            r["related_chunk"] = chunk0.replace("\n", " ")[:250]
            r["ok"] = True
            page.screenshot(path=str(SHOTS / f"{vid}_related_already.png"))
            return r

    try:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.55)")
        page.wait_for_timeout(800)
    except Exception:
        pass

    opened = False
    for sel in (
        "ytcp-shorts-content-links-picker",
        "text=Related video",
        "#related-video",
    ):
        try:
            loc = page.locator(sel).first
            if loc.count():
                loc.scroll_into_view_if_needed(timeout=3000)
                loc.click(force=True, timeout=3000)
                opened = True
                break
        except Exception:
            continue
    if not opened:
        try:
            page.get_by_text(re.compile(r"Related video", re.I)).first.click(
                force=True, timeout=3000
            )
            opened = True
        except Exception as e:
            r["error"] = f"open_related:{e}"[:160]
            page.screenshot(path=str(SHOTS / f"{vid}_related_fail.png"))
            return r

    page.wait_for_timeout(1200)
    try:
        page.locator("ytcp-video-pick-dialog").wait_for(timeout=15000)
    except Exception:
        r["error"] = "no_pick_dialog"
        page.screenshot(path=str(SHOTS / f"{vid}_related_nodialog.png"))
        return r

    search = page.locator("ytcp-video-pick-dialog #search-yours")
    if not search.count():
        search = page.get_by_placeholder(re.compile(r"Search your videos", re.I))
    matched = False
    for q in (LONG_TITLE, LONG_ID, "Black Hole", "Orbit's Cosmic Journey"):
        try:
            search.first.fill("")
            search.first.fill(q)
            page.wait_for_timeout(2200)
            body = page.locator("ytcp-video-pick-dialog").inner_text()
            if "No matching results" not in body:
                matched = True
                r["search_q"] = q
                break
        except Exception:
            continue
    if not matched:
        r["error"] = "not_found_in_picker"
        page.keyboard.press("Escape")
        page.screenshot(path=str(SHOTS / f"{vid}_related_notfound.png"))
        return r

    cells = page.locator("ytcp-video-pick-dialog ytcp-video-list-cell-video")
    if not cells.count():
        cells = page.locator("ytcp-video-pick-dialog ytcp-entity-card")
    picked = False
    for i in range(min(cells.count(), 12)):
        t = cells.nth(i).inner_text()
        is_shortish = bool(re.search(r"\b0:\d{2}\b", t)) and not re.search(
            r"\b\d{2}:\d{2}\b", t
        )
        if (LONG_ID in t or "Black Hole" in t or "Fall Into" in t) and not is_shortish:
            cells.nth(i).click(force=True)
            r["picked"] = t[:180]
            picked = True
            break
    if not picked and cells.count():
        for i in range(min(cells.count(), 8)):
            t = cells.nth(i).inner_text()
            if "Black Hole" in t or "Fall Into" in t:
                cells.nth(i).click(force=True)
                r["picked"] = t[:180]
                picked = True
                break
    if not picked:
        r["error"] = "no_cell"
        page.keyboard.press("Escape")
        return r

    page.wait_for_timeout(700)
    for name in ("Done", "Select", "Save"):
        try:
            b = page.get_by_role("button", name=name, exact=True).first
            if b.count() and b.is_visible() and b.is_enabled():
                b.click(force=True, timeout=2000)
                page.wait_for_timeout(700)
                break
        except Exception:
            continue
    r["saved"] = save_edit(page)

    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2800)
    body = page.locator("body").inner_text()
    chunk = body.split("Related video", 1)[-1][:300] if "Related video" in body else ""
    r["related_chunk"] = chunk.replace("\n", " ")[:250]
    r["ok"] = ("None" not in chunk[:50]) and (
        "Black Hole" in chunk
        or "Fall Into" in chunk
        or "Orbit" in chunk
        or LONG_ID in chunk
    )
    page.screenshot(path=str(SHOTS / f"{vid}_related.png"))
    return r


def pin_comment(page, vid: str) -> dict:
    r: dict = {"id": vid, "step": "pin"}
    page.goto(
        f"https://www.youtube.com/watch?v={vid}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    page.evaluate("window.scrollTo(0, Math.min(document.body.scrollHeight, 1600))")
    page.wait_for_timeout(1500)
    body0 = page.locator("body").inner_text()
    r["already"] = NEEDLE.lower() in body0.lower()

    if not r["already"]:
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
                    loc.scroll_into_view_if_needed(timeout=2000)
                    loc.click(force=True, timeout=2000)
                    page.wait_for_timeout(400)
                    placed = True
                    break
            except Exception:
                continue
        r["box"] = placed
        if placed:
            page.keyboard.type(COMMENT, delay=8)
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
            r["comment_click"] = clicked
            page.wait_for_timeout(2800)

    page.goto(
        f"https://studio.youtube.com/video/{vid}/comments",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    studio_text = page.locator("body").inner_text()
    r["studio_has"] = NEEDLE.lower() in studio_text.lower()

    if not r["studio_has"]:
        try:
            page.get_by_text(re.compile(r"Add a comment|Comment as", re.I)).first.click(
                timeout=2500
            )
            page.wait_for_timeout(500)
            page.keyboard.type(COMMENT, delay=8)
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
            r["studio_has"] = NEEDLE.lower() in studio_text.lower()
        except Exception as e:
            r["studio_post_err"] = str(e)[:160]

    if r.get("studio_has") or r.get("already"):
        # Already pinned?
        if "pinned by" in studio_text.lower() and NEEDLE.lower() in studio_text.lower():
            r["already_pinned"] = True
            r["ok"] = True
            page.screenshot(path=str(SHOTS / f"{vid}_comments.png"))
            return r

        menu = page.evaluate(
            """(needle) => {
              const all=[...document.querySelectorAll('*')];
              let target=null;
              for (const el of all) {
                const t=(el.innerText||'');
                if (t.toLowerCase().includes(needle) && t.length<900) {
                  const r=el.getBoundingClientRect();
                  if (r.width>80 && r.height>18) { target=el; break; }
                }
              }
              if (!target) return 'no';
              let row=target;
              for (let i=0;i<12 && row;i++) {
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
        r["menu"] = menu
        page.wait_for_timeout(700)
        pinned = False
        try:
            page.get_by_text(re.compile(r"^Pin$", re.I)).first.click(force=True, timeout=2500)
            pinned = True
        except Exception:
            try:
                page.get_by_role("menuitem", name=re.compile(r"Pin", re.I)).first.click(
                    force=True, timeout=2500
                )
                pinned = True
            except Exception:
                pass
        if pinned:
            page.wait_for_timeout(600)
            for name in ("Pin", "Confirm", "OK", "Done"):
                try:
                    page.get_by_role("button", name=name, exact=True).first.click(
                        timeout=800
                    )
                    page.wait_for_timeout(400)
                except Exception:
                    pass
        r["pin_clicked"] = pinned
        page.wait_for_timeout(1500)
        after = page.locator("body").inner_text().lower()
        r["ok"] = pinned or ("pinned" in after)
    else:
        r["ok"] = False
        r["error"] = "comment_not_found"

    page.screenshot(path=str(SHOTS / f"{vid}_comments.png"))
    return r


def main() -> int:
    results = {
        "ok": False,
        "blockedOn": None,
        "executedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "parentLongId": LONG_ID,
        "targets": SHORTS,
        "related": [],
        "pins": [],
        "skipped": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_viewport_size({"width": 1440, "height": 1100})
        page.add_init_script("window.onbeforeunload=null;")
        page.on("dialog", lambda d: d.accept())

        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        body = page.locator("body").inner_text()
        if "don't have permission" in body.lower():
            results["blockedOn"] = "wrong_google_account"
            OUT.write_text(json.dumps(results, indent=2) + "\n")
            print(json.dumps({"fatal": "no_permission"}))
            return 2
        if "Orbit" not in body and "Orbit" not in page.title():
            # soft check — dashboard snippet usually shows channel name
            results["authNote"] = "Orbit name not clearly in dashboard body; continuing"
        results["signedInChannel"] = {
            "name": "Orbit with Ben",
            "id": CHANNEL,
            "studioUrl": page.url,
        }

        for vid in SHORTS:
            print(f"RELATED {vid}", flush=True)
            rel = set_related(page, vid)
            if rel.get("error") in ("unavailable", "no_permission"):
                results["skipped"].append(rel)
            else:
                results["related"].append(rel)
            print(
                json.dumps(
                    {k: rel.get(k) for k in ("id", "ok", "error", "already_set", "picked")},
                    ensure_ascii=False,
                ),
                flush=True,
            )

        for item in list(results["related"]):
            if not item.get("ok") and item.get("error") in (
                "not_found_in_picker",
                "open_related",
                "no_pick_dialog",
                "no_cell",
            ):
                # still try pin if video loads
                pass
            vid = item["id"]
            print(f"PIN {vid}", flush=True)
            pin = pin_comment(page, vid)
            results["pins"].append(pin)
            print(
                json.dumps(
                    {
                        k: pin.get(k)
                        for k in (
                            "id",
                            "ok",
                            "error",
                            "pin_clicked",
                            "already_pinned",
                            "studio_has",
                        )
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )

        page.close()

    related_ok = [x for x in results["related"] if x.get("ok")]
    pin_ok = [x for x in results["pins"] if x.get("ok")]
    results["ok"] = bool(related_ok) and len(related_ok) == len(results["related"]) and len(
        pin_ok
    ) == len(results["pins"])
    results["summary"] = {
        "related_ok": len(related_ok),
        "related_total": len(results["related"]),
        "pin_ok": len(pin_ok),
        "pin_total": len(results["pins"]),
        "skipped": len(results["skipped"]),
    }
    OUT.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"ok": results["ok"], "summary": results["summary"], "out": str(OUT)}, indent=2))
    return 0 if results["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
