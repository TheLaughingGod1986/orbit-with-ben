#!/usr/bin/env python3
"""Upload vertical Shorts covers through Studio desktop.

The Data API's thumbnails.set treats every image as a 16:9 video thumbnail and
letterboxes it, so a 1080x1920 Short cover never reaches the vertical slot that
Studio and the Shorts shelf read. YouTube only accepts Shorts covers through
Studio on desktop, so drive that UI instead.
"""
import argparse
import json
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
REPO = Path(__file__).resolve().parents[3]
COVERS = REPO / "00_Brand/Channel-Setup/assets/shorts_covers_2026-08-25"
SHOT = COVERS / "_run_shots"
SHOT.mkdir(parents=True, exist_ok=True)

# Studio caps custom-thumbnail changes per day ("Daily customised thumbnail
# limit reached"); stop the run rather than burn attempts once it appears.
DAILY_LIMIT_TEXT = "Daily customised thumbnail limit"


def clean_tabs():
    try:
        with urllib.request.urlopen(f"{CDP}/json", timeout=5) as r:
            tabs = json.load(r)
        for t in tabs:
            if t.get("type") == "page" and "studio.youtube.com" in (t.get("url") or ""):
                urllib.request.urlopen(f"{CDP}/json/close/{t['id']}", timeout=5).read()
        time.sleep(2)
    except Exception as e:  # noqa: BLE001
        print("clean err:", e)


def visible_editor(page):
    eds = page.locator("ytcp-thumbnail-editor")
    for i in range(eds.count()):
        if eds.nth(i).is_visible():
            return eds.nth(i)
    return None


def menu_items(page):
    return page.evaluate("""() => [...document.querySelectorAll('tp-yt-paper-item, ytcp-text-menu tp-yt-paper-item, [role=option], [role=menuitem]')]
        .filter(e => e.offsetParent !== null)
        .map(e => (e.innerText || '').trim()).filter(Boolean)""")


def click_menu(page, label):
    """Click the open menu's own item, not same-named text elsewhere on the page."""
    return page.evaluate("""(label) => {
        const items = [...document.querySelectorAll('tp-yt-paper-item, [role=option], [role=menuitem]')]
            .filter(e => e.offsetParent !== null)
            .filter(e => (e.innerText || '').trim().toLowerCase() === label.toLowerCase());
        if (!items.length) return false;
        items[0].click();
        return true;
    }""", label)


def do_one(ctx, vid, img, dump=False):
    page = ctx.new_page()
    page.on("dialog", lambda d: d.accept())
    page.set_viewport_size({"width": 1560, "height": 980})
    out = {"vid": vid}
    try:
        page.goto(f"https://studio.youtube.com/video/{vid}/edit",
                  wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(9000)

        ed = visible_editor(page)
        if ed is None:
            out["status"] = "no_editor"
            return out, page
        ed.scroll_into_view_if_needed(timeout=5000)
        page.wait_for_timeout(1000)

        opts = ed.locator("button[aria-label='Options']")
        if not opts.count():
            out["status"] = "no_options_button"
            page.screenshot(path=str(SHOT / f"{vid}_noopts.png"))
            return out, page
        opts.first.evaluate("b => b.click()")
        page.wait_for_timeout(1800)

        items = menu_items(page)
        out["menu"] = items
        if dump:
            print(f"  menu: {items}")
            page.screenshot(path=str(SHOT / f"{vid}_menu.png"))

        target = next((t for t in ("Upload file", "Change", "Upload thumbnail")
                       if any(t.lower() in i.lower() for i in items)), None)
        if not target:
            out["status"] = "no_upload_item"
            return out, page

        chooser = None
        try:
            with page.expect_file_chooser(timeout=9000) as fc:
                click_menu(page, target)
            chooser = fc.value
        except Exception:
            # some states interpose a Continue confirm (deletes an A/B test)
            cont = page.get_by_role("button", name="Continue")
            if cont.count() and cont.first.is_visible():
                with page.expect_file_chooser(timeout=9000) as fc2:
                    cont.first.click(timeout=4000)
                chooser = fc2.value
                out["confirm"] = True
        if chooser is None:
            body = page.locator("body").inner_text()
            out["status"] = "daily_limit" if DAILY_LIMIT_TEXT in body else "no_file_chooser"
            page.screenshot(path=str(SHOT / f"{vid}_nochooser.png"))
            return out, page

        chooser.set_files(img)
        out["uploaded_via"] = target
        page.wait_for_timeout(6000)

        if "Verify that it's you" in page.locator("body").inner_text():
            out["verify_wall"] = True
            page.screenshot(path=str(SHOT / f"{vid}_verify.png"))
            return out, page

        save = page.get_by_role("button", name="Save")
        if save.count() and save.first.is_enabled():
            save.first.click(timeout=6000)
            page.wait_for_timeout(8000)
            out["status"] = "saved"
        else:
            out["status"] = "save_not_enabled"
        page.screenshot(path=str(SHOT / f"{vid}_final.png"))
    except Exception as e:  # noqa: BLE001
        out["status"] = f"error: {str(e)[:150]}"
        try:
            page.screenshot(path=str(SHOT / f"{vid}_error.png"))
        except Exception:
            pass
    return out, page


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", help="video ids; default = every rebuilt cover")
    ap.add_argument("--dump", action="store_true")
    args = ap.parse_args()

    ids = args.ids or sorted(p.stem.replace("cover_", "") for p in COVERS.glob("cover_*.jpg"))
    clean_tabs()
    results = {}
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP, timeout=45000)
        ctx = browser.contexts[0]
        for vid in ids:
            img = COVERS / f"cover_{vid}.jpg"
            if not img.exists():
                results[vid] = {"status": "no_cover_file"}
                print(vid, results[vid])
                continue
            out, page = do_one(ctx, vid, str(img), dump=args.dump)
            results[vid] = out
            print(vid, {k: v for k, v in out.items() if k != "menu"}, flush=True)
            try:
                page.close()
            except Exception:
                pass
            if out.get("status") == "daily_limit":
                print("Studio daily custom-thumbnail limit hit — stopping; resume tomorrow.")
                break

    (COVERS / "UPLOAD_RESULT.json").write_text(json.dumps(results, indent=1))
    ok = sum(1 for r in results.values() if r.get("status") == "saved")
    print(f"\nsaved {ok} / {len(results)}")
    remaining = [v for v in ids if results.get(v, {}).get("status") != "saved"]
    if remaining:
        print(f"remaining ({len(remaining)}): {' '.join(remaining)}")
    raise SystemExit(0 if ok and not remaining else 1)


if __name__ == "__main__":
    main()
