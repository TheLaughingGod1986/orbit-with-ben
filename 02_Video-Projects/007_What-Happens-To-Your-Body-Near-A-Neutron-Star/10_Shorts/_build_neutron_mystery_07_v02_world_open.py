#!/usr/bin/env python3
"""Neutron mystery 07 v02 — world-first open (replaces Orbit-first v01).

Audit 2026-09-10 (`00_Brand/Channel-Setup/audits/channel_technical_audit_2026-09-10`):
v01 (`mAAMsbhm88w`, scheduled Tue 16 Sep 11:30) opens on Orbit full-frame at 0 s.
The only other Orbit-first Short (`TE_HDKAnqms`) got 0 % Shorts-feed traffic.

Fix: keep the VO window (412–437 s of the long) and the captions untouched; cover
the first 8 s of picture with the world-only lightning-star span (430–438 s), then
return to the synced picture from 420 s. Orbit still appears later in the cut.

Source: the public broadcast long (`Yk1tLh23rko`), fetched with yt-dlp to
/tmp/orbit_neutron_fix/neutron_long.mp4 because the local 09_Final-Export master
is not on this machine.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/TikTok/auto"))
sys.path.insert(0, str(REPO / "04_Audio/tools"))

from onscreen_captions import (  # noqa: E402
    auto_beats_from_phrases,
    ffmpeg_overlay_filter,
    render_beat_png,
    render_cta_png,
    vertical_base_filter,
)
from orbit_cfr_delivery import shorts_encode_args  # noqa: E402

LONG = Path("/tmp/orbit_neutron_fix/neutron_long.mp4")
OUT = ROOT / "10_Shorts/06_Final-Exports"
REPORT = ROOT / "10_Shorts/MYSTERY_07_V02_WORLD_OPEN.json"
FILM_TITLE = "What Happens to Your Body Near a Neutron Star?"
LONG_ID = "Yk1tLh23rko"
LONG_URL = f"https://www.youtube.com/watch?v={LONG_ID}"

ITEM = {
    "id": "07",
    "slug": "probe-closer-than-you",
    "audio_start": 412.0,
    "duration": 25.0,
    # picture: world-only cover, then synced picture
    "cover_start": 430.0,
    "cover_len": 7.0,
    "synced_start": 419.0,  # = audio_start + cover_len
    "title": "Could a Probe Get Closer to a Neutron Star?",
    "phrases": [
        "you wouldn't last",
        "could a probe?",
        "built for\nmilliseconds",
        "the answer\nis worse",
    ],
    "schedule_uk": "2026-09-16T11:30:00+01:00",
    "replaces": "mAAMsbhm88w",
}


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def description_for(title: str) -> str:
    return (
        f"{title}\n\n"
        f"Watch the full film — {FILM_TITLE}\n"
        f"{LONG_URL}\n\n"
        "#NeutronStar #Astronomy #Shorts #Astrophysics #Gravity "
        "#SpaceDocumentary #Physics #OrbitWithBen"
    )


def build_source(temp: Path) -> Path:
    """Continuous VO from audio_start; picture = world cover + synced tail."""
    src = temp / "source_world_open.mp4"
    a0 = ITEM["audio_start"]
    dur = ITEM["duration"]
    c0, cl = ITEM["cover_start"], ITEM["cover_len"]
    s0 = ITEM["synced_start"]
    tail = dur - cl
    fc = (
        f"[0:v]trim=start={c0}:end={c0 + cl},setpts=PTS-STARTPTS[c];"
        f"[0:v]trim=start={s0}:end={s0 + tail},setpts=PTS-STARTPTS[t];"
        f"[c][t]concat=n=2:v=1:a=0[v];"
        f"[0:a]atrim=start={a0}:end={a0 + dur},asetpts=PTS-STARTPTS[a]"
    )
    run(
        [
            "ffmpeg", "-y", "-i", str(LONG),
            "-filter_complex", fc,
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "14",
            "-c:a", "pcm_s16le",
            str(src),
        ]
    )
    return src


def render(temp: Path) -> Path:
    src = build_source(temp)
    beats = auto_beats_from_phrases(
        ITEM["phrases"], duration=ITEM["duration"], hook_end=9.0, punch_first_hook=True
    )
    beats.append(
        {
            "start": 10.5,
            "end": 15.0,
            "lines": [("full film", "white"), (FILM_TITLE.lower(), "yellow")],
        }
    )
    beat_paths: list[Path] = []
    for i, beat in enumerate(beats):
        p = temp / f"s07-beat-{i:02d}.png"
        kwargs = {"pointsize": 52, "y_center": 700} if i == len(beats) - 1 else {}
        render_beat_png(p, beat["lines"], **kwargs)
        beat_paths.append(p)
    cta = temp / "s07-cta.png"
    render_cta_png(cta, text="watch the full film →")

    output = OUT / f"neutron_mystery-{ITEM['id']}_{ITEM['slug']}_v02_world-open.mp4"
    OUT.mkdir(parents=True, exist_ok=True)
    overlay = ffmpeg_overlay_filter(
        beats, cta_start=max(ITEM["duration"] - 4.0, 0.0), beat_input_start=1
    )
    filtergraph = vertical_base_filter(framed=False) + ";" + overlay
    cmd = ["ffmpeg", "-y", "-i", str(src)]
    for bp in beat_paths:
        cmd += ["-loop", "1", "-framerate", "30", "-i", str(bp)]
    cmd += ["-loop", "1", "-framerate", "30", "-i", str(cta)]
    cmd += [
        "-filter_complex", filtergraph,
        "-map", "[v]", "-map", "0:a:0",
        *shorts_encode_args(),
        "-t", str(ITEM["duration"]),
        str(output),
    ]
    run(cmd)
    return output


def probe(path: Path) -> dict:
    raw = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration,size:stream=codec_type,width,height", "-of", "json", str(path)],
        text=True,
    )
    return json.loads(raw)


def main() -> None:
    if not LONG.exists():
        raise SystemExit(
            f"Missing long: {LONG}\n"
            "yt-dlp -f 'bv*[height<=1080][ext=mp4]+ba[ext=m4a]' --merge-output-format mp4 "
            f"-o {LONG} https://www.youtube.com/watch?v={LONG_ID}"
        )
    with tempfile.TemporaryDirectory(prefix="neutron-m07-v02-") as tmp:
        out = render(Path(tmp))
    meta = probe(out)
    report = {
        **ITEM,
        "file": str(out),
        "duration_s": round(float(meta["format"]["duration"]), 2),
        "bytes": int(meta["format"]["size"]),
        "description": description_for(ITEM["title"]),
        "related": LONG_ID,
        "status": "rendered — upload private, parity, Related, schedule 16 Sep 11:30, then unschedule mAAMsbhm88w",
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(f"→ {out} {report['duration_s']}s")
    print("REPORT", REPORT)


if __name__ == "__main__":
    main()
