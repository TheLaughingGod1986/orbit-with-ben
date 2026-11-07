#!/usr/bin/env python3
"""Enqueue/unblock Studio upload (or Buffer social) jobs for Passed films with a complete listing package.

Ben, 7 Nov 2026: once Ben OK'd a cut (Passed) and title/thumbnail/description/tags are set, create or unblock a
normal Studio upload job so the Mac mini worker uploads Private + publishAt in the locked cadence. Social-only
clips use Buffer. This cloud agent never uploads, never invents YouTube ids, never turns a swap into a silent
new upload, and never reuses TtgHNLXfDSs or k9pXeeJvLpc as destinations.

  python3 scripts/approved_deliver.py            # dry-run
  python3 scripts/approved_deliver.py --apply --git
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import jobs as J  # noqa: E402
import listing_package as lp  # noqa: E402
import video_tracker as vt  # noqa: E402

LONDON = ZoneInfo("Europe/London")
BANNED_REUSE_IDS = frozenset({"TtgHNLXfDSs", "k9pXeeJvLpc"})
SWAP_RE = re.compile(r"\bswap\b", re.I)
LISTING_HOLD_RE = re.compile(r"listing|title|thumbnail|description|tags|package incomplete|needs title", re.I)
# Locked cadence (Ben, 7 Nov 2026). Weekday: Mon=0 … Sun=6. (weekday, hour, minute) London.
CADENCE = {
    "OWB": {
        "long": [(6, 18, 0), (2, 18, 0)],          # Sun / Wed 18:00
        "short": [(0, 11, 30), (2, 11, 30), (4, 11, 30), (5, 11, 30)],  # Mon Wed Fri Sat 11:30
    },
    "HOS": {
        "long": [(3, 18, 0)],                       # Thu 18:00
        "short": [(5, 11, 30), (4, 11, 30), (6, 11, 30), (1, 11, 30)],  # Sat Fri Sun Tue 11:30
    },
}


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def is_public(v: dict) -> bool:
    yt = v.get("youtube") or {}
    return yt.get("privacy") == "public" or yt.get("state") == "live"


def is_scheduled(v: dict) -> bool:
    yt = v.get("youtube") or {}
    return (not is_public(v)) and yt.get("state") == "scheduled" and bool(yt.get("publishAt") or yt.get("publishAtLondon"))


def is_uploaded(v: dict) -> bool:
    """Already has a YouTube id in uploaded/scheduled/live state — never invent a second upload."""
    yt = v.get("youtube") or {}
    vid = yt.get("videoId") or ""
    if not vid:
        return False
    return yt.get("state") in ("scheduled", "live", "uploaded") or is_public(v) or is_scheduled(v)


def london_day(at: str) -> str:
    """YYYY-MM-DD in London from an ISO publishAt, or '' if unparseable. Never invents a day."""
    if not at:
        return ""
    try:
        when = dt.datetime.fromisoformat(str(at).replace("Z", "+00:00")).astimezone(LONDON)
    except ValueError:
        return ""
    return when.date().isoformat()


def short_identity(v: dict) -> str:
    """Real Short identity when known: shortId, YouTube id, or the `:S:<id>` key suffix.

    Empty means this card is not yet tied to a specific uploaded Short (an approved/OK or
    planned Short). Two Shorts of the same film with empty identity are different cuts —
    never collapse them to the film number alone (Orbit ships 2+ Shorts per long).
    """
    sid = str(v.get("shortId") or "").strip()
    if sid:
        return sid
    yt = str(((v.get("youtube") or {}).get("videoId") or "")).strip()
    if yt:
        return yt
    key = str(v.get("key") or "")
    m = re.search(r":S:([A-Za-z0-9_-]+)$", key)
    return m.group(1) if m else ""


def same_cut_identity(a: dict, b: dict) -> bool:
    """True only for the same cut: one long per film, or the same Short identity.

    Shorts of the same film are different cuts unless they share a real Short identity
    (same shortId / YouTube id / `:S:` key) or the exact same card key.
    """
    if str(a.get("channel") or "").upper() != str(b.get("channel") or "").upper():
        return False
    if (a.get("type") == "short") != (b.get("type") == "short"):
        return False
    na, nb = str(a.get("number") or ""), str(b.get("number") or "")
    if a.get("type") == "short":
        ka, kb = str(a.get("key") or ""), str(b.get("key") or "")
        if ka and kb and ka == kb:
            return True
        sa, sb = short_identity(a), short_identity(b)
        if sa and sb:
            return sa == sb
        # No shared Short identity → different Shorts (even with the same film number).
        return False
    if na and nb and na != nb:
        return False
    return bool(na and nb and na == nb)


def already_delivered(video: dict, videos: list[dict]) -> str:
    """Why this Passed cut must not get another upload, or '' if clear."""
    yt = video.get("youtube") or {}
    vid = yt.get("videoId") or ""
    if vid in BANNED_REUSE_IDS:
        return f"Banned reuse id {vid}"
    if is_public(video) or is_scheduled(video) or is_uploaded(video):
        return "Already on YouTube"
    for other in videos:
        if other is video or other.get("key") == video.get("key"):
            continue
        if not same_cut_identity(video, other):
            continue
        oyt = other.get("youtube") or {}
        oid = oyt.get("videoId") or ""
        if oid in BANNED_REUSE_IDS:
            return f"Banned reuse id {oid}"
        if is_public(other) or is_scheduled(other) or is_uploaded(other):
            return f"Already on YouTube as {other.get('key')}"
    return ""


def is_swap(job: dict | None, video: dict | None = None) -> bool:
    bits = []
    if job:
        bits += [job.get("title") or "", job.get("body") or "", ((job.get("approved_from") or {}).get("what") or "")]
    if video:
        bits += [((video.get("approved") or {}).get("what") or ""), video.get("title") or ""]
    return bool(SWAP_RE.search(" ".join(bits)))


def parent_long_public(video: dict, videos: list[dict]) -> bool:
    """House rule: social that accompanies a long waits until that long is public."""
    parent = str(video.get("parent") or "")
    if parent:
        for v in videos:
            if v.get("key") == parent:
                return is_public(v)
        return False
    # A long's own social posts wait on itself.
    if video.get("type") == "long":
        return is_public(video)
    # Short without a named parent: allow only when no parent key is required / unknown.
    return True


def _uploads_publish_days(path: Path, *, channel: str, want_short: bool, from_day: dt.date) -> set[str]:
    """London days booked in one UPLOADS.json for this channel and long/short kind."""
    out: set[str] = set()
    try:
        vids = json.loads(path.read_text()).get("videos", {})
    except (OSError, ValueError, AttributeError):
        return out
    for meta in vids.values():
        if not isinstance(meta, dict) or meta.get("retired"):
            continue
        kind = meta.get("kind") or "long"
        is_short = kind == "short"
        if is_short != want_short:
            continue
        # OWB UPLOADS rows are OWB; HOS UPLOADS may set channel or live under HOS checkout.
        row_ch = str(meta.get("channel") or channel).upper()
        if row_ch != channel:
            continue
        day = london_day(meta.get("publishAt") or "")
        if day and day >= from_day.isoformat():
            out.add(day)
    return out


def taken_cadence_days(videos: list[dict], channel: str, vtype: str, from_day: dt.date,
                       *, root: Path | None = None) -> set[str]:
    """London YYYY-MM-DD that already have a Short (or long) scheduled or public on this channel.

    Reads tracker cards plus OWB/HOS UPLOADS.json so empty stubs cannot hide a booked Monday 11:30
    or Sunday 18:00. Fill gaps only; never invent ids.
    """
    ch = (channel or "OWB").upper()
    want_short = vtype == "short"
    out: set[str] = set()
    for v in videos:
        if str(v.get("channel") or "").upper() != ch:
            continue
        if (v.get("type") == "short") != want_short:
            continue
        yt = v.get("youtube") or {}
        day = london_day(yt.get("publishAt") or "")
        if not day and is_public(v) and v.get("air"):
            day = str(v.get("air"))[:10]
        if day and day >= from_day.isoformat():
            out.add(day)
    root = root or ROOT
    owb_uploads = root / "00_Brand" / "Channel-Setup" / "social" / "UPLOADS.json"
    if ch == "OWB" and owb_uploads.is_file():
        out |= _uploads_publish_days(owb_uploads, channel="OWB", want_short=want_short, from_day=from_day)
    if ch == "HOS":
        try:
            import channels
            hos_root = channels.repo_path("hos")
            hos_uploads = hos_root / "00_Brand" / "Channel-Setup" / "social" / "UPLOADS.json"
            if hos_uploads.is_file():
                out |= _uploads_publish_days(hos_uploads, channel="HOS", want_short=want_short, from_day=from_day)
        except Exception:  # noqa: BLE001
            pass
    return out


# Back-compat name used by older tests/callers.
def taken_short_days(videos: list[dict], channel: str, from_day: dt.date, *, root: Path | None = None) -> set[str]:
    return taken_cadence_days(videos, channel, "short", from_day, root=root)


def next_cadence_slot(channel: str, vtype: str, *, now: dt.datetime, taken_days: set[str] | None = None,
                     airs: str = "") -> str:
    """Next London cadence ISO (…Z) for a ready cut. Skips any London day already taken for this kind.

    A known `airs` is used only when that London day is free; otherwise the next free cadence slot wins.
    Never invents past dates or YouTube ids.
    """
    ch = (channel or "OWB").upper()
    kind = "short" if vtype == "short" else "long"
    slots = CADENCE.get(ch, CADENCE["OWB"]).get(kind) or CADENCE["OWB"]["long"]
    local = now.astimezone(LONDON)
    taken = set(taken_days or set())
    if airs:
        raw = airs if airs.endswith("Z") or "+" in airs else airs
        day = london_day(raw if "T" in raw else raw)
        if not day:
            try:
                day = london_day(raw.replace(" ", "T") if "T" not in raw else raw)
            except Exception:  # noqa: BLE001
                day = ""
        # approved_from airs is usually already …Z
        if day and day not in taken:
            try:
                when = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
                if when.tzinfo is None:
                    when = when.replace(tzinfo=dt.timezone.utc)
                if when > now:
                    return when.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
            except ValueError:
                pass
    for day_offset in range(0, 60):
        day = (local + dt.timedelta(days=day_offset)).date()
        wd = day.weekday()
        for slot_wd, hour, minute in slots:
            if slot_wd != wd:
                continue
            when = dt.datetime(day.year, day.month, day.day, hour, minute, tzinfo=LONDON)
            if when <= local:
                continue
            if day.isoformat() in taken:
                continue
            return when.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    return ""


def delivery_jobs_for(video: dict, alljobs: list[dict]) -> list[dict]:
    """Live jobs that already deliver this Passed cut (upload / Buffer), excluding unrelated follow-ups."""
    appr = video.get("approved") or {}
    job_id = appr.get("job") or ""
    film = str(video.get("number") or "")
    key = video.get("key") or ""
    out = []
    for j in alljobs:
        if j.get("status") not in ("open", "claimed", "blocked", "done"):
            continue
        if job_id and j.get("id") == job_id:
            out.append(j)
            continue
        if is_swap(j):
            continue
        af = j.get("approved_from") if isinstance(j.get("approved_from"), dict) else {}
        if af and (af.get("card") == key or (film and af.get("number") == film and af.get("version") == (appr.get("version") or video.get("version")))):
            out.append(j)
            continue
        title = (j.get("title") or "") + " " + (j.get("body") or "")
        kind = j.get("kind") or ""
        if film and re.search(rf"\b{re.escape(film)}\b", title) and (
                kind in ("studio",) or re.search(r"\bupload\b|\bbuffer-mirror\b|\bbuffer\b", title, re.I)):
            # Prefer jobs that name this cut's version when known.
            ver = appr.get("version") or video.get("version") or ""
            if ver and ver not in title and j.get("id") != job_id:
                continue
            out.append(j)
    return out


def passed_candidates(videos: list[dict]) -> list[dict]:
    """Tracker videos in Passed: Ben OK'd, not scheduled, not public."""
    out = []
    for v in videos:
        if is_public(v) or is_scheduled(v):
            continue
        if v.get("lane") != "approved":
            continue
        if v.get("readyFor") == "Ben":
            continue
        out.append(v)
    return out


def plan_actions(videos: list[dict], alljobs: list[dict], *, now: dt.datetime | None = None,
                 root: Path | None = None) -> list[dict]:
    """Dry plan of create/unblock actions. No queue writes."""
    now = now or now_utc()
    root = root or ROOT
    actions = []
    from_day = now.astimezone(LONDON).date()
    # Per channel+kind: days already booked (tracker + UPLOADS), grown as this plan assigns slots.
    taken_by: dict[tuple[str, str], set[str]] = {}

    def taken_for(channel: str, vtype: str) -> set[str]:
        key = (channel, vtype)
        if key not in taken_by:
            taken_by[key] = taken_cadence_days(videos, channel, vtype, from_day, root=root)
        return taken_by[key]

    for v in passed_candidates(videos):
        listing = lp.for_video(v, root)
        dest = listing.get("destination") or "youtube"
        if not listing.get("complete"):
            actions.append({"op": "wait", "key": v.get("key"), "reason": listing.get("status") or "Needs listing",
                            "missing": listing.get("missing") or []})
            continue
        if dest == "social" and not parent_long_public(v, videos):
            actions.append({"op": "wait", "key": v.get("key"),
                            "reason": "Social waits until the parent long is public"})
            continue
        jobs = delivery_jobs_for(v, alljobs)
        # Never touch a swap path.
        if any(is_swap(j, v) for j in jobs) or is_swap(None, v):
            actions.append({"op": "skip", "key": v.get("key"), "reason": "Swap stays on its own path"})
            continue
        # Already on YouTube (this card or a sibling film/Short card) — no second upload; never retarget banned ids.
        why = already_delivered(v, videos)
        if why:
            actions.append({"op": "skip", "key": v.get("key"), "reason": why})
            continue
        live = [j for j in jobs if j.get("status") in ("open", "claimed", "blocked")]
        if live:
            j = live[0]
            if j.get("status") == "blocked" and LISTING_HOLD_RE.search(str(j.get("result") or "") + str((j.get("hold") or {}).get("condition") or "")):
                actions.append({"op": "unblock", "key": v.get("key"), "job": j["id"],
                                "destination": dest, "reason": "Listing package complete"})
            else:
                actions.append({"op": "skip", "key": v.get("key"), "job": j["id"],
                                "reason": f"Delivery job already {j.get('status')}"})
            continue
        # Create a new delivery job.
        channel = str(v.get("channel") or "OWB").upper()
        vtype = "short" if v.get("type") == "short" else "long"
        airs = ((v.get("approved") or {}).get("airs") or "")
        taken = taken_for(channel, vtype)
        slot = next_cadence_slot(channel, vtype, now=now, taken_days=taken, airs=airs)
        if dest != "social" and not slot:
            actions.append({"op": "wait", "key": v.get("key"),
                            "reason": "No free cadence slot in the next 60 days"})
            continue
        if slot:
            day = london_day(slot)
            if day:
                taken.add(day)
        title_bit = (v.get("title") or listing.get("title") or v.get("key") or "")[:80]
        num = v.get("number") or ""
        ver = (v.get("approved") or {}).get("version") or v.get("version") or ""
        if dest == "social":
            title = f"{channel} {num} {vtype}: Buffer social for {title_bit}".strip()
            body = ("Deliver social-only posts through Buffer (Instagram / Facebook / YouTube Community"
                    + ("; HOS TikTok stays Buffer-only" if channel == "HOS" else "")
                    + "). Do not use the TikTok browser or API. Only after the parent long is public when that"
                    " house rule applies. Listing package is complete.")
            kind = "studio"
        else:
            when = f", {slot}" if slot else ""
            title = f"Upload {channel} {num} {vtype} {ver} ({title_bit}) Private{when}".strip()
            body = ("Upload to YouTube Studio as Private and set publishAt in the locked cadence. "
                    "Use youtube:package on the Mini. Do not swap a file onto an existing id. "
                    f"Do not reuse {' or '.join(sorted(BANNED_REUSE_IDS))} as destinations. "
                    "Listing package is complete (title, thumbnail, description, tags).")
            kind = "studio"
        actions.append({
            "op": "create", "key": v.get("key"), "destination": dest, "title": title, "body": body,
            "kind": kind, "film": num if channel == "OWB" and re.fullmatch(r"\d{3}", str(num)) else "",
            "stage": "upload" if channel == "OWB" and re.fullmatch(r"\d{3}", str(num)) else "",
            "repo": "hos" if channel == "HOS" else "owb",
            "airs": slot, "version": ver, "channel": channel, "type": vtype,
            "approved_job": (v.get("approved") or {}).get("job") or "",
        })
    return actions


def apply_actions(data: dict, actions: list[dict], *, agent: str, at: dt.datetime) -> list[str]:
    """Mutate the queue for create/unblock actions. Returns touched job ids."""
    touched = []
    by_id = {j["id"]: j for j in data["jobs"]}
    for a in actions:
        if a.get("op") == "unblock":
            j = by_id.get(a["job"])
            if not j or j.get("status") != "blocked":
                continue
            j.update(status="open", by="", since="", eta="", result="")
            j.pop("hold", None)
            J.log(j, at, agent, "unblocked: listing package complete — ready to upload")
            touched.append(j["id"])
        elif a.get("op") == "create":
            # Idempotent: skip if a matching open job appeared this run.
            if any(x.get("title") == a["title"] and x.get("status") in ("open", "claimed", "blocked") for x in data["jobs"]):
                continue
            kwargs = {"film": a["film"], "stage": a["stage"]} if a.get("film") and a.get("stage") else {}
            job = J.do_add(data, title=a["title"], needs="mini", body=a["body"], by=agent, at=at,
                           kind=a.get("kind") or "studio", repo=a.get("repo") or "owb",
                           action=("Upload to YouTube Studio as Private" if a.get("destination") != "social"
                                   else "Schedule Buffer social posts"),
                           **kwargs)
            # Link Ben's approval onto the delivering job when we know the ask.
            src_id = a.get("approved_job") or ""
            src = by_id.get(src_id) if src_id else None
            over = {k: a[k] for k in ("airs", "version", "channel", "type", "title") if a.get(k)}
            over["card"] = a.get("key") or ""
            over["what"] = "Passed cut — deliver listing package"
            if src and (src.get("awaits_ben") or src.get("awaits_was") or src.get("approved_from")):
                try:
                    J.do_approved(job, src, agent, at, over=over)
                except ValueError:
                    job["approved_from"] = {k: str(over.get(k) or "") for k in
                                            ("what", "version", "airs", "card", "title", "number", "type", "channel")
                                            if over.get(k)}
                    job["approved_from"]["job"] = src_id or job["id"]
                    job["approved_from"]["number"] = str(a.get("film") or "")
            else:
                job["approved_from"] = {
                    "what": over.get("what") or "Passed cut — deliver listing package",
                    "version": a.get("version") or "",
                    "airs": a.get("airs") or "",
                    "card": a.get("key") or "",
                    "title": a.get("title") or "",
                    "number": a.get("film") or "",
                    "type": a.get("type") or "",
                    "channel": a.get("channel") or "",
                    "job": job["id"],
                    "okAt": J.studio.iso(at),
                }
            touched.append(job["id"])
            by_id[job["id"]] = job
    return touched


def load_owb_films(root: Path) -> list[dict]:
    """Every OWB status.json, with PACKAGE_UPLOAD_RESULT release when present (same as kanban_snapshot)."""
    films = []
    for path in sorted((root / "02_Video-Projects").glob("*/status.json")):
        try:
            film = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        if not isinstance(film, dict):
            continue
        try:
            from kanban_snapshot import release_record
            rec = release_record(str(film.get("film") or ""), root)
            if rec:
                film["release"] = rec
        except Exception:  # noqa: BLE001 — release is best-effort; UPLOADS still attaches
            pass
        films.append(film)
    return films


def load_hos_pipeline(root: Path | None = None) -> dict:
    """HOS PIPELINE.json + long upload read-back from HOS UPLOADS (board_publish / kanban_snapshot path)."""
    hos: dict = {"films": []}
    try:
        import channels
        hos_root = channels.repo_path("hos")
    except Exception:  # noqa: BLE001
        return hos
    pipe = hos_root / "00_Brand" / "Channel-Setup" / "PIPELINE.json"
    if not pipe.is_file():
        return hos
    try:
        hos = json.loads(pipe.read_text())
    except (OSError, ValueError):
        return {"films": []}
    if not isinstance(hos.get("films"), list):
        return {"films": []}
    try:
        from kanban_snapshot import attach_hos_uploads
        attach_hos_uploads(hos_root, hos)
    except Exception:  # noqa: BLE001
        pass
    return hos


def load_briefs(root: Path) -> dict:
    path = root / "05_Analytics" / "kanban" / "film_briefs.json"
    if not path.is_file():
        return {}
    try:
        doc = json.loads(path.read_text())
    except (OSError, ValueError):
        return {}
    if isinstance(doc, dict) and isinstance(doc.get("films"), dict):
        return doc["films"]
    return doc if isinstance(doc, dict) else {}


def load_delivery_videos(root: Path, alljobs: list[dict], *, now: dt.datetime) -> list[dict]:
    """Rebuild tracker videos the way the live board does — real PIPELINE, status.json, UPLOADS, briefs.

    Passing uploads={} (the old path) stripped youtube metadata so a Passed card that was already
    scheduled/public looked like it still needed an upload. Always load uploads_index (and HOS
    attachments); never invent YouTube ids.
    """
    uploads = vt.uploads_index(root)
    hos = load_hos_pipeline(root)
    owb = load_owb_films(root)
    briefs = load_briefs(root)
    live = [j for j in alljobs if j.get("status") in vt.LIVE_STATUSES]
    doc = vt.build_videos(
        hos=hos,
        owb=owb,
        briefs=briefs,
        jobs=live,
        checks={},
        uploads=uploads,
        now=now,
        approved=vt.approved_entries(alljobs),
        alljobs=alljobs,
    )
    return doc.get("videos") or []


def run(*, apply: bool = False, git: bool = False, agent: str = "relay",
        root: Path | None = None, at: dt.datetime | None = None,
        videos: list[dict] | None = None) -> dict:
    root = root or ROOT
    at = at or now_utc()
    qpath = root / "jobs" / "queue.json"
    data = json.loads(qpath.read_text()) if qpath.is_file() else {"next_id": 1, "jobs": []}
    if videos is None:
        try:
            videos = load_delivery_videos(root, data["jobs"], now=at)
        except Exception:  # noqa: BLE001 — never block the publisher; plan with whatever we have
            videos = []
    actions = plan_actions(videos, data["jobs"], now=at, root=root)
    result = {"at": at.isoformat().replace("+00:00", "Z"), "apply": apply, "actions": actions, "touched": [],
              "videos": len(videos)}
    if not apply:
        return result

    def mutate(d):
        touched = apply_actions(d, actions, agent=agent, at=at)
        result["touched"] = touched
        return {"touched": touched, "n": len(touched)}, None, []

    if git:
        out, err, _ = J.with_git(lambda d: (mutate(d)[0], None, [qpath, J.JOBS_MD]),
                                 f"jobs: approved_deliver ({len([a for a in actions if a.get('op') in ('create','unblock')])} actions)")
        if err:
            result["error"] = err
        else:
            result["touched"] = (out or {}).get("touched") or []
    else:
        out, err, _ = mutate(data)
        if err:
            result["error"] = err
        else:
            J.save(data, qpath)
            result["touched"] = out.get("touched") or []
    return result


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--apply", action="store_true", help="write create/unblock into the queue")
    p.add_argument("--git", action="store_true", help="commit queue changes (with --apply)")
    p.add_argument("--agent", default="relay")
    args = p.parse_args(argv)
    res = run(apply=args.apply, git=args.git, agent=args.agent)
    print(json.dumps({k: res[k] for k in ("at", "apply", "touched", "error") if k in res or k == "touched"}, indent=2))
    for a in res.get("actions") or []:
        print(f"  {a.get('op'):8} {a.get('key') or '-':20} {a.get('job') or ''} {a.get('reason') or a.get('title') or ''}"[:160])
    return 1 if res.get("error") else 0


if __name__ == "__main__":
    raise SystemExit(main())
