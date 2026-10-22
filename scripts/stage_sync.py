#!/usr/bin/env python3
"""Move OWB film stages that the record already proves finished, so the board's progress is real (J0814).

Ben, 21 Oct 2026: "Since yesterday does not seem to be showing progress". Stages only moved when a job carried
film + stage, so films sat at review for days after they were cut, passed and even uploaded.

Two rules, and nothing parsed from job text (that matched the wrong stages):
1. A later stage done proves the earlier ones: a film can't be edited without its picture, or uploaded without
   its edit and thumbnail. Thumbnails run alongside the edit, so only an upload proves them.
2. Ben's OK on the board (/api/checks verdict ok) proves the film is edited: every stage up to edit is done.

Only todo/doing/review/blocked stages move, never skip. Dry run by default; --apply writes status.json and STATUS.md,
--git also commits and pushes them.

  python3 scripts/stage_sync.py                      # what would move
  python3 scripts/stage_sync.py --apply --git        # move it
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request

import studio

CHECKS_URL = "https://studio-kanban.vercel.app/api/checks"
OPEN = ("todo", "doing", "review", "blocked")
# Stages a later finished stage proves. Thumbnails are made alongside the edit, so only upload proves them.
PARALLEL = {"thumbs"}


def implied(stages: dict, ben_ok: str = "") -> dict:
    """{stage: reason} for open stages the film's own record proves done."""
    out = {}
    order = studio.STAGES
    for i, stage in enumerate(order):
        s = stages.get(stage, {})
        if s.get("state") != "done" or stage in PARALLEL:
            continue
        for earlier in order[:i]:
            if earlier in PARALLEL and stage != "upload":
                continue
            out.setdefault(earlier, f"{stage} done" + (f" ({s['ref']})" if s.get("ref") else ""))
    if ben_ok:
        for earlier in order[:order.index("edit") + 1]:
            if earlier not in PARALLEL:
                out.setdefault(earlier, ben_ok)
    return {k: v for k, v in out.items() if stages.get(k, {}).get("state", "todo") in OPEN}


def ben_oks(checks: dict) -> dict:
    """{"026": "Ben OK v06 (22 Oct)"} for OWB films Ben approved on the board."""
    out = {}
    for key, c in (checks or {}).items():
        if key.startswith("OWB-") and c.get("verdict") == "ok":
            out[key[4:]] = f"Ben OK {c.get('version', '')} ({(c.get('at') or '')[:10]})".replace("  ", " ")
    return out


def fetch_checks(url: str = CHECKS_URL) -> dict:
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return json.load(r).get("checks", {})
    except (OSError, ValueError):
        return {}  # the board being down never stops rule 1


def plan(films, checks: dict) -> list[tuple]:
    oks = ben_oks(checks)
    moves = []
    for p in sorted(films.glob("*/status.json")):
        data = studio.load(p)
        film = data.get("film") or p.parent.name.split("_")[0]
        for stage, why in implied(data.get("stages", {}), oks.get(film, "")).items():
            moves.append((p, film, stage, data["stages"].get(stage, {}).get("state", "todo"), why))
    return moves


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true", help="write the moves to status.json and STATUS.md")
    ap.add_argument("--git", action="store_true", help="with --apply: commit and push each film's status")
    ap.add_argument("--checks", help="a saved /api/checks JSON instead of fetching it")
    a = ap.parse_args(argv)
    films = studio.FILMS
    checks = json.load(open(a.checks)).get("checks", {}) if a.checks else fetch_checks()
    moves = plan(films, checks)
    for _, film, stage, was, why in moves:
        print(f"{film} {stage}: {was} -> done ({why})")
    if not moves:
        print("stage_sync: nothing to move")
    if not a.apply or not moves:
        return 0
    by_film = {}
    for p, film, stage, _, why in moves:
        by_film.setdefault(p, (film, []))[1].append((stage, why))

    for p, (film, items) in by_film.items():
        def change(data, items=items):
            for stage, why in items:
                if data["stages"].get(stage, {}).get("state", "todo") in OPEN:
                    studio.do_set(data, stage, "done", why, None)
            return None
        if a.git:
            err = studio.with_git(p, change, f"studio: {film} stages proven done ({', '.join(s for s, _ in items)})",
                                  films)
            if err:
                print(f"stage_sync: {film}: {err}", file=sys.stderr)
                return 1
        else:
            data = studio.load(p)
            change(data)
            studio.save(p, data)
    if not a.git:
        studio.write_status(films)
    return 0


if __name__ == "__main__":
    sys.exit(main())
