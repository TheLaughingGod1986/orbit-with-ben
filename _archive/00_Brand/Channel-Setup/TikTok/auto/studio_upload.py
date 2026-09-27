#!/usr/bin/env python3
"""Orbit TikTok Studio CDP client — post one short via Chrome :9222."""
from __future__ import annotations

import re
import time
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

from upload_block import blocked_result, uploads_paused

UPLOAD = "https://www.tiktok.com/tiktokstudio/upload?from=upload"
CONTENT = "https://www.tiktok.com/tiktokstudio/content"
CDP = "http://127.0.0.1:9222"


def body(page: Page) -> str:
    try:
        return page.inner_text("body")
    except Exception:
        return ""


def click_button(page: Page, *labels: str) -> bool:
    for label in labels:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{re.escape(label)}$", re.I))
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=4000)
                return True
        except Exception:
            pass
    return False


def content_check_limited(page: Page) -> bool:
    t = body(page).lower()
    return "check limit" in t or "reached your check limit" in t


def something_went_wrong(page: Page) -> bool:
    return "Something went wrong" in body(page)


def turn_off_content_check(page: Page) -> bool:
    """Disable Content check lite when present (avoids daily check-limit hard fails)."""
    try:
        return bool(
            page.evaluate(
                """() => {
                  const label=[...document.querySelectorAll('*')].find(
                    e => (e.textContent||'').trim()==='Content check lite'
                  );
                  if (!label) return false;
                  label.scrollIntoView({block:'center'});
                  let root=label;
                  for (let i=0;i<10 && root;i++) {
                    const div=root.querySelector('.Switch__content');
                    const inp=root.querySelector('input.Switch__input, input[role=switch]');
                    if (div || inp) {
                      const on = (div && div.className.includes('checked-true')) ||
                                 (inp && (inp.checked || inp.getAttribute('aria-checked')==='true'));
                      if (!on) return false;
                      if (div) div.click();
                      if (inp) inp.click();
                      return true;
                    }
                    root=root.parentElement;
                  }
                  // Fallback: nearest role=switch by Y
                  const cy=label.getBoundingClientRect().y;
                  const switches=[...document.querySelectorAll(
                    'button[role=switch],[role=switch],input[role=switch]'
                  )];
                  let best=null, bd=1e9;
                  for (const sw of switches) {
                    const r=sw.getBoundingClientRect();
                    const d=Math.abs(r.y-cy);
                    if (d<bd) { best=sw; bd=d; }
                  }
                  if (!best) return false;
                  const checked=(best.getAttribute('aria-checked')||'')==='true' || best.checked;
                  if (checked) { best.click(); return true; }
                  return false;
                }"""
            )
        )
    except Exception:
        return False


def dismiss_modals(page: Page) -> None:
    for _ in range(6):
        text = body(page)
        if "Are you sure that you want to exit" in text:
            click_button(page, "Cancel")
            page.wait_for_timeout(700)
            continue
        if "Turn on automatic content checks" in text:
            # Prefer skipping the check when rate-limited; otherwise Turn on is fine.
            if content_check_limited(page):
                click_button(page, "Not now", "Dismiss", "Cancel")
            else:
                click_button(page, "Turn on")
            page.wait_for_timeout(900)
            continue
        if "Allow your video to be saved" in text:
            click_button(page, "Allow")
            page.wait_for_timeout(900)
            continue
        if "Continue to post" in text or "continue posting before the check" in text:
            click_button(page, "Post now")
            page.wait_for_timeout(1200)
            continue
        click_button(page, "Got it", "Dismiss", "Not now")
        break


def wait_upload_ready(page: Page, timeout_s: float = 180) -> bool:
    end = time.time() + timeout_s
    while time.time() < end:
        dismiss_modals(page)
        if page.locator(
            'div.public-DraftEditor-content[contenteditable="true"]'
        ).count() and "When to post" in body(page):
            return True
        page.wait_for_timeout(1000)
    return False


def fill_caption(page: Page, caption: str) -> bool:
    try:
        editor = page.locator(
            'div.public-DraftEditor-content[contenteditable="true"]'
        ).first
        editor.click(force=True, timeout=5000)
        page.wait_for_timeout(200)
        page.keyboard.press("Meta+a")
        page.keyboard.press("Backspace")
        page.keyboard.type(caption[:2200], delay=2)
        return True
    except Exception:
        return False


def click_post(page: Page) -> bool:
    btns = page.locator("button").filter(has_text=re.compile(r"^Post$"))
    best = None
    best_y = -1.0
    for i in range(btns.count()):
        b = btns.nth(i)
        if not b.is_visible():
            continue
        box = b.bounding_box()
        if box and box["width"] >= 100 and box["y"] > best_y:
            best_y = box["y"]
            best = b
    if best is not None:
        best.click(force=True, timeout=5000)
        return True
    return click_button(page, "Post")


def confirm_posted(page: Page, needle: str, timeout_s: float = 90) -> bool:
    """True when Studio content list contains needle (caption fragment)."""
    end = time.time() + timeout_s
    needle_l = needle.lower()
    while time.time() < end:
        dismiss_modals(page)
        text = body(page)
        if "Video published" in text or "tiktokstudio/content" in page.url:
            if "tiktokstudio/content" not in page.url:
                page.goto(CONTENT, wait_until="domcontentloaded", timeout=90000)
                page.wait_for_timeout(3500)
            if needle_l in body(page).lower():
                return True
        page.wait_for_timeout(1500)
    page.goto(CONTENT, wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(4000)
    return needle_l in body(page).lower()


def post_short(
    *,
    video_path: Path,
    caption: str,
    confirm_needle: str | None = None,
    audit_dir: Path | None = None,
    page: Page | None = None,
) -> dict:
    """Upload + Post now. Returns {status, ...}. Reuses page if provided."""
    if uploads_paused():
        return blocked_result()
    video_path = Path(video_path)
    needle = confirm_needle or caption[:48]
    out: dict = {
        "status": "started",
        "file": str(video_path),
        "caption": caption,
        "needle": needle,
    }
    if not video_path.exists():
        out["status"] = "missing_file"
        return out

    def _safe_dialog(dialog) -> None:
        try:
            dialog.dismiss()
        except Exception:
            try:
                dialog.accept()
            except Exception:
                pass

    own_pw = page is None
    pw = None
    browser = None
    if own_pw:
        pw = sync_playwright().start()
        browser = pw.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        page.on("dialog", _safe_dialog)
        page.bring_to_front()
    else:
        try:
            page.on("dialog", _safe_dialog)
        except Exception:
            pass

    assert page is not None
    try:
        page.goto(UPLOAD, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(1500)
        dismiss_modals(page)
        page.locator('input[type="file"]').first.set_input_files(str(video_path))

        if not wait_upload_ready(page):
            out["status"] = "upload_timeout"
            return out
        dismiss_modals(page)

        out["caption_ok"] = fill_caption(page, caption)
        turn_off_content_check(page)
        try:
            page.locator(
                '[data-e2e="schedule_container"] label:has-text("Now")'
            ).click(force=True, timeout=3000)
        except Exception:
            pass
        dismiss_modals(page)

        if content_check_limited(page):
            out["status"] = "check_limit"
            out["url"] = page.url
            if audit_dir:
                audit_dir.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(audit_dir / f"limit_{video_path.stem}.png"))
            return out

        if audit_dir:
            audit_dir.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(audit_dir / f"before_{video_path.stem}.png"))

        ok = False
        for attempt in range(5):
            if "upload" not in page.url:
                break
            if content_check_limited(page) or something_went_wrong(page):
                out["status"] = (
                    "check_limit" if content_check_limited(page) else "upload_error"
                )
                break
            click_post(page)
            page.wait_for_timeout(1200)
            dismiss_modals(page)
            page.wait_for_timeout(1000)
            dismiss_modals(page)
            if something_went_wrong(page) or content_check_limited(page):
                out["status"] = (
                    "check_limit" if content_check_limited(page) else "upload_error"
                )
                break
            if confirm_posted(page, needle, timeout_s=45):
                ok = True
                break
            out[f"attempt_{attempt+1}"] = "not_confirmed"
            if "upload" not in page.url:
                break

        if audit_dir:
            page.screenshot(path=str(audit_dir / f"after_{video_path.stem}.png"))

        if out.get("status") in {"check_limit", "upload_error"}:
            out["url"] = page.url
            return out
        out["status"] = "ok" if ok else "unconfirmed"
        out["url"] = page.url
        return out
    finally:
        if own_pw:
            try:
                if page:
                    page.close()
            except Exception:
                pass
            if pw:
                pw.stop()
