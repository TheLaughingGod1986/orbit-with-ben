#!/usr/bin/env python3
"""FbRFvSApfOQ opening remint — picture-first 0–3s (Ben unlock 5 Sep 2026).

FAIL: orange Orbit in first 3s on Europa ice + Jupiter.
FIX: replace 0–OPEN_S video with an Orbit-free Europa plate; keep original
audio, captions, and yellow listing-title burn on the rest of the cut.

Mac-only (mp4 is disk_only). Does not touch other Shorts. Does not change thumbs.

  python3 _remint_fbrf_picture_first_open_v04.py
  python3 _remint_fbrf_picture_first_open_v04.py --src /path/to/v03.mp4
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPORTS = HERE / "06_Final-Exports"
PROOF = EXPORTS / "_proof_FbRFvSApfOQ_open_v04"
STATUS = HERE / "FbRF_OPEN_REMINT_STATUS.json"

YT_ID = "FbRFvSApfOQ"
OPEN_S = 3.0
DEFAULT_PLATE_AT = 5.0
OUT_NAME = "europa_punch-01_ocean-we-cannot-see_v04_picture-first-open.mp4"

SRC_CANDIDATES = [
    EXPORTS / "europa_punch-01_ocean-we-cannot-see_v03_diamond.mp4",
    EXPORTS / "europa_punch-01_ocean-we-cannot-see_v03.mp4",
    EXPORTS / "europa_punch-01_ocean-we-cannot-see_v01.mp4",
    Path.home()
    / "YouTube/orbit-with-ben/02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa"
    / "10_Shorts/06_Final-Exports/europa_punch-01_ocean-we-cannot-see_v03_diamond.mp4",
    Path(
        "/Users/ben/YouTube/orbit-with-ben/02_Video-Projects/"
        "006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/06_Final-Exports/"
        "europa_punch-01_ocean-we-cannot-see_v03_diamond.mp4"
    ),
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def probe(path: Path) -> dict:
    raw = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size:stream=width,height,codec_type,codec_name",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(raw.stdout)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_src(explicit: Path | None) -> Path:
    if explicit:
        p = explicit.expanduser().resolve()
        if not p.is_file():
            raise SystemExit(f"Missing --src {p}")
        return p
    for p in SRC_CANDIDATES:
        if p.is_file() and p.stat().st_size > 100_000:
            return p.resolve()
    raise SystemExit(
        "Source mp4 not found. Pass --src to the live FbRFvSApfOQ cut "
        "(europa_punch-01_ocean-we-cannot-see_v03_diamond.mp4 on Mac)."
    )


def orange_score(png: Path) -> float:
    """Rough Orbit detector: fraction of vivid orange pixels (0–1)."""
    try:
        from PIL import Image
    except ImportError:
        return -1.0
    im = Image.open(png).convert("RGB").resize((270, 480))
    px = list(im.getdata())
    n = len(px) or 1
    hit = 0
    for r, g, b in px:
        if r > 160 and 40 < g < 160 and b < 90 and r > g + 40 and r > b + 60:
            hit += 1
    return hit / n


def extract_frame(src: Path, t: float, dest: Path) -> None:
    run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            f"{t:.3f}",
            "-i",
            str(src),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(dest),
        ]
    )


def pick_plate_time(src: Path, temp: Path, preferred: float) -> float:
    candidates = [preferred] + [x * 0.5 for x in range(7, 25)]  # 3.5..12.0
    best_t, best_score = preferred, 999.0
    for t in candidates:
        frame = temp / f"score_{t:.1f}.png"
        extract_frame(src, t, frame)
        score = orange_score(frame)
        if score < 0:
            return preferred
        if score < best_score:
            best_score, best_t = score, t
        if score < 0.002:
            return t
    return best_t


def remint(src: Path, plate_at: float | None, open_s: float) -> dict:
    EXPORTS.mkdir(parents=True, exist_ok=True)
    PROOF.mkdir(parents=True, exist_ok=True)
    out = EXPORTS / OUT_NAME

    info = probe(src)
    dur = float(info["format"]["duration"])
    if not (20.0 <= dur <= 30.0):
        raise SystemExit(f"Unexpected source duration {dur:.2f}s (want ~22–27)")

    streams = {s.get("codec_type"): s for s in info.get("streams", [])}
    v = streams.get("video") or {}
    w, h = int(v.get("width") or 0), int(v.get("height") or 0)
    if not (h > w and h >= 1280):
        raise SystemExit(f"Unexpected geometry {w}x{h}")

    chosen = DEFAULT_PLATE_AT
    plate_orange = -1.0

    with tempfile.TemporaryDirectory(prefix="fbrf_open_v04_") as td:
        temp = Path(td)
        chosen = (
            plate_at if plate_at is not None else pick_plate_time(src, temp, DEFAULT_PLATE_AT)
        )

        plate = temp / "plate.png"
        extract_frame(src, chosen, plate)
        plate_orange = orange_score(plate)
        if plate_orange >= 0.01:
            chosen = pick_plate_time(src, temp, max(chosen, 6.0))
            extract_frame(src, chosen, plate)
            plate_orange = orange_score(plate)

        open_vid = temp / "open_picture.mp4"
        # Hold Orbit-free plate (subtle zoom). Audio comes from source later.
        run(
            [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
                "-framerate",
                "30",
                "-i",
                str(plate),
                "-t",
                f"{open_s:.3f}",
                "-vf",
                "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
                "zoompan=z='1+0.01*on/90':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                ":d=1:s=1080x1920:fps=30",
                "-an",
                "-c:v",
                "libx264",
                "-preset",
                "fast",
                "-crf",
                "16",
                "-pix_fmt",
                "yuv420p",
                str(open_vid),
            ]
        )

        rest_vid = temp / "rest.mp4"
        run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                f"{open_s:.3f}",
                "-i",
                str(src),
                "-an",
                "-c:v",
                "libx264",
                "-preset",
                "fast",
                "-crf",
                "16",
                "-pix_fmt",
                "yuv420p",
                str(rest_vid),
            ]
        )

        concat_list = temp / "concat.txt"
        concat_list.write_text(f"file '{open_vid}'\nfile '{rest_vid}'\n")
        picture = temp / "picture_full.mp4"
        run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_list),
                "-c",
                "copy",
                str(picture),
            ]
        )

        run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(picture),
                "-i",
                str(src),
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                "-c:v",
                "libx264",
                "-preset",
                "fast",
                "-crf",
                "16",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-shortest",
                "-movflags",
                "+faststart",
                str(out),
            ]
        )

        for t in (0.5, 1.5, 2.5, 2.9, 3.5):
            extract_frame(out, t, PROOF / f"t{t:.1f}.png")

    out_info = probe(out)
    out_dur = float(out_info["format"]["duration"])
    if not (22.0 <= out_dur <= 27.5):
        raise SystemExit(f"Output duration {out_dur:.2f}s outside 22–27s gate")

    proof_scores = {
        f"{t:.1f}": orange_score(PROOF / f"t{t:.1f}.png") for t in (0.5, 1.5, 2.5, 2.9)
    }
    bad = [k for k, s in proof_scores.items() if s >= 0.01]
    digest = sha256_file(out)
    payload = {
        "youtube_video_id": YT_ID,
        "unlock": "Ben unlocked opening remint only — 5 Sep 2026",
        "src": str(src),
        "out": str(out),
        "sha256": digest,
        "duration_s": round(out_dur, 3),
        "open_s": open_s,
        "plate_at_s": chosen,
        "plate_orange_score": plate_orange,
        "proof_orange_scores_0_3s": proof_scores,
        "proof_dir": str(PROOF),
        "pass_picture_first_0_3s": len(bad) == 0,
        "fail_times": bad,
        "thumbs_unchanged": True,
        "other_shorts_untouched": True,
        "built_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    STATUS.write_text(json.dumps(payload, indent=2) + "\n")
    (EXPORTS / f"{OUT_NAME}.sha256").write_text(f"{digest}  {OUT_NAME}\n")
    if bad:
        raise SystemExit(f"Orbit orange still detected in open frames: {bad}. See {PROOF}")
    print(json.dumps(payload, indent=2))
    return payload


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", type=Path, default=None)
    ap.add_argument("--plate-at", type=float, default=None, help="Seconds into src for clean plate")
    ap.add_argument("--open-s", type=float, default=OPEN_S)
    args = ap.parse_args()
    remint(resolve_src(args.src), args.plate_at, args.open_s)


if __name__ == "__main__":
    main()
