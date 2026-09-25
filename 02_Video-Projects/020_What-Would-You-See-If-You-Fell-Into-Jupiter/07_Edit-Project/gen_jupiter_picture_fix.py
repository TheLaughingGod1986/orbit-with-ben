#!/usr/bin/env python3
"""Replace Jupiter shots that are not the thing the sentence names.

Picture only. Veo 3.1 Fast, 16:9, 8s, x1, silent. One retry.
Two failures on the same plate stop the queue. Does not click
Redeem, Agree, delete, or undo. Does not touch the Moon queue.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(
    0,
    "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
    "013_Why-The-Moon-Is-Slowly-Leaving-Us/07_Edit-Project/sunday_moon_long",
)
import gen_flow as g  # noqa: E402

ROOT = Path(
    "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
    "020_What-Would-You-See-If-You-Fell-Into-Jupiter"
)
OUT = ROOT / "04_Generated-Clips" / "picture_fix"
OUT.mkdir(parents=True, exist_ok=True)
g.OUT = OUT
FFMPEG = "/opt/homebrew/bin/ffmpeg"
MODEL = "Veo 3.1 - Fast"
STATUS = OUT / "status.json"
SEEN_PATH = OUT / "seen.json"
TAIL = " Silent picture only. 16:9. Continuous motion. No text."
PROBE = (
    "One Galileo probe only: a blunt brown-gold cone, heat shield forward, "
    "not chrome, not a sphere, not a future ship."
)

# Shot index matches motion_v02/SHOTS.json. Keep plates are not in this list.
PLATES: list[tuple[str, str]] = [
    ("s02", "Jupiter only. Cream, ochre and rust cloud bands rolling. No ground, no rock, no tunnel. Camera falls through the deck." + TAIL),
    ("s03", "Falling through Jupiter. Cream cloud, then darker cloud, then brown murk. No floor, no tunnel, no canyon. Camera keeps descending." + TAIL),
    ("s05", "Jupiter only. Pale zones and darker belts wrapping the planet. No continents, no ocean world, no land. Camera arcs along the bands." + TAIL),
    ("s06", "Jupiter's stripes only. Fast cream and rust bands on a deep atmosphere. No black hole, no land. Camera slides sideways." + TAIL),
    ("s09", "Jupiter's top deck. Bright cream clouds in sunlight. No tunnel, no black hole. Camera drifts forward over the cream." + TAIL),
    ("s10", "Deeper in Jupiter. Rust and brown cloud under a cream deck. No black hole. Camera tilts down." + TAIL),
    ("s11", "Jupiter weather only. Ochre and rust bands. No black hole, no spacecraft. Camera rises through the deck." + TAIL),
    ("s12", "A horizon made of Jupiter cloud. Wind in cream and ochre bands. No mountain, no hole in a planet. Camera looks along the cloud horizon." + TAIL),
    ("s13", "Jupiter clouds, vivid and empty of ground. No desert, no mountain, no canyon. Camera banks across the bands." + TAIL),
    ("s14", "Only Jupiter's bright cloud lid. Cream and rust deck, nothing solid under it. No canyon. Camera pulls back over the lid." + TAIL),
    ("s15", "Falling into Jupiter. No crust, no sea floor, no ice. Cream deck above, thicker air below. Camera drops." + TAIL),
    ("s16", "Jupiter atmosphere. Ochre clouds you would step onto, not ground. No planet with a hole. Camera pushes in." + TAIL),
    ("s17", "Falling through Jupiter cloud only. Cream deck overhead, darker amber cloud below, no shaft, no canyon, no ice wall. Camera descends." + TAIL),
    ("s18", "Deeper Jupiter weather. Dark amber cloud all around, no coast, no tunnel, no rock. Camera keeps sinking." + TAIL),
    ("s19", "Jupiter pulling inward. Cream deck above, air thickening to dark amber below. No black hole, no rock. Camera falls." + TAIL),
    ("s20", "Sinking into Jupiter, not toward rock. Darker amber cloud, no canyon, no desert. Camera descends." + TAIL),
    ("s21", "Jupiter stays atmosphere. Dark cloud all around, no ice crevasse, no seabed. Camera drifts down." + TAIL),
    ("s22", "Falling through Jupiter. Cream bands peel into ochre cloud. Below is thicker air, no shoreline, no canyon, no tunnel. Camera drops." + TAIL),
    ("s23", "Jupiter cloud only. A cream lid above and amber murk below, no tear, no shaft, no ice wall. Camera looks down through cloud." + TAIL),
    ("s24", "Descent through Jupiter. Pressure-dark amber weather all around. No coast, no canyon, no floor. Camera sinks." + TAIL),
    ("s25", PROBE + " It enters Jupiter's ochre clouds. No second craft. Camera follows." + TAIL),
    ("s26", PROBE + " A parachute opens. It falls through ochre clouds. No second craft. Camera beside it." + TAIL),
    ("s27", PROBE + " Parachute open, falling through Jupiter cloud. No second craft. Camera drops with it." + TAIL),
    ("s28", PROBE + " Deeper, parachute gone, darker Jupiter cloud. Same cone. Camera looks down past it." + TAIL),
    ("s29", PROBE + " Hot murk, darker cloud, same cone. No ground. Camera circles it." + TAIL),
    ("s30", PROBE + " Same cone in dark cloud. No ground, no chrome ship. Camera pulls back." + TAIL),
    ("s31", PROBE + " Same cone inside the weather, ochre murk. Camera closes in." + TAIL),
    ("s32", PROBE + " Same small cone, still in the cloud. Darker air ahead. Camera drifts past." + TAIL),
    ("s33", PROBE + " Same cone left behind in dark cloud. A long dark ahead, no floor. Camera looks onward." + TAIL),
    ("s34", PROBE + " Same cone in thinner hot cloud. No second craft. Camera slides by." + TAIL),
    ("s35", PROBE + " Same cone in one patch of vast Jupiter bands. Not a black hole. Camera widens to the planet." + TAIL),
    ("s36", PROBE + " Same small cone against Jupiter's bright deck. Camera looks up at the bands." + TAIL),
    ("s39", "Under Jupiter's clouds. Sunlight dying into brown murk. No tunnel, no canyon, no blue sky. Camera falls." + TAIL),
    ("s40", "Jupiter cloud blankets. Pale ammonia, then dirtier cloud, then darker water cloud. No canyon, no ice. Camera descends through them." + TAIL),
    ("s41", "Brown murk under Jupiter. Sunlight scattering out. No ice canyon, no blue sky, no rock. Camera pushes into the murk." + TAIL),
    ("s48", "Inside Jupiter. Dark amber fluid, pressure climbing, no spacecraft, no cave, no floor. Camera drifts." + TAIL),
    ("s49", "Jupiter's hydrogen becoming a dark amber fluid. No spacecraft. Camera sinks." + TAIL),
    ("s50", "Metallic hydrogen. Slow dark-amber fluid, no wire, no spacecraft, no floor. Camera glides." + TAIL),
    ("s51", "A planet-sized current in dark amber fluid. No chrome ship, no cavern. Camera drifts through it." + TAIL),
    ("s52", "Dark amber pressure, slow and hot, no floor, no shining cavern, no spacecraft. Camera eases forward." + TAIL),
    ("s54", "No hard core. Heavy material smeared through dark amber fluid. No boulder, no spacecraft. Camera moves through the gradient." + TAIL),
    ("s46", "Inside Jupiter. Near-black brown murk and one brief white lightning flash. No blue planet, no ice, no walls, no ground. Cloud keeps moving." + TAIL),
    ("s58", "Jupiter's top deck only. Lateral wind in cream and rust bands. A horizon made of cloud. No ocean, no ice giant, no blue world. Camera slides." + TAIL),
    ("s61", PROBE + " It fades into dark murk. No impact, no fireball, no ground. Camera stays with the same cone." + TAIL),
    ("s68", "Jupiter only. Quiet pull-back until cream, ochre and rust stripes fill the frame and the red oval spins. No blue world, no ice, no second planet. Camera drifts back." + TAIL),
    ("s71", "Jupiter only. Quiet pull-back until cream, ochre and rust bands fill the frame and the red oval keeps spinning. No ice giant, no second planet, no haze world. Camera drifts back over the deck." + TAIL),
]


def timeouts(page) -> int:
    return page.evaluate(
        """() => (document.body.innerText.match(/Generation timed out/g) || []).length"""
    )


def audio_fails(page) -> int:
    return page.evaluate(
        """() => (document.body.innerText.match(/Audio generation failed/g) || []).length"""
    )


def ensure_silent(page) -> None:
    """Flow fails the plate when audio generation fails. Silent pictures only."""
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    state = page.evaluate(
        """() => {
          const b=[...document.querySelectorAll('button')].find(el =>
            (el.getAttribute('aria-label')||el.innerText||'').includes('Return silent videos'));
          if (!b) return 'missing';
          return b.getAttribute('aria-checked') || 'false';
        }"""
    )
    if state == "true":
        print(" silent videos on", flush=True)
        page.keyboard.press("Escape")
        return
    opened = page.evaluate(
        """() => {
          const tile=document.querySelector('flow-error-tile');
          const b=tile && [...tile.querySelectorAll('button')].find(el => (el.innerText||'').trim()==='settings');
          if (!b) return false;
          b.click();
          return true;
        }"""
    )
    page.wait_for_timeout(700)
    if not opened and state == "missing":
        print(" silent toggle not visible", flush=True)
        return
    page.evaluate(
        """() => {
          const b=[...document.querySelectorAll('button')].find(el =>
            (el.getAttribute('aria-label')||el.innerText||'').includes('Return silent videos'));
          if (b && b.getAttribute('aria-checked') !== 'true') b.click();
        }"""
    )
    page.wait_for_timeout(300)
    print(" silent videos set", flush=True)
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)


def top_card(page) -> str:
    g.scroll_top(page)
    return page.evaluate(
        """() => {
          const img=[...document.querySelectorAll('img')].filter(el => {
            const r=el.getBoundingClientRect();
            return r.height>100 && r.y>0 && r.y<1200;
          }).sort((a,b)=>a.getBoundingClientRect().y-b.getBoundingClientRect().y)[0];
          return img ? (img.currentSrc||'') : '';
        }"""
    )


def write_status(payload: dict) -> None:
    STATUS.write_text(json.dumps(payload, indent=2))


def save_clip(key: str, body: bytes) -> None:
    raw = OUT / f"{key}.mp4"
    silent = OUT / f"{key}_silent.mp4"
    raw.write_bytes(body)
    subprocess.run(
        [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw), "-an", "-c:v", "copy", str(silent)],
        check=True,
    )
    for ss, name in (("1", "t1"), ("4", "mid"), ("7", "t7")):
        subprocess.run(
            [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-ss", ss, "-i", str(silent),
             "-frames:v", "1", str(OUT / f"{key}_{name}.jpg")],
            check=True,
        )


def configure_veo(page) -> None:
    """16:9 Veo 3.1 Fast. Monday left this project on Omni."""
    g.ensure_project(page)
    page.bring_to_front()
    g.open_settings(page)
    if not g.settings_open(page):
        g.open_settings(page)
    model = page.evaluate(
        """() => {
          const el=[...document.querySelectorAll('button')].find(b => /Omni|Veo/.test(b.innerText||''));
          if (!el) return '';
          return (el.innerText||'').replace(/\\s+/g,' ').trim();
        }"""
    )
    print(" model", model, flush=True)
    if "Veo 3.1 - Fast" not in model:
        if not model:
            raise RuntimeError("model button hidden")
        g.click_button_including(page, "arrow_drop_down")
        page.wait_for_timeout(400)
        hit = page.evaluate(
            """() => {
              const el=[...document.querySelectorAll('button')].find(b =>
                (b.innerText||'').replace(/\\s+/g,' ').trim().endsWith('Veo 3.1 - Fast'));
              if (!el) return null;
              const r=el.getBoundingClientRect();
              return {x:r.x+r.width/2, y:r.y+r.height/2, t:(el.innerText||'').trim()};
            }"""
        )
        if not hit:
            raise RuntimeError("missing Veo 3.1 - Fast")
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(400)
        g.open_settings(page)
    summary = page.evaluate(
        """() => (document.querySelector('[settingstriggercontent], .settings-summary')?.innerText||'').replace(/\\s+/g,' ').trim()"""
    )
    if "crop_16_9" not in summary:
        clicked = page.evaluate(
            """() => {
              const el=[...document.querySelectorAll('button')].find(b => {
                const t=(b.innerText||'').replace(/\\s+/g,' ').trim();
                const r=b.getBoundingClientRect();
                return t.endsWith('16:9') && !t.includes('9:16') && r.width>4;
              });
              if (!el) return false;
              el.click();
              return true;
            }"""
        )
        if not clicked:
            g.open_settings(page)
            clicked = page.evaluate(
                """() => {
                  const el=[...document.querySelectorAll('button')].find(b => {
                    const t=(b.innerText||'').replace(/\\s+/g,' ').trim();
                    const r=b.getBoundingClientRect();
                    return t.endsWith('16:9') && !t.includes('9:16') && r.width>4;
                  });
                  if (!el) return false;
                  el.click();
                  return true;
                }"""
            )
        if not clicked:
            raise RuntimeError("16:9 missing")
        page.wait_for_timeout(300)
    page.evaluate(
        """() => {
          const exact=(t) => [...document.querySelectorAll('button')].find(b => (b.innerText||'').trim()===t);
          const eight=exact('8s');
          if (eight) eight.click();
          const one=exact('x1');
          if (one) one.click();
        }"""
    )
    page.keyboard.press("Escape")
    page.wait_for_timeout(250)
    final = page.evaluate(
        """() => (document.querySelector('[settingstriggercontent], .settings-summary')?.innerText||'').replace(/\\s+/g,' ').trim()"""
    )
    print(" settings", final, flush=True)
    if "crop_16_9" not in final:
        raise RuntimeError(f"not 16:9: {final}")


def main() -> None:
    from playwright.sync_api import sync_playwright

    print("plates", len(PLATES), flush=True)
    seen = {
        "4703c1e3-4ffe-42d1-8905-c55a9bc6cceb",
        "5b5af0fb-6fe7-4be1-b098-3fcc7e674e90",
    }
    if SEEN_PATH.exists():
        seen.update(json.loads(SEEN_PATH.read_text()))
    fails: dict[str, int] = {}
    if STATUS.exists():
        old = json.loads(STATUS.read_text())
        fails = {k: int(v) for k, v in (old.get("fails") or {}).items()}
        if old.get("stopped") or old.get("paused"):
            print("already stopped", old.get("key"), old.get("reason"), flush=True)
            raise SystemExit(2)
    jobs = list(PLATES)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(g.CDP)
        page = next(
            pg for ctx in browser.contexts for pg in ctx.pages
            if "flow.google" in (pg.url or "") and "RotateCookies" not in (pg.url or "")
        )
        page.bring_to_front()
        g.ensure_project(page)
        ensure_silent(page)
        configure_veo(page)
        idx = 0
        while idx < len(jobs):
            key, prompt = jobs[idx]
            silent = OUT / f"{key}_silent.mp4"
            if silent.exists() and silent.stat().st_size > 100_000:
                print("have", key, flush=True)
                idx += 1
                continue
            g.clear_chips(page)
            attached = page.evaluate(
                """() => [...document.querySelectorAll('flow-video-ingredient-chip')].some(el => {
                  const r=el.getBoundingClientRect();
                  const t=el.innerText||'';
                  return /orbit/i.test(t) || (r.width>80 && !!el.querySelector('img'));
                })"""
            )
            if attached:
                raise RuntimeError("Orbit ingredient still on the Jupiter prompt")
            blocking = page.evaluate(
                """() => [...document.querySelectorAll('button')].some(b => {
                  const t=(b.innerText||'');
                  const r=b.getBoundingClientRect();
                  return /agree|redeem/i.test(t) && r.width>20 && r.height>20;
                })"""
            )
            if blocking:
                raise RuntimeError("prepaid dialog is open; not clicking Agree")
            before = top_card(page)
            before_srcs = set(page.evaluate(
                """() => [...document.querySelectorAll('video')].map(el => el.currentSrc||el.src||'').filter(Boolean)"""
            ))
            before_to = timeouts(page)
            before_audio = audio_fails(page)
            box = page.locator('[contenteditable="true"]').first
            box.click()
            page.keyboard.press("Meta+A")
            page.keyboard.press("Backspace")
            page.wait_for_timeout(80)
            page.keyboard.insert_text(prompt)
            page.locator('button[aria-label="Start generation"]').first.click()
            print("submitted", key, "timeouts", before_to, flush=True)
            src = None
            reason = ""
            t0 = time.time()
            while time.time() - t0 < 210:
                page.wait_for_timeout(8000)
                g.ensure_project(page)
                if timeouts(page) > before_to:
                    reason = "flow-timeout"
                    page.keyboard.press("Escape")
                    break
                if audio_fails(page) > before_audio:
                    reason = "audio-fail"
                    page.keyboard.press("Escape")
                    break
                now = top_card(page)
                fresh = bool(now) and now != before and not any(uid in now for uid in seen)
                print(f"  {key} {int(time.time()-t0)}s fresh={fresh}", flush=True)
                if not fresh:
                    continue
                src = g.download_top(page, seen)
                page.keyboard.press("Escape")
                if not src:
                    fresh_srcs = [
                        s for s in page.evaluate(
                            """() => [...document.querySelectorAll('video')].map(el => el.currentSrc||el.src||'').filter(Boolean)"""
                        )
                        if s not in before_srcs and not any(uid in s for uid in seen)
                    ]
                    if fresh_srcs:
                        src = fresh_srcs[0]
                        print("  src fallback", flush=True)
                if src:
                    break
            if not src:
                if not reason:
                    reason = "timeout-wait"
                fails[key] = fails.get(key, 0) + 1
                write_status({"fails": fails, "stopped": fails[key] >= 2, "key": key, "reason": reason, "done": idx})
                print("fail", key, reason, fails[key], flush=True)
                if fails[key] >= 2:
                    raise SystemExit(2)
                jobs.insert(idx + 1, (key, prompt))
                idx += 1
                continue
            resp = page.request.get(src)
            body = resp.body()
            if resp.status != 200 or b"ftyp" not in body[:64] or len(body) < 100_000:
                fails[key] = fails.get(key, 0) + 1
                write_status({"fails": fails, "stopped": fails[key] >= 2, "key": key, "reason": "bad-file", "done": idx})
                print("bad", key, resp.status, len(body), flush=True)
                if fails[key] >= 2:
                    raise SystemExit(2)
                jobs.insert(idx + 1, (key, prompt))
                idx += 1
                continue
            uid = g.uid_of(src)
            if uid:
                seen.add(uid)
                SEEN_PATH.write_text(json.dumps(sorted(seen), indent=2))
            save_clip(key, body)
            print("saved", key, silent.stat().st_size, flush=True)
            write_status({"fails": fails, "stopped": False, "last": key, "done": idx + 1, "of": len(PLATES)})
            idx += 1
    print("ALL", flush=True)


if __name__ == "__main__":
    main()
