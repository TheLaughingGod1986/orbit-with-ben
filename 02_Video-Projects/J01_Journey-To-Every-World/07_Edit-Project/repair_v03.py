#!/usr/bin/env python3
"""J2221 v03: duck linking music under the eight narration takes.

Keeps J01_Journey_v02.mp4 picture (including the 53:37 luma lift).
Does not re-slice the seven films and does not add a second score under them.
Does not invent a full-length laid score: the locked Earth-spin bed is 26 s
on disk and the passing gate recorded 446.3 s.

£0. No new credits.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
SCRATCH = Path("/Volumes/MiniWork/scratch/J2221")
STEMS = SCRATCH / "stems"
AUDIO = SCRATCH / "audio"
OUT_DIR = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/J01_Journey-To-Every-World/07_Edit-Project")
FILM = OUT_DIR.parent
V02 = OUT_DIR / "J01_Journey_v02.mp4"
SR = 48000
HOP = SR // 10
TARGET_UNDER = 18.0  # LU under the voice momentary; the check fails inside 10. Extra covers the 400 ms window.
XFADE = 0.50
VO_PIECES = ["cold", "bridge1", "bridge2", "bridge3", "bridge4", "bridge5", "bridge6", "close"]
LINK_ORDER = [
    "cold", "card1", "bridge1", "card2", "bridge2", "card3", "bridge3",
    "card4", "bridge4", "card5", "bridge5", "card6", "bridge6", "card7", "close",
]
FILM_ORDER = [
    ("cold", "link"),
    ("card1", "link"),
    ("part1_027", "part"),
    ("bridge1", "link"),
    ("card2", "link"),
    ("part2_023", "part"),
    ("bridge2", "link"),
    ("card3", "link"),
    ("part3_025", "part"),
    ("bridge3", "link"),
    ("card4", "link"),
    ("part4_028", "part"),
    ("bridge4", "link"),
    ("card5", "link"),
    ("part5_026", "part"),
    ("bridge5", "link"),
    ("card6", "link"),
    ("part6_024", "part"),
    ("bridge6", "link"),
    ("card7", "link"),
    ("part7_029", "part"),
    ("close", "link"),
]


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def run(cmd: list) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout or "")[-800:])


def probe(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True).strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_stereo(path: Path) -> np.ndarray:
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"])
    audio = np.frombuffer(raw, np.float32).reshape(-1, 2)
    return np.array(audio, dtype=np.float32, copy=True)


def save_stereo(path: Path, audio: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
           "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "pipe:0",
           "-c:a", "pcm_s16le", str(path)]
    r = subprocess.run(cmd, input=audio.astype(np.float32).tobytes(), capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-400:].decode())


def ebur128(path: Path):
    sys.path.insert(0, str(REPO / "scripts"))
    import sfx_kit
    return sfx_kit.ebur128(path), sfx_kit


def duck_piece(name: str) -> None:
    bed_path = STEMS / f"{name}_bed.wav"
    vo_path = STEMS / f"{name}_vo.wav"
    out = STEMS / "ducked" / f"{name}_bed.wav"
    (mom, _integ), kit = ebur128(vo_path)
    bed_m, _bed_i = kit.ebur128(bed_path)
    n = min(len(mom), len(bed_m))
    # The level check hears the pieces joined, so speech is judged against that
    # joined voice (-16.7 LUFS), not against one piece's own average.
    joined_i = -16.7
    raw = np.zeros(n, np.float64)
    for i in range(n):
        speaking = mom[i] > kit.SILENT and mom[i] >= joined_i - 10.0
        margin = mom[i] - bed_m[i]
        raw[i] = min(0.0, (margin - TARGET_UNDER) if speaking and margin < TARGET_UNDER else 0.0)
    # The checker uses a 400 ms momentary window, so hold the deepest cut across that window.
    gain = raw.copy()
    for i in range(n):
        lo, hi = max(0, i - 6), min(n, i + 4)
        gain[i] = raw[lo:hi].min()
    audio = load_stereo(bed_path)
    hops = min(n, len(audio) // HOP)
    env = np.repeat(10 ** (gain[:hops] / 20.0), HOP).astype(np.float32)
    if len(env) < len(audio):
        env = np.pad(env, (0, len(audio) - len(env)), constant_values=env[-1] if len(env) else 1)
    audio *= env[:len(audio), None]
    save_stereo(out, audio)
    log(f"ducked {name} deepest {gain.min():.1f} dB")


def duck_cards() -> None:
    """Chapter cards sit against narration in the joined stem. Drop the whole card so the 400 ms window clears."""
    for i in range(1, 8):
        src = STEMS / f"card{i}_bed.wav"
        out = STEMS / "ducked" / f"card{i}_bed.wav"
        audio = load_stereo(src) * (10 ** (-20 / 20))
        save_stereo(out, audio)
        log(f"card{i} bed -20 dB")


def bed_src(name: str) -> Path:
    ducked = STEMS / "ducked" / f"{name}_bed.wav"
    return ducked if ducked.exists() else STEMS / f"{name}_bed.wav"


def concat(names: list[str], kind: str, out: Path) -> None:
    listing = out.with_suffix(".txt")
    lines = []
    for name in names:
        src = bed_src(name) if kind == "bed" else STEMS / f"{name}_{kind}.wav"
        lines.append(f"file '{src}'")
    listing.write_text("\n".join(lines) + "\n")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(out)])


def level_check() -> dict:
    out = STEMS / "ducked" / "sfx_level.json"
    vo = STEMS / "ducked" / "linking_vo.wav"
    sfx = STEMS / "ducked" / "linking_sfx.wav"
    bed = STEMS / "ducked" / "linking_bed.wav"
    concat(LINK_ORDER, "vo", vo)
    concat(LINK_ORDER, "sfx", sfx)
    concat(LINK_ORDER, "bed", bed)
    r = subprocess.run([sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
                        "--vo", str(vo), "--sfx", str(sfx), "--bed", str(bed),
                        "--minutes", "3.2", "--out", str(out)])
    log(f"sfx_kit exit {r.returncode}")
    return json.loads(out.read_text())


def remix_links() -> None:
    dest = SCRATCH / "audio_v03"
    dest.mkdir(parents=True, exist_ok=True)
    for name in LINK_ORDER:
        out = dest / f"{name}.wav"
        old = AUDIO / ("close.wav" if name == "close" else f"{name.replace('bridge', 'bridge_').replace('card', 'card_')}.wav")
        # audio/ names: cold.wav, card_1.wav, bridge_1.wav, close.wav
        if name == "cold" or name == "close":
            old = AUDIO / f"{name}.wav"
        elif name.startswith("card"):
            old = AUDIO / f"card_{name[4:]}.wav"
        elif name.startswith("bridge"):
            old = AUDIO / f"bridge_{name[6:]}.wav"
        dur = probe(old)
        if out.exists() and abs(probe(out) - dur) < 0.05:
            log(f"keep mix {name}")
            continue
        bed = bed_src(name)
        vo = STEMS / f"{name}_vo.wav"
        sfx = STEMS / f"{name}_sfx.wav"
        log(f"mix {name}")
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-i", str(bed), "-i", str(vo), "-i", str(sfx),
             "-filter_complex",
             f"[0:a]apad=whole_dur={dur:.3f}[b];[1:a]apad=whole_dur={dur:.3f}[v];"
             f"[2:a]apad=whole_dur={dur:.3f}[s];[b][v][s]amix=inputs=3:duration=first:dropout_transition=0:normalize=0[a]",
             "-map", "[a]", "-t", f"{dur:.3f}", "-c:a", "pcm_s16le", "-ar", str(SR), "-ac", "2", str(out)])


def part_wav(name: str) -> Path:
    out = SCRATCH / "audio_v03" / f"{name}.wav"
    if out.exists() and out.stat().st_size > 100000:
        return out
    src = SCRATCH / f"seg_{name}.mp4"
    log(f"extract {name}")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
         "-vn", "-c:a", "pcm_s16le", "-ar", str(SR), "-ac", "2", str(out)])
    return out


def link_wav(name: str) -> Path:
    return SCRATCH / "audio_v03" / f"{name}.wav"


def join_audio(out: Path) -> None:
    files = []
    for name, kind in FILM_ORDER:
        files.append(part_wav(name) if kind == "part" else link_wav(name))
    durs = [probe(p) for p in files]
    expect = sum(durs) - XFADE * (len(files) - 1)
    log(f"join audio ~{expect:.1f}s")
    parts = []
    acc_label = "[0:a]"
    for i in range(1, len(files)):
        parts.append(f"{acc_label}[{i}:a]acrossfade=d={XFADE}:c1=tri:c2=tri[ax{i}]")
        acc_label = f"[ax{i}]"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for p in files:
        cmd += ["-i", str(p)]
    cmd += ["-filter_complex", ";".join(parts), "-map", acc_label,
            "-c:a", "pcm_s16le", "-ar", str(SR), "-ac", "2", str(out)]
    run(cmd)


def loudnorm_json(blob: str) -> dict:
    dec = json.JSONDecoder()
    start = blob.rfind("\n{")
    start = blob.find("{") if start < 0 else start + 1
    if start < 0:
        raise RuntimeError("loudnorm measure failed\n" + blob[-500:])
    measured, _end = dec.raw_decode(blob[start:])
    if "input_i" not in measured:
        raise RuntimeError("loudnorm measure had no input_i\n" + blob[-500:])
    return measured


def mux_and_norm(audio: Path, dest: Path) -> dict:
    raw = SCRATCH / "J01_Journey_v03_preloud.mp4"
    log("mux picture copy")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-i", str(V02), "-i", str(audio),
         "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-ac", "2",
         "-shortest", str(raw)])
    log("measure loudness")
    r = subprocess.run(["ffmpeg", "-hide_banner", "-vn", "-i", str(raw),
                        "-af", "loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    measured = loudnorm_json(r.stderr or "")
    af = ("loudnorm=I=-14:TP=-1.0:LRA=11:measured_I={input_i}:measured_TP={input_tp}:"
          "measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}:linear=true")
    af = af.format(**{k: measured[k] for k in ("input_i", "input_tp", "input_lra", "input_thresh", "target_offset")})
    log(f"apply loudnorm I={measured['input_i']} TP={measured['input_tp']}")
    local = SCRATCH / "J01_Journey_v03.mp4"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw),
         "-af", af, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), str(local)])
    log(f"copy {dest.name}")
    run(["rsync", "-a", "--partial", str(local), str(dest)])
    digest = sha256(dest)
    (OUT_DIR / "J01_Journey_v03.sha256").write_text(f"{digest}  J01_Journey_v03.mp4\n")
    return {"sha256": digest, "seconds": round(probe(dest), 3), "input_i": measured["input_i"],
            "input_tp": measured["input_tp"], "v02_seconds": round(probe(V02), 3)}


def copy_sfx() -> str:
    kit = FILM / "06_Sound-Effects" / "kit_v01"
    kit.mkdir(parents=True, exist_ok=True)
    for src in (SCRATCH / "sfx_ui", SCRATCH / "sfx_ink"):
        if not src.exists():
            continue
        run(["rsync", "-a", "--partial", str(src) + "/", str(kit / src.name) + "/"])
    lines = []
    for p in sorted(kit.rglob("*")):
        if p.is_file() and not p.name.startswith("."):
            lines.append(f"{sha256(p)}  {p.relative_to(kit)}")
    (kit / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n")
    return str(kit)


def missing_score_note() -> dict:
    bed = Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning/05_Music/earth-spin_score_take2_straight_v01j.wav")
    note = {
        "laid_score": "not written",
        "reason": "The locked 027 bed file is 26.0 s and 4992044 bytes. music_gate_v01j_locked.json records that same filename at 446.3 s when it passed. No other copy of the 446 s file was found. Looping the 26 s stub, or filling the part with another film's bed, would invent the score. music_gate stays failed until that source is restored.",
        "file": str(bed),
        "seconds_on_disk": round(probe(bed), 3),
        "seconds_when_gate_passed": 446.3,
        "part": "part1_027",
        "other_scores_present": {
            "023": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/023_What-Happened-To-Venus/05_Music/venus_score_bed_v01_full.mp3",
            "024": "/Volumes/data/mac-mini-archive/2026-11-05/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed/05_Music/light-speed_score_bed_v01_full.mp3",
            "025": "/Volumes/data/mac-mini-archive/2026-11-05/YouTube/orbit-with-ben/02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/05_Music/mars-robot_score_bed_v02_full.mp3",
            "026": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/026_How-Far-Is-The-Nearest-Star/05_Music/nearest-star_score_bed_v01_full.wav",
            "028": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/05_Music/gliese_score_bed_v03.mp3",
            "029": "/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode/05_Music/betelgeuse_score_bed_v01.mp3",
        },
    }
    path = FILM / "05_Music" / "J01_LAID_SCORE_BLOCK.json"
    path.write_text(json.dumps(note, indent=2) + "\n")
    return note


def frame_match() -> str:
    a = SCRATCH / "qa" / "v02_3216.jpg"
    b = SCRATCH / "qa" / "v03_3216.jpg"
    a.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", "3216.8", "-i", str(V02), "-frames:v", "1", str(a)])
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", "3216.8", "-i", str(OUT_DIR / "J01_Journey_v03.mp4"), "-frames:v", "1", str(b)])
    return "match" if sha256(a) == sha256(b) else "DIFFER"


def main() -> int:
    os.environ["TMPDIR"] = str(SCRATCH / "tmp")
    (SCRATCH / "tmp").mkdir(parents=True, exist_ok=True)
    (STEMS / "ducked").mkdir(parents=True, exist_ok=True)
    for name in VO_PIECES:
        duck_piece(name)
    duck_cards()
    report = level_check()
    log(f"linking level {report['verdict']} fails {len(report['fails'])}")
    (STEMS / "ducked" / "LEVEL.txt").write_text(json.dumps(report, indent=2) + "\n")
    if report["verdict"] != "PASS":
        log("level still failing; not muxing")
        return 2
    if "--stems-only" in sys.argv:
        log("stems only")
        return 0
    block = missing_score_note()
    kit = copy_sfx()
    remix_links()
    joined = SCRATCH / "audio_v03" / "journey_v03.wav"
    join_audio(joined)
    info = mux_and_norm(joined, OUT_DIR / "J01_Journey_v03.mp4")
    info["frame_3216"] = frame_match()
    info["sfx_level"] = report["verdict"]
    info["sfx_fails"] = report["fails"]
    info["laid_score"] = block["reason"]
    info["sfx_kit"] = kit
    (OUT_DIR / "j01_v03_pack").mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "j01_v03_pack" / "REPAIR.json").write_text(json.dumps(info, indent=2) + "\n")
    log(json.dumps(info))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        log(f"FAILED {exc}")
        sys.exit(1)
