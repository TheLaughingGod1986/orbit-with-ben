#!/usr/bin/env python3
"""Pin full-film CTA via Studio Comments / Shorts UI."""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
LONG_ID = "3xrxdmaOwJI"
COMMENT = (
    "Want to see the full journey into a black hole? "
    "Watch the complete episode using the related video link 👇\n"
    f"https://youtu.be/{LONG_ID}"
)
NEEDLE = "full journey into a black hole"
OUT = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/audits/"
    "punch_first_shorts_sprint_2026-08-11/STUDIO_RELATED_PIN_RESULT.json"
)
SHOTS = Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/audits/"
    "punch_first_shorts_sprint_2026-08-11/studio_finish_shots"
)
SHOTS.mkdir(parents=True, exist_ok=True)


def body_text(page) -> str:
    try:
        return page.evaluate("() => document.body ? document.body.innerText : ''") or ""
    except Exception:
        return ""


def merge_pin(item: dict) -> None:
    data = json.loads(OUT.read_text()) if OUT.exists() else {}
    pins = [p for p in data.get("pins", []) if p.get("id") != item["id"]]
    pins.append(item)
    order = ["JRfhE6yWom4", "L2OFjL4neOo", "tUAdhOnMW2g", "svYOx07OrIM"]
    pins.sort(key=lambda x: order.index(x["id"]) if x.get("id") in order else 99)
    data["pins"] = pins
    data["executedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    data["summary"] = {
        "related_ok": sum(1 for x in data.get("related", []) if x.get("ok")),
        "related_total": len(data.get("related", [])),
        "pin_ok": sum(1 for x in pins if x.get("ok")),
        "pin_total": len(pins),
    }
    data["ok"] = (
        data["summary"]["related_ok"] == data["summary"]["related_total"]
        and data["summary"]["related_total"] == 4
        and data["summary"]["pin_ok"] == data["summary"]["pin_total"]
        and data["summary"]["pin_total"] == 4
    )
    OUT.write_text(json.dumps(data, indent=2) + "\n")


def pin_via_studio(page, vid: str) -> dict:
    r: dict = {"id": vid, "step": "pin_studio"}
    for url in (
        f"https://www.youtube.com/shorts/{vid}",
        f"https://www.youtube.com/watch?v={vid}",
    ):
        page.goto(url, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(3500)
        t = body_text(page)
        if "Pinned by" in t and (
            NEEDLE.lower() in t.lower() or "Full film here" in t or LONG_ID in t
        ):
            r["ok"] = True
            r["already_pinned"] = True
            r["checked_url"] = url
            return r

    # Post via classic watch page using evaluate clicks (more reliable)
    page.goto(
        f"https://www.youtube.com/watch?v={vid}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(5000)
    for _ in range(6):
        page.mouse.wheel(0, 1200)
        page.wait_for_timeout(400)
    try:
        page.locator("#comments").first.scroll_into_view_if_needed(timeout=5000)
    except Exception:
        pass
    page.wait_for_timeout(1000)

    box = page.evaluate(
        """() => {
          const ph=document.querySelector('#simplebox-placeholder, #placeholder-area');
          if (!ph) return null;
          ph.scrollIntoView({block:'center'});
          ph.click();
          return 'clicked';
        }"""
    )
    r["box"] = box
    page.wait_for_timeout(700)
    typed = page.evaluate(
        """(text) => {
          const el=document.querySelector('#contenteditable-root');
          if(!el) return false;
          el.focus();
          el.innerText=text;
          el.dispatchEvent(new InputEvent('input',{bubbles:true}));
          return true;
        }""",
        COMMENT,
    )
    r["typed"] = typed
    if typed:
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

    # Pin in Studio
    page.goto(
        f"https://studio.youtube.com/video/{vid}/comments",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(5000)
    text = body_text(page)
    r["studio_has"] = (
        NEEDLE.lower() in text.lower()
        or "related video link" in text.lower()
        or "Full film here" in text
    )
    page.screenshot(path=str(SHOTS / f"{vid}_studio_comments.png"))

    if not r["studio_has"]:
        # try studio compose
        try:
            page.get_by_text(re.compile(r"Add a comment|Comment as", re.I)).first.click(
                timeout=3000
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
            page.wait_for_timeout(3000)
            text = body_text(page)
            r["studio_has"] = NEEDLE.lower() in text.lower() or "related video link" in text.lower()
        except Exception as e:
            r["studio_post_err"] = str(e)[:160]

    if not r.get("studio_has"):
        r["ok"] = False
        r["error"] = "comment_not_found"
        return r

    if "pinned" in text.lower():
        r["ok"] = True
        r["already_pinned"] = True
        return r

    menu = page.evaluate(
        """(needle) => {
          const all=[...document.querySelectorAll('*')];
          let target=null;
          for (const el of all) {
            const t=(el.innerText||'');
            if ((t.toLowerCase().includes(needle) || t.includes('Full film') || t.includes('youtu.be/3xrx')) && t.length < 900) {
              const r=el.getBoundingClientRect();
              if (r.width>60 && r.height>16) { target=el; break; }
            }
          }
          if (!target) return 'no';
          let row=target;
          for (let i=0;i<14 && row;i++) {
            for (const b of row.querySelectorAll('button, ytcp-icon-button, [aria-label]')) {
              const al=(b.getAttribute('aria-label')||'')+(b.innerText||'');
              if (/more|action|options|menu/i.test(al)) { b.click(); return 'menu'; }
            }
            row=row.parentElement;
          }
          return 'fail';
        }""",
        NEEDLE.lower(),
    )
    r["menu"] = menu
    page.wait_for_timeout(800)
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
    r["pin_clicked"] = pinned
    if pinned:
        page.wait_for_timeout(600)
        for name in ("Pin", "Confirm", "OK", "Done"):
            try:
                page.get_by_role("button", name=name, exact=True).first.click(timeout=900)
                page.wait_for_timeout(300)
            except Exception:
                pass
    page.wait_for_timeout(2000)
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(4000)
    after = body_text(page)
    r["ok"] = pinned or (
        "pinned" in after.lower()
        and (
            NEEDLE.lower() in after.lower()
            or "Full film" in after
            or LONG_ID in after
        )
    )
    page.screenshot(path=str(SHOTS / f"{vid}_pin_studio_after.png"))
    return r


def main() -> int:
    vid = sys.argv[1]
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        for pg in list(ctx.pages)[1:]:
            try:
                pg.close()
            except Exception:
                pass
        page = ctx.new_page()
        page.set_viewport_size({"width": 1400, "height": 1000})
        page.add_init_script("window.onbeforeunload=null;")
        page.on("dialog", lambda d: d.accept())
        page.goto(
            "https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(2000)
        if "don't have permission" in body_text(page).lower():
            print(json.dumps({"fatal": "no_permission"}))
            return 2
        item = pin_via_studio(page, vid)
        page.close()
        merge_pin(item)
        print(json.dumps(item, indent=2)[:2000], flush=True)
        return 0 if item.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
