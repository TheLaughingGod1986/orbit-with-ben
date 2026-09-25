#!/usr/bin/env python3
"""Sync socials to match live YouTube Shorts.

1) Privatize obsolete YT v01 dupes still public (UWwNKYf_aU8, MO19iXYCu0c)
2) Ensure the 4 current public aliens shorts are on FB Page, IG, Threads, TikTok
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
EXPORTS = ROOT / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/06_Final-Exports"
OUT = ROOT / "00_Brand/Channel-Setup/audits/sync_socials_to_yt_2026-08-03"
OUT.mkdir(parents=True, exist_ok=True)
CDP = "http://127.0.0.1:9222"
LONDON = ZoneInfo("Europe/London")
FULL = "https://youtu.be/Mo93x0fxB1Q"

# Current product shorts (after privatizing old v01s)
SHORTS = [
    {
        "yt": "1HuV8o3gOss",
        "key": "everybody",
        "title": "Where Is Everybody?",
        "file": EXPORTS / "aliens_short-02_fermi-paradox_v02.mp4",
        "caption": f"Where Is Everybody? Full film on YouTube. {FULL} #space #orbitwithben",
        "ig_have": False,
        "fb_have": False,
        "tt_have": True,  # already on TikTok
        "thr_have": False,
    },
    {
        "yt": "dPMJQp2gMNc",
        "key": "distance",
        "title": "Space Is Rude About Distance",
        "file": EXPORTS / "aliens_short-01_distance_v02.mp4",
        "caption": f"Space Is Rude About Distance. Full film on YouTube. {FULL} #space #orbitwithben",
        "ig_have": False,
        "fb_have": False,
        "tt_have": True,
        "thr_have": False,
    },
    {
        "yt": "rFJoOdQAc9c",
        "key": "watching",
        "title": "What If Aliens Are Watching Us?",
        "file": EXPORTS / "aliens_short-03_zoo-hypothesis_v02.mp4",
        "caption": f"What If Aliens Are Watching Us? Full film on YouTube. {FULL} #space #orbitwithben",
        "ig_have": False,
        "fb_have": False,
        "tt_have": True,
        "thr_have": False,
    },
    {
        "yt": "KcKBixwmcV4",
        "key": "clue",
        "title": "What If the First Alien Clue Is Already Here?",
        "file": EXPORTS / "aliens_short-04_hidden-clues_v02.mp4",
        "caption": f"What If the First Alien Clue Is Already Here? Full film on YouTube. {FULL} #space #orbitwithben",
        "ig_have": True,  # Dbk4wQMAkLM
        "fb_have": False,
        "tt_have": False,
        "thr_have": False,
    },
]

OLD_YT = ["UWwNKYf_aU8", "MO19iXYCu0c"]
HELPER = ROOT / (
    "02_Video-Projects/002_What-Happens-If-You-Fall-Into-A-Black-Hole/"
    "11_Upload-Package/Schedule/_force_schedule_shorts_v01.py"
)


def load_helper():
    spec = importlib.util.spec_from_file_location("force_sched", HELPER)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def shot(page, name: str) -> None:
    try:
        page.screenshot(path=str(OUT / name), timeout=12000)
    except Exception:
        pass


def privatize_public(mod, page, video_id: str) -> dict:
    """Force a currently-public Studio video to Private."""
    result = {"id": video_id, "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    time.sleep(4)
    mod.skip(page)
    mod.dismiss(page)
    body = page.locator("body").inner_text()
    if "Sign in" in body and "Email or phone" in body:
        result["error"] = "login_wall"
        return result
    if re.search(r"\bPrivate\b", body) and "Scheduled" not in body and "Public" not in body[:800]:
        # soft already private
        pass
    try:
        mod.open_visibility(page)
    except Exception as e:
        result["open_err"] = str(e)[:160]
        try:
            page.get_by_text(re.compile(r"Visibility|Public|Private|Scheduled", re.I)).first.click(
                force=True, timeout=3000
            )
            time.sleep(1)
        except Exception:
            pass
    shot(page, f"yt_priv_{video_id}_dialog.png")
    hit = page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog') || document;
          const cands=[];
          const walk=(node)=>{
            if(!node) return;
            for (const el of node.querySelectorAll('tp-yt-paper-radio-button,[role=radio],label,div')) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              const al=el.getAttribute('aria-label')||'';
              if (!(t==='Private' || /^Private\\b/i.test(t) || /^Private\\b/i.test(al))) continue;
              const r=el.getBoundingClientRect();
              if (r.width>30 && r.height>10 && r.height<120) {
                cands.push({x:r.x+r.width/2,y:r.y+r.height/2});
              }
            }
            for (const el of node.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          walk(dlg);
          cands.sort((a,b)=>a.y-b.y||a.x-b.x);
          return cands[0]||null;
        }"""
    )
    result["hit"] = hit
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        time.sleep(0.5)
    try:
        page.get_by_role("radio", name=re.compile(r"^Private", re.I)).first.click(force=True, timeout=1500)
    except Exception:
        pass
    mod.click_done(page)
    time.sleep(0.8)
    saved = mod.save_edit(page)
    result["saved"] = saved
    if not saved:
        page.evaluate(
            """() => {
              for (const b of document.querySelectorAll('button, ytcp-button')) {
                const t=(b.innerText||'').trim();
                if (/^Save$/i.test(t) && !b.disabled) { b.click(); return t; }
              }
            }"""
        )
        time.sleep(2.5)
    time.sleep(2)
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    time.sleep(3)
    body2 = page.locator("body").inner_text()
    result["chip_private"] = bool(re.search(r"\bPrivate\b", body2)) and "Public" not in body2.split("\n")[0:30]
    # stronger check via oembed later
    result["body_has_private"] = "Private" in body2
    result["body_has_public"] = bool(re.search(r"\bPublic\b", body2))
    result["ok"] = result["body_has_private"] and not (
        "Visibility" in body2 and re.search(r"Visibility\\s*Public", body2)
    )
    shot(page, f"yt_priv_{video_id}_after.png")
    return result


def post_fb_page(page, path: Path, caption: str, key: str) -> dict:
    PAGE = "https://www.facebook.com/profile.php?id=61592833318203&sk=reels_tab"
    page.goto(PAGE, wait_until="domcontentloaded", timeout=120000)
    time.sleep(3)
    try:
        page.get_by_role("button", name=re.compile("Create reel", re.I)).first.click(timeout=5000)
    except Exception:
        page.get_by_text("Create reel", exact=False).first.click(timeout=5000)
    time.sleep(2.5)
    uploaded = False
    try:
        with page.expect_file_chooser(timeout=12000) as fc:
            ok = page.evaluate(
                """() => {
                  const el=[...document.querySelectorAll('div[role=button],button')]
                    .find(e => /^(Upload|Add Video)$/i.test((e.innerText||'').trim()));
                  if (!el) return false; el.click(); return true;
                }"""
            )
            if not ok:
                page.get_by_text(re.compile(r"^(Upload|Add Video)$", re.I)).first.click(timeout=3000)
        fc.value.set_files(str(path))
        uploaded = True
    except Exception as e:
        return {"key": key, "status": "upload_fail", "error": str(e)[:160]}
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
    # caption
    page.evaluate(
        """(cap) => {
          const dlg=[...document.querySelectorAll('[role=dialog]')].pop()||document;
          const boxes=[...dlg.querySelectorAll('[contenteditable=true],[role=textbox],textarea')];
          let box=boxes.find(el => /describe|caption/i.test((el.getAttribute('aria-label')||'')+(el.getAttribute('aria-placeholder')||'')));
          if (!box) box=boxes.find(el => el.getBoundingClientRect().width>80);
          if (!box) return false;
          box.focus(); box.click();
          if (box.isContentEditable) {
            box.innerHTML='';
            document.execCommand('selectAll');
            document.execCommand('insertText', false, cap);
          } else box.value=cap;
          box.dispatchEvent(new InputEvent('input',{bubbles:true,data:cap,inputType:'insertText'}));
          return true;
        }""",
        caption,
    )
    page.mouse.click(1100, 420)
    time.sleep(1)
    for w in range(30):
        st = page.evaluate(
            """() => [...document.querySelectorAll('div[role=button],button')]
              .filter(e => (e.innerText||'').trim()==='Post')
              .map(e => e.getAttribute('aria-disabled'))"""
        )
        if st and any(x in (None, "false", False) for x in st):
            break
        time.sleep(2)
    clicked = page.evaluate(
        """() => {
          const posts=[...document.querySelectorAll('div[role=button],button')]
            .filter(e => (e.innerText||'').trim()==='Post');
          const el=posts.find(e => e.getAttribute('aria-disabled')!=='true');
          if (!el) return false; el.click(); return true;
        }"""
    )
    time.sleep(10)
    shot(page, f"fb_after_{key}.png")
    still = page.evaluate(
        "() => /Reel settings|Describe your reel/i.test(document.body ? document.body.innerText : '')"
    )
    return {"key": key, "status": "ok" if clicked and not still else "fail", "clicked": clicked, "still": still}


def post_ig(page, path: Path, caption: str, key: str) -> dict:
    """Instagram create reel via web."""
    page.goto("https://www.instagram.com/", wait_until="domcontentloaded", timeout=90000)
    time.sleep(3)
    # Create
    opened = False
    for sel in ('svg[aria-label="New post"]', '[aria-label="New post"]', 'svg[aria-label="Create"]'):
        try:
            page.locator(sel).first.click(timeout=2500)
            opened = True
            break
        except Exception:
            continue
    if not opened:
        try:
            page.get_by_role("link", name=re.compile(r"Create|New post", re.I)).first.click(timeout=3000)
            opened = True
        except Exception:
            pass
    time.sleep(1.5)
    # Choose Post / Reel
    try:
        page.get_by_text(re.compile(r"^Post$", re.I)).first.click(timeout=2000)
    except Exception:
        pass
    time.sleep(0.5)
    try:
        page.get_by_text(re.compile(r"^Reel$", re.I)).first.click(timeout=2500)
    except Exception:
        pass
    time.sleep(1)
    uploaded = False
    try:
        with page.expect_file_chooser(timeout=8000) as fc:
            page.get_by_role("button", name=re.compile(r"Select from computer|Select files", re.I)).first.click(
                timeout=4000
            )
        fc.value.set_files(str(path))
        uploaded = True
    except Exception:
        try:
            loc = page.locator('input[type="file"]')
            if loc.count():
                loc.last.set_input_files(str(path))
                uploaded = True
        except Exception as e:
            shot(page, f"ig_upload_fail_{key}.png")
            return {"key": key, "status": "upload_fail", "error": str(e)[:160]}
    if not uploaded:
        shot(page, f"ig_no_upload_{key}.png")
        return {"key": key, "status": "no_upload"}
    time.sleep(4)
    for label in ("OK", "Next", "Crop"):
        try:
            page.get_by_role("button", name=re.compile(rf"^{label}$", re.I)).first.click(timeout=2500)
            time.sleep(1.2)
        except Exception:
            try:
                page.get_by_text(label, exact=True).first.click(timeout=1500)
                time.sleep(1)
            except Exception:
                pass
    # more Next to caption
    for _ in range(4):
        try:
            page.get_by_role("button", name=re.compile(r"^Next$", re.I)).first.click(timeout=2000)
            time.sleep(1.2)
        except Exception:
            break
    # caption
    try:
        box = page.get_by_role("textbox").first
        box.click(timeout=3000)
        page.keyboard.type(caption, delay=5)
    except Exception:
        page.evaluate(
            """(cap) => {
              const box=document.querySelector('[aria-label*="caption" i], textarea, [contenteditable=true]');
              if(!box) return;
              box.focus();
              if (box.isContentEditable) {
                document.execCommand('selectAll'); document.execCommand('insertText', false, cap);
              } else box.value=cap;
              box.dispatchEvent(new Event('input',{bubbles:true}));
            }""",
            caption,
        )
    time.sleep(1)
    shared = False
    for label in ("Share", "Post"):
        try:
            page.get_by_role("button", name=re.compile(rf"^{label}$", re.I)).first.click(timeout=3000)
            shared = True
            break
        except Exception:
            continue
    time.sleep(8)
    shot(page, f"ig_after_{key}.png")
    return {"key": key, "status": "ok" if shared else "fail", "shared": shared}


def main() -> int:
    results: dict = {"at": datetime.now(LONDON).isoformat(), "privatize": [], "fb": [], "ig": [], "threads": [], "tiktok": []}
    mod = load_helper()

    # import platform uploaders
    sys.path.insert(0, str(ROOT / "00_Brand/Channel-Setup/Threads/auto"))
    sys.path.insert(0, str(ROOT / "00_Brand/Channel-Setup/TikTok/auto"))
    import studio_upload as thr_up  # type: ignore
    # TikTok module name collision — load explicitly
    tt_spec = importlib.util.spec_from_file_location(
        "tt_studio", ROOT / "00_Brand/Channel-Setup/TikTok/auto/studio_upload.py"
    )
    tt_up = importlib.util.module_from_spec(tt_spec)
    assert tt_spec.loader
    tt_spec.loader.exec_module(tt_up)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = next((pg for pg in ctx.pages if not pg.is_closed()), None) or ctx.new_page()
        page.bring_to_front()
        page.set_viewport_size({"width": 1440, "height": 900})

        print("=== Privatize old YT v01s ===", flush=True)
        for vid in OLD_YT:
            try:
                r = privatize_public(mod, page, vid)
            except Exception as e:
                r = {"id": vid, "ok": False, "error": str(e)[:240]}
            results["privatize"].append(r)
            print(r, flush=True)

        print("=== Facebook Page ===", flush=True)
        for s in SHORTS:
            if s["fb_have"]:
                results["fb"].append({"key": s["key"], "status": "skip_have"})
                continue
            print("FB", s["key"], flush=True)
            try:
                r = post_fb_page(page, s["file"], s["caption"], s["key"])
            except Exception as e:
                r = {"key": s["key"], "status": "error", "error": str(e)[:240]}
            results["fb"].append(r)
            print(r, flush=True)
            time.sleep(2)

        print("=== Instagram ===", flush=True)
        for s in SHORTS:
            if s["ig_have"]:
                results["ig"].append({"key": s["key"], "status": "skip_have"})
                continue
            print("IG", s["key"], flush=True)
            try:
                r = post_ig(page, s["file"], s["caption"], s["key"])
            except Exception as e:
                r = {"key": s["key"], "status": "error", "error": str(e)[:240]}
                shot(page, f"ig_err_{s['key']}.png")
            results["ig"].append(r)
            print(r, flush=True)
            time.sleep(2)

        print("=== Threads ===", flush=True)
        for s in SHORTS:
            if s["thr_have"]:
                results["threads"].append({"key": s["key"], "status": "skip_have"})
                continue
            print("THR", s["key"], flush=True)
            try:
                r = thr_up.post_short(
                    video_path=s["file"],
                    caption=s["caption"],
                    confirm_needle=s["title"][:24],
                    audit_dir=OUT / "threads",
                    page=page,
                    port=9222,
                )
                r["key"] = s["key"]
            except Exception as e:
                r = {"key": s["key"], "status": "error", "error": str(e)[:240]}
            results["threads"].append(r)
            print(r, flush=True)
            time.sleep(2)

        print("=== TikTok ===", flush=True)
        for s in SHORTS:
            if s["tt_have"]:
                results["tiktok"].append({"key": s["key"], "status": "skip_have"})
                continue
            print("TT", s["key"], flush=True)
            try:
                r = tt_up.post_short(
                    video_path=s["file"],
                    caption=s["caption"],
                    confirm_needle=s["title"][:24],
                    audit_dir=OUT / "tiktok",
                    page=page,
                )
                r["key"] = s["key"]
            except Exception as e:
                r = {"key": s["key"], "status": "error", "error": str(e)[:240]}
            results["tiktok"].append(r)
            print(r, flush=True)

    (OUT / "SYNC_RESULT.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
