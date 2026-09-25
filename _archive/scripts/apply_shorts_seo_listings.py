#!/usr/bin/env python3
"""Apply VidIQ-backed Shorts titles, descriptions, and tags in Studio CDP.

Does not open visibility. Does not change dates. No new pins. Zero /go/.
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
CDP = "http://127.0.0.1:9222"
PACK = ROOT / "00_Brand/Channel-Setup/audits/vidiq_optimize_2026-09-03/SHORTS_LISTING_UPDATES.json"
OUT = Path("/tmp/orbit_shorts_seo_apply_result.json")
SHOTS = Path("/tmp/orbit_shorts_seo_apply")


def arg_only() -> str:
    for a in sys.argv[1:]:
        if a.startswith("--only="):
            return a.split("=", 1)[1]
        if a == "--only":
            idx = sys.argv.index(a)
            return sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ""
    return ""


def cdp_list() -> list[dict]:
    try:
        with urllib.request.urlopen(f"{CDP}/json/list", timeout=5) as r:
            return json.loads(r.read())
    except Exception:
        return []


def dismiss(page) -> None:
    for name in ("Got it", "Dismiss", "Not now", "Close"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=600)
        except Exception:
            pass
    page.evaluate("() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())")


def click_save(page) -> bool:
    page.keyboard.press("Tab")
    page.wait_for_timeout(600)
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if btn.count():
            try:
                btn.first.wait_for(state="visible", timeout=2000)
            except Exception:
                pass
            if btn.first.is_enabled():
                btn.first.click(timeout=4000)
                page.wait_for_timeout(2800)
                return True
        btn2 = page.get_by_role("button", name=re.compile(r"^Save changes$", re.I))
        if btn2.count() and btn2.first.is_enabled():
            btn2.first.click(timeout=4000)
            page.wait_for_timeout(2800)
            return True
    except Exception:
        pass
    return False


def set_title(page, title: str) -> bool:
    box = page.get_by_role("textbox", name=re.compile(r"title that describes", re.I))
    if not box.count():
        box = page.locator("#textbox").first
    box.first.click(force=True)
    page.wait_for_timeout(150)
    page.keyboard.press("Meta+a")
    page.keyboard.press("Backspace")
    box.first.fill(title)
    page.wait_for_timeout(200)
    return True


def set_description(page, text: str) -> bool:
    box = page.get_by_role("textbox", name=re.compile(r"tell viewers about your video", re.I))
    if not box.count():
        box = page.locator("#description-textarea #textbox")
    if not box.count():
        return False
    box.first.click(force=True)
    page.wait_for_timeout(150)
    page.keyboard.press("Meta+a")
    page.keyboard.press("Backspace")
    box.first.fill(text)
    page.wait_for_timeout(250)
    return True


def set_tags(page, tags: list[str]) -> str:
    """Add missing tags only. Never click generic Remove — that can wipe Related."""
    page.mouse.wheel(0, 2400)
    page.wait_for_timeout(400)
    for _ in range(2):
        try:
            page.get_by_text("Show more", exact=True).first.click(force=True, timeout=1500)
            page.wait_for_timeout(350)
        except Exception:
            break
    existing = page.evaluate(
        """() => {
          const found = [];
          const walk = (root) => {
            if (!root) return;
            for (const el of root.querySelectorAll('ytcp-chip,yt-formatted-string,#chip-text')) {
              const t = (el.innerText || el.textContent || '').trim();
              if (t && t.length < 80) found.push(t.toLowerCase());
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          walk(document);
          return found;
        }"""
    ) or []
    have = {t.strip().lower() for t in existing}
    tb = page.get_by_role("textbox", name=re.compile(r"^Tags$", re.I))
    if not tb.count():
        return f"have_{len(have)};no_tags_box"
    tb.first.click(force=True)
    page.wait_for_timeout(120)
    packed = []
    used = sum(len(t) + 1 for t in have) if have else 0
    for tag in tags:
        key = tag.strip().lower()
        if key in have:
            continue
        extra = len(tag) + 1
        if used + extra > 420:
            break
        packed.append(tag)
        used += extra
        have.add(key)
    for tag in packed:
        page.keyboard.type(tag, delay=4)
        page.keyboard.press("Enter")
        page.wait_for_timeout(35)
    return f"had_{len(existing)};added_{len(packed)}"


def apply_one(ctx, row: dict, i: int) -> dict:
    vid = row["id"]
    out = {"id": vid, "title": row["title"], "title_set": False, "desc_set": False, "tags": None, "saved": False}
    page = ctx.new_page()
    try:
        page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(2800)
        if "accounts.google.com" in page.url:
            out["error"] = "BLOCKED_NEED_BEN_LOGIN"
            return out
        if f"/video/{vid}/" not in page.url:
            out["error"] = f"url_mismatch:{page.url[:160]}"
            return out
        dismiss(page)
        out["title_set"] = set_title(page, row["title"])
        out["desc_set"] = set_description(page, row["description"])
        out["tags"] = set_tags(page, row.get("tags") or [])
        out["saved"] = click_save(page)
        if not out["saved"]:
            page.wait_for_timeout(800)
            out["saved"] = click_save(page)
        try:
            out["title_now"] = page.get_by_role(
                "textbox", name=re.compile(r"title that describes", re.I)
            ).first.inner_text()[:80]
        except Exception:
            out["title_now"] = None
        shot = SHOTS / f"{i:02d}_{vid}.png"
        page.screenshot(path=str(shot), full_page=False)
        out["screenshot"] = str(shot)
    except Exception as e:
        out["error"] = str(e)[:400]
    finally:
        page.close()
    return out


def main() -> int:
    SHOTS.mkdir(parents=True, exist_ok=True)
    pack = json.loads(PACK.read_text())
    only = set()
    raw_only = arg_only()
    if raw_only:
        only = {x.strip() for x in raw_only.split(",") if x.strip()}
    shorts = [s for s in pack["shorts"] if not only or s["id"] in only]
    report = {
        "task": "shorts_seo_listings",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "cdp_tabs": [t.get("url", "")[:160] for t in cdp_list() if t.get("type") == "page"],
        "studio_results": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        for i, row in enumerate(shorts, start=1):
            print(f"{i:02d} {row['id']}", flush=True)
            result = apply_one(ctx, row, i)
            report["studio_results"].append(result)
            print(json.dumps({k: result.get(k) for k in ("id", "title_set", "desc_set", "tags", "saved", "error", "title_now")}, indent=2), flush=True)
            if result.get("error") == "BLOCKED_NEED_BEN_LOGIN":
                break
            time.sleep(0.35)
    ok = bool(report["studio_results"]) and all(
        r.get("title_set") and r.get("desc_set") and r.get("saved") for r in report["studio_results"]
    )
    report["exit_reason"] = "success" if ok else "partial_or_failed"
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps({"exit": report["exit_reason"], "n": len(report["studio_results"])}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
