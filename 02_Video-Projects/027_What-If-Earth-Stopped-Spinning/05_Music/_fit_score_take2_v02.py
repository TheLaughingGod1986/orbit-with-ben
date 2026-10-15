#!/usr/bin/env python3
"""Time-fit 027 take 2 (375 s, Chief's 5,200-credit cap) onto v01i. No further spend.

The cut is 446.3 s. The lay script's last slice needs 449.6 s of bed, so this stretches the
375 s take to 452 s (one atempo, not a loop) and writes a plan whose prompt is the film brief
(Pace 76-88 BPM and the NOT list). Chapter times in BED_PROMPT_v02.txt are the 375 s clock;
times 452/375 land on the v01i cards.

  python3 _fit_score_take2_v02.py
"""
from pathlib import Path
import json, subprocess as sp

HERE = Path(__file__).resolve().parent
SRC = HERE / "earth-spin_score_bed_v02.mp3"
OUT = HERE / "earth-spin_score_bed_v02_fit.wav"
FIT_S = 452.0
BRIEF = (
    "Instrumental science documentary underscore for Orbit with Ben, Earth Stopped Spinning film, "
    "told with calm wonder, never a disaster movie. Opens light and curious for twenty seconds, then "
    "a taut, rising pulse for the sudden-stop thought experiment (about 0:25 to 1:35) that peaks and "
    "eases rather than crashes; then relaxed and airy for the everyday spin (1:35 to 3:00); spacious "
    "and slow for a planet that has stopped turning (3:00 to 4:10); gently ticking and curious for "
    "clocks and tides (4:10 to 6:00); warm and grounded to close on a held chord. Plucked strings, "
    "marimba and soft clockwork percussion carry the pulse; warm woodwinds on top; light piano only "
    "near the end. Pace: 76-88 BPM, a clear steady pulse under British narration. NOT orchestral "
    "string-pad beds, NOT Jupiter music, NOT Saturn ring chimes, NOT Moon Leaving lunar piano, NOT "
    "Sun golden strings, NOT the Mars robot's lonely felt piano and low strings, NOT the Nearest "
    "Star's glassy celesta and bells, NOT Venus slow heat drones, NOT Light Speed clock arpeggios. "
    "No vocals, no choir words, no EDM, no trailer hit, no disaster-movie booms."
)


def dur(p: Path) -> float:
    return float(sp.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], text=True))


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing {SRC.name}")
    src_s = dur(SRC)
    tempo = src_s / FIT_S
    if not 0.5 <= tempo <= 2.0:
        raise SystemExit(f"atempo {tempo:.3f} is outside 0.5-2.0")
    sp.run(["ffmpeg", "-y", "-v", "error", "-i", str(SRC), "-af", f"atempo={tempo:.6f}", "-ar", "48000", str(OUT)], check=True)
    src_plan = json.loads(SRC.with_name(SRC.stem + "_plan.json").read_text())
    plan = {
        "created_at": src_plan.get("created_at"),
        "project": "earth-spin",
        "prompt": BRIEF,
        "length_ms": int(FIT_S * 1000),
        "model_id": "music_v2",
        "force_instrumental": True,
        "audio_file": OUT.name,
        "status": "time-fit",
        "source": SRC.name,
        "source_seconds": round(src_s, 3),
        "fit_seconds": FIT_S,
        "atempo": round(tempo, 6),
        "why": "Chief cap 375 s / 5200 credits (J0265). One atempo to the v01i lay length. Not a loop.",
        "generator_prompt": src_plan.get("prompt"),
    }
    OUT.with_name(OUT.stem + "_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    print(f"fit {src_s:.2f}s -> {dur(OUT):.2f}s atempo {tempo:.4f} -> {OUT.name}")


if __name__ == "__main__":
    main()
