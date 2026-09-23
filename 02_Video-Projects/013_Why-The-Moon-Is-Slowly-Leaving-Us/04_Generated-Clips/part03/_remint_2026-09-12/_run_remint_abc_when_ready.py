#!/usr/bin/env python3
"""Mint Moon 013 Part 03 remint plates A/B/C once Flow is signed in as benoats@googlemail.com.

Hard rules:
  - Account MUST be benoats@googlemail.com (never benoats86@gmail.com)
  - Veo 3.1 Fast only
  - Write exactly: p03A_modern_earth.mp4 / p03B_terminator.mp4 / p03C_fossil_rock.mp4
  - Do not overwrite *_LOCKED_*.mp4
  - scenery_only (no Orbit / mascot / text)

Usage (after Flow login is warm on CDP :9222):
  python3 .../_run_remint_abc_when_ready.py --probe
  python3 .../_run_remint_abc_when_ready.py --mint
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
HERE = Path(__file__).resolve().parent
BRIEF = HERE / "REMINT_BRIEF.md"
REQUIRED_ACCOUNT_NEEDLES = ("benoats@googlemail.com",)
FORBIDDEN_ACCOUNT_NEEDLES = ("benoats86@gmail.com", "benoats86")
ENGINE_LABEL = "Veo 3.1 Fast"

PROMPTS = [
    (
        "p03A_modern_earth.mp4",
        "Silent cinematic CGI documentary. Present-day Moon in clean vacuum, then a slow drift revealing whole modern Earth: realistic continents, white clouds, blue oceans on the curved globe, city lights on the night side. Earth is TODAY — no lava cracks, no molten crust, no Hadean magma. Continuous slow camera. No text. No people. No mascot. No flat water plane.",
    ),
    (
        "p03B_terminator.mp4",
        "Silent cinematic CGI. Whole modern Earth from space, terminator line creeping — daylight continents into night city lights. Blue oceans stay on the globe surface. Slow rotation. No lava. No giant Moon on water. No cliffs. No crashing wave. No text. No people. No mascot. No flat water plane.",
    ),
    (
        "p03C_fossil_rock.mp4",
        "Silent macro documentary. Real fossilized coral or limestone on dark rock, dry matte calcium texture, natural growth rings only, museum-specimen lighting. No glowing rings, no neon, no nacre, no polished jewelry, no plastic sheen. Slow push-in. No text. No people. No mascot.",
    ),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def flow_page(browser):
    for ctx in browser.contexts:
        for page in ctx.pages:
            if "flow.google" in (page.url or ""):
                return page
    page = browser.contexts[0].new_page()
    page.goto("https://flow.google.com/", wait_until="domcontentloaded", timeout=60_000)
    return page


def account_guard(page) -> dict:
    body = page.inner_text("body")
    lower = body.lower()
    forbidden = [n for n in FORBIDDEN_ACCOUNT_NEEDLES if n.lower() in lower]
    required_hit = any(n.lower() in lower for n in REQUIRED_ACCOUNT_NEEDLES)
    credits = None
    m = re.search(r"([0-9][0-9,]{2,})\s*credits?", body, re.I)
    if m:
        credits = int(m.group(1).replace(",", ""))
    return {
        "url": page.url,
        "required_account_hint": required_hit,
        "forbidden_account_hit": forbidden,
        "credits": credits,
        "signed_in_guess": "sign in" not in lower[:800].lower(),
        "body_head": body[:400],
    }


def set_prompt(page, text: str) -> None:
    page.evaluate(
        """() => {
          document.querySelectorAll('.cdk-overlay-backdrop').forEach(e => {
            try { e.click(); } catch (err) {}
          });
        }"""
    )
    page.wait_for_timeout(120)
    for _ in range(2):
        page.keyboard.press("Escape")
        page.wait_for_timeout(60)
    box = page.locator('[contenteditable="true"]').first
    box.click(force=True, timeout=8000)
    page.keyboard.press("Meta+A")
    page.keyboard.press("Backspace")
    page.wait_for_timeout(80)
    page.keyboard.insert_text(text)
    page.wait_for_timeout(200)


def click_start(page) -> bool:
    for name in ("Create", "Generate", "Start", "Send"):
        loc = page.get_by_role("button", name=re.compile(name, re.I))
        if loc.count():
            try:
                loc.first.click(timeout=4000)
                return True
            except Exception:
                pass
    return bool(
        page.evaluate(
            """() => {
              const els=[...document.querySelectorAll('button,[role=button]')];
              const el=els.find(e => /^(Create|Generate|Start|Send)$/i.test((e.innerText||'').trim()));
              if(!el) return false; el.click(); return true;
            }"""
        )
    )


def wait_download(page, dest: Path, timeout_s: int = 420) -> Path | None:
    got: list[Path] = []

    def on_download(download):
        target = HERE / f"_dl_{int(time.time())}_{download.suggested_filename}"
        download.save_as(str(target))
        got.append(target)

    page.on("download", on_download)
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if got:
            src = got[-1]
            dest.write_bytes(src.read_bytes())
            return dest
        page.wait_for_timeout(2000)
    return None


def probe(page) -> dict:
    info = account_guard(page)
    info["engine_target"] = ENGINE_LABEL
    info["brief_exists"] = BRIEF.exists()
    info["dest"] = str(HERE)
    info["plates"] = {name: (HERE / name).exists() for name, _ in PROMPTS}
    info["checked_at_utc"] = utc_now()
    return info


def mint(page) -> dict:
    info = probe(page)
    if info["forbidden_account_hit"]:
        raise SystemExit(f"ABORT wrong account markers: {info['forbidden_account_hit']}")
    if not info["signed_in_guess"]:
        raise SystemExit("ABORT Flow does not look signed in — login first")
    results = []
    for name, prompt in PROMPTS:
        dest = HERE / name
        if dest.exists() and dest.stat().st_size > 200_000:
            results.append({"name": name, "status": "already_present", "bytes": dest.stat().st_size})
            continue
        set_prompt(page, prompt)
        try:
            page.get_by_text(re.compile(r"Veo\s*3\.1.*Fast|Fast", re.I)).first.click(timeout=1500)
        except Exception:
            pass
        if not click_start(page):
            results.append({"name": name, "status": "start_click_failed"})
            continue
        shot = HERE / f"mint_{name}.png"
        page.screenshot(path=str(shot))
        landed = wait_download(page, dest)
        if landed and landed.exists():
            results.append(
                {
                    "name": name,
                    "status": "ok",
                    "bytes": landed.stat().st_size,
                    "sha256": file_sha256(landed),
                    "screenshot": str(shot),
                }
            )
        else:
            results.append(
                {
                    "name": name,
                    "status": "pending_manual_download",
                    "note": "Generation started; save MP4 into remint folder with exact filename",
                    "screenshot": str(shot),
                }
            )
    report = {
        "minted_at_utc": utc_now(),
        "account_probe": info,
        "results": results,
    }
    (HERE / "REMINT_RUN_RESULT.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--mint", action="store_true")
    args = ap.parse_args()
    if not args.probe and not args.mint:
        ap.error("pass --probe and/or --mint")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = flow_page(browser)
        page.bring_to_front()
        if args.probe:
            info = probe(page)
            print(json.dumps(info, indent=2))
            (HERE / "REMINT_PROBE.json").write_text(json.dumps(info, indent=2) + "\n")
        if args.mint:
            print(json.dumps(mint(page), indent=2))


if __name__ == "__main__":
    main()
