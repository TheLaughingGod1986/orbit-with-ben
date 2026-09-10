#!/usr/bin/env python3
"""Replace Orbit-first mystery 07 (`mAAMsbhm88w`, Tue 16 Sep 11:30) with v02 world-open.

Replace rule (`orbit-shorts-punch-first`): upload new private → metadata/thumb parity →
set new publishAt exactly → Related → then unschedule old (Private, no publishAt).
Never delete the old id.

Steps are idempotent-ish and state is written to STATE after each one so a re-run
resumes rather than uploading twice.

Run log (10 Sep 2026): `U.upload_one` uploaded the file but its Save click never landed
(Studio's dialog Save is `ytcp-button#done-button`, not a native button role) so the video
sat as a Draft. Finished by hand from the Shorts list → "Edit draft" → Next ×3 → Private →
`#done-button` → id `to-b2baeoWQ`; `new_id` was written into STATE and this script resumed
for thumb → schedule → Related → unschedule old. Related picker needed a real mouse click
on the `ytcp-entity-card` (force-click on the cell did not register).
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _upload_schedule_mystery_punches_v01 as U  # noqa: E402

OLD_ID = "mAAMsbhm88w"
ITEM_JSON = HERE / "MYSTERY_07_V02_WORLD_OPEN.json"
STATE = HERE / "MYSTERY_07_V02_REPLACE_LIVE.json"
WORK = Path("/tmp/orbit_neutron_fix")
U.AUDIT = WORK / "replace_audit"
U.AUDIT.mkdir(parents=True, exist_ok=True)


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"old_id": OLD_ID, "started_at": datetime.now(timezone.utc).isoformat()}


def save_state(s: dict) -> None:
    s["updated_at"] = datetime.now(timezone.utc).isoformat()
    STATE.write_text(json.dumps(s, indent=2) + "\n")


def read_old(page, ctx, s: dict) -> None:
    page.goto(f"https://studio.youtube.com/video/{OLD_ID}/edit", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(5000)
    U.dismiss(page)
    boxes = page.locator("#textbox")
    s["old_title"] = boxes.nth(0).inner_text().strip()
    s["old_description"] = boxes.nth(1).inner_text().strip()
    src = page.evaluate(
        """() => {
          const walk=(root)=>{
            for (const img of root.querySelectorAll('img')) {
              const u=img.currentSrc||img.src||'';
              if (/ytimg|ggpht|googleusercontent/.test(u) && img.getBoundingClientRect().width>80) return u;
            }
            for (const el of root.querySelectorAll('*')) { if (el.shadowRoot) { const x=walk(el.shadowRoot); if (x) return x; } }
            return null;
          };
          const ed=document.querySelector('ytcp-thumbnails-compact-editor, ytcp-thumbnail-editor');
          return walk(ed||document);
        }"""
    )
    s["old_thumb_src"] = src
    if src:
        resp = ctx.request.get(src)
        if resp.ok:
            p = WORK / f"thumb_{OLD_ID}.jpg"
            p.write_bytes(resp.body())
            s["old_thumb_file"] = str(p)
    page.screenshot(path=str(U.AUDIT / "00_old_before.png"))
    save_state(s)


def set_thumbnail(page, vid: str, thumb: Path, s: dict) -> None:
    page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(5000)
    U.dismiss(page)
    inputs = page.locator("ytcp-thumbnails-compact-editor input[type=file], ytcp-thumbnail-editor input[type=file], ytcp-thumbnail-uploader input[type=file]")
    if not inputs.count():
        inputs = page.locator("input[type=file][accept*='image']")
    if not inputs.count():
        s["thumb"] = {"ok": False, "error": "no_file_input"}
        save_state(s)
        return
    inputs.first.set_input_files(str(thumb))
    page.wait_for_timeout(4000)
    saved = U.save_edit(page)
    page.wait_for_timeout(2500)
    s["thumb"] = {"ok": saved, "file": str(thumb)}
    page.screenshot(path=str(U.AUDIT / "03_thumb.png"))
    save_state(s)


def set_private(page, vid: str, s: dict) -> None:
    page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(5000)
    U.dismiss(page)
    U.open_visibility(page)
    page.evaluate(
        """() => {
          const walk=(r)=>{
            for (const el of r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]')) {
              const t=(el.innerText||'').toLowerCase();
              if (t.includes('private') && !t.includes('schedule')) { el.click(); return true; }
            }
            for (const el of r.querySelectorAll('*')) { if (el.shadowRoot && walk(el.shadowRoot)) return true; }
            return false;
          };
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]');
          return walk(dlg||document);
        }"""
    )
    page.wait_for_timeout(800)
    U.click_done(page)
    saved = U.save_edit(page)
    page.wait_for_timeout(2500)
    page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(5000)
    body = page.locator("body").inner_text()
    snip = body.split("Visibility", 1)[-1][:200].replace("\n", " ") if "Visibility" in body else ""
    s["old_unscheduled"] = {"saved": saved, "visibility_snip": snip, "ok": "Private" in snip and "Scheduled" not in snip}
    page.screenshot(path=str(U.AUDIT / "06_old_private.png"))
    save_state(s)


def verify_new(page, vid: str, s: dict) -> None:
    """Read the Visibility dialog + Related picker directly (body-text snippets gave a
    false 'related_ok' from the thumbnail-preview title on the first run)."""
    page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(5000)
    U.dismiss(page)
    rel = page.locator("ytcp-shorts-content-links-picker").first.inner_text().replace("\n", " ")
    U.open_visibility(page)
    page.wait_for_timeout(1200)
    dlg = page.locator('tp-yt-paper-dialog[aria-label="Select video privacy"]')
    vis = re.sub(r"\s+", " ", dlg.inner_text()) if dlg.count() else ""
    page.keyboard.press("Escape")
    s["verify_new"] = {
        "visibility_dialog": vis[:300],
        "related_field": rel[:200],
        "scheduled_16_sep": ("16 Sep" in vis and "11:30" in vis),
        # Studio shows the long under its *current* title (A/B variant in flight) — accept either.
        "related_ok": ("None" not in rel and "Neutron Star" in rel),
    }
    page.screenshot(path=str(U.AUDIT / "05_new_verify.png"))
    save_state(s)


def main() -> int:
    item = json.loads(ITEM_JSON.read_text())
    s = load_state()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(U.CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.set_viewport_size({"width": 1500, "height": 1300})
        try:
            if "old_title" not in s:
                print("read old…", flush=True)
                read_old(page, ctx, s)
            # parity: use live title/description of the old id
            item["title"] = s["old_title"] or item["title"]
            if s.get("old_description"):
                item["description"] = s["old_description"]
            if not s.get("new_id"):
                print("upload new…", flush=True)
                up = U.upload_one(page, item)
                s["upload"] = up
                s["new_id"] = up.get("video_id") or ""
                save_state(s)
                if not s["new_id"]:
                    print("upload failed", up)
                    return 1
            vid = s["new_id"]
            if s.get("old_thumb_file") and "thumb" not in s:
                print("thumb…", flush=True)
                set_thumbnail(page, vid, Path(s["old_thumb_file"]), s)
            if "schedule" not in s or not s["schedule"].get("ok"):
                print("schedule…", flush=True)
                s["schedule"] = U.schedule_one(page, item, vid)
                save_state(s)
            if "related" not in s or not s["related"].get("ok"):
                print("related…", flush=True)
                s["related"] = U.set_related(page, vid, "07")
                save_state(s)
            verify_new(page, vid, s)
            v = s["verify_new"]
            if v["scheduled_16_sep"] and v["related_ok"] and "old_unscheduled" not in s:
                print("unschedule old…", flush=True)
                set_private(page, OLD_ID, s)
            elif not (v["scheduled_16_sep"] and v["related_ok"]):
                print("NEW NOT VERIFIED — old left scheduled", v)
        finally:
            page.close()
    s["finished_at"] = datetime.now(timezone.utc).isoformat()
    s["all_ok"] = bool(
        s.get("new_id")
        and s.get("verify_new", {}).get("scheduled_16_sep")
        and s.get("verify_new", {}).get("related_ok")
        and s.get("old_unscheduled", {}).get("ok")
    )
    save_state(s)
    print(json.dumps(s, indent=2))
    return 0 if s["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
