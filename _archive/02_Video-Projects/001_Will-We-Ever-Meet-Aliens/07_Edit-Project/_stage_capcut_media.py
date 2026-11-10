#!/usr/bin/env python3
"""Stage full VO + Orbit + all polished B-roll into CapCut draft media."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
DRAFT = (
    Path.home()
    / "Movies/CapCut/User Data/Projects/com.lveditor.draft"
    / "Orbit - 001 Will We Ever Meet Aliens"
)
BIN = ROOT / "07_Edit-Project/CapCut-Media-Bin"


def copy_into(src: Path, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    shutil.copy2(src, dest)
    print("staged", dest.relative_to(DRAFT) if DRAFT in dest.parents else dest)


def main() -> None:
    vdir = DRAFT / "imported_media/video"
    adir = DRAFT / "imported_media/audio"
    broll_dir = vdir / "broll"
    for d in (vdir, adir, broll_dir, BIN / "broll", BIN / "orbit", BIN / "audio"):
        d.mkdir(parents=True, exist_ok=True)

    # Orbit beds
    for p in sorted((ROOT / "04_Generated-Clips/03_Polished").glob("orbit_*.mp4")):
        copy_into(p, vdir)
        copy_into(p, BIN / "orbit")

    # B-roll
    for p in sorted((ROOT / "04_Generated-Clips/03_Polished/broll").glob("*.mp4")):
        copy_into(p, broll_dir)
        copy_into(p, vdir)  # also flat for CapCut browser
        copy_into(p, BIN / "broll")

    # VO master + sections (prefer v02)
    master = ROOT / "02_Voiceover/05_Master/aliens_voiceover_master_v01.wav"
    if master.exists():
        copy_into(master, adir)
        copy_into(master, BIN / "audio")
    master_mp3 = ROOT / "02_Voiceover/05_Master/aliens_voiceover_master_v01.mp3"
    if master_mp3.exists():
        copy_into(master_mp3, adir)
        copy_into(master_mp3, BIN / "audio")

    sec = ROOT / "02_Voiceover/04_Section-Exports"
    for p in sorted(sec.glob("aliens_vo_section-*_v02.wav")):
        copy_into(p, adir)
        copy_into(p, BIN / "audio")

    link = ROOT / "07_Edit-Project/capcut_draft_link"
    if link.exists() or link.is_symlink():
        link.unlink()
    link.symlink_to(DRAFT, target_is_directory=True)
    print("link →", DRAFT)


if __name__ == "__main__":
    main()
