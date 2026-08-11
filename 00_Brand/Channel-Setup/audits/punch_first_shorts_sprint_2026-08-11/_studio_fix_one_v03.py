#!/usr/bin/env python3
"""Fix BH Short Related → long parent; pin remaining Shorts. One target per run via argv."""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
LONG_ID = "3xrxdmaOwJI"
LONG_PAT = re.compile(r"Fall Into|What Happens If You Fall|3xrxdmaOwJI", re.I)
WRONG_PAT = re.compile(r"Time Dilation Near Black Holes|Observer vs", re.I)
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


def body_text(page) -> str:
    try:
        return page.evaluate("() => document.body ? document.body.innerText : ''") or ""
    except Exception:
        return ""


def related_chunk(text: str) -> str:
    if "Related video" not in text:
        return ""
    return text.split("Related video", 1)[-1][:280].replace("\n", " ")


def related_ok(chunk: str) -> bool:
    if not chunk or chunk.strip().startswith("None"):
        return False
    if WRONG_PAT.search(chunk):
        return False
    return bool(LONG_PAT.search(chunk))


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


def prune_pages(context) -> None:
    pages = list(context.pages)
    # keep first, close extras
    for p in pages[1:]:
        try:
            p.close()
        except Exception:
            pass


def fix_related(page, vid: str) -> dict:
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
    before = related_chunk(body_text(page))
    r["before"] = before[:220]
    if related_ok(before):
        r["ok"] = True
        r["already_correct"] = True
        return r

    page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.55)")
    page.wait_for_timeout(800)
    page.locator("ytcp-shorts-content-links-picker").first.click(force=True, timeout=8000)
    page.wait_for_timeout(1500)
    page.locator("ytcp-video-pick-dialog").wait_for(timeout=20000)
    search = page.locator("ytcp-video-pick-dialog #search-yours")
    if not search.count():
        search = page.get_by_placeholder(re.compile(r"Search", re.I))

    picked = None
    for q in [
        "Orbit",
        "Orbit's Cosmic Journey",
        "What Happens If You Fall Into a Black Hole",
        "Fall Into a Black Hole",
    ]:
        search.first.fill("")
        search.first.fill(q)
        page.wait_for_timeout(2800)
        cards = page.evaluate(
            """() => [...document.querySelectorAll('ytcp-video-pick-dialog ytcp-entity-card, ytcp-video-pick-dialog [role=option]')].map(e => (e.innerText||'').replace(/\\n/g,' | ').slice(0,220))"""
        )
        r.setdefault("searches", []).append({"q": q, "cards": cards[:12]})
        print(f"  search {q!r} -> {cards}", flush=True)
        clicked = page.evaluate(
            """() => {
              const cards=[...document.querySelectorAll('ytcp-video-pick-dialog ytcp-entity-card, ytcp-video-pick-dialog [role=option]')];
              const want=/Fall Into|What Happens If You Fall|3xrxdmaOwJI/i;
              for (const c of cards) {
                const t=c.innerText||'';
                if (want.test(t)) { c.click(); return t.replace(/\\n/g,' | ').slice(0,220); }
              }
              return null;
            }"""
        )
        if clicked:
            picked = clicked
            r["search_q"] = q
            break

    if not picked:
        r["error"] = "long_not_in_picker"
        r["ok"] = False
        page.screenshot(path=str(SHOTS / f"{vid}_related_not_in_picker.png"))
        page.keyboard.press("Escape")
        return r

    r["picked"] = picked
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
    page.wait_for_timeout(3500)
    after = related_chunk(body_text(page))
    r["after"] = after[:220]
    r["ok"] = related_ok(after)
    page.screenshot(path=str(SHOTS / f"{vid}_related_fixed.png"))
    return r


def pin_one(page, vid: str) -> dict:
    r: dict = {"id": vid, "step": "pin"}
    page.goto(
        f"https://www.youtube.com/watch?v={vid}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(5000)
    for _ in range(5):
        page.mouse.wheel(0, 1100)
        page.wait_for_timeout(400)
    try:
        page.locator("#comments").first.scroll_into_view_if_needed(timeout=4000)
    except Exception:
        pass
    body = body_text(page)
    if "Pinned by" in body and (
        NEEDLE.lower() in body.lower() or "Full film here" in body or LONG_ID in body
    ):
        r["ok"] = True
        r["already_pinned"] = True
        return r

    try:
        page.locator("#simplebox-placeholder").first.click(force=True, timeout=5000)
    except Exception:
        page.get_by_text(re.compile(r"Add a comment", re.I)).first.click(
            force=True, timeout=5000
        )
    page.wait_for_timeout(600)
    try:
        page.locator("#contenteditable-root").first.click(timeout=5000)
        page.keyboard.type(COMMENT, delay=8)
        r["typed"] = True
    except Exception:
        r["typed"] = page.evaluate(
            """(text) => {
              const el=document.querySelector('#contenteditable-root');
              if(!el) return false;
              el.focus(); el.innerText=text;
              el.dispatchEvent(new InputEvent('input',{bubbles:true}));
              return true;
            }""",
            COMMENT,
        )
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
    page.wait_for_timeout(4000)
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(4500)
    for _ in range(4):
        page.mouse.wheel(0, 1000)
        page.wait_for_timeout(350)
    body2 = body_text(page)
    r["posted"] = NEEDLE.lower() in body2.lower() or "related video link" in body2.lower()
    if not r["posted"]:
        r["ok"] = False
        r["error"] = "not_posted"
        page.screenshot(path=str(SHOTS / f"{vid}_pin_notposted.png"))
        return r

    r["menu"] = page.evaluate(
        """(needle) => {
          const nodes=[...document.querySelectorAll('ytd-comment-thread-renderer, ytd-comment-renderer')];
          let target=null;
          for (const n of nodes) {
            const t=(n.innerText||'').toLowerCase();
            if (t.includes(needle) || t.includes('related video link') || t.includes('youtu.be/3xrx')) {
              target=n; break;
            }
          }
          if (!target) return 'no_thread';
          const btn=target.querySelector('#action-menu button, ytd-menu-renderer button, button[aria-label*="Action"], button[aria-label*="More"]');
          if (!btn) return 'no_btn';
          btn.click(); return 'menu';
        }""",
        NEEDLE.lower(),
    )
    page.wait_for_timeout(900)
    pinned = False
    try:
        page.locator("ytd-menu-service-item-renderer, tp-yt-paper-item").filter(
            has_text=re.compile(r"^Pin$", re.I)
        ).first.click(timeout=2500)
        pinned = True
    except Exception:
        try:
            page.get_by_text(re.compile(r"^Pin$", re.I)).first.click(
                force=True, timeout=2500
            )
            pinned = True
        except Exception:
            pass
    r["pin_clicked"] = pinned
    if pinned:
        page.wait_for_timeout(700)
        for name in ("Pin", "Confirm", "OK", "Done"):
            try:
                page.get_by_role("button", name=name, exact=True).first.click(timeout=900)
                page.wait_for_timeout(300)
            except Exception:
                pass
    page.wait_for_timeout(1800)
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(4500)
    for _ in range(4):
        page.mouse.wheel(0, 1000)
        page.wait_for_timeout(350)
    final = body_text(page)
    r["ok"] = ("Pinned by" in final) and (
        NEEDLE.lower() in final.lower()
        or "related video link" in final.lower()
        or LONG_ID in final
    )
    i = final.lower().find("pinned by")
    r["chunk"] = final[i : i + 220].replace("\n", " ") if i >= 0 else ""
    page.screenshot(path=str(SHOTS / f"{vid}_pin_final.png"))
    return r


def merge_result(kind: str, item: dict) -> dict:
    data = {}
    if OUT.exists():
        try:
            data = json.loads(OUT.read_text())
        except Exception:
            data = {}
    data.setdefault("parentLongId", LONG_ID)
    data.setdefault(
        "signedInChannel",
        {"name": "Orbit with Ben", "id": "UC_esArsDKd3GJvOkeO0DUog"},
    )
    data["executedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    data["note"] = (
        "Related must be BH long 3xrxdmaOwJI — not Time Dilation Short. "
        "Wrong Related treated as failure."
    )
    key = "related" if kind == "related" else "pins"
    items = [x for x in data.get(key, []) if x.get("id") != item["id"]]
    items.append(item)
    # stable order
    order = ["JRfhE6yWom4", "L2OFjL4neOo", "tUAdhOnMW2g", "svYOx07OrIM"]
    items.sort(key=lambda x: order.index(x["id"]) if x.get("id") in order else 99)
    data[key] = items
    data["summary"] = {
        "related_ok": sum(1 for x in data.get("related", []) if x.get("ok")),
        "related_total": len(data.get("related", [])),
        "pin_ok": sum(1 for x in data.get("pins", []) if x.get("ok")),
        "pin_total": len(data.get("pins", [])),
    }
    data["ok"] = (
        data["summary"]["related_total"] >= 1
        and data["summary"]["related_ok"] == data["summary"]["related_total"]
        and data["summary"]["pin_total"] >= 1
        and data["summary"]["pin_ok"] == data["summary"]["pin_total"]
    )
    OUT.write_text(json.dumps(data, indent=2) + "\n")
    return data


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: script.py related|pin VIDEO_ID")
        return 2
    kind, vid = sys.argv[1], sys.argv[2]
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        prune_pages(ctx)
        page = ctx.new_page()
        page.set_viewport_size({"width": 1400, "height": 1000})
        page.add_init_script("window.onbeforeunload=null;")
        page.on("dialog", lambda d: d.accept())
        # auth check
        page.goto(
            "https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(2500)
        text = body_text(page)
        if "don't have permission" in text.lower():
            print(json.dumps({"fatal": "no_permission"}))
            return 2
        if kind == "related":
            item = fix_related(page, vid)
        elif kind == "pin":
            item = pin_one(page, vid)
        else:
            print("bad kind")
            return 2
        page.close()
        data = merge_result(kind, item)
        print(json.dumps({"item": item, "summary": data.get("summary")}, indent=2)[:2000])
        return 0 if item.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
