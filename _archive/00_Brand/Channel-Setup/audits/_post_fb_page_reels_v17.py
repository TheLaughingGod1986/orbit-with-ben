#!/usr/bin/env python3
"""Post 3 Orbit shorts to FB Page via CDP :9222 (TikTok Chrome profile has live FB session).

Uses Playwright over CDP. Requires Chrome started with --remote-allow-origins=*.
Meta profile ~/.orbit-chrome-meta-dev was wiped; do not use :9223 until re-login.
"""
from __future__ import annotations

import json
import re
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "fb_page_retry_2026-08-03"
OUT.mkdir(parents=True, exist_ok=True)
EXPORTS = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens"
    "/10_Shorts/06_Final-Exports"
)
PAGE_REELS = "https://www.facebook.com/profile.php?id=61592833318203&sk=reels_tab"
CDP = "http://127.0.0.1:9222"

VIDEOS = [
    (
        EXPORTS / "aliens_short-02_fermi-paradox_v02.mp4",
        "Where Is Everybody? Full film on YouTube. https://youtu.be/Mo93x0fxB1Q",
        "fermi",
    ),
    (
        EXPORTS / "aliens_short-01_distance_v02.mp4",
        "Space Is Rude About Distance. Full film on YouTube. https://youtu.be/Mo93x0fxB1Q",
        "distance",
    ),
    (
        EXPORTS / "aliens_short-03_zoo-hypothesis_v02.mp4",
        "What If Aliens Are Watching Us? Full film on YouTube. https://youtu.be/Mo93x0fxB1Q",
        "zoo",
    ),
]


def cdp_up() -> bool:
    try:
        urllib.request.urlopen(f"{CDP}/json/version", timeout=2).read()
        return True
    except Exception:
        return False


def shot(page, name: str) -> None:
    try:
        page.screenshot(path=str(OUT / name), timeout=15000)
    except Exception as e:
        print("shot", name, type(e).__name__, flush=True)


def fill_caption(page, caption: str) -> dict:
    res = page.evaluate(
        """(cap) => {
          const dlg=[...document.querySelectorAll('[role=dialog]')].find(d =>
            /Reel settings|Describe your reel|Create reel/i.test(d.innerText||''))
            || [...document.querySelectorAll('[role=dialog]')].pop();
          const root=dlg||document;
          const boxes=[...root.querySelectorAll('[contenteditable=true],[role=textbox],textarea')];
          let box=boxes.find(el => {
            const al=(el.getAttribute('aria-label')||'')+(el.getAttribute('aria-placeholder')||'')+(el.getAttribute('placeholder')||'');
            return /describe|caption|write a/i.test(al);
          });
          if (!box) {
            box=boxes.find(el => {
              const r=el.getBoundingClientRect();
              return r.width>80 && r.height>20 && r.x < 620;
            });
          }
          if (!box) return {ok:false, n:boxes.length};
          box.focus();
          box.click();
          if (box.isContentEditable) {
            box.innerHTML='';
            document.execCommand('selectAll');
            document.execCommand('insertText', false, cap);
          } else {
            box.value = cap;
          }
          box.dispatchEvent(new InputEvent('input',{bubbles:true,data:cap,inputType:'insertText'}));
          ['input','change','keyup'].forEach(ev =>
            box.dispatchEvent(new Event(ev,{bubbles:true})));
          return {ok:true, t:(box.innerText||box.value||'').slice(0,120)};
        }""",
        caption,
    )
    if isinstance(res, dict) and res.get("ok"):
        return res
    try:
        page.get_by_label(re.compile("Describe", re.I)).first.click(timeout=2500)
        page.keyboard.press("Meta+a")
        page.keyboard.type(caption, delay=8)
        return {"ok": True, "via": "keyboard"}
    except Exception as e:
        return {"ok": False, "error": type(e).__name__, "eval": res}


def post_one(page, path: Path, caption: str, key: str) -> dict:
    page.goto(PAGE_REELS, wait_until="domcontentloaded", timeout=120000)
    time.sleep(3)
    page.evaluate(
        """() => {
          for (const lab of ['Discard','Leave','OK','Close','Not now']) {
            const el=[...document.querySelectorAll('div[role=button],button')]
              .find(e => (e.innerText||'').trim()===lab);
            if (el) el.click();
          }
        }"""
    )
    time.sleep(0.5)

    try:
        page.get_by_role("button", name=re.compile("Create reel", re.I)).first.click(timeout=5000)
    except Exception:
        page.get_by_text("Create reel", exact=False).first.click(timeout=5000)
    time.sleep(2.5)
    shot(page, f"v17_open_{key}.png")

    uploaded = False
    try:
        with page.expect_file_chooser(timeout=12000) as fc:
            ok = page.evaluate(
                """() => {
                  const el=[...document.querySelectorAll('div[role=button],button')]
                    .find(e => /^(Upload|Add Video)$/i.test((e.innerText||'').trim()));
                  if (!el) return false;
                  el.click(); return true;
                }"""
            )
            if not ok:
                page.get_by_text(re.compile(r"^(Upload|Add Video)$", re.I)).first.click(timeout=3000)
        fc.value.set_files(str(path))
        uploaded = True
    except Exception as e:
        print("chooser", type(e).__name__, e, flush=True)
        try:
            loc = page.locator('input[type="file"]')
            n = loc.count()
            if n:
                loc.nth(n - 1).set_input_files(str(path), timeout=8000)
                uploaded = True
        except Exception as e2:
            print("input", type(e2).__name__, e2, flush=True)

    print("upload", uploaded, flush=True)
    if not uploaded:
        return {"key": key, "status": "upload_fail"}

    for _ in range(70):
        t = page.evaluate("() => document.body ? document.body.innerText : ''")
        if "Edit reel" in t or ("Next" in t and "Upload your video in order" not in t):
            break
        time.sleep(1.2)

    for _ in range(6):
        t = page.evaluate("() => document.body ? document.body.innerText : ''")
        if "Reel settings" in t or "Describe your reel" in t:
            break
        page.evaluate(
            """() => {
              const els=[...document.querySelectorAll('div[role=button],button')]
                .filter(e => (e.innerText||'').trim()==='Next');
              const el=els.sort((a,b)=>b.getBoundingClientRect().width-a.getBoundingClientRect().width)[0];
              if (el) el.click();
            }"""
        )
        time.sleep(2)
    print("settings", flush=True)

    if page.evaluate("() => /Choose a date and time/i.test(document.body.innerText||'')"):
        page.evaluate(
            """() => {
              const b=[...document.querySelectorAll('div[role=button],button')]
                .find(e => /^(Cancel|Close)$/i.test((e.innerText||'').trim()));
              if (b) b.click();
            }"""
        )
        time.sleep(0.5)

    cap = fill_caption(page, caption)
    print("caption", cap, flush=True)
    page.mouse.click(1100, 420)
    time.sleep(0.8)
    shot(page, f"v17_cap_{key}.png")

    enabled = False
    for w in range(40):
        st = page.evaluate(
            """() => [...document.querySelectorAll('div[role=button],button')]
              .filter(e => (e.innerText||'').trim()==='Post')
              .map(e => e.getAttribute('aria-disabled'))"""
        )
        print("wait", w, st, flush=True)
        if st and any(x in (None, "false", False) for x in st):
            enabled = True
            break
        if w in (5, 12, 20):
            fill_caption(page, caption)
            page.mouse.click(1100, 420)
        time.sleep(2)

    clicked = page.evaluate(
        """() => {
          const posts=[...document.querySelectorAll('div[role=button],button')]
            .filter(e => (e.innerText||'').trim()==='Post');
          const el=posts.find(e => e.getAttribute('aria-disabled')!=='true');
          if (!el) return {ok:false, dis: posts[0]&&posts[0].getAttribute('aria-disabled'), n:posts.length};
          el.click();
          return {ok:true};
        }"""
    )
    print("clicked", clicked, "enabled", enabled, flush=True)
    time.sleep(12)
    shot(page, f"v17_after_{key}.png")
    still = page.evaluate(
        "() => /Reel settings|Describe your reel/i.test(document.body ? document.body.innerText : '')"
    )
    if still:
        page.keyboard.press("Escape")
        time.sleep(0.5)
        page.evaluate(
            """() => {
              const b=[...document.querySelectorAll('div[role=button],button')]
                .find(e => /^(Discard|Leave|OK)$/i.test((e.innerText||'').trim()));
              if (b) b.click();
            }"""
        )
        time.sleep(1)
    return {
        "key": key,
        "caption_ok": bool(isinstance(cap, dict) and cap.get("ok")),
        "enabled": enabled,
        "clicked": clicked,
        "still": still,
        "status": "ok" if (isinstance(clicked, dict) and clicked.get("ok") and not still) else "fail",
    }


def main() -> None:
    if not cdp_up():
        raise SystemExit("CDP 9222 down — start TikTok/FB Chrome with --remote-allow-origins=*")
    results: dict = {"posts": [], "cdp": CDP}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = None
        for pg in ctx.pages:
            if "facebook.com" in (pg.url or ""):
                page = pg
                break
        if page is None:
            page = ctx.new_page()
        page.bring_to_front()
        page.goto(PAGE_REELS, wait_until="domcontentloaded", timeout=120000)
        time.sleep(3)
        shot(page, "v17_start.png")
        print("start", page.url, flush=True)

        for path, caption, key in VIDEOS:
            print(f"\n=== {key} ===", flush=True)
            if not path.exists():
                results["posts"].append({"key": key, "status": "missing_file", "path": str(path)})
                continue
            try:
                entry = post_one(page, path, caption, key)
            except Exception as e:
                print("ERR", key, e, flush=True)
                entry = {"key": key, "status": "error", "error": str(e)[:240]}
                shot(page, f"v17_err_{key}.png")
            results["posts"].append(entry)
            print(entry, flush=True)
            time.sleep(2)

        page.goto(PAGE_REELS, wait_until="domcontentloaded", timeout=120000)
        time.sleep(6)
        shot(page, "v17_verify.png")
        body = page.evaluate("() => document.body ? document.body.innerText : ''")
        low = body.lower()
        results["verify"] = {
            "empty": ("haven't created any reels" in low) or ("no reels yet" in low),
            "everybody": "Everybody" in body,
            "distance": "Distance" in body,
            "watching": ("Watching" in body) or ("Aliens" in body),
            "snip": re.sub(r"\s+", " ", body)[200:750],
            "cdp_alive": cdp_up(),
        }
        (OUT / "V17_RESULT.json").write_text(json.dumps(results, indent=2))
        print(json.dumps(results, indent=2), flush=True)


if __name__ == "__main__":
    main()
