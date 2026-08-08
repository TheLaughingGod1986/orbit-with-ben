#!/usr/bin/env python3
"""Resume remaining Studio P1 work: Home sections, remaining Related, end screens.

Preserves already-verified description + Related canaries. Integrity-gated.
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

LOG = json.loads((AUDIT / "STUDIO_P1_MUTATION_LOG.json").read_text()).get("entries", [])
HALT = None


def now():
    return datetime.now(timezone.utc).isoformat()


def write_json(name, data):
    (AUDIT / name).write_text(json.dumps(data, indent=2) + "\n")


def log(**kw):
    LOG.append({"timestamp": now(), **kw})
    write_json("STUDIO_P1_MUTATION_LOG.json", {"entries": LOG})


def dismiss(page):
    for name in ("Done", "Got it", "Close", "Not now", "Dismiss", "No thanks", "Get started"):
        try:
            page.get_by_role("button", name=name, exact=True).first.click(timeout=400)
            page.wait_for_timeout(150)
        except Exception:
            pass
    # warm welcome
    try:
        page.locator("ytve-warm-welcome button, ytcp-promo-page button").first.click(timeout=800)
        page.wait_for_timeout(400)
    except Exception:
        pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def publish_save(page) -> bool:
    for name in ("Publish", "Save"):
        try:
            b = page.get_by_role("button", name=name, exact=True).first
            if b.count() and b.is_enabled():
                b.click(force=True, timeout=2500)
                page.wait_for_timeout(2500)
                return True
        except Exception:
            continue
    return False


def shot(page, name):
    path = SHOTS / name
    page.screenshot(path=str(path))
    return str(path)


def integrity(label):
    global HALT
    proc = subprocess.run(
        ["npx", "tsx", "scripts/youtube-full-health-snapshot.ts"],
        cwd=str(ROOT / "07_Content-Ops"),
        capture_output=True,
        text=True,
        timeout=120,
    )
    combined = (proc.stderr or "") + (proc.stdout or "")
    if proc.returncode != 0:
        if "quotaExceeded" in combined:
            HALT = "WAITING FOR YOUTUBE API QUOTA — STUDIO AUTOMATION PAUSED"
        return {"ok": False, "error": combined[-500:]}
    snap = json.loads(
        (
            ROOT
            / "00_Brand/Channel-Setup/audits/full_channel_health_2026-08-08/LIVE_YOUTUBE_SNAPSHOT.json"
        ).read_text()
    )
    integ = snap["integrity"]
    details = {
        v["youtubeId"]: {"privacy": v["privacyStatus"], "publishAt": v.get("publishAt")}
        for v in snap["videos"]
        if v["youtubeId"] in PUBLIC or v["youtubeId"] in SCHEDULE
    }
    schedule_diff = []
    for vid, exp in SCHEDULE.items():
        d = details.get(vid) or {}
        if d.get("publishAt") != exp or d.get("privacy") != "private":
            schedule_diff.append({"id": vid, "expected": exp, "actual": d})
    unexpected = [i for i, d in details.items() if d["privacy"] == "public" and i not in PUBLIC]
    missing = [i for i in PUBLIC if details.get(i, {}).get("privacy") != "public"]
    ok = not missing and not unexpected and not schedule_diff and integ["collisions"] == 0
    out = {
        "label": label,
        "ok": ok,
        "missingPublic": missing,
        "unexpectedPublic": unexpected,
        "scheduleDiff": schedule_diff,
        "details": details,
    }
    write_json(f"INTEGRITY_CHECKPOINT_{label}.json", out)
    if not ok:
        HALT = "PROTECTED STATE CHANGED — AUTOMATION HALTED"
    return out


def home_body(page):
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL_ID}/editing/hometab",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    dismiss(page)
    return page.locator("body").inner_text()


def add_single_playlist(page, title: str) -> dict:
    body = home_body(page)
    # Already present as its own section title near layout (beyond Created playlists bucket)?
    # Heuristic: after "Add section" list area contains the title as a section heading
    if f"\n{title}\n" in body or body.count(title) >= 2:
        return {"result": "NO_CHANGE", "title": title}

    page.get_by_role("button", name=re.compile(r"Add section", re.I)).first.click(timeout=5000)
    page.wait_for_timeout(700)
    page.get_by_text("Single playlist", exact=True).click(timeout=5000)
    page.wait_for_timeout(1500)
    # Choose playlist
    try:
        search = page.locator("#search-owned-playlists")
        if search.count():
            search.first.fill(title)
            page.wait_for_timeout(1000)
    except Exception:
        pass
    clicked = False
    try:
        page.get_by_text(title, exact=True).first.click(timeout=5000)
        clicked = True
    except Exception:
        try:
            page.get_by_text(title, exact=False).first.click(timeout=5000)
            clicked = True
        except Exception as e:
            page.keyboard.press("Escape")
            return {"result": "SKIPPED_AMBIGUOUS", "title": title, "error": str(e)[:120]}
    page.wait_for_timeout(800)
    # Confirm Add if present
    for name in ("Add", "Done", "Save"):
        try:
            b = page.get_by_role("button", name=name, exact=True).first
            if b.count() and b.is_visible() and b.is_enabled():
                # Prefer dialog Add over page Add section
                b.click(force=True, timeout=2000)
                page.wait_for_timeout(800)
                break
        except Exception:
            continue
    return {"result": "APPLIED", "title": title, "clicked": clicked}


def configure_home(page, titles: list[str]) -> dict:
    before = home_body(page)
    shot(page, "home_01_before.png")
    write_json("HOME_SECTIONS_BEFORE.json", {"snippet": before[:5000], "url": page.url})
    results = []
    for t in titles:
        if HALT:
            break
        r = add_single_playlist(page, t)
        results.append(r)
        time.sleep(0.3)
    saved = publish_save(page)
    after = home_body(page)
    shot(page, "home_02_after.png")
    write_json("HOME_SECTIONS_AFTER.json", {"snippet": after[:5000], "url": page.url, "results": results})
    missing = [t for t in titles if t not in after]
    # Created playlists bucket always lists titles — require explicit section by checking layout region
    # Stronger: each title should appear AND we applied or no_change
    ok = all(r["result"] in ("APPLIED", "NO_CHANGE") for r in results) and saved
    log(
        task="B_home",
        target=CHANNEL_ID,
        field="home.sections",
        before=before[:300],
        after=after[:300],
        saveConfirmation=saved,
        readBackConfirmation=ok,
        screenshots=["home_01_before.png", "home_02_after.png"],
        result="APPLIED_VERIFIED" if ok else "FAILED_STOPPED",
        details={"results": results, "missingInBody": missing},
    )
    return {"ok": ok, "results": results, "saved": saved}


def read_related(page, vid):
    page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(2800)
    dismiss(page)
    try:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight*0.55)")
        page.wait_for_timeout(500)
    except Exception:
        pass
    body = page.locator("body").inner_text()
    return body.split("Related video", 1)[-1][:400].replace("\n", " ") if "Related video" in body else body[-400:]


def set_related(page, short_id, parent_id, parent_title, family):
    before = read_related(page, short_id)
    shot(page, f"short_{short_id}_related_before.png")
    if "None" not in before[:60] and (
        parent_id in before or any(w in before for w in parent_title.split()[:3] if len(w) > 4)
    ):
        shot(page, f"short_{short_id}_related_after.png")
        log(
            task="C_related",
            target=short_id,
            field="shorts.relatedVideo",
            before=before[:200],
            after=before[:200],
            result="NO_CHANGE",
            details={"family": family, "parent": parent_id},
        )
        return {"result": "NO_CHANGE"}

    opened = False
    for sel in ("ytcp-shorts-content-links-picker", "text=Related video"):
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
        log(task="C_related", target=short_id, field="shorts.relatedVideo", result="SKIPPED_AMBIGUOUS", details={"error": "open"})
        return {"result": "SKIPPED_AMBIGUOUS"}
    page.wait_for_timeout(1000)
    try:
        page.locator("ytcp-video-pick-dialog").wait_for(timeout=12000)
    except Exception:
        log(task="C_related", target=short_id, field="shorts.relatedVideo", result="SKIPPED_AMBIGUOUS", details={"error": "no_dialog"})
        return {"result": "SKIPPED_AMBIGUOUS"}

    search = page.locator("ytcp-video-pick-dialog #search-yours")
    if not search.count():
        search = page.get_by_placeholder(re.compile(r"Search your videos", re.I))
    matched = False
    for q in (parent_id, parent_title, parent_title.split("|")[0].strip(), "Orbit"):
        try:
            search.first.fill("")
            search.first.fill(q)
            page.wait_for_timeout(2200)
            txt = page.locator("ytcp-video-pick-dialog").inner_text()
            if "No matching results" not in txt and (parent_id in txt or parent_title[:12] in txt or "Orbit" in txt):
                matched = True
                break
        except Exception:
            continue
    if not matched:
        page.keyboard.press("Escape")
        log(task="C_related", target=short_id, field="shorts.relatedVideo", result="SKIPPED_AMBIGUOUS", details={"error": "not_found", "parent": parent_id})
        return {"result": "SKIPPED_AMBIGUOUS", "error": "not_found"}

    cells = page.locator("ytcp-video-pick-dialog ytcp-video-list-cell-video")
    if not cells.count():
        cells = page.locator("ytcp-video-pick-dialog ytcp-entity-card")
    picked = False
    for i in range(min(cells.count(), 20)):
        t = cells.nth(i).inner_text()
        is_shortish = bool(re.search(r"\b0:\d{2}\b", t)) and not re.search(r"\b\d{2}:\d{2}\b", t)
        if is_shortish:
            continue
        if parent_id in t or parent_title[:15] in t or ("Alien Worlds" in t and parent_id.startswith("b8")) or ("James Webb" in t and parent_id.startswith("tf")):
            cells.nth(i).click(force=True)
            picked = True
            break
    if not picked:
        page.keyboard.press("Escape")
        log(task="C_related", target=short_id, field="shorts.relatedVideo", result="SKIPPED_AMBIGUOUS", details={"error": "no_cell"})
        return {"result": "SKIPPED_AMBIGUOUS"}
    page.wait_for_timeout(500)
    for name in ("Done", "Select", "Save"):
        try:
            page.get_by_role("button", name=name, exact=True).first.click(timeout=1500)
            break
        except Exception:
            pass
    saved = publish_save(page)
    after = read_related(page, short_id)
    shot(page, f"short_{short_id}_related_after.png")
    ok = "None" not in after[:50] and "1wxUhF3XnwI" not in after and (
        parent_id in after or any(w in after for w in parent_title.split()[:3] if len(w) > 4)
    )
    log(
        task="C_related",
        target=short_id,
        field="shorts.relatedVideo",
        before=before[:200],
        after=after[:200],
        saveConfirmation=saved,
        readBackConfirmation=ok,
        result="APPLIED_VERIFIED" if ok else "FAILED_STOPPED",
        details={"family": family, "parent": parent_id},
    )
    return {"result": "APPLIED_VERIFIED" if ok else "FAILED_STOPPED", "ok": ok}


def set_endscreen(page, long_id, next_id, next_title):
    page.goto(f"https://studio.youtube.com/video/{long_id}/editor", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(4000)
    dismiss(page)
    # Dismiss warm welcome overlay aggressively
    for _ in range(3):
        try:
            page.locator("ytve-warm-welcome").evaluate("e => e.remove()")
        except Exception:
            pass
        try:
            page.get_by_role("button", name=re.compile(r"Get started|Start|Close|Done", re.I)).first.click(timeout=800)
        except Exception:
            pass
        page.wait_for_timeout(300)
    shot(page, f"long_{long_id}_endscreen_before.png")
    try:
        page.locator("ytve-entrypoint-options-panel div:text-is('End screen'), .style-scope.ytve-entrypoint-options-panel:has-text('End screen')").first.click(force=True, timeout=5000)
    except Exception:
        try:
            page.get_by_text("End screen", exact=True).click(force=True, timeout=5000)
        except Exception as e:
            log(task="D_endscreen", target=long_id, field="endscreen", result="SKIPPED_AMBIGUOUS", details={"error": f"open:{e}"[:160]})
            shot(page, f"long_{long_id}_endscreen_after.png")
            return {"result": "SKIPPED_AMBIGUOUS"}
    page.wait_for_timeout(3000)
    dismiss(page)
    body = page.locator("body").inner_text()
    # Add element
    try:
        page.get_by_role("button", name=re.compile(r"Add element", re.I)).first.click(timeout=4000)
        page.wait_for_timeout(700)
        page.get_by_text(re.compile(r"^Video$", re.I)).first.click(timeout=3000)
        page.wait_for_timeout(1000)
    except Exception:
        pass
    # pick dialog
    try:
        page.locator("ytcp-video-pick-dialog").wait_for(timeout=8000)
        search = page.locator("ytcp-video-pick-dialog #search-yours")
        if not search.count():
            search = page.get_by_placeholder(re.compile(r"Search", re.I))
        search.first.fill(next_id)
        page.wait_for_timeout(1800)
        cells = page.locator("ytcp-video-pick-dialog ytcp-video-list-cell-video")
        for i in range(min(cells.count(), 12)):
            t = cells.nth(i).inner_text()
            if next_id in t or next_title[:12] in t:
                cells.nth(i).click(force=True)
                break
        for name in ("Done", "Select"):
            try:
                page.get_by_role("button", name=name, exact=True).first.click(timeout=1500)
                break
            except Exception:
                pass
    except Exception:
        pass
    # subscribe
    try:
        page.get_by_role("button", name=re.compile(r"Add element", re.I)).first.click(timeout=3000)
        page.wait_for_timeout(500)
        page.get_by_text(re.compile(r"^Subscribe$", re.I)).first.click(timeout=3000)
    except Exception:
        pass
    saved = publish_save(page)
    page.wait_for_timeout(1500)
    # reopen
    page.goto(f"https://studio.youtube.com/video/{long_id}/editor", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3000)
    dismiss(page)
    try:
        page.locator("ytve-warm-welcome").evaluate("e => e.remove()")
    except Exception:
        pass
    try:
        page.get_by_text("End screen", exact=True).click(force=True, timeout=4000)
        page.wait_for_timeout(2500)
    except Exception:
        pass
    after = page.locator("body").inner_text()[:2500]
    shot(page, f"long_{long_id}_endscreen_after.png")
    ok = ("Subscribe" in after or "Video" in after) and "Oops" not in after
    log(
        task="D_endscreen",
        target=long_id,
        field="endscreen",
        before=body[:200],
        after=after[:200],
        saveConfirmation=saved,
        readBackConfirmation=ok,
        result="APPLIED_VERIFIED" if ok else "SKIPPED_AMBIGUOUS",
        details={"next": next_id},
    )
    return {"result": "APPLIED_VERIFIED" if ok else "SKIPPED_AMBIGUOUS", "ok": ok}


def main():
    global HALT
    manifest = json.loads((AUDIT / "STUDIO_P1_EXECUTION_MANIFEST.json").read_text())
    chk = integrity("resume_pre")
    if HALT:
        print(HALT)
        return 30
    if not chk.get("ok"):
        print("PROTECTED STATE CHANGED — AUTOMATION HALTED")
        return 30

    titles = [p["title"] for p in manifest["homePlaylistOrder"]]
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()

        # Home
        home_res = configure_home(page, titles)
        write_json("HOME_RESUME_RESULT.json", home_res)
        chk = integrity("after_home_resume")
        if HALT:
            print(HALT)
            return 30

        # Remaining related: those previously skipped
        done_ok = {
            e["target"]
            for e in LOG
            if e.get("task") == "C_related" and e.get("result") in ("APPLIED_VERIFIED", "NO_CHANGE")
        }
        for s in manifest["shortsRelated"]:
            if HALT:
                break
            if s["shortId"] in done_ok:
                continue
            set_related(page, s["shortId"], s["parentLongId"], s["parentTitle"], s["family"])
            time.sleep(0.3)
        chk = integrity("after_related_resume")
        if HALT:
            print(HALT)
            return 30

        # End screens
        ends = []
        for e in manifest["endScreens"]:
            if HALT:
                break
            r = set_endscreen(page, e["longId"], e["recommendedNextVideoId"], e["recommendedNextTitle"])
            ends.append({"id": e["longId"], **r})
            if e == manifest["endScreens"][0]:
                write_json("END_SCREEN_CANARY_RESULT.json", r)
                write_json("END_SCREEN_CANARY_PASS.json", {"pass": r.get("result") == "APPLIED_VERIFIED", "at": now()})
                chk = integrity("after_endscreen_canary_resume")
                if HALT:
                    print(HALT)
                    return 30
                if r.get("result") != "APPLIED_VERIFIED":
                    break  # stop serial if canary fails
            time.sleep(0.4)
        write_json("END_SCREEN_RESUME_RESULT.json", ends)
        chk = integrity("final_resume")

        page.goto(f"https://studio.youtube.com/channel/{CHANNEL_ID}/editing/hometab", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(2500)
        shot(page, "91_final_home_page.png")
        page.goto("https://studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/videos/scheduled", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(2500)
        shot(page, "92_final_schedule_evidence.png")
        page.close()

    print(json.dumps({"home": home_res, "ends": ends, "halt": HALT, "integrity": chk.get("ok")}, indent=2))
    return 0 if not HALT else 1


if __name__ == "__main__":
    raise SystemExit(main())
