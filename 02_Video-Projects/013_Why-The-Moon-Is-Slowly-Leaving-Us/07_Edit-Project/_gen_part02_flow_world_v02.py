#!/usr/bin/env python3
"""Part 02 Flow world gens — wait on new thumbnails, click to capture signed MP4s."""
from __future__ import annotations

import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
PROMPTS = HERE / "parts/part-02_flow_prompts_v01.json"
OUT = PROJ / "04_Generated-Clips/part02/flow_world_v01"
SHOT = Path("/tmp/flow_p02_gen")
OUT.mkdir(parents=True, exist_ok=True)
SHOT.mkdir(parents=True, exist_ok=True)

WORLD_PREFIX = (
    "Silent cinematic CGI only. No people. No readable text. No logos. "
    "No mascot. No cartoon. Premium documentary look. "
)


def thumb_uids(page) -> dict[str, dict]:
    rows = page.evaluate(
        """() => [...document.querySelectorAll('img[alt="Generated video thumbnail"]')]
          .map(img => {
            const r = img.getBoundingClientRect();
            const m = (img.currentSrc || '').match(/image\\/([0-9a-f-]{36})/);
            return {
              uid: m && m[1],
              x: r.x, y: r.y, w: r.width, h: r.height
            };
          }).filter(t => t.uid && t.w > 100)"""
    )
    return {r["uid"]: r for r in rows}


def set_prompt(page, text: str) -> None:
    box = page.locator('[contenteditable="true"]').first
    box.click()
    page.keyboard.press("Meta+A")
    page.keyboard.press("Backspace")
    page.wait_for_timeout(150)
    page.keyboard.insert_text(text)
    page.wait_for_timeout(250)


def start_generation(page) -> None:
    page.locator('button[aria-label="Start generation"]').first.click()


def scroll_thumb_into_view(page, uid: str) -> dict | None:
    for _ in range(25):
        thumbs = thumb_uids(page)
        t = thumbs.get(uid)
        if t and 40 <= t["y"] <= 700:
            return t
        if t and t["y"] < 40:
            page.mouse.wheel(0, -350)
        elif t and t["y"] > 700:
            page.mouse.wheel(0, 350)
        else:
            page.mouse.wheel(0, -500)
        page.wait_for_timeout(200)
    return thumb_uids(page).get(uid)


def capture_uid(page, uid: str, dest: Path, timeout_s: float = 50) -> bool:
    box: dict[str, bytes] = {}

    def on_resp(resp) -> None:
        try:
            u = resp.url
            if f"/video/{uid}" not in u or resp.status != 200:
                return
            body = resp.body()
            if b"ftyp" in body[:64] and len(body) > 200_000:
                box[uid] = body
        except Exception:
            return

    page.on("response", on_resp)
    try:
        t = scroll_thumb_into_view(page, uid)
        if not t:
            return False
        page.mouse.click(t["x"] + t["w"] / 2, t["y"] + t["h"] / 2)
        t0 = time.time()
        while time.time() - t0 < timeout_s:
            if uid in box:
                dest.write_bytes(box[uid])
                page.keyboard.press("Escape")
                return True
            srcs = page.evaluate(
                """() => [...document.querySelectorAll('video')]
                  .map(v => v.currentSrc || v.src || '')"""
            )
            for src in srcs:
                if uid in (src or ""):
                    r = page.request.get(src)
                    body = r.body()
                    if r.status == 200 and b"ftyp" in body[:64] and len(body) > 200_000:
                        dest.write_bytes(body)
                        page.keyboard.press("Escape")
                        return True
            page.wait_for_timeout(500)
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
        page.wait_for_timeout(400)

        report = []
        for i, row in enumerate(rows):
            stem = row["id"]
            if list(OUT.glob(f"{stem}_*.mp4")):
                print(f"SKIP {stem}", flush=True)
                report.append({"id": stem, "status": "skip"})
                continue

            useful = [
                f
                for f in OUT.glob("*.mp4")
                if not f.name.startswith("gallery_") and "p02_new_" not in f.name
            ]
            if len(useful) >= 16:
                print("enough plates — stop", flush=True)
                break

            prompt = WORLD_PREFIX + row["prompt"]
            print(f"\n=== [{i+1}/{len(rows)}] {stem} ===", flush=True)
            before = set(thumb_uids(page))
            set_prompt(page, prompt)
            page.screenshot(path=str(SHOT / f"prompt_{stem}.png"))
            start_generation(page)
            print("  submitted", flush=True)

            new_uids: list[str] = []
            t0 = time.time()
            while time.time() - t0 < 360:
                now = thumb_uids(page)
                fresh = [u for u in now if u not in before]
                if fresh:
                    page.wait_for_timeout(8000)
                    now = thumb_uids(page)
                    new_uids = [u for u in now if u not in before]
                    break
                page.wait_for_timeout(4000)
                print(f"  waiting thumbs… {int(time.time()-t0)}s", flush=True)

            if not new_uids:
                report.append({"id": stem, "status": "fail", "error": "no new thumbs"})
                print("  FAIL no thumbs", flush=True)
                continue

            files = []
            for uid in new_uids[:2]:
                dest = OUT / f"{stem}_{uid[:8]}.mp4"
                ok = capture_uid(page, uid, dest)
                print(f"  capture {uid[:8]} -> {ok}", flush=True)
                if ok:
                    files.append(dest.name)
            report.append(
                {
                    "id": stem,
                    "status": "ok" if files else "fail",
                    "uids": new_uids,
                    "files": files,
                }
            )
            page.wait_for_timeout(1200)

        (OUT / "_gen_report_v02.json").write_text(json.dumps(report, indent=2) + "\n")
        print("DONE", json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
    main()
