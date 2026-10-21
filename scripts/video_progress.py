#!/usr/bin/env python3
"""Read past video stages from Git, plus recorded job activity. Never infer stage progress from jobs."""
from __future__ import annotations

import datetime as dt
import io
import json
import re
import subprocess
from pathlib import Path

OWB_STAGES = ["topic", "script", "sources", "vo", "shots", "picture", "edit", "thumbs", "upload"]


def stage_record(stages):
    return {key: {k: v for k, v in stage.items() if k in ("state", "status", "progress", "steps", "review")}
            for key, stage in stages.items()}


def stamp(at):
    return at.astimezone(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def parse(at):
    try:
        return dt.datetime.fromisoformat(at.replace("Z", "+00:00")).astimezone(dt.timezone.utc)
    except (ValueError, TypeError, AttributeError):
        return None


def git(repo, *args, data=None):
    return subprocess.run(["git", "-C", str(repo), *args], input=data, capture_output=True,
                          timeout=45, check=True).stdout


def documents_at(repo, revision, paths):
    """One batch reads all JSON blobs, including paths containing spaces, without checking out old files."""
    stream = io.BytesIO(git(repo, "cat-file", "--batch", data="".join(f"{revision}:{p}\n" for p in paths).encode()))
    docs = {}
    for path in paths:
        header = stream.readline().decode().strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise ValueError(f"Historical blob unavailable: {path}")
        docs[path] = json.loads(stream.read(int(header[2])))
        stream.read(1)
    return docs


def historical_stages(repo, channel, since, cache):
    """A missing/shallow history is unknown, never a zero baseline or proof the video is new."""
    try:
        revision = git(repo, "rev-list", "-1", "--before=" + stamp(since), "HEAD").decode().strip()
        if not revision:
            return {"available": False, "reason": "Earlier repository history is unavailable"}
        source_at = git(repo, "show", "-s", "--format=%cI", revision).decode().strip()
        if not parse(source_at) or parse(source_at) > since:
            return {"available": False, "reason": "Earlier repository history is unavailable"}
        key = channel + ":" + revision
        if key in cache:
            return cache[key]
        if channel == "HOS":
            pipeline = documents_at(repo, revision, ["00_Brand/Channel-Setup/PIPELINE.json"])["00_Brand/Channel-Setup/PIPELINE.json"]
            films = {"HOS:" + f["id"]: {"stages": stage_record(f["stages"])} for f in pipeline["films"]}
            definitions = [{"key": s["key"], "weight": s["weight"]} for s in pipeline["stages"]]
        else:
            paths = git(repo, "ls-tree", "-r", "--name-only", "-z", revision, "--", "02_Video-Projects").decode().split("\0")
            paths = [p for p in paths if re.fullmatch(r"02_Video-Projects/\d{3}_[^/]+/status.json", p)]
            docs = documents_at(repo, revision, paths)
            films = {"OWB:" + d["film"]: {"film": d["film"], "stages": stage_record(d.get("stages", {})),
                     "claims": [{k: v for k, v in c.items() if k in ("stage", "by", "at", "eta")} for c in d.get("claims", [])]}
                     for d in docs.values()}
            definitions = [{"key": s, "weight": 100 / 9} for s in OWB_STAGES]
        out = {"available": True, "commit": revision, "sourceAt": source_at, "films": films, "definitions": definitions}
        cache[key] = out
        return out
    except (OSError, subprocess.SubprocessError, ValueError, TypeError, KeyError, AttributeError):
        return {"available": False, "reason": "Earlier repository history could not be read"}


def job_targets(j):
    explicit = {k for k in j.get("taskKeys", []) if re.fullmatch(r"(?:HOS|OWB):\d{3}", k)}
    if explicit:
        return sorted(explicit)
    title = j.get("title", "")
    keys = {ch.upper() + ":" + no for ch, no in re.findall(r"\b(HOS|OWB)\s*[:·-]?\s*(\d{3})\b", title, re.I)}
    film = str(j.get("film", ""))
    if re.fullmatch(r"(?:HOS|OWB):\d{3}", film):
        keys.add(film)
    elif not keys:
        number = re.match(r"^\s*(\d{3})\b", title)
        no = film if re.fullmatch(r"\d{3}", film) else number[1] if number else ""
        if no:
            channel = "HOS" if j.get("repo") == "hos" or re.search(r"\bHOS\b|history of science", title, re.I) else "OWB"
            keys.add(channel + ":" + no)
    keys.update(ch.upper() + ":" + no for ch, no in re.findall(r"\b(HOS|OWB)\s*[:·-]?\s*(\d{3})\b", j.get("result", ""), re.I))
    return sorted(keys)


def work_since(jobs, since, until):
    items = []
    for j in jobs:
        events = [(parse(h.get("at")), h.get("what", "")) for h in j.get("history", [])]
        events = [(at, what) for at, what in events if at and since < at <= until]
        # Escalations and re-posted blocker notes are not fresh work.
        worked = [at for at, what in events if re.match(r"^(claimed|step \d+ of \d+|done\b)", what)]
        if not worked:
            continue
        finished = [at for at, what in events if what.startswith("done")]
        last_step = None
        for h in j.get("history", []):
            when, what = parse(h.get("at")), h.get("what", "")
            if not when or when > until:
                continue
            if what.startswith(("added", "reopened")):
                last_step = None
            match = re.match(r"step (\d+) of (\d+) done", what)
            if match:
                last_step = (when, int(match[1]), int(match[2]))
        reported_complete = bool(last_step and since < last_step[0] <= until and last_step[2] > 0 and last_step[1] >= last_step[2])
        review_ready = (reported_complete and j.get("status") == "blocked"
                        and bool(re.search(r"parked for (?:the )?chief\b", j.get("result", ""), re.I)))
        items.append({"id": j["id"], "title": j.get("title", ""), "repo": j.get("repo", ""),
                      "film": j.get("film", ""), "stage": j.get("stage", ""), "taskKeys": job_targets(j),
                      "status": j.get("status", ""), "workedAt": stamp(max(worked)),
                      "done": bool(finished) and j.get("status") == "done", "readyForReview": review_ready})
    return items


def progress_document(owb, hos, jobs, out_dir, at=None):
    at = at or dt.datetime.now(dt.timezone.utc)
    # Hourly comparison anchors keep the publishing clock from masquerading as work on every minute check.
    anchor = at.replace(minute=0, second=0, microsecond=0)
    cache_path = Path(out_dir) / "video-progress-cache.json"
    try:
        cache = json.loads(cache_path.read_text())
    except (OSError, ValueError):
        cache = {}
    periods = {}
    for name, days in (("day", 1), ("week", 7)):
        since = anchor - dt.timedelta(days=days)
        periods[name] = {"since": stamp(since), "channels": {
            "OWB": historical_stages(owb, "OWB", since, cache),
            "HOS": historical_stages(hos, "HOS", since, cache)}, "work": work_since(jobs, since, at)}
    used = {ch + ":" + h["commit"] for period in periods.values() for ch, h in period["channels"].items() if h.get("commit")}
    try:
        cache_path.write_text(json.dumps({k: v for k, v in cache.items() if k in used}))
    except OSError:
        pass  # Cache failure cannot stop publishing the board.
    return {"version": 2, "periods": periods}
