#!/usr/bin/env python3
"""Upload missing v02 TikTok shorts (clue + 6 BH + hot) via Chrome CDP :9222.

Workaround: Playwright CDP cannot transfer files >50MB — use pre-compressed
copy under audit/tt_v02_replace/upload_under50/ when needed.

Verifies schedule inputs (HH:MM + YYYY-MM-DD) before clicking Schedule, then
checks Studio content for the caption needle after each post.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

ROOT = Path("/Users/ben/code/Orbit-YouTube")
SETUP = ROOT / "00_Brand/Channel-Setup/TikTok"
sys.path.insert(0, str(SETUP / "auto"))
from upload_block import MESSAGE, uploads_paused  # noqa: E402
LEDGER = SETUP / "TIKTOK_POSTED.json"
AUDIT = SETUP / "audit" / "tt_v02_replace"
RESULT = SETUP / "TIKTOK_MISSING_UPLOAD_RESULT.json"
UNDER50 = AUDIT / "upload_under50"
CONTENT = "https://www.tiktok.com/tiktokstudio/content"
UPLOAD = "https://www.tiktok.com/tiktokstudio/upload?from=upload"
LONDON = ZoneInfo("Europe/London")

ALIENS = ROOT / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/06_Final-Exports"
BH = ROOT / "02_Video-Projects/002_What-Happens-If-You-Fall-Into-A-Black-Hole/10_Shorts/06_Final-Exports"
EXO = ROOT / "02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds/10_Shorts/06_Final-Exports"

# Only posts currently missing from Studio inventory.
QUEUE = [
    {
        "id": "aliens-clue",
        "file": UNDER50 / "aliens_short-04_hidden-clues_v02_cdp.mp4",
        "needle": "first alien clue",
        "when": "2026-08-04T12:30:00+01:00",
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
        "caption": (
            "The point of no return, explained. Full film on YouTube. "
            "#eventhorizon #blackhole #orbitwithben"
        ),
        "yt_id": "5nMieBeymKU",
    },
    {
        "id": "exo-hot",
        "file": EXO / "exoplanets_short-04_hot-jupiter_v02.mp4",
        "needle": "hottest nights",
        "when": "2026-08-24T12:30:00+01:00",
        "caption": (
            "The hottest nights in the universe — Hot Jupiters that glow on the nightside. "
            "Full film on YouTube. #hotjupiter #exoplanets #alienworlds #orbitwithben"
        ),
        "yt_id": "e8-rKGv37o4",
    },
]


def body(page) -> str:
    try:
        return page.inner_text("body")
    except Exception:
        return ""


def dismiss(page) -> None:
    """Dismiss common TikTok Studio modals, including content-check continue."""
    for _ in range(4):
        t = body(page).lower()
        handled = False
        # Content-check interrupt — keep going so Schedule completes.
        if "continue to post" in t or "continue posting before the check" in t:
            for label in ("Post now", "Continue", "Schedule"):
                try:
                    page.get_by_role("button", name=re.compile(rf"^{label}$", re.I)).first.click(
                        force=True, timeout=1500
                    )
                    page.wait_for_timeout(900)
                    handled = True
                    break
                except Exception:
                    continue
        for needle, pat in [
            ("want to exit", r"^Cancel$"),
            ("automatic content checks", r"^Not now$|^Turn on$"),
            ("saved for scheduled", r"^Allow$"),
            ("got it", r"^Got it$"),
            ("not now", r"^Not now$"),
        ]:
            if needle not in t:
                continue
            try:
                page.get_by_role("button", name=re.compile(pat, re.I)).first.click(
                    force=True, timeout=1200
                )
                page.wait_for_timeout(400)
                handled = True
            except Exception:
                pass
        if not handled:
            break


def blocked(page) -> str | None:
    t = body(page).lower()
    if "check limit" in t or "reached your check limit" in t:
        return "content_check_limit"
    if "something went wrong" in t:
        return "something_went_wrong"
    return None


def turn_off_content_check(page) -> dict:
    """TikTok uses input.Switch__input[role=switch] with .checked — not aria-checked buttons."""
    return page.evaluate(
        """() => {
          const label=[...document.querySelectorAll('*')].find(
            e => e.childNodes.length<=3 && (e.textContent||'').trim()==='Content check lite'
          );
          if (!label) return {ok:false, err:'no_label'};
          const lr=label.getBoundingClientRect();
          let best=null, bd=1e9;
          for (const sw of document.querySelectorAll('input.Switch__input[role=switch], input[role=switch]')) {
            const r=sw.getBoundingClientRect();
            if (r.width<4) continue;
            const dy=Math.abs((r.y+r.height/2)-(lr.y+lr.height/2));
            if (dy<50 && dy<bd) { best=sw; bd=dy; }
          }
          if (!best) return {ok:false, err:'no_switch'};
          const before=!!best.checked;
          if (best.checked) {
            // Click the visible track (parent) — raw input click is flaky
            const track=best.closest('.Switch, [class*=Switch]') || best.parentElement || best;
            track.click();
            if (best.checked) best.click();
          }
          return {ok:true, before, after:!!best.checked, y:Math.round(lr.y)};
        }"""
    )


def fill_caption(page, caption: str) -> bool:
    for sel in (
        '[data-e2e="caption_container"] [contenteditable="true"]',
        'div[contenteditable="true"]',
        "textarea",
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


def readonly_schedule_values(page) -> list[str]:
    return page.evaluate(
        """() => [...document.querySelectorAll('input.TUXTextInputCore-input')]
            .filter(el => el.readOnly && el.getBoundingClientRect().width>40)
            .map(el => el.value)"""
    )


def click_time_option(page, side: str, value: str) -> bool:
    """side: 'left' (hour) or 'right' (minute)."""
    return bool(
        page.evaluate(
            """({side, value}) => {
              const cls = side === 'left'
                ? 'tiktok-timepicker-left'
                : 'tiktok-timepicker-right';
              const nodes = [...document.querySelectorAll('span.' + cls)];
              const hit = nodes.find(n => (n.textContent||'').trim() === value);
              if (!hit) return false;
              hit.scrollIntoView({block:'center'});
              hit.click();
              return true;
            }""",
            {"side": side, "value": value},
        )
    )


def ensure_calendar_month(page, dt: datetime) -> dict:
    """Navigate calendar-wrapper to target month/year."""
    want_month = dt.strftime("%B")  # August
    want_year = str(dt.year)
    info = {"month": want_month, "year": want_year, "nav": []}
    for _ in range(14):
        header = page.evaluate(
            """() => {
              const t=document.querySelector('.calendar-wrapper .month-title');
              const y=document.querySelector('.calendar-wrapper .month-header-wrapper');
              const txt=(y&&y.innerText)||'';
              return {title:(t&&t.textContent||'').trim(), txt:txt.replace(/\\s+/g,' ').trim()};
            }"""
        )
        info["header"] = header
        txt = (header or {}).get("txt") or ""
        if want_month in txt and want_year in txt:
            info["ok"] = True
            return info
        # Decide direction from parsed month
        clicked = page.evaluate(
            """({want_month, want_year}) => {
              const wrap=document.querySelector('.calendar-wrapper .month-header-wrapper');
              if (!wrap) return null;
              const arrows=[...wrap.querySelectorAll('button,span,div,svg')].filter(el=>{
                const r=el.getBoundingClientRect();
                return r.width>8 && r.height>8 && r.width<48;
              });
              // heuristic: first arrow = prev, last = next
              if (arrows.length<2) return null;
              const cur=wrap.innerText||'';
              const months=['January','February','March','April','May','June','July','August','September','October','November','December'];
              let ci=-1;
              for (let i=0;i<months.length;i++) if (cur.includes(months[i])) ci=i;
              const wi=months.indexOf(want_month);
              let cy=parseInt((cur.match(/20\\d{2}/)||[])[0]||'0',10);
              const wy=parseInt(want_year,10);
              const curIdx=cy*12+ci, wantIdx=wy*12+wi;
              if (ci<0||wi<0) { arrows[arrows.length-1].click(); return 'next-fallback'; }
              if (wantIdx>curIdx) { arrows[arrows.length-1].click(); return 'next'; }
              if (wantIdx<curIdx) { arrows[0].click(); return 'prev'; }
              return 'same';
            }""",
            {"want_month": want_month, "want_year": want_year},
        )
        info["nav"].append(clicked)
        if clicked == "same":
            info["ok"] = True
            return info
        page.wait_for_timeout(400)
    info["ok"] = False
    return info


def set_schedule(page, when_iso: str) -> dict:
    out: dict = {"when": when_iso, "ok": False}
    dt = datetime.fromisoformat(when_iso)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=LONDON)
    date_s = dt.strftime("%Y-%m-%d")
    hour = f"{dt.hour:02d}"
    # TikTok minutes are 5-min steps
    minute = f"{(dt.minute // 5) * 5:02d}"
    time_s = f"{hour}:{minute}"
    out["want"] = [time_s, date_s]

    # Select Schedule radio
    try:
        page.locator("input[type=radio][value=schedule]").first.click(force=True, timeout=2500)
        page.wait_for_timeout(500)
    except Exception:
        try:
            page.get_by_text(re.compile(r"^Schedule$", re.I)).first.click(force=True, timeout=2500)
            page.wait_for_timeout(500)
        except Exception as e:
            out["open_err"] = str(e)[:120]
            return out
    out["opened"] = True

    vals = readonly_schedule_values(page)
    out["before"] = vals

    # --- Time ---
    clicked_time = page.evaluate(
        """() => {
          const inputs=[...document.querySelectorAll('input.TUXTextInputCore-input')]
            .filter(el => el.readOnly && /^\\d{2}:\\d{2}$/.test(el.value));
          if (!inputs.length) return false;
          inputs[0].click();
          return true;
        }"""
    )
    out["time_clicked"] = clicked_time
    page.wait_for_timeout(500)
    out["hour"] = click_time_option(page, "left", hour)
    page.wait_for_timeout(200)
    out["minute"] = click_time_option(page, "right", minute)
    page.wait_for_timeout(300)
    # Close timepicker by pressing Escape / clicking schedule label
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(300)

    # --- Date ---
    page.evaluate(
        """() => {
          const inputs=[...document.querySelectorAll('input.TUXTextInputCore-input')]
            .filter(el => el.readOnly && /^\\d{4}-\\d{2}-\\d{2}$/.test(el.value));
          if (!inputs.length) return false;
          inputs[0].click();
          return true;
        }"""
    )
    page.wait_for_timeout(600)
    out["month_nav"] = ensure_calendar_month(page, dt)

    day = str(dt.day)
    picked = page.evaluate(
        """(day) => {
          const wrap=document.querySelector('.calendar-wrapper');
          if (!wrap) return null;
          // Only current-month selectable days
          const days=[...wrap.querySelectorAll('span.day.valid')];
          const hit=days.find(el => (el.textContent||'').trim()===day);
          if (!hit) return null;
          hit.click();
          return 'valid:'+day;
        }""",
        day,
    )
    out["date_pick"] = picked
    page.wait_for_timeout(500)

    vals2 = readonly_schedule_values(page)
    out["values"] = vals2
    out["ok"] = len(vals2) >= 2 and vals2[0] == time_s and vals2[1] == date_s
    return out


def wait_uploaded(page, timeout_s: int = 90) -> bool:
    for _ in range(timeout_s):
        t = body(page).lower()
        if "uploaded" in t and "uploading" not in t:
            return True
        if "upload failed" in t or "couldn’t upload" in t or "couldn't upload" in t:
            return False
        page.wait_for_timeout(1000)
    return "uploaded" in body(page).lower()


def studio_has_needle(page, needle: str) -> bool:
    page.goto(CONTENT, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3500)
    dismiss(page)
    for _ in range(8):
        try:
            page.keyboard.press("PageDown")
        except Exception:
            break
        page.wait_for_timeout(500)
    return needle.lower() in body(page).lower()


def upload_one(page, item: dict) -> dict:
    path = Path(item["file"])
    if not path.exists():
        raise FileNotFoundError(path)
    size_mb = path.stat().st_size / 1e6
    if size_mb > 49.5:
        raise RuntimeError(f"file {path.name} is {size_mb:.1f}MB > 49.5 CDP limit")

    page.goto(UPLOAD, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(2500)
    dismiss(page)

    inputs = page.locator('input[type="file"]')
    if not inputs.count():
        raise RuntimeError("no file input")
    inputs.first.set_input_files(str(path))

    if not wait_uploaded(page):
        page.screenshot(path=str(AUDIT / f"err_upload_{item['id']}.png"))
        return {"id": item["id"], "ok": False, "error": "upload_not_ready", "size_mb": size_mb}

    turn_off = turn_off_content_check(page)
    page.wait_for_timeout(400)
    fill_caption(page, item["caption"])
    turn_off2 = turn_off_content_check(page)
    page.wait_for_timeout(400)
    dismiss(page)

    # Content-check daily limit is noisy but Schedule often still works if toggle is OFF.
    pre_block = blocked(page)
    if pre_block:
        print(f"  note: pre-schedule block={pre_block} toggle={turn_off2}", flush=True)

    sched = set_schedule(page, item["when"])
    if not sched.get("ok"):
        page.wait_for_timeout(800)
        sched = set_schedule(page, item["when"])

    turn_off3 = turn_off_content_check(page)
    page.wait_for_timeout(500)

    posted = False
    cta_err = None
    if not sched.get("ok"):
        page.screenshot(path=str(AUDIT / f"err_sched_{item['id']}.png"))
        return {
            "id": item["id"],
            "file": str(path),
            "size_mb": round(size_mb, 1),
            "schedule": sched,
            "posted_click": False,
            "ok": False,
            "error": "schedule_values_mismatch",
            "pre_block": pre_block,
            "toggle": turn_off3,
            "caption": item["caption"][:100],
        }

    # Footer Schedule via mouse — get_by_role can hit the wrong control
    click = page.evaluate(
        """() => {
          const btns=[...document.querySelectorAll('button')].filter(
            b => (b.innerText||'').trim()==='Schedule' && !b.disabled
          );
          if (!btns.length) return null;
          btns.sort((a,b)=>b.getBoundingClientRect().y - a.getBoundingClientRect().y);
          const r=btns[0].getBoundingClientRect();
          return {x:r.x+r.width/2, y:r.y+r.height/2};
        }"""
    )
    post_api = {"seen": False}
    def _on_post_api(resp):
        try:
            if "project/post" not in resp.url:
                return
            post_api["seen"] = True
            post_api["status"] = resp.status
            post_api["url"] = resp.url[:220]
            try:
                post_api["body"] = resp.json()
            except Exception:
                try:
                    post_api["text"] = resp.text()[:500]
                except Exception:
                    pass
        except Exception:
            pass
    page.on("response", _on_post_api)

    if not click:
        cta_err = "schedule_cta_missing_or_disabled"
    else:
        try:
            page.mouse.click(click["x"], click["y"])
            posted = True
            page.wait_for_timeout(1500)
            # Content-check often pops "Continue to post?" — must confirm.
            for _ in range(8):
                dismiss(page)
                if "upload" not in (page.url or "") or "Video published" in body(page):
                    break
                t = body(page).lower()
                if "continue to post" in t or "continue posting before the check" in t:
                    try:
                        page.get_by_role("button", name=re.compile(r"^Post now$", re.I)).first.click(
                            force=True, timeout=2000
                        )
                    except Exception:
                        pass
                page.wait_for_timeout(1000)
            page.wait_for_timeout(4000)
        except Exception as e:
            cta_err = str(e)[:160]

    dismiss(page)
    page.wait_for_timeout(2000)
    still_on_upload = "upload" in (page.url or "")
    blk2 = blocked(page)
    page.screenshot(path=str(AUDIT / f"up_{item['id']}.png"))

    result = {
        "id": item["id"],
        "file": str(path),
        "size_mb": round(size_mb, 1),
        "schedule": sched,
        "posted_click": posted,
        "still_on_upload": still_on_upload,
        "pre_block": pre_block,
        "block": blk2,
        "toggle": {"first": turn_off, "mid": turn_off2, "pre_cta": turn_off3},
        "cta_err": cta_err,
        "post_api": post_api,
        "caption": item["caption"][:100],
    }

    # TikTok account restriction (status_code 21) — fail fast, do not claim success.
    api_body = post_api.get("body") if isinstance(post_api.get("body"), dict) else {}
    api_code = api_body.get("status_code")
    api_msg = str(api_body.get("status_msg") or "")
    if api_code not in (None, 0) or "temporarily prevented from posting" in api_msg.lower():
        result["ok"] = False
        result["error"] = "account_posting_restricted"
        result["status_code"] = api_code
        result["status_msg"] = api_msg[:300]
        result["abort"] = True
        return result

    if still_on_upload and "something went wrong" in body(page).lower():
        result["ok"] = False
        result["error"] = "something_went_wrong"
        result["abort"] = True
        return result

    # Verify in Studio on a fresh page (avoids leave-dialog ERR_ABORTED).
    present = False
    try:
        present = studio_has_needle(page, item["needle"])
    except Exception as e:
        result["verify_err"] = str(e)[:240]
        try:
            page2 = page.context.new_page()
            present = studio_has_needle(page2, item["needle"])
            page2.close()
        except Exception as e2:
            result["verify_err2"] = str(e2)[:240]
    result["verified"] = present
    result["ok"] = bool(posted and sched.get("ok") and present)
    if posted and sched.get("ok") and not present:
        result["ok"] = False
        result["error"] = "not_in_studio_after_schedule"
        result["still_on_upload"] = still_on_upload
    elif still_on_upload and not present:
        result["ok"] = False
        result["error"] = "still_on_upload_after_schedule"
    return result


def main() -> int:
    if uploads_paused():
        print(MESSAGE, flush=True)
        return 2
    AUDIT.mkdir(parents=True, exist_ok=True)
    UNDER50.mkdir(parents=True, exist_ok=True)
    results = []
    ledger = json.loads(LEDGER.read_text()) if LEDGER.exists() else {"posted": {}}
    posted = ledger.setdefault("posted", {})

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = browser.contexts[0]
        for pg in list(ctx.pages)[1:]:
            try:
                pg.close()
            except Exception:
                pass
        page = ctx.new_page()
        page.on("dialog", lambda d: d.dismiss())
        page.bring_to_front()

        for item in QUEUE:
            print(f"\n=== Upload {item['id']} → {item['when']} ===", flush=True)
            row: dict = {"id": item["id"]}
            try:
                up = upload_one(page, item)
                row.update(up)
                print(
                    f"  ok={up.get('ok')} sched={up.get('schedule',{}).get('values')} "
                    f"verified={up.get('verified')} err={up.get('error')}",
                    flush=True,
                )
                if up.get("ok"):
                    key = f"tt:{item['id']}"
                    posted[key] = {
                        "file": str(item["file"]),
                        "when": item["when"],
                        "mode": "scheduled",
                        "caption_style": "finalverdict-yellow-white-v02",
                        "yt_id": item.get("yt_id"),
                        "uploaded_at": datetime.now(LONDON).isoformat(),
                    }
                    if item.get("yt_id"):
                        posted[f"yt:{item['yt_id']}"] = {
                            "tt_id": item["id"],
                            "when": item["when"],
                            "mode": "scheduled",
                        }
                if up.get("abort"):
                    print("ABORT: content check limit — stop batch", flush=True)
                    results.append(row)
                    break
            except Exception as e:
                row["ok"] = False
                row["error"] = str(e)[:400]
                print(f"  ERR {e}", flush=True)
                try:
                    page.screenshot(path=str(AUDIT / f"err_{item['id']}.png"))
                except Exception:
                    pass
            results.append(row)

        try:
            page.close()
        except Exception:
            pass

    ledger["updated_at"] = datetime.now(LONDON).isoformat()
    ledger["mode"] = "missing_v02_upload"
    LEDGER.write_text(json.dumps(ledger, indent=2) + "\n")
    payload = {
        "ran_at": datetime.now(LONDON).isoformat(),
        "ok": sum(1 for r in results if r.get("ok")),
        "total": len(results),
        "results": results,
    }
    RESULT.write_text(json.dumps(payload, indent=2) + "\n")
    print(RESULT)
    print(f"OK {payload['ok']}/{payload['total']}")
    return 0 if payload["ok"] == len(QUEUE) else 1


if __name__ == "__main__":
    sys.exit(main())
