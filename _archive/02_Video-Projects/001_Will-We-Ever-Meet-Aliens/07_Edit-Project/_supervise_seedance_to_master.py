#!/usr/bin/env python3
"""Supervise Seedance pipeline until 96/96, then rebuild v10 (music + chapters). HTTP-only."""
from __future__ import annotations

import subprocess
import time
from pathlib import Path

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens/07_Edit-Project")
PID_FILE = Path("/tmp/orbit_seedance_pipeline.pid")
LOG = Path("/tmp/orbit_seedance_pipeline_v11.log")
WATCH = Path("/tmp/orbit_seedance_supervise.log")
PY = ROOT / ".venv_orbit/bin/python3"
BUILDER = "_build_bold_explainer_v10_music_chapters.py"
MASTER = ROOT.parent / "09_Final-Export/aliens_BOLD_EXPLAINER_v10_MUSIC_CHAPTERS_MASTER.mp4"


def missing_count() -> int:
    return int(
        subprocess.check_output(
            [str(PY), "-c", "import _animate_bold_scenes_elevenlabs_v10 as m; print(len(m.missing_scenes()))"],
            cwd=str(ROOT),
            text=True,
        ).strip()
    )


def ready_count() -> int:
    anim = ROOT.parent / "04_Generated-Clips/03_Polished/bold_rebuild_v05/animated"
    return len(list(anim.glob("*_seedance-mini.mp4")))


def pipeline_alive() -> bool:
    if not PID_FILE.exists():
        return False
    try:
        pid = int(PID_FILE.read_text().strip())
    except ValueError:
        return False
    return subprocess.call(["kill", "-0", str(pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0


def start_pipeline() -> None:
    logf = open(LOG, "a")
    proc = subprocess.Popen(
        [str(PY), "-u", "_seedance_pipeline_v11.py"],
        cwd=str(ROOT),
        stdout=logf,
        stderr=subprocess.STDOUT,
    )
    PID_FILE.write_text(str(proc.pid))
    WATCH.write_text("") if False else None
    with WATCH.open("a") as handle:
        handle.write(f"{time.strftime('%H:%M:%S')} started pipeline pid={proc.pid}\n")


def harvest_http() -> None:
    subprocess.call(
        [
            str(PY),
            "-c",
            "import _seedance_pipeline_v11 as p; p.harvest_once(p.load_pending())",
        ],
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def rebuild() -> None:
    with WATCH.open("a") as handle:
        handle.write(f"{time.strftime('%H:%M:%S')} rebuilding v10 music+chapters\n")
    subprocess.check_call([str(PY), "-u", BUILDER], cwd=str(ROOT))
    subprocess.call(["open", str(MASTER)])


def main() -> None:
    WATCH.parent.mkdir(parents=True, exist_ok=True)
    while True:
        miss = missing_count()
        ready = ready_count()
        alive = pipeline_alive()
        line = f"{time.strftime('%H:%M:%S')} ready={ready} missing={miss} alive={alive}"
        print(line, flush=True)
        with WATCH.open("a") as handle:
            handle.write(line + "\n")

        if miss == 0:
            rebuild()
            break

        harvest_http()

        if not alive:
            start_pipeline()

        time.sleep(60)


if __name__ == "__main__":
    main()
