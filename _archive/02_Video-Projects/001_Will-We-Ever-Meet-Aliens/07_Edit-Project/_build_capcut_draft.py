#!/usr/bin/env python3
"""Build CapCut draft for Orbit 001 — scene-plan cut (B-roll spine + sparse Orbit).

Picture follows aliens_scene_manifest_v01.csv, scaled to the full VO master.
Orbit appears only on orbit beats (and is never looped wall-to-wall).
Missing / edit_only scenes fall back to section B-roll — never Eiffel, never blank.
"""
from __future__ import annotations

import copy
import csv
import json
import shutil
import subprocess
import time
import uuid
from collections import defaultdict
from pathlib import Path

ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
DRAFT_ROOT = Path.home() / "Movies/CapCut/User Data/Projects/com.lveditor.draft"
PROJECT_NAME = "Orbit - 001 Will We Ever Meet Aliens"
DRAFT = DRAFT_ROOT / PROJECT_NAME
TEMPLATE_DRAFT = DRAFT_ROOT / "OpptiAI - Video 003 - Find Missing ALT Tags"
SCAFFOLD = TEMPLATE_DRAFT / "draft_info.json.pre_v003_scaffold.bak"
FULL_TMPL = TEMPLATE_DRAFT / "draft_info.json"
MANIFEST = ROOT / "03_Seedance-Prompts/01_Master-Scene-Plan/aliens_scene_manifest_v01.csv"
VO_MASTER = ROOT / "02_Voiceover/05_Master/aliens_voiceover_master_v01.wav"
POLISHED = ROOT / "04_Generated-Clips/03_Polished"
BROLL = POLISHED / "broll"

W, H, FPS = 1920, 1080, 30.0
VO_VOL = 1.0

# Soft cap: don't let Orbit dominate picture time
MAX_ORBIT_SHARE = 0.18


def uid() -> str:
    return str(uuid.uuid4()).upper()


def us(seconds: float) -> int:
    return int(round(float(seconds) * 1_000_000))


def probe(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def probe_wh(path: Path) -> tuple[int, int]:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=p=0",
            str(path),
        ],
        text=True,
    ).strip()
    if not out:
        return W, H
    parts = out.split(",")
    return int(parts[0]), int(parts[1])


def resolve_asset(row: dict, by_section_broll: dict[str, list[Path]], all_broll: list[Path]) -> Path | None:
    """Pick a real on-disk clip for this scene."""
    pref = (row.get("preferred_asset") or "").strip()
    stype = row["type"]
    section = row["section"]

    candidates: list[Path] = []
    if pref and not pref.startswith("MISSING"):
        p = ROOT / pref if not Path(pref).is_absolute() else Path(pref)
        if not p.exists():
            # preferred_asset sometimes relative without ROOT, or basename only
            alt = POLISHED / Path(pref).name
            alt2 = BROLL / Path(pref).name
            if alt.exists():
                p = alt
            elif alt2.exists():
                p = alt2
        if p.exists():
            candidates.append(p)

    # Orbit named beds in polished root
    marker = (row.get("orbit_marker") or "").lower()
    if stype == "orbit":
        mapping = {
            "explaining": POLISHED / "orbit_explaining_talk_v01_polished.mp4",
            "surprised": POLISHED / "orbit_surprised_reaction_v01_polished.mp4",
            "ending": POLISHED / "orbit_ending_goodbye_v01_polished.mp4",
            "thinking": POLISHED / "orbit_surprised_reaction_v01_polished.mp4",  # stand-in
            "intro_wave": POLISHED / "orbit_explaining_talk_v01_polished.mp4",  # stand-in
        }
        for key, path in mapping.items():
            if key in marker or key in pref.lower():
                if path.exists():
                    candidates.append(path)
        # generic explaining fallback for orbit
        exp = POLISHED / "orbit_explaining_talk_v01_polished.mp4"
        if exp.exists():
            candidates.append(exp)

    # Section broll pool
    candidates.extend(by_section_broll.get(section, []))
    candidates.extend(all_broll)

    seen = set()
    for c in candidates:
        rp = c.resolve()
        if rp in seen or not rp.exists():
            continue
        seen.add(rp)
        return rp
    return None


def build_picture_plan(vo_dur: float) -> list[dict]:
    rows = list(csv.DictReader(MANIFEST.open()))
    all_broll = sorted(BROLL.glob("aliens_scene-*.mp4"))
    by_section: dict[str, list[Path]] = defaultdict(list)

    # Index ready broll by section from manifest
    for r in rows:
        if r["type"] != "broll":
            continue
        pref = (r.get("preferred_asset") or "").strip()
        if not pref:
            continue
        p = ROOT / pref
        if not p.exists():
            p = BROLL / f"{r['scene_id']}_v01.mp4"
        if p.exists():
            by_section[r["section"]].append(p)

    # Skip pure buffer orbit spare if we have enough; keep buffer broll
    work = []
    for r in rows:
        if r["scene_id"] == "aliens_scene-059":
            continue  # spare explaining loop — causes repetition
        work.append(r)

    # Resolve assets + raw weights
    items = []
    for r in work:
        path = resolve_asset(r, by_section, all_broll)
        if path is None:
            continue
        weight = max(2.0, float(r["est_duration_sec"]))
        items.append({
            "scene_id": r["scene_id"],
            "section": r["section"],
            "type": r["type"],
            "visual": r["visual"],
            "path": path,
            "weight": weight,
            "orbit_marker": r.get("orbit_marker") or "",
        })

    def pick_broll(scene_id: str, section: str, avoid: set[str], salt: str = "") -> Path | None:
        pool = list(by_section.get(section) or []) + list(all_broll)
        if not pool:
            return None
        # Rotate: prefer unused clip names
        ranked = sorted(pool, key=lambda p: (p.name in avoid, hash(scene_id + salt + p.name) & 0xFFFF))
        return ranked[0]

    # Anti-repetition for consecutive explaining Orbit
    last_orbit_path = None
    orbit_run = 0
    used_broll: set[str] = set()
    keep_orbit_markers = {"surprised", "ending", "intro_wave"}  # keep character moments

    for it in items:
        marker = (it.get("orbit_marker") or "").lower()
        is_orbit = it["type"] == "orbit" or "orbit_" in it["path"].name
        protect = any(k in marker for k in keep_orbit_markers) or "surprised" in it["path"].name or "ending" in it["path"].name

        if is_orbit and not protect:
            if last_orbit_path == it["path"]:
                orbit_run += 1
            else:
                orbit_run = 1
                last_orbit_path = it["path"]
            # After 1 consecutive explaining orbit, swap to fresh broll
            if orbit_run >= 2 and "explaining" in it["path"].name:
                alt = pick_broll(it["scene_id"], it["section"], used_broll, "fb")
                if alt:
                    it["path"] = alt
                    used_broll.add(alt.name)
                    it["type"] = "broll_fallback"
                    it["visual"] = f"[fallback broll] {it['visual']}"
                    orbit_run = 0
                    last_orbit_path = None
        elif is_orbit and protect:
            last_orbit_path = it["path"]
            orbit_run = 1
        else:
            if "orbit_" not in it["path"].name:
                used_broll.add(it["path"].name)
            last_orbit_path = None
            orbit_run = 0

        # Titles / graphics: always broll, rotate away from last clip
        if it["type"] in ("title", "graphic"):
            alt = pick_broll(it["scene_id"], it["section"], used_broll, "tg")
            if alt:
                it["path"] = alt
                used_broll.add(alt.name)

    # Cap total Orbit share (convert excess explaining only; keep surprised/ending/intro)
    total_w = sum(i["weight"] for i in items)
    def is_orbit_item(i: dict) -> bool:
        return i["type"] == "orbit" or (
            i["type"] != "broll_fallback" and "orbit_" in i["path"].name
        )

    orbit_w = sum(i["weight"] for i in items if is_orbit_item(i))
    if total_w > 0 and orbit_w / total_w > MAX_ORBIT_SHARE:
        excess = orbit_w - MAX_ORBIT_SHARE * total_w
        for it in items:
            if excess <= 0:
                break
            marker = (it.get("orbit_marker") or "").lower()
            if it["type"] != "orbit":
                continue
            if any(k in marker for k in keep_orbit_markers):
                continue
            if "explaining" not in it["path"].name and "thinking" not in marker:
                continue
            alt = pick_broll(it["scene_id"], it["section"], used_broll, "cap")
            if not alt:
                continue
            it["path"] = alt
            used_broll.add(alt.name)
            excess -= it["weight"]
            it["type"] = "broll_fallback"
            it["visual"] = f"[orbit-cap broll] {it['visual']}"

    # De-dupe immediate identical broll repeats (swap second)
    for i in range(1, len(items)):
        if items[i]["path"] == items[i - 1]["path"] and "orbit_" not in items[i]["path"].name:
            alt = pick_broll(items[i]["scene_id"], items[i]["section"], {items[i]["path"].name}, "dedupe")
            if alt and alt != items[i]["path"]:
                items[i]["path"] = alt

    # Scale weights to VO duration
    total_w = sum(i["weight"] for i in items)
    scale = vo_dur / total_w if total_w else 1.0
    t = 0.0
    plan = []
    for it in items:
        dur = it["weight"] * scale
        plan.append({
            **it,
            "start": t,
            "duration": dur,
            "path": it["path"],
        })
        t += dur

    # Fix float drift on last clip
    if plan:
        drift = vo_dur - sum(p["duration"] for p in plan)
        plan[-1]["duration"] += drift
    return plan


def main() -> None:
    assert VO_MASTER.exists(), VO_MASTER
    assert SCAFFOLD.exists(), SCAFFOLD
    media = DRAFT / "imported_media"
    assert (media / "video").exists() and (media / "audio").exists(), "Run _stage_capcut_media.py first"

    vo_src = media / "audio" / VO_MASTER.name
    if not vo_src.exists():
        shutil.copy2(VO_MASTER, vo_src)
    vo_dur = probe(vo_src)
    plan = build_picture_plan(vo_dur)

    draft = json.loads(SCAFFOLD.read_text())
    tmpl = json.loads(FULL_TMPL.read_text())
    v_mat_tmpl = tmpl["materials"]["videos"][0]
    a_mat_tmpl = tmpl["materials"]["audios"][0]
    for a in tmpl["materials"]["audios"]:
        if "VO_" in a.get("name", "") or a.get("type") == 0:
            a_mat_tmpl = a
            break
    v_seg_tmpl = next(t for t in tmpl["tracks"] if t["type"] == "video" and t.get("flag") == 0)["segments"][0]
    a_seg_tmpl = next(t for t in tmpl["tracks"] if t["type"] == "audio")["segments"][0]

    draft_id = uid()
    now = int(time.time())
    now_us = int(time.time() * 1_000_000)

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

    videos: list[dict] = []
    audios: list[dict] = []
    speeds: list[dict] = []
    canvases: list[dict] = []
    placeholders: list[dict] = []
    sound_maps: list[dict] = []
    mat_colors: list[dict] = []
    vocal_seps: list[dict] = []
    v_segments: list[dict] = []
    vo_segments: list[dict] = []

    # ---- VIDEO: one segment per scene (trim or soft-loop short clips) ----
    for shot in plan:
        src = shot["path"]
        # Prefer CapCut-imported copy when present
        imported = media / "video" / src.name
        if imported.exists():
            src = imported
        src = src.resolve()
        src_dur = probe(src)
        ww, hh = probe_wh(src)
        need = shot["duration"]

        filled = 0.0
        part = 0
        while filled < need - 0.015:
            chunk = min(src_dur, need - filled)
            # Prefer starting at 0 each loop for beds; for short broll use full clip
            mid = uid()
            mat = copy.deepcopy(v_mat_tmpl)
            mat["id"] = mid
            mat["path"] = str(src)
            mat["duration"] = us(src_dur)
            mat["width"] = ww
            mat["height"] = hh
            mat["material_name"] = f"{shot['scene_id']}_p{part}"
            mat["has_audio"] = False
            videos.append(mat)

            speed_id, ph_id, canvas_id, scm_id, color_id, vocal_id = (
                uid(), uid(), uid(), uid(), uid(), uid()
            )
            speeds.append({"id": speed_id, "mode": 0, "speed": 1.0, "type": "speed"})
            placeholders.append({"id": ph_id})
            canvases.append({
                "id": canvas_id, "type": "canvas_color", "color": "", "blur": 0.0,
                "image": "", "image_id": "", "image_name": "",
                "source_platform": 0, "album_id": "", "album_name": "",
            })
            sound_maps.append({"id": scm_id})
            mat_colors.append({"id": color_id})
            vocal_seps.append({"id": vocal_id})

            seg = copy.deepcopy(v_seg_tmpl)
            seg["id"] = uid()
            seg["material_id"] = mid
            seg["target_timerange"] = {"start": us(shot["start"] + filled), "duration": us(chunk)}
            seg["source_timerange"] = {"start": us(0.0), "duration": us(chunk)}
            seg["speed"] = 1.0
            seg["volume"] = 0.0
            seg["extra_material_refs"] = [speed_id, ph_id, canvas_id, scm_id, color_id, vocal_id]
            v_segments.append(seg)
            filled += chunk
            part += 1
            # safety against infinite loop on tiny clips
            if part > 40:
                break

    # ---- AUDIO: single master VO ----
    mid = uid()
    mat = copy.deepcopy(a_mat_tmpl)
    mat["id"] = mid
    mat["path"] = str(vo_src.resolve())
    mat["duration"] = us(vo_dur)
    mat["name"] = "VO_master"
    mat["material_name"] = "aliens_voiceover_master_v01"
    mat["type"] = a_mat_tmpl.get("type", 0)
    audios.append(mat)
    speed_id = uid()
    speeds.append({"id": speed_id, "mode": 0, "speed": 1.0, "type": "speed"})
    seg = copy.deepcopy(a_seg_tmpl)
    seg["id"] = uid()
    seg["material_id"] = mid
    seg["target_timerange"] = {"start": 0, "duration": us(vo_dur)}
    seg["source_timerange"] = {"start": 0, "duration": us(vo_dur)}
    seg["speed"] = 1.0
    seg["volume"] = VO_VOL
    refs = seg.get("extra_material_refs") or []
    seg["extra_material_refs"] = [speed_id] + (list(refs[1:]) if refs else [])
    vo_segments.append(seg)

    mats = draft.setdefault("materials", {})
    mats["videos"] = videos
    mats["audios"] = audios
    mats["speeds"] = speeds
    mats["canvases"] = canvases
    mats["sound_channel_mappings"] = sound_maps
    mats["material_colors"] = mat_colors
    mats["vocal_separations"] = vocal_seps
    if "placeholders" in mats or "placeholder_infos" in mats:
        mats["placeholders"] = placeholders
    else:
        draft["materials"]["placeholder_infos"] = placeholders

    new_tracks = []
    for tr in draft.get("tracks") or tmpl.get("tracks") or []:
        t = copy.deepcopy(tr)
        if t.get("type") == "video" and t.get("flag", 0) == 0:
            t["segments"] = v_segments
        elif t.get("type") == "audio":
            if not any(x.get("type") == "audio" for x in new_tracks):
                t["segments"] = vo_segments
            else:
                t["segments"] = []
        else:
            t["segments"] = []
        new_tracks.append(t)
    if not any(t.get("type") == "video" for t in new_tracks):
        new_tracks.insert(0, {"id": uid(), "type": "video", "flag": 0, "segments": v_segments})
    if not any(t.get("type") == "audio" for t in new_tracks):
        new_tracks.append({"id": uid(), "type": "audio", "flag": 0, "segments": vo_segments})
    draft["tracks"] = new_tracks
    draft["duration"] = us(vo_dur)

    DRAFT.mkdir(parents=True, exist_ok=True)
    draft_path = DRAFT / "draft_info.json"
    if draft_path.exists():
        bak = DRAFT / f"draft_info.pre_scenecut_{time.strftime('%Y%m%d_%H%M%S')}.json"
        shutil.copy2(draft_path, bak)
    draft_path.write_text(json.dumps(draft, ensure_ascii=False))
    (DRAFT / "draft_info.json.bak").write_text(json.dumps(draft, ensure_ascii=False))

    # Cover from first broll in plan
    cover = DRAFT / "draft_cover.jpg"
    first_vid = next((p["path"] for p in plan if "orbit_" not in p["path"].name), plan[0]["path"])
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", "1", "-i", str(first_vid),
         "-frames:v", "1", str(cover)],
        check=False,
    )

    # Meta + root registry (reuse prior pattern lightly)
    meta_src = json.loads((TEMPLATE_DRAFT / "draft_meta_info.json").read_text())
    meta = copy.deepcopy(meta_src)
    meta["draft_id"] = draft_id
    meta["draft_name"] = PROJECT_NAME
    meta["draft_fold_path"] = str(DRAFT)
    meta["draft_root_path"] = str(DRAFT_ROOT)
    meta["draft_cover"] = "draft_cover.jpg"
    meta["tm_draft_create"] = now_us
    meta["tm_draft_modified"] = now_us
    meta["tm_duration"] = us(vo_dur)

    lib_entries = []
    for p in sorted((DRAFT / "imported_media/audio").glob("*")):
        if p.suffix.lower() not in {".mp3", ".wav", ".m4a"}:
            continue
        d_us = us(probe(p))
        lib_entries.append({
            "ai_group_type": "", "create_time": -1, "duration": d_us, "enter_from": 0,
            "extra_info": p.name, "file_Path": f"./imported_media/audio/{p.name}",
            "height": 0, "id": uid(), "import_time": now, "import_time_ms": now * 1000,
            "item_source": 1, "material_color_tag": "", "md5": "", "metetype": "music",
            "roughcut_time_range": {"duration": d_us, "start": 0},
            "sub_time_range": {"duration": -1, "start": -1}, "type": 0, "width": 0,
        })
    for folder in [DRAFT / "imported_media/video", DRAFT / "imported_media/video/broll"]:
        if not folder.exists():
            continue
        for p in sorted(folder.glob("*.mp4")):
            d_us = us(probe(p))
            ww, hh = probe_wh(p)
            rel = p.relative_to(DRAFT / "imported_media")
            lib_entries.append({
                "ai_group_type": "", "create_time": -1, "duration": d_us, "enter_from": 0,
                "extra_info": p.name, "file_Path": f"./imported_media/{rel.as_posix()}",
                "height": hh, "id": uid(), "import_time": now, "import_time_ms": now * 1000,
                "item_source": 1, "material_color_tag": "", "md5": "", "metetype": "video",
                "roughcut_time_range": {"duration": d_us, "start": 0},
                "sub_time_range": {"duration": -1, "start": -1}, "type": 0, "width": ww,
            })
    blocks = meta.get("draft_materials") or [{"type": 0, "value": []}]
    new_blocks = []
    for block in blocks:
        b = copy.deepcopy(block)
        b["value"] = lib_entries if b.get("type") == 0 else []
        new_blocks.append(b)
    meta["draft_materials"] = new_blocks or [{"type": 0, "value": lib_entries}]
    (DRAFT / "draft_meta_info.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))

    root_path = DRAFT_ROOT / "root_meta_info.json"
    root = json.loads(root_path.read_text())
    store = [
        x for x in (root.get("all_draft_store") or [])
        if x.get("draft_name") != PROJECT_NAME and x.get("draft_fold_path") != str(DRAFT)
    ]
    store.insert(0, {
        "cloud_draft_cover": False, "cloud_draft_sync": False,
        "draft_cloud_last_action_download": False, "draft_cloud_purchase_info": "",
        "draft_cloud_template_id": "", "draft_cloud_tutorial_info": "",
        "draft_cloud_videocut_purchase_info": "", "draft_cover": str(cover),
        "draft_fold_path": str(DRAFT), "draft_id": draft_id,
        "draft_is_ai_shorts": False, "draft_is_cloud_temp_draft": False,
        "draft_is_invisible": False, "draft_is_pippit_draft": False,
        "draft_is_web_article_video": False, "draft_json_file": str(draft_path),
        "draft_name": PROJECT_NAME, "draft_new_version": "",
        "draft_root_path": str(DRAFT_ROOT),
        "draft_timeline_materials_size": draft_path.stat().st_size,
        "draft_type": "", "draft_web_article_video_enter_from": "",
        "pippit_avatar_url": "", "pippit_extra_info": "", "pippit_id": "",
        "pippit_user_name": "", "streaming_edit_draft_ready": False,
        "tm_draft_cloud_completed": "", "tm_draft_cloud_entry_id": "",
        "tm_draft_cloud_modified": "", "tm_draft_cloud_parent_entry_id": "",
        "tm_draft_cloud_space_id": "", "tm_draft_cloud_user_id": "",
        "tm_draft_create": now_us, "tm_draft_modified": now_us,
        "tm_draft_removed": 0, "tm_duration": us(vo_dur),
    })
    root["all_draft_store"] = store
    root["draft_ids"] = len(store)
    shutil.copy2(root_path, DRAFT_ROOT / f"root_meta_info.pre_orbit001_{time.strftime('%Y%m%d_%H%M%S')}.json")
    root_path.write_text(json.dumps(root, ensure_ascii=False, indent=2))

    # Write edit decision list + report
    edl = []
    for p in plan:
        edl.append({
            "scene_id": p["scene_id"],
            "section": p["section"],
            "type": p["type"],
            "start_s": round(p["start"], 3),
            "end_s": round(p["start"] + p["duration"], 3),
            "duration_s": round(p["duration"], 3),
            "clip": p["path"].name,
            "visual": p["visual"],
        })
    (ROOT / "07_Edit-Project/SCENE_EDL_v01.json").write_text(json.dumps(edl, indent=2))

    orbit_secs = sum(
        p["duration"] for p in plan
        if p["type"] == "orbit" or ("orbit_" in p["path"].name and p["type"] != "broll_fallback")
    )
    broll_secs = vo_dur - orbit_secs
    report = {
        "project": PROJECT_NAME,
        "draft_id": draft_id,
        "duration_s": round(vo_dur, 3),
        "scenes": len(plan),
        "video_segments": len(v_segments),
        "orbit_picture_s": round(orbit_secs, 1),
        "broll_picture_s": round(broll_secs, 1),
        "orbit_share": round(orbit_secs / vo_dur, 3) if vo_dur else 0,
        "draft_path": str(DRAFT),
        "edl": str(ROOT / "07_Edit-Project/SCENE_EDL_v01.json"),
        "note": "Scene-plan cut: B-roll spine + sparse Orbit; master VO synced",
    }
    (ROOT / "07_Edit-Project/DRAFT_BUILD_REPORT.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
