#!/usr/bin/env python3
"""Standalone Shorts S1-S4 (J0163): trim VO pauses to 0.4 s, per Chief's J0162 PASS (#99 6126452775).

Gaps between words come from the Scribe pass (vo_v01/stt/<stem>/stt_raw.json). Every gap over MAX_GAP is cut to
MAX_GAP by removing its middle, so breaths at each edge stay. Writes vo_v01/trim/<stem>_trim.wav (git-ignored) and
<stem>_trim_words.json (the remapped word times, for captions) plus pause_trim_meta.json. No spend.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
VO = HERE / "vo_v01"
OUT = VO / "trim"
STEMS = ["owb_sa_s1_mercury_vo_v01", "owb_sa_s2_neptune_vo_v01",
         "owb_sa_s3_iss_sunrises_vo_v01", "owb_sa_s4_uranus_vo_v01"]
MAX_GAP = 0.40
LEAD, TAIL = 0.10, 0.35


def dur(p: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(p)], capture_output=True, text=True, check=True).stdout)


def trim(stem: str) -> dict:
    raw = json.loads((VO / "stt" / stem / "stt_raw.json").read_text())
    words = [w for w in raw["words"] if w["type"] == "word"]
    src = VO / f"{stem}.wav"
    total = dur(src)
    keep: list[tuple[float, float]] = []
    a = max(0.0, words[0]["start"] - LEAD)
    for prev, nxt in zip(words, words[1:]):
        gap = nxt["start"] - prev["end"]
        if gap > MAX_GAP:
            keep.append((a, prev["end"] + MAX_GAP / 2))
            a = nxt["start"] - MAX_GAP / 2
    keep.append((a, min(total, words[-1]["end"] + TAIL)))

    def remap(t: float) -> float:
        out = 0.0
        for s, e in keep:
            if t <= e:
                return round(out + max(0.0, t - s), 3)
            out += e - s
        return round(out, 3)

    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"{stem}_trim.wav"
    parts = "".join(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,"
                    f"afade=t=out:st={e - s - 0.01:.3f}:d=0.01[p{i}];" for i, (s, e) in enumerate(keep))
    concat = "".join(f"[p{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[out]"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-filter_complex", parts + concat,
                    "-map", "[out]", "-ar", "48000", str(dest)], check=True)
    mapped = [{"word": w["text"].strip(), "start": remap(w["start"]), "end": remap(w["end"])} for w in words]
    (OUT / f"{stem}_trim_words.json").write_text(json.dumps({"stem": stem, "words": mapped}, indent=1) + "\n")
    return {"stem": stem, "source_s": round(total, 2), "trimmed_s": round(dur(dest), 2),
            "segments": len(keep), "words": len(words), "max_gap_s": MAX_GAP}


def main() -> None:
    rows = [trim(s) for s in STEMS]
    (OUT / "pause_trim_meta.json").write_text(json.dumps(rows, indent=1) + "\n")
    for r in rows:
        print(f"{r['stem']}: {r['source_s']} s -> {r['trimmed_s']} s ({r['segments']} segments)")


if __name__ == "__main__":
    main()
