#!/usr/bin/env python3
"""Extract Short hook audio → ElevenLabs Scribe words → VO-synced caption beat maps.

Writes per-short ``*_words.json`` + ``*_beats.json`` under each episode's
``10_Shorts/07_Caption-Sync/``. Builders load these when present.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/ben/code/Orbit-YouTube")
CAPTION_LIB = ROOT / "00_Brand/Channel-Setup/TikTok/auto"
AUDIO_TOOLS = ROOT / "04_Audio/tools"
sys.path.insert(0, str(CAPTION_LIB))
sys.path.insert(0, str(AUDIO_TOOLS))

from el_auth import load_token  # noqa: E402
from el_client import multipart_post  # noqa: E402
from onscreen_captions import align_phrases_to_words, punch_first  # noqa: E402

EPISODES = [
    {
        "name": "aliens",
        "builder": ROOT
        / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/_build_aliens_shorts_v02.py",
        "out": ROOT
        / "02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/07_Caption-Sync",
    },
    {
        "name": "blackhole",
        "builder": ROOT
        / "02_Video-Projects/002_What-Happens-If-You-Fall-Into-A-Black-Hole/10_Shorts/_build_blackhole_shorts_v02.py",
        "out": ROOT
        / "02_Video-Projects/002_What-Happens-If-You-Fall-Into-A-Black-Hole/10_Shorts/07_Caption-Sync",
    },
    {
        "name": "exoplanets",
        "builder": ROOT
        / "02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds/10_Shorts/_build_exoplanets_shorts_v02.py",
        "out": ROOT
        / "02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds/10_Shorts/07_Caption-Sync",
    },
]


def load_builder(path: Path) -> dict:
    ns: dict = {"__name__": "builder_ns", "__file__": str(path)}
    code = path.read_text()
    # Avoid running main()
    code = code.replace('if __name__ == "__main__":\n    main()', "")
    exec(compile(code, str(path), "exec"), ns)
    return ns


def resolve_master(ns: dict) -> Path:
    if "resolve_master" in ns and callable(ns["resolve_master"]):
        return ns["resolve_master"]()
    master = ns.get("MASTER")
    if master and Path(master).exists():
        return Path(master)
    raise SystemExit(f"No master in builder ns keys={list(ns)[:20]}")


def extract_hook_audio(master: Path, start: float, duration: float, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    hook = min(10.0, max(duration - 1.0, 4.0))
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            str(start),
            "-t",
            str(hook),
            "-i",
            str(master),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-c:a",
            "pcm_s16le",
            str(dest),
        ],
        check=True,
        capture_output=True,
    )
    return dest


def scribe_words(audio: Path) -> list[dict]:
    token, mode = load_token()
    code, body = multipart_post(
        "/v1/speech-to-text",
        token,
        mode,
        fields={
            "model_id": "scribe_v2",
            "language_code": "eng",
            "timestamps_granularity": "word",
            "diarize": "false",
        },
        files=[("file", audio)],
        timeout=900,
    )
    if code != 200:
        raise SystemExit(f"STT failed {code}: {body[:800]!r}")
    data = json.loads(body.decode())
    return data.get("words") or []


def main() -> None:
    only = set(sys.argv[1:])
    report: dict = {"episodes": []}
    with tempfile.TemporaryDirectory(prefix="shorts-stt-") as tmp:
        tmp_path = Path(tmp)
        for ep in EPISODES:
            if only and ep["name"] not in only:
                continue
            print(f"=== {ep['name']} ===", flush=True)
            ns = load_builder(ep["builder"])
            shorts = ns.get("SHORTS") or []
            master = resolve_master(ns)
            out_dir: Path = ep["out"]
            out_dir.mkdir(parents=True, exist_ok=True)
            ep_rep = {"name": ep["name"], "master": str(master), "shorts": []}
            for item in shorts:
                sid = item["id"]
                slug = item["slug"]
                print(f"  STT S{sid} {slug}…", flush=True)
                wav = tmp_path / f"{ep['name']}-{sid}.wav"
                extract_hook_audio(master, float(item["start"]), float(item["duration"]), wav)
                words = scribe_words(wav)
                phrases = punch_first(item["phrases"], hook=item.get("hook"))
                beats = align_phrases_to_words(
                    phrases,
                    words,
                    duration=float(item["duration"]),
                    hook_end=8.0,
                    punch_first_hook=False,
                )
                words_path = out_dir / f"{ep['name']}_short-{sid}_{slug}_words.json"
                beats_path = out_dir / f"{ep['name']}_short-{sid}_{slug}_beats.json"
                words_path.write_text(json.dumps({"words": words}, indent=2) + "\n")
                beats_path.write_text(
                    json.dumps(
                        {
                            "phrases": phrases,
                            "beats": beats,
                            "synced": sum(1 for b in beats if b.get("synced")),
                            "total": len(beats),
                        },
                        indent=2,
                    )
                    + "\n"
                )
                synced = sum(1 for b in beats if b.get("synced"))
                ep_rep["shorts"].append(
                    {
                        "id": sid,
                        "slug": slug,
                        "words": len(words),
                        "synced": synced,
                        "beats": str(beats_path),
                    }
                )
                print(f"    words={len(words)} synced={synced}/{len(beats)}", flush=True)
            report["episodes"].append(ep_rep)
            (out_dir / "sync_report.json").write_text(json.dumps(ep_rep, indent=2) + "\n")
    summary = ROOT / "00_Brand/Channel-Setup/TikTok/CAPTION_VO_SYNC_REPORT.json"
    summary.write_text(json.dumps(report, indent=2) + "\n")
    print(summary)


if __name__ == "__main__":
    main()
