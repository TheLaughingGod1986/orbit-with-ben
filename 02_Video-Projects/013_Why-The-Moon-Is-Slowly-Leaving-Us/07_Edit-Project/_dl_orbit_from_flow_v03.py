#!/usr/bin/env python3
"""Download on-model Orbit cards from the open Flow project (CDP :9222)."""
from __future__ import annotations

import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "04_Generated-Clips/part01/orbit_from_flow_v03"
SHOT = Path("/tmp/flow_orbit_dl")
OUT.mkdir(parents=True, exist_ok=True)
SHOT.mkdir(parents=True, exist_ok=True)

CDP = "http://127.0.0.1:9222"

COLLECT_THUMBS_JS = """
() => [...document.querySelectorAll('img[alt="Generated video thumbnail"]')].map(img => {
  const r = img.getBoundingClientRect();
  let title = '';
  let el = img;
  while (el && el !== document.body) {
    const t = (el.innerText || '').trim();
    if (t && t.length > 10 && t.length < 500 && !t.startsWith('play_circle')) {
      title = t.split('\\n').filter(Boolean)[0].slice(0, 140);
      break;
    }
    el = el.parentElement;
  }
  return {
    src: img.currentSrc || img.src || '',
    x: Math.round(r.x),
    y: Math.round(r.y),
    w: Math.round(r.width),
    h: Math.round(r.height),
    title,
  };
})
"""

SCROLL_JS = """
() => {
  const sc = [...document.querySelectorAll('*')].find(
    el => el.scrollHeight > el.clientHeight + 200
      && el.querySelector('img[alt="Generated video thumbnail"], button')
  );
  if (sc) sc.scrollBy(0, 300);
  else window.scrollBy(0, 300);
}
"""

SCROLL_TOP_JS = """
() => {
  const sc = [...document.querySelectorAll('*')].find(
    el => el.scrollHeight > el.clientHeight + 200
  );
  if (sc) sc.scrollTop = 0;
  window.scrollTo(0, 0);
}
"""


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = next(
            pg
            for ctx in browser.contexts
            for pg in ctx.pages
            if "flow.google" in (pg.url or "")
        )
        page.bring_to_front()
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        page.evaluate(SCROLL_TOP_JS)
        page.wait_for_timeout(600)
        page.screenshot(path=str(SHOT / "top.png"))

        seen: set[str] = set()
        all_thumbs: list[dict] = []
        for _ in range(10):
            thumbs = page.evaluate(COLLECT_THUMBS_JS)
            for t in thumbs:
                m = re.search(r"/image/([0-9a-f-]{36})", t.get("src") or "")
                key = m.group(1) if m else t.get("src") or ""
                if not key or key in seen or t.get("w", 0) < 100:
                    continue
                seen.add(key)
                t["uid"] = m.group(1) if m else None
                all_thumbs.append(t)
                print(
                    f"FOUND y={t['y']} title={t['title'][:80]!r} uid={t['uid']}",
                    flush=True,
                )
            page.evaluate(SCROLL_JS)
            page.wait_for_timeout(450)

        print(f"TOTAL {len(all_thumbs)}", flush=True)
        page.evaluate(SCROLL_TOP_JS)
        page.wait_for_timeout(400)

        orbitish = [
            t
            for t in all_thumbs
            if re.search(r"orbit|look|moon|visor|identity|sphere", t["title"], re.I)
        ]
        picks = (orbitish or all_thumbs)[:3]
        print(f"picks={len(picks)}", flush=True)

        captured: list[tuple[str, bytes]] = []

        def on_resp(resp) -> None:
            try:
                u = resp.url
                ct = (resp.headers.get("content-type") or "").lower()
                if resp.status != 200:
                    return
                interesting = (
                    "video" in ct
                    or u.endswith(".mp4")
                    or "/video/" in u
                    or "octet-stream" in ct
                )
                if not interesting:
                    return
                b = resp.body()
                if len(b) > 200_000 and b"ftyp" in b[:64]:
                    captured.append((u, b))
                    print(f"CAPTURE {len(b)} {u[:140]}", flush=True)
            except Exception:
                return

        page.on("response", on_resp)

        for i, t in enumerate(picks):
            print(f"\n=== pick {i} {t['title'][:70]} ===", flush=True)
            uid = t.get("uid") or ""
            page.evaluate(
                """(uid) => {
                  const imgs = [...document.querySelectorAll('img[alt="Generated video thumbnail"]')];
                  const hit = imgs.find(img => (img.currentSrc || img.src || '').includes(uid));
                  if (hit) hit.scrollIntoView({block: 'center'});
                }""",
                uid,
            )
            page.wait_for_timeout(500)
            box = page.evaluate(
                """(uid) => {
                  const imgs = [...document.querySelectorAll('img[alt="Generated video thumbnail"]')];
                  const hit = imgs.find(img => (img.currentSrc || img.src || '').includes(uid));
                  if (!hit) return null;
                  const r = hit.getBoundingClientRect();
                  return {x: r.x, y: r.y, w: r.width, h: r.height, src: hit.currentSrc || hit.src};
                }""",
                uid,
            )
            if not box:
                print("not visible", flush=True)
                continue

            page.mouse.move(box["x"] + box["w"] / 2, box["y"] + box["h"] / 2)
            page.wait_for_timeout(350)
            page.mouse.click(box["x"] + box["w"] - 28, box["y"] + 18)
            page.wait_for_timeout(500)
            page.screenshot(path=str(SHOT / f"menu_pick_{i}.png"))

            before = len(captured)
            dl = page.locator('[role=menuitem]:has-text("Download")')
            if dl.count() == 0:
                print("no download item", flush=True)
                page.keyboard.press("Escape")
                continue

            saved = False
            try:
                with page.expect_download(timeout=10_000) as di:
                    dl.first.click()
                d = di.value
                dest = OUT / f"orbit_pick_{i:02d}.mp4"
                d.save_as(str(dest))
                print(f"EVENT SAVE {dest} {dest.stat().st_size}", flush=True)
                saved = True
            except Exception as e:
                print(f"download event miss {e.__class__.__name__}", flush=True)
                for _ in range(25):
                    if len(captured) > before:
                        break
                    page.wait_for_timeout(400)
                if len(captured) > before:
                    dest = OUT / f"orbit_pick_{i:02d}.mp4"
                    dest.write_bytes(captured[-1][1])
                    print(f"NET SAVE {dest} {dest.stat().st_size}", flush=True)
                    saved = True
                elif t.get("src"):
                    vurl = t["src"].replace("/image/", "/video/")
                    r = page.request.get(vurl)
                    b = r.body()
                    print(f"direct {r.status} {len(b)}", flush=True)
                    if r.status == 200 and b"ftyp" in b[:64]:
                        dest = OUT / f"orbit_pick_{i:02d}.mp4"
                        dest.write_bytes(b)
                        print(f"DIRECT SAVE {dest} {dest.stat().st_size}", flush=True)
                        saved = True

            if not saved:
                print("FAILED to save pick", i, flush=True)
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)

        print("done", list(OUT.glob("*.mp4")), flush=True)


if __name__ == "__main__":
    main()
