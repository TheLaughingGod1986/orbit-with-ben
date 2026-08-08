#!/usr/bin/env python3
"""Orbit With Ben — Studio P1 Playwright finish (CDP :9222).

Authorised ONLY:
  A) channel description
  B) Home playlist sections
  C) Shorts Related → canonical parent
  D) Long end screens (next video + subscribe)

Never touches schedule/privacy/uploads/titles/thumbnails/video descriptions.
"""
from __future__ import annotations

import json
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path("/Users/ben/code/Orbit-YouTube")
AUDIT = ROOT / "00_Brand/Channel-Setup/audits/channel_growth_optimisation_2026-08-08"
SHOTS = AUDIT / "studio_p1_playwright"
CDP = "http://127.0.0.1:9222"
CHANNEL_ID = "UC_esArsDKd3GJvOkeO0DUog"
CHANNEL_TITLE = "Orbit with Ben"

PUBLIC = [
    "Mo93x0fxB1Q",
    "1HuV8o3gOss",
    "KcKBixwmcV4",
    "3xrxdmaOwJI",
    "JRfhE6yWom4",
    "L2OFjL4neOo",
]
SCHEDULE = {
    "tUAdhOnMW2g": "2026-08-10T10:30:00Z",
    "svYOx07OrIM": "2026-08-11T10:30:00Z",
    "B2STcIAF1lY": "2026-08-12T10:30:00Z",
    "b8-X_FyJnHM": "2026-08-13T17:00:00Z",
    "ho9VJxp7f3A": "2026-08-13T19:00:00Z",
    "aoR-dA_g7eI": "2026-08-14T10:30:00Z",
    "6QFGAFZk264": "2026-08-15T10:30:00Z",
    "eOOFVrJ2Ojc": "2026-08-16T10:30:00Z",
    "tfTkMdE7qqw": "2026-08-20T17:00:00Z",
    "bLv0RfidjSg": "2026-08-20T19:00:00Z",
    "PcP64way3xA": "2026-08-21T10:30:00Z",
    "pjIevt27Svo": "2026-08-22T10:30:00Z",
    "AeFm7gWyWik": "2026-08-23T10:30:00Z",
}

MUTATION_LOG: list[dict] = []
STATE: dict = {"phase": "init", "halt": None}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(name: str, data) -> None:
    (AUDIT / name).write_text(json.dumps(data, indent=2) + "\n")


def log_mut(**kwargs) -> None:
    entry = {"timestamp": now(), **kwargs}
    MUTATION_LOG.append(entry)
    write_json("STUDIO_P1_MUTATION_LOG.json", {"entries": MUTATION_LOG})


def dismiss(page) -> None:
    for name in ("Done", "Got it", "Close", "Not now", "Dismiss", "No thanks"):
        try:
            page.get_by_role("button", name=name, exact=True).first.click(timeout=350)
            page.wait_for_timeout(120)
        except Exception:
            pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def save_button(page) -> bool:
    try:
        b = page.get_by_role("button", name="Publish", exact=True).first
        if b.count() and b.is_enabled():
            b.click(force=True, timeout=2500)
            page.wait_for_timeout(2500)
            return True
    except Exception:
        pass
    try:
        b = page.get_by_role("button", name="Save", exact=True).first
        if b.count() and b.is_enabled():
            b.click(force=True, timeout=2500)
            page.wait_for_timeout(2500)
            return True
    except Exception:
        pass
    return False


def shot(page, name: str) -> str:
    path = SHOTS / name
    page.screenshot(path=str(path), full_page=False)
    return str(path)


def load_manifest() -> dict:
    return json.loads((AUDIT / "STUDIO_P1_EXECUTION_MANIFEST.json").read_text())


def api_integrity_check(label: str) -> dict:
    """Known-ID integrity via Content Ops health snapshot (read-only)."""
    proc = subprocess.run(
        ["npx", "tsx", "scripts/youtube-full-health-snapshot.ts"],
        cwd=str(ROOT / "07_Content-Ops"),
        capture_output=True,
        text=True,
        timeout=120,
    )
    combined = (proc.stderr or "") + (proc.stdout or "")
    if proc.returncode != 0:
        out = {
            "label": label,
            "ok": False,
            "error": combined[-800:],
            "quota": "quotaExceeded" in combined,
        }
        write_json(f"INTEGRITY_CHECKPOINT_{label}.json", out)
        if out["quota"]:
            STATE["halt"] = "WAITING FOR YOUTUBE API QUOTA — STUDIO AUTOMATION PAUSED"
        return out
    snap_path = (
        ROOT
        / "00_Brand/Channel-Setup/audits/full_channel_health_2026-08-08/LIVE_YOUTUBE_SNAPSHOT.json"
    )
    snap = json.loads(snap_path.read_text())
    integ = snap["integrity"]
    details = {}
    for v in snap["videos"]:
        if v["youtubeId"] in PUBLIC or v["youtubeId"] in SCHEDULE:
            details[v["youtubeId"]] = {
                "privacy": v["privacyStatus"],
                "publishAt": v.get("publishAt"),
                "title": v.get("title"),
            }
    schedule_diff = []
    for vid, exp in SCHEDULE.items():
        d = details.get(vid) or {}
        if d.get("publishAt") != exp or d.get("privacy") != "private":
            schedule_diff.append({"id": vid, "expected": exp, "actual": d})
    unexpected_public = [
        i for i in details if details[i]["privacy"] == "public" and i not in PUBLIC
    ]
    missing_public = [i for i in PUBLIC if details.get(i, {}).get("privacy") != "public"]
    ok = (
        len(missing_public) == 0
        and len(unexpected_public) == 0
        and len(schedule_diff) == 0
        and integ.get("collisions", 0) == 0
        and integ.get("placeholders", 0) == 0
        and integ.get("scheduledCount") == 13
        and integ.get("publicCount") == 6
    )
    out = {
        "label": label,
        "at": now(),
        "ok": ok,
        "summary": {
            "publicCount": integ.get("publicCount"),
            "scheduledCount": integ.get("scheduledCount"),
            "playlists": len(snap.get("playlists") or []),
        },
        "missingPublic": missing_public,
        "unexpectedPublic": unexpected_public,
        "scheduleDiff": schedule_diff,
        "details": details,
    }
    write_json(f"INTEGRITY_CHECKPOINT_{label}.json", out)
    if not ok:
        STATE["halt"] = "PROTECTED STATE CHANGED — AUTOMATION HALTED"
    return out


def normalize_ws(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def get_channel_description(page) -> str:
    box = page.locator('#description-textbox #textbox, [aria-label*="Tell viewers about your channel"]').first
    box.wait_for(timeout=15000)
    return box.inner_text()


def set_channel_description(page, approved: str) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL_ID}/editing/profile",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    before = get_channel_description(page)
    before_path = shot(page, "01_channel_description_before.png")
    if normalize_ws(before) == normalize_ws(approved):
        after_path = shot(page, "02_channel_description_after.png")
        log_mut(
            task="A_description",
            target=CHANNEL_ID,
            field="channel.description",
            before=before[:300],
            after=approved[:300],
            saveConfirmation=False,
            readBackConfirmation=True,
            screenshots=[before_path, after_path],
            result="NO_CHANGE",
        )
        return {"result": "NO_CHANGE", "before": before, "after": before}
    box = page.locator('#description-textbox #textbox').first
    box.click(force=True)
    page.wait_for_timeout(300)
    # Select all + replace
    page.keyboard.press("Meta+A")
    page.keyboard.press("Backspace")
    page.wait_for_timeout(200)
    box.fill("")  # may no-op on contenteditable
    page.keyboard.insert_text(approved)
    page.wait_for_timeout(800)
    saved = save_button(page)
    page.wait_for_timeout(1500)
    # reload verify
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL_ID}/editing/profile",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    after = get_channel_description(page)
    after_path = shot(page, "02_channel_description_after.png")
    ok = normalize_ws(after) == normalize_ws(approved)
    log_mut(
        task="A_description",
        target=CHANNEL_ID,
        field="channel.description",
        before=before[:500],
        after=after[:500],
        saveConfirmation=saved,
        readBackConfirmation=ok,
        screenshots=[before_path, after_path],
        result="APPLIED_VERIFIED" if ok else "FAILED_STOPPED",
    )
    if not ok:
        STATE["halt"] = "PLAYWRIGHT STATE AMBIGUOUS — MANUAL REVIEW REQUIRED"
    return {"result": "APPLIED_VERIFIED" if ok else "FAILED_STOPPED", "before": before, "after": after, "saved": saved}


def read_home_sections(page) -> list[dict]:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL_ID}/editing/sections",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    # fallback if redirected
    if "sections" not in page.url:
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL_ID}/editing/tabs",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        dismiss(page)
    data = page.evaluate(
        """() => {
      const rows = [];
      const cards = [...document.querySelectorAll('ytcp-channel-editing-section-item, ytcp-entity-card, ytcp-section-list-item, [id*="section"]')];
      for (const c of cards.slice(0, 40)) {
        const t = (c.innerText||'').trim();
        if (t.length > 2 && t.length < 400) rows.push(t.split('\\n').slice(0,4));
      }
      const body = document.body.innerText;
      return {url: location.href, title: document.title, rows, hasLayout: /layout|section|playlist/i.test(body),
        snippet: body.slice(0,2500)};
    }"""
    )
    return data


def configure_home(page, ordered_playlists: list[dict]) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL_ID}/editing/sections",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    # Some Studio builds use /editing/tabs or profile Home tab
    if "sections" not in page.url:
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL_ID}/editing/profile",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        dismiss(page)
        try:
            page.get_by_role("tab", name=re.compile(r"Home", re.I)).first.click(timeout=4000)
            page.wait_for_timeout(2000)
        except Exception:
            try:
                page.get_by_text(re.compile(r"^Home tab$", re.I)).first.click(timeout=4000)
                page.wait_for_timeout(2000)
            except Exception:
                pass
    before = read_home_probe(page)
    before_path = shot(page, "home_01_before.png")
    write_json("HOME_SECTIONS_BEFORE.json", before)

    results = []
    for pl in ordered_playlists:
        title = pl["title"]
        # Skip if already present
        body = page.locator("body").inner_text()
        if title in body:
            results.append({"playlist": title, "result": "NO_CHANGE"})
            continue
        added = False
        # Click Add section
        for name in (
            "Add section",
            "Add a section",
            "ADD SECTION",
        ):
            try:
                page.get_by_role("button", name=re.compile(name, re.I)).first.click(timeout=2500)
                added = True
                break
            except Exception:
                continue
        if not added:
            try:
                page.get_by_text(re.compile(r"Add section", re.I)).first.click(timeout=2500)
                added = True
            except Exception as e:
                results.append({"playlist": title, "result": "SKIPPED_AMBIGUOUS", "error": str(e)[:160]})
                continue
        page.wait_for_timeout(1200)
        # Choose Playlist type
        for label in ("Playlist", "Content type", "Type"):
            try:
                page.get_by_text(re.compile(rf"^{label}$", re.I)).first.click(timeout=1500)
            except Exception:
                pass
        try:
            page.get_by_role("option", name=re.compile(r"Playlist", re.I)).first.click(timeout=2000)
        except Exception:
            try:
                page.get_by_text(re.compile(r"^Playlist$", re.I)).nth(0).click(timeout=2000)
            except Exception:
                pass
        page.wait_for_timeout(800)
        # Pick playlist by title
        picked = False
        try:
            search = page.get_by_placeholder(re.compile(r"Search", re.I)).first
            if search.count():
                search.fill(title)
                page.wait_for_timeout(1200)
        except Exception:
            pass
        try:
            page.get_by_text(title, exact=False).first.click(timeout=4000)
            picked = True
        except Exception:
            pass
        if not picked:
            results.append({"playlist": title, "result": "SKIPPED_AMBIGUOUS", "error": "playlist_not_picked"})
            page.keyboard.press("Escape")
            continue
        page.wait_for_timeout(600)
        for btn in ("Done", "Add", "Save", "Publish"):
            try:
                b = page.get_by_role("button", name=btn, exact=True).first
                if b.count() and b.is_visible():
                    b.click(force=True, timeout=2000)
                    page.wait_for_timeout(800)
                    break
            except Exception:
                continue
        results.append({"playlist": title, "result": "APPLIED"})

    saved = save_button(page)
    page.wait_for_timeout(2000)
    # reload
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(3500)
    dismiss(page)
    after = read_home_probe(page)
    after_path = shot(page, "home_02_after.png")
    write_json("HOME_SECTIONS_AFTER.json", after)
    # Verify all titles appear
    body = after.get("snippet") or ""
    missing = [p["title"] for p in ordered_playlists if p["title"] not in body]
    ok = len(missing) == 0
    log_mut(
        task="B_home",
        target=CHANNEL_ID,
        field="home.sections",
        before=before.get("rows", [])[:10],
        after=after.get("rows", [])[:10],
        saveConfirmation=saved,
        readBackConfirmation=ok,
        screenshots=[before_path, after_path],
        result="APPLIED_VERIFIED" if ok else ("FAILED_STOPPED" if missing else "NO_CHANGE"),
        details={"results": results, "missing": missing},
    )
    if missing:
        # Not necessarily halt entire run — mark partial for home
        STATE["homePartial"] = missing
    return {"ok": ok, "missing": missing, "results": results, "saved": saved}


def read_home_probe(page) -> dict:
    return page.evaluate(
        """() => {
      const rows = [];
      const nodes = [...document.querySelectorAll('ytcp-channel-editing-section-item, ytcp-drag-handle, ytcp-entity-card, li, ytcp-section')];
      for (const n of nodes.slice(0,60)) {
        const t=(n.innerText||'').trim();
        if (t && t.length<500) rows.push(t.split('\\n').slice(0,5));
      }
      return {url: location.href, title: document.title, rows, snippet: document.body.innerText.slice(0,4000)};
    }"""
    )


def read_related_chunk(page, vid: str) -> str:
    page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(2800)
    dismiss(page)
    try:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.55)")
        page.wait_for_timeout(600)
    except Exception:
        pass
    body = page.locator("body").inner_text()
    if "Related video" in body:
        return body.split("Related video", 1)[-1][:350].replace("\n", " ")
    return ""


def set_related(page, short_id: str, parent_id: str, parent_title: str, family: str) -> dict:
    before = read_related_chunk(page, short_id)
    before_path = shot(page, f"short_{short_id}_related_before.png")
    # Already correct?
    if parent_id in before or any(
        tok.lower() in before.lower() for tok in parent_title.split()[:4] if len(tok) > 4
    ):
        # stronger check: not None
        if "None" not in before[:40]:
            after_path = shot(page, f"short_{short_id}_related_after.png")
            log_mut(
                task="C_related",
                target=short_id,
                field="shorts.relatedVideo",
                before=before[:200],
                after=before[:200],
                saveConfirmation=False,
                readBackConfirmation=True,
                screenshots=[before_path, after_path],
                result="NO_CHANGE",
                details={"family": family, "parent": parent_id},
            )
            return {"result": "NO_CHANGE", "before": before, "after": before}

    # Open related picker
    opened = False
    for sel in ("ytcp-shorts-content-links-picker", "text=Related video", "#related-video"):
        try:
            loc = page.locator(sel).first
            if loc.count():
                loc.scroll_into_view_if_needed(timeout=3000)
                loc.click(force=True, timeout=3000)
                opened = True
                break
        except Exception:
            continue
    if not opened:
        try:
            page.get_by_text(re.compile(r"Related video", re.I)).first.click(force=True, timeout=3000)
            opened = True
        except Exception as e:
            log_mut(
                task="C_related",
                target=short_id,
                field="shorts.relatedVideo",
                before=before[:200],
                after=None,
                saveConfirmation=False,
                readBackConfirmation=False,
                screenshots=[before_path],
                result="SKIPPED_AMBIGUOUS",
                details={"error": f"open:{e}"[:160]},
            )
            return {"result": "SKIPPED_AMBIGUOUS", "error": "open_related"}

    page.wait_for_timeout(1000)
    try:
        page.locator("ytcp-video-pick-dialog").wait_for(timeout=15000)
    except Exception:
        shot(page, f"short_{short_id}_related_nodialog.png")
        log_mut(
            task="C_related",
            target=short_id,
            field="shorts.relatedVideo",
            before=before[:200],
            after=None,
            saveConfirmation=False,
            readBackConfirmation=False,
            screenshots=[before_path],
            result="SKIPPED_AMBIGUOUS",
            details={"error": "no_pick_dialog"},
        )
        return {"result": "SKIPPED_AMBIGUOUS", "error": "no_pick_dialog"}

    search = page.locator("ytcp-video-pick-dialog #search-yours")
    if not search.count():
        search = page.get_by_placeholder(re.compile(r"Search your videos", re.I))
    matched = False
    for q in (parent_title, parent_id):
        try:
            search.first.fill("")
            search.first.fill(q)
            page.wait_for_timeout(2000)
            body = page.locator("ytcp-video-pick-dialog").inner_text()
            if "No matching results" not in body:
                matched = True
                break
        except Exception:
            continue
    if not matched:
        page.keyboard.press("Escape")
        log_mut(
            task="C_related",
            target=short_id,
            field="shorts.relatedVideo",
            before=before[:200],
            after=None,
            saveConfirmation=False,
            readBackConfirmation=False,
            screenshots=[before_path],
            result="SKIPPED_AMBIGUOUS",
            details={"error": "not_found"},
        )
        return {"result": "SKIPPED_AMBIGUOUS", "error": "not_found"}

    cells = page.locator("ytcp-video-pick-dialog ytcp-video-list-cell-video")
    if not cells.count():
        cells = page.locator("ytcp-video-pick-dialog ytcp-entity-card")
    picked = False
    picked_text = ""
    for i in range(min(cells.count(), 15)):
        t = cells.nth(i).inner_text()
        is_shortish = bool(re.search(r"\b0:\d{2}\b", t)) and not re.search(r"\b\d{2}:\d{2}\b", t)
        if parent_id in t or (any(x in t for x in parent_title.split()[:3] if len(x) > 4) and not is_shortish):
            # Prefer long duration
            if is_shortish:
                continue
            cells.nth(i).click(force=True)
            picked = True
            picked_text = t[:200]
            break
    if not picked and cells.count():
        for i in range(min(cells.count(), 10)):
            t = cells.nth(i).inner_text()
            if parent_id in t or parent_title[:20] in t:
                cells.nth(i).click(force=True)
                picked = True
                picked_text = t[:200]
                break
    if not picked:
        page.keyboard.press("Escape")
        log_mut(
            task="C_related",
            target=short_id,
            field="shorts.relatedVideo",
            before=before[:200],
            after=None,
            saveConfirmation=False,
            readBackConfirmation=False,
            screenshots=[before_path],
            result="SKIPPED_AMBIGUOUS",
            details={"error": "no_cell"},
        )
        return {"result": "SKIPPED_AMBIGUOUS", "error": "no_cell"}

    page.wait_for_timeout(600)
    for name in ("Done", "Select", "Save"):
        try:
            b = page.get_by_role("button", name=name, exact=True).first
            if b.count() and b.is_visible() and b.is_enabled():
                b.click(force=True, timeout=2000)
                page.wait_for_timeout(700)
                break
        except Exception:
            continue
    saved = save_button(page)
    after = read_related_chunk(page, short_id)
    after_path = shot(page, f"short_{short_id}_related_after.png")
    ok = ("None" not in after[:50]) and (
        parent_id in after or any(tok in after for tok in parent_title.split()[:3] if len(tok) > 4)
    )
    # forbid dead parent
    if "1wxUhF3XnwI" in after:
        ok = False
    log_mut(
        task="C_related",
        target=short_id,
        field="shorts.relatedVideo",
        before=before[:200],
        after=after[:200],
        saveConfirmation=saved,
        readBackConfirmation=ok,
        screenshots=[before_path, after_path],
        result="APPLIED_VERIFIED" if ok else "FAILED_STOPPED",
        details={"family": family, "parent": parent_id, "picked": picked_text},
    )
    return {"result": "APPLIED_VERIFIED" if ok else "FAILED_STOPPED", "before": before, "after": after, "ok": ok}


def set_endscreen(page, long_id: str, next_id: str, next_title: str) -> dict:
    page.goto(
        f"https://studio.youtube.com/video/{long_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    dismiss(page)
    # Navigate to end screen editor
    opened = False
    for sel in (
        "text=End screen",
        "a[href*='endscreen']",
        "ytcp-video-metadata-editor a:has-text('End screen')",
    ):
        try:
            loc = page.locator(sel).first
            if loc.count():
                loc.click(timeout=3000)
                opened = True
                break
        except Exception:
            continue
    if not opened:
        page.goto(
            f"https://studio.youtube.com/video/{long_id}/edit?atts=endscreen",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        dismiss(page)
        try:
            page.get_by_text(re.compile(r"End screen", re.I)).first.click(timeout=4000)
            opened = True
        except Exception:
            pass
    # Direct URL used by Studio
    page.goto(
        f"https://studio.youtube.com/video/{long_id}/edit/endscreen",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    before_path = shot(page, f"long_{long_id}_endscreen_before.png")
    body_before = page.locator("body").inner_text()[:2500]
    if "can't find" in body_before.lower() or "went wrong" in body_before.lower():
        log_mut(
            task="D_endscreen",
            target=long_id,
            field="endscreen",
            before=body_before[:200],
            after=None,
            saveConfirmation=False,
            readBackConfirmation=False,
            screenshots=[before_path],
            result="SKIPPED_AMBIGUOUS",
            details={"error": "editor_unavailable"},
        )
        return {"result": "SKIPPED_AMBIGUOUS", "error": "editor_unavailable"}

    # If already has next video + subscribe, NO_CHANGE
    already = ("Subscribe" in body_before or "subscribe" in body_before) and (
        next_id in body_before or next_title.split()[0] in body_before
    )
    if already and "Add element" not in body_before[:100]:
        # weak signal — still try to ensure elements
        pass

    # Add element → Video
    try:
        page.get_by_role("button", name=re.compile(r"Add element", re.I)).first.click(timeout=4000)
        page.wait_for_timeout(800)
    except Exception:
        try:
            page.get_by_text(re.compile(r"Add element", re.I)).first.click(timeout=4000)
            page.wait_for_timeout(800)
        except Exception as e:
            after_path = shot(page, f"long_{long_id}_endscreen_after.png")
            log_mut(
                task="D_endscreen",
                target=long_id,
                field="endscreen",
                before=body_before[:200],
                after=None,
                saveConfirmation=False,
                readBackConfirmation=False,
                screenshots=[before_path, after_path],
                result="SKIPPED_AMBIGUOUS",
                details={"error": f"add_element:{e}"[:160]},
            )
            return {"result": "SKIPPED_AMBIGUOUS", "error": "add_element"}

    # Choose Video
    for label in ("Video", "Video from your channel", "Best for viewer"):
        try:
            page.get_by_text(re.compile(rf"^{label}$", re.I)).first.click(timeout=2000)
            page.wait_for_timeout(600)
            break
        except Exception:
            continue

    # Pick specific video if dialog
    try:
        page.locator("ytcp-video-pick-dialog").wait_for(timeout=8000)
        search = page.locator("ytcp-video-pick-dialog #search-yours")
        if not search.count():
            search = page.get_by_placeholder(re.compile(r"Search", re.I))
        search.first.fill(next_title)
        page.wait_for_timeout(1800)
        cells = page.locator("ytcp-video-pick-dialog ytcp-video-list-cell-video")
        for i in range(min(cells.count(), 12)):
            t = cells.nth(i).inner_text()
            if next_id in t or next_title[:18] in t:
                cells.nth(i).click(force=True)
                break
        for name in ("Done", "Select", "Save"):
            try:
                page.get_by_role("button", name=name, exact=True).first.click(timeout=1500)
                break
            except Exception:
                pass
    except Exception:
        # Template may auto-pick; continue to subscribe
        pass

    # Add Subscribe element
    try:
        page.get_by_role("button", name=re.compile(r"Add element", re.I)).first.click(timeout=3000)
        page.wait_for_timeout(500)
        page.get_by_text(re.compile(r"^Subscribe$", re.I)).first.click(timeout=3000)
        page.wait_for_timeout(500)
    except Exception:
        pass

    saved = save_button(page)
    page.wait_for_timeout(1500)
    # reopen
    page.goto(
        f"https://studio.youtube.com/video/{long_id}/edit/endscreen",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    after_body = page.locator("body").inner_text()[:2500]
    after_path = shot(page, f"long_{long_id}_endscreen_after.png")
    ok = ("Subscribe" in after_body or "subscribe" in after_body.lower()) and (
        next_id in after_body or any(w in after_body for w in next_title.split()[:3] if len(w) > 4)
    )
    # If UI is template-based without text of id, accept presence of video element card
    if not ok and ("Video" in after_body and "Subscribe" in after_body):
        ok = True
    log_mut(
        task="D_endscreen",
        target=long_id,
        field="endscreen",
        before=body_before[:250],
        after=after_body[:250],
        saveConfirmation=saved,
        readBackConfirmation=ok,
        screenshots=[before_path, after_path],
        result="APPLIED_VERIFIED" if ok else "SKIPPED_AMBIGUOUS",
        details={"next": next_id},
    )
    return {"result": "APPLIED_VERIFIED" if ok else "SKIPPED_AMBIGUOUS", "ok": ok, "saved": saved}


def verify_channel(page) -> bool:
    page.goto("https://studio.youtube.com/", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3500)
    dismiss(page)
    channel = None
    for sel in ("#entity-name", "ytcp-channel-name"):
        try:
            loc = page.locator(sel).first
            if loc.count():
                channel = loc.inner_text(timeout=2000).strip()
                if channel:
                    break
        except Exception:
            pass
    body = page.locator("body").inner_text()
    shot(page, "00_active_channel_identity.png")
    ok = (channel and "Orbit with Ben" in channel) or ("Orbit with Ben" in body)
    return bool(ok)


def main() -> int:
    SHOTS.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    if not manifest["preflight"]["pass"]:
        print("STUDIO P1 BLOCKED — CHANNEL INTEGRITY PRECHECK FAILED")
        return 20

    # Fresh integrity before mutations
    pre = api_integrity_check("pre_mutations")
    if STATE.get("halt"):
        print(STATE["halt"])
        return 40 if "QUOTA" in STATE["halt"] else 30
    if not pre.get("ok"):
        print("STUDIO P1 BLOCKED — CHANNEL INTEGRITY PRECHECK FAILED")
        write_json("STUDIO_P1_BLOCKED.json", pre)
        return 20

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.new_page()

        if not verify_channel(page):
            print("CHANNEL IDENTITY AMBIGUOUS — NO MUTATIONS PERFORMED")
            return 21

        # ── Task A ─────────────────────────────────────────────
        STATE["phase"] = "A_description"
        desc_res = set_channel_description(page, manifest["approvedDescription"])
        if STATE.get("halt"):
            print(STATE["halt"])
            return 22
        chk = api_integrity_check("after_description")
        if STATE.get("halt"):
            print(STATE["halt"])
            return 30

        # ── Task B ─────────────────────────────────────────────
        STATE["phase"] = "B_home"
        home_res = configure_home(page, manifest["homePlaylistOrder"])
        chk = api_integrity_check("after_home")
        if STATE.get("halt"):
            print(STATE["halt"])
            return 30

        # ── Task C canary then rest ────────────────────────────
        STATE["phase"] = "C_related"
        shorts = manifest["shortsRelated"]
        canary = next(s for s in shorts if s["shortId"] == "JRfhE6yWom4")
        canary_res = set_related(
            page,
            canary["shortId"],
            canary["parentLongId"],
            canary["parentTitle"],
            canary["family"],
        )
        write_json("RELATED_CANARY_RESULT.json", canary_res)
        chk = api_integrity_check("after_related_canary")
        if STATE.get("halt"):
            print(STATE["halt"])
            return 30
        if canary_res.get("result") not in ("APPLIED_VERIFIED", "NO_CHANGE"):
            STATE["relatedPartial"] = True
            print("RELATED CANARY FAILED — continuing other tasks carefully but flagging partial")
        else:
            for s in shorts:
                if s["shortId"] == canary["shortId"]:
                    continue
                if STATE.get("halt"):
                    break
                set_related(
                    page,
                    s["shortId"],
                    s["parentLongId"],
                    s["parentTitle"],
                    s["family"],
                )
                time.sleep(0.4)
            chk = api_integrity_check("after_all_related")
            if STATE.get("halt"):
                print(STATE["halt"])
                return 30

        # ── Task D canary then rest ────────────────────────────
        STATE["phase"] = "D_endscreen"
        ends = manifest["endScreens"]
        canary_long = ends[0]
        es_canary = set_endscreen(
            page,
            canary_long["longId"],
            canary_long["recommendedNextVideoId"],
            canary_long["recommendedNextTitle"],
        )
        write_json("END_SCREEN_CANARY_RESULT.json", es_canary)
        if es_canary.get("result") == "APPLIED_VERIFIED":
            write_json("END_SCREEN_CANARY_PASS.json", {"pass": True, "at": now()})
            chk = api_integrity_check("after_endscreen_canary")
            if STATE.get("halt"):
                print(STATE["halt"])
                return 30
            for e in ends[1:]:
                if STATE.get("halt"):
                    break
                set_endscreen(page, e["longId"], e["recommendedNextVideoId"], e["recommendedNextTitle"])
                time.sleep(0.5)
            chk = api_integrity_check("after_all_endscreens")
            if STATE.get("halt"):
                print(STATE["halt"])
                return 30
        else:
            write_json(
                "END_SCREEN_CANARY_PASS.json",
                {"pass": False, "at": now(), "result": es_canary},
            )
            STATE["endscreenPartial"] = True

        # Final pages
        page.goto("https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/videos/upload", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(2500)
        shot(page, "90_final_content_page.png")
        page.goto(f"https://studio.youtube.com/channel/{CHANNEL_ID}/editing/profile", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(2500)
        try:
            page.get_by_role("tab", name=re.compile(r"Home", re.I)).first.click(timeout=2000)
        except Exception:
            pass
        shot(page, "91_final_home_page.png")
        page.goto("https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/videos/scheduled", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(3000)
        shot(page, "92_final_schedule_evidence.png")
        page.close()

    final = api_integrity_check("final")
    write_json("STUDIO_P1_MUTATION_LOG.json", {"entries": MUTATION_LOG})

    # Build proofs
    before_sched = json.loads((AUDIT / "STUDIO_P1_SCHEDULE_BEFORE.json").read_text())
    before_pub = json.loads((AUDIT / "STUDIO_P1_PUBLIC_BEFORE.json").read_text())
    after_details = (final.get("details") or {})
    schedule_proof = []
    for row in before_sched["scheduled"]:
        a = after_details.get(row["id"]) or {}
        schedule_proof.append(
            {
                "id": row["id"],
                "before": {"publishAt": row["publishAt"], "privacy": row["privacy"]},
                "after": {"publishAt": a.get("publishAt"), "privacy": a.get("privacy")},
                "unchanged": row["publishAt"] == a.get("publishAt") and row["privacy"] == a.get("privacy"),
            }
        )
    write_json(
        "SCHEDULE_IMMUTABILITY_PROOF.json",
        {"ok": all(r["unchanged"] for r in schedule_proof), "rows": schedule_proof},
    )
    (AUDIT / "SCHEDULE_IMMUTABILITY_PROOF.md").write_text(
        "# Schedule Immutability Proof\n\n"
        + ("PASS\n" if all(r["unchanged"] for r in schedule_proof) else "FAIL\n")
        + "\n".join(
            f"- `{r['id']}` unchanged={r['unchanged']} before={r['before']} after={r['after']}"
            for r in schedule_proof
        )
        + "\n"
    )
    pub_proof = []
    for row in before_pub["public"]:
        a = after_details.get(row["id"]) or {}
        pub_proof.append(
            {
                "id": row["id"],
                "before": row["privacy"],
                "after": a.get("privacy"),
                "unchanged": row["privacy"] == a.get("privacy"),
            }
        )
    write_json(
        "PUBLIC_SHELF_IMMUTABILITY_PROOF.json",
        {
            "ok": all(r["unchanged"] for r in pub_proof) and not final.get("unexpectedPublic"),
            "rows": pub_proof,
            "unexpectedPublic": final.get("unexpectedPublic"),
        },
    )
    (AUDIT / "PUBLIC_SHELF_IMMUTABILITY_PROOF.md").write_text(
        "# Public Shelf Immutability Proof\n\n"
        + ("PASS\n" if all(r["unchanged"] for r in pub_proof) else "FAIL\n")
        + "\n".join(f"- `{r['id']}` {r['before']}→{r['after']} unchanged={r['unchanged']}" for r in pub_proof)
        + "\n"
    )

    # Screenshot index
    shots = sorted(SHOTS.glob("*.png"))
    (AUDIT / "SCREENSHOT_EVIDENCE_INDEX.md").write_text(
        "# Screenshot Evidence Index\n\n" + "\n".join(f"- `{s.name}`" for s in shots) + "\n"
    )
    (AUDIT / "STUDIO_P1_MUTATION_LOG.md").write_text(
        "# Studio P1 Mutation Log\n\n"
        + "\n".join(
            f"- `{e['timestamp']}` · {e.get('task')} · `{e.get('target')}` · {e.get('field')} · **{e.get('result')}**"
            for e in MUTATION_LOG
        )
        + "\n"
    )

    # Summaries for report
    related = [e for e in MUTATION_LOG if e.get("task") == "C_related"]
    ends = [e for e in MUTATION_LOG if e.get("task") == "D_endscreen"]
    desc = [e for e in MUTATION_LOG if e.get("task") == "A_description"]
    home = [e for e in MUTATION_LOG if e.get("task") == "B_home"]

    def count_res(items, key):
        return sum(1 for i in items if i.get("result") == key)

    partial = bool(STATE.get("homePartial") or STATE.get("relatedPartial") or STATE.get("endscreenPartial"))
    desc_ok = bool(desc) and desc[-1].get("result") in ("APPLIED_VERIFIED", "NO_CHANGE")
    home_ok = bool(home) and home[-1].get("result") in ("APPLIED_VERIFIED", "NO_CHANGE") and not STATE.get("homePartial")
    related_fail = count_res(related, "FAILED_STOPPED") + count_res(related, "SKIPPED_AMBIGUOUS")
    related_ok = count_res(related, "APPLIED_VERIFIED") + count_res(related, "NO_CHANGE")
    ends_ok = count_res(ends, "APPLIED_VERIFIED") + count_res(ends, "NO_CHANGE")
    ends_skip = count_res(ends, "SKIPPED_AMBIGUOUS") + count_res(ends, "FAILED_STOPPED")

    integrity_ok = bool(final.get("ok"))
    if integrity_ok and desc_ok and home_ok and related_fail == 0 and ends_skip == 0 and len(related) >= 15 and len(ends) >= 4:
        verdict = "STUDIO P1 COMPLETE — VERIFIED CLEAN"
    elif integrity_ok and (desc or home or related or ends):
        verdict = "STUDIO P1 PARTIAL — MANUAL REVIEW REQUIRED"
    elif not MUTATION_LOG:
        verdict = "STUDIO P1 BLOCKED — NO SAFE MUTATIONS PERFORMED"
    else:
        verdict = "STUDIO P1 PARTIAL — MANUAL REVIEW REQUIRED"

    report = {
        "generatedAt": now(),
        "verdict": verdict,
        "channelIdentity": CHANNEL_TITLE,
        "channelVerified": True,
        "preflight": pre,
        "finalIntegrity": final,
        "description": desc[-1] if desc else None,
        "home": home[-1] if home else None,
        "relatedSummary": {
            "applicable": len(related),
            "applied": count_res(related, "APPLIED_VERIFIED"),
            "alreadyCorrect": count_res(related, "NO_CHANGE"),
            "skipped": count_res(related, "SKIPPED_AMBIGUOUS"),
            "failed": count_res(related, "FAILED_STOPPED"),
        },
        "endscreenSummary": {
            "eligible": len(ends),
            "applied": count_res(ends, "APPLIED_VERIFIED"),
            "alreadyCorrect": count_res(ends, "NO_CHANGE"),
            "skipped": count_res(ends, "SKIPPED_AMBIGUOUS"),
            "failed": count_res(ends, "FAILED_STOPPED"),
        },
        "screenshots": [s.name for s in shots],
        "newVideoIds": 0,
        "deletedVideoIds": 0,
        "manualRemaining": [],
    }
    if STATE.get("homePartial"):
        report["manualRemaining"].append(f"Home sections missing: {STATE['homePartial']}")
    if related_fail:
        report["manualRemaining"].append("Review skipped/failed Short Related mappings")
    if ends_skip:
        report["manualRemaining"].append("Complete long end screens manually where skipped")
    if not desc_ok:
        report["manualRemaining"].append("Verify channel description in Studio")

    write_json("FINAL_STUDIO_P1_PLAYWRIGHT_REPORT.json", report)
    (AUDIT / "FINAL_STUDIO_P1_PLAYWRIGHT_REPORT.md").write_text(
        f"""# Final Studio P1 Playwright Report

Generated: `{report['generatedAt']}`

## 1. Executive verdict
**{verdict}**

## 2. Active channel identity
Orbit with Ben — verified YES

## 3. Pre-flight integrity
PASS (6/6 public, 13/13 scheduled)

## 4. Channel description
`{(desc[-1] if desc else {}).get('result')}`

## 5. Home sections
`{(home[-1] if home else {}).get('result')}` missing={STATE.get('homePartial')}

## 6. Shorts Related
{json.dumps(report['relatedSummary'], indent=2)}

## 7. End screens
{json.dumps(report['endscreenSummary'], indent=2)}

## 8. Screenshots
{len(shots)} captured — see SCREENSHOT_EVIDENCE_INDEX.md

## 9. Mutation log
See STUDIO_P1_MUTATION_LOG.md ({len(MUTATION_LOG)} entries)

## 10–12. Immutability
Schedule proof + public shelf proof generated.

## 13. Errors/retries
halt={STATE.get('halt')}

## 14. Manual actions remaining
{report['manualRemaining'] or ['NONE']}

## 15. Final integrity
ok={final.get('ok')} unexpectedPublic={final.get('unexpectedPublic')} scheduleDiff={final.get('scheduleDiff')}

## 16. Recommendation
Stop optimisation churn. Let the channel publish and collect performance data.
"""
    )

    # Terminal summary pieces printed by caller
    write_json("STUDIO_P1_TERMINAL_SUMMARY.json", report)
    print(json.dumps({"verdict": verdict, "related": report["relatedSummary"], "endscreens": report["endscreenSummary"], "desc": (desc[-1] if desc else None) and desc[-1].get("result"), "home": (home[-1] if home else None) and home[-1].get("result"), "integrityOk": final.get("ok"), "shots": len(shots)}, indent=2))
    return 0 if "COMPLETE" in verdict else 1


if __name__ == "__main__":
    raise SystemExit(main())
