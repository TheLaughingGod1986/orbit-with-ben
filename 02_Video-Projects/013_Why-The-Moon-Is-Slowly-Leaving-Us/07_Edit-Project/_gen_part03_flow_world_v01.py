#!/usr/bin/env python3
"""Part 03 Flow gens — fingerprint thumbs by src; capture new /video/ MP4s after Start."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
PROMPTS = HERE / "parts/part-03_flow_prompts_v01.json"
OUT = PROJ / "04_Generated-Clips/part03/flow_world_v01"
SHOT = Path("/tmp/flow_p03_gen")
OUT.mkdir(parents=True, exist_ok=True)
SHOT.mkdir(parents=True, exist_ok=True)

WORLD_PREFIX = (
    "Silent cinematic CGI only. No people. No readable text. No logos. "
    "No mascot. No cartoon. Premium documentary look. "
)
TARGET_PLATES = 18


def plate_count() -> int:
    return len([f for f in OUT.glob("*.mp4") if f.stat().st_size > 200_000])


def thumb_rows(page) -> list[dict]:
    return page.evaluate(
        """() => [...document.querySelectorAll('img')].map(img => {
          const alt=(img.alt||'');
          if (!/thumbnail|generated video/i.test(alt)) return null;
          const r=img.getBoundingClientRect();
          if (r.width < 80) return null;
          const src=img.currentSrc||img.src||'';
          if (!src) return null;
          return {src, x:r.x, y:r.y, w:r.width, h:r.height, alt};
        }).filter(Boolean)"""
    )


def thumb_keys(page) -> set[str]:
    keys = set()
    for t in thumb_rows(page):
        src = t["src"]
        m = re.search(r"/asb/([^?]+)", src) or re.search(
            r"/image/([0-9a-f-]{36})", src
        )
        keys.add(m.group(1) if m else src[-48:])
    return keys


def set_prompt(page, text: str) -> None:
    box = page.locator('[contenteditable="true"]').first
    box.click()
    page.keyboard.press("Meta+A")
    page.keyboard.press("Backspace")
    page.wait_for_timeout(100)
    page.keyboard.insert_text(text)
    page.wait_for_timeout(200)


def ensure_x1(page) -> None:
    try:
        page.locator('button[aria-label="Settings trigger"]').first.click(timeout=1500)
        page.wait_for_timeout(400)
        page.get_by_text("x1", exact=True).first.click(timeout=700)
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
    except Exception:
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass


def credits_blocked(page) -> bool:
    if page.locator('button[aria-label="Insufficient credits warning"]').count():
        return True
    txt = page.evaluate("() => document.body.innerText.slice(0,2000)") or ""
    return bool(re.search(r"out of Google Flow credits|Not enough credits", txt, re.I))


def start_generation(page) -> None:
    if credits_blocked(page):
        raise RuntimeError("insufficient_credits")
    loc = page.locator('button[aria-label="Start generation"]')
    if not loc.count() or loc.first.is_disabled():
        raise RuntimeError("start_unavailable")
    loc.first.click()


def scroll_to(page, t: dict) -> dict | None:
    for _ in range(25):
        # refresh matching by src suffix
        rows = thumb_rows(page)
        match = None
        for r in rows:
            if r["src"] == t["src"] or r["src"][-40:] == t["src"][-40:]:
                match = r
                break
        if match and 50 <= match["y"] <= 760:
            return match
        if match and match["y"] < 50:
            page.mouse.wheel(0, -400)
        else:
            page.mouse.wheel(0, 400)
        page.wait_for_timeout(150)
    return None


def capture_by_click(page, t: dict, dest: Path, timeout_s: float = 50) -> bool:
    box: dict[str, bytes] = {}

    def on_resp(resp) -> None:
        try:
            u = resp.url
            if "/video/" not in u or resp.status != 200:
                return
            body = resp.body()
            if b"ftyp" in body[:64] and len(body) > 200_000:
                box[u] = body
        except Exception:
            return

    page.on("response", on_resp)
    try:
        m = scroll_to(page, t) or t
        page.mouse.click(m["x"] + m["w"] / 2, max(60, min(780, m["y"] + m["h"] / 2)))
        t0 = time.time()
        while time.time() - t0 < timeout_s:
            if box:
                body = next(iter(box.values()))
                dest.write_bytes(body)
                page.keyboard.press("Escape")
                return True
            srcs = page.evaluate(
                """() => [...document.querySelectorAll('video')]
                  .map(v => v.currentSrc || v.src || '')"""
            )
            for src in srcs:
                if not src or "/video/" not in src:
                    continue
                r = page.request.get(src)
                body = r.body()
                if r.status == 200 and b"ftyp" in body[:64] and len(body) > 200_000:
                    dest.write_bytes(body)
                    page.keyboard.press("Escape")
                    return True
            page.wait_for_timeout(400)
        page.keyboard.press("Escape")
        return False
    finally:
        try:
            page.remove_listener("response", on_resp)
        except Exception:
            pass


def main() -> None:
    rows = json.loads(PROMPTS.read_text())
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = next(
            pg
            for ctx in browser.contexts
            for pg in ctx.pages
            if "flow.google" in (pg.url or "")
        )
        page.bring_to_front()
        page.on("dialog", lambda d: d.dismiss())
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        ensure_x1(page)

        report = []
        print(f"start plates={plate_count()}", flush=True)

        for i, row in enumerate(rows):
            stem = row["id"]
            if list(OUT.glob(f"{stem}_*.mp4")):
                print(f"SKIP {stem}", flush=True)
                report.append({"id": stem, "status": "skip"})
                continue
            if plate_count() >= TARGET_PLATES:
                print(f"enough plates ({plate_count()})", flush=True)
                break
            if credits_blocked(page):
                print("BLOCKED credits", flush=True)
                report.append({"id": stem, "status": "blocked_credits"})
                break

            prompt = WORLD_PREFIX + row["prompt"]
            print(
                f"\n=== [{i+1}/{len(rows)}] {stem} plates={plate_count()} ===",
                flush=True,
            )

            before_keys = thumb_keys(page)
            before_rows = { (re.search(r'/asb/([^?]+)', t['src']) or re.search(r'/image/([0-9a-f-]{36})', t['src']) or type('X',(),{'group':lambda s,t=t:t['src'][-48:]})()).group(1): t for t in thumb_rows(page) }

            # network bag for any new video during/after gen
            bag: dict[str, bytes] = {}

            def on_any(resp) -> None:
                try:
                    u = resp.url
                    if "/video/" not in u or resp.status != 200:
                        return
                    body = resp.body()
                    if b"ftyp" in body[:64] and len(body) > 200_000:
                        bag[u] = body
                except Exception:
                    return

            page.on("response", on_any)
            set_prompt(page, prompt)
            page.screenshot(path=str(SHOT / f"prompt_{stem}.png"))
            try:
                start_generation(page)
            except Exception as e:
                page.remove_listener("response", on_any)
                print(f"  FAIL start: {e}", flush=True)
                report.append({"id": stem, "status": "fail", "error": str(e)})
                if "insufficient" in str(e) or credits_blocked(page):
                    break
                continue
            print("  submitted", flush=True)

            new_row = None
            t0 = time.time()
            while time.time() - t0 < 300:
                # prefer network capture if player prefetch happens
                if bag:
                    break
                keys_now = thumb_keys(page)
                fresh_keys = [k for k in keys_now if k not in before_keys]
                if fresh_keys:
                    page.wait_for_timeout(5000)
                    # pick top-most fresh thumb
                    for t in sorted(thumb_rows(page), key=lambda r: r["y"]):
                        m = re.search(r"/asb/([^?]+)", t["src"]) or re.search(
                            r"/image/([0-9a-f-]{36})", t["src"]
                        )
                        key = m.group(1) if m else t["src"][-48:]
                        if key in fresh_keys:
                            new_row = t
                            break
                    if new_row:
                        break
                if credits_blocked(page):
                    print("  credits died", flush=True)
                    break
                page.wait_for_timeout(3000)
                print(f"  waiting… {int(time.time()-t0)}s bag={len(bag)}", flush=True)

            files = []
            if bag and not new_row:
                # save first network video
                u, body = next(iter(bag.items()))
                m = re.search(r"/video/([0-9a-f-]{36})", u)
                short = (m.group(1).split("-")[0][:8] if m else f"net{int(time.time())%10000:04d}")
                dest = OUT / f"{stem}_{short}.mp4"
                dest.write_bytes(body)
                files.append(dest.name)
                print(f"  net_capture {short} ok", flush=True)
            elif new_row:
                m = re.search(r"/asb/([^?]+)", new_row["src"]) or re.search(
                    r"/image/([0-9a-f-]{36})", new_row["src"]
                )
                short = (m.group(1)[:8] if m else f"src{int(time.time())%10000:04d}")
                dest = OUT / f"{stem}_{short}.mp4"
                # remove global listener before click capture to avoid double-handle issues
                try:
                    page.remove_listener("response", on_any)
                except Exception:
                    pass
                ok = capture_by_click(page, new_row, dest)
                print(f"  click_capture {short} -> {ok}", flush=True)
                if ok:
                    files.append(dest.name)
            else:
                print("  FAIL no new thumb/video", flush=True)

            try:
                page.remove_listener("response", on_any)
            except Exception:
                pass

            report.append(
                {
                    "id": stem,
                    "status": "ok" if files else "fail",
                    "files": files,
                }
            )
            page.keyboard.press("Escape")
            page.wait_for_timeout(800)

        (OUT / "_gen_report_v04.json").write_text(json.dumps(report, indent=2) + "\n")
        print("DONE plates=", plate_count(), flush=True)
        print(json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
    main()
