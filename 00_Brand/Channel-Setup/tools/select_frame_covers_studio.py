#!/usr/bin/env python3
"""Set Shorts covers via Studio's 'Select from video' frame picker.

Quota-free fallback: the daily customised-thumbnail limit blocks uploads, but
frame selection is not gated. Scores YouTube's three offered frames (least
Orbit-orange, brightest, most detail) and saves the best. Used to clear the
grey Studio tiles left by broken custom-thumbnail renditions on 25 Aug 2026.

Usage:
  select_frame_covers_studio.py <videoId> [videoId…]   set frame covers
  select_frame_covers_studio.py --verify-grid          check Studio Shorts grid tiles
"""
import base64
import io
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageStat
from playwright.sync_api import sync_playwright

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from build_scene_first_short_covers import orange_fraction  # noqa: E402

CDP = "http://127.0.0.1:9222"
PROFILE = str(Path.home() / ".orbit-chrome-youtube-studio")
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"


def cdp_alive():
    try:
        urllib.request.urlopen(f"{CDP}/json/version", timeout=4)
        return True
    except Exception:
        return False


def ensure_chrome():
    if cdp_alive():
        return
    print("relaunching Studio Chrome…", flush=True)
    subprocess.run(["bash", "-c", f'rm -f "{PROFILE}"/Singleton*'], check=False)
    subprocess.run([
        "open", "-na", "Google Chrome", "--args",
        "--remote-debugging-port=9222", "--remote-allow-origins=*",
        f"--user-data-dir={PROFILE}", "--profile-directory=Default",
        "--no-first-run", "--no-default-browser-check",
        "https://studio.youtube.com/",
    ], check=False)
    for _ in range(30):
        time.sleep(2)
        if cdp_alive():
            time.sleep(4)
            return
    raise RuntimeError("Chrome CDP did not come up")


def clean_tabs():
    try:
        with urllib.request.urlopen(f"{CDP}/json", timeout=5) as r:
            tabs = json.load(r)
        for t in tabs:
            if t.get("type") == "page" and "studio.youtube.com" in (t.get("url") or ""):
                urllib.request.urlopen(f"{CDP}/json/close/{t['id']}", timeout=5).read()
        time.sleep(1.5)
    except Exception:
        pass


def tile_score(img_bytes):
    im = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    st = ImageStat.Stat(im)
    return (min(sum(st.stddev) / 3, 55)
            - orange_fraction(im) * 300
            - (25 - min(sum(st.mean) / 3, 25)) * 2)


def do_one(ctx, vid):
    page = ctx.new_page()
    page.on("dialog", lambda d: d.accept())
    page.set_viewport_size({"width": 1560, "height": 980})
    out = {"vid": vid}
    try:
        page.goto(f"https://studio.youtube.com/video/{vid}/edit",
                  wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(8000)

        eds = page.locator("ytcp-thumbnail-editor")
        ed = next((eds.nth(i) for i in range(eds.count()) if eds.nth(i).is_visible()), None)
        if ed is None:
            out["status"] = "no_editor"
            return out, page
        ed.scroll_into_view_if_needed(timeout=5000)
        page.wait_for_timeout(1000)
        ed.locator("button[aria-label='Options']").first.evaluate("b => b.click()")
        page.wait_for_timeout(1400)

        clicked = page.evaluate("""() => {
            const items = [...document.querySelectorAll('tp-yt-paper-item, [role=option], [role=menuitem]')]
                .filter(e => e.offsetParent !== null)
                .filter(e => (e.innerText || '').trim().toLowerCase() === 'select from video');
            if (!items.length) return false;
            items[0].click();
            return true;
        }""")
        if not clicked:
            out["status"] = "no_menu_item"
            return out, page
        page.wait_for_timeout(4500)

        if "Daily customised thumbnail limit" in page.locator("body").inner_text():
            out["status"] = "daily_limit"
            return out, page

        tiles = page.evaluate("""() => {
            const btns = [...document.querySelectorAll('button')]
                .filter(b => b.offsetParent !== null &&
                        (b.getAttribute('aria-label') || '').startsWith('Auto-generated thumbnail'));
            return btns.map(b => {
                const img = b.querySelector('img');
                return {label: b.getAttribute('aria-label'), src: img ? img.src : null};
            });
        }""")
        if not tiles:
            out["status"] = "no_tiles"
            return out, page

        scores = []
        for t in tiles:
            if not t["src"]:
                scores.append(-999)
                continue
            if t["src"].startswith("data:"):
                raw = base64.b64decode(t["src"].split(",", 1)[1])
            else:
                raw = page.request.get(t["src"]).body()
            scores.append(tile_score(raw))
        best = scores.index(max(scores))
        out["picked"] = best + 1
        out["scores"] = [round(s, 1) for s in scores]

        page.evaluate("""(label) => {
            const b = [...document.querySelectorAll('button')]
                .find(b => b.offsetParent !== null && b.getAttribute('aria-label') === label);
            if (b) b.click();
        }""", tiles[best]["label"])
        page.wait_for_timeout(1000)

        done = page.get_by_role("button", name="Done")
        ok = False
        for i in range(done.count()):
            el = done.nth(i)
            if el.is_visible() and el.is_enabled():
                el.click(timeout=4000)
                ok = True
                break
        if not ok:
            out["status"] = "done_disabled"
            return out, page
        page.wait_for_timeout(2500)

        save = page.get_by_role("button", name="Save")
        if save.count() and save.first.is_enabled():
            save.first.click(timeout=6000)
            page.wait_for_timeout(6000)
            if "Verify that it's you" in page.locator("body").inner_text():
                out["status"] = "verify_wall"
                return out, page
            out["status"] = "saved"
        else:
            out["status"] = "save_not_enabled"
    except Exception as e:  # noqa: BLE001
        out["status"] = f"error: {str(e)[:110]}"
    return out, page


def verify_grid():
    ensure_chrome()
    clean_tabs()
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp(CDP, timeout=45000)
        page = b.contexts[0].new_page()
        page.set_viewport_size({"width": 1560, "height": 1000})
        all_bad = []
        for pgno in (1, 2):
            if pgno == 1:
                page.goto(f"https://studio.youtube.com/channel/{CHANNEL}/videos/short",
                          wait_until="domcontentloaded", timeout=90000)
                page.wait_for_timeout(9000)
            else:
                nxt = page.locator("#navigate-after, [aria-label='Go to next page']")
                if not nxt.count():
                    break
                nxt.first.click(timeout=5000)
                page.wait_for_timeout(8000)
            imgs = page.evaluate("""() => [...document.querySelectorAll('img')]
                .filter(i => i.src.includes('ytimg'))
                .map(i => ({src:(i.src.split('?')[0].split('/vi/')[1]||'').slice(0,40),
                            ok:i.naturalWidth>0}))""")
            bad = [i["src"] for i in imgs if not i["ok"]]
            all_bad += bad
            print(f"page{pgno}: tiles={len(imgs)} broken={len(bad)} {bad}")
        page.close()
        return all_bad


def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    if args[0] == "--verify-grid":
        bad = verify_grid()
        raise SystemExit(0 if not bad else 1)

    ensure_chrome()
    clean_tabs()
    results = {}
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP, timeout=45000)
        ctx = browser.contexts[0]
        for vid in args:
            out, page = do_one(ctx, vid)
            results[vid] = out
            print(vid, out, flush=True)
            try:
                page.close()
            except Exception:
                pass
            if out.get("status") in ("daily_limit", "verify_wall"):
                break
    ok = sum(1 for r in results.values() if r.get("status") == "saved")
    print(f"saved {ok} / {len(results)}")


if __name__ == "__main__":
    main()
