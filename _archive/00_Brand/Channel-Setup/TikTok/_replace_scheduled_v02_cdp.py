#!/usr/bin/env python3
"""Delete scheduled TikTok posts and re-upload kinetic-caption v02 shorts.

Uses Chrome CDP :9222 (@orbitwithben). Captions soft-funnel to the full YT film.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

ROOT = Path("/Users/ben/code/Orbit-YouTube")
SETUP = ROOT / "00_Brand/Channel-Setup/TikTok"
LEDGER = SETUP / "TIKTOK_POSTED.json"
AUDIT = SETUP / "audit" / "tt_v02_replace"
RESULT = SETUP / "TIKTOK_V02_REPLACE_RESULT.json"
CONTENT = "https://www.tiktok.com/tiktokstudio/content"
UPLOAD = "https://www.tiktok.com/tiktokstudio/upload?from=upload"
LONDON = ZoneInfo("Europe/London")

ALIENS = ROOT / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/06_Final-Exports"
BH = ROOT / "02_Video-Projects/002_What-Happens-If-You-Fall-Into-A-Black-Hole/10_Shorts/06_Final-Exports"
EXO = ROOT / "02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds/10_Shorts/06_Final-Exports"

# Scheduled / upcoming only — already-live aliens get a fresh upload too so the
# feed shows the new caption style. Funnel line always points to YouTube.
QUEUE = [
    {
        "id": "aliens-fermi",
        "file": ALIENS / "aliens_short-02_fermi-paradox_v02.mp4",
        "needle": "Fermi Paradox",
        "when": "2026-08-02T22:30:00+01:00",  # refresh soon
        "post_now": True,
        "caption": (
            "Where is everybody? The Fermi Paradox in under a minute — countless stars, no clear hello. "
            "Full film on YouTube. #FermiParadox #AreWeAlone #Space #OrbitWithBen"
        ),
        "yt_id": "z-DLqoSoEBo",
    },
    {
        "id": "aliens-distance",
        "file": ALIENS / "aliens_short-01_distance_v02.mp4",
        "needle": "rude about distance",
        "when": "2026-08-03T12:30:00+01:00",
        "post_now": False,
        "caption": (
            "Space is rude about distance — even a quick alien hello could take generations. "
            "Full film on YouTube. #Space #Aliens #FermiParadox #OrbitWithBen"
        ),
        "yt_id": "UWwNKYf_aU8",
    },
    {
        "id": "aliens-zoo",
        "file": ALIENS / "aliens_short-03_zoo-hypothesis_v02.mp4",
        "needle": "zoo hypothesis",
        "when": "2026-08-03T18:00:00+01:00",
        "post_now": False,
        "caption": (
            "What if aliens are watching us? The zoo hypothesis — science, not fearbait. "
            "Full film on YouTube. #Aliens #SpaceMystery #FermiParadox #OrbitWithBen"
        ),
        "yt_id": "MO19iXYCu0c",
    },
    {
        "id": "aliens-clue",
        "file": ALIENS / "aliens_short-04_hidden-clues_v02.mp4",
        "needle": "first alien clue",
        "when": "2026-08-04T12:30:00+01:00",
        "post_now": False,
        "caption": (
            "What if the first alien clue is already here — in an archive we haven't read yet? "
            "Full film on YouTube. #Aliens #Astronomy #AreWeAlone #OrbitWithBen"
        ),
        "yt_id": "--CxhjNqtSY",
    },
    {
        "id": "bh-horizon",
        "file": BH / "blackhole_short-01_event-horizon_v02.mp4",
        "needle": "never come back",
        "when": "2026-08-05T21:00:00+01:00",
        "post_now": False,
        "caption": (
            "Cross this line and you never come back. The event horizon, in under a minute. "
            "Full film on YouTube. #eventhorizon #blackhole #orbitwithben"
        ),
        "yt_id": "eZGAhF8dN7w",
    },
    {
        "id": "bh-spaghetti",
        "file": BH / "blackhole_short-02_spaghettification_v02.mp4",
        "needle": "wouldn't feel like falling",
        "when": "2026-08-06T12:30:00+01:00",
        "post_now": False,
        "caption": (
            "Falling into a black hole wouldn't feel like falling — until it does. "
            "Full film on YouTube. #spaghettification #blackhole #orbitwithben"
        ),
        "yt_id": "C4GuFEFGySI",
    },
    {
        "id": "bh-time",
        "file": BH / "blackhole_short-03_time-dilation_v02.mp4",
        "needle": "Time stops",
        "when": "2026-08-07T12:30:00+01:00",
        "post_now": False,
        "caption": (
            "Time stops at the edge — for them. Black hole time dilation. "
            "Full film on YouTube. #timedilation #blackhole #orbitwithben"
        ),
        "yt_id": "hdlr1soUwNA",
    },
    {
        "id": "bh-lookback",
        "file": BH / "blackhole_short-04_look-back_v02.mp4",
        "needle": "look back",
        "when": "2026-08-08T12:30:00+01:00",
        "post_now": False,
        "caption": (
            "Would you look back as you fall past the event horizon? "
            "Full film on YouTube. #blackhole #eventhorizon #orbitwithben"
        ),
        "yt_id": "80S5E-AWFhA",
    },
    {
        "id": "bh-photon",
        "file": BH / "blackhole_short-05_photon-sphere_v02.mp4",
        "needle": "eyes would see",
        "when": "2026-08-09T12:30:00+01:00",
        "post_now": False,
        "caption": (
            "What your eyes would see near a black hole — light bent into impossible shapes. "
            "Full film on YouTube. #photonsphere #blackhole #orbitwithben"
        ),
        "yt_id": "olnaYqeOtFs",
    },
    {
        "id": "bh-noreturn",
        "file": BH / "blackhole_short-06_point-of-no-return_v02.mp4",
        "needle": "point of no return",
        "when": "2026-08-10T12:30:00+01:00",
        "post_now": False,
        "caption": (
            "The point of no return, explained. Full film on YouTube. "
            "#eventhorizon #blackhole #orbitwithben"
        ),
        "yt_id": "5nMieBeymKU",
    },
    {
        "id": "exo-glass",
        "file": EXO / "exoplanets_short-01_glass-rain_v02.mp4",
        "needle": "glass sideways",
        "when": "2026-08-21T21:00:00+01:00",
        "post_now": False,
        "caption": (
            "It rains glass sideways on this alien world — molten glass in 5,000+ mph winds. "
            "Full film on YouTube. #glassrain #exoplanets #alienworlds #orbitwithben"
        ),
        "yt_id": "aX_7Qg_qzyo",
    },
    {
        "id": "exo-diamond",
        "file": EXO / "exoplanets_short-02_diamond_v02.mp4",
        "needle": "diamond crusts",
        "when": "2026-08-22T12:30:00+01:00",
        "post_now": False,
        "caption": (
            "We found planets that may have diamond crusts thicker than anything on Earth. "
            "Full film on YouTube. #diamondplanet #exoplanets #alienworlds #orbitwithben"
        ),
        "yt_id": "niqnBlzqaFs",
    },
    {
        "id": "exo-suns",
        "file": EXO / "exoplanets_short-03_three-suns_v02.mp4",
        "needle": "Three suns",
        "when": "2026-08-23T12:30:00+01:00",
        "post_now": False,
        "caption": (
            "Three suns in the sky — real exoplanets in multi-star systems. "
            "Full film on YouTube. #threesuns #exoplanets #alienworlds #orbitwithben"
        ),
        "yt_id": "PYhQ0x9HcPM",
    },
    {
        "id": "exo-hot",
        "file": EXO / "exoplanets_short-04_hot-jupiter_v02.mp4",
        "needle": "hottest nights",
        "when": "2026-08-24T12:30:00+01:00",
        "post_now": False,
        "caption": (
            "The hottest nights in the universe — Hot Jupiters that glow on the nightside. "
            "Full film on YouTube. #hotjupiter #exoplanets #alienworlds #orbitwithben"
        ),
        "yt_id": "e8-rKGv37o4",
    },
    {
        "id": "exo-eyeball",
        "file": EXO / "exoplanets_short-05_eyeball_v02.mp4",
        "needle": "Eyeball planets",
        "when": "2026-08-25T12:30:00+01:00",
        "post_now": False,
        "caption": (
            "Eyeball planets: one face fire, one face ice, thin twilight belt between. "
            "Full film on YouTube. #eyeballplanet #exoplanets #alienworlds #orbitwithben"
        ),
        "yt_id": "LQtNmzXJW4w",
    },
    {
        "id": "exo-hab",
        "file": EXO / "exoplanets_short-06_habitability_v02.mp4",
        "needle": "habitable zone",
        "when": "2026-08-26T12:30:00+01:00",
        "post_now": False,
        "caption": (
            "Could any of these alien worlds host life? The habitable zone, explained. "
            "Full film on YouTube. #habitablezone #exoplanets #alienlife #orbitwithben"
        ),
        "yt_id": "i18OD5Ab748",
    },
]


def body(page) -> str:
    try:
        return page.inner_text("body")
    except Exception:
        return ""


def dismiss(page) -> None:
    t = body(page).lower()
    for needle, pat in [
        ("want to exit", r"^Cancel$"),
        ("automatic content checks", r"^Turn on$"),
        ("saved for scheduled", r"^Allow$"),
        ("got it", r"^Got it$"),
    ]:
        if needle not in t:
            continue
        try:
            page.get_by_role("button", name=re.compile(pat, re.I)).first.click(
                force=True, timeout=1200
            )
            page.wait_for_timeout(500)
        except Exception:
            pass


def click_menu_item(page, label: str) -> bool:
    hits = page.evaluate(
        """(label) => {
          const out=[];
          for (const el of document.querySelectorAll('div,span,button,li')) {
            const t=(el.childNodes.length<=4?(el.textContent||''):'').trim();
            if (t!==label) continue;
            const r=el.getBoundingClientRect();
            if (r.width>40 && r.height>16 && r.height<60) out.push({x:r.x+r.w/2,y:r.y+r.h/2});
          }
          return out;
        }""",
        label,
    )
    if not hits:
        return False
    page.mouse.click(hits[0]["x"], hits[0]["y"])
    page.wait_for_timeout(600)
    return True


def delete_matching(page, needle: str) -> dict:
    """Best-effort delete of a scheduled/posted row matching needle text."""
    out = {"needle": needle, "deleted": False}
    page.goto(CONTENT, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3500)
    dismiss(page)
    # Find row with needle, open ⋮, Delete / Remove
    hit = page.evaluate(
        """(needle) => {
          const n=needle.toLowerCase();
          const rows=[...document.querySelectorAll('tr,div,li')];
          for (const row of rows) {
            const t=(row.innerText||'').toLowerCase();
            if (!t.includes(n)) continue;
            const btns=[...row.querySelectorAll('button,[role=button]')];
            for (const b of btns) {
              const al=(b.getAttribute('aria-label')||'').toLowerCase();
              if (al.includes('more') || al.includes('action') || al.includes('menu')) {
                const r=b.getBoundingClientRect();
                if (r.width>8) return {x:r.x+r.width/2,y:r.y+r.height/2,snip:t.slice(0,80)};
              }
            }
          }
          return null;
        }""",
        needle,
    )
    out["row"] = hit
    if not hit:
        return out
    page.mouse.click(hit["x"], hit["y"])
    page.wait_for_timeout(700)
    for label in ("Delete", "Remove", "Delete post", "Discard"):
        if click_menu_item(page, label):
            out["menu"] = label
            break
    page.wait_for_timeout(700)
    for label in ("Delete", "Confirm", "Remove", "OK"):
        try:
            page.get_by_role("button", name=re.compile(rf"^{label}$", re.I)).first.click(
                force=True, timeout=1200
            )
            out["confirm"] = label
            out["deleted"] = True
            break
        except Exception:
            pass
    page.wait_for_timeout(1500)
    return out


def turn_off_content_check(page) -> None:
    page.evaluate(
        """() => {
          const label=[...document.querySelectorAll('*')].find(
            e => e.childNodes.length<=2 && (e.textContent||'').trim()==='Content check lite'
          );
          if (!label) return false;
          const cy=label.getBoundingClientRect().y;
          const switches=[...document.querySelectorAll('button[role=switch],[role=switch]')];
          let best=null, bd=1e9;
          for (const sw of switches) {
            const r=sw.getBoundingClientRect();
            const d=Math.abs(r.y-cy);
            if (d<bd) { best=sw; bd=d; }
          }
          if (!best) return false;
          if ((best.getAttribute('aria-checked')||'')==='true') best.click();
          return true;
        }"""
    )
    page.wait_for_timeout(400)


def fill_caption(page, caption: str) -> bool:
    for sel in (
        '[data-e2e="caption_container"] [contenteditable="true"]',
        'div[contenteditable="true"]',
        'textarea',
    ):
        try:
            loc = page.locator(sel).first
            if loc.count():
                loc.click(timeout=2000)
                page.keyboard.press("Meta+a")
                page.keyboard.type(caption[:2100], delay=2)
                return True
        except Exception:
            continue
    return False


def set_schedule(page, when_iso: str) -> dict:
    """Best-effort schedule picker. Returns status dict."""
    out = {"when": when_iso, "ok": False}
    dt = datetime.fromisoformat(when_iso)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=LONDON)
    # Toggle schedule mode
    try:
        page.get_by_text(re.compile(r"^Schedule$", re.I)).first.click(force=True, timeout=2500)
        page.wait_for_timeout(800)
        out["opened"] = True
    except Exception as e:
        out["open_err"] = str(e)[:120]
        return out
    # Type date/time if inputs exist
    try:
        date_s = dt.strftime("%Y-%m-%d")
        time_s = dt.strftime("%H:%M")
        inputs = page.locator("input")
        for i in range(min(inputs.count(), 8)):
            try:
                ph = (inputs.nth(i).get_attribute("placeholder") or "").lower()
                aria = (inputs.nth(i).get_attribute("aria-label") or "").lower()
                typ = (inputs.nth(i).get_attribute("type") or "").lower()
                if "date" in ph or "date" in aria or typ == "date":
                    inputs.nth(i).fill(date_s)
                    out["date"] = date_s
                if "time" in ph or "time" in aria or typ == "time":
                    inputs.nth(i).fill(time_s)
                    out["time"] = time_s
            except Exception:
                continue
        out["ok"] = bool(out.get("date") or out.get("time") or out.get("opened"))
    except Exception as e:
        out["err"] = str(e)[:160]
    return out


def upload_one(page, item: dict) -> dict:
    path = Path(item["file"])
    if not path.exists():
        raise FileNotFoundError(path)
    page.goto(UPLOAD, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3000)
    dismiss(page)
    turn_off_content_check(page)

    inputs = page.locator('input[type="file"]')
    if inputs.count():
        inputs.first.set_input_files(str(path))
    else:
        with page.expect_file_chooser(timeout=20000) as fc:
            page.get_by_role("button", name=re.compile(r"select|upload", re.I)).first.click(
                force=True
            )
        fc.value.set_files(str(path))

    page.wait_for_timeout(4000)
    fill_caption(page, item["caption"])
    turn_off_content_check(page)

    sched = None
    if not item.get("post_now"):
        sched = set_schedule(page, item["when"])

    # CTA: Schedule or Post
    posted = False
    for label in ("Schedule", "Post", "Publish"):
        try:
            btn = page.get_by_role("button", name=re.compile(rf"^{label}$", re.I))
            if btn.count() and btn.first.is_enabled():
                btn.first.click(force=True, timeout=3000)
                posted = True
                page.wait_for_timeout(5000)
                break
        except Exception:
            continue
    page.screenshot(path=str(AUDIT / f"up_{item['id']}.png"))
    return {
        "id": item["id"],
        "file": str(path),
        "posted": posted,
        "schedule": sched,
        "caption": item["caption"][:120],
        "ok": posted,
    }


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    results = []
    ledger = json.loads(LEDGER.read_text()) if LEDGER.exists() else {"posted": {}}
    posted = ledger.setdefault("posted", {})

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = browser.contexts[0]
        for pg in ctx.pages[1:]:
            try:
                pg.close()
            except Exception:
                pass
        page = ctx.new_page()
        page.bring_to_front()

        for item in QUEUE:
            print(f"TikTok replace {item['id']}…", flush=True)
            row: dict = {"id": item["id"]}
            try:
                row["delete"] = delete_matching(page, item["needle"])
            except Exception as e:
                row["delete"] = {"error": str(e)[:200]}
            try:
                up = upload_one(page, item)
                row["upload"] = up
                row["ok"] = bool(up.get("ok"))
                key = f"tt:{item['id']}"
                posted[key] = {
                    "file": str(item["file"]),
                    "when": item["when"],
                    "mode": "post_now" if item.get("post_now") else "scheduled",
                    "caption_style": "finalverdict-yellow-white-v02",
                    "yt_id": item.get("yt_id"),
                    "replaced_at": datetime.now(LONDON).isoformat(),
                }
                if item.get("yt_id"):
                    posted[f"yt:{item['yt_id']}"] = {
                        "tt_id": item["id"],
                        "when": item["when"],
                        "mode": posted[key]["mode"],
                    }
                print(f"  → ok={row['ok']} del={row.get('delete',{}).get('deleted')}", flush=True)
            except Exception as e:
                row["ok"] = False
                row["error"] = str(e)[:400]
                print(f"  ERR {e}", flush=True)
                page.screenshot(path=str(AUDIT / f"err_{item['id']}.png"))
            results.append(row)

        page.close()

    ledger["updated_at"] = datetime.now(LONDON).isoformat()
    ledger["mode"] = "v02_replace"
    LEDGER.write_text(json.dumps(ledger, indent=2) + "\n")
    RESULT.write_text(
        json.dumps(
            {
                "ran_at": datetime.now(LONDON).isoformat(),
                "ok": sum(1 for r in results if r.get("ok")),
                "results": results,
            },
            indent=2,
        )
        + "\n"
    )
    print(RESULT)
    print(f"OK {sum(1 for r in results if r.get('ok'))}/{len(results)}")


if __name__ == "__main__":
    main()
