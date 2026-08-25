#!/usr/bin/env python3
"""Set the vidIQ thumbnail A/B test on the Last Star premiere (REXYxuLOBoI).

Run AFTER the premiere is public (Thu 27 Aug 2026 18:00 UK) — vidIQ cannot
hold a rotation test on a scheduled/premiere video (verified 25 Aug: setup
completes with no error but no test row is created; same failure signature as
europa_abc_v03.log on a scheduled video).

Flow proven end-to-end 25 Aug 00:52 (see audits/channel_review_2026-08-24/
studio_finish/). Uses the Studio Chrome CDP profile on :9222 — start it with
the `open -na` command in _run_ab_test.sh so it detaches from the shell.
"""
import json
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
VIDEO = "REXYxuLOBoI"
SEL = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/005_The-Last-Star-In-The-Universe/08_Thumbnail/Selected"
)
# Scene-first v02 (no Orbit) — tests Ben's 25 Aug observation that thumbs
# without the Orbit character outperform. A (live thumb, Orbit badge) = control.
THUMB_B = SEL / "last-star_thumb_B_final-sunset_scene_v02_1280x720.png"
THUMB_C = SEL / "last-star_thumb_C_what-comes-after_scene_v02_1280x720.png"
OUT = Path(__file__).parent / "AB_TEST_RESULT.json"
SHOTS = Path(__file__).parent / "ab_test_shots"
SHOTS.mkdir(exist_ok=True)


def clean_studio_tabs():
    try:
        with urllib.request.urlopen(f"{CDP}/json", timeout=5) as r:
            tabs = json.load(r)
        for t in tabs:
            if t.get("type") == "page" and "studio.youtube.com" in t.get("url", ""):
                urllib.request.urlopen(f"{CDP}/json/close/{t['id']}", timeout=5).read()
        time.sleep(2)
    except Exception:
        pass


def add_by_label(page, label_text, file_path):
    lbl = page.get_by_text(label_text, exact=True).first
    lb = lbl.bounding_box()
    adds = page.get_by_text("Add thumbnail", exact=True)
    for i in range(adds.count()):
        el = adds.nth(i)
        try:
            bb = el.bounding_box()
        except Exception:
            continue
        if bb and lb and abs((bb["y"] + bb["height"] / 2) - (lb["y"] + lb["height"] / 2)) < 90:
            with page.expect_file_chooser(timeout=9000) as fc:
                el.click(timeout=4000, force=True)
            fc.value.set_files(str(file_path))
            page.wait_for_timeout(4500)
            return True
    return False


def main() -> dict:
    out = {"at": datetime.now().isoformat(), "video": VIDEO}
    clean_studio_tabs()
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP, timeout=45000)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.on("dialog", lambda d: d.accept())
        page.set_viewport_size({"width": 1560, "height": 980})
        page.goto(
            f"https://studio.youtube.com/video/{VIDEO}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(9000)
        body0 = page.locator("body").inner_text()
        out["verify_wall"] = "Verify that it's you" in body0
        if out["verify_wall"]:
            out["ok"] = False
            out["error"] = "verify_wall — Ben must complete Verify in Chrome"
            page.screenshot(path=str(SHOTS / "verify_wall.png"))
            page.close()
            return out

        ed = page.locator("ytcp-thumbnail-editor").first
        ed.scroll_into_view_if_needed(timeout=5000)
        page.wait_for_timeout(1000)
        ed.locator("img").first.hover(timeout=4000)
        page.wait_for_timeout(900)
        ed.locator(
            "ytcp-icon-button, tp-yt-paper-icon-button, button[aria-label*='ptions']"
        ).first.click(timeout=5000)
        page.wait_for_timeout(2200)
        items = page.get_by_text("A/B Testing", exact=False)
        pick = None
        for i in range(items.count()):
            el = items.nth(i)
            try:
                bb = el.bounding_box()
            except Exception:
                continue
            if el.is_visible() and bb and 0 < bb["y"] < 950 and bb["x"] < 700:
                pick = bb
        if pick is None:
            out["ok"] = False
            out["error"] = "ab_menu_item_not_found"
            page.screenshot(path=str(SHOTS / "no_menu_item.png"))
            page.close()
            return out
        page.mouse.click(pick["x"] + pick["width"] / 2, pick["y"] + pick["height"] / 2)
        page.wait_for_timeout(5000)
        body1 = page.locator("body").inner_text()
        if "Add thumbnail" in body1:
            out["uploaded_B"] = add_by_label(page, "Thumbnail 2 (required)", THUMB_B)
            out["uploaded_C"] = add_by_label(page, "Thumbnail 3", THUMB_C)
        if "Set test" not in page.locator("body").inner_text():
            out["ok"] = False
            out["error"] = "no_set_test_button"
            page.screenshot(path=str(SHOTS / "no_set_button.png"))
            page.close()
            return out
        page.get_by_text("Set test", exact=True).first.click(timeout=5000)
        page.wait_for_timeout(12000)
        page.screenshot(path=str(SHOTS / "after_set.png"))
        page.close()

        # verify the test registered in the vidIQ A/B list
        page2 = ctx.new_page()
        page2.on("dialog", lambda d: d.accept())
        page2.set_viewport_size({"width": 1560, "height": 980})
        page2.goto(
            "https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/videos/upload",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page2.wait_for_timeout(9000)
        page2.get_by_text("A/B Tests", exact=True).first.click(timeout=5000)
        page2.wait_for_timeout(6000)
        page2.screenshot(path=str(SHOTS / "ab_list.png"))
        b3 = page2.locator("body").inner_text()
        out["in_list"] = "Last Star" in b3
        out["ok"] = out["in_list"]
        if not out["in_list"]:
            out["error"] = "test_not_in_list_after_set (video public yet?)"
        page2.close()
    return out


if __name__ == "__main__":
    result = main()
    OUT.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("ok") else 1)
