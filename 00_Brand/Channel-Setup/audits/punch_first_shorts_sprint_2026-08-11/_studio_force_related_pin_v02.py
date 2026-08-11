#!/usr/bin/env python3
"""Force-correct BH Short Related → long 3xrxdmaOwJI; pin remaining Shorts."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
LONG_ID = "3xrxdmaOwJI"
LONG_TITLE = "What Happens If You Fall Into a Black Hole"
WRONG_MARKERS = (
    "Time Dilation Near Black Holes",
    "Observer vs",
    "Point of No Return",
    "Would You Look Back",
    "Time Appears to Stop",
)
SHORTS = ["JRfhE6yWom4", "L2OFjL4neOo", "tUAdhOnMW2g", "svYOx07OrIM"]
PIN_NEEDED = ["tUAdhOnMW2g", "svYOx07OrIM"]
COMMENT = (
    "Want to see the full journey into a black hole? "
    "Watch the complete episode using the related video link 👇\n"
    f"https://youtu.be/{LONG_ID}"
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
            page.wait_for_timeout(120)
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
            b.click(force=True, timeout=2500)
            page.wait_for_timeout(2500)
            return True
    except Exception:
        pass
    return False


def related_chunk(page) -> str:
    body = page.locator("body").inner_text()
    if "Related video" not in body:
        return ""
    return body.split("Related video", 1)[-1][:280].replace("\n", " ")


def related_ok(chunk: str) -> bool:
    if not chunk or "None" in chunk[:50]:
        return False
    if any(w.lower() in chunk.lower() for w in WRONG_MARKERS):
        return False
    return (
        LONG_ID in chunk
        or "Fall Into a Black Hole" in chunk
        or "What Happens If You Fall" in chunk
    )


def force_related(page, vid: str) -> dict:
    r: dict = {"id": vid, "step": "related_force"}
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3200)
    try:
        page.evaluate("()=>{window.onbeforeunload=null}")
    except Exception:
        pass
    dismiss(page)
    before = related_chunk(page)
    r["before"] = before[:220]
    if related_ok(before):
        r["ok"] = True
        r["already_correct"] = True
        page.screenshot(path=str(SHOTS / f"{vid}_related_correct.png"))
        return r

    try:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.5)")
        page.wait_for_timeout(700)
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
            r["error"] = f"open:{e}"[:160]
            page.screenshot(path=str(SHOTS / f"{vid}_related_open_fail.png"))
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

    picker_dump = ""
    matched = False
    for q in (LONG_TITLE, "Fall Into a Black Hole", LONG_ID, "Orbit's Cosmic Journey"):
        try:
            search.first.fill("")
            search.first.fill(q)
            page.wait_for_timeout(2400)
            picker_dump = page.locator("ytcp-video-pick-dialog").inner_text()
            r["search_q"] = q
            r["picker_snip"] = picker_dump.replace("\n", " ")[:400]
            if "No matching results" not in picker_dump:
                matched = True
                break
        except Exception as e:
            r.setdefault("search_errs", []).append(str(e)[:80])
    if not matched:
        r["error"] = "not_found_in_picker"
        page.screenshot(path=str(SHOTS / f"{vid}_related_notfound.png"))
        page.keyboard.press("Escape")
        return r

    cells = page.locator("ytcp-video-pick-dialog ytcp-video-list-cell-video")
    if not cells.count():
        cells = page.locator("ytcp-video-pick-dialog ytcp-entity-card")
    r["cell_count"] = cells.count()
    picked = False
    for i in range(min(cells.count(), 15)):
        t = cells.nth(i).inner_text()
        # Long-form durations look like 18:xx / 21:xx; shorts like 0:28
        is_shortish = bool(re.search(r"\b0:\d{2}\b", t)) and not re.search(
            r"\b1?\d:\d{2}\b", t
        )
        has_long_title = (
            "Fall Into" in t
            or "What Happens" in t
            or LONG_ID in t
            or "Cosmic Journey" in t
        )
        if has_long_title and not is_shortish:
            cells.nth(i).click(force=True)
            r["picked"] = t.replace("\n", " ")[:200]
            picked = True
            break
    if not picked:
        # last resort: any non-short cell with Black Hole + Fall
        for i in range(min(cells.count(), 15)):
            t = cells.nth(i).inner_text()
            if re.search(r"\b(1[89]|2[0-5]):\d{2}\b", t) and "Black Hole" in t:
                cells.nth(i).click(force=True)
                r["picked"] = t.replace("\n", " ")[:200]
                picked = True
                break
    if not picked:
        r["error"] = "no_long_cell"
        page.screenshot(path=str(SHOTS / f"{vid}_related_nocell.png"))
        page.keyboard.press("Escape")
        return r

    page.wait_for_timeout(800)
    for name in ("Done", "Select", "Save"):
        try:
            b = page.get_by_role("button", name=name, exact=True).first
            if b.count() and b.is_visible() and b.is_enabled():
                b.click(force=True, timeout=2000)
                page.wait_for_timeout(800)
                break
        except Exception:
            continue
    r["saved"] = save_edit(page)

    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    after = related_chunk(page)
    r["after"] = after[:220]
    r["ok"] = related_ok(after)
    page.screenshot(path=str(SHOTS / f"{vid}_related_after.png"))
    return r


def pin_one(page, vid: str) -> dict:
    r: dict = {"id": vid, "step": "pin"}
    page.goto(
        f"https://www.youtube.com/watch?v={vid}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)
    for _ in range(5):
        page.mouse.wheel(0, 1100)
        page.wait_for_timeout(500)
    try:
        page.locator("#comments").first.scroll_into_view_if_needed(timeout=4000)
    except Exception:
        pass
    page.wait_for_timeout(1000)
    body = page.locator("body").inner_text()
    if "Pinned by" in body and (
        NEEDLE.lower() in body.lower()
        or "Full film here" in body
        or LONG_ID in body
    ):
        r["ok"] = True
        r["already_pinned"] = True
        return r

    # open comment box
    try:
        page.locator("#simplebox-placeholder").first.click(force=True, timeout=4000)
    except Exception:
        try:
            page.get_by_text(re.compile(r"Add a comment", re.I)).first.click(
                force=True, timeout=4000
            )
        except Exception as e:
            r["error"] = f"no_box:{e}"[:160]
            page.screenshot(path=str(SHOTS / f"{vid}_pin_nobox.png"))
            return r
    page.wait_for_timeout(600)
    try:
        page.locator("#contenteditable-root").first.click(timeout=4000)
        page.keyboard.type(COMMENT, delay=10)
        r["typed"] = True
    except Exception as e:
        ok = page.evaluate(
            """(text) => {
              const el=document.querySelector('#contenteditable-root');
              if(!el) return false;
              el.focus(); el.innerText=text;
              el.dispatchEvent(new InputEvent('input',{bubbles:true}));
              return true;
            }""",
            COMMENT,
        )
        r["typed"] = bool(ok)
        r["type_fallback"] = str(e)[:80]
    page.wait_for_timeout(400)
    r["comment_click"] = page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button, yt-button-shape button')) {
            const t=(b.innerText||'').trim();
            if (/^Comment$/i.test(t) && !b.disabled) { b.click(); return t; }
          }
          return null;
        }"""
    )
    page.wait_for_timeout(3500)
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(4000)
    for _ in range(4):
        page.mouse.wheel(0, 1000)
        page.wait_for_timeout(400)
    body2 = page.locator("body").inner_text()
    r["posted"] = NEEDLE.lower() in body2.lower() or "related video link" in body2.lower()
    if not r["posted"]:
        r["error"] = "not_posted"
        page.screenshot(path=str(SHOTS / f"{vid}_pin_notposted.png"))
        return r

    menu = page.evaluate(
        """(needle) => {
          const nodes=[...document.querySelectorAll('ytd-comment-thread-renderer, ytd-comment-renderer')];
          let target=null;
          for (const n of nodes) {
            const t=(n.innerText||'').toLowerCase();
            if (t.includes(needle) || t.includes('related video link') || t.includes('youtu.be/3xrx')) {
              target=n; break;
            }
          }
          if(!target) return 'no_thread';
          const btn=target.querySelector('#action-menu button, ytd-menu-renderer button, button[aria-label*="Action"], button[aria-label*="More"]');
          if(!btn) return 'no_btn';
          btn.click(); return 'menu';
        }""",
        NEEDLE.lower(),
    )
    r["menu"] = menu
    page.wait_for_timeout(800)
    pinned = False
    for _ in range(2):
        try:
            page.locator("ytd-menu-service-item-renderer, tp-yt-paper-item, yt-list-item-view-model").filter(
                has_text=re.compile(r"^Pin$", re.I)
            ).first.click(timeout=2000)
            pinned = True
            break
        except Exception:
            try:
                page.get_by_text(re.compile(r"^Pin$", re.I)).first.click(
                    force=True, timeout=2000
                )
                pinned = True
                break
            except Exception:
                pass
    r["pin_clicked"] = pinned
    if pinned:
        page.wait_for_timeout(600)
        for name in ("Pin", "Confirm", "OK", "Done"):
            try:
                page.get_by_role("button", name=name, exact=True).first.click(timeout=900)
                page.wait_for_timeout(350)
            except Exception:
                pass
    page.wait_for_timeout(2000)
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(4000)
    for _ in range(4):
        page.mouse.wheel(0, 1000)
        page.wait_for_timeout(400)
    final = page.locator("body").inner_text()
    r["ok"] = ("Pinned by" in final) and (
        NEEDLE.lower() in final.lower()
        or "related video link" in final.lower()
        or LONG_ID in final
    )
    i = final.lower().find("pinned by")
    r["chunk"] = final[i : i + 220].replace("\n", " ") if i >= 0 else ""
    page.screenshot(path=str(SHOTS / f"{vid}_pin_final.png"))
    return r


def main() -> int:
    results = {
        "ok": False,
        "executedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "parentLongId": LONG_ID,
        "requiredRelatedTitle": LONG_TITLE,
        "signedInChannel": {
            "name": "Orbit with Ben",
            "id": "UC_esArsDKd3GJvOkeO0DUog",
        },
        "related": [],
        "pins": [],
        "note": "Force-correct Related away from wrong Short (Time Dilation…) to parent long.",
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.set_viewport_size({"width": 1440, "height": 1100})
        page.add_init_script("window.onbeforeunload=null;")
        page.on("dialog", lambda d: d.accept())

        page.goto(
            "https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(2500)
        if "don't have permission" in page.locator("body").inner_text().lower():
            results["blockedOn"] = "wrong_google_account"
            OUT.write_text(json.dumps(results, indent=2) + "\n")
            return 2

        for vid in SHORTS:
            print(f"RELATED {vid}", flush=True)
            rel = force_related(page, vid)
            results["related"].append(rel)
            print(
                json.dumps(
                    {
                        k: rel.get(k)
                        for k in (
                            "id",
                            "ok",
                            "error",
                            "already_correct",
                            "picked",
                            "after",
                            "search_q",
                        )
                    },
                    ensure_ascii=False,
                )[:700],
                flush=True,
            )

        # Keep known-good pins for first two; attempt remaining
        results["pins"].append(
            {
                "id": "JRfhE6yWom4",
                "ok": True,
                "step": "pin_verify",
                "note": "verified earlier: Full film here → parent long",
            }
        )
        results["pins"].append(
            {
                "id": "L2OFjL4neOo",
                "ok": True,
                "step": "pin_verify",
                "note": "verified earlier: Full film here → parent long",
            }
        )
        for vid in PIN_NEEDED:
            print(f"PIN {vid}", flush=True)
            pin = pin_one(page, vid)
            results["pins"].append(pin)
            print(
                json.dumps(
                    {
                        k: pin.get(k)
                        for k in (
                            "id",
                            "ok",
                            "error",
                            "typed",
                            "comment_click",
                            "posted",
                            "menu",
                            "pin_clicked",
                            "chunk",
                        )
                    },
                    ensure_ascii=False,
                )[:700],
                flush=True,
            )

        page.close()

    results["summary"] = {
        "related_ok": sum(1 for x in results["related"] if x.get("ok")),
        "related_total": len(results["related"]),
        "pin_ok": sum(1 for x in results["pins"] if x.get("ok")),
        "pin_total": len(results["pins"]),
    }
    results["ok"] = (
        results["summary"]["related_ok"] == results["summary"]["related_total"]
        and results["summary"]["pin_ok"] == results["summary"]["pin_total"]
    )
    OUT.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"ok": results["ok"], "summary": results["summary"]}, indent=2))
    return 0 if results["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
