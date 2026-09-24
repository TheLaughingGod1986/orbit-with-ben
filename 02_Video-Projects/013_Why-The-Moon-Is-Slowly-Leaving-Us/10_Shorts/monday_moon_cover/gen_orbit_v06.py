#!/usr/bin/env python3
"""Monday Moon Short. Rebuild the Orbit plate only.

Attaches the canonical 16:9 still. The square filename is not on disk.
Does not attach the rejected 3s frame. Does not schedule. Does not resume Jupiter.
Replaces the UAT file only after the open, react, and loop frames pass the face gate.
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
    "013_Why-The-Moon-Is-Slowly-Leaving-Us/10_Shorts/monday_moon_cover"
)
OUT = ROOT / "plates" / "orbit_v06"
OUT.mkdir(parents=True, exist_ok=True)
FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"
PY = "/tmp/stt-venv/bin/python"
GATE = ROOT / "gate_face.py"
REF = Path(
    "/Users/benjaminoats/YouTube/orbit-with-ben/01_Orbit-Character/"
    "05_Seedance-References/orbit-seedance-reference-16x9-v01.png"
)
MODEL = "Omni 1.1 Flash"
STATUS = OUT / "status.json"
VOICE = ROOT / "monday_moon_short_v01.mp4"
SUN = Path("/tmp/moon_short_asm/sun.mp4")
BARE = Path("/tmp/moon_short_asm/bare.mp4")
CAPS = Path("/tmp/moon_short_asm")
UAT = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/"
    "OWB UAT/monday-moon-short.mp4"
)
FINAL = ROOT / "monday_moon_short_v06.mp4"
MAX_FAILS = 4
PROMPT = (
    "The attached still is the only character. Copy that Orbit exactly. "
    "One solid matte orange rounded floater. One black visor on the front, a face window, "
    "not a hole through the head. Inside the visor, exactly two separate cream circular eyes, "
    "each with a dark pupil. Short stubby orange arms. One antenna with a small bulb. "
    "No legs. One small soft glow centered under the body. "
    "He faces the camera, floats, and tips slightly toward the Moon. "
    "One grey cratered Moon is in the near-black sky beside him and drifts a little farther. "
    "Both stay large in frame the whole shot. No second character. No Earth. "
    "Silent picture only. Vertical 9:16. Continuous motion. No text. No letters."
)


def abort_if_cushion(page) -> None:
    label = page.evaluate(
        """() => {
          const b=[...document.querySelectorAll('button')].find(el => {
            const t=el.innerText||'';
            if (!/Agree|Redeem/i.test(t)) return false;
            const r=el.getBoundingClientRect();
            return r.width>20 && r.height>20;
          });
          return b ? (b.innerText||'').trim().slice(0,80) : '';
        }"""
    )
    if label:
        raise SystemExit(f"cushion button visible, not clicking: {label}")


def panel_open(page) -> bool:
    return bool(page.evaluate(
        """() => [...document.querySelectorAll('button')].some(b => {
          const t=b.innerText||'';
          const r=b.getBoundingClientRect();
          return r.width>4 && (t.includes('9:16') || t.includes('16:9') || t.includes('crop_9_16') || t.includes('crop_16_9'));
        })"""
    ))


def model_text(page) -> str:
    return page.evaluate(
        """() => {
          const el=[...document.querySelectorAll('button')].find(b =>
            (b.innerText||'').includes('arrow_drop_down') && /Omni|Veo/.test(b.innerText||''));
          return el ? (el.innerText||'').replace(/\\s+/g,' ').trim() : '';
        }"""
    )


def summary_text(page) -> str:
    return page.evaluate(
        """() => (document.querySelector('[settingstriggercontent], .settings-summary')?.innerText||'').replace(/\\s+/g,' ').trim()"""
    )


def configure_vertical(page) -> None:
    g.ensure_project(page)
    page.bring_to_front()
    opened = False
    for _ in range(3):
        g.open_settings(page)
        if panel_open(page):
            opened = True
            break
    if not opened:
        page.screenshot(path=str(OUT / "settings_closed.png"))
        raise RuntimeError("settings closed")
    page.evaluate(
        """() => {
          const b=[...document.querySelectorAll('button')].find(el =>
            (el.innerText||'').trim()==='videocam\\nVideo' || (el.innerText||'').trim()==='Video');
          if (b) b.click();
        }"""
    )
    page.wait_for_timeout(250)
    summary = summary_text(page)
    print(" summary before aspect", summary, flush=True)
    if "crop_9_16" not in summary and "9:16" not in summary:
        if not g.click_button_including(page, "9:16") and not g.click_button_including(page, "crop_9_16"):
            page.screenshot(path=str(OUT / "aspect_miss.png"))
            raise RuntimeError("9:16 missing")
        page.wait_for_timeout(400)
    if not panel_open(page):
        g.open_settings(page)
    now = model_text(page)
    print(" model", now, flush=True)
    if MODEL not in now:
        box = page.evaluate(
            """() => {
              const el=[...document.querySelectorAll('button')].find(b =>
                (b.innerText||'').includes('arrow_drop_down') && /Omni|Veo/.test(b.innerText||''));
              if (!el) return null;
              const r=el.getBoundingClientRect();
              return {x:r.x+r.width/2, y:r.y+r.height/2};
            }"""
        )
        if not box:
            raise RuntimeError("model button hidden")
        page.mouse.click(box["x"], box["y"])
        page.wait_for_timeout(500)
        hit = page.evaluate(
            """(model) => {
              const el=[...document.querySelectorAll('button')].find(b =>
                (b.innerText||'').replace(/\\s+/g,' ').trim().endsWith(model));
              if (!el) return null;
              const r=el.getBoundingClientRect();
              if (r.width<4) return null;
              return {x:r.x+r.width/2, y:r.y+r.height/2};
            }""",
            MODEL,
        )
        if not hit:
            page.screenshot(path=str(OUT / "model_miss.png"))
            raise RuntimeError(f"missing {MODEL}")
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(400)
        if not panel_open(page):
            g.open_settings(page)
    page.evaluate(
        """() => {
          const exact=(t) => [...document.querySelectorAll('button')].find(b => (b.innerText||'').trim()===t);
          const eight=exact('8s');
          if (eight) eight.click();
          const one=exact('x1');
          if (one) one.click();
          const b=[...document.querySelectorAll('button')].find(el =>
            (el.getAttribute('aria-label')||el.innerText||'').includes('Return silent videos'));
          if (b && b.getAttribute('aria-checked') !== 'true') b.click();
        }"""
    )
    page.wait_for_timeout(300)
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    final = summary_text(page)
    now = model_text(page)
    print(" settings", final, "model", now, flush=True)
    if "crop_9_16" not in final and "9:16" not in final:
        raise RuntimeError(f"not vertical: {final}")
    if MODEL not in now:
        raise RuntimeError(f"model is {now}")


def real_chips(page) -> list[dict]:
    return page.evaluate(
        """() => [...document.querySelectorAll('flow-video-ingredient-chip')].map(el => {
          const r=el.getBoundingClientRect();
          return {w:Math.round(r.width), h:Math.round(r.height), t:(el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,120)};
        }).filter(c => c.w>80)"""
    )


def attach_ref(page) -> None:
    if not REF.exists():
        raise FileNotFoundError(REF)
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    chips = real_chips(page)
    print(" chips before", chips, flush=True)
    bad = [c for c in chips if "reject" in c["t"].lower() or "melted" in c["t"].lower() or "sprite" in c["t"].lower()]
    if bad:
        raise RuntimeError(f"rejected frame is attached: {bad}")
    if any("orbit-seedance-reference" in c["t"] for c in chips):
        print(" canonical still already attached", flush=True)
        return
    page.locator('button[aria-label="Add ingredients to the prompt box"]').click()
    page.wait_for_timeout(800)
    uploaded = False
    for label in ("Upload media", "Upload image", "Upload"):
        btn = page.locator(f'button:has-text("{label}")')
        if btn.count() == 0:
            continue
        try:
            with page.expect_file_chooser(timeout=8000) as fc:
                btn.last.click()
            fc.value.set_files(str(REF))
            uploaded = True
            print(" uploaded", label, flush=True)
            break
        except Exception as exc:
            print(" upload miss", label, type(exc).__name__, flush=True)
    if not uploaded:
        fi = page.locator('input[type="file"]')
        if fi.count() == 0:
            page.screenshot(path=str(OUT / "picker_miss.png"))
            raise RuntimeError("could not upload the canonical still")
        fi.last.set_input_files(str(REF))
        print(" uploaded via input", flush=True)
    page.wait_for_timeout(4000)
    how = page.evaluate(
        """() => {
          const labels=[...document.querySelectorAll('*')].filter(e =>
            (e.innerText||'').includes('orbit-seedance-reference-16x9') && (e.innerText||'').length<160
            && e.children.length===0);
          const label=labels[0];
          if (!label) return 'missing-label';
          let card=label;
          for (let i=0;i<8 && card;i++) {
            const img=card.querySelector && card.querySelector('img');
            if (img) { img.click(); return 'clicked-image'; }
            card=card.parentElement;
          }
          label.click();
          return 'clicked-label';
        }"""
    )
    print(" ingredient", how, flush=True)
    page.wait_for_timeout(400)
    page.evaluate(
        """() => {
          const el=[...document.querySelectorAll('button')].find(e =>
            /Add to prompt/i.test(e.innerText||'') && !/Agree/i.test(e.innerText||''));
          if (el) el.click();
        }"""
    )
    page.wait_for_timeout(800)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    chips = real_chips(page)
    print(" chips after", chips, flush=True)
    page.screenshot(path=str(OUT / "attached.png"))
    if not chips:
        raise RuntimeError("Orbit ingredient missing from the prompt")
    if any("reject" in c["t"].lower() or "melted" in c["t"].lower() for c in chips):
        raise RuntimeError(f"rejected frame attached: {chips}")


def video_srcs(page) -> list[str]:
    g.scroll_top(page)
    return page.evaluate(
        """() => [...document.querySelectorAll('video')].map(el => el.currentSrc||el.src||'')
          .filter(s => s && (s.includes('/video/') || s.includes('/asb/')))"""
    )


def uid_of(url: str) -> str:
    found = g.uid_of(url)
    if found:
        return found
    tail = url.split("?")[0].rstrip("/").split("/")[-1]
    return tail[:64]


def gate_frames(paths: list[Path]) -> dict:
    proc = subprocess.run(
        [PY, str(GATE), *[str(p) for p in paths]],
        check=False, capture_output=True, text=True,
    )
    if not proc.stdout.strip():
        raise RuntimeError(proc.stderr[-400:])
    report = json.loads(proc.stdout)
    print(json.dumps({"pass": report["pass"], "reasons": report["reasons"]}), flush=True)
    return report


def sample_plate(silent: Path, tag: str) -> list[Path]:
    # Assembled clock: 0.5s open, 3.0s react, loop near 21s is plate 1.625s.
    frames = []
    for ss, name in (("0.5", "open"), ("1.625", "loop"), ("3.0", "react"), ("5.5", "late")):
        dest = OUT / f"{tag}_{name}.jpg"
        subprocess.run(
            [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-ss", ss, "-i", str(silent), "-frames:v", "1", str(dest)],
            check=True,
        )
        frames.append(dest)
    return frames


def cut_clip(src: Path, ss: float, dur: float, dest: Path) -> None:
    subprocess.run(
        [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{ss:.3f}", "-t", f"{dur:.3f}", "-i", str(src),
            "-an", "-vf", "scale=1080:1920:flags=lanczos,fps=24,format=yuv420p",
            "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", str(dest),
        ],
        check=True,
    )


def assemble(plate: Path) -> None:
    work = OUT / "asm"
    work.mkdir(exist_ok=True)
    cut_clip(plate, 0, 1.583333, work / "open.mp4")
    cut_clip(plate, 1.583333, 4.541667, work / "react.mp4")
    cut_clip(SUN, 0, 8.0, work / "sun.mp4")
    cut_clip(BARE, 0, 5.25, work / "bare.mp4")
    cut_clip(plate, 0, 4.0, work / "loop.mp4")
    listing = work / "list.txt"
    listing.write_text("".join(f"file '{name}'\n" for name in ("open.mp4", "react.mp4", "sun.mp4", "bare.mp4", "loop.mp4")))
    body = work / "body.mp4"
    subprocess.run(
        [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(body)],
        check=True,
    )
    burned = work / "burned.mp4"
    caps = [CAPS / f"cap{i}.png" for i in range(6)] + [CAPS / "title.png"]
    filt = (
        "[0:v][1:v]overlay=enable='between(t,0,1.55)':format=auto[v1];"
        "[v1][2:v]overlay=enable='between(t,1.55,6.10)':format=auto[v2];"
        "[v2][3:v]overlay=enable='between(t,6.10,10.05)':format=auto[v3];"
        "[v3][4:v]overlay=enable='between(t,10.05,14.08)':format=auto[v4];"
        "[v4][5:v]overlay=enable='between(t,14.08,19.37)':format=auto[v5];"
        "[v5][6:v]overlay=enable='between(t,19.37,23.40)':format=auto[v6];"
        "[v6][7:v]overlay=enable='between(t,9.00,14.00)':format=auto[vout]"
    )
    subprocess.run(
        [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(body), *sum([["-i", str(p)] for p in caps], []),
            "-filter_complex", filt, "-map", "[vout]", "-an",
            "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p",
            str(burned),
        ],
        check=True,
    )
    subprocess.run(
        [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(burned), "-i", str(VOICE),
            "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "copy", "-shortest",
            str(FINAL),
        ],
        check=True,
    )
    dur = subprocess.check_output(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(FINAL)],
        text=True,
    ).strip()
    print(" final", FINAL.name, FINAL.stat().st_size, "dur", dur, flush=True)
    seconds = float(dur)
    if not 22 <= seconds <= 27:
        raise RuntimeError(f"duration {seconds} outside 22-27s")


def replace_uat() -> None:
    swift = Path("/tmp/replace_monday.swift")
    subprocess.run(["swift", str(swift), str(FINAL), str(UAT)], check=True)


def main() -> None:
    go = "go" in sys.argv
    seen_path = OUT / "seen.json"
    seen = set(json.loads(seen_path.read_text())) if seen_path.exists() else set()
    fails = 0
    if STATUS.exists():
        old = json.loads(STATUS.read_text())
        fails = int(old.get("fails") or 0)
        if old.get("passed"):
            print("already passed", flush=True)
            return
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(g.CDP)
        page = next(
            pg for ctx in browser.contexts for pg in ctx.pages
            if "d2ebe084-78fb-4d48-9006-2d897c5a80fb" in (pg.url or "")
        )
        page.bring_to_front()
        abort_if_cushion(page)
        configure_vertical(page)
        attach_ref(page)
        abort_if_cushion(page)
        if not go:
            print("PROBE_OK", flush=True)
            return
        while fails < MAX_FAILS:
            before = set(video_srcs(page))
            box = page.locator('[contenteditable="true"]').first
            box.click()
            page.keyboard.press("Meta+A")
            page.keyboard.press("Backspace")
            page.wait_for_timeout(80)
            page.keyboard.insert_text(PROMPT)
            page.locator('button[aria-label="Start generation"]').first.click()
            print("submitted", fails, flush=True)
            src = None
            t0 = time.time()
            while time.time() - t0 < 240:
                page.wait_for_timeout(8000)
                abort_if_cushion(page)
                g.ensure_project(page)
                fresh = []
                for s in video_srcs(page):
                    if s in before:
                        continue
                    uid = uid_of(s)
                    if uid and uid in seen:
                        continue
                    fresh.append(s)
                print(f"  wait {int(time.time()-t0)}s fresh={len(fresh)}", flush=True)
                if fresh:
                    src = fresh[0]
                    break
            if not src:
                fails += 1
                STATUS.write_text(json.dumps({"fails": fails, "passed": False, "reason": "timeout"}, indent=2))
                print("timeout", fails, flush=True)
                continue
            resp = page.request.get(src)
            body = resp.body()
            if resp.status != 200 or b"ftyp" not in body[:64] or len(body) < 100_000:
                fails += 1
                STATUS.write_text(json.dumps({"fails": fails, "passed": False, "reason": "bad-file"}, indent=2))
                print("bad file", resp.status, len(body), flush=True)
                continue
            uid = uid_of(src)
            if uid:
                seen.add(uid)
                seen_path.write_text(json.dumps(sorted(seen), indent=2))
            raw = OUT / f"hold_{fails}.mp4"
            silent = OUT / f"hold_{fails}_silent.mp4"
            raw.write_bytes(body)
            subprocess.run(
                [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw), "-an", "-c:v", "copy", str(silent)],
                check=True,
            )
            frames = sample_plate(silent, f"hold_{fails}")
            report = gate_frames(frames)
            (OUT / f"hold_{fails}_gate.json").write_text(json.dumps(report, indent=2))
            if not report.get("pass"):
                fails += 1
                STATUS.write_text(json.dumps({
                    "fails": fails, "passed": False, "reason": "face-gate", "detail": report.get("reasons"),
                }, indent=2))
                print("reject", report.get("reasons"), flush=True)
                continue
            kept = OUT / "hold_silent.mp4"
            kept.write_bytes(silent.read_bytes())
            assemble(kept)
            # The three frames Ben will watch: open 0.5s, react 3s, loop ~21s.
            qa = []
            for ss, name in (("0.5", "qa_open"), ("3.0", "qa_react"), ("21.0", "qa_loop")):
                dest = OUT / f"{name}.jpg"
                subprocess.run(
                    [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-ss", ss, "-i", str(FINAL), "-frames:v", "1", str(dest)],
                    check=True,
                )
                qa.append(dest)
            final_gate = gate_frames(qa)
            (OUT / "final_gate.json").write_text(json.dumps(final_gate, indent=2))
            if not final_gate.get("pass"):
                fails += 1
                STATUS.write_text(json.dumps({
                    "fails": fails, "passed": False, "reason": "final-face-gate",
                    "detail": final_gate.get("reasons"),
                }, indent=2))
                print("final reject", final_gate.get("reasons"), flush=True)
                continue
            replace_uat()
            STATUS.write_text(json.dumps({"fails": fails, "passed": True, "file": FINAL.name}, indent=2))
            print("UAT_REPLACED", flush=True)
            return
    STATUS.write_text(json.dumps({"fails": fails, "passed": False, "reason": "exhausted"}, indent=2))
    raise SystemExit(2)


if __name__ == "__main__":
    main()
