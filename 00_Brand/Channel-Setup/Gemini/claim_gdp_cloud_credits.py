#!/usr/bin/env python3
"""Claim Google Developer Program monthly Cloud credits onto Main bill acc.

August 2026: credits issued to inactive billing account First
(0124D1-E6EFD6-40F6DA). Gemini API Prepay lives on Main bill acc
(01CE64-7A6ACD-232329). This job selects Main and leaves
"Always use this billing account" on so later months follow.

Uses the same Playwright Google profile as Flow / AI Studio.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = HERE / "gdp_credits_claim.log"
BENEFITS_URL = "https://me.developers.google.com/benefits"
MAIN_ID = "01CE64-7A6ACD-232329"
MAIN_NAME = "Main bill acc"
FIRST_ID = "0124D1-E6EFD6-40F6DA"
PROFILE = Path(
    os.environ.get(
        "ORBIT_AISTUDIO_PROFILE",
        str(Path.home() / "code" / "youtube" / ".playwright-aistudio-profile"),
    )
)


def _log(event: dict) -> None:
    event["ts"] = datetime.now(timezone.utc).isoformat()
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event) + "\n")
    print(json.dumps(event), flush=True)


def _account_text(page) -> str:
    combo = page.get_by_role("combobox", name="Billing account")
    if combo.count():
        return (combo.first.inner_text() or "").strip()
    return page.locator("body").inner_text()[:4000]


def _on_main(text: str) -> bool:
    return MAIN_ID in text or MAIN_NAME.lower() in text.lower()


def main() -> int:
    from playwright.sync_api import TimeoutError as PlaywrightTimeout
    from playwright.sync_api import sync_playwright

    check_only = "--check-only" in sys.argv
    headed = "--headed" in sys.argv or os.environ.get("ORBIT_GDP_HEADED") == "1"
    PROFILE.mkdir(parents=True, exist_ok=True)
    _log({"event": "start", "headed": headed, "check_only": check_only, "profile": str(PROFILE)})

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(PROFILE),
            headless=not headed,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1400, "height": 900},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            page.goto(BENEFITS_URL, wait_until="domcontentloaded", timeout=90_000)
            page.get_by_text("monthly Gen AI", exact=False).wait_for(timeout=60_000)
            page.wait_for_timeout(1500)
            text = _account_text(page)
            _log({"event": "loaded", "account": text[:200]})

            if _on_main(text):
                _log({"event": "already_main", "ok": True, "switched": True})
                return 0
            if check_only:
                _log(
                    {
                        "event": "still_first",
                        "ok": False,
                        "switched": False,
                        "stuck_on": FIRST_ID if FIRST_ID in text else text[:80],
                    }
                )
                return 1

            always = page.get_by_label("Always use this billing account")
            if not always.count():
                always = page.get_by_text("Always use this billing account")
            if always.count():
                always.first.click(timeout=10_000, force=True)
                page.wait_for_timeout(2000)
                err = page.get_by_role("heading", name="Error")
                if err.count() and err.first.is_visible():
                    ok_btn = page.get_by_role("button", name="OK")
                    if ok_btn.count():
                        ok_btn.first.click(timeout=5_000)
                    _log(
                        {
                            "event": "uncheck_failed",
                            "ok": False,
                            "detail": "Google refused to move credits off First onto Main",
                            "stuck_on": FIRST_ID,
                            "claimed": True,
                        }
                    )
                    return 2

            combo = page.get_by_role("combobox", name="Billing account")
            if combo.count() and combo.first.get_attribute("aria-disabled") == "true":
                _log(
                    {
                        "event": "select_locked",
                        "ok": False,
                        "detail": "Billing picker still locked to First",
                        "stuck_on": FIRST_ID,
                        "claimed": True,
                    }
                )
                return 2
            combo.first.click(timeout=10_000)
            page.wait_for_timeout(500)
            option = page.get_by_role("option", name=MAIN_NAME)
            if not option.count():
                option = page.get_by_text(MAIN_ID)
            option.first.click(timeout=10_000)
            page.wait_for_timeout(1500)

            if always.count() and not always.first.is_checked():
                always.first.click(timeout=10_000)
                page.wait_for_timeout(1500)

            text = _account_text(page)
            ok = _on_main(text)
            _log({"event": "applied", "ok": ok, "account": text[:200]})
            return 0 if ok else 3
        except PlaywrightTimeout as exc:
            _log({"event": "timeout", "ok": False, "error": str(exc)[:400]})
            return 4
        except Exception as exc:
            _log({"event": "error", "ok": False, "error": f"{type(exc).__name__}: {exc}"[:400]})
            return 5
        finally:
            ctx.close()


if __name__ == "__main__":
    raise SystemExit(main())
