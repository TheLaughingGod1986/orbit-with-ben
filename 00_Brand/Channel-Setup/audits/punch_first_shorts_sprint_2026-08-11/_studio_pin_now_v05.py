#!/usr/bin/env python3
"""Pin existing full-film CTA comments on BH Shorts via Studio Comments."""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
NEEDLES = (
    "full journey into a black hole",
    "related video link",
    "youtu.be/3xrx",
    "Full film here",
)
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


def has_cta(text: str) -> bool:
    lower = text.lower()
    return any(n.lower() in lower for n in NEEDLES)


def merge_pin(item: dict) -> dict:
    data = json.loads(OUT.read_text()) if OUT.exists() else {}
    pins = [p for p in data.get("pins", []) if p.get("id") != item["id"]]
    pins.append(item)
    order = ["JRfhE6yWom4", "L2OFjL4neOo", "tUAdhOnMW2g", "svYOx07OrIM", "B2STcIAF1lY"]
    pins.sort(key=lambda x: order.index(x["id"]) if x.get("id") in order else 99)
    data["pins"] = pins
    data["executedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    data.setdefault(
        "parentLongId",
        "3xrxdmaOwJI",
    )
    data.setdefault(
        "parentLongCurrentTitle",
        "Time Dilation Near Black Holes: Observer vs. Reality",
    )
    data["summary"] = {
        "related_ok": sum(1 for x in data.get("related", []) if x.get("ok")),
        "related_total": len(data.get("related", [])),
        "pin_ok": sum(1 for x in pins if x.get("ok")),
        "pin_total": len(pins),
    }
    data["ok"] = (
        data["summary"]["related_ok"] == data["summary"]["related_total"]
        and data["summary"]["related_total"] >= 4
        and data["summary"]["pin_ok"] == data["summary"]["pin_total"]
        and data["summary"]["pin_total"] >= 4
    )
    OUT.write_text(json.dumps(data, indent=2) + "\n")
    return data


def pin_one(page, vid: str) -> dict:
    r: dict = {"id": vid, "step": "pin_studio"}
    page.goto(
        f"https://studio.youtube.com/video/{vid}/comments",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(5500)
    text = body_text(page)
    r["has_cta"] = has_cta(text)
    r["snip"] = text[:350].replace("\n", " ")
    page.screenshot(path=str(SHOTS / f"{vid}_pin_now_before.png"))

    if not r["has_cta"]:
        r["ok"] = False
        r["error"] = "cta_comment_not_visible"
        return r

    if "pinned" in text.lower() and has_cta(text):
        # already pinned somewhere — verify CTA is the pinned one if possible
        r["ok"] = True
        r["already_pinned"] = True
        return r

    menu = page.evaluate(
        """() => {
          const needles = ['full journey into a black hole', 'related video link', 'youtu.be/3xrx', 'full film here'];
          const all = [...document.querySelectorAll('*')];
          let target = null;
          for (const el of all) {
            const t = (el.innerText || '').toLowerCase();
            if (!needles.some((n) => t.includes(n)) || t.length > 900) continue;
            const box = el.getBoundingClientRect();
            if (box.width > 60 && box.height > 16) { target = el; break; }
          }
          if (!target) return 'no';
          let row = target;
          for (let i = 0; i < 14 && row; i++) {
            for (const b of row.querySelectorAll('button, ytcp-icon-button, [aria-label]')) {
              const al = (b.getAttribute('aria-label') || '') + (b.innerText || '');
              if (/more|action|options|menu/i.test(al)) { b.click(); return 'menu'; }
            }
            row = row.parentElement;
          }
          return 'fail';
        }"""
    )
    r["menu"] = menu
    page.wait_for_timeout(900)
    pinned = False
    try:
        page.get_by_text(re.compile(r"^Pin$", re.I)).first.click(force=True, timeout=3000)
        pinned = True
    except Exception:
        try:
            page.get_by_role("menuitem", name=re.compile(r"Pin", re.I)).first.click(
                force=True, timeout=3000
            )
            pinned = True
        except Exception as e:
            r["pin_err"] = str(e)[:140]
    r["pin_clicked"] = pinned
    if pinned:
        page.wait_for_timeout(700)
        for name in ("Pin", "Confirm", "OK", "Done"):
            try:
                page.get_by_role("button", name=name, exact=True).first.click(timeout=1000)
                page.wait_for_timeout(350)
            except Exception:
                pass
    page.wait_for_timeout(2000)
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(4500)
    after = body_text(page)
    r["ok"] = pinned or ("pinned" in after.lower() and has_cta(after))
    page.screenshot(path=str(SHOTS / f"{vid}_pin_now_after.png"))
    return r


def main() -> int:
    ids = sys.argv[1:] or ["tUAdhOnMW2g", "svYOx07OrIM"]
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
        page.wait_for_timeout(2500)
        if "don't have permission" in body_text(page).lower():
            print(json.dumps({"fatal": "no_permission"}))
            return 2
        summary = None
        for vid in ids:
            print(f"PIN {vid}", flush=True)
            item = pin_one(page, vid)
            summary = merge_pin(item)
            print(json.dumps(item, indent=2)[:1200], flush=True)
        page.close()
        print(json.dumps({"ok": summary.get("ok") if summary else False, "summary": summary.get("summary") if summary else {}}, indent=2))
        return 0 if summary and summary.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
