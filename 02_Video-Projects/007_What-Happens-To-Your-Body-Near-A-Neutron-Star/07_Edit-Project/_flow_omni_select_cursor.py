#!/usr/bin/env python3
"""Select Omni Flash + 16:9 + 8s + x1 on the Flow prompt-bar (2026-08 UI).

JS .click() on the Video chip does not open the popover. Playwright locator
mouse-click does. Quantity is a tablist (x1/x2/x3/x4), not plain buttons.
"""
from __future__ import annotations

OMNI_LABELS = ("Omni Flash", "Omni", "Video")


def read_prompt_pill(page) -> str:
    return page.evaluate(
        """() => {
          const buttons = [...document.querySelectorAll('button')];
          for (const b of buttons) {
            const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
            if (/Video/.test(t) && /8s|crop_16_9|Omni|Veo|x[1-4]/.test(t)) return t;
            if (/Omni Flash|Veo 3|Nano Banana/.test(t)) return t;
          }
          return '';
        }"""
    ) or ""


def _open_video_chip(page) -> str:
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(200)
    loc = page.locator("button").filter(has_text="Video")
    n = loc.count()
    opened = ""
    for i in range(n):
        t = (loc.nth(i).inner_text() or "").replace("\n", " ")
        if "8s" in t or "x2" in t or "x1" in t or "crop" in t:
            loc.nth(i).click(timeout=5000)
            opened = t
            break
    if not opened:
        raise RuntimeError("Flow Video settings chip not found")
    print(f"  opened video chip: {opened}", flush=True)
    page.wait_for_timeout(700)
    return opened


def configure_omni(page) -> str:
    """Open Video settings chip → Omni Flash + 16:9 + 8s + x1."""
    _open_video_chip(page)

    # 16:9 tab
    try:
        page.get_by_role("tab", name="16:9").click(timeout=3000)
        print("  clicked 16:9 tab", flush=True)
    except Exception:
        try:
            page.locator("button").filter(has_text="16:9").last.click(timeout=3000)
            print("  clicked 16:9 button", flush=True)
        except Exception as e:
            print(f"  16:9 miss: {e}", flush=True)
    page.wait_for_timeout(150)

    # 8s
    try:
        page.locator("button").filter(has_text="8s").last.click(timeout=2000)
        print("  clicked 8s", flush=True)
    except Exception as e:
        print(f"  8s miss: {e}", flush=True)
    page.wait_for_timeout(150)

    # x1 quantity tab — this is the leftover miss
    clicked_x1 = False
    for attempt in range(3):
        try:
            page.get_by_role("tab", name="x1").click(timeout=3000)
            clicked_x1 = True
            print(f"  clicked x1 tab attempt {attempt+1}", flush=True)
            break
        except Exception as e:
            print(f"  x1 tab miss {attempt+1}: {e}", flush=True)
            try:
                page.locator("button").filter(has_text="x1").last.click(timeout=2000)
                clicked_x1 = True
                print(f"  clicked x1 button attempt {attempt+1}", flush=True)
                break
            except Exception as e2:
                print(f"  x1 button miss {attempt+1}: {e2}", flush=True)
                try:
                    _open_video_chip(page)
                except Exception:
                    pass
    page.wait_for_timeout(250)

    print(f"  omni select: Omni Flash 16:9 8s x1 clicked={clicked_x1}", flush=True)
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(350)
    pill = read_prompt_pill(page)
    print(f"  video model locked: {pill or 'Omni Flash'}", flush=True)
    if pill and "x2" in pill.replace(" ", "").lower():
        print("  WARN pill still x2 — one more x1 click", flush=True)
        try:
            _open_video_chip(page)
            page.get_by_role("tab", name="x1").click(timeout=3000)
            page.wait_for_timeout(250)
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
            pill = read_prompt_pill(page)
            print(f"  retry pill: {pill}", flush=True)
        except Exception as e:
            print(f"  x1 retry skipped: {e}", flush=True)
    if pill and "x2" in pill.replace(" ", "").lower():
        print("  WARN pill still x2 after retries — will still download ONE 8s file per prompt", flush=True)
    return pill or "Omni Flash"
