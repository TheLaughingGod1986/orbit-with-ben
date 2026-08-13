#!/usr/bin/env python3
"""Upload custom stills via Studio thumbnail file input; verify edit page no longer grey."""
from __future__ import annotations

import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

AUD = Path(__file__).resolve().parent
SHOTS = AUD / "studio_after"
SHOTS.mkdir(parents=True, exist_ok=True)
TARGETS = [
    ("nAZRIBm5wJw", AUD / "covers/nAZRIBm5wJw_cover_v03.jpg"),
    ("f8V6wCjWwHA", AUD / "covers/f8V6wCjWwHA_cover_v03.jpg"),
    ("OlwENQcY-jg", AUD / "covers/OlwENQcY-jg_cover_v03.jpg"),
]


def dismiss(page) -> None:
    for name in ("Done", "Got it", "Close", "Not now", "Dismiss", "Skip"):
        try:
            page.get_by_role("button", name=name, exact=True).first.click(timeout=400)
            page.wait_for_timeout(150)
        except Exception:
            pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def save_edit(page) -> bool:
    try:
        b = page.get_by_role("button", name="Save", exact=True).first
        if b.count() and b.is_enabled():
            b.click(force=True, timeout=2500)
            page.wait_for_timeout(3000)
            return True
    except Exception:
        pass
    return False


def thumb_state(page) -> dict:
    return page.evaluate(
        """() => {
      const imgs = [...document.querySelectorAll(
        'ytcp-video-thumbnail-editor img, ytcp-thumbnail-uploader img, ytcp-img-with-fallback img, .thumbnail img'
      )].map(i => ({
        src: (i.src || '').slice(0, 220),
        w: i.naturalWidth,
        h: i.naturalHeight,
        complete: i.complete,
      }));
      const good = imgs.filter(i => i.w >= 100 && /ytimg|googleusercontent|ggpht|blob:|lh3|data:image\\/jpeg/i.test(i.src));
      const broken = imgs.filter(i => !i.src || i.w < 20 || /placeholder|data:image\\/svg|empty/i.test(i.src));
      return { imgs: imgs.slice(0, 12), broken: broken.length, good: good.length, title: document.title };
    }"""
    )


def main() -> None:
    results = []
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = browser.contexts[0]
        page = ctx.new_page()
        for vid, cover in TARGETS:
            r: dict = {"id": vid, "cover": str(cover)}
            assert cover.exists(), cover
            page.goto(
                f"https://studio.youtube.com/video/{vid}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(4500)
            dismiss(page)
            page.screenshot(path=str(SHOTS / f"{vid}_before.png"), full_page=False)
            r["before"] = thumb_state(page)

            uploaded = False
            file_input = page.locator("ytcp-thumbnail-uploader input#file-loader, input#file-loader")
            try:
                if file_input.count():
                    file_input.first.set_input_files(str(cover))
                    uploaded = True
                    page.wait_for_timeout(5000)
            except Exception as e:
                r["file_input_err"] = str(e)[:240]

            if not uploaded:
                for sel in (
                    "ytcp-thumbnail-uploader #select-button",
                    "ytcp-video-custom-still-editor #select-button",
                    "button#select-button",
                ):
                    try:
                        loc = page.locator(sel).first
                        if loc.count():
                            with page.expect_file_chooser(timeout=5000) as fc:
                                loc.click(force=True, timeout=3000)
                            fc.value.set_files(str(cover))
                            uploaded = True
                            page.wait_for_timeout(5000)
                            break
                    except Exception as e:
                        r.setdefault("click_errs", []).append(f"{sel}:{str(e)[:120]}")

            r["uploaded"] = uploaded
            for _ in range(12):
                page.wait_for_timeout(1000)
                st = thumb_state(page)
                if st.get("good", 0) > 0:
                    break
            r["mid"] = thumb_state(page)
            r["saved"] = save_edit(page)
            page.wait_for_timeout(2500)
            page.goto(
                f"https://studio.youtube.com/video/{vid}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(5000)
            dismiss(page)
            r["after"] = thumb_state(page)
            page.screenshot(path=str(SHOTS / f"{vid}_after.png"), full_page=False)
            results.append(r)
            print(json.dumps({"id": vid, "uploaded": uploaded, "saved": r["saved"], "after_good": r["after"].get("good")}, indent=2))

        page.goto(
            "https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/videos/short",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(6000)
        dismiss(page)
        page.screenshot(path=str(SHOTS / "shorts_list.png"), full_page=False)
        page.close()

    out = {
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "results": results,
    }
    (AUD / "STUDIO_UPLOAD_RESULT.json").write_text(json.dumps(out, indent=2) + "\n")
    print("WROTE", AUD / "STUDIO_UPLOAD_RESULT.json")


if __name__ == "__main__":
    main()
