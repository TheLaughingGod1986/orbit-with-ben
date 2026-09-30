#!/usr/bin/env python3
"""Set Jupiter long end screen: Last Star + Subscribe. Studio CDP only.

Video: -jmMROGoZCM
End screen: REXYxuLOBoI (Last Star) + Subscribe
Connects to existing Chrome on localhost:9222.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

JUPITER_ID = "-jmMROGoZCM"
LAST_STAR_ID = "REXYxuLOBoI"
CDP = "http://127.0.0.1:9334"  # ~/.orbit-chrome-youtube-studio
AUDIT = Path(__file__).resolve().parent / "_studio_audit_end_screen"
OUT = Path(__file__).resolve().parent / "jupiter_end_screen_result.json"


def dismiss(page) -> None:
    try:
        page.evaluate(
            "() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())"
        )
    except Exception:
        pass
    for name in ("Got it", "Dismiss", "Not now", "Close", "Skip"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=700)
        except Exception:
            pass
        try:
            l = page.get_by_role("link", name=re.compile(name, re.I))
            if l.count() and l.first.is_visible():
                l.first.click(force=True, timeout=700)
        except Exception:
            pass


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / name), full_page=False)


def click_save(page) -> str | bool:
    saved = page.evaluate(
        """() => {
          const walk=(r)=>{
            if(!r)return false;
            for(const b of (r.querySelectorAll?r.querySelectorAll('button'):[])){
              const t=(b.innerText||'').trim();
              if((t==='SAVE'||t==='Save')&&!b.disabled){b.click();return t;}
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[])){
              if(el.shadowRoot){const x=walk(el.shadowRoot); if(x) return x;}
            }
            return false;
          };
          return walk(document);
        }"""
    )
    return saved


def main() -> None:
    result: dict = {
        "video": JUPITER_ID,
        "target_end": LAST_STAR_ID,
        "ok": False,
        "startedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()
        try:
            page.goto(
                f"https://studio.youtube.com/video/{JUPITER_ID}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(4000)
            dismiss(page)
            shot(page, "01_edit.png")

            # Sign-in / verify gate?
            body = page.inner_text("body")[:2000]
            if "Sign in" in body and "studio.youtube.com" not in page.url:
                result["blocker"] = "sign_in_required"
                shot(page, "BLOCKED_sign_in.png")
                OUT.write_text(json.dumps(result, indent=2))
                print(json.dumps(result, indent=2))
                return
            if "Verify that it's you" in body or "Confirm it's you" in body:
                result["blocker"] = "verify_required"
                shot(page, "BLOCKED_verify.png")
                OUT.write_text(json.dumps(result, indent=2))
                print(json.dumps(result, indent=2))
                return

            # Open End screen editor (left nav or tabs)
            opened = False
            for locator in (
                page.get_by_role("tab", name=re.compile(r"End screen", re.I)),
                page.get_by_text("End screen", exact=True),
                page.locator("a[href*='endscreen'], ytcp-ve[title*='End'], #endscreen-button"),
            ):
                try:
                    if locator.count():
                        locator.first.click(force=True, timeout=5000)
                        opened = True
                        break
                except Exception as e:
                    result.setdefault("open_tries", []).append(str(e)[:80])
            if not opened:
                # Fallback: navigate to end screen URL pattern used by Studio
                page.goto(
                    f"https://studio.youtube.com/video/{JUPITER_ID}/editor/endscreen",
                    wait_until="domcontentloaded",
                    timeout=120000,
                )
                opened = True
            page.wait_for_timeout(3500)
            dismiss(page)
            shot(page, "02_endscreen_open.png")
            result["opened"] = True

            # Pick template with video + subscribe
            for label in (
                "1 video, 1 subscribe",
                "Video and subscribe",
                "1 video + subscribe",
                "Video + Subscribe",
            ):
                try:
                    loc = page.get_by_text(label, exact=False)
                    if loc.count():
                        loc.first.click(force=True)
                        page.wait_for_timeout(2000)
                        result["template"] = label
                        break
                except Exception:
                    continue
            shot(page, "03_template.png")

            # Try to point the video element at Last Star
            # Click the video element / "Add element" / content picker
            picked = False
            for text in (
                "Choose a video",
                "Select video",
                "Best for viewer",
                "Add video",
                "Video",
            ):
                try:
                    loc = page.get_by_text(text, exact=False)
                    if loc.count():
                        loc.first.click(force=True, timeout=3000)
                        page.wait_for_timeout(1500)
                        result["picker_click"] = text
                        break
                except Exception:
                    continue

            # Search for Last Star by id or title
            search = page.locator(
                "input[placeholder*='Search'], input[aria-label*='Search'], "
                "#search-input input, ytcp-entity-search input"
            )
            if search.count():
                search.first.click(force=True)
                search.first.fill("")
                search.first.type(LAST_STAR_ID, delay=40)
                page.wait_for_timeout(2500)
                shot(page, "04_search.png")
                # Click first result that mentions Last Star or the id
                for needle in (
                    "What Happens When the Last Star Dies",
                    LAST_STAR_ID,
                    "Last Star",
                ):
                    try:
                        hit = page.get_by_text(needle, exact=False)
                        if hit.count():
                            hit.first.click(force=True)
                            picked = True
                            result["picked"] = needle
                            page.wait_for_timeout(1500)
                            break
                    except Exception:
                        continue
            else:
                result["search_missing"] = True

            shot(page, "05_before_save.png")
            saved = click_save(page)
            result["saved_btn"] = saved
            page.wait_for_timeout(3500)
            # Sometimes a second confirm Save on the edit page
            try:
                b = page.get_by_role("button", name="Save", exact=True)
                if b.count() and b.first.is_enabled():
                    b.first.click(force=True)
                    page.wait_for_timeout(2500)
                    result["page_save"] = True
            except Exception:
                pass
            shot(page, "06_after_save.png")

            # Re-open to verify
            page.goto(
                f"https://studio.youtube.com/video/{JUPITER_ID}/editor/endscreen",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(3000)
            dismiss(page)
            verify_body = page.inner_text("body")[:4000]
            result["verify_has_last_star"] = (
                "Last Star" in verify_body
                or LAST_STAR_ID in verify_body
                or "What Happens When the Last Star Dies" in verify_body
            )
            result["verify_has_subscribe"] = "Subscribe" in verify_body
            shot(page, "07_verify.png")
            result["ok"] = bool(saved) and (
                result.get("verify_has_last_star") or result.get("picked")
            )
            result["picked_ok"] = picked
        except Exception as e:
            result["error"] = str(e)[:300]
            try:
                shot(page, "ERROR.png")
            except Exception:
                pass
        finally:
            try:
                page.close()
            except Exception:
                pass
            result["finishedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            OUT.write_text(json.dumps(result, indent=2) + "\n")
            print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
