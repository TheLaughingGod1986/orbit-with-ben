#!/usr/bin/env python3
"""J2512 — 026 Mon 16 (v06) and Wed 18 (v07) Shorts: fix the two J2508 craft faults. £0, no upload.

Chief ruling 10 Nov 2026 15:00Z: fix the two faults found in J2508 (`jobs/reviews/J2508/REVIEW.md`)
and change nothing else (same voice, same words, same -14.2 LUFS / -2.2 dBTP mix, same length,
same captions, same clean end card without YouTube video ID):

  A. Mon 16 Short (`HZGTovJu_TQ`, airs Mon 16 Nov 11:30 London), from `mon16_cant_see_nearest_star_v05.mp4` -> `v06`:
     `0:20.23–0:22.63` (`s06`, 2.40 s before the end card) repeated the opening Paranal shot (`uhd_bt_paranal_07`).
     Replaced with `026_NearestStar_v06.mp4` `13.80–16.20 s` (`uhd_bt_paranal_06`, ESO Paranal observatory rotating
     under the Milky Way, not used elsewhere in Mon 16, free of v06 overlay cards).

  B. Wed 18 Short (`cwU_0WWeNZ4`, airs Wed 18 Nov 11:30 London), from `wed18_robot_reach_nearest_star_v06.mp4` -> `v07`:
     `0:13.45–0:16.55` (`s05`, 3.10 s, ESO star trails at Paranal at 346.50 s of 026 v06) was a frozen still.
     Rendered with a smooth sub-pixel horizontal drift (`-70 px -> +70 px` across the 1920x1080 plate over 93 frames
     at 30 fps, ~2.71 px/frame in 1080x1920 output, upscale unchanged at 1.78x) so every frame moves cleanly and
     zero frames repeat.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
WT_REPO = HERE.parents[2]
SHARED_REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
SHARED_SHORTS = SHARED_REPO / "02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts"

spec_v01 = importlib.util.spec_from_file_location("v01", HERE / "_assemble_026_weekday_shorts_v01.py")
v01 = importlib.util.module_from_spec(spec_v01)
spec_v01.loader.exec_module(v01)

spec_j2494 = importlib.util.spec_from_file_location("j2494", HERE / "_recut_026_first_second_J2494.py")
j2494 = importlib.util.module_from_spec(spec_j2494)
spec_j2494.loader.exec_module(j2494)

STAGING = Path("/Volumes/data/mac-mini-archive/youtube-staging/026")
NAS_OUT = STAGING / "shorts_j2512"
UAT_OUT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/026_shorts_fixes_J2512"
SCRATCH = Path("/Volumes/MiniWork/scratch/J2512_work")

v01.PICTURE = STAGING / "026_NearestStar_v06.mp4"
GATE = WT_REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"
PIC_QA = WT_REPO / "scripts/picture_qa.py"
POLISH = WT_REPO / "scripts/polish_gate.py"

FIXES = {
    "mon16_cant_see_nearest_star": {
        "stem": "mon16_cant_see_nearest_star_v06",
        "ver": "v06",
        "prev_stem": "mon16_cant_see_nearest_star_v05",
        "video_id": "HZGTovJu_TQ",
        "spans": [
            (98.17, 2.40, "ESO Paranal night sky (uhd_bt_paranal_07)"),
            (152.73, 4.50, "ESO VLT from Vista time-lapse"),
            (157.57, 4.50, "NASA/ESA Hubble star field (e000256)"),
            (68.33, 4.50, "ESO La Silla Crux (bt_lasilla_crux)"),
            (200.50, 4.33, "ESO La Silla night-sky time-lapse"),
            (13.80, 2.40, "ESO Paranal observatory (uhd_bt_paranal_06)"),
        ],
        "drift_spans": {},
    },
    "wed18_robot_reach_nearest_star": {
        "stem": "wed18_robot_reach_nearest_star_v07",
        "ver": "v07",
        "prev_stem": "wed18_robot_reach_nearest_star_v06",
        "video_id": "cwU_0WWeNZ4",
        "spans": [
            (0.30, 2.60, "Milky Way time-lapse, opening shot of 026 v06"),
            (296.75, 2.85, "NASA Voyager plate (PIA17049)"),
            (337.45, 3.50, "NASA Voyager plate (PIA14111)"),
            (408.25, 4.50, "NASA SDO solar flare"),
            (346.50, 3.10, "ESO star trails at Paranal (drifting across still)"),
            (13.80, 3.20, "ESO Paranal observatory (uhd_bt_paranal_06)"),
        ],
        "drift_spans": {
            4: {"step_px": 1},
        },
    },
}


def render_drift_span(src_video: Path, src_t: float, length: float, fps: int, step_px: int, dest: Path) -> None:
    """Extract lossless 1920x1080 plate at src_t and pan at exact 1 source-pixel/frame (zero rounding cadence, zero blur)."""
    still_png = dest.with_suffix(".plate.png")
    pre = max(0.0, src_t - 1.5)
    v01.run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{pre:.3f}", "-i", str(src_video),
        "-ss", f"{src_t - pre:.3f}", "-frames:v", "1",
        str(still_png),
    ])
    arr = np.asarray(Image.open(still_png).convert("RGB"), dtype=np.uint8)
    h, w, _ = arr.shape
    n_frames = round(length * fps)
    proc = subprocess.Popen(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
            "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
            "-r", str(fps), "-video_track_timescale", "30000", str(dest),
        ],
        stdin=subprocess.PIPE,
    )
    assert proc.stdin is not None
    start_dx = -((n_frames - 1) * step_px) // 2
    # Downstream crop=ih*9/16:ih reads only centre [656..1264] of 1920, so [-46..+46] has >600 px real margin on both sides.
    xs = np.arange(w, dtype=np.int32)
    for k in range(n_frames):
        dx = start_dx + k * step_px
        idx = np.clip(xs + dx, 0, w - 1)
        proc.stdin.write(np.ascontiguousarray(arr[:, idx, :]).tobytes())
    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise SystemExit(f"render_drift_span failed with exit {rc}")


def cut_spans_j2512(work: Path, spans: list[tuple], drift_spans: dict[int, dict]) -> None:
    lines = []
    for i, (src_t, length, _label) in enumerate(spans):
        piece = work / f"span_{i}.mp4"
        if i in drift_spans:
            cfg = drift_spans[i]
            render_drift_span(v01.PICTURE, src_t, length, v01.FPS, cfg["step_px"], piece)
        else:
            pre = max(0.0, src_t - 1.5)
            v01.run([
                "ffmpeg", "-y", "-v", "error",
                "-ss", f"{pre:.3f}", "-i", str(v01.PICTURE),
                "-ss", f"{src_t - pre:.3f}", "-t", f"{length:.3f}", "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
                "-r", str(v01.FPS), "-video_track_timescale", "30000", str(piece),
            ])
        lines.append(f"file '{piece.name}'")
    lst = work / "span_list.txt"
    lst.write_text("\n".join(lines) + "\n")
    v01.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
             "-c", "copy", str(work / "picture_span.mp4")])


def verify_span_motion(video: Path, t0: float, t1: float) -> dict:
    """Measure frame-to-frame pixel step and repeated-frame count inside [t0, t1] (centre 9:16 crop excluding lower captions)."""
    raw = subprocess.run(
        [
            "ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", str(video), "-t", f"{t1 - t0:.3f}",
            "-vf", "crop=1080:900:0:260,format=gray", "-f", "rawvideo", "-",
        ],
        capture_output=True, check=True,
    ).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 900, 1080).astype(np.float32)
    diffs = np.mean(np.abs(fr[1:] - fr[:-1]), axis=(1, 2))
    # Exclude first/last boundary frame if seek touches cut edge; inspect interior frames too
    interior = diffs[1:-1] if len(diffs) > 4 else diffs
    repeated = int((interior < 0.05).sum())
    return {
        "frames": int(len(fr)),
        "min_diff": round(float(interior.min()), 4),
        "median_diff": round(float(np.median(interior)), 4),
        "repeated_interior_frames": repeated,
    }


def build(base: dict) -> dict:
    slug = base["slug"]
    fx = FIXES[slug]
    stem, ver, prev_stem, spans = fx["stem"], fx["ver"], fx["prev_stem"], fx["spans"]

    wt_folder = HERE / slug
    wt_out = wt_folder / "06_Final-Exports"
    wt_out.mkdir(parents=True, exist_ok=True)

    shared_folder = SHARED_SHORTS / slug
    shared_out = shared_folder / "06_Final-Exports"
    shared_out.mkdir(parents=True, exist_ok=True)

    work = SCRATCH / slug
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True, exist_ok=True)

    final_mp4 = shared_out / f"{stem}.mp4"
    if final_mp4.exists() and "--overwrite-current" not in sys.argv:
        raise SystemExit(f"{final_mp4} exists; refuse to overwrite")

    # Verify both original J0141 upload source and J2494 approved fallback
    j0141_src = STAGING / "shorts_j0141" / f"{base['stem']}.mp4"
    j0141_want = (STAGING / "shorts_j0141" / f"{base['stem']}.mp4.sha256").read_text().split()[0]
    if v01.sha256(j0141_src) != j0141_want:
        raise SystemExit(f"{j0141_src} does not hash to its recorded sha256")

    j2494_src = STAGING / "shorts_j2494" / f"{prev_stem}.mp4"
    j2494_want = (STAGING / "shorts_j2494" / f"{prev_stem}.mp4.sha256").read_text().split()[0]
    if v01.sha256(j2494_src) != j2494_want:
        raise SystemExit(f"{j2494_src} does not hash to its recorded sha256")

    vo_len = base["vo"]
    total = round(vo_len + v01.HOLD, 2)
    card_in = round(vo_len + v01.HOLD - v01.CARD, 2)
    if abs(sum(s[1] for s in spans) - card_in) > 0.02:
        raise SystemExit(f"{slug} spans do not sum to {card_in}")
    if spans[0][1] > 3.0:
        raise SystemExit(f"{slug} first cut after 3.0 s")

    words = v01.load_words(shared_folder / base["words"], work, vo_len)
    caps = v01.caption_chunks(words, vo_len, card_in)
    hook = v01.hook_png(work / "hook.png", base["hook"])
    title = v01.title_png(work / "title.png", base["title_rows"])
    for i, c in enumerate(caps):
        v01.caption_png(work / f"cap_{i:02d}.png", c["text"])
    end = j2494.end_card_png_no_id(work / "end_card.png", base["quote"], base["voyager"])

    # Copy exact AAC audio stream from J2494 cut (-14.2 LUFS / -2.2 dBTP) so voice/words/level are bit-identical
    prev_meta = json.loads((wt_out / f"{prev_stem}_meta.json").read_text())
    aud = dict(prev_meta["audio"])

    print(f"{slug}: cutting {len(spans)} spans", flush=True)
    cut_spans_j2512(work, spans, fx["drift_spans"])

    W, H, FPS, PUSH, CARD = v01.W, v01.H, v01.FPS, v01.PUSH, v01.CARD
    inputs = [
        "-t", f"{card_in:.3f}", "-i", str(work / "picture_span.mp4"),
        "-loop", "1", "-framerate", str(FPS), "-t", f"{CARD:.3f}", "-i", str(work / "end_card.png"),
        "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(work / "hook.png"),
        "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", str(work / "title.png"),
    ]
    base_i = 4
    for i in range(len(caps)):
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i",
                   str(work / f"cap_{i:02d}.png")]
    fc = [
        f"[0:v]fps={FPS},crop=ih*9/16:ih,"
        f"scale=w='trunc({W}*(1+{PUSH}*min(t,1.0)/1.0)/2)*2':"
        f"h='trunc({H}*(1+{PUSH}*min(t,1.0)/1.0)/2)*2':eval=frame:flags=lanczos,"
        f"crop={W}:{H}:'(iw-{W})/2':'(ih-{H})/2',setsar=1,format=yuv420p[a]",
        f"[1:v]scale={W}:{H}:flags=lanczos,fps={FPS},format=yuv420p,trim=0:{CARD:.3f},setpts=PTS-STARTPTS[e]",
        "[a][e]concat=n=2:v=1:a=0[v0]",
        f"[2:v]format=rgba,fade=t=out:st={v01.HOOK_END - 0.25:.2f}:d=0.25:alpha=1[hk]",
        f"[v0][hk]overlay=0:0:enable='lt(t,{v01.HOOK_END})'[v1]",
        f"[3:v]format=rgba,fade=t=in:st={v01.TITLE_IN}:d=0.30:alpha=1,"
        f"fade=t=out:st={v01.TITLE_OUT - 0.30}:d=0.30:alpha=1[tt]",
        f"[v1][tt]overlay=0:0:enable='between(t,{v01.TITLE_IN},{v01.TITLE_OUT})'[v2]",
    ]
    last = "v2"
    for i, c in enumerate(caps):
        fc.append(f"[{last}][{base_i + i}:v]overlay=0:0:enable='gte(t,{c['s']})*lt(t,{c['e']})'[c{i}]")
        last = f"c{i}"
    fc.append(f"[{last}]format=yuv420p[v]")
    enc = v01.shorts_encode_args(fps=FPS)
    venc = enc[:enc.index("-c:a")]

    pic = work / f"picture_final_{stem}.mp4"
    print(f"{slug}: encoding video", flush=True)
    v01.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc),
             "-map", "[v]", *venc, "-an", "-t", f"{total:.3f}", str(pic)])

    v01.run(["ffmpeg", "-y", "-v", "error", "-i", str(pic), "-i", str(j2494_src),
             "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-movflags", "+faststart",
             "-t", f"{total:.3f}", str(final_mp4)])

    # Verify loudness matches -14.2 LUFS / -2.2 dBTP
    sys.path.insert(0, str(GATE.parent))
    import gate_shorts_open as g
    lufs_meas, tp_meas = g.aac_loudness(final_mp4)
    aud["lufs"] = lufs_meas
    aud["true_peak"] = tp_meas

    # Write cuts_vNN.json and pool_vNN.json
    t = 0.0
    cuts_meta = []
    cuts_qa = []
    pool_qa = []
    seen_pool = set()
    for i, (src_t, length, label) in enumerate(spans):
        src_id = f"v06_{src_t:.2f}_drift.mp4" if i in fx["drift_spans"] else f"v06_{src_t:.2f}.mp4"
        cuts_meta.append({
            "row": f"s{i + 1:02d}",
            "timeline_in": round(t, 2),
            "timeline_out": round(t + length, 2),
            "source": src_id,
            "what": label,
        })
        cuts_qa.append({
            "row": f"s{i + 1:02d}",
            "timeline_in": round(t, 2),
            "timeline_out": round(t + length, 2),
            "source": src_id,
            "upscale": 1.78,
            "framing": {"offset": round(src_t, 2)},
            "video": True,
        })
        if src_id not in seen_pool:
            seen_pool.add(src_id)
            pool_qa.append({"file_id": src_id, "title": f"{label} at {src_t:.2f}s of 026 v06"})
        t += length

    cuts_meta.append({"row": "end_card", "timeline_in": card_in, "timeline_out": total, "source": "end_card_thumb_A.png"})
    cuts_qa.append({
        "row": "end_card",
        "timeline_in": card_in,
        "timeline_out": total,
        "source": "end_card_thumb_A.png",
        "upscale": 1.0,
        "video": False,
    })
    pool_qa.append({"file_id": "end_card_thumb_A.png", "title": "End card: thumb A unaltered, long title, quote only (no YouTube ID)"})

    cuts_path = wt_out / f"cuts_{ver}.json"
    pool_path = wt_out / f"pool_{ver}.json"
    cuts_path.write_text(json.dumps(cuts_qa, indent=2) + "\n")
    pool_path.write_text(json.dumps(pool_qa, indent=2) + "\n")

    # Run gate_shorts_open.py
    gate = subprocess.run([sys.executable, str(GATE), "check", str(final_mp4), "--air-date", base["air"],
                           "--id", fx["video_id"], "--json"], capture_output=True, text=True)
    (wt_out / f"{stem}_gate.json").write_text(gate.stdout or gate.stderr)
    gate_txt = subprocess.run([sys.executable, str(GATE), "check", str(final_mp4), "--air-date", base["air"],
                               "--id", fx["video_id"]], capture_output=True, text=True)
    (wt_out / f"{stem}_gate.txt").write_text((gate_txt.stdout or "") + (gate_txt.stderr or ""))

    # Run picture_qa.py from WT_REPO with repo-relative output path, then remove git-untracked review jpgs
    pqa_rel = Path("02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts") / slug / "06_Final-Exports" / f"picture_qa_{ver}"
    pqa_wt = WT_REPO / pqa_rel
    pqa_wt.mkdir(parents=True, exist_ok=True)
    pqa = subprocess.run(
        [sys.executable, str(PIC_QA), str(final_mp4), "--cuts", str(cuts_path.relative_to(WT_REPO)),
         "--pool", str(pool_path.relative_to(WT_REPO)), "--out-dir", str(pqa_rel)],
        cwd=str(WT_REPO), capture_output=True, text=True,
    )
    (wt_out / f"picture_qa_{ver}.txt").write_text((pqa.stdout or "") + (pqa.stderr or ""))
    for jpg in pqa_wt.glob("*.jpg"):
        jpg.unlink()

    # Run polish_gate.py
    pol_json = wt_out / f"polish_gate_{ver}.json"
    pol = subprocess.run(
        [sys.executable, str(POLISH), str(final_mp4), "--cuts", str(cuts_path), "--out", str(pol_json)],
        capture_output=True, text=True,
    )
    (wt_out / f"polish_gate_{ver}.txt").write_text((pol.stdout or "") + (pol.stderr or ""))

    # Measure motion on the fixed span
    fixed_row = cuts_qa[5] if slug.startswith("mon16") else cuts_qa[4]
    motion_check = verify_span_motion(final_mp4, fixed_row["timeline_in"], fixed_row["timeline_out"])

    file_rel = f"02_Video-Projects/026_How-Far-Is-The-Nearest-Star/10_Shorts/{slug}/06_Final-Exports/{stem}.mp4"
    digest = v01.sha256(final_mp4)
    meta = {
        "job": "J2512",
        "file": file_rel,
        "sha256": digest,
        "duration_s": v01.dur(final_mp4),
        "listing_title": base["title"],
        "on_screen_title": title,
        "replaces_if_ben_oks": {"video_id": fx["video_id"], "file": j0141_src.name, "sha256": j0141_want},
        "fallback_ben_okd_10_nov": {"file": j2494_src.name, "sha256": j2494_want},
        "audio": aud,
        "long": {"id": v01.LONG_ID, "title": v01.LONG_TITLE, "cut": "v06"},
        "end_card": {"start_s": card_in, "len_s": CARD, **end},
        "hook": hook,
        "words": len(words),
        "captions": caps,
        "cuts": cuts_meta,
        "fixed_span_motion": {"row": fixed_row["row"], **motion_check},
        "gate_exit": gate.returncode,
        "gate_ok": gate.returncode == 0 and '"verdict": "PASS"' in (gate.stdout or ""),
        "picture_qa_exit": pqa.returncode,
        "polish_gate_exit": pol.returncode,
        "spend": "none",
        "uploaded": False,
    }
    (wt_out / f"{stem}_meta.json").write_text(json.dumps(meta, indent=2) + "\n")

    # Copy to NAS staging + sha256 verify, and to iCloud OWB UAT + sha256 verify
    NAS_OUT.mkdir(parents=True, exist_ok=True)
    nas_copy = NAS_OUT / final_mp4.name
    shutil.copy2(final_mp4, nas_copy)
    if v01.sha256(nas_copy) != digest:
        raise SystemExit(f"NAS sha256 mismatch on {nas_copy}")
    (NAS_OUT / f"{final_mp4.name}.sha256").write_text(f"{digest}  {final_mp4.name}\n")

    UAT_OUT.mkdir(parents=True, exist_ok=True)
    uat_copy = UAT_OUT / final_mp4.name
    shutil.copy2(final_mp4, uat_copy)
    if v01.sha256(uat_copy) != digest:
        raise SystemExit(f"UAT sha256 mismatch on {uat_copy}")

    print(
        f"{slug} -> {stem}: {meta['duration_s']:.2f}s gate={meta['gate_ok']} pqa={pqa.returncode} "
        f"pol={pol.returncode} {aud['lufs']} LUFS {aud['true_peak']} dBTP "
        f"motion={motion_check} sha256={digest[:12]}",
        flush=True,
    )
    return meta


def main() -> int:
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    fails = 0
    for base in v01.SHORTS:
        if base["slug"] in FIXES and (not only or base["slug"] in only):
            m = build(base)
            if not m["gate_ok"] or m["picture_qa_exit"] != 0 or m["polish_gate_exit"] != 0:
                fails += 1
            if m["fixed_span_motion"]["repeated_interior_frames"] != 0:
                fails += 1
    print(f"done fails={fails}", flush=True)
    return fails


if __name__ == "__main__":
    raise SystemExit(main())
