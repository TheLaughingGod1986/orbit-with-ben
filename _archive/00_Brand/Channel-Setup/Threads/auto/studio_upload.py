#!/usr/bin/env python3
"""
Orbit Threads CDP client — post one short as a Threads video via Chrome.

Uses the logged-in @orbitwithben session (port 9222 by default).
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

_AUTO = Path(__file__).resolve().parent
if str(_AUTO) not in sys.path:
    sys.path.insert(0, str(_AUTO))

from playwright.sync_api import Page, sync_playwright


import importlib.util as _ilu
from pathlib import Path as _P
def _threads_load(name: str):
    auto = _P(__file__).resolve().parent
    key = f"orbit_threads_auto_{name}"
    import sys as _sys
    if key in _sys.modules:
        return _sys.modules[key]
    path = auto / f"{name}.py"
    spec = _ilu.spec_from_file_location(key, path)
    mod = _ilu.module_from_spec(spec)
    _sys.modules[key] = mod
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod

load = _threads_load

config = load("config")

# Prefer threads.com (threads.net redirects here; some CDP sessions abort mid-redirect).
HOME = "https://www.threads.com/"
PROFILE_TMPL = "https://www.threads.com/@{username}"


def body(page: Page) -> str:
    try:
        return page.inner_text("body")
    except Exception:
        return ""


def click_text(page: Page, *labels: str) -> bool:
    for label in labels:
        try:
            b = page.get_by_role(
                "button", name=re.compile(rf"^{re.escape(label)}$", re.I)
            )
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=4000)
                return True
        except Exception:
            pass
        try:
            loc = page.get_by_text(label, exact=True)
            if loc.count():
                loc.first.click(force=True, timeout=4000)
                return True
        except Exception:
            pass
    return False


def dismiss(page: Page) -> None:
    for label in ("Not now", "Close", "Got it", "Dismiss", "Skip"):
        click_text(page, label)


def fill_caption(page: Page, caption: str) -> bool:
    selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[aria-label*="Empty text field" i][contenteditable="true"]',
        'div[contenteditable="true"]',
    ]
    for sel in selectors:
        try:
            el = page.locator(sel).first
            if not el.count():
                continue
            el.click(force=True, timeout=4000)
            page.wait_for_timeout(200)
            page.keyboard.press("Meta+a")
            page.keyboard.press("Backspace")
            page.keyboard.type(caption[:480], delay=2)
            return True
        except Exception:
            continue
    return False


def _attach_media(page: Page, video_path: Path) -> bool:
    file_input = page.locator("input[type=file]")
    if file_input.count():
        try:
            file_input.first.set_input_files(str(video_path))
            return True
        except Exception:
            pass

    # Open media picker then set files
    page.evaluate(
        """() => {
                          for (const el of document.querySelectorAll('[aria-label],[role=button],button,svg')) {
                            const a=(el.getAttribute('aria-label')||'').toLowerCase();
                            if (/photo|video|media|gallery|attach|image/.test(a)) {
                              (el.closest('button,[role=button]')||el).click();
                              return a;
                            }
                          }
                        }"""
    )
    page.wait_for_timeout(800)
    file_input = page.locator("input[type=file]")
    if not file_input.count():
        return False
    try:
        file_input.first.set_input_files(str(video_path))
        return True
    except Exception as e:
        raise RuntimeError(f"upload_error: {e}") from e


def _click_post(page: Page) -> str | None:
    clicked = page.evaluate(
        """() => {
                  for (const b of document.querySelectorAll('button,[role=button]')) {
                    const t=(b.innerText||'').trim();
                    if (/^(Post|Publish|Share)$/i.test(t)) { b.click(); return t; }
                  }
                  return null;
                }"""
    )
    if clicked:
        return clicked
    if click_text(page, "Post", "Publish", "Share"):
        return "Post"
    return None


def post_short(
    *,
    video_path: Path,
    caption: str,
    confirm_needle: str | None = None,
    audit_dir: Path | None = None,
    page: Page | None = None,
    port: int | None = None,
) -> dict:
    video_path = Path(video_path)
    needle = confirm_needle or caption[:48]
    creds = config.load_credentials()
    port = int(port or creds.get("cdp_port") or 9222)
    username = creds.get("threads_username") or creds.get("username") or "orbitwithben"
    out: dict = {
        "status": "failed",
        "method": "cdp",
        "file": str(video_path),
        "caption": caption,
        "needle": needle,
        "port": port,
    }
    if not video_path.exists():
        out["status"] = "missing_file"
        out["error"] = f"missing file: {video_path}"
        return out

    own_pw = page is None
    pw = None
    if own_pw:
        pw = sync_playwright().start()
        browser = pw.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
        ctx = browser.contexts[0]

        def _dialog(d):
            try:
                d.dismiss()
            except Exception:
                try:
                    d.accept()
                except Exception:
                    pass

        ctx.on("dialog", _dialog)
        page = ctx.new_page()
        page.on("dialog", _dialog)
        page.bring_to_front()

    assert page is not None
    try:
        def _dialog2(d):
            try:
                d.dismiss()
            except Exception:
                try:
                    d.accept()
                except Exception:
                    pass

        try:
            page.on("dialog", _dialog2)
        except Exception:
            pass
        def goto_retry(url: str, *, timeout: int = 120000, tries: int = 3) -> None:
            """Navigate with retries. Stay on threads.com only — .net redirects abort CDP."""
            last: Exception | None = None
            # Normalize any .net URL to .com
            url = url.replace("https://www.threads.net", "https://www.threads.com")
            for i in range(tries):
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=timeout)
                    return
                except Exception as e:
                    last = e
                    # ERR_ABORTED often still lands on the page
                    if "threads.com" in (page.url or ""):
                        return
                    page.wait_for_timeout(1500 * (i + 1))
            assert last is not None
            raise last

        goto_retry(HOME)
        page.wait_for_timeout(2000)
        dismiss(page)

        text = body(page)
        if "Log in" in text and "Edit profile" not in text and f"@{username}" not in text.lower():
            # Soft check — profile nav usually present when logged in
            if "Profile" not in text and "New thread" not in text:
                out["status"] = "threads_not_logged_in"
                if audit_dir:
                    audit_dir.mkdir(parents=True, exist_ok=True)
                    page.screenshot(path=str(audit_dir / "not_logged_in.png"))
                return out

        # Open composer
        opened = click_text(page, "New thread", "Create")
        if not opened:
            try:
                page.get_by_label(
                    "Empty text field. Type to compose a new post."
                ).first.click(timeout=4000)
                opened = True
            except Exception:
                pass
        page.wait_for_timeout(1200)

        try:
            attached = _attach_media(page, video_path)
        except RuntimeError as e:
            out["status"] = "upload_failed"
            out["error"] = str(e)
            if audit_dir:
                audit_dir.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(audit_dir / "upload_fail.png"))
            return out

        if not attached:
            out["status"] = "upload_failed"
            out["error"] = "no file input"
            if audit_dir:
                audit_dir.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(audit_dir / "upload_fail.png"))
            return out

        # Wait for a real video preview (not just a YouTube link-card image).
        video_ready = False
        for _ in range(45):
            txt = body(page)
            if re.search(r"Failed to upload attachment|couldn't upload|upload failed", txt, re.I):
                out["status"] = "upload_failed"
                out["error"] = "Failed to upload attachment"
                if audit_dir:
                    audit_dir.mkdir(parents=True, exist_ok=True)
                    page.screenshot(path=str(audit_dir / "upload_fail.png"))
                return out
            try:
                if page.locator('[role="dialog"] video, video').count():
                    video_ready = True
                    break
            except Exception:
                pass
            page.wait_for_timeout(2000)
        out["video_ready"] = video_ready
        if not video_ready:
            out["status"] = "upload_failed"
            out["error"] = "no video preview after attach"
            if audit_dir:
                audit_dir.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(audit_dir / "upload_fail.png"))
            return out

        # Prefer caption without a raw youtu.be URL — bare URLs often become
        # link cards and crowd out / replace the attached video.
        safe_caption = caption
        if "youtu.be/" in caption or "youtube.com/" in caption:
            safe_caption = re.sub(
                r"https?://(?:www\.)?(?:youtu\.be/\S+|youtube\.com/\S+)",
                "",
                caption,
            ).strip()
            safe_caption = re.sub(r"\n{3,}", "\n\n", safe_caption)
            out["caption_stripped_url"] = True
        out["caption_ok"] = fill_caption(page, safe_caption)
        if audit_dir:
            audit_dir.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(audit_dir / f"before_{video_path.stem}.png"))

        posted = False
        for attempt in range(5):
            label = _click_post(page)
            out[f"attempt_{attempt + 1}"] = label or "no_button"
            page.wait_for_timeout(2500)
            dismiss(page)
            txt = body(page).lower()
            if "failed to upload attachment" in txt:
                out["status"] = "upload_failed"
                out["error"] = "Failed to upload attachment (after Post)"
                if audit_dir:
                    audit_dir.mkdir(parents=True, exist_ok=True)
                    page.screenshot(path=str(audit_dir / "after_post.png"))
                return out
            if "posting" in txt:
                # Give Threads time to finish the upload+publish spinner.
                page.wait_for_timeout(15000)
                txt = body(page).lower()
            if needle.lower() in txt or "view" in txt or "posted" in txt:
                # Composer usually closes after success
                if page.locator('text=New thread').count() == 0 or "What's new?" in body(page):
                    posted = True
                    break
            # If composer gone, treat as posted click
            if "cancel" not in txt.lower() or page.locator('text=Cancel').count() == 0:
                if label:
                    posted = True
                    break

        if audit_dir:
            page.screenshot(path=str(audit_dir / "after_post.png"))

        # Confirm on profile — require the needle AND a video element nearby when possible.
        goto_retry(PROFILE_TMPL.format(username=username), timeout=90000)
        page.wait_for_timeout(4000)
        profile_txt = body(page)
        confirmed = needle.lower() in profile_txt.lower()
        has_video = False
        try:
            has_video = page.locator("video").count() > 0
        except Exception:
            pass
        out["url"] = page.url
        out["profile_has_video"] = has_video
        if confirmed and has_video:
            out["status"] = "ok"
        elif confirmed:
            # Text/link card only — do not treat as a successful video mirror.
            out["status"] = "link_or_text_only"
        elif posted:
            out["status"] = "unconfirmed"
        else:
            out["status"] = "failed"
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
