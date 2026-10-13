#!/usr/bin/env python3
"""J0167 step 6a: render the five trimmed film bodies for the OWB compilation.

Each master is cut 0 -> its `out` from COMPILATION_TRIMS_v01.json (plus any cut with apply=true),
scaled lanczos to 1920x1080 at 30 fps, and written as
  /private/tmp/owb_comp/bodies_v01/body_<film>.mp4  (picture + film audio, h264 crf 17, aac 256k)
  /private/tmp/owb_comp/bodies_v01/body_<film>.wav  (film audio stem, 48 kHz stereo PCM, untouched level)
plus bodies.json with durations and EBU R128 integrated loudness / true peak per body.
Loudness is only measured here; the final assembly (step 6b) normalises the whole cut to about -14 LUFS.

Usage: python3 _render_film_bodies_v01.py [--only 021,013] [--out-dir DIR]
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTERS = Path("/private/tmp/owb_comp/masters.json")
TRIMS = HERE / "COMPILATION_TRIMS_v01.json"
FPS = 30


def keep_ranges(film):
    """Spans of the master to keep, in order, after applied cuts."""
    spans, t = [], 0.0
    for c in sorted((c for c in film["cuts"] if c.get("apply")), key=lambda c: c["remove"][0]):
        a, b = c["remove"]
        spans.append((t, a))
        t = b
    spans.append((t, film["out"]))
    return [(a, b) for a, b in spans if b - a > 0.05]


def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
                        "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", tail)
    p = re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail)
    return (float(i.group(1)) if i else None, float(p.group(1)) if p else None)


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout
    return round(float(out.strip()), 3)


def render(film, src, out_dir):
    spans = keep_ranges(film)
    n = len(spans)
    chains = []
    for k, (a, b) in enumerate(spans):
        chains.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS,"
                      f"scale=1920:1080:flags=lanczos:force_original_aspect_ratio=increase,crop=1920:1080,"
                      f"fps={FPS},setsar=1,format=yuv420p[v{k}]")
        chains.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,aresample=48000,"
                      f"aformat=channel_layouts=stereo[a{k}]")
    if n == 1:
        chains.append("[v0]null[vout]")
        chains.append("[a0]asplit=2[aout][awav]")
    else:
        # internal cuts: 0.4 s picture xfade, 80 ms audio crossfade, on measured VO gaps only
        v, a, off = "v0", "a0", spans[0][1] - spans[0][0]
        for k in range(1, n):
            off -= 0.4
            chains.append(f"[{v}][v{k}]xfade=transition=fade:duration=0.4:offset={off:.3f}[vx{k}]")
            chains.append(f"[{a}][a{k}]acrossfade=d=0.08[ax{k}]")
            v, a = f"vx{k}", f"ax{k}"
            off += spans[k][1] - spans[k][0]
        chains.append(f"[{v}]null[vout]")
        chains.append(f"[{a}]asplit=2[aout][awav]")
    mp4 = out_dir / f"body_{film['film']}.mp4"
    wav = out_dir / f"body_{film['film']}.wav"
    cmd = ["ffmpeg", "-hide_banner", "-y", "-loglevel", "error", "-i", src,
           "-filter_complex", ";".join(chains),
           "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
           "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
           "-movflags", "+faststart", str(mp4),
           "-map", "[awav]", "-c:a", "pcm_s16le", "-ar", "48000", str(wav)]
    print(f"render {film['film']}: {n} span(s) {spans} -> {mp4}", flush=True)
    subprocess.run(cmd, check=True)
    lufs, peak = loudness(wav)
    rec = {"film": film["film"], "id": film["id"], "src": src, "spans": spans,
           "mp4": str(mp4), "wav": str(wav), "duration": duration(mp4),
           "planned": round(sum(b - a for a, b in spans) - 0.4 * (n - 1), 3),
           "lufs_i": lufs, "true_peak_dbfs": peak}
    print(f"  done {film['film']}: {rec['duration']} s (planned {rec['planned']}), {lufs} LUFS, peak {peak}",
          flush=True)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--out-dir", default="/private/tmp/owb_comp/bodies_v01")
    args = ap.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    masters = json.loads(MASTERS.read_text())
    trims = json.loads(TRIMS.read_text())
    only = {s for s in args.only.split(",") if s}
    index = out_dir / "bodies.json"
    recs = json.loads(index.read_text()) if index.exists() else {}
    for film in trims["films"]:
        if only and film["film"] not in only:
            continue
        src = masters[film["film"]]
        if not Path(src).exists():
            sys.exit(f"missing master for {film['film']}: {src}")
        recs[film["film"]] = render(film, src, out_dir)
        index.write_text(json.dumps(recs, indent=2))
    print("all bodies done", flush=True)


if __name__ == "__main__":
    main()
