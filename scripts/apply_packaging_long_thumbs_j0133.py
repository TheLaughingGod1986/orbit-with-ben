#!/usr/bin/env python3
"""J0133: set the five Packaging §2.B long thumbs in desktop Studio via CDP 9223.

Image-only file inputs. Never Replace / video file. Never thumbnails.set.
No visibility or date dialogs. Skips any video with a Test & Compare running.
Usage: apply_packaging_long_thumbs_j0133.py [--probe] [ids...]
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from apply_melodysheep_long_thumbs_v01 import click_save, dismiss, upload_cover  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CDP = "http://127.0.0.1:9223"
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"
MANIFEST = Path.home() / "_desk/thumb_packaging_1011/MANIFEST.json"
OUT_DIR = Path.home() / "_desk/thumb_packaging_1011/apply"

TEST_RE = re.compile(r"test\s*(&|and)\s*compare|testing thumbnails|test in progress|test results", re.I)


def thumb_section(page) -> dict:
    return page.evaluate(
        """() => {
          const find = (root) => {
            for (const el of root.querySelectorAll('*')) {
              const tag = el.tagName.toLowerCase();
              if (tag.includes('thumbnail') && tag.includes('editor')) return el;
              if (el.shadowRoot) { const r = find(el.shadowRoot); if (r) return r; }
            }
            return null;
          };
          const el = find(document);
          const imgs = el ? [...el.querySelectorAll('img')].map(i => i.src).filter(Boolean) : [];
          return {tag: el ? el.tagName.toLowerCase() : null, text: el ? el.innerText.slice(0, 400) : '', imgs};
        }"""
    )


def channel_id(page) -> str | None:
    return page.evaluate(
        """() => {
          try {
            const c = window.ytcfg && (ytcfg.get('CHANNEL_ID') || (ytcfg.get('CHANNEL') || {}).id);
            if (c) return c;
          } catch (e) {}
          const m = location.href.match(/channel\\/(UC[\\w-]{22})/);
          return m ? m[1] : null;
        }"""
    )


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    probe = "--probe" in sys.argv
    thumbs = json.loads(MANIFEST.read_text())["thumbs"]
    if args:
        thumbs = [t for t in thumbs if t["id"] in args]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = {"job": "J0133", "probe": probe, "started_at": datetime.now(timezone.utc).isoformat(), "results": []}
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx = p.chromium.connect_over_cdp(CDP).contexts[0]
        page = ctx.new_page()
        for t in thumbs:
            vid, cover = t["id"], ROOT / t["file"]
            row = {"id": vid, "text": t["text"], "cover": str(cover),
                   "sha256": hashlib.sha256(cover.read_bytes()).hexdigest() if cover.exists() else None}
            report["results"].append(row)
            try:
                page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=90000)
                page.wait_for_timeout(5000)
                if "accounts.google.com" in page.url:
                    row["error"] = "BLOCKED_NEED_BEN_LOGIN"
                    break
                dismiss(page)
                row["channel"] = channel_id(page)
                before = thumb_section(page)
                row["before"] = before
                body = page.evaluate("() => document.body.innerText")
                if row["channel"] != CHANNEL:
                    row["error"] = f"wrong_channel:{row['channel']}"
                    continue
                if TEST_RE.search(body) or len(before["imgs"]) > 1 and TEST_RE.search(before["text"] or ""):
                    row["skipped"] = "test_and_compare_running"
                    continue
                if probe:
                    continue
                ok, how = upload_cover(page, cover)
                row["uploaded"], row["upload_how"] = ok, how
                if not ok:
                    row["error"] = how
                    continue
                page.wait_for_timeout(2500)
                row["saved"] = click_save(page)
                page.wait_for_timeout(3000)
                page.reload(wait_until="domcontentloaded")
                page.wait_for_timeout(6000)
                after = thumb_section(page)
                row["after"] = after
                row["changed"] = bool(after["imgs"]) and after["imgs"] != before["imgs"]
            except Exception as e:  # noqa: BLE001
                row["error"] = str(e)[:400]
            finally:
                shot = OUT_DIR / f"{'probe' if probe else 'after'}_{vid}.png"
                try:
                    page.screenshot(path=str(shot), full_page=True)
                    row["screenshot"] = str(shot)
                except Exception:
                    pass
                print(json.dumps({k: row.get(k) for k in ("id", "channel", "skipped", "uploaded", "saved", "changed", "error")}), flush=True)
            time.sleep(0.5)
        page.close()
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    (OUT_DIR / ("probe.json" if probe else "result.json")).write_text(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
