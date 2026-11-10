#!/usr/bin/env python3
"""Rebuild CapCut draft from SECTION_EDL_v03_noloop.json.
HARD RULES: never reuse clips; never loop cutscenes (Orbit PiP may loop).
"""
from __future__ import annotations

import copy
import json
import shutil
import subprocess
import time
import uuid
from pathlib import Path

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
DRAFT_ROOT = Path.home() / "Movies/CapCut/User Data/Projects/com.lveditor.draft"
PROJECT_NAME = "Orbit - 001 Will We Ever Meet Aliens"
DRAFT = DRAFT_ROOT / PROJECT_NAME
TEMPLATE_DRAFT = DRAFT_ROOT / "OpptiAI - Video 003 - Find Missing ALT Tags"
SCAFFOLD = TEMPLATE_DRAFT / "draft_info.json.pre_v003_scaffold.bak"
FULL_TMPL = TEMPLATE_DRAFT / "draft_info.json"
EDL = ROOT / "07_Edit-Project/SECTION_EDL_v09_flying_orbit.json"
VO = ROOT / "02_Voiceover/05_Master/aliens_voiceover_master_storyteller_v03.wav"
POLISHED = ROOT / "04_Generated-Clips/03_Polished"

W, H, FPS = 1920, 1080, 30.0
PIP_SCALE = 0.22
PIP_X = 0.72
PIP_Y = -0.62


def uid() -> str:
    return str(uuid.uuid4()).upper()


def us(seconds: float) -> int:
    return int(round(float(seconds) * 1_000_000))


def probe(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)], text=True).strip())


def probe_wh(path: Path) -> tuple[int, int]:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path)],
        text=True).strip()
    a, b = out.split(",")
    return int(a), int(b)


def resolve_clip(name: str, kind: str) -> Path:
    candidates = [
        POLISHED / "broll_vibrant" / name,
        POLISHED / "broll_mystery" / name,
        POLISHED / "broll" / name,
        POLISHED / "chapter_cards" / name,
        POLISHED / "unique_cards" / name,
        POLISHED / "brand" / name,
        POLISHED / name,
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError(f"missing clip {name} ({kind})")


def make_video_mat(tmpl, path: Path, name: str) -> dict:
    mid = uid()
    mat = copy.deepcopy(tmpl)
    mat["id"] = mid
    mat["path"] = str(path.resolve())
    mat["duration"] = us(probe(path))
    ww, hh = probe_wh(path)
    mat["width"] = ww
    mat["height"] = hh
    mat["material_name"] = name
    mat["has_audio"] = False
    return mat


def make_vseg(tmpl, mat_id: str, start: float, dur: float, src_dur: float, pip: bool) -> tuple[dict, list]:
    extras = []
    speed_id, ph_id, canvas_id, scm_id, color_id, vocal_id = uid(), uid(), uid(), uid(), uid(), uid()
    extras += [
        {"kind": "speed", "obj": {"id": speed_id, "mode": 0, "speed": 1.0, "type": "speed"}},
        {"kind": "ph", "obj": {"id": ph_id}},
        {"kind": "canvas", "obj": {
            "id": canvas_id, "type": "canvas_color", "color": "", "blur": 0.0,
            "image": "", "image_id": "", "image_name": "",
            "source_platform": 0, "album_id": "", "album_name": "",
        }},
        {"kind": "scm", "obj": {"id": scm_id}},
        {"kind": "color", "obj": {"id": color_id}},
        {"kind": "vocal", "obj": {"id": vocal_id}},
    ]
    chunk = min(src_dur, dur)
    seg = copy.deepcopy(tmpl)
    seg["id"] = uid()
    seg["material_id"] = mat_id
    seg["target_timerange"] = {"start": us(start), "duration": us(dur)}
    seg["source_timerange"] = {"start": 0, "duration": us(chunk)}
    seg["speed"] = 1.0
    seg["volume"] = 0.0
    seg["extra_material_refs"] = [speed_id, ph_id, canvas_id, scm_id, color_id, vocal_id]
    seg["clip"] = {
        "scale": {"x": PIP_SCALE if pip else 1.0, "y": PIP_SCALE if pip else 1.0},
        "rotation": 0.0,
        "transform": {"x": PIP_X if pip else 0.0, "y": PIP_Y if pip else 0.0},
        "flip": {"vertical": False, "horizontal": False},
        "alpha": 1.0,
    }
    if pip:
        seg["render_index"] = 1
    return seg, extras


def main() -> None:
    data = json.loads(EDL.read_text())
    shots = data["shots"]
    assert VO.exists(), VO

    # Hard uniqueness check
    names = [s["clip"] for s in shots]
    assert len(names) == len(set(names)), "REUSE in EDL — abort CapCut build"

    media = DRAFT / "imported_media"
    vdir = media / "video"
    adir = media / "audio"
    vdir.mkdir(parents=True, exist_ok=True)
    adir.mkdir(parents=True, exist_ok=True)

    for s in shots:
        src = resolve_clip(s["clip"], s["kind"])
        shutil.copy2(src, vdir / s["clip"])
        orb = s.get("orbit")
        if orb:
            osrc = POLISHED / orb
            if osrc.exists():
                shutil.copy2(osrc, vdir / orb)
    shutil.copy2(VO, adir / VO.name)

    draft = json.loads(SCAFFOLD.read_text())
    tmpl = json.loads(FULL_TMPL.read_text())
    v_mat_tmpl = tmpl["materials"]["videos"][0]
    a_mat_tmpl = tmpl["materials"]["audios"][0]
    v_tracks = [t for t in tmpl["tracks"] if t.get("type") == "video"]
    v_seg_tmpl = v_tracks[0]["segments"][0]
    a_seg_tmpl = next(t for t in tmpl["tracks"] if t["type"] == "audio")["segments"][0]

    draft_id = uid()
    now = int(time.time())
    vo_dur = probe(VO)

    draft["id"] = draft_id
    draft["name"] = PROJECT_NAME
    draft["fps"] = FPS
    draft["create_time"] = now
    draft["update_time"] = now
    draft["canvas_config"] = {"ratio": "16:9", "width": W, "height": H, "background": None}
    draft["platform"] = copy.deepcopy(tmpl.get("platform"))
    draft["last_modified_platform"] = copy.deepcopy(tmpl.get("last_modified_platform"))
    draft["path"] = str(DRAFT)
    draft["render_index_track_mode_on"] = True
    draft["duration"] = us(vo_dur)

    videos, audios, speeds, canvases = [], [], [], []
    placeholders, sound_maps, mat_colors, vocal_seps = [], [], [], []
    broll_segs, orbit_segs = [], []

    def absorb(extras):
        for e in extras:
            k, o = e["kind"], e["obj"]
            if k == "speed":
                speeds.append(o)
            elif k == "ph":
                placeholders.append(o)
            elif k == "canvas":
                canvases.append(o)
            elif k == "scm":
                sound_maps.append(o)
            elif k == "color":
                mat_colors.append(o)
            elif k == "vocal":
                vocal_seps.append(o)

    # Cutscenes: ONE play each — never loop
    for s in shots:
        src = vdir / s["clip"]
        src_dur = probe(src)
        dur = min(float(s["duration_s"]), src_dur)
        mat = make_video_mat(v_mat_tmpl, src, s["clip"])
        videos.append(mat)
        seg, extras = make_vseg(v_seg_tmpl, mat["id"], float(s["start_s"]), dur, src_dur, pip=False)
        absorb(extras)
        broll_segs.append(seg)

    # Orbit PiP — may loop; skip brand intro/outro
    i = 0
    while i < len(shots):
        orb = shots[i].get("orbit")
        if not orb or shots[i]["kind"] in ("brand_intro", "brand_outro", "chapter", "card"):
            i += 1
            continue
        start = float(shots[i]["start_s"])
        j = i
        while j < len(shots) and shots[j].get("orbit") == orb and shots[j]["kind"] not in ("brand_intro", "brand_outro", "chapter", "card"):
            j += 1
        end = float(shots[j - 1]["start_s"]) + float(shots[j - 1]["duration_s"])
        need = end - start
        src = vdir / orb
        if not src.exists():
            src = POLISHED / orb
        src_dur = probe(src)
        filled = 0.0
        part = 0
        while filled < need - 0.02:
            chunk = min(src_dur, need - filled)
            mat = make_video_mat(v_mat_tmpl, src, f"pip_{orb}_{part}")
            videos.append(mat)
            seg, extras = make_vseg(v_seg_tmpl, mat["id"], start + filled, chunk, src_dur, pip=True)
            absorb(extras)
            orbit_segs.append(seg)
            filled += chunk
            part += 1
            if part > 80:
                break
        i = j

    # Audio
    a_mat = copy.deepcopy(a_mat_tmpl)
    a_mat["id"] = uid()
    a_mat["path"] = str((adir / VO.name).resolve())
    a_mat["name"] = VO.name
    a_mat["duration"] = us(vo_dur)
    audios.append(a_mat)
    a_seg = copy.deepcopy(a_seg_tmpl)
    a_seg["id"] = uid()
    a_seg["material_id"] = a_mat["id"]
    a_seg["target_timerange"] = {"start": 0, "duration": us(vo_dur)}
    a_seg["source_timerange"] = {"start": 0, "duration": us(vo_dur)}
    a_seg["volume"] = 1.0

    draft["materials"] = {
        "videos": videos,
        "audios": audios,
        "speeds": speeds,
        "canvases": canvases,
        "placeholder_infos": placeholders,
        "sound_channel_mappings": sound_maps,
        "material_colors": mat_colors,
        "vocal_separations": vocal_seps,
        "texts": [],
        "images": [],
        "effects": [],
        "transitions": [],
        "filters": [],
        "stickers": [],
        "beats": [],
        "chromas": [],
        "green_screens": [],
        "handwrites": [],
        "realtime_denoises": [],
        "log_color_wheels": [],
        "manual_deformations": [],
        "material_animations": [],
        "primary_color_wheels": [],
        "hsl": [],
        "digital_effects": [],
    }
    # Keep any required empty lists from template if present
    for k, v in tmpl.get("materials", {}).items():
        if k not in draft["materials"]:
            draft["materials"][k] = [] if isinstance(v, list) else v

    draft["tracks"] = [
        {"id": uid(), "type": "video", "segments": broll_segs, "attribute": 0, "flag": 0},
        {"id": uid(), "type": "video", "segments": orbit_segs, "attribute": 0, "flag": 0},
        {"id": uid(), "type": "audio", "segments": [a_seg], "attribute": 0, "flag": 0},
    ]

    out = DRAFT / "draft_info.json"
    out.write_text(json.dumps(draft, ensure_ascii=False))
    meta = {
        "project": PROJECT_NAME,
        "draft_id": draft_id,
        "edl": str(EDL),
        "vo": str(VO),
        "shots": len(shots),
        "unique_clips": len(set(names)),
        "rules": ["no_reuse", "no_loop_cutscenes"],
        "updated": now,
    }
    (ROOT / "07_Edit-Project/DRAFT_BUILD_REPORT.json").write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
