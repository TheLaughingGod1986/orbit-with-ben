#!/usr/bin/env python3
"""J1199 S6 Titan v11. Chief scope 5 Nov 2026 (PR558). £0. No upload.

Opening and forward loop preroll come only from
S6_flow_t2_silent.mp4 sha256 2218c817e96a1444da45a7130e5cc8d0cc8824a322f4a16ed6078c85562dad2a.
Frames 28..91 are the opening (64/24 s). Frames 0..27 are the tail (28/24 s).
Crop 720:405:0:875, scale to 1080x608 at y=656, feathered over a moving blur
of the same crop (gblur sigma 28). Locked v02 VO, Stay-line already removed.
Does not touch v01 or v02.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
AUDIT = REPO / "00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10"
SRC = Path("/Users/benjaminoats/_desk/handoff/J1208/flow-20261105/S6_flow_t2_silent.mp4")
SRC_SHA = "2218c817e96a1444da45a7130e5cc8d0cc8824a322f4a16ed6078c85562dad2a"
VO = Path("/Volumes/data/mac-mini-archive/scratch/J1199/s6_v02/vo_v02.wav")
VO_SHA = "1298d4fbbe2be1d633546dd348212383c09cf868eb9c518bdbcd06cdd30a0e53"
META_V02 = AUDIT / "06_Final-Exports/owb_sa_s6_titan_v02_meta.json"
PLATES = Path("/Volumes/data/mac-mini-archive/scratch/J1199/plates")
WORK = Path("/private/tmp/J1199-s6-v11")
OUT = AUDIT / "06_Final-Exports"
QA = AUDIT / "qa_shorts_v01/owb_sa_s6_titan_v11"
STEM = "owb_sa_s6_titan_v11"
FPS = 24
W, H = 1080, 1920
OPEN_N, TAIL_N = 64, 28  # source frames
TOTAL_FRAMES = 18 * FPS  # 432
BODY = [
    ("p2", "s6_titan/PIA06230.jpg", "fit", 1.00, 1.14, 0.50, 0.50, -0.08, 0.06, 120),
    ("p3", "s6_titan/PIA09739.jpg", "cover", 1.10, 1.30, 0.40, 0.35, 0.20, 0.12, 120),
    ("p4", "s6_titan/PIA21625.jpg", "fit", 1.00, 1.14, 0.50, 0.50, -0.06, -0.08, 100),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list) -> None:
    subprocess.run([str(c) for c in cmd], check=True)


def load_mod():
    path = AUDIT / "_assemble_s5_s6_v02.py"
    spec = importlib.util.spec_from_file_location("s5s6_v02", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def encode_frames(frames, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    enc = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
         "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-an", str(path)],
        stdin=subprocess.PIPE,
    )
    for im in frames:
        enc.stdin.write(im.convert("RGB").tobytes())
    enc.stdin.close()
    if enc.wait():
        raise SystemExit(f"encode failed {path}")


def nb_frames(path: Path) -> int:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
         "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip()
    return int(out)


def build_cycle(cycle: Path) -> None:
    # One filter over frames 0..91 so the f27->f28 seam stays contiguous.
    filt = (
        "[0:v]trim=start_frame=0:end_frame=92,setpts=PTS-STARTPTS,split=2[bg][fg];"
        "[bg]crop=720:405:0:875,scale=1080:1920:flags=lanczos,gblur=sigma=28,setsar=1[b];"
        "[fg]crop=720:405:0:875,scale=1080:608:flags=lanczos,format=rgba,"
        "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
        "a='if(lt(Y,72),255*Y/72,if(gt(Y,H-73),255*(H-1-Y)/72,255))'[f];"
        "[b][f]overlay=0:656:format=auto,format=yuv420p[v]"
    )
    run(["ffmpeg", "-y", "-v", "error", "-i", SRC, "-filter_complex", filt,
         "-map", "[v]", "-r", str(FPS), "-an", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", "-pix_fmt", "yuv420p", cycle])
    got = nb_frames(cycle)
    if got != OPEN_N + TAIL_N:
        raise SystemExit(f"cycle has {got} frames, wanted {OPEN_N + TAIL_N}")


def split_cycle(cycle: Path, open_path: Path, tail_path: Path) -> None:
    run(["ffmpeg", "-y", "-v", "error", "-i", cycle,
         "-vf", f"select='lt(n\\,{TAIL_N})',setpts=N/{FPS}/TB",
         "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
         tail_path])
    run(["ffmpeg", "-y", "-v", "error", "-i", cycle,
         "-vf", f"select='gte(n\\,{TAIL_N})',setpts=N/{FPS}/TB",
         "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
         open_path])
    if nb_frames(tail_path) != TAIL_N or nb_frames(open_path) != OPEN_N:
        raise SystemExit(
            f"split counts tail={nb_frames(tail_path)} open={nb_frames(open_path)}"
        )


def composite(base, picture: Path, overlays: list, out: Path) -> None:
    frames = round(base.dur(picture) * FPS)
    inputs: list[str] = ["-i", str(picture)]
    for p, _, _ in overlays:
        if p.suffix == ".png":
            inputs += ["-loop", "1", "-framerate", str(FPS), "-i", str(p)]
        else:
            inputs += ["-i", str(p)]
    parts, prev = [], "[0:v]"
    for i, (p, a, b) in enumerate(overlays, start=1):
        tag = f"[v{i}]"
        if p.suffix == ".mov":
            parts.append(
                f"[{i}:v]setpts=PTS+{a:.3f}/TB[d{i}];{prev}[d{i}]overlay=enable='between(t,{a:.3f},{b:.3f})'{tag}"
            )
        else:
            parts.append(f"{prev}[{i}:v]overlay=enable='between(t,{a:.3f},{b:.3f})'{tag}")
        prev = tag
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(parts),
         "-map", prev, "-frames:v", str(frames), "-r", str(FPS),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-pix_fmt", "yuv420p", "-an", out])


def main() -> None:
    if sha256(SRC) != SRC_SHA:
        raise SystemExit("source hash mismatch")
    if sha256(VO) != VO_SHA:
        raise SystemExit("locked VO hash mismatch")
    meta_v02 = json.loads(META_V02.read_text())
    words = meta_v02["captions"]
    spoken = " ".join(w["word"] for w in words)
    low = spoken.lower().replace("i’ll", "i'll")
    if "stay" in low or "i'll show" in low or spoken != meta_v02["spoken"]:
        raise SystemExit(f"captions drifted: {spoken}")
    last_end = float(words[-1]["end"])
    total = 18.0
    if abs(last_end - 16.13) > 0.02:
        raise SystemExit(f"last word {last_end} is not the locked 16.13s")

    mod = load_mod()
    base = mod.base
    uranus = mod.uranus
    WORK.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)

    cycle = WORK / "cycle_f0_91.mp4"
    open_path = WORK / "s6_open_illustration.mp4"
    tail_path = WORK / "s6_preroll_illustration.mp4"
    print("cycle", flush=True)
    build_cycle(cycle)
    split_cycle(cycle, open_path, tail_path)

    counts = [OPEN_N, 120, 120, 100, TAIL_N]
    if sum(counts) != TOTAL_FRAMES:
        raise SystemExit(f"frame budget {sum(counts)} != {TOTAL_FRAMES}")
    parts = [open_path]
    cuts = []
    frame_i = 0
    open_src = str(open_path)
    cuts.append({
        "row": 1,
        "timeline_in": 0.0,
        "timeline_out": round(OPEN_N / FPS, 6),
        "source": open_src,
        "video": True,
        "upscale": 1.5,
        "zoom": "source frames 28-91, crop 720:405:0:875, band y656 feathered",
        "max_upscale": 1.5,
        "framing": {"offset": 28 / FPS},
    })
    frame_i = OPEN_N
    for name, rel, mode, z0, z1, cx, cy, px, py, n in BODY:
        path = WORK / f"seg_{name}.mp4"
        plate = PLATES / rel
        print(f"  {name} {n} frames mode={mode}", flush=True)
        if mode == "cover":
            gen = mod.cover_frames(plate, n, z0, z1, cx, cy, px, py, phase0=0)
        else:
            gen = mod.fit_frames(plate, n, z0, z1, cx, cy, px, py, phase0=0)
        encode_frames(gen, path)
        del gen
        a, b = frame_i / FPS, (frame_i + n) / FPS
        parts.append(path)
        cuts.append({
            "row": len(cuts) + 1,
            "timeline_in": round(a, 6),
            "timeline_out": round(b, 6),
            "source": str(plate),
            "upscale": 2.2,
            "zoom": "push/pan",
            "max_upscale": 2.2,
            "framing": {"offset": round(b - a, 3)},
        })
        frame_i += n
    parts.append(tail_path)
    a, b = frame_i / FPS, (frame_i + TAIL_N) / FPS
    cuts.append({
        "row": 5,
        "timeline_in": round(a, 6),
        "timeline_out": round(b, 6),
        "source": str(tail_path),
        "video": True,
        "upscale": 1.5,
        "zoom": "source frames 0-27 forward preroll, same crop and feather",
        "max_upscale": 1.5,
        "framing": {"offset": 0.0},
        "role": "forward_preroll",
    })
    if abs(b - total) > 1e-6:
        raise SystemExit(f"timeline ends {b} not {total}")
    if cuts[0]["timeline_out"] > 3.0:
        raise SystemExit("first cut after 3.0s")

    main_v = WORK / "main.mp4"
    uranus.concat(parts, main_v)
    picture = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", main_v,
         "-vf", "noise=alls=4:allf=t,format=yuv420p",
         "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-an", picture])

    spec = mod.SHORTS["s6"]
    hook_spec = {"title": spec["title"], "hook": spec["hook"], "yellow": spec["yellow"]}
    ov = WORK / "ov"
    ov.mkdir(exist_ok=True)
    hook_p, title_p = ov / "hook.png", ov / "title.png"
    base.save_png(base.hook_png(hook_spec), hook_p)
    base.save_png(base.title_png(hook_spec), title_p)
    overlays = [(hook_p, 0.0, base.HOOK_END), (title_p, base.TITLE[0], base.TITLE[1])]
    for i, (a0, b0, im) in enumerate(base.caption_pngs(words, total)):
        p = ov / f"cap_{i:02d}.png"
        base.save_png(im, p)
        overlays.append((p, a0, b0))
    ov_word = next(w for w in words if w["word"].lower().startswith("2034"))
    ov_window = (round(ov_word["start"] - 0.15, 3), round(min(ov_word["end"] + 0.6, cuts[-1]["timeline_in"] - 0.05), 3))
    if ov_window[0] < 14.0 or ov_window[1] <= ov_window[0]:
        raise SystemExit(f"fact card would hit the title or invert: {ov_window}")
    data = ov / "fact.mov"
    mod.fact_card(ov_window, spec["ov_lines"], data)
    overlays.append((data, ov_window[0], ov_window[1]))

    comp = WORK / "comp.mp4"
    print("composite", flush=True)
    composite(base, picture, overlays, comp)
    vo_s, bed_s, sfx_s = uranus.stems(WORK, VO, total, last_end, ov_window[0] + 0.05)

    sys.path.insert(0, str(REPO / "04_Audio/tools"))
    from orbit_cfr_delivery import shorts_encode_args
    enc_args = shorts_encode_args(fps=FPS)
    final = OUT / f"{STEM}.mp4"
    OUT.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-i", comp, "-i", vo_s, "-i", bed_s, "-i", sfx_s,
         "-filter_complex",
         "[1:a]volume=1.35[v];[v][2:a][3:a]amix=inputs=3:duration=first:normalize=0,"
         "loudnorm=I=-14.0:TP=-1.6:LRA=11,"
         "alimiter=limit=0.82:attack=7:release=60:level=false,aresample=48000[a]",
         "-map", "0:v", "-map", "[a]", *enc_args, "-t", f"{total:.3f}", final])
    levels = uranus.measure_lufs(final)
    print("levels", levels, flush=True)
    tries = 0
    while tries < 5 and (levels["tp"] > -1.55 or levels["lufs"] < -14.5 or levels["lufs"] > -13.5):
        tries += 1
        tmp = WORK / f"final_fix{tries}.mp4"
        if levels["tp"] > -1.55 and levels["lufs"] >= -14.4:
            af = "volume=0.985,alimiter=limit=0.80:attack=5:release=50:level=false"
        elif levels["lufs"] < -14.5:
            af = "volume=1.08,alimiter=limit=0.82:attack=7:release=60:level=false"
        else:
            af = "volume=0.96,alimiter=limit=0.80:attack=5:release=50:level=false"
        run(["ffmpeg", "-y", "-v", "error", "-i", final, "-af", af,
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", tmp])
        shutil.move(tmp, final)
        levels = uranus.measure_lufs(final)
        print(f"levels after tweak {tries}", levels, flush=True)

    phone = OUT / f"{STEM}_PHONE.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", final, "-vf", "scale=720:1280:flags=lanczos",
         "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", phone])
    frames = OUT / f"{STEM}_frames.jpg"
    mids = [(c["timeline_in"] + c["timeline_out"]) / 2 for c in cuts]
    base.sheet(final, [0.0, 0.5, 1.2, 2.8, 5.0, 9.5, 12.0, last_end, total - 0.08] + mids, frames)
    sheet2 = OUT / f"{STEM}_2fps.jpg"
    uranus.sheet_2fps(final, sheet2)

    digest = sha256(final)
    meta = {
        "job": "J1199",
        "short": "s6",
        "version": "v11",
        "air_date": "2026-11-10",
        "youtube_id": "RLSJm59OSzI",
        "title_on_screen": " ".join(spec["title"]),
        "package_title": spec["package_title"],
        "file": str(final.relative_to(REPO)),
        "phone": str(phone.relative_to(REPO)),
        "frames": str(frames.relative_to(REPO)),
        "sheet_2fps": str(sheet2.relative_to(REPO)),
        "sha256": digest,
        "duration_s": round(base.dur(final), 3),
        "vo": str(VO),
        "vo_sha256": VO_SHA,
        "words": len(words),
        "last_word_end_s": last_end,
        "spoken": spoken,
        "captions": words,
        "hook": meta_v02["hook"],
        "title_window_s": [9.0, 14.0],
        "overlay": {"kind": "fact", "window": list(ov_window), "lines": ["2034", "LANDS"]},
        "cuts": cuts,
        "loudness": levels,
        "opening": {
            "source": str(SRC),
            "source_sha256": SRC_SHA,
            "opening_frames": "28..91",
            "preroll_frames": "0..27",
            "crop": "720:405:0:875",
            "scale": "1080x608",
            "band_y": 656,
            "blur": "gblur sigma 28",
            "feather_px": 72,
            "disclosure": "Artist's illustration of Titan haze and low-relief terrain. Not NASA footage. Not a measured landing site. No Short corner credit.",
        },
        "brief": {
            "frame0_source": "S6_flow_t2_silent frames 28-91, centre band, feathered blur fill",
            "first_word_onset_s": words[0]["start"],
            "first_cut_s": cuts[0]["timeline_out"],
            "last_word_to_loop_s": round(total - last_end, 3),
            "meta_promise": "no",
            "longest_plate_s": round(max(c["timeline_out"] - c["timeline_in"] for c in cuts), 3),
        },
        "audio": {
            "bed": str(base.BED.relative_to(REPO)),
            "sfx": f"rumble at 0 s, tick at {ov_window[0] + 0.05:.2f} s",
            "stems": {"vo": str(vo_s), "bed": str(bed_s), "sfx": str(sfx_s)},
            "mix": "-14 LUFS target, loudnorm",
        },
        "grain": "noise=alls=4:allf=t",
        "spend": "none",
        "loop": "forward: tail is source frames 0-27, opening is frames 28-91, seam f27 to f28",
        "preserves": "v01 and v02 files and manifests untouched",
        "rule8": "frame 0 moving illustration + Stay-line already excised; no new VO",
    }
    meta_path = OUT / f"{STEM}_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    (QA / f"cuts_{STEM}.json").write_text(json.dumps(cuts, indent=2) + "\n")
    pool = {
        "items": [
            {"file": open_path.name, "title": "artist's illustration of Titan haze and terrain"},
            {"file": tail_path.name, "title": "artist's illustration of Titan haze and terrain"},
            {"file": "PIA06230.jpg", "title": "Cassini image of Titan"},
            {"file": "PIA09739.jpg", "title": "Cassini image of Titan"},
            {"file": "PIA21625.jpg", "title": "Cassini image of Titan"},
        ]
    }
    pool_path = QA / f"pool_{STEM}.json"
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(final), "--air-date", "2026-11-10", "--id", "RLSJm59OSzI", "--vo", str(vo_s)],
        capture_output=True, text=True)
    (OUT / f"{STEM}_gate.txt").write_text(gate.stdout + gate.stderr)
    level = subprocess.run(
        [sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
         "--vo", str(vo_s), "--sfx", str(sfx_s), "--bed", str(bed_s),
         "--minutes", f"{total / 60:.4f}"],
        capture_output=True, text=True)
    (OUT / f"{STEM}_sfx_level.txt").write_text(level.stdout + level.stderr)
    polish_cuts = WORK / "polish_cuts.json"
    polish_cuts.write_text(json.dumps(cuts, indent=2))
    polish = subprocess.run(
        [sys.executable, str(REPO / "scripts/polish_gate.py"), str(final),
         "--cuts", str(polish_cuts), "--out", str(WORK / "polish_gate.json")],
        capture_output=True, text=True)
    (OUT / f"{STEM}_polish.txt").write_text(polish.stdout + polish.stderr)
    others = []
    for p in (REPO / "02_Video-Projects").glob("*/05_Music/*"):
        if p.suffix.lower() in {".mp3", ".wav", ".m4a", ".aac"} and p.name != base.BED.name:
            others.append(str(p))
    music = subprocess.run(
        [sys.executable, str(REPO / "scripts/music_gate.py"), str(AUDIT),
         "--bed", str(base.BED), "--video", str(final),
         "--out", str(WORK / "music_gate.json"), "--others", *others],
        capture_output=True, text=True)
    (OUT / f"{STEM}_music_gate.txt").write_text(music.stdout + music.stderr)
    picture_qa = subprocess.run(
        [sys.executable, str(REPO / "scripts/picture_qa.py"), str(final),
         "--cuts", str(QA / f"cuts_{STEM}.json"),
         "--pool", str(pool_path),
         "--out-dir", str(QA)],
        capture_output=True, text=True)
    (OUT / f"{STEM}_picture_qa.txt").write_text(picture_qa.stdout + picture_qa.stderr)
    sys.path.insert(0, str(REPO / "scripts"))
    from short_c37 import finish_scan
    try:
        m = finish_scan(final)
        loop_txt = (
            f"PASS loop_diff_masked {m['loop_diff_masked']:.2f} open_median_step {m['open_median_step']:.2f} "
            f"head_matches {m['head_matches']}\n"
        )
        loop_rc = 0
    except SystemExit as e:
        loop_txt = f"FAIL {e}\n"
        loop_rc = 1
    (OUT / f"{STEM}_loop.txt").write_text(loop_txt)
    print(f"gate={gate.returncode} level={level.returncode} polish={polish.returncode} "
          f"music={music.returncode} picture_qa={picture_qa.returncode} loop={loop_rc}", flush=True)
    print(gate.stdout)
    print(polish.stdout)
    print(picture_qa.stdout)
    print(loop_txt)
    print("SHA", digest, flush=True)
    fails = []
    if gate.returncode:
        fails.append(f"gate {gate.returncode}")
    if level.returncode:
        fails.append(f"sfx {level.returncode}")
    if polish.returncode:
        fails.append(f"polish {polish.returncode}")
    if music.returncode:
        fails.append(f"music {music.returncode}")
    if picture_qa.returncode:
        fails.append(f"picture_qa {picture_qa.returncode}")
    if loop_rc:
        fails.append("loop")
    if fails:
        raise SystemExit("GATES FAIL: " + ", ".join(fails))

    delivered = [final, phone, frames, sheet2, meta_path,
                 OUT / f"{STEM}_gate.txt", OUT / f"{STEM}_loop.txt",
                 OUT / f"{STEM}_polish.txt", OUT / f"{STEM}_music_gate.txt",
                 OUT / f"{STEM}_sfx_level.txt", OUT / f"{STEM}_picture_qa.txt"]
    for dest in (
        Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/standalone_shorts_s6_v11",
        Path("/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/OWB UAT/standalone_shorts_s6_v11"),
    ):
        dest.mkdir(parents=True, exist_ok=True)
        manifest = []
        for src_f in delivered:
            shutil.copy2(src_f, dest / src_f.name)
            digest_d = sha256(dest / src_f.name)
            if digest_d != sha256(src_f):
                raise SystemExit(f"sha mismatch {dest / src_f.name}")
            manifest.append(f"{digest_d}  {src_f.name}")
        (dest / "MANIFEST.sha256").write_text("\n".join(manifest) + "\n")
        print(f"copied {dest}", flush=True)
    print("DONE", digest, flush=True)


if __name__ == "__main__":
    main()
