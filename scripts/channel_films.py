#!/usr/bin/env python3
"""Each channel's films, read the way its channel file says (docs/MULTI_CHANNEL_PLAN.md phase 1).

`channels/<slug>/channel.json` names how a channel keeps its film state (`pipeline.kind`):
  film_status    one `02_Video-Projects/NNN_*/status.json` per film, stages {key: {state: ...}} (Orbit With Ben)
  pipeline_json  one file listing every film, stages {key: {status: ...}} (History of Science PIPELINE.json)

`films(slug, root)` gives the same rows for either: {key 'HOS:011', id '011', title, air 'YYYY-MM-DD' or '',
stages {key: 'done'|'doing'|...}, raw (the record as stored)}. A new channel picks one of the kinds (or adds a reader
here), and everything that reads films through this module picks it up.
"""
from __future__ import annotations

import json
from pathlib import Path

import channels


def _state(v) -> str:
    return str((v or {}).get("state") or (v or {}).get("status") or "") if isinstance(v, dict) else str(v or "")


def _row(slug: str, fid: str, title: str, air: str, stages: dict, raw: dict) -> dict:
    return {"key": f"{channels.label(slug)}:{fid}", "id": fid, "title": title, "air": str(air or "")[:10],
            "stages": {k: _state(v) for k, v in (stages or {}).items()}, "raw": raw}


def _film_status(slug: str, root: Path, pattern: str) -> list[dict]:
    out = []
    for p in sorted(root.glob(pattern)):
        try:
            d = json.loads(p.read_text())
        except (OSError, ValueError):
            continue
        fid = str(d.get("film") or p.parent.name[:3])
        out.append(_row(slug, fid, d.get("title", ""), d.get("air", ""), d.get("stages") or {}, d))
    return out


def _pipeline_json(slug: str, root: Path, path: str) -> list[dict]:
    try:
        d = json.loads((root / path).read_text())
    except (OSError, ValueError):
        return []
    return [_row(slug, str(f.get("id")), f.get("title", ""), f.get("air", ""), f.get("stages") or {}, f)
            for f in d.get("films") or []]


READERS = {"film_status": _film_status, "pipeline_json": _pipeline_json}


def films(slug: str, root: Path | None = None) -> list[dict]:
    c = channels.get(slug)
    p = c.get("pipeline") or {}
    reader = READERS.get(p.get("kind"))
    if not reader:
        raise ValueError(f"channel {slug}: unknown pipeline kind {p.get('kind')!r} (have {', '.join(READERS)})")
    base = Path(root) if root else (Path(__file__).resolve().parent.parent if c.get("home") else channels.repo_path(slug))
    return reader(slug, base, p["path"])
