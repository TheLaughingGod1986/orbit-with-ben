#!/usr/bin/env python3
"""
Orbit Meta Business Suite CDP client — post one Reel via Chrome.

Fallback when Graph API credentials / App Review are not ready.
Posts cross-post targets depending on what's selected in the logged-in Suite
session (Facebook Page + Instagram professional).
"""
from __future__ import annotations

import re
import time
from pathlib import Path

import sys
from pathlib import Path as _Path

_AUTO = _Path(__file__).resolve().parent
if str(_AUTO) not in sys.path:
    sys.path.insert(0, str(_AUTO))

from playwright.sync_api import Page, sync_playwright

from _sib import load

config = load("config")
suite_ids = load("suite_ids")

COMPOSER = suite_ids.COMPOSER_PATH
CONTENT = suite_ids.CONTENT_PATH


def suite_url(base: str, creds: dict) -> str:
    """Pin CDP navigation to the Orbit portfolio + Page asset."""
    return suite_ids.suite_url(base, creds)


def body(page: Page) -> str:
    try:
        return page.inner_text("body")
    except Exception:
        return ""


def click_button(page: Page, *labels: str) -> bool:
    for label in labels:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{re.escape(label)}$", re.I))
            if b.count() and b.first.is_visible() and b.first.is_enabled():
                b.first.click(timeout=4000)
                return True
        except Exception:
            pass
        try:
            loc = page.locator(f'button:has-text("{label}")').first
            if loc.count() and loc.is_visible() and loc.is_enabled():
                loc.click(timeout=4000)
                return True
        except Exception:
            pass
        # Business Suite primary actions are often DIVs (not <button>), e.g. Next / Share.
        try:
            hit = page.evaluate(
                """(label) => {
                  const hits=[];
                  for (const el of document.querySelectorAll('button,div,span,[role=button]')) {
                    const t=(el.innerText||'').trim();
                    if (t!==label) continue;
                    const r=el.getBoundingClientRect();
                    if (r.width<15 || r.height<10 || r.width>300) continue;
                    const disabled =
                      el.getAttribute('aria-disabled') === 'true' ||
                      el.hasAttribute('disabled');
                    if (disabled) continue;
                    const s=getComputedStyle(el);
                    if (Number(s.opacity || 1) < 0.55) continue;
                    hits.push({
                      x:r.x+r.width/2, y:r.y+r.height/2,
                      bg:s.backgroundColor||'', y0:Math.round(r.y), x0:Math.round(r.x)
                    });
                  }
                  if (!hits.length) return null;
                  hits.sort((a,b)=>{
                    const blue=h=>/10,\\s*120,\\s*190|0,\\s*97,\\s*160|24,\\s*119/.test(h.bg)?1:0;
                    return (blue(a)-blue(b)) || (a.y0-b.y0) || (a.x0-b.x0);
                  });
                  return hits[hits.length-1];
                }""",
                label,
            )
            if hit:
                page.mouse.move(hit["x"], hit["y"])
                page.wait_for_timeout(120)
                page.mouse.down()
                page.wait_for_timeout(50)
                page.mouse.up()
                page.wait_for_timeout(800)
                return True
        except Exception:
            pass
    return False


def stay_on_composer(page: Page) -> None:
    """Never discard a reel draft. Suite 'Leave Page?' must stay."""
    page.evaluate(
        """() => {
          for (const el of document.querySelectorAll('button,[role=button],div,span')) {
            const t = (el.innerText || '').trim();
            if (t === 'Continue editing') { el.click(); return 'continue'; }
          }
          return null;
        }"""
    )


def dismiss_modals(page: Page) -> None:
    stay_on_composer(page)
    for label in (
        "Continue editing",
        "Not now",
        "Got it",
        "Dismiss",
        "Skip",
    ):
        click_button(page, label)
    stay_on_composer(page)


def fill_caption(page: Page, caption: str) -> bool:
    selectors = [
        'div[aria-label*="Tell viewers" i][contenteditable="true"]',
        'div[aria-label*="what your reel" i][contenteditable="true"]',
        'div[aria-label*="caption" i][contenteditable="true"]',
        'div[aria-label*="Write" i][contenteditable="true"]',
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"]',
        'textarea[placeholder*="caption" i]',
        'textarea[aria-label*="caption" i]',
        'textarea[placeholder*="reel" i]',
        'textarea',
    ]
    # Prefer the Text field in reels composer (not title)
    try:
        text_label = page.get_by_text("Text (optional)", exact=False)
        if text_label.count():
            text_label.first.click(force=True, timeout=2000)
            page.wait_for_timeout(200)
    except Exception:
        pass
    for sel in selectors:
        try:
            el = page.locator(sel).first
            if not el.count():
                continue
            el.click(force=True, timeout=4000)
            page.wait_for_timeout(200)
            page.keyboard.press("Meta+a")
            page.keyboard.press("Backspace")
            page.keyboard.type(caption[:2100], delay=2)
            return True
        except Exception:
            continue
    # JS fallback
    ok = page.evaluate(
        """(cap) => {
          const nodes=[...document.querySelectorAll('div[contenteditable="true"], textarea')];
          // Prefer larger text areas
          nodes.sort((a,b)=> (b.getBoundingClientRect().height*b.getBoundingClientRect().width)
            - (a.getBoundingClientRect().height*a.getBoundingClientRect().width));
          for (const el of nodes) {
            const r=el.getBoundingClientRect();
            if (r.width < 80 || r.height < 20) continue;
            el.focus();
            if (el.tagName === 'TEXTAREA') el.value = cap;
            else el.textContent = cap;
            el.dispatchEvent(new InputEvent('input', {bubbles:true, data:cap, inputType:'insertText'}));
            el.dispatchEvent(new Event('change', {bubbles:true}));
            return true;
          }
          return false;
        }""",
        caption[:2100],
    )
    return bool(ok)


def wait_upload_ready(page: Page, timeout_s: float = 180) -> bool:
    end = time.time() + timeout_s
    while time.time() < end:
        dismiss_modals(page)
        text = body(page).lower()
        if any(
            x in text
            for x in (
                "share reel",
                "publish",
                "next",
                "add a caption",
                "write a caption",
                "reel details",
            )
        ):
            # Prefer presence of caption box or Share/Publish
            if page.locator('div[contenteditable="true"], textarea').count():
                return True
            if page.get_by_role("button", name=re.compile(r"Share|Publish|Next", re.I)).count():
                return True
        page.wait_for_timeout(1000)
    return False


def click_share_cta(page: Page) -> bool:
    """Click the bottom Share / Publish button — never the step-indicator spinner."""
    try:
        hit = page.evaluate(
            """() => {
              const labels = new Set(['Share', 'Share reel', 'Publish', 'Post']);
              const viewportH = window.innerHeight || 800;
              const hits = [];
              for (const el of document.querySelectorAll('button,div[role=button],[role=button]')) {
                const t = (el.innerText || '').trim();
                if (!labels.has(t)) continue;
                const r = el.getBoundingClientRect();
                if (r.width < 40 || r.height < 24 || r.width > 280) continue;
                if (r.y < viewportH * 0.55) continue;
                const s = getComputedStyle(el);
                if (s.visibility === 'hidden' || s.display === 'none') continue;
                const disabled =
                  el.getAttribute('aria-disabled') === 'true' ||
                  el.hasAttribute('disabled') ||
                  Number(s.opacity || 1) < 0.5;
                if (disabled) continue;
                hits.push({
                  x: r.x + r.width / 2,
                  y: r.y + r.height / 2,
                  y0: Math.round(r.y),
                  x0: Math.round(r.x),
                  bg: s.backgroundColor || '',
                });
              }
              if (!hits.length) return null;
              hits.sort((a, b) => (a.y0 - b.y0) || (a.x0 - b.x0));
              return hits[hits.length - 1];
            }"""
        )
        if hit:
            page.mouse.move(hit["x"], hit["y"])
            page.wait_for_timeout(120)
            page.mouse.down()
            page.wait_for_timeout(50)
            page.mouse.up()
            page.wait_for_timeout(800)
            return True
    except Exception:
        pass
    return False


def share_controls_state(page: Page) -> dict:
    try:
        return page.evaluate(
            """() => {
              const text = (document.body && document.body.innerText) || '';
              const radios = [...document.querySelectorAll('input[type=radio]')];
              const disabledRadios = radios.filter(r =>
                r.disabled || r.getAttribute('aria-disabled') === 'true'
              );
              const spinner = !!document.querySelector(
                '[role=progressbar], [aria-busy=true]'
              );
              return {
                radioCount: radios.length,
                disabledRadioCount: disabledRadios.length,
                spinner,
                pageOnly: /only available for posts to a Facebook Page/i.test(text),
                whoCanSee: /Who can see this/i.test(text),
              };
            }"""
        )
    except Exception:
        return {}


def try_select_facebook_page_destination(page: Page) -> bool:
    """If Suite is on Instagram-only, switch Post-to to the Orbit Facebook Page."""
    try:
        return bool(
            page.evaluate(
                """() => {
                  const labels = [
                    'Facebook Page',
                    'Post to Facebook',
                  ];
                  for (const lab of labels) {
                    const el = [...document.querySelectorAll(
                      'input[type=checkbox],input[type=radio],[role=checkbox],[role=switch]'
                    )].find(e => {
                      const t = ((e.innerText || '') + ' ' + (e.getAttribute('aria-label') || '')).trim();
                      return t.includes(lab);
                    });
                    if (!el) continue;
                    const checked =
                      el.checked === true ||
                      el.getAttribute('aria-checked') === 'true';
                    if (checked) return true;
                    el.click();
                    return true;
                  }
                  return false;
                }"""
            )
        )
    except Exception:
        return False


def discard_leftover_draft(page: Page) -> None:
    """Clear a stuck previous reel only when media is already attached."""
    dismiss_modals(page)
    text = body(page).lower()
    leftover = any(
        x in text
        for x in (
            "replace video",
            "remove video",
            "safe to publish",
            "replace media",
        )
    )
    if not leftover:
        return
    for label in ("Discard", "Discard reel", "Start over", "Remove video"):
        click_button(page, label)
        page.wait_for_timeout(400)
    dismiss_modals(page)


def attach_video(page: Page, video_path: Path) -> bool:
    """Attach an mp4 via hidden file input or the Media 'Add video' chooser."""
    video_path = Path(video_path)
    inputs = page.locator('input[type="file"]')
    try:
        n = inputs.count()
    except Exception:
        n = 0
    for i in range(n):
        el = inputs.nth(i)
        try:
            accept = (el.get_attribute("accept") or "").lower()
            if accept and "video" not in accept and "image" in accept:
                continue
            el.set_input_files(str(video_path))
            page.wait_for_timeout(800)
            return True
        except Exception:
            continue

    # Dismiss the "Please add video" Next tooltip so it does not eat the click.
    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
    except Exception:
        pass

    locators = [
        page.get_by_role("button", name=re.compile(r"^Add video$", re.I)),
        page.locator('div[role="button"]:has-text("Add video")'),
        page.get_by_text("Add video", exact=True),
    ]
    for loc in locators:
        try:
            if not loc.count():
                continue
            with page.expect_file_chooser(timeout=15000) as fc_info:
                loc.first.click(timeout=4000)
            fc_info.value.set_files(str(video_path))
            page.wait_for_timeout(800)
            return True
        except Exception:
            continue
    return False


def wait_details_ready(page: Page, timeout_s: float = 90) -> bool:
    """Wait until a video is attached and processing finishes."""
    end = time.time() + timeout_s
    while time.time() < end:
        stay_on_composer(page)
        text = body(page).lower()
        processing = any(
            x in text
            for x in (
                "processing",
                "checking for copyright",
                "uploading",
                "still working",
            )
        )
        attached = any(
            x in text
            for x in (
                "safe to publish",
                "replace video",
                "remove video",
                "replace media",
                "1080",
                "1920",
            )
        )
        if attached and not processing:
            return True
        page.wait_for_timeout(1000)
    return False


def advance_to_share(page: Page, timeout_s: float = 75) -> dict:
    """Keep hitting Next until Share is interactive, or diagnose a hang."""
    end = time.time() + timeout_s
    last: dict = {"state": "unknown", "needs_page_asset": False, "reasons": [], "hint": ""}
    while time.time() < end:
        dismiss_modals(page)
        last = suite_ids.diagnose_share_step(body(page), page.url)
        if last.get("state") in {"ready", "details_ready"}:
            if last.get("state") == "details_ready":
                click_button(page, "Next")
                page.wait_for_timeout(1800)
                last = suite_ids.diagnose_share_step(body(page), page.url)
                if last.get("state") == "ready":
                    return last
                continue
            return last
        if last.get("state") == "hung_wrong_asset":
            if try_select_facebook_page_destination(page):
                page.wait_for_timeout(1200)
            click_button(page, "Next")
            page.wait_for_timeout(1500)
            continue
        click_button(page, "Next")
        page.wait_for_timeout(1800)
        last = wait_share_ready(page, timeout_s=8)
        if last.get("state") == "ready":
            return last
    return last


def wait_share_ready(page: Page, timeout_s: float = 45) -> dict:
    """Wait until Share is interactive, or diagnose a wrong-asset hang."""
    end = time.time() + timeout_s
    last: dict = {"state": "unknown", "needs_page_asset": False, "reasons": [], "hint": ""}
    hung_since: float | None = None
    while time.time() < end:
        dismiss_modals(page)
        text = body(page)
        last = suite_ids.diagnose_share_step(text, page.url)
        controls = share_controls_state(page)
        last["controls"] = controls
        if last.get("state") == "ready":
            if controls.get("disabledRadioCount") and controls.get("pageOnly"):
                last["state"] = "hung_wrong_asset"
                last["needs_page_asset"] = True
            else:
                return last
        if last.get("state") == "hung_wrong_asset":
            if hung_since is None:
                hung_since = time.time()
            elif time.time() - hung_since >= 8:
                return last
        page.wait_for_timeout(1000)
    if last.get("state") == "unknown":
        last["state"] = "hung_loading"
        last["hint"] = (
            "Reels Share step never became ready. Close extra Meta Suite tabs "
            f"and open {suite_ids.composer_url()}."
        )
    return last


def click_publish(page: Page) -> bool:
    if click_share_cta(page):
        return True
    for label in ("Publish", "Post"):
        if click_button(page, label):
            page.wait_for_timeout(800)
            return True
    return False


def confirm_posted(page: Page, needle: str, timeout_s: float = 90) -> bool:
    """Confirm on the composer only. Navigating away discards an unpublished reel."""
    end = time.time() + timeout_s
    needle_l = needle.lower()
    while time.time() < end:
        stay_on_composer(page)
        text = body(page).lower()
        if any(
            x in text
            for x in (
                "reel shared",
                "reel published",
                "your reel is shared",
                "your reel was shared",
                "publishing your post",
                "this may take a moment",
                "is being shared",
                "is live",
                "view reel",
                "reel is now live",
            )
        ):
            return True
        if needle_l and needle_l in text and "create reel" not in text:
            return True
        page.wait_for_timeout(1500)
    return False


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
    port = int(port or creds.get("cdp_port") or 9223)
    out: dict = {
        "status": "started",
        "method": "cdp",
        "file": str(video_path),
        "caption": caption,
        "needle": needle,
        "port": port,
    }
    if not video_path.exists():
        out["status"] = "missing_file"
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
        # Ensure dialog handler even when page is reused
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
        creds = suite_ids.pin_suite_creds(creds, config.load_accounts())
        page.goto(
            suite_url(COMPOSER, creds),
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(2500)
        dismiss_modals(page)
        discard_leftover_draft(page)

        if suite_ids.url_has_stale_suite_ids(page.url):
            page.goto(
                suite_url(COMPOSER, creds),
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(2000)
            dismiss_modals(page)

        uploaded = attach_video(page, video_path)

        if not uploaded:
            out["status"] = "no_file_input"
            out["url"] = page.url
            if audit_dir:
                audit_dir.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(audit_dir / f"no_input_{video_path.stem}.png"))
            return out

        if not wait_upload_ready(page):
            out["status"] = "upload_timeout"
            out["url"] = page.url
            return out
        out["details_ready"] = wait_details_ready(page)

        out["caption_ok"] = fill_caption(page, caption)
        try:
            title_box = page.locator(
                'input[placeholder*="title" i]:not([disabled]), '
                'textarea[placeholder*="title" i]:not([disabled])'
            ).first
            if title_box.count() and title_box.is_enabled():
                title_box.fill((confirm_needle or caption)[:80], timeout=4000)
        except Exception:
            pass
        if audit_dir:
            audit_dir.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(audit_dir / f"before_{video_path.stem}.png"))

        ok = False
        share = advance_to_share(page)
        out["share_diagnosis"] = {
            k: share.get(k)
            for k in ("state", "needs_page_asset", "reasons", "hint")
        }
        if share.get("state") == "hung_wrong_asset":
            if try_select_facebook_page_destination(page):
                page.wait_for_timeout(1500)
                share = advance_to_share(page)
                out["share_diagnosis"]["retried_page_destination"] = True
                out["share_diagnosis"]["state"] = share.get("state")
        if share.get("state") in {"hung_wrong_asset", "hung_loading"}:
            out["status"] = "share_step_hung"
            out["url"] = page.url
            out["hint"] = share.get("hint") or suite_ids.diagnose_share_step(
                body(page), page.url
            ).get("hint")
            if audit_dir:
                audit_dir.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(audit_dir / f"share_hung_{video_path.stem}.png"))
            return out

        for attempt in range(3):
            click_button(page, "Next")
            page.wait_for_timeout(600)
            click_publish(page)
            page.wait_for_timeout(2000)
            dismiss_modals(page)
            if confirm_posted(page, needle, timeout_s=55):
                ok = True
                break
            out[f"attempt_{attempt + 1}"] = "not_confirmed"

        if audit_dir:
            page.screenshot(path=str(audit_dir / f"after_{video_path.stem}.png"))

        # CDP path posts both destinations when Suite cross-post is enabled in session
        plat = {
            "instagram": {"status": "ok" if ok else "unconfirmed", "method": "cdp"},
            "facebook": {"status": "ok" if ok else "unconfirmed", "method": "cdp"},
        }
        out["platforms"] = plat
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
