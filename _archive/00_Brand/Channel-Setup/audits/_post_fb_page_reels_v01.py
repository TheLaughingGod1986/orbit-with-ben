#!/usr/bin/env python3
"""Post the 3 live Orbit shorts to the Facebook Page (they were IG-only).

Also attempts to connect FB Page as a Suite share destination.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "fb_page_missing_2026-08-03"
OUT.mkdir(parents=True, exist_ok=True)
ROOT = Path("/Users/ben/code/Orbit-YouTube")
EXPORTS = ROOT / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/06_Final-Exports"
PAGE = "https://www.facebook.com/profile.php?id=61592833318203"

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


def dismiss(page) -> None:
    for lab in (
        "Allow all cookies",
        "Decline optional cookies",
        "Close",
        "Not Now",
        "Not now",
        "Got it",
    ):
        try:
            page.get_by_role("button", name=re.compile(rf"^{re.escape(lab)}$", re.I)).click(
                timeout=800
            )
        except Exception:
            pass


def click_text(page, label: str, timeout: int = 2500) -> bool:
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
          for (const el of document.querySelectorAll('div[role=button], button, span[role=button]')) {
            if ((el.innerText||'').trim()!==lab) continue;
            const r=el.getBoundingClientRect();
            if (r.width<15||r.height<10||r.width>400) continue;
            const bg=getComputedStyle(el).backgroundColor||'';
            hits.push({x:r.x+r.width/2,y:r.y+r.height/2,bg,y0:r.y,x0:r.x});
          }
          if (!hits.length) return null;
          hits.sort((a,b)=>{
            const blue=h=>/24,\\s*119|0,\\s*97|10,\\s*120/.test(h.bg)?1:0;
            return (blue(b)-blue(a))||(a.y0-b.y0)||(a.x0-b.x0);
          });
          return hits[hits.length-1];
        }""",
        label,
    )
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        return True
    return False


def main() -> None:
    results: dict = {"connect": None, "posts": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223")
        page = next(x for x in browser.contexts[0].pages if not x.is_closed())
        page.bring_to_front()
        page.set_viewport_size({"width": 1440, "height": 900})

        # Connect FB Page destination in Suite (if offered)
        page.goto(
            "https://business.facebook.com/latest/reels_composer"
            "?asset_id=1251385088056874&business_id=1203116147241086",
            wait_until="domcontentloaded",
            timeout=90000,
        )
        time.sleep(3)
        try:
            page.locator('[role="combobox"]').first.click(timeout=3000)
            time.sleep(1)
            page.get_by_role("link", name=re.compile("Connect a Facebook Page", re.I)).click(
                timeout=3000
            )
            time.sleep(3)
            page.screenshot(path=str(OUT / "connect_page_flow.png"), full_page=True)
            snip = re.sub(r"\s+", " ", page.inner_text("body"))[:900]
            results["connect"] = {"opened": True, "snip": snip}
            print("CONNECT", snip[:400], flush=True)
            for label in ("Orbit with Ben", "Continue", "Confirm", "Connect", "Done", "Next"):
                if click_text(page, label, timeout=1800):
                    print("clicked", label, flush=True)
                    time.sleep(1.2)
            page.screenshot(path=str(OUT / "connect_page_after.png"), full_page=True)
            results["connect"]["after"] = re.sub(r"\s+", " ", page.inner_text("body"))[:700]
        except Exception as e:
            results["connect"] = {"opened": False, "error": str(e)[:220]}
            print("connect fail", e, flush=True)

        # Post each reel on the Facebook Page itself
        for i, item in enumerate(VIDEOS):
            assert item["file"].exists(), item["file"]
            print(f"\n=== FB POST {i+1} {item['id']} ===", flush=True)
            page.goto(PAGE, wait_until="domcontentloaded", timeout=90000)
            time.sleep(3)
            dismiss(page)

            opened = False
            for sel in ('[aria-label="Reel"]', 'div[aria-label="Reel"]'):
                try:
                    page.locator(sel).first.click(timeout=2500)
                    opened = True
                    break
                except Exception:
                    continue
            if not opened:
                opened = click_text(page, "Reel")
            time.sleep(2.5)
            page.screenshot(path=str(OUT / f"fb_reel_open_{i}.png"), full_page=True)

            upload_ok = False
            try:
                with page.expect_file_chooser(timeout=10000) as fc_info:
                    triggered = False
                    for lab in ("Add video", "Upload video", "Select video", "Photo/video"):
                        if click_text(page, lab, timeout=1500):
                            triggered = True
                            break
                    if not triggered:
                        page.evaluate(
                            """() => {
                              const el = Array.from(document.querySelectorAll(
                                'div[role=button], button, span'
                              )).find(e => /add video|upload|select video|photo\\/video/i.test(
                                (e.innerText||e.getAttribute('aria-label')||'')
                              ));
                              if (el) el.click();
                            }"""
                        )
                fc_info.value.set_files(str(item["file"]))
                upload_ok = True
                print("upload via chooser", flush=True)
            except Exception as e:
                print("chooser fail", e, flush=True)
                try:
                    inp = page.locator('input[type="file"]')
                    if inp.count():
                        inp.first.set_input_files(str(item["file"]))
                        upload_ok = True
                        print("upload via input", flush=True)
                except Exception as e2:
                    print("input fail", e2, flush=True)

            # wait for processing UI
            for _ in range(50):
                body = page.inner_text("body")
                if any(
                    k in body
                    for k in ("Next", "Describe", "caption", "Share", "Post", "100%", "Ready")
                ):
                    break
                time.sleep(1.2)
            page.screenshot(path=str(OUT / f"fb_reel_uploaded_{i}.png"), full_page=True)

            cap_ok = False
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
                    box.click(timeout=2000)
                    time.sleep(0.25)
                    page.keyboard.press("Meta+a")
                    page.keyboard.type(item["caption"], delay=7)
                    cap_ok = True
                    break
                except Exception:
                    continue
            print("caption", cap_ok, flush=True)

            for lab in ("Next", "Continue"):
                click_text(page, lab, timeout=2000)
                time.sleep(1.2)

            share_ok = False
            for lab in ("Share", "Post", "Publish"):
                if click_text(page, lab, timeout=3000):
                    share_ok = True
                    break
            time.sleep(5)
            page.screenshot(path=str(OUT / f"fb_reel_after_{i}.png"), full_page=True)
            entry = {
                "id": item["id"],
                "upload_ok": upload_ok,
                "caption_ok": cap_ok,
                "share_ok": share_ok,
                "url": page.url,
                "snip": re.sub(r"\s+", " ", page.inner_text("body"))[:450],
            }
            results["posts"].append(entry)
            print(entry, flush=True)
            time.sleep(2)

        # Verify
        page.goto(PAGE + "&sk=reels_tab", wait_until="domcontentloaded", timeout=90000)
        time.sleep(5)
        dismiss(page)
        try:
            page.get_by_text("Reels", exact=True).first.click(timeout=2000)
            time.sleep(3)
        except Exception:
            pass
        page.screenshot(path=str(OUT / "fb_reels_after.png"), full_page=True)
        body = page.inner_text("body")
        results["verify"] = {
            "empty": "haven't created any reels" in body.lower(),
            "fullfilm": body.lower().count("full film"),
            "snip": re.sub(r"\s+", " ", body)[:900],
        }
        (OUT / "FB_POST_RESULT.json").write_text(json.dumps(results, indent=2))
        print(
            json.dumps(
                {
                    "connect": results.get("connect"),
                    "posts": [
                        {k: p[k] for k in ("id", "upload_ok", "caption_ok", "share_ok")}
                        for p in results["posts"]
                    ],
                    "verify": results["verify"],
                },
                indent=2,
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
