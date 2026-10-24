#!/usr/bin/env python3
"""Per-video Studio tracker (Ben, 24 Oct 2026): five lanes, one card per long/Short.

Lanes (left → right):
  upcoming → progress → changes → ready → done

Derived from jobs/queue.json, UPLOADS.json / PACKAGE_UPLOAD_RESULT, film_briefs, HOS PIPELINE,
OWB status.json, and Ben's board checks (`[Ben] OK/changes` via /api/checks). Optional overrides
in 05_Analytics/kanban/video_overrides.json.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from video_progress import job_targets

ROOT = Path(__file__).resolve().parents[1]
OVERRIDES = ROOT / "05_Analytics" / "kanban" / "video_overrides.json"
UPLOADS = ROOT / "00_Brand" / "Channel-Setup" / "social" / "UPLOADS.json"
LONDON = ZoneInfo("Europe/London")

LANES = ("upcoming", "progress", "changes", "ready", "done")
LANE_LABELS = {
    "upcoming": "Upcoming",
    "progress": "In progress",
    "changes": "Changes requested",
    "ready": "Ready for OK",
    "done": "Done on YouTube",
}
LIVE_STATUSES = frozenset({"open", "claimed", "blocked"})
DONE_PUBLIC_DAYS = 14

BEN_CHANGES_RE = re.compile(
    r"Ben'?s?\s+(\d+)\s+changes|\bchanges?\s+on\s+master\b|\bchange tick\b",
    re.I,
)
NOTE_LINE_RE = re.compile(
    r"(?:^|\n)\s*(?:\(?\d+\)|[•\-*]|\d+\.)\s*(?:(?P<t>\d{1,2}:\d{2})\s*[:\-]?\s*)?(?P<text>.+)",
)


def _parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00")).astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def check_id(key: str) -> str:
    """OWB:028 → OWB-028 (board checks store)."""
    return key.replace(":", "-")


def load_overrides(path: Path | None = None) -> dict:
    p = path or OVERRIDES
    if not p.exists():
        return {}
    try:
        doc = json.loads(p.read_text())
    except (OSError, ValueError):
        return {}
    return doc if isinstance(doc, dict) else {}


def parse_change_notes(text: str) -> list[dict]:
    """Pull timecoded fix lines from a Ben changes post or job body."""
    out, seen = [], set()
    for m in NOTE_LINE_RE.finditer(text or ""):
        t = (m.group("t") or "").strip()
        body = (m.group("text") or "").strip()
        body = re.sub(r"\s+", " ", body)
        if len(body) < 8:
            continue
        if re.match(r"^(Chief ruling|URGENT|HOS|OWB|Studio Kanban|After |Follow )\b", body, re.I):
            continue
        key = (t, body[:80].lower())
        if key in seen:
            continue
        seen.add(key)
        out.append({"t": t, "text": body[:200], "done": False})
    return out


def notes_from_check(doc: dict | None) -> list[dict]:
    if not doc or doc.get("verdict") != "change":
        return []
    fixes = doc.get("fixes") or []
    notes = []
    for f in fixes:
        if not isinstance(f, dict):
            continue
        text = str(f.get("text") or "").strip()
        if not text:
            continue
        notes.append({"t": str(f.get("t") or "").strip(), "text": text[:200], "done": False})
    if notes:
        return notes
    return parse_change_notes(str(doc.get("note") or ""))


def notes_from_job(job: dict) -> list[dict]:
    blob = (job.get("title") or "") + "\n" + (job.get("body") or "")
    if not BEN_CHANGES_RE.search(blob):
        return []
    return parse_change_notes(job.get("body") or "") or parse_change_notes(job.get("title") or "")


def is_ben_changes_job(job: dict) -> bool:
    blob = (job.get("title") or "") + "\n" + (job.get("body") or "")
    return bool(BEN_CHANGES_RE.search(blob))


def london_slot(iso: str | None) -> str:
    dt = _parse_iso(iso)
    if not dt:
        return ""
    local = dt.astimezone(LONDON)
    # %-d is libc-only; strip a leading zero instead for portability.
    return local.strftime("%a %d %b %Y %H:%M %Z").replace(" 0", " ").replace("UTC", "GMT")


def youtube_state(release: dict | None, upload_meta: dict | None) -> dict | None:
    """Normalize to {state, videoId, publishAt, url, privacy}."""
    if release and release.get("videoId"):
        publish_at = release.get("publishAt") or ""
        state = release.get("state") or "uploaded"
        privacy = "public" if state == "live" else "private" if state in ("scheduled", "uploaded") else state
        return {
            "state": state,
            "videoId": release["videoId"],
            "publishAt": publish_at,
            "privacy": privacy,
            "url": f"https://youtu.be/{release['videoId']}",
            "publishAtLondon": london_slot(publish_at),
        }
    if upload_meta and upload_meta.get("videoId"):
        vid = upload_meta["videoId"]
        publish_at = upload_meta.get("publishAt") or ""
        privacy = upload_meta.get("privacyStatus") or upload_meta.get("privacy") or "private"
        if privacy == "public":
            state = "live"
        elif publish_at:
            state = "scheduled"
        else:
            state = "uploaded"
        return {
            "state": state,
            "videoId": vid,
            "publishAt": publish_at,
            "privacy": privacy,
            "url": f"https://youtu.be/{vid}",
            "publishAtLondon": london_slot(publish_at),
        }
    return None


def _receipt_privacy(root: Path, package_dir: str) -> tuple[str, str]:
    """Best privacy/publishAt from the newest PACKAGE_UPLOAD_RESULT in a package dir."""
    if not package_dir:
        return "", ""
    folder = root / package_dir
    if not folder.is_dir():
        return "", ""
    best = ("", "")
    for path in sorted(folder.glob("PACKAGE_UPLOAD_RESULT*.json")):
        try:
            doc = json.loads(path.read_text())
            upload = doc.get("upload") or {}
            if doc.get("ok") is not True or doc.get("dryRun") is not False:
                continue
            response = upload.get("responseSummary") or {}
            if isinstance(response, str):
                try:
                    response = json.loads(response)
                except ValueError:
                    response = {}
            privacy = response.get("privacyStatus") or ""
            publish_at = upload.get("scheduledFor") or response.get("publishAt") or ""
            if privacy or publish_at:
                best = (privacy, publish_at)
        except (OSError, ValueError, TypeError):
            continue
    return best


def uploads_index(root: Path | None = None) -> dict:
    """Map film key / short id → upload meta from UPLOADS.json (+ receipt privacy)."""
    root = root or ROOT
    path = root / "00_Brand" / "Channel-Setup" / "social" / "UPLOADS.json"
    try:
        vids = json.loads(path.read_text()).get("videos", {})
    except (OSError, ValueError):
        return {}
    by_film: dict[str, list] = {}
    for vid, meta in vids.items():
        kind = meta.get("kind") or "long"
        pkg = str(meta.get("packageDir") or meta.get("file") or "")
        m = re.search(r"02_Video-Projects/(\d{3})_", pkg)
        if not m:
            continue
        film = m.group(1)
        privacy = meta.get("privacyStatus") or meta.get("privacy") or ""
        publish_at = meta.get("publishAt") or ""
        if not privacy or not publish_at:
            rp, ra = _receipt_privacy(root, meta.get("packageDir") or "")
            privacy = privacy or rp
            publish_at = publish_at or ra
        row = {
            "videoId": vid,
            "kind": kind,
            "film": film,
            "channel": "OWB",
            "long": meta.get("long") or "",
            "file": meta.get("file") or "",
            "packageDir": meta.get("packageDir") or "",
            "privacyStatus": privacy,
            "publishAt": publish_at,
            "title": meta.get("title") or "",
        }
        key = f"OWB:{film}" if kind == "long" else f"OWB:{film}:S:{vid}"
        by_film.setdefault(key, []).append(row)
    return by_film


def job_is_channel_wide(job: dict, keys: list[str]) -> bool:
    """Backlog/audit jobs that tag many films must not drive a single card's lane line."""
    if len(keys) >= 4:
        return True
    title = job.get("title") or ""
    return bool(re.match(r"^Backlog\b", title, re.I)) and len(keys) > 1


def job_index(jobs: list[dict], overrides: dict) -> dict[str, list[dict]]:
    """film key → live jobs (open/claimed/blocked), film-specific first."""
    force = (overrides.get("jobFilms") or {}) if overrides else {}
    out: dict[str, list] = {}
    for j in jobs:
        if j.get("status") not in LIVE_STATUSES:
            continue
        keys = list(force.get(j["id"], [])) or job_targets(j)
        if job_is_channel_wide(j, keys):
            continue
        for k in keys:
            out.setdefault(k, []).append(j)
    return out


def version_of(text: str) -> str:
    m = re.search(r"\bv(\d+[a-z]?)\b", text or "", re.I)
    return f"v{m.group(1)}" if m else ""


def waiting_on(lane: str, check: dict | None, jobs: list[dict], brief: dict, youtube: dict | None) -> tuple[str, str]:
    """(who, plain English line)."""
    if lane == "done" and youtube:
        if youtube["state"] == "live":
            return "YouTube", f"Public on YouTube ({youtube['videoId']})."
        if youtube.get("publishAtLondon"):
            return "YouTube", f"Private, scheduled {youtube['publishAtLondon']}."
        return "YouTube", f"On YouTube as {youtube.get('privacy') or 'private'} ({youtube['videoId']})."

    if lane == "changes":
        who = "worker"
        if any(j.get("status") == "claimed" for j in jobs):
            by = next((j.get("by") for j in jobs if j.get("status") == "claimed"), "") or "worker"
            return by, f"Fixing your notes ({by})."
        if jobs:
            return "queue", "Your changes are queued; a worker picks them up next."
        return "Chief", "You asked for changes — no fix job is queued yet."

    if lane == "ready":
        if check and check.get("verdict") == "ok" and not check.get("handled"):
            return "Chief", "You OK'd it — waiting on Chief PASS."
        # parked-for-Chief jobs
        for j in jobs:
            blob = (j.get("title") or "") + " " + (j.get("body") or "") + " " + (j.get("result") or "")
            if j.get("status") == "blocked" and re.search(r"parked for Chief|for Chief", blob, re.I):
                return "Chief", "Waiting on Chief PASS."
        if (brief.get("you") or "").strip():
            return "Ben", (brief.get("youShort") or brief.get("you") or "Needs your OK.").split(".")[0] + "."
        return "Ben", "Ready for your OK."

    if lane == "progress":
        claimed = [j for j in jobs if j.get("status") == "claimed"]
        if claimed:
            by = claimed[0].get("by") or "worker"
            return by, f"{by} is working on it now."
        if jobs:
            j = jobs[0]
            return "queue", f"Queued: {(j.get('title') or 'work')[:80]}."
        return "worker", "Work is under way."

    # upcoming
    air = brief.get("timing") or ""
    if air:
        return "queue", f"Planned — {air}"
    return "queue", "Planned; no work started yet."


def derive_lane(
    *,
    youtube: dict | None,
    check: dict | None,
    jobs: list[dict],
    brief: dict,
    override_lane: str | None = None,
) -> str:
    if override_lane in LANES:
        return override_lane
    if youtube and youtube.get("videoId"):
        return "done"

    unhandled = bool(check) and not check.get("handled")
    change_check = unhandled and check.get("verdict") == "change"
    ok_check = unhandled and check.get("verdict") == "ok"
    change_jobs = [j for j in jobs if is_ben_changes_job(j)]
    other_jobs = [j for j in jobs if not is_ben_changes_job(j)]

    # Ben asked for changes: stay in Changes until the fix job is done and a new cut is ready.
    if change_check or change_jobs:
        # If the change jobs are all gone and brief/you asks for a rewatch → Ready for OK
        if change_check and not change_jobs and (brief.get("you") or "").strip() and not other_jobs:
            return "ready"
        if change_check or change_jobs:
            return "changes"

    if ok_check:
        # Ben OK'd: if release/build jobs are live → in progress; else ready for Chief.
        if other_jobs or change_jobs:
            return "progress"
        return "ready"

    you = (brief.get("you") or "").strip()
    if you and not ok_check:
        # Waiting on Ben's watch/OK (and he hasn't OK'd this version).
        if other_jobs and not change_jobs:
            # Worker still finishing something before the watch — progress wins only if claimed.
            if any(j.get("status") == "claimed" for j in other_jobs):
                return "progress"
        return "ready"

    # Chief review parked
    for j in jobs:
        blob = (j.get("title") or "") + " " + (j.get("body") or "")
        if j.get("status") == "blocked" and re.search(r"parked for Chief", blob, re.I):
            return "ready"

    if jobs:
        return "progress"
    return "upcoming"


def flags_for(
    *,
    key: str,
    lane: str,
    check: dict | None,
    jobs: list[dict],
    brief: dict,
    now: datetime,
) -> list[dict]:
    flags = []
    unhandled = bool(check) and not check.get("handled")
    if unhandled and check.get("verdict") in ("ok", "change") and not jobs:
        flags.append({"kind": "stuck", "text": "No job queued"})

    you = (brief.get("you") or "").strip()
    if you and unhandled and check.get("verdict") == "ok":
        flags.append({"kind": "stale", "text": "Brief still asks for your OK (you already OK'd)"})

    # Deadline: youWhen / you deadline within 2 days, or air within 3 days while not done.
    if lane == "ready":
        deadline = _parse_iso(brief.get("youWhen")) or _parse_iso(
            next((s.get("when") for s in (brief.get("steps") or [])
                  if not s.get("done") and s.get("who") in ("Ben", "Ready for you")), None)
        )
        if deadline and now <= deadline <= now + timedelta(days=2):
            flags.append({"kind": "deadline", "text": f"OK needed by {deadline.astimezone(LONDON).strftime('%-d %b')}"})
    return flags


def short_title_from_path(meta: dict) -> str:
    pkg = str(meta.get("packageDir") or meta.get("file") or "")
    # …/10_Shorts/mon30_comets/…
    m = re.search(r"10_Shorts/([^/]+)", pkg)
    if m:
        slug = m.group(1).replace("_", " ")
        return slug[:60]
    return meta.get("title") or meta.get("videoId") or "Short"


def build_videos(
    *,
    hos: dict,
    owb: list[dict],
    briefs: dict,
    jobs: list[dict],
    checks: dict,
    watch: dict | None = None,
    uploads: dict | None = None,
    overrides: dict | None = None,
    now: datetime | None = None,
) -> dict:
    """Return {updatedAt, lanes, videos} for board/tracker."""
    now = now or datetime.now(timezone.utc)
    overrides = overrides if overrides is not None else load_overrides()
    watch = watch or {}
    uploads = uploads if uploads is not None else uploads_index()
    by_jobs = job_index(jobs, overrides)
    film_lanes = (overrides.get("lanes") or {}) if overrides else {}
    videos = []

    # --- Longs: HOS ---
    for f in hos.get("films") or []:
        num = str(f.get("id") or "")
        if not re.fullmatch(r"\d{3}", num):
            continue
        key = f"HOS:{num}"
        videos.append(_card(
            key=key, channel="HOS", number=num, title=f.get("title") or "",
            vtype="long", air=f.get("air") or "", brief=briefs.get(key) or {},
            release=None, upload_rows=uploads.get(key) or [],
            jobs=by_jobs.get(key) or [], check=checks.get(check_id(key)),
            watch=watch.get(key), override_lane=film_lanes.get(key), now=now,
        ))

    # --- Longs: OWB ---
    for f in owb:
        num = str(f.get("film") or "")
        if not re.fullmatch(r"\d{3}", num):
            continue
        key = f"OWB:{num}"
        videos.append(_card(
            key=key, channel="OWB", number=num, title=f.get("title") or "",
            vtype="long", air=f.get("air") or "", brief=briefs.get(key) or {},
            release=f.get("release"), upload_rows=uploads.get(key) or [],
            jobs=by_jobs.get(key) or [], check=checks.get(check_id(key)),
            watch=watch.get(key), override_lane=film_lanes.get(key), now=now,
        ))

    # --- Shorts from UPLOADS (each Short its own card) ---
    for key, rows in uploads.items():
        if ":S:" not in key:
            continue
        meta = rows[0]
        num = meta["film"]
        vid = meta["videoId"]
        parent = f"OWB:{num}"
        parent_title = next((v["title"] for v in videos if v["key"] == parent), f"{num}")
        title = short_title_from_path(meta) or f"Short · {parent_title}"
        skey = f"OWB:{num}:S:{vid}"
        # Attach jobs that mention this Short id or the parent film's Shorts work
        sjobs = list(by_jobs.get(skey) or [])
        for j in by_jobs.get(parent) or []:
            blob = (j.get("title") or "") + (j.get("body") or "")
            if re.search(r"\bShorts?\b", blob, re.I) and vid in blob:
                sjobs.append(j)
        videos.append(_card(
            key=skey, channel="OWB", number=num, title=title,
            vtype="short", air="", brief={},
            release=None, upload_rows=[meta],
            jobs=sjobs, check=None,  # Ben's OK/changes attach to the long, not each Short
            watch=None, override_lane=film_lanes.get(skey), now=now,
            short_id=vid, parent=parent,
        ))

    # --- Standalone / extraWatch Shorts (HOS S1…) ---
    for extra in (briefs.get("_extraWatch") or []):
        pass  # briefs.json nests extraWatch at top level; caller may pass via overrides

    # Collapse old public Done items for the page (keep data; mark collapsed)
    cutoff = now - timedelta(days=DONE_PUBLIC_DAYS)
    for v in videos:
        if v["lane"] != "done":
            continue
        yt = v.get("youtube") or {}
        if yt.get("state") == "live":
            pub = _parse_iso(yt.get("publishAt")) or _parse_iso(v.get("air"))
            v["collapsed"] = bool(pub and pub < cutoff)
        else:
            v["collapsed"] = False

    videos.sort(key=lambda v: (LANES.index(v["lane"]), v.get("air") or "9999", v["key"]))
    counts = {lane: sum(1 for v in videos if v["lane"] == lane and not v.get("collapsed")) for lane in LANES}
    return {
        "updatedAt": now.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "lanes": [{"id": lane, "label": LANE_LABELS[lane], "count": counts[lane]} for lane in LANES],
        "videos": videos,
        "donePublicDays": DONE_PUBLIC_DAYS,
    }


def _card(
    *,
    key, channel, number, title, vtype, air, brief, release, upload_rows, jobs, check,
    watch, override_lane, now, short_id="", parent="",
) -> dict:
    upload_meta = None
    if upload_rows:
        u = upload_rows[0]
        upload_meta = {
            "videoId": u.get("videoId"),
            "publishAt": u.get("publishAt") or "",
            "privacyStatus": u.get("privacyStatus") or "",
            "privacy": u.get("privacyStatus") or "",
        }
    youtube = youtube_state(release, upload_meta)
    # Prefer PACKAGE receipt over a bare UPLOADS row with no privacy
    if not youtube and release:
        youtube = youtube_state(release, None)
    # Older longs may lack a local receipt/UPLOADS row; trust the brief only when it says the film is public.
    if not youtube:
        blob = " ".join(str(brief.get(k) or "") for k in ("holdup", "line", "done"))
        if re.search(r"\b(it is public\.|live since|public on youtube)\b", blob, re.I):
            if not (brief.get("you") or "").strip() and not jobs:
                youtube = {"state": "live", "videoId": "", "publishAt": air or "", "privacy": "public",
                           "url": "", "publishAtLondon": ""}

    lane = derive_lane(youtube=youtube, check=check, jobs=jobs, brief=brief, override_lane=override_lane)

    notes = notes_from_check(check) if check and check.get("verdict") == "change" else []
    if not notes:
        for j in jobs:
            notes = notes_from_job(j)
            if notes:
                break
    # Tick notes off when the Ben-changes job for this round is done (no live changes job).
    change_jobs_live = [j for j in jobs if is_ben_changes_job(j)]
    if notes and not change_jobs_live and lane in ("ready", "done", "progress"):
        notes = [{**n, "done": True} for n in notes]

    version = ""
    if check and check.get("version"):
        version = str(check["version"])
    if not version and brief.get("you"):
        version = version_of(brief["you"])
    if not version:
        for j in jobs:
            version = version_of(j.get("title") or "")
            if version:
                break
    if not version and youtube:
        version = version_of(str((upload_rows or [{}])[0].get("file") or ""))

    who, line = waiting_on(lane, check, jobs, brief, youtube)
    # Ready for OK: label Ben vs Chief clearly
    ready_for = ""
    if lane == "ready":
        if check and check.get("verdict") == "ok" and not check.get("handled"):
            ready_for = "Chief"
        elif any(j.get("status") == "blocked" and re.search(r"Chief", (j.get("title") or "") + (j.get("body") or ""), re.I) for j in jobs):
            ready_for = "Chief"
        else:
            ready_for = "Ben"

    flags = flags_for(key=key, lane=lane, check=check, jobs=jobs, brief=brief, now=now)

    air_text = ""
    if air:
        try:
            d = datetime.strptime(air[:10], "%Y-%m-%d").replace(tzinfo=LONDON)
            # Longs default 18:00 London Sundays; Shorts 11:30 — keep date only unless publishAt known
            air_text = d.strftime("%a %d %b").replace(" 0", " ")
        except ValueError:
            air_text = air
    if youtube and youtube.get("publishAtLondon"):
        air_text = youtube["publishAtLondon"]

    return {
        "key": key,
        "checkId": check_id(key.split(":S:")[0] if ":S:" in key else key),
        "channel": channel,
        "number": number,
        "title": title,
        "type": vtype,
        "version": version,
        "air": air,
        "airText": air_text,
        "lane": lane,
        "line": line,
        "waitingOn": who,
        "readyFor": ready_for,
        "notes": notes,
        "flags": flags,
        "youtube": youtube,
        "watch": watch,
        "jobs": [{"id": j.get("id"), "status": j.get("status"), "title": (j.get("title") or "")[:120],
                  "by": j.get("by") or "", "kind": j.get("kind") or ""} for j in jobs],
        "check": ({"verdict": check.get("verdict"), "version": check.get("version"), "at": check.get("at"),
                   "handled": bool(check.get("handled"))} if check else None),
        "shortId": short_id,
        "parent": parent,
        "collapsed": False,
    }


def build_from_docs(docs: dict, checks: dict | None = None, overrides: dict | None = None) -> dict:
    """Build tracker from board section docs (hos/owb/briefs) + checks."""
    hos = (docs.get("hos") or {}).get("pipeline") or docs.get("hos") or {}
    owb_doc = docs.get("owb") or {}
    owb = owb_doc.get("films") or []
    briefs_doc = docs.get("briefs") or {}
    films = briefs_doc.get("films") or briefs_doc
    # Attach extraWatch for Shorts cards if present
    if isinstance(briefs_doc, dict) and briefs_doc.get("extraWatch"):
        films = dict(films)
        films["_extraWatch"] = briefs_doc["extraWatch"]
    live_jobs = owb_doc.get("jobs") or []
    # Prefer full queue when available (live jobs only lack done ones; enough for lanes)
    qpath = ROOT / "jobs" / "queue.json"
    if qpath.exists():
        try:
            live_jobs = [j for j in json.loads(qpath.read_text())["jobs"] if j.get("status") in LIVE_STATUSES]
        except (OSError, ValueError, KeyError):
            pass
    return build_videos(
        hos=hos if "films" in hos else {"films": []},
        owb=owb,
        briefs=films,
        jobs=live_jobs,
        checks=checks or {},
        watch=briefs_doc.get("watch") or {},
        overrides=overrides,
    )


if __name__ == "__main__":
    import sys
    checks = {}
    try:
        import urllib.request
        with urllib.request.urlopen("https://studio-kanban.vercel.app/api/checks", timeout=15) as r:
            checks = json.loads(r.read().decode()).get("checks") or {}
    except Exception as e:
        print(f"checks not read: {e}", file=sys.stderr)
    hos = json.loads(Path("/tmp/hos-sparse/00_Brand/Channel-Setup/PIPELINE.json").read_text())
    owb = [json.loads(p.read_text()) for p in sorted((ROOT / "02_Video-Projects").glob("*/status.json"))]
    for film in owb:
        from kanban_snapshot import release_record
        rec = release_record(str(film.get("film", "")))
        if rec:
            film["release"] = rec
    briefs = json.loads((ROOT / "05_Analytics" / "kanban" / "film_briefs.json").read_text())["films"]
    jobs = json.loads((ROOT / "jobs" / "queue.json").read_text())["jobs"]
    doc = build_videos(hos=hos, owb=owb, briefs=briefs, jobs=jobs, checks=checks)
    for v in doc["videos"]:
        if v["key"] in ("HOS:006", "HOS:007", "OWB:028", "OWB:029") or v["number"] in ("006", "007", "028", "029"):
            print(f"{v['key']:20} lane={v['lane']:10} wait={v['waitingOn']:8} flags={[f['text'] for f in v['flags']]} notes={len(v['notes'])} · {v['line'][:70]}")
