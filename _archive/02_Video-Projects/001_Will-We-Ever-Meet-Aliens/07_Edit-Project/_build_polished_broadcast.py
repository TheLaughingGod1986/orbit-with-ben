#!/usr/bin/env python3
"""Orbit 001 — polished broadcast cut.

Layout:
  - Full-frame B-roll matched to each VO section (2–3 unique clips, no reuse)
  - Orbit as small bottom-right PiP (expressions), never full-screen
  - Smoothed VO master (crossfades + light dynamics + long-pause trim)

Outputs:
  - 02_Voiceover/05_Master/aliens_voiceover_master_smooth_v01.wav
  - 09_Final-Export/aliens_broadcast_v01.mp4
  - 07_Edit-Project/SECTION_EDL_v01.json
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
SEC_DIR = ROOT / "02_Voiceover/04_Section-Exports"
MASTER_DIR = ROOT / "02_Voiceover/05_Master"
BROLL = ROOT / "04_Generated-Clips/03_Polished/broll"
POLISHED = ROOT / "04_Generated-Clips/03_Polished"
OUT = ROOT / "09_Final-Export/aliens_broadcast_v01.mp4"
EDL_PATH = ROOT / "07_Edit-Project/SECTION_EDL_v01.json"
SMOOTH_VO = MASTER_DIR / "aliens_voiceover_master_smooth_v01.wav"

W, H, FPS = 1920, 1080, 30

# Unique B-roll per VO section (content-matched). Each clip id used at most once.
SECTION_BROLL: dict[str, list[str]] = {
    "01_cold-open": [
        "aliens_scene-001_v01.mp4",  # night sky
        "aliens_scene-002_v01.mp4",  # starfield push
        "aliens_scene-006_v01.mp4",  # galaxy
    ],
    "02_galaxy-scale": [
        "aliens_scene-011_v01.mp4",  # tiny probe / distance
        "aliens_scene-012_v01.mp4",  # milky way
        "aliens_scene-008_v01.mp4",  # earth night
    ],
    "03_exoplanets": [
        "aliens_scene-013_v01.mp4",  # transit
        "aliens_scene-061_v01.mp4",  # habitable zone planet
        "aliens_scene-017_v01.mp4",  # busy vs empty
        "aliens_scene-048_v01.mp4",  # catalogue
    ],
    "04_fermi-paradox": [
        "aliens_scene-020_v01.mp4",  # silence wave
        "aliens_scene-021_v01.mp4",  # clean empty stars
    ],
    "05_great-filter": [
        "aliens_scene-024_v01.mp4",  # lights fade
        "aliens_scene-025_v01.mp4",  # zoo abstract
        "aliens_scene-062_v01.mp4",  # radio eras
        "aliens_scene-046_v01.mp4",  # lonely probe
    ],
    "06_explanations": [
        "aliens_scene-030_v01.mp4",  # slow ship / distance
        "aliens_scene-031_v01.mp4",  # spectrum
        "aliens_scene-033_v01.mp4",  # telescopes
        "aliens_scene-063_v01.mp4",  # optical seti
    ],
    "07_detection": [
        "aliens_scene-037_v01.mp4",  # atmosphere
        "aliens_scene-038_v01.mp4",  # mirror
        "aliens_scene-041_v01.mp4",  # data glow
        "aliens_scene-035_v01.mp4",  # wow chart
    ],
    "08_first-contact": [
        "aliens_scene-042_v01.mp4",  # mars
        "aliens_scene-043_v01.mp4",  # icy moon
        "aliens_scene-064_v01.mp4",  # ice grain
        "aliens_scene-050_v01.mp4",  # earth to stars
    ],
    "09_conclusion": [
        "aliens_scene-055_v01.mp4",  # invitation stars
        "aliens_scene-060_v01.mp4",  # beauty galaxy
        "aliens_scene-051_v01.mp4",  # caution signal
        "aliens_scene-065_v01.mp4",  # final hold
    ],
}

SECTION_ORBIT: dict[str, str] = {
    "01_cold-open": "orbit_explaining_talk_v01_polished.mp4",
    "02_galaxy-scale": "orbit_explaining_talk_v01_polished.mp4",
    "03_exoplanets": "orbit_explaining_talk_v01_polished.mp4",
    "04_fermi-paradox": "orbit_surprised_reaction_v01_polished.mp4",
    "05_great-filter": "orbit_explaining_talk_v01_polished.mp4",
    "06_explanations": "orbit_explaining_talk_v01_polished.mp4",
    "07_detection": "orbit_explaining_talk_v01_polished.mp4",
    "08_first-contact": "orbit_surprised_reaction_v01_polished.mp4",
    "09_conclusion": "orbit_ending_goodbye_v01_polished.mp4",
}

SECTION_ORDER = [
    "01_cold-open",
    "02_galaxy-scale",
    "03_exoplanets",
    "04_fermi-paradox",
    "05_great-filter",
    "06_explanations",
    "07_detection",
    "08_first-contact",
    "09_conclusion",
]


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1",
                str(path),
            ],
            text=True,
        ).strip()
    )


def assert_unique_mapping() -> None:
    seen: set[str] = set()
    for sec, clips in SECTION_BROLL.items():
        for c in clips:
            if c in seen:
                raise SystemExit(f"duplicate broll mapping: {c} in {sec}")
            seen.add(c)
            if not (BROLL / c).exists():
                raise SystemExit(f"missing broll {c}")


def build_smooth_vo(td: Path) -> Path:
    """Crossfade section joins + light polish; shrink only very long silences."""
    parts = []
    for name in SECTION_ORDER:
        src = SEC_DIR / f"aliens_vo_section-{name}_v02.wav"
        assert src.exists(), src
        parts.append(src)

    # Acrossfade 60ms between sections to kill hard robotic butts
    # Build via ffmpeg acrossfade chain
    if len(parts) == 1:
        shutil.copy2(parts[0], SMOOTH_VO)
        return SMOOTH_VO

    # First pass: concat with short crossfades
    # Use filter_complex acrossfade iteratively
    current = parts[0]
    tmp_prev = td / "vo_acc.wav"
    shutil.copy2(current, tmp_prev)
    for i, nxt in enumerate(parts[1:], 1):
        out = td / f"vo_acc_{i}.wav"
        # 80ms crossfade
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(tmp_prev), "-i", str(nxt),
                "-filter_complex",
                "acrossfade=d=0.08:c1=tri:c2=tri",
                str(out),
            ],
            check=True,
        )
        tmp_prev = out

    # Dynamics + highpass + gentle silence compress for pauses > 0.55s → 0.28s
    # silenceremove: stop_periods=-1 stop_duration=0.55 stop_threshold=-38dB stop_silence=0.28
    polished = td / "vo_polished.wav"
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(tmp_prev),
            "-af",
            (
                "highpass=f=80,"
                "lowpass=f=12000,"
                "silenceremove=stop_periods=-1:stop_duration=0.55:stop_threshold=-38dB:stop_silence=0.28:detection=peak,"
                "acompressor=threshold=-18dB:ratio=2.5:attack=15:release=120:makeup=2,"
                "loudnorm=I=-16:TP=-1.5:LRA=11"
            ),
            "-ar", "44100", "-ac", "1",
            str(polished),
        ],
        check=True,
    )
    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(polished, SMOOTH_VO)
    # also mp3
    mp3 = SMOOTH_VO.with_suffix(".mp3")
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(SMOOTH_VO), "-codec:a", "libmp3lame", "-b:a", "192k", str(mp3),
        ],
        check=True,
    )
    return SMOOTH_VO


def split_duration(total: float, n: int) -> list[float]:
    if n <= 0:
        return []
    base = total / n
    # Prefer ~12–22s cuts when possible
    durs = [base] * n
    # fix drift
    durs[-1] += total - sum(durs)
    return durs


def build_edl(vo_dur_by_section: dict[str, float]) -> list[dict]:
    edl = []
    t = 0.0
    for name in SECTION_ORDER:
        sec_dur = vo_dur_by_section[name]
        clips = SECTION_BROLL[name]
        # Use 2 clips if section < 40s, else up to 3–4 as listed (cap 3 for vibrancy without frenzy)
        if sec_dur < 40:
            use = clips[:2]
        elif sec_dur < 70:
            use = clips[:3]
        else:
            use = clips[:4] if len(clips) >= 4 else clips
        durs = split_duration(sec_dur, len(use))
        for clip, dur in zip(use, durs):
            edl.append({
                "section": name,
                "start_s": round(t, 3),
                "end_s": round(t + dur, 3),
                "duration_s": round(dur, 3),
                "broll": clip,
                "orbit": SECTION_ORBIT[name],
            })
            t += dur
    return edl


def render_broll_bed(edl: list[dict], td: Path) -> Path:
    parts = []
    for i, shot in enumerate(edl):
        src = BROLL / shot["broll"]
        part = td / f"b_{i:03d}.mp4"
        dur = shot["duration_s"]
        # Scale to cover 1080p, mild Ken Burns via zoompan for polish (slow zoom)
        # Keep simple: cover scale + center crop, loop if needed
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-stream_loop", "-1", "-i", str(src),
                "-t", f"{dur:.4f}",
                "-an",
                "-vf",
                (
                    f"scale={W}:{H}:force_original_aspect_ratio=increase,"
                    f"crop={W}:{H},"
                    f"fps={FPS},"
                    "format=yuv420p"
                ),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                str(part),
            ],
            check=True,
        )
        parts.append(part)

    lst = td / "broll_list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    bed = td / "broll_bed.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(lst),
            "-c", "copy", str(bed),
        ],
        check=True,
    )
    return bed


def render_orbit_pip_track(edl: list[dict], total_dur: float, td: Path) -> Path:
    """Build a full-timeline Orbit plate (looped), later overlaid as PiP."""
    # Simpler: one continuous orbit explain loop for whole show, swap expression per section via concat
    parts = []
    # Group consecutive same orbit file
    i = 0
    while i < len(edl):
        orbit_name = edl[i]["orbit"]
        start = edl[i]["start_s"]
        j = i
        while j < len(edl) and edl[j]["orbit"] == orbit_name:
            j += 1
        end = edl[j - 1]["end_s"]
        dur = end - start
        src = POLISHED / orbit_name
        part = td / f"o_{i:03d}.mp4"
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-stream_loop", "-1", "-i", str(src),
                "-t", f"{dur:.4f}",
                "-an",
                "-vf", f"scale=640:-1,fps={FPS},format=yuv420p",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                str(part),
            ],
            check=True,
        )
        parts.append(part)
        i = j

    lst = td / "orbit_list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    orbit_bed = td / "orbit_bed.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(lst),
            "-c", "copy", str(orbit_bed),
        ],
        check=True,
    )
    return orbit_bed


def composite(broll: Path, orbit: Path, vo: Path, out: Path) -> None:
    """Full B-roll + Orbit PiP bottom-right (~18% width) + soft shadow pad + VO."""
    # PiP size ~ 320px wide on 1920 (~16.7%); margin 48px
    # overlay=W-w-48:H-h-48
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(broll),
            "-i", str(orbit),
            "-i", str(vo),
            "-filter_complex",
            (
                # soft dark plate behind Orbit for readability
                "[1:v]scale=340:-1,format=rgba,"
                "pad=360:ih+20:10:10:color=0x00000099[orb];"
                "[0:v][orb]overlay=W-w-40:H-h-40:format=auto[v]"
            ),
            "-map", "[v]", "-map", "2:a:0",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            "-movflags", "+faststart",
            str(out),
        ],
        check=True,
    )


def main() -> None:
    assert_unique_mapping()
    OUT.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="orbit_broadcast_") as td:
        td = Path(td)
        print("smoothing VO…")
        vo = build_smooth_vo(td)
        # After silence trim, section durations no longer match raw section files.
        # Rebuild EDL against SMOOTH total by proportion of original section lengths.
        raw_durs = {
            name: probe(SEC_DIR / f"aliens_vo_section-{name}_v02.wav")
            for name in SECTION_ORDER
        }
        raw_total = sum(raw_durs.values())
        smooth_total = probe(vo)
        scale = smooth_total / raw_total
        vo_durs = {k: v * scale for k, v in raw_durs.items()}

        edl = build_edl(vo_durs)
        # Fix last end to exact smooth duration
        if edl:
            drift = smooth_total - edl[-1]["end_s"]
            edl[-1]["end_s"] = round(edl[-1]["end_s"] + drift, 3)
            edl[-1]["duration_s"] = round(edl[-1]["end_s"] - edl[-1]["start_s"], 3)

        EDL_PATH.write_text(json.dumps({
            "vo": str(vo),
            "vo_duration_s": round(smooth_total, 3),
            "layout": "broll_fullscreen + orbit_pip_bottom_right",
            "shots": edl,
        }, indent=2))
        print(f"EDL {len(edl)} shots, VO {smooth_total:.1f}s")

        print("rendering B-roll bed…")
        broll = render_broll_bed(edl, td)
        print("rendering Orbit PiP plate…")
        orbit = render_orbit_pip_track(edl, smooth_total, td)
        print("compositing broadcast…")
        composite(broll, orbit, vo, OUT)

    dur = probe(OUT)
    used = [s["broll"] for s in edl]
    report = {
        "out": str(OUT),
        "duration_s": round(dur, 3),
        "shots": len(edl),
        "unique_broll": len(set(used)),
        "orbit_mode": "corner_pip_~18pct",
        "vo": str(vo),
        "edl": str(EDL_PATH),
    }
    (ROOT / "07_Edit-Project/BROADCAST_BUILD_REPORT.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
