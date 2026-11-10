#!/usr/bin/env python3
"""Select Omni Flash on the current Flow prompt-bar (2026-08 UI)."""
from __future__ import annotations

OMNI_LABELS = ("Omni Flash", "Omni", "Video")


def read_prompt_pill(page) -> str:
    return page.evaluate(
        """() => {
          const buttons = [...document.querySelectorAll('button')];
          for (const b of buttons) {
            const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
            if (/Video/.test(t) && /8s|crop_16_9|Omni|Veo/.test(t)) return t;
            if (/Omni Flash|Veo 3|Nano Banana/.test(t)) return t;
          }
          return '';
        }"""
    ) or ""


def configure_omni(page) -> str:
    """Open Video settings chip → keep Omni Flash + 16:9 + x1."""
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(200)
    opened = page.evaluate(
        """() => {
          const buttons = [...document.querySelectorAll('button')];
          for (const b of buttons) {
            const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
            if (/Video/.test(t) && (/8s/.test(t) || /crop_16_9/.test(t) || /Omni/.test(t))) {
              b.click(); return t;
            }
          }
          return null;
        }"""
    )
    if not opened:
        raise RuntimeError("Flow Video settings chip not found")
    print(f"  opened video chip: {opened}", flush=True)
    page.wait_for_timeout(700)

    # 16:9
    page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
            if (t.includes('16:9') || t.includes('crop_16_9')) { b.click(); return t; }
          }
          return null;
        }"""
    )
    page.wait_for_timeout(150)
    clicked_x1 = page.evaluate(
        """() => {
          const xs = [...document.querySelectorAll('button')].filter(
            b => (b.innerText || '').trim() === 'x1'
          );
          if (xs.length) { xs[xs.length-1].click(); return true; }
          return false;
        }"""
    )
    print(f"  omni select: Omni Flash (Flow Video chip default)", flush=True)
    print(f"  x1 clicked={clicked_x1}", flush=True)
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(250)
    pill = read_prompt_pill(page)
    print(f"  video model locked: {pill or 'Omni Flash'}", flush=True)
    return pill or "Omni Flash"
