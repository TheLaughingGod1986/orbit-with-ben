#!/usr/bin/env python3
"""Remove the excessive pre-brand pause from the approved v13 master.

The locked voice finishes the hook at approximately 17.531 seconds. In v13 the
brand ident starts at 19.650, leaving a 2.119-second dead beat over the closing
galaxy image. Remove 1.900 seconds from both picture and mixed audio:

  hook ends       17.531
  brand starts    17.750
  ident fully up  17.950
  "This is Orbit" 17.983

All later picture, narration, music and sound cues move together and remain in
sync. The 50 ms audio fades sit in the quiet beat and prevent a music-bed click.
"""
from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "001_Will-We-Ever-Meet-Aliens"
)
SOURCE = (
    ROOT
    / "09_Final-Export/"
    "aliens_BOLD_EXPLAINER_v13_VO_SYNC_UPLOAD_READY_MASTER.mp4"
)
OUTPUT = (
    ROOT
    / "09_Final-Export/"
    "aliens_BOLD_EXPLAINER_v14_TIGHT_VO_SYNC_UPLOAD_READY_MASTER.mp4"
)
PROOF = (
    ROOT
    / "09_Final-Export/"
    "aliens_v14_PROOF_tight_vo_synced_intro_45s.mp4"
)

CUT_START = 17.750
CUT_END = 19.650
FADE = 0.050


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def filter_graph() -> str:
    fade_start = CUT_START - FADE
    return (
        # Select the retained frames in one decode pass. The earlier two-trim
        # graph caused the long source to be decoded twice.
        f"[0:v]select='lt(t,{CUT_START})+gte(t,{CUT_END})',"
        "setpts=N/(30*TB),format=yuv420p[v];"
        f"[0:a]atrim=start=0:end={CUT_START},asetpts=PTS-STARTPTS,"
        f"afade=t=out:st={fade_start}:d={FADE}[a0];"
        f"[0:a]atrim=start={CUT_END},asetpts=PTS-STARTPTS,"
        f"afade=t=in:st=0:d={FADE}[a1];"
        "[a0][a1]concat=n=2:v=0:a=1[a]"
    )


def render(destination: Path, *, proof: bool = False) -> None:
    command = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
    ]
    if proof:
        command += ["-t", "45", "-i", str(SOURCE)]
    else:
        command += ["-i", str(SOURCE)]
    command += [
        "-filter_complex",
        filter_graph(),
        "-map",
        "[v]",
        "-map",
        "[a]",
    ]
    command += [
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-profile:v",
        "high",
        "-pix_fmt",
        "yuv420p",
        "-fps_mode",
        "cfr",
        "-r",
        "30",
    ]
    command += [
        "-c:a",
        "aac",
        "-b:a",
        "256k",
        "-movflags",
        "+faststart",
        str(destination),
    ]
    run(command)


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing source master: {SOURCE}")
    if not PROOF.exists():
        render(PROOF, proof=True)
    render(OUTPUT)
    print(OUTPUT)
    print(PROOF)


if __name__ == "__main__":
    main()
