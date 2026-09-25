#!/usr/bin/env python3
"""Upload 3 Orbit shorts to Facebook Page via Create reel modal."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "fb_page_missing_2026-08-03"
OUT.mkdir(parents=True, exist_ok=True)
EXPORTS = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens"
    "/10_Shorts/06_Final-Exports"
)
PAGE_REELS = "https://www.facebook.com/profile.php?id=61592833318203&sk=reels_tab"

VIDEOS = [
    {
        "id": "1HuV8o3gOss",
        "file": EXPORTS / "aliens_short-02_fermi-paradox_v02.mp4",
        "caption": (
            "Where Is Everybody? Full film on YouTube. "
            "https://youtu.be/Mo93x0fxB1Q #space #orbitwithben #reels"
        ),
    },
    {
        "id": "dPMJQp2gMNc",
        "file": EXPORTS / "aliens_short-01_distance_v02.mp4",
        "caption": (
            "Space Is Rude About Distance. Full film on YouTube. "
            "https://youtu.be/Mo93x0fxB1Q #space #orbitwithben #reels"
        ),
    },
    {
        "id": "rFJoOdQAc9c",
        "file": EXPORTS / "aliens_short-03_zoo-hypothesis_v02.mp4",
        "caption": (
            "What If Aliens Are Watching Us? Full film on YouTube. "
            "https://youtu.be/Mo93x0fxB1Q #space #orbitwithben #reels"
        ),
    },
]


def shot(page, name: str) -> None:
    try:
        page.screenshot(path=str(OUT / name), full_page=False, timeout=15000)
    except Exception as e:
        print("shot fail", name, e, flush=True)


def click_label(page, label: str, timeout: int = 3000) -> bool:
    for exact in (True, False):
        try:
            page.get_by_role("button", name=re.compile(rf"^{re.escape(label)}$", re.I)).click(
                timeout=timeout
            )
            return True
        except Exception:
            pass
    try:
        page.get_by_text(label, exact=True).first.click(timeout=timeout)
        return True
    except Exception:
        pass
    hit = page.evaluate(
        """(lab) => {
          const hits=[];
          for (const el of document.querySelectorAll('div[role=button], button, span')) {
            const t=(el.innerText||'').trim();
            const al=el.getAttribute('aria-label')||'';
            if (t!==lab && al!==lab) continue;
            const r=el.getBoundingClientRect();
            if (r.width<12||r.height<10||r.width>420) continue;
            const bg=getComputedStyle(el).backgroundColor||'';
            hits.push({x:r.x+r.width/2,y:r.y+r.height/2,bg,w:r.width,h:r.height});
          }
          if (!hits.length) return null;
          hits.sort((a,b)=>{
            const blue=h=>/24,\\s*119|0,\\s*97|10,\\s*120/.test(h.bg)?1:0;
            return (blue(b)-blue(a))||(b.w*b.h-a.w*a.h);
          });
          return hits[0];
        }""",
        label,
    )
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        return True
    return False


def open_create_reel(page) -> bool:
    page.goto(PAGE_REELS, wait_until="domcontentloaded", timeout=90000)
    time.sleep(3)
    for lab in ("Create reel", "Create Reel", "Reel"):
        if click_label(page, lab, timeout=2500):
            time.sleep(2.5)
            body = page.inner_text("body")
            if "Create reel" in body or "Add Video" in body or "Upload" in body:
                return True
    # direct create URL
    page.goto("https://www.facebook.com/reels/create/?surface=profile_reels_tab", wait_until="domcontentloaded", timeout=90000)
    time.sleep(4)
    body = page.inner_text("body")
    return "Add Video" in body or "Upload" in body or "Create reel" in body


def upload_video(page, path: Path) -> bool:
    # Prefer filechooser on Upload / Add Video
    for lab in ("Upload", "Add Video", "Add video"):
        try:
            with page.expect_file_chooser(timeout=6000) as fc:
                click_label(page, lab, timeout=2500)
            fc.value.set_files(str(path))
            return True
        except Exception:
            continue
    # Hidden inputs
    try:
        loc = page.locator('input[type="file"]')
        n = loc.count()
        if n:
            loc.nth(n - 1).set_input_files(str(path))
            return True
    except Exception:
        pass
    # page.once pattern used successfully for Suite
    try:
        chosen = {"ok": False}

        def on_fc(fc):
            fc.set_files(str(path))
            chosen["ok"] = True

        page.once("filechooser", on_fc)
        # click blue Upload region
        page.evaluate(
            """() => {
              const el = Array.from(document.querySelectorAll('div[role=button], button')).find(e =>
                /^(Upload|Add Video)$/i.test((e.innerText||'').trim())
              );
              if (el) el.click();
            }"""
        )
        time.sleep(2)
        return chosen["ok"]
    except Exception:
        return False


def wait_ready(page, seconds: int = 120) -> bool:
    end = time.time() + seconds
    while time.time() < end:
        body = page.inner_text("body")
        if any(
            k in body
            for k in (
                "Next",
                "Describe your reel",
                "Write a caption",
                "Share",
                "Post",
                "100%",
                "Edit cover",
                "Trim",
            )
        ):
            # avoid early "Next" on empty modal alone — prefer preview signals
            if "preview" in body.lower() or "Next" in body or "Share" in body or "Post" in body:
                if "Upload your video in order to see a preview" not in body:
                    return True
                if "Next" in body and "Add Video" not in body:
                    return True
        time.sleep(2)
    return False


def fill_caption(page, caption: str) -> bool:
    for sel in (
        '[aria-label*="Describe"]',
        '[aria-label*="Write a caption"]',
        '[aria-label*="caption" i]',
        'div[contenteditable="true"]',
        "textarea",
    ):
        try:
            box = page.locator(sel).first
            if not box.count():
                continue
            box.click(timeout=2500)
            time.sleep(0.2)
            page.keyboard.press("Meta+a")
            page.keyboard.type(caption, delay=6)
            return True
        except Exception:
            continue
    return False


def share(page) -> bool:
    for lab in ("Next",):
        click_label(page, lab, timeout=2500)
        time.sleep(1.5)
    for lab in ("Share", "Post", "Publish"):
        if click_label(page, lab, timeout=3500):
            time.sleep(4)
            return True
    return False


def main() -> None:
    results = {"posts": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223")
        page = next(x for x in browser.contexts[0].pages if not x.is_closed())
        page.bring_to_front()
        page.set_viewport_size({"width": 1440, "height": 900})

        for i, item in enumerate(VIDEOS):
            assert item["file"].exists(), item["file"]
            print(f"\n=== {i+1}/3 {item['id']} ===", flush=True)
            # close leftover dialogs
            page.keyboard.press("Escape")
            time.sleep(0.4)
            page.keyboard.press("Escape")

            opened = open_create_reel(page)
            shot(page, f"v02_open_{i}.png")
            print("opened", opened, flush=True)
            if not opened:
                results["posts"].append({"id": item["id"], "status": "no_composer"})
                continue

            up = upload_video(page, item["file"])
            print("upload", up, flush=True)
            ready = wait_ready(page, 150) if up else False
            print("ready", ready, flush=True)
            shot(page, f"v02_ready_{i}.png")

            # sometimes need Next before caption
            click_label(page, "Next", timeout=2000)
            time.sleep(1.5)
            cap = fill_caption(page, item["caption"])
            print("caption", cap, flush=True)
            shot(page, f"v02_cap_{i}.png")

            shared = share(page)
            print("share", shared, flush=True)
            time.sleep(5)
            shot(page, f"v02_after_{i}.png")
            results["posts"].append(
                {
                    "id": item["id"],
                    "opened": opened,
                    "upload": up,
                    "ready": ready,
                    "caption": cap,
                    "share": shared,
                    "status": "ok" if shared else "fail",
                    "snip": re.sub(r"\s+", " ", page.inner_text("body"))[:350],
                }
            )

        # Verify reels tab
        page.goto(PAGE_REELS, wait_until="domcontentloaded", timeout=90000)
        time.sleep(5)
        shot(page, "v02_verify.png")
        body = page.inner_text("body")
        results["verify"] = {
            "empty": "haven't created any reels" in body.lower(),
            "fullfilm": body.lower().count("full film"),
            "snip": re.sub(r"\s+", " ", body)[:700],
        }
        (OUT / "FB_POST_V02.json").write_text(json.dumps(results, indent=2))
        print(json.dumps(results, indent=2), flush=True)


if __name__ == "__main__":
    main()
