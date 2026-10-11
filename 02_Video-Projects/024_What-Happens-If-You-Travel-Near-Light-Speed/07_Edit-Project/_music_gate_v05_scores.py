#!/usr/bin/env python3
"""J0129 item 8: 024 bed music_gate, clean re-run with every file compared and its score.

Skips the two 027 earth-spin beds parked in 027/05_Music/RETIRED.md. iCloud files that won't read in place
(OWB UAT placeholders) are read from a local copy in /private/tmp when one exists.
  python3 _music_gate_v05_scores.py [--video <cut.mp4>]
"""
import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import music_gate as mg  # noqa: E402

FILM = REPO / "02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed"
BED = FILM / "05_Music/light-speed_score_bed_v01_full.mp3"
OUT = FILM / "07_Edit-Project/full_rough_v05_pack/music_gate_v05.json"
PARKED = {"earth-spin_score_bed_v01.mp3", "earth-spin_score_bed_v01_lift.mp3"}
MUSIC_HINTS = ("music", "bed", "score")


def local(p: Path) -> Path:
    alt = Path("/private/tmp") / p.name
    return alt if mg.UAT in p.parents and alt.exists() else p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video")
    a = ap.parse_args()
    others = [local(p) for p in mg.others_default(FILM) if p.name not in PARKED]
    fa = mg.frames(mg.decode(BED))
    scores, unread = [], []
    for o in others:
        try:
            scores.append(dict(file=str(o), similarity=round(mg.similarity(fa, mg.frames(mg.decode(o))), 3)))
        except Exception as e:  # noqa: BLE001
            unread.append(dict(file=str(o), error=e.__class__.__name__,
                               music=any(h in o.name.lower() for h in MUSIC_HINTS)))
    res = mg.judge(FILM, BED, Path(a.video) if a.video else None, [Path(s["file"]) for s in scores])
    res["parked_skipped"] = sorted(PARKED)
    res["compared"] = sorted(scores, key=lambda s: -s["similarity"])
    res["unread"] = unread
    OUT.write_text(json.dumps(res, indent=1) + "\n")
    print(res["verdict"], "max", res["compared"][0] if res["compared"] else None,
          "unread music:", [u["file"] for u in unread if u["music"]])
    return 0 if res["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
