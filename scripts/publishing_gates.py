#!/usr/bin/env python3
"""Shared, fail-closed preflight for uploads and scheduled-video rechecks.

Inputs come from <export>_meta.json under `publishing_gates` when present (see docs/PUBLISHING_GATES.md),
and deterministically from the film folder and sidecars beside the export for existing cuts.
Gate results are always recomputed, never trusted from recorded PASS strings.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".aac", ".flac")
# Gates that inspect the rendered cut itself: a real FAIL (exit 1) means fixing it produces a new cut needing Ben's watch.
WATCH_GATES = frozenset({"shorts_open", "music", "picture", "sfx"})
WAIVER_PREFIXES = ("chief", "[chief]", "claude", "ben")


def run(command: list[str], *, cwd: Path | None = None) -> tuple[int, str]:
    try:
        p = subprocess.run(command, capture_output=True, text=True, timeout=600, cwd=str(cwd) if cwd else None)
        return p.returncode, (p.stdout + p.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 2, f"gate unavailable: {type(exc).__name__}"


def _canonical_studio_name() -> str:
    try:
        return str(json.loads((ROOT / "studio-core" / "CORE_FILES.json").read_text()).get("canonical") or "")
    except (OSError, ValueError):
        return ""


def _studio_roots() -> list[Path]:
    cands: list[Path] = [ROOT]
    for env_key in ("STUDIO_REPO", "ORBIT_REPO"):
        if os.environ.get(env_key):
            cands.append(Path(os.environ[env_key]))
    canonical = _canonical_studio_name()
    if canonical:
        cands.extend([ROOT.parent / canonical, Path.home() / "YouTube" / canonical])
    out: list[Path] = []
    seen: set[Path] = set()
    for c in cands:
        try:
            r = c.resolve()
        except OSError:
            continue
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


def _tool(name: str) -> Path:
    for base in _studio_roots():
        p = base / "scripts" / name
        if p.is_file():
            return p
    return ROOT / "scripts" / name


def _shorts_gate_path(repo: Path, override: Path | None = None) -> Path:
    if override is not None:
        return override
    for base in (repo, *_studio_roots()):
        p = base / "00_Brand" / "Channel-Setup" / "tools" / "gate_shorts_open.py"
        if p.is_file():
            return p
    return repo / "00_Brand" / "Channel-Setup" / "tools" / "gate_shorts_open.py"


def _file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_channel_config(repo: Path) -> tuple[dict, str | None]:
    try:
        data = json.loads((repo / "studio" / "channel.json").read_text())
        if not isinstance(data, dict):
            return {}, "studio/channel.json must be a JSON object"
        return data, None
    except (OSError, ValueError) as exc:
        return {}, str(exc)


def required_gates(config: dict, fmt: str, *, repo: Path | None = None, has_cuts: bool = False) -> tuple[list[str], str | None]:
    """Ordered blocking gates for this channel and format (short | long), driven by studio/channel.json capabilities."""
    pg = config.get("publishing_gates")
    if pg is not None and not isinstance(pg, dict):
        return [], "channel publishing_gates must be an object"
    pg = pg or {}
    by_fmt = pg.get("by_format") if isinstance(pg.get("by_format"), dict) else {}
    configured = by_fmt.get(fmt) if fmt in by_fmt else pg.get(fmt)
    if configured is not None:
        if not isinstance(configured, list):
            return [], f"channel publishing_gates.{fmt} must be a list"
        gates = list(configured)
    else:
        has_package_lint = bool(repo and (repo / "07_Content-Ops" / "scripts" / "package-lint.ts").is_file())
        long_only = isinstance(config.get("shorts"), dict) and config["shorts"].get("planned_per_long") == 0
        open_gate_lib = isinstance(config.get("analytics"), dict) and config["analytics"].get("open_gate_library") is True
        if has_package_lint:
            gates = ["shorts_open", "music", "sfx", "lint_package"] if fmt == "short" else ["music", "sfx", "lint_package"]
        elif long_only:
            gates = ["shorts_open", "music"] if fmt == "short" else ["music", "archive_provenance"]
        elif open_gate_lib:
            gates = ["shorts_open", "music", "sfx"] if fmt == "short" else ["music", "picture", "sfx"]
            if fmt == "short" and has_cuts and "picture" not in gates:
                gates.append("picture")
        else:
            gates = ["shorts_open", "music", "picture", "sfx"] if fmt == "short" else ["music", "picture", "sfx"]
    extra = pg.get("required", [])
    if not isinstance(extra, list):
        return [], "channel required gates must be a list"
    for g in extra:
        if g not in gates:
            gates.append(g)
    return gates, None


def gates_fingerprint(repo: Path, fmt: str) -> str:
    """Short hash of the channel's gate list + gate script hashes so tightening/adding a gate is auditable."""
    config, _ = _load_channel_config(repo)
    gates, _ = required_gates(config, fmt, repo=repo)
    h = hashlib.sha256()
    h.update(json.dumps({"slug": config.get("slug", ""), "format": fmt, "gates": gates}, sort_keys=True).encode())
    for p in (_shorts_gate_path(repo), _tool("music_gate.py"), _tool("picture_qa.py"), _tool("sfx_kit.py"), Path(__file__).resolve()):
        if p.is_file():
            h.update(p.name.encode())
            h.update(_file_sha256(p).encode())
    return h.hexdigest()[:16]


def _resolve_explicit(value: str, base: Path) -> Path:
    p = Path(value).expanduser()
    return p if p.is_absolute() else (base / p).resolve()


def _find_film_dir(video: Path, package_dir: Path | None, config: dict) -> Path | None:
    """Walk up from the export (or package dir) to locate the film folder (<film>/05_Music or 02_Video-Projects/<film>)."""
    starts = [p for p in (video.parent, package_dir) if p is not None]
    for start in starts:
        cur = start.resolve()
        for _ in range(8):
            if cur.parent.name == "02_Video-Projects" and not cur.name.startswith("_"):
                return cur
            if (cur / "05_Music").is_dir() or (cur / "status.json").is_file() or (cur / "03_Picture").is_dir():
                return cur
            if cur.parent == cur:
                break
            cur = cur.parent
    # If the export lives under _dated_shorts/<slug>/06_Final-Exports/, its parent is the short folder.
    for start in starts:
        cur = start.resolve()
        for _ in range(4):
            if (cur / "05_Music").is_dir():
                return cur
            if cur.parent == cur:
                break
            cur = cur.parent
    # Fallback: check NAS studio-live mirror when film folder name matches.
    nas_folder = str(config.get("nas_folder") or config.get("slug") or "")
    if nas_folder:
        for start in starts:
            for part in start.parts:
                if re.match(r"^(?:\d{3}|[A-Z]\d{2})_", part):
                    cand = Path("/Volumes/data/studio-live") / nas_folder / "02_Video-Projects" / part
                    if cand.is_dir():
                        return cand
    return None


def _music_dir_for(film_dir: Path, config: dict) -> Path:
    local = film_dir / "05_Music"
    if local.is_dir() and any(not p.name.startswith("._") and p.suffix.lower() in AUDIO_EXTS for p in local.iterdir()):
        return local
    nas_folder = str(config.get("nas_folder") or config.get("slug") or "")
    if nas_folder and film_dir.name:
        nas = Path("/Volumes/data/studio-live") / nas_folder / "02_Video-Projects" / film_dir.name / "05_Music"
        if nas.is_dir():
            return nas
    return local


def _find_bed(film_dir: Path | None, meta: dict, meta_base: Path, video: Path, config: dict) -> Path | None:
    if isinstance(meta.get("bed"), str) and meta["bed"].strip():
        p = _resolve_explicit(meta["bed"], meta_base)
        if p.is_file():
            return p
        if film_dir and (film_dir / "05_Music" / meta["bed"]).is_file():
            return film_dir / "05_Music" / meta["bed"]
        return p
    if not film_dir:
        return None
    mdir = _music_dir_for(film_dir, config)
    if not mdir.is_dir():
        return None
    # Prefer a planned bed (audio next to *_plan.json); fall back to any audio in 05_Music so music_gate reports missing plan.
    planned: list[Path] = []
    unplanned: list[Path] = []
    for p in sorted(mdir.iterdir()):
        if p.name.startswith("._") or not p.is_file() or p.suffix.lower() not in AUDIO_EXTS:
            continue
        if p.with_name(p.stem + "_plan.json").is_file():
            planned.append(p)
        else:
            unplanned.append(p)
    pool = planned or unplanned
    if not pool:
        return None
    # Prefer exact stem match if a Short has its own bed in 05_Music, else prefer .mp3 then .wav, newest name last.
    vstem = video.stem.lower()
    exact = [p for p in pool if p.stem.lower() in vstem or vstem in p.stem.lower()]
    picks = exact or pool
    picks.sort(key=lambda p: (0 if p.suffix.lower() == ".mp3" else 1 if p.suffix.lower() == ".wav" else 2, p.name))
    return picks[-1]


def _pick_existing(*cands: Path | None) -> Path | None:
    for c in cands:
        if c is not None and c.is_file():
            return c
    return None


def _find_adjacent(video: Path, suffixes: tuple[str, ...]) -> Path | None:
    for suf in suffixes:
        cand = video.with_name(video.stem + suf)
        if cand.is_file():
            return cand
    return None


def _film_number(film_dir: Path | None, package_dir: Path | None, video: Path) -> str:
    for p in (film_dir, package_dir, video):
        if not p:
            continue
        for part in reversed(p.parts):
            m = re.match(r"^(\d{3})_", part)
            if m:
                return m.group(1)
    return ""


def _shorts_waivers(video: Path, output: str) -> list[dict] | None:
    fails = [line.strip()[5:].strip() for line in output.splitlines()
             if line.startswith(" ") and line.strip().startswith("FAIL ")]
    if not fails:
        return None
    side = video.with_name(video.stem + "_gate.json")
    if not side.is_file():
        return None
    try:
        data = json.loads(side.read_text())
        records = data if isinstance(data, list) else [data]
        book = {
            str(w.get("fail", "")).strip(): w
            for r in records if isinstance(r, dict)
            for w in (r.get("waivers") or []) if isinstance(w, dict)
            if str(w.get("waived_by", "")).strip().lower().startswith(WAIVER_PREFIXES)
        }
        if all(f in book for f in fails):
            return [book[f] for f in fails]
    except (OSError, ValueError, TypeError, AttributeError):
        return None
    return None


def _run_archive_provenance(film_dir: Path, repo: Path) -> tuple[int, str]:
    """Field Order History (WW2) rule 5: every archive image logged in 03_Picture/ARCHIVE_PROVENANCE.md."""
    cands = [film_dir / "03_Picture" / "ARCHIVE_PROVENANCE.md"]
    if film_dir.name:
        cands.append(repo / "02_Video-Projects" / film_dir.name / "03_Picture" / "ARCHIVE_PROVENANCE.md")
    for p in cands:
        if p.is_file():
            text = p.read_text(errors="replace").strip()
            if len(text) >= 20:
                return 0, f"PASS archive_provenance: {p.name} ({len(text)} chars)"
            return 1, f"FAIL archive_provenance: {p} is empty"
    return 1, f"FAIL archive_provenance: missing 03_Picture/ARCHIVE_PROVENANCE.md for {film_dir.name}"


def evaluate(
    video: Path,
    repo: Path,
    fmt: str,
    air: str,
    *,
    video_id: str = "",
    length_test: bool = False,
    meta_path: Path | None = None,
    package_dir: Path | None = None,
    expected_sha256: str | None = None,
    shorts_gate_script: Path | None = None,
    short_run=run,
) -> dict:
    """Run every applicable blocking check; unavailable evidence is a blocking finding too."""
    results: list[dict] = []
    video, repo = video.absolute(), repo.absolute()
    package_dir = package_dir.absolute() if package_dir else None

    if not video.is_file():
        return dict(
            ok=False, waived=False, needs_watch=False, failed_gates=["inputs"],
            gates_fingerprint=gates_fingerprint(repo, fmt),
            checks=[dict(gate="inputs", ok=False, exit_code=2, output=f"Export file not found: {video}")],
        )

    config, config_err = _load_channel_config(repo)
    if config_err:
        results.append(dict(gate="channel", ok=False, exit_code=2, output=config_err))

    # Load optional sidecar metadata (strictly validated when present).
    resolved_meta = meta_path
    if resolved_meta is None:
        for cand in (video.with_name(video.stem + "_meta.json"), video.parent.parent / f"{video.stem}_meta.json"):
            if cand.is_file():
                resolved_meta = cand
                break
    meta: dict = {}
    inputs: dict = {}
    meta_base = resolved_meta.parent if resolved_meta else video.parent
    if resolved_meta is not None:
        try:
            loaded = json.loads(resolved_meta.read_text())
            if not isinstance(loaded, dict):
                raise ValueError("export metadata must be an object")
            meta = loaded
            raw_inputs = meta.get("publishing_gates")
            if raw_inputs is not None:
                if not isinstance(raw_inputs, dict):
                    raise ValueError("publishing_gates must be an object")
                inputs = raw_inputs
        except (OSError, ValueError) as exc:
            return dict(
                ok=False, waived=False, needs_watch=False, failed_gates=["inputs"],
                gates_fingerprint=gates_fingerprint(repo, fmt),
                checks=[dict(gate="inputs", ok=False, exit_code=2, output=f"Missing/invalid export metadata: {exc}")],
            )

    # Verify export hash whenever recorded in metadata, explicit publishing_gates, or UPLOADS.json.
    recorded_sha = meta.get("sha256") or meta.get("sha256_mp4") or expected_sha256
    if inputs and not meta.get("sha256") and not meta.get("sha256_mp4"):
        results.append(dict(gate="identity", ok=False, exit_code=2, output="export sha256 missing in metadata"))
    elif recorded_sha:
        try:
            digest = _file_sha256(video)
            if str(recorded_sha).strip().lower() != digest:
                results.append(dict(gate="identity", ok=False, exit_code=2, output="export sha256 does not match metadata"))
        except OSError as exc:
            results.append(dict(gate="identity", ok=False, exit_code=2, output=str(exc)))

    # Resolve inputs: explicit publishing_gates first, then deterministic derivation from sidecars/film folder.
    film_dir = _resolve_explicit(inputs["film"], meta_base) if isinstance(inputs.get("film"), str) and inputs["film"] else _find_film_dir(video, package_dir, config)
    bed = _resolve_explicit(inputs["bed"], meta_base) if isinstance(inputs.get("bed"), str) and inputs["bed"] else _find_bed(film_dir, meta, meta_base, video, config)
    cuts = _resolve_explicit(inputs["cuts"], meta_base) if isinstance(inputs.get("cuts"), str) and inputs["cuts"] else _find_adjacent(video, ("_cuts.json",))
    pool = _resolve_explicit(inputs["pool"], meta_base) if isinstance(inputs.get("pool"), str) and inputs["pool"] else _find_adjacent(video, ("_pool.json",))
    reviewed_ok = _resolve_explicit(inputs["reviewed_ok"], meta_base) if isinstance(inputs.get("reviewed_ok"), str) and inputs["reviewed_ok"] else _find_adjacent(video, ("_reviewed_ok.json",))
    terminal_loop = _resolve_explicit(inputs["terminal_loop"], meta_base) if isinstance(inputs.get("terminal_loop"), str) and inputs["terminal_loop"] else None

    stems = (meta.get("audio") or {}).get("stems") if isinstance(meta.get("audio"), dict) else {}
    stems = stems if isinstance(stems, dict) else {}
    vo_raw = inputs.get("vo") or meta.get("vo") or meta.get("vo_stem") or stems.get("vo")
    sfx_raw = inputs.get("sfx") or meta.get("sfx") or stems.get("sfx")
    bed_stem_raw = inputs.get("bed_stem") or stems.get("bed")
    vo = _resolve_explicit(vo_raw, meta_base) if isinstance(vo_raw, str) and vo_raw else _find_adjacent(video, ("_vo.wav", "_vo.mp3"))
    sfx = _resolve_explicit(sfx_raw, meta_base) if isinstance(sfx_raw, str) and sfx_raw else _find_adjacent(video, ("_sfx.wav", "_sfx.mp3"))
    bed_stem = _resolve_explicit(bed_stem_raw, meta_base) if isinstance(bed_stem_raw, str) and bed_stem_raw else (_find_adjacent(video, ("_bed.wav", "_bed.mp3")) or bed)

    gates, gates_err = required_gates(config, fmt, repo=repo, has_cuts=cuts is not None)
    if gates_err:
        results.append(dict(gate="channel", ok=False, exit_code=2, output=gates_err))

    def record(name: str, command: list[str], runner=run, *, cwd: Path | None = None) -> dict:
        code, output = runner(command, cwd=cwd) if cwd is not None else runner(command)
        waived_flag = code == 0 and any(ln.startswith("WAIVED ") for ln in output.splitlines())
        entry = dict(gate=name, ok=code == 0, exit_code=code, output=output, waived=waived_flag)
        results.append(entry)
        return entry

    with tempfile.TemporaryDirectory(prefix="publishing-gates-") as tmp:
        for name in gates:
            try:
                if name == "shorts_open":
                    gate_bin = _shorts_gate_path(repo, shorts_gate_script)
                    command = [sys.executable, str(gate_bin), "check", str(video), "--air-date", air]
                    if resolved_meta is not None:
                        command += ["--meta", str(resolved_meta)]
                    if video_id:
                        command += ["--id", video_id]
                    if length_test:
                        command += ["--length-test"]
                    entry = record("shorts_open", command, short_run)
                    if entry["exit_code"] == 1:
                        used = _shorts_waivers(video, entry["output"])
                        if used:
                            entry.update(ok=True, waived=True, waivers=used)
                elif name == "music":
                    if film_dir is None:
                        raise ValueError("publishing_gates.film is required (film folder with 05_Music not found)")
                    if bed is None:
                        raise ValueError(f"publishing_gates.bed is required (no music bed found in {film_dir / '05_Music'})")
                    music_film = bed.parent.parent if bed.parent.name == "05_Music" else film_dir
                    command = [sys.executable, str(_tool("music_gate.py")), str(music_film),
                               "--bed", str(bed), "--video", str(video)]
                    record("music", command)
                elif name == "picture":
                    if cuts is None:
                        raise ValueError("publishing_gates.cuts is required (no cuts.json found)")
                    command = [sys.executable, str(_tool("picture_qa.py")), str(video),
                               "--cuts", str(cuts), "--out-dir", tmp]
                    for path_val, flag in ((pool, "--pool"), (reviewed_ok, "--reviewed-ok"), (terminal_loop, "--terminal-loop")):
                        if path_val is not None:
                            command += [flag, str(path_val)]
                    record("picture", command)
                elif name == "sfx":
                    if vo is None:
                        raise ValueError("publishing_gates.vo is required (no VO stem found)")
                    if sfx is None:
                        raise ValueError("publishing_gates.sfx is required (no SFX stem found)")
                    command = [sys.executable, str(_tool("sfx_kit.py")), "level",
                               "--vo", str(vo), "--sfx", str(sfx)]
                    if bed_stem is not None:
                        command += ["--bed", str(bed_stem)]
                    record("sfx", command)
                elif name == "lint_package":
                    linter = repo / "07_Content-Ops" / "scripts" / "package-lint.ts"
                    film_no = _film_number(film_dir, package_dir, video)
                    if not linter.is_file():
                        raise ValueError(f"lint_package script not found at {linter}")
                    if not film_no:
                        raise ValueError("lint_package requires a numbered film folder (NNN_*)")
                    record("lint_package", ["npx", "tsx", str(linter), "--film", film_no], cwd=repo / "07_Content-Ops")
                elif name == "archive_provenance":
                    if film_dir is None:
                        raise ValueError("archive_provenance requires a film folder")
                    code, output = _run_archive_provenance(film_dir, repo)
                    results.append(dict(gate="archive_provenance", ok=code == 0, exit_code=code, output=output, waived=False))
                else:
                    raise ValueError(f"Unknown required gate {name!r}; add its runner before shipping")
            except (OSError, ValueError) as exc:
                results.append(dict(gate=name, ok=False, exit_code=2, output=str(exc), waived=False))

    ok = all(c["ok"] for c in results)
    waived_any = ok and any(c.get("waived") for c in results)
    failed_gates = [c["gate"] for c in results if not c["ok"]]
    # Ben's watch will be needed when a cut-level gate actually ran and failed (exit 1), not on metadata/coverage gaps alone.
    needs_watch = any((not c["ok"]) and c["gate"] in WATCH_GATES and c.get("exit_code") == 1 for c in results)
    return dict(
        ok=ok,
        waived=waived_any,
        needs_watch=needs_watch,
        failed_gates=failed_gates,
        gates_fingerprint=gates_fingerprint(repo, fmt),
        checks=results,
    )


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--video", type=Path, required=True)
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--format", choices=["short", "long"], required=True)
    p.add_argument("--air-date", default=datetime.now(ZoneInfo("Europe/London")).date().isoformat())
    p.add_argument("--id", default="")
    p.add_argument("--length-test", action="store_true")
    p.add_argument("--package-dir", type=Path, default=None)
    p.add_argument("--meta", type=Path, default=None)
    a = p.parse_args(argv)
    result = evaluate(
        a.video, a.repo, a.format, a.air_date,
        video_id=a.id, length_test=a.length_test,
        meta_path=a.meta, package_dir=a.package_dir,
    )
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
