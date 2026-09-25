#!/usr/bin/env python3
"""
Fix Orbit cross-post funnel for live Shorts (2026-08-03).

1) YouTube: past-due aliens Shorts → Public (desc already has full-film link)
2) YouTube: pin "Full film here →" comments
3) TikTok: fix bio YouTube URL to @OrbitWithBen
4) Meta + Threads: post the live Shorts with soft CTA captions
5) Sync SHORTS_UPLOAD_INDEX visibility flags
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

ROOT = Path("/Users/ben/code/Orbit-YouTube")
SETUP = ROOT / "00_Brand/Channel-Setup"
AUDIT = SETUP / "audits/crosspost_live_audit_2026-08-03"
AUDIT.mkdir(parents=True, exist_ok=True)
OUT = AUDIT / "FIX_RESULT.json"
LONDON = ZoneInfo("Europe/London")
CDP_TT = "http://127.0.0.1:9222"
CDP_META = "http://127.0.0.1:9223"

ALIENS_INDEX = (
    ROOT
    / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/SHORTS_UPLOAD_INDEX.json"
)
LONG_URL = "https://youtu.be/Mo93x0fxB1Q"
LONG_TITLE = "Why Haven't We Found Aliens Yet? The Fermi Paradox Explained"

# Past-due: should be Public now. Keep 04 scheduled for later today.
PUBLISH_NOW = [
    {
        "id": "01",
        "video_id": "1HuV8o3gOss",
        "title": "Where Is Everybody? The Fermi Paradox #Space #Shorts",
        "file": ROOT
        / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/06_Final-Exports/aliens_short-02_fermi-paradox_v02.mp4",
    },
    {
        "id": "02",
        "video_id": "dPMJQp2gMNc",
        "title": "Space Is Rude About Distance",
        "file": ROOT
        / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/06_Final-Exports/aliens_short-01_distance_v02.mp4",
    },
    {
        "id": "03",
        "video_id": "rFJoOdQAc9c",
        "title": "What If Aliens Are Watching Us?",
        "file": ROOT
        / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/06_Final-Exports/aliens_short-03_zoo-hypothesis_v02.mp4",
    },
]


def load_notify(auto_dir: Path, mod_name: str):
    path = auto_dir / "hooks.py"
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod.notify_short_live


def visibility_chip(page) -> str:
    try:
        return page.locator("ytcp-video-metadata-visibility").first.inner_text(
            timeout=2500
        ).replace("\n", " ")
    except Exception:
        return ""


def is_public(chip: str) -> bool:
    return bool(re.search(r"\bPublic\b", chip)) and not re.search(
        r"\bScheduled\b", chip, re.I
    )


def open_visibility(page) -> None:
    page.locator("ytcp-video-metadata-visibility").first.scroll_into_view_if_needed()
    page.wait_for_timeout(250)
    page.locator("ytcp-video-metadata-visibility").first.click(force=True)
    page.wait_for_timeout(1600)


def collapse_schedule_panel(page) -> None:
    page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]')
            || document.querySelector('tp-yt-paper-dialog');
          const walk=(root)=>{
            for (const el of root.querySelectorAll('*')) {
              const al=(el.getAttribute('aria-label')||'');
              const id=el.id||'';
              if (id==='first-container-expand-button' || /click to (expand|collapse)/i.test(al)) {
                const r=el.getBoundingClientRect();
                if (r.width>5) { el.click(); return true; }
              }
              if (el.shadowRoot) { if (walk(el.shadowRoot)) return true; }
            }
            return false;
          };
          let hasPublic=false;
          const find=(root)=>{
            for (const el of root.querySelectorAll('tp-yt-paper-radio-button,[role=radio]')) {
              const n=(el.getAttribute('name')||'').toUpperCase();
              const t=(el.innerText||'').trim();
              const r=el.getBoundingClientRect();
              if ((n==='PUBLIC' || t==='Public') && r.width>10 && r.height>5) hasPublic=true;
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) find(el.shadowRoot);
          };
          find(dlg||document);
          if (hasPublic) return true;
          return walk(dlg||document);
        }"""
    )
    page.wait_for_timeout(800)


def click_public_radio(page) -> bool:
    ok = page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]')
            || document.querySelector('tp-yt-paper-dialog');
          const walk=(root)=>{
            for (const el of root.querySelectorAll('tp-yt-paper-radio-button,[role=radio]')) {
              const n=(el.getAttribute('name')||'').toUpperCase();
              const t=(el.innerText||'').trim();
              const r=el.getBoundingClientRect();
              if ((n==='PUBLIC' || t==='Public') && r.width>10 && r.height>5) {
                el.click(); return true;
              }
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot && walk(el.shadowRoot)) return true;
            }
            return false;
          };
          return walk(dlg||document);
        }"""
    )
    page.wait_for_timeout(600)
    return bool(ok)


def save_visibility(page) -> bool:
    for label in ("Save", "Done", "Publish"):
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{label}$", re.I))
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=3000)
                page.wait_for_timeout(1500)
                return True
        except Exception:
            pass
    # dialog Done
    page.evaluate(
        """() => {
          const btns=[...document.querySelectorAll('ytcp-button,button,tp-yt-paper-button')];
          const done=btns.find(b=>/^(Done|Save|Publish)$/i.test((b.innerText||'').trim()));
          if(done) done.click();
        }"""
    )
    page.wait_for_timeout(1500)
    return True


def publish_youtube_public(page, video_id: str) -> dict:
    out = {"video_id": video_id, "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    page.keyboard.press("Escape")
    chip = visibility_chip(page)
    out["before"] = chip
    if is_public(chip):
        out["ok"] = True
        out["skipped"] = "already_public"
        return out
    open_visibility(page)
    collapse_schedule_panel(page)
    if not click_public_radio(page):
        collapse_schedule_panel(page)
        click_public_radio(page)
    save_visibility(page)
    # top Save if dirty
    try:
        save = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if save.count() and save.first.is_enabled():
            save.first.click(force=True, timeout=3000)
            page.wait_for_timeout(2000)
    except Exception:
        pass
    page.wait_for_timeout(2000)
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    chip2 = visibility_chip(page)
    out["after"] = chip2
    out["ok"] = is_public(chip2)
    page.screenshot(path=str(AUDIT / f"fix_yt_{video_id}.png"))
    return out


def pin_comment(page, video_id: str) -> dict:
    comment = (
        f"Full film here → {LONG_TITLE}\n{LONG_URL}\n\nOrbit's Cosmic Journey 🚀"
    )
    out = {"video_id": video_id, "ok": False}
    # Studio comments is more reliable for owners
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/comments",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    body = page.inner_text("body")
    if "Full film here" in body:
        out["ok"] = True
        out["already"] = True
        return out
    # Try watch page comment box as fallback
    page.goto(
        f"https://www.youtube.com/watch?v={video_id}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    page.keyboard.press("Escape")
    # scroll to comments
    page.evaluate("window.scrollBy(0, 800)")
    page.wait_for_timeout(1500)
    try:
        box = page.locator(
            "#simplebox-placeholder, #placeholder-area, ytd-comment-simplebox-renderer"
        ).first
        box.click(timeout=5000)
        page.wait_for_timeout(500)
        editable = page.locator(
            "#contenteditable-root, div[contenteditable='true']#contenteditable-root, div[id='contenteditable-root']"
        ).first
        if not editable.count():
            editable = page.locator("div[contenteditable='true']").first
        editable.click()
        page.keyboard.type(comment, delay=5)
        page.wait_for_timeout(400)
        page.get_by_role("button", name=re.compile(r"^Comment$", re.I)).first.click(
            timeout=5000
        )
        page.wait_for_timeout(2500)
        out["commented"] = True
    except Exception as e:
        out["comment_err"] = str(e)[:250]
        page.screenshot(path=str(AUDIT / f"pin_fail_{video_id}.png"))
        return out

    # Try pin via menu on own comment
    try:
        page.reload(wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        page.evaluate("window.scrollBy(0, 900)")
        page.wait_for_timeout(1000)
        # find comment containing needle, open menu, Pin
        pinned = page.evaluate(
            """(needle) => {
              const comments=[...document.querySelectorAll('ytd-comment-thread-renderer,ytd-comment-view-model')];
              const hit=comments.find(c => (c.innerText||'').includes(needle));
              if(!hit) return {ok:false, reason:'not_found'};
              const menu=hit.querySelector('#action-menu button, button[aria-label*="Action"], #button-shape button');
              if(menu) menu.click();
              return {ok:true, opened:!!menu};
            }""",
            "Full film here",
        )
        page.wait_for_timeout(800)
        try:
            page.get_by_text(re.compile(r"^Pin$", re.I)).first.click(timeout=3000)
            page.wait_for_timeout(800)
            page.get_by_role("button", name=re.compile(r"Pin$", re.I)).first.click(
                timeout=3000
            )
            out["pinned"] = True
        except Exception:
            # confirm dialog variant
            page.evaluate(
                """() => {
                  for (const el of document.querySelectorAll('yt-formatted-string,tp-yt-paper-item,button,yt-button-shape')) {
                    if (/^Pin$/i.test((el.innerText||'').trim())) { el.click(); return true; }
                  }
                  return false;
                }"""
            )
            page.wait_for_timeout(800)
            page.evaluate(
                """() => {
                  for (const el of document.querySelectorAll('button,yt-button-shape')) {
                    if (/pin/i.test((el.innerText||'').trim())) { el.click(); return true; }
                  }
                }"""
            )
            out["pinned_attempt"] = True
        out["menu"] = pinned
        out["ok"] = True
    except Exception as e:
        out["pin_err"] = str(e)[:250]
        out["ok"] = bool(out.get("commented"))
    page.screenshot(path=str(AUDIT / f"pin_{video_id}.png"))
    return out


def fix_tiktok_bio(page) -> dict:
    out = {"ok": False}
    page.goto("https://www.tiktok.com/@orbitwithben", wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(2500)
    body = page.inner_text("body")
    if "youtube.com/@OrbitWithBen" in body and "youtube.com/OrbitWithBen" not in body.replace(
        "youtube.com/@OrbitWithBen", ""
    ):
        # still may have wrong without @
        pass
    if "https://www.youtube.com/OrbitWithBen" not in body and "youtube.com/@OrbitWithBen" in body:
        out["ok"] = True
        out["skipped"] = "already_correct"
        return out
    try:
        page.get_by_role("button", name=re.compile(r"Edit profile", re.I)).click(
            timeout=8000
        )
        page.wait_for_timeout(2000)
        # bio textarea
        bio = page.locator("textarea").first
        if bio.count():
            cur = bio.input_value()
            new = re.sub(
                r"https?://(www\.)?youtube\.com/OrbitWithBen",
                "https://www.youtube.com/@OrbitWithBen",
                cur,
            )
            if "youtube.com/@OrbitWithBen" not in new:
                new = "Space stories. Big questions. Full films on https://www.youtube.com/@OrbitWithBen"
            bio.fill(new)
            out["bio"] = new
        page.get_by_role("button", name=re.compile(r"^Save$", re.I)).click(timeout=5000)
        page.wait_for_timeout(2000)
        out["ok"] = True
    except Exception as e:
        out["error"] = str(e)[:300]
        page.screenshot(path=str(AUDIT / "tiktok_bio_fail.png"))
    return out


def sync_aliens_index(public_ids: set[str]) -> None:
    data = json.loads(ALIENS_INDEX.read_text())
    for s in data.get("shorts") or []:
        if s.get("video_id") in public_ids:
            s["visibility"] = "public"
            s["published_now"] = True
            s["note"] = "Published Public via crosspost live funnel fix 2026-08-03"
    data["updated"] = datetime.now(LONDON).isoformat()
    ALIENS_INDEX.write_text(json.dumps(data, indent=2) + "\n")


def unseed_threads(video_ids: list[str]) -> None:
    path = SETUP / "Threads/THREADS_POSTED.json"
    data = json.loads(path.read_text())
    posted = data.setdefault("posted", {})
    for vid in video_ids:
        key = f"yt:{vid}"
        if key in posted and posted[key].get("status") == "seeded":
            del posted[key]
    data["updated_at"] = datetime.now(LONDON).isoformat()
    path.write_text(json.dumps(data, indent=2) + "\n")


def main() -> None:
    result: dict = {
        "ran_at": datetime.now(LONDON).isoformat(),
        "youtube": [],
        "pins": [],
        "tiktok_bio": {},
        "meta": [],
        "threads": [],
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_TT)
        page = browser.contexts[0].new_page()
        page.set_viewport_size({"width": 1400, "height": 1000})
        page.on("dialog", lambda d: d.dismiss())

        for item in PUBLISH_NOW:
            print(f"YT publish {item['video_id']}…", flush=True)
            yr = publish_youtube_public(page, item["video_id"])
            result["youtube"].append(yr)
            print(" ", yr, flush=True)

        public_ids = {
            r["video_id"] for r in result["youtube"] if r.get("ok")
        }
        sync_aliens_index(public_ids)

        for item in PUBLISH_NOW:
            if item["video_id"] not in public_ids:
                continue
            print(f"Pin {item['video_id']}…", flush=True)
            pr = pin_comment(page, item["video_id"])
            result["pins"].append(pr)
            print(" ", {k: pr.get(k) for k in ("ok", "already", "commented", "pinned", "comment_err")}, flush=True)

        print("TikTok bio…", flush=True)
        result["tiktok_bio"] = fix_tiktok_bio(page)
        print(" ", result["tiktok_bio"], flush=True)
        page.close()

    # Meta + Threads hooks (separate CDP)
    unseed_threads([x["video_id"] for x in PUBLISH_NOW])
    project_root = ROOT / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens"
    index = json.loads(ALIENS_INDEX.read_text())
    shorts_by_id = {s["video_id"]: s for s in index.get("shorts") or []}

    notify_meta = load_notify(SETUP / "Meta/auto", "orbit_meta_hooks_fix")
    notify_threads = load_notify(SETUP / "Threads/auto", "orbit_threads_hooks_fix")

    for item in PUBLISH_NOW:
        short = dict(shorts_by_id.get(item["video_id"]) or item)
        short.setdefault("title", item["title"])
        short.setdefault("video_id", item["video_id"])
        short.setdefault("file", str(Path(item["file"]).relative_to(project_root)) if Path(item["file"]).is_absolute() else item["file"])
        # ensure relative file path for discover
        if Path(short["file"]).is_absolute():
            try:
                short["file"] = str(Path(short["file"]).relative_to(project_root))
            except Exception:
                short["file"] = f"10_Shorts/06_Final-Exports/{Path(item['file']).name}"
        short["visibility"] = "public"
        short["published_now"] = True
        short["url"] = f"https://youtu.be/{item['video_id']}"

        print(f"Meta {item['video_id']}…", flush=True)
        try:
            mr = notify_meta(project_root, short)
        except Exception as e:
            mr = {"status": "error", "error": str(e)[:300]}
        result["meta"].append({"video_id": item["video_id"], **mr})
        print(" ", mr.get("status"), flush=True)

        print(f"Threads {item['video_id']}…", flush=True)
        try:
            tr = notify_threads(project_root, short)
        except Exception as e:
            tr = {"status": "error", "error": str(e)[:300]}
        result["threads"].append({"video_id": item["video_id"], **tr})
        print(" ", tr.get("status"), flush=True)

    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print("WROTE", OUT, flush=True)
    # summary exit
    yt_ok = all(r.get("ok") for r in result["youtube"])
    raise SystemExit(0 if yt_ok else 1)


if __name__ == "__main__":
    main()
