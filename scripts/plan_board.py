#!/usr/bin/env python3
"""The plan block on the studio board (J2866).

`studio/plan.json` holds the words and the dates. This builds the `plan` block the
publish adds to board.json: each step's stand, from the queue and the video tracker,
and each public test film's numbers, from the channel read the publish already has.
The page reads only that block. A second plan in the file needs no new code.

The block keeps its previous `updatedAt` when nothing behind it changed, so a quiet
publish stays quiet. The Chief changes `studio/plan.json` when a date or a decision
changes (see studio/RULES.md and STUDIO_PLAYBOOK.md §2).
"""
from __future__ import annotations

import datetime as dt
import re
from zoneinfo import ZoneInfo

import channels
from video_progress import job_targets

LONDON = ZoneInfo("Europe/London")
UTC = dt.timezone.utc


class PlanError(ValueError):
    """A date that does not parse, or a job id that is not in the queue."""


def parse_when(value: str) -> dt.datetime:
    """A date (`2026-12-13`) or a UTC instant (`2026-12-08T18:00Z`)."""
    if not isinstance(value, str) or not value:
        raise PlanError("empty date")
    if "T" not in value:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise PlanError(f"bad date {value}")
        year, month, day = (int(part) for part in value.split("-"))
        try:
            return dt.datetime(year, month, day, tzinfo=LONDON)
        except ValueError as exc:
            raise PlanError(f"bad date {value}") from exc
    if not value.endswith("Z"):
        raise PlanError(f"bad date {value}")
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PlanError(f"bad date {value}") from exc


def validate(plans, job_ids: set[str]) -> None:
    """Every job id is in the queue, and every date parses. An empty step date is allowed."""
    if not isinstance(plans, list) or not plans:
        raise PlanError("studio/plan.json must be a list of plans")
    for plan in plans:
        parse_when(plan.get("agreed") or "")
        base = plan.get("baseline") or {}
        parse_when(base.get("readAt") or "")
        for step in plan.get("steps") or []:
            if step.get("when"):
                parse_when(step["when"])
            for job_id in step.get("jobs") or []:
                if job_id not in job_ids:
                    raise PlanError(f"{job_id} is not in the queue")
            test = step.get("test") or {}
            if test and (int(test.get("days") or 0) < 1 or "keep" not in test or "drop" not in test):
                raise PlanError(f"{step.get('id') or 'step'} has a test with no days, keep or drop")
        for decision in plan.get("decisions") or []:
            parse_when(decision.get("at") or "")


def _as_utc(moment: dt.datetime) -> dt.datetime:
    if moment.tzinfo is None:
        return moment.replace(tzinfo=UTC)
    return moment.astimezone(UTC)


def _london(moment: dt.datetime) -> dt.datetime:
    return _as_utc(moment).astimezone(LONDON)


def _day_label(moment: dt.datetime) -> str:
    local = moment if moment.tzinfo == LONDON and "T" not in "" else _london(moment)
    return f"{local.strftime('%a')} {local.day} {local.strftime('%b')}"


def when_label(value: str, *, with_time: bool) -> str:
    if not value:
        return "No date yet"
    moment = parse_when(value)
    label = _day_label(moment)
    if with_time and "T" in value:
        label += ", " + _london(moment).strftime("%H:%M")
    return label


def _read_label(value: str) -> str:
    moment = parse_when(value)
    local = _london(moment)
    return f"{local.day} {local.strftime('%b')}"


def _decision_label(value: str) -> str:
    moment = parse_when(value)
    local = _london(moment)
    return f"{local.day} {local.strftime('%b')} {local.year}"


def short_name(name: str) -> str:
    return (name or "").split("(", 1)[0].strip()


def _figure_count(value):
    if value is None:
        return "no figure yet"
    number = int(value) if isinstance(value, (int, float)) and float(value).is_integer() else value
    if isinstance(number, int):
        return f"{number:,}"
    return "no figure yet"


def _percent(value):
    if value is None or isinstance(value, bool):
        return "no figure yet"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "no figure yet"
    text = f"{number:.2f}".rstrip("0").rstrip(".")
    return text + "%"


def _days_live(publish_at: str, now: dt.datetime) -> int:
    start = _as_utc(parse_when(publish_at))
    elapsed = _as_utc(now) - start
    if elapsed.total_seconds() < 0:
        return 0
    return int(elapsed.total_seconds() // 86400) + 1


def _until_label(publish_at: str, days: int) -> str:
    start = _as_utc(parse_when(publish_at))
    return _day_label(start + dt.timedelta(days=max(days, 1) - 1))


def _video_for(step: dict, videos: list, jobs_by_id: dict) -> dict | None:
    films = [str(step.get("film") or "").strip()]
    keys = set()
    for job_id in step.get("jobs") or []:
        job = jobs_by_id.get(job_id) or {}
        film = str(job.get("film") or "").strip()
        if film:
            films.append(film)
        keys.update(job_targets(job))
    for film in films:
        if not film:
            continue
        keys.add(film)
        for label in channels.labels():
            keys.add(f"{label}:{film}")
    wanted = set(step.get("jobs") or [])
    for video in videos or []:
        if not isinstance(video, dict):
            continue
        if video.get("key") in keys or str(video.get("number") or "") in keys:
            return video
        ids = {item.get("id") for item in (video.get("jobs") or []) if isinstance(item, dict)}
        if ids & wanted:
            return video
    return None


def _picture(video: dict | None) -> str:
    youtube = (video or {}).get("youtube") or {}
    if not isinstance(youtube, dict) or not youtube:
        return ""
    privacy = youtube.get("privacy") or ""
    state = youtube.get("state") or ""
    if privacy == "public" or state == "live":
        return "live"
    if state == "scheduled" or youtube.get("publishAt"):
        return "scheduled"
    if youtube.get("videoId"):
        return "private"
    return ""


def _progress_phrase(job: dict) -> str:
    blob = " ".join(str(job.get(key) or "") for key in ("title", "remaining_action", "plain")).lower()
    head = "Being repaired" if "repair" in blob else "In progress"
    progress = job.get("progress") or {}
    step, total = progress.get("step"), progress.get("of")
    if isinstance(step, int) and isinstance(total, int) and total >= 1 and step > 0:
        return f"{head}, step {step} of {total}"
    return head


def stand_of(step: dict, related: list, video: dict | None, now: dt.datetime) -> str:
    picture = _picture(video)
    youtube = (video or {}).get("youtube") or {}
    test = step.get("test") or {}
    if picture == "live":
        publish_at = youtube.get("publishAt") or ""
        if publish_at:
            day = _days_live(publish_at, now)
            span = int(test.get("days") or 0)
            if span:
                return f"Live, day {day} of {span}"
            return f"Live, day {day}"
        return "Live"
    if picture == "scheduled":
        return "Scheduled"
    if picture == "private":
        return "Uploaded, private"
    if step.get("needsBen") and not step.get("when"):
        return "Waiting for your lock"
    claimed = [job for job in related if job.get("status") == "claimed"]
    if claimed:
        return _progress_phrase(claimed[0])
    listing_done = any(job.get("kind") == "listing" and job.get("status") == "done" for job in related)
    if listing_done:
        return "Listing ready"
    if any(job.get("status") in ("open", "blocked") for job in related):
        return "Waiting its turn"
    if related and all(job.get("status") == "done" for job in related):
        return "Done"
    return "Not started yet"


def _lock_bit(step: dict) -> str:
    if "planet" in (step.get("name") or "").lower():
        return "lock the every-planet film"
    name = short_name(step.get("name") or "this film")
    return "lock " + name[0].lower() + name[1:]


def _needs_line(steps: list) -> str:
    waiting = [step for step in steps if step.get("stand") == "Waiting for your lock"]
    if not waiting:
        return ""
    if len(waiting) == 1:
        return "1 thing needs you: " + _lock_bit(waiting[0])
    return f"{len(waiting)} things need you"


def _next_line(steps: list, now: dt.datetime) -> str:
    coming = []
    for step in steps:
        value = step.get("when") or ""
        if not value:
            continue
        moment = parse_when(value)
        if "T" in value:
            if _as_utc(moment) < _as_utc(now):
                continue
        elif moment.date() < _london(now).date():
            continue
        coming.append((moment, step))
    if not coming:
        return "Next: nothing dated ahead"
    moment, step = min(coming, key=lambda item: _as_utc(item[0]))
    return f"Next: {short_name(step.get('name') or 'the next film')}, {_day_label(moment)}"


def _analytics_index(analytics: dict | None) -> dict:
    found = {}
    for channel in (analytics or {}).get("channels") or []:
        for video in channel.get("videos") or []:
            if isinstance(video, dict) and video.get("id"):
                found[video["id"]] = video
    return found


def _stat(row: dict, *keys):
    for key in keys:
        if key in row and row.get(key) is not None:
            return row.get(key)
    lifetime = row.get("lifetime")
    if isinstance(lifetime, dict):
        for key in keys:
            if key in lifetime and lifetime.get(key) is not None:
                return lifetime.get(key)
    return None


def _verdict(views, test: dict, day: int, publish_at: str) -> dict:
    """Keep at `keep` or more, One more from `drop` up to just under `keep`, else Drop or change.
    Before day `days`, the row is still reading on."""
    span = int(test.get("days") or 14)
    if day < span:
        return {"verdict": "reading on", "until": _until_label(publish_at, span)}
    if views is None:
        return {"verdict": "no figure yet", "until": ""}
    keep, drop = test.get("keep"), test.get("drop")
    if keep is not None and views >= keep:
        word = "Keep"
    elif drop is not None and views >= drop:
        word = "One more"
    else:
        word = "Drop or change"
    return {"verdict": word, "until": ""}


def _result_row(step: dict, video: dict, numbers: dict, now: dt.datetime) -> dict | None:
    test = step.get("test") or {}
    if not test or _picture(video) != "live":
        return None
    youtube = video.get("youtube") or {}
    publish_at = youtube.get("publishAt") or ""
    if not publish_at:
        return None
    video_id = youtube.get("videoId") or ""
    row = numbers.get(video_id) or {}
    views = _stat(row, "views", "studioViews")
    day = _days_live(publish_at, now)
    called = _verdict(views, test, day, publish_at)
    return {
        "id": step.get("id") or "",
        "name": short_name(step.get("name") or ""),
        "daysLive": day,
        "daysText": f"Day {day} of {int(test.get('days') or day)}",
        "views": _figure_count(views),
        "showings": _figure_count(_stat(row, "impressions")),
        "clickRate": _percent(_stat(row, "impressionsCtr")),
        "share": _percent(_stat(row, "studioAvgViewPct")),
        "verdict": called["verdict"],
        "until": called["until"],
    }


def _score_line(results: list, baseline: dict) -> str:
    if (baseline or {}).get("bestLongViews") is None:
        tail = ""
        if not results:
            return "No film is public yet."
    else:
        tail = f"Best long so far: {_figure_count((baseline or {}).get('bestLongViews'))} views"
    if not results:
        return f"No test film is public yet. {tail}"
    def views_of(row):
        text = row.get("views") or ""
        if text == "no figure yet":
            return -1
        try:
            return int(text.replace(",", ""))
        except ValueError:
            return -1
    top = max(results, key=views_of)
    return f"{top.get('name') or 'The test film'}: {top.get('views')} views on day {top.get('daysLive')}. {tail}".strip()


def _baseline_row(baseline: dict) -> dict:
    showings = _figure_count((baseline or {}).get("longShowingsTotal"))
    longs = (baseline or {}).get("longs")
    if not longs and (baseline or {}).get("bestLongViews") is None:
        return {"best": "No long film yet", "showings": f"No long films yet (read {_read_label((baseline or {}).get('readAt') or '')})"}
    return {
        "best": f"Best long so far: {_figure_count((baseline or {}).get('bestLongViews'))} views",
        "showings": f"All {longs} longs: about {showings} showings (read {_read_label((baseline or {}).get('readAt') or '')})",
    }


def _one(plan: dict, jobs_by_id: dict, videos: list, numbers: dict, now: dt.datetime) -> dict:
    steps = []
    results = []
    for raw in plan.get("steps") or []:
        related = [jobs_by_id[job_id] for job_id in (raw.get("jobs") or []) if job_id in jobs_by_id]
        video = _video_for(raw, videos, jobs_by_id)
        stand = stand_of(raw, related, video, now)
        built = {
            "id": raw.get("id") or "",
            "name": raw.get("name") or "",
            "what": raw.get("what") or "",
            "when": when_label(raw.get("when") or "", with_time=True),
            "stand": stand,
            "needsYou": stand == "Waiting for your lock",
            "videoKey": (video or {}).get("key") or "",
            "jobs": list(raw.get("jobs") or []),
        }
        steps.append({**raw, **built, "stand": stand})
        row = _result_row(raw, video or {}, numbers, now) if video else None
        if row:
            results.append(row)
    # steps above mixed raw fields (when as the source date) back in. Rebuild clean rows.
    clean = []
    for raw, mixed in zip(plan.get("steps") or [], steps):
        clean.append({
            "id": raw.get("id") or "",
            "name": raw.get("name") or "",
            "what": raw.get("what") or "",
            "when": mixed["when"],
            "stand": mixed["stand"],
            "needsYou": mixed["needsYou"],
            "videoKey": mixed["videoKey"],
            "jobs": list(raw.get("jobs") or []),
        })
    decisions = []
    for index, decision in enumerate(plan.get("decisions") or []):
        decisions.append((decision.get("at") or "", index, {
            "at": _decision_label(decision.get("at") or ""),
            "by": decision.get("by") or "",
            "text": decision.get("text") or "",
        }))
    decisions.sort(key=lambda item: (item[0], item[1]), reverse=True)
    baseline = plan.get("baseline") or {}
    return {
        "id": plan.get("id") or "",
        "channel": plan.get("channel") or "",
        "title": plan.get("title") or "",
        "goal": plan.get("goal") or "",
        "why": list(plan.get("why") or []),
        "card": {
            "title": "Plan: " + (plan.get("title") or "the plan")[:1].lower() + (plan.get("title") or "the plan")[1:],
            "next": _next_line(plan.get("steps") or [], now),
            "needs": _needs_line(clean),
            "score": _score_line(results, baseline),
        },
        "steps": clean,
        "results": results,
        "baseline": _baseline_row(baseline),
        "decisions": [item[2] for item in decisions],
    }


def section(plans, jobs, videos, analytics, updated_at: str, previous: dict | None = None, now: dt.datetime | None = None) -> dict:
    """The plan block. `updated_at` is the publish time. It is kept from `previous` when the rest matches."""
    now = now or dt.datetime.now(UTC)
    if now.tzinfo is None:
        now = now.replace(tzinfo=UTC)
    job_list = [job for job in (jobs or []) if isinstance(job, dict) and job.get("id")]
    validate(plans, {job["id"] for job in job_list})
    jobs_by_id = {job["id"]: job for job in job_list}
    body = {"plans": [_one(plan, jobs_by_id, videos or [], _analytics_index(analytics), now) for plan in plans]}
    prev = previous or {}
    prev_body = {key: value for key, value in prev.items() if key != "updatedAt"}
    if prev_body == body and prev.get("updatedAt"):
        body["updatedAt"] = prev["updatedAt"]
    else:
        body["updatedAt"] = updated_at
    return body
