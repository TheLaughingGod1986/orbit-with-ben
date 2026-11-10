#!/usr/bin/env python3
"""First-day check: a few hours after a video goes live, read how it is doing, say why, and say what to do.

    python3 scripts/launch_check.py due                    which videos are due a check now (nothing written)
    python3 scripts/launch_check.py record <id> --hours 6 --views 4 --rank 10 --of 10 [more figures] [--git]
    python3 scripts/launch_check.py judge <id>             the verdict, what is different about it, what to do
    python3 scripts/launch_check.py note <id> "what we did about it" [--git]
    python3 scripts/launch_check.py report                 every checked video, and what the weak starts share

Ben, 10 Nov 2026, with a Short on 4 views after 77 minutes where the two before it reached 1,000 and 1,200: "set
something up in the Studio to learn from our failures and iterate and improve ... do a scan or an audit, maybe 5-6
hours after the short goes live or the long goes live ... or even on the same video, we can iterate and improve the
video if we know how to fix it."

Why six hours. Our daily snapshots show a Short gets nearly all its views in its first day: the Short that had 888
views the next morning has 892 now. So the first hours are the only time a fault can still be put right, and the only
time a weak start can be told apart from a slow one.

How it runs, with nobody asking:
  1. `refill.py` (the Mini's 10-minute tick) calls `queue_due`. A video on any plugged-in channel that went live
     6 hours ago gets one job; a long gets a second at 48 hours, when it has enough impressions to judge its title
     and thumbnail. One job per video and age, ever.
  2. The job is read-only in YouTube Studio: is anything broken, then the numbers. The worker stores them with
     `record` and pastes `judge` into the job's result.
  3. `judge` says where it stands against our own recent videos, which step lost the viewers (not shown, swiped,
     left early, not clicked), what is different about this video, what can still be fixed on it, and what to carry
     to the next ones. The Chief acts on that and writes what was done with `note`.
  4. The weekly audit starts from `report`. A difference seen on three weak starts goes to the Chief as a rule or a
     test in 05_Analytics/LEARNINGS.md, the one rulebook. This script never writes a rule itself.

What it reads: each channel's newest daily snapshot (every scheduled video and its publish time), its register of
uploads, and its Studio read (`studio_ctr.json`, for the channel's own usual rates). What it writes: one file per
video, `<the channel's numbers folder>/launch/<video id>.json`. It never touches YouTube.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import functools
import json
import pathlib
import re
import statistics
import sys
from zoneinfo import ZoneInfo

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import channels  # noqa: E402
import studio  # noqa: E402

LONDON = ZoneInfo("Europe/London")

# Hours after going live at which a video is checked. A long is looked at twice: at 6 h for faults, at 48 h for its
# title and thumbnail, which need impressions before they can be judged.
CHECKS = {"short": (6,), "long": (6, 48)}
LATE_H = 18          # a check that could not run on time is still worth making this late; after that the daily read has it
LOOK_BACK = 10       # "our recent videos": the ten before this one, same channel and format
MIN_TO_COMPARE = 3   # fewer earlier figures than this is not a baseline
FIRST_MORNING_H = 36  # a snapshot this soon after going live counts as "by the next morning"
BEHIND, AHEAD = 0.4, 1.5   # against the median of the same figure at the same age
SHOWN_MIN = 100      # below this Studio has too few viewers to say anything about the cut
CTR_FLOOR = 2.0      # a long's click rate (%), judged only from 200 impressions up
CTR_MIN_IMPRESSIONS = 200
GONE = ("supersededBy", "retired", "replacedBy")   # register marks: this upload will never air
FIGURES = ("views", "typical", "rank", "of", "shown", "feedViews", "stayed", "avgPct", "impressions", "ctr", "likes")
COMPARED = ("views", "shown", "stayed", "avgPct", "impressions", "ctr")   # figures that have a "usual for us"
STOP = set("""about after already been before being could does ever every feel from have into just last like long
made many more most much over real really than that their there they this time what when where which while will with
would year years your days first were still does""".split())
FORMAT_NAME = {"short": "Short", "long": "long"}


def _json(path: pathlib.Path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def _snapshot_files(slug: str) -> list[pathlib.Path]:
    return sorted((channels.analytics_dir(slug) / "snapshots").glob("*.json"))


def _snapshot(path: pathlib.Path):
    """(when it was taken, {video id: its row}) or None. Read once per file version: a report reads them often."""
    try:
        return _snapshot_at(str(path), path.stat().st_mtime_ns)
    except OSError:
        return None


@functools.lru_cache(maxsize=256)
def _snapshot_at(path_text: str, _version: int):
    path = pathlib.Path(path_text)
    doc = _json(path)
    if not isinstance(doc, dict):
        return None
    taken = doc.get("takenAt") or f"{doc.get('date') or path.stem}T06:40:00Z"
    try:
        return studio.parse(taken), {v["id"]: v for v in doc.get("videos") or [] if v.get("id")}
    except (ValueError, TypeError):
        return None


def latest_snapshot(slug: str):
    for path in reversed(_snapshot_files(slug)):
        snap = _snapshot(path)
        if snap:
            return snap
    return None


def register(slug: str) -> dict:
    """The channel's uploads register: {video id: entry}. Empty when its checkout is not on this machine."""
    path = channels.uploads_file(slug)
    doc = _json(path) if path else None
    return (doc or {}).get("videos") or {}


def went_live(slug: str, now: dt.datetime, days: float = 4) -> list[dict]:
    """Videos of this channel that went live in the last `days`: the newest snapshot first (YouTube's own record of
    every scheduled video), then the register for anything scheduled since that snapshot was taken."""
    snap = latest_snapshot(slug)
    reg = register(slug)
    out = {}
    for vid, v in (snap[1] if snap else {}).items():
        if v.get("format") not in CHECKS:
            continue
        public = v.get("privacy") == "public"
        when = v.get("publishedAt") if public else v.get("publishAt")
        entry = reg.get(vid) or {}
        pulled = entry.get("unscheduledAt")
        if not public and (any(entry.get(k) for k in GONE) or (pulled and studio.parse(pulled) > snap[0])):
            continue   # taken off the schedule since the snapshot
        if when:
            out[vid] = {"id": vid, "title": v.get("title") or entry.get("title") or "", "format": v["format"],
                        "at": studio.parse(when), "seconds": v.get("seconds")}
    for vid, entry in reg.items():
        if vid in out or entry.get("kind") not in CHECKS or not entry.get("publishAt"):
            continue
        if any(entry.get(k) for k in GONE) or entry.get("unscheduledAt") or (snap and vid in snap[1]):
            continue
        out[vid] = {"id": vid, "title": entry.get("title") or "", "format": entry["kind"],
                    "at": studio.parse(entry["publishAt"]), "seconds": None}
    return sorted((v for v in out.values() if now - dt.timedelta(days=days) <= v["at"] <= now),
                  key=lambda v: (v["at"], v["id"]))


def lookup(vid: str, now: dt.datetime | None = None) -> tuple[str, dict] | None:
    """(channel, what we know about the video) for a video id, whichever channel it is on."""
    now = now or dt.datetime.now(dt.timezone.utc)
    for slug in channels.slugs():
        for v in went_live(slug, now, days=3650):
            if v["id"] == vid:
                return slug, v
    return None


# ---- the record of one video -------------------------------------------------------------------------------------

def record_path(slug: str, vid: str) -> pathlib.Path:
    return channels.analytics_dir(slug) / "launch" / f"{vid}.json"


def load_record(slug: str, vid: str) -> dict | None:
    doc = _json(record_path(slug, vid))
    return doc if isinstance(doc, dict) else None


def records(slug: str) -> list[dict]:
    out = [doc for path in sorted((channels.analytics_dir(slug) / "launch").glob("*.json"))
           if isinstance(doc := _json(path), dict) and doc.get("id")]
    return sorted(out, key=lambda r: (r.get("wentLive") or "", r["id"]))


def with_reading(rec: dict | None, slug: str, video: dict, reading: dict, faults=()) -> dict:
    """The record with this reading added. A second reading at the same age replaces the first (a correction)."""
    rec = dict(rec or {"id": video["id"], "channel": slug, "format": video["format"], "title": video["title"],
                       "wentLive": studio.iso(video["at"]), "seconds": video.get("seconds"),
                       "readings": [], "faults": [], "notes": []})
    reading = {k: v for k, v in reading.items() if v is not None}
    rec["readings"] = sorted([r for r in rec.get("readings", []) if r.get("hours") != reading["hours"]] + [reading],
                             key=lambda r: r["hours"])
    rec["faults"] = list(dict.fromkeys(list(rec.get("faults", [])) + [f.strip() for f in faults if f.strip()]))
    return rec


def save_record(slug: str, rec: dict) -> pathlib.Path:
    path = record_path(slug, rec["id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rec, indent=2) + "\n")
    return path


# ---- what is due, and the job that does it -----------------------------------------------------------------------

def due(now: dt.datetime, queue: dict | None = None) -> list[dict]:
    """Every (video, age) whose check is due now and has neither a reading nor a job yet."""
    asked = {j.get("launch") for j in (queue or {}).get("jobs", []) if j.get("launch")}
    out = []
    for slug in channels.slugs():
        for v in went_live(slug, now):
            have = {r.get("hours") for r in (load_record(slug, v["id"]) or {}).get("readings", [])}
            for hours in CHECKS[v["format"]]:
                start = v["at"] + dt.timedelta(hours=hours)
                if start <= now <= start + dt.timedelta(hours=LATE_H) and hours not in have \
                        and f"{v['id']}@{hours}" not in asked:
                    out.append({**v, "channel": slug, "hours": hours})
    return sorted(out, key=lambda d: (d["at"], d["id"], d["hours"]))


def _when(t: dt.datetime) -> str:
    return t.astimezone(LONDON).strftime("%a %-d %b %H:%M")


def job_spec(item: dict) -> dict:
    """Title, body and board line of the job that makes one check."""
    kind = FORMAT_NAME[item["format"]]
    name = item["title"] or item["id"]
    port = channels.studio_port(item["channel"])
    browser = f"its signed-in Studio browser (CDP {port})" if port else "its signed-in Studio browser"
    if item["format"] == "short":
        figures = ("Analytics for the video, period \"Since published\". Overview: views, the line \"N more (or less) "
                   "than usual\" (give the usual figure: views minus or plus N), and \"Ranking by views N of 10\" (it "
                   "may only be on the channel dashboard's latest-Short card). Reach: the views that came from the "
                   "Shorts feed (traffic sources), and Shown in feed if Studio has that card. Engagement: Viewed vs "
                   "swiped away (the % who stayed), Average percentage viewed. Likes.")
        flags = "--typical <n> --feed-views <n> --stayed <%> --avg-pct <%> --likes <n>` (add `--shown <n>` if Studio shows it) `"
    else:
        figures = ("Analytics for the video, period \"Since published\". Overview: views, the line \"N more (or less) "
                   "than usual\" (give the usual figure: views minus or plus N), and \"Ranking by views N of 10\". "
                   "Reach: Impressions and Impressions click-through rate. Engagement: Average percentage viewed. "
                   "Likes.")
        flags = "--typical <n> --impressions <n> --ctr <%> --avg-pct <%> --likes <n>"
    body = f"""First-day check, {item['hours']} hours after it went live (Ben, 10 Nov 2026; scripts/launch_check.py). Read-only: change nothing in Studio. £0. About 15 minutes.

Video: "{name}" (`{item['id']}`), {channels.name(item['channel'])}, a {kind}. It went live {_when(item['at'])} London. Use {browser}.

1. Is anything broken? Studio > Content > the video. Visibility is Public. {"It is listed under the Shorts tab. " if item['format'] == 'short' else ""}The Restrictions column is empty (no copyright claim, not "Made for kids", no age restriction). HD processing has finished. The Related video and the description are as its upload package says. Write each thing that is wrong as one plain line.

2. Read the numbers. {figures} Where Studio has no figure yet, leave that flag out; never guess a number.

3. Store them:
   `python3 scripts/launch_check.py record {item['id']} --hours {item['hours']} --views <n> --rank <N> --of 10 {flags} --by <your agent name> --git`
   Leave out any flag Studio gives no figure for.
   Add `--fault "<what is wrong>"` once for each thing found in step 1.

4. Paste the whole output of `python3 scripts/launch_check.py judge {item['id']}` as this job's result.

5. If step 1 found a fault, or the verdict is BEHIND, park for the Chief: "parked for Chief: first-day check, <the verdict line>". The Chief decides what is changed on the video. Otherwise close the job as done.

Never: edit the video, its title, cover, description, visibility, schedule or any setting. Never delete anything. No spend."""
    return {
        "title": f"First-day check at {item['hours']} h: \"{name[:70]}\" ({item['id']})",
        "body": body,
        "action": f"Read the {kind}'s Studio numbers {item['hours']} h after it went live, record them and give the verdict"[:180],
        "plain": f"Check how \"{name[:60]}\" is doing {item['hours']} hours after it went live",
    }


def queue_due(data: dict, at: dt.datetime) -> list[str]:
    """Add one job to the queue for each check that is due. Returns the new job ids."""
    import jobs

    added = []
    for item in due(at, data):
        spec = job_spec(item)
        job = jobs.do_add(data, title=spec["title"], needs="mini", body=spec["body"], by="refill", at=at,
                          repo=item["channel"], eta_min=20, kind="studio", action=spec["action"],
                          due=studio.iso(at + dt.timedelta(hours=2)))
        job["launch"] = f"{item['id']}@{item['hours']}"
        job["plain"] = spec["plain"]
        added.append(job["id"])
    return added


# ---- what our own recent videos did ------------------------------------------------------------------------------

def history(slug: str, fmt: str) -> list[dict]:
    """Every video of this format the snapshots saw go public, oldest first, with its views in the first snapshot
    taken after it went live (`firstMorning`; None when that snapshot came too late to mean the first day)."""
    seen = {}
    for path in _snapshot_files(slug):
        snap = _snapshot(path)
        if not snap:
            continue
        taken, videos = snap
        for vid, v in videos.items():
            if vid in seen or v.get("format") != fmt or v.get("privacy") != "public" or not v.get("publishedAt"):
                continue
            at = studio.parse(v["publishedAt"])
            age = (taken - at).total_seconds() / 3600
            seen[vid] = {"id": vid, "title": v.get("title") or "", "seconds": v.get("seconds"), "at": at,
                         "firstMorning": v.get("views") if 0 <= age <= FIRST_MORNING_H else None}
    return sorted(seen.values(), key=lambda h: (h["at"], h["id"]))


def _median(values) -> float | None:
    values = [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]
    return statistics.median(values) if len(values) >= MIN_TO_COMPARE else None


def same_age(slug: str, fmt: str, hours: int, before: str, exclude: str) -> dict:
    """Medians of each figure at the same age, over the last ten earlier videos of this format that were checked."""
    rows = [r for rec in records(slug) if rec.get("format") == fmt and rec["id"] != exclude
            and (rec.get("wentLive") or "") < before for r in rec.get("readings", []) if r.get("hours") == hours]
    rows = rows[-LOOK_BACK:]
    out = {k: m for k in COMPARED if (m := _median(r.get(k) for r in rows)) is not None}
    if out:
        out["n"] = len(rows)
    return out


def usual_rates(slug: str, fmt: str) -> dict:
    """The channel's own usual rates from its lifetime Studio read: what "normal for us" is before there are enough
    first-day checks to compare like with like."""
    videos = ((_json(channels.analytics_dir(slug) / "studio_ctr.json") or {}).get("videos") or {}).values()
    if fmt == "short":
        rows = [v for v in videos if "stayedToWatch" in v and (v.get("views") or 0) >= 100]
        got = {"stayed": _median(v.get("stayedToWatch") for v in rows), "avgPct": _median(v.get("avgViewPct") for v in rows)}
    else:
        rows = [v for v in videos if (v.get("impressions") or 0) >= CTR_MIN_IMPRESSIONS]
        got = {"ctr": _median(v.get("impressionsCtr") for v in rows), "avgPct": _median(v.get("avgViewPct") for v in rows)}
    return {k: v for k, v in got.items() if v is not None}


def _words(title: str) -> set[str]:
    found = (re.sub(r"['’]s$", "", w).replace("'", "").replace("’", "") for w in re.findall(r"[a-z0-9'’]+", title.lower()))
    return {w for w in found if len(w) >= 4 and w not in STOP}


def _opener(title: str) -> str:
    first = re.findall(r"[A-Za-z']+", title)
    return first[0].lower() if first else ""


def differences(slug: str, video: dict) -> list[dict]:
    """What sets this video apart from the ones before it, as [{key, text}]. Each line is a fact from our own
    numbers, not a cause: the weekly audit decides what three of the same add up to."""
    earlier = [h for h in history(slug, video["format"]) if h["at"] < video["at"] and h["id"] != video["id"]]
    recent = earlier[-LOOK_BACK:]
    out = []
    kind = FORMAT_NAME[video["format"]] + "s"
    if len(recent) >= MIN_TO_COMPARE:
        slots = collections.Counter(h["at"].astimezone(LONDON).strftime("%H:%M") for h in recent)
        usual = slots.most_common(1)[0][0]
        mine = video["at"].astimezone(LONDON).strftime("%H:%M")
        if mine != usual and abs(_minutes(mine) - _minutes(usual)) > 20:
            out.append({"key": "slot", "text": f"It went live at {mine} London; the last {len(recent)} {kind} mostly at {usual}."})
        lengths = [h["seconds"] for h in recent if h.get("seconds")]
        if video.get("seconds") and lengths and not min(lengths) <= video["seconds"] <= max(lengths):
            out.append({"key": "length", "text": f"It is {video['seconds']} s long; the last {len(lengths)} {kind} "
                                                 f"were {min(lengths)} to {max(lengths)} s."})
    overall = _median(h["firstMorning"] for h in earlier)
    if overall:
        def against(group, what, key):
            mid = _median(group)
            if mid is None:
                return
            ratio = mid / overall
            if ratio <= 0.5 or ratio >= AHEAD:
                out.append({"key": f"{key}-{'weak' if ratio <= 0.5 else 'strong'}",
                            "text": f"{what} {len(group)} earlier {kind}: they had {round(mid)} views by the next "
                                    f"morning (median), against {round(overall)} for all {kind}."})
        for word in sorted(_words(video["title"])):
            against([h["firstMorning"] for h in earlier if word in _words(h["title"]) and h["firstMorning"] is not None],
                    f"\"{word.capitalize()}\" was in the title of", "subject")
        opener = _opener(video["title"])
        if opener:
            against([h["firstMorning"] for h in earlier if _opener(h["title"]) == opener and h["firstMorning"] is not None],
                    f"The title starts with \"{opener.capitalize()}\", like", "opener")
    entry = register(slug).get(video["id"]) or {}
    old = entry.get("supersedes") or entry.get("replaces")
    if old:
        out.append({"key": "reupload", "text": f"It is a second upload of the same video (it replaced {old})."})
    return out


def _minutes(hhmm: str) -> int:
    return int(hhmm[:2]) * 60 + int(hhmm[3:])


# ---- the verdict -------------------------------------------------------------------------------------------------

ADVICE = {
    ("short", "not shown"): (
        ["Nothing in the cut explains this yet: YouTube has shown it to too few people to judge it.",
         "Check the faults list is empty, then read tomorrow morning's snapshot. Under a tenth of the usual first "
         "day means the feed tried it and stopped: treat the subject and the title as the cause, not the edit."],
        ["If the subject line below says earlier videos on it were weak too, take that subject off the next four "
         "weeks of the schedule and tell the topic go/no-go."]),
    ("short", "swiped"): (
        ["People were shown it and swiped away: the first second or the promise is the fault. A live Short cannot "
         "be re-cut, and its title does not change what the feed shows.",
         "Run the first-second gate (`gate_shorts_open.py`) on every scheduled Short and fix the ones that share "
         "the fault before they air."],
        ["A re-cut may go out later as a new upload only after Ben has watched it; the old one stays up (we never "
         "delete a video)."]),
    ("short", "left early"): (
        ["People stayed past the first second, then left: a hold over 4 s, a pause, or the answer given too soon "
         "(LEARNINGS rules 3, 6 and 7). Nothing can be changed on the live Short."],
        ["Check the scheduled Shorts for the same hold or pause and fix them before they air."]),
    ("short", "small pool"): (
        ["It was shown and watched about as usual, to few people so far. Nothing to fix."],
        ["Read tomorrow morning's snapshot before drawing anything from it."]),
    ("long", "not shown"): (
        ["Few impressions. While a channel is small a long is shown by search and by our own Shorts (LEARNINGS rule "
         "26). Check today: its Shorts have it as their Related video; the title starts with the phrase people "
         "type; the first two lines of the description say it again.",
         "These are listing fixes and can be made on the live video. The Chief queues them."],
        ["If the phrase has no search suggestions, say so at the next topic go/no-go."]),
    ("long", "not clicked"): (
        ["It is being shown and not clicked: title and thumbnail.",
         "Allowed on a live long: a title in the rule 26 shape (search phrase first, stakes in a bracketed tail), "
         "with the before, after and time recorded. A thumbnail test only where no Test & Compare is set: a set "
         "test is never replaced or deleted without Ben."],
        ["Give the losing title and thumbnail idea to the weekly thumbnail audit."]),
    ("long", "left early"): (
        ["It is clicked and then left early: the opening. A live long cannot be re-cut."],
        ["Carry it to the next long's first 30 seconds (LEARNINGS rule 10, and the proof-first test in rule 30)."]),
    ("long", "small pool"): (
        ["Shown, clicked and watched about as usual, to few people so far. Nothing to fix."],
        ["Look again at the 48 hour check."]),
}


def shown_in_feed(reading: dict):
    """How many times the feed showed a Short. Studio does not always give the figure (10 Nov 2026: no "Shown in
    feed" card on either Short read), so without it: the views that came from the feed, divided by the share who
    stayed. "Viewed vs swiped away" is exactly that share, so 2 feed views at 25% stayed means about 8 showings."""
    if reading.get("shown") is not None:
        return reading["shown"]
    feed, stayed = reading.get("feedViews"), reading.get("stayed")
    if feed is None:
        return None
    return round(feed / (stayed / 100)) if stayed else feed


NO_FIGURES = ["Studio gave no reach figures at this check, so the step that lost the viewers is not known. Read "
              "them again before deciding anything."]


def _below(value, usual, margin: float) -> bool:
    return value is not None and usual is not None and value < usual - margin


def _stage(fmt: str, reading: dict, base: dict, usual: dict) -> str:
    """Which step lost the viewers: "not shown", "swiped" or "not clicked", "left early", "small pool". "" when
    Studio gave no reach figure to tell by. Only asked of a video that is behind."""
    shown = shown_in_feed(reading) if fmt == "short" else reading.get("impressions")
    usual_shown = base.get("shown" if fmt == "short" else "impressions")
    if shown is None:
        return ""
    if shown < (BEHIND * usual_shown if usual_shown else SHOWN_MIN):
        return "not shown"
    avg = reading.get("avgPct")
    usual_avg = base.get("avgPct") or usual.get("avgPct")
    if fmt == "short":
        if _below(reading.get("stayed"), base.get("stayed") or usual.get("stayed"), 10):
            return "swiped"
        return "left early" if _below(avg, usual_avg, 15) else "small pool"
    ctr = reading.get("ctr")
    if ctr is not None and shown >= CTR_MIN_IMPRESSIONS and ctr < CTR_FLOOR:
        return "not clicked"
    return "left early" if _below(avg, usual_avg, 8) else "small pool"


def verdict(slug: str, rec: dict, hours: int | None = None) -> dict:
    """Where the video stands at its latest check (or the one at `hours`), why, and what to do."""
    readings = [r for r in rec.get("readings", []) if hours is None or r.get("hours") == hours]
    if not readings:
        return {"level": "unknown", "stage": "", "why": ["No reading has been recorded yet."], "now": [], "carry": [],
                "differences": [], "hours": hours}
    reading = readings[-1]
    fmt = rec["format"]
    at = studio.parse(rec["wentLive"])
    base = same_age(slug, fmt, reading["hours"], rec["wentLive"], rec["id"])
    usual = usual_rates(slug, fmt)
    why, level = [], "unknown"
    views, rank, of = reading.get("views"), reading.get("rank"), reading.get("of")
    if views is not None and base.get("views") is not None:
        ratio = views / max(base["views"], 1)
        level = "behind" if ratio < BEHIND else "ahead" if ratio > AHEAD else "usual"
        why.append(f"{views} views at {reading['hours']} h; the last {base['n']} checked at the same age had "
                   f"{round(base['views'])} (median).")
    typical = reading.get("typical")
    if views is not None and typical is not None:
        if level == "unknown":
            ratio = views / max(typical, 1)
            level = "behind" if ratio < BEHIND else "ahead" if ratio > AHEAD else "usual"
        why.append(f"{views} views at {reading['hours']} h; Studio says the usual for us at this age is {typical}.")
    if rank and of:
        if level == "unknown":
            level = "behind" if rank > 0.7 * of else "ahead" if rank <= 0.3 * of else "usual"
        why.append(f"Studio ranks it {rank} of {of} against our latest videos at the same age.")
    if level == "unknown":
        why.append("Nothing to compare it with yet: no usual figure or rank from Studio, and fewer than three earlier "
                   "checks at this age.")
    mine = next((h for h in history(slug, fmt) if h["id"] == rec["id"]), None)
    prior = [h["firstMorning"] for h in history(slug, fmt) if h["at"] < at and h["firstMorning"] is not None][-LOOK_BACK:]
    before = _median(prior)
    if mine and mine["firstMorning"] is not None and before:
        why.append(f"By the next morning it had {mine['firstMorning']} views; the {len(prior)} before it had "
                   f"{round(before)} (median).")
    faults = rec.get("faults") or []
    stage, now, carry = "", [], []
    if faults:
        why = [f"Fault: {f}" for f in faults] + why
        now.append("Put the fault right today. The Chief queues the Studio fix; visibility and schedule changes are Ben's.")
    if level == "behind":
        stage = _stage(fmt, reading, base, usual)
        do, later = ADVICE[(fmt, stage)] if stage else (NO_FIGURES, [])
        now += do
        carry += later
    elif level == "ahead":
        now += [] if faults else ["Nothing to fix."]
        carry.append("A strong start is a lesson too: note what is different about this one.")
    elif level == "usual":
        now += [] if faults else ["Nothing to fix."]
    else:
        now.append("Read it again from tomorrow morning's snapshot.")
    if faults:
        level = "fault"
    video = {"id": rec["id"], "title": rec.get("title") or "", "format": fmt, "at": at, "seconds": rec.get("seconds")}
    return {"level": level, "stage": stage, "why": why, "now": now, "carry": carry, "hours": reading["hours"],
            "differences": differences(slug, video), "reading": reading, "usual": usual}


def _figures_line(fmt: str, r: dict) -> str:
    def show(key, label, unit=""):
        return f"{label} {r[key]}{unit}" if r.get(key) is not None else f"{label} no figure yet"
    parts = [show("views", "views")]
    if r.get("rank") and r.get("of"):
        parts.append(f"Studio rank {r['rank']} of {r['of']}")
    if fmt == "short":
        if r.get("shown") is None and shown_in_feed(r) is not None:
            parts.append(f"shown in feed about {shown_in_feed(r)} (from {r['feedViews']} feed views)")
        else:
            parts.append(show("shown", "shown in feed"))
        parts.append(show("stayed", "stayed to watch", "%"))
    else:
        parts += [show("impressions", "impressions"), show("ctr", "click rate", "%")]
    parts.append(show("avgPct", "average viewed", "%"))
    return " · ".join(parts)


def judge_text(slug: str, rec: dict) -> str:
    v = verdict(slug, rec)
    lines = [f"\"{rec.get('title') or rec['id']}\" ({rec['id']}) · {channels.name(slug)} · {FORMAT_NAME[rec['format']]} "
             f"· went live {_when(studio.parse(rec['wentLive']))} London"]
    if v.get("reading"):
        lines.append(f"At {v['hours']} h: {_figures_line(rec['format'], v['reading'])}")
    usual = v.get("usual") or {}
    if usual:
        names = {"stayed": "stayed to watch", "avgPct": "average viewed", "ctr": "click rate"}
        lines.append("Usual for this channel: " + ", ".join(f"{names[k]} {round(val, 1)}%" for k, val in usual.items()))
    lines += ["", "Verdict: " + v["level"].upper() + (f", {v['stage']}" if v["stage"] else "")]
    lines += [f"  - {w}" for w in v["why"]]
    if v["differences"]:
        lines += ["", "What is different about this one"] + [f"  - {d['text']}" for d in v["differences"]]
    if v["now"]:
        lines += ["", "Do now"] + [f"  - {n}" for n in v["now"]]
    if v["carry"]:
        lines += ["", "Carry forward"] + [f"  - {c}" for c in v["carry"]]
    for note in rec.get("notes") or []:
        lines += ["", f"Done ({note.get('at', '')}, {note.get('by', '')}): {note.get('text', '')}"]
    return "\n".join(lines)


def report_text() -> str:
    """Every checked video, newest last, then what the weak starts have in common."""
    lines = []
    for slug in channels.slugs():
        recs = records(slug)
        if not recs:
            continue
        lines += [f"{channels.name(slug)}: {len(recs)} checked", ""]
        weak, rest = collections.Counter(), collections.Counter()
        n_weak = n_rest = 0
        for rec in recs:
            v = verdict(slug, rec)
            r = v.get("reading") or {}
            mine = next((h for h in history(slug, rec["format"]) if h["id"] == rec["id"]), None)
            morning = mine["firstMorning"] if mine and mine["firstMorning"] is not None else "-"
            lines.append(f"  {(rec.get('wentLive') or '')[:10]}  {FORMAT_NAME[rec['format']]:<5} "
                         f"{(rec.get('title') or rec['id'])[:52]:<52}  {v['hours']} h: {r.get('views', '-')} views"
                         f"  next morning: {morning}  {v['level']}{', ' + v['stage'] if v['stage'] else ''}")
            keys = {d["key"] for d in v["differences"]} | ({"stage: " + v["stage"]} if v["stage"] else set())
            if v["level"] in ("behind", "fault"):
                n_weak += 1
                weak.update(keys)
            else:
                n_rest += 1
                rest.update(keys)
        shared = [(k, n) for k, n in weak.most_common() if n >= MIN_TO_COMPARE]
        lines.append("")
        if shared:
            lines.append(f"  What the {n_weak} weak starts share (three or more; a rule or test for LEARNINGS.md is the Chief's call):")
            lines += [f"    - {k}: {n} of {n_weak} weak starts, {rest[k]} of {n_rest} others" for k, n in shared]
        else:
            lines.append(f"  Nothing is shared by three weak starts yet ({n_weak} weak so far).")
        lines.append("")
    return "\n".join(lines).rstrip() or "No video has been checked yet."


# ---- command line ------------------------------------------------------------------------------------------------

def _commit(change, message: str, git: bool) -> str | None:
    """Run `change()` (it returns the path it wrote); with `git`, do it on a fresh main and push."""
    if not git:
        change()
        return None
    return studio.git_transaction(lambda: (None, None, [change()]), message)[1]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("due", help="which videos are due a check now")
    rec = sub.add_parser("record", help="store one reading")
    rec.add_argument("id")
    rec.add_argument("--hours", type=int, required=True, help="the age the check is for (6, or 48 for a long)")
    rec.add_argument("--views", type=int, required=True)
    rec.add_argument("--typical", type=int, help="Studio's \"N more/less than usual\": the usual views at this age")
    rec.add_argument("--rank", type=int, help="Studio's Ranking by views: the N of \"N of 10\"")
    rec.add_argument("--of", type=int, default=None, help="the 10 of \"N of 10\"")
    rec.add_argument("--shown", type=int, help="Short: Shown in feed, when Studio has that card")
    rec.add_argument("--feed-views", dest="feedViews", type=int, help="Short: views that came from the Shorts feed")
    rec.add_argument("--stayed", type=float, help="Short: Viewed vs swiped away, the %% who stayed")
    rec.add_argument("--avg-pct", dest="avgPct", type=float, help="Average percentage viewed")
    rec.add_argument("--impressions", type=int, help="long: Impressions")
    rec.add_argument("--ctr", type=float, help="long: Impressions click-through rate, %%")
    rec.add_argument("--likes", type=int)
    rec.add_argument("--fault", action="append", default=[], help="one thing that is wrong with the video; repeatable")
    rec.add_argument("--by", default="", help="who read the numbers")
    rec.add_argument("--read-at", default="", help="when they were read (ISO, UTC); now if left out")
    rec.add_argument("--git", action="store_true")
    jud = sub.add_parser("judge", help="the verdict and what to do")
    jud.add_argument("id")
    note = sub.add_parser("note", help="write down what was done about it")
    note.add_argument("id")
    note.add_argument("text")
    note.add_argument("--by", default="chief")
    note.add_argument("--git", action="store_true")
    sub.add_parser("report", help="every checked video, and what the weak starts share")
    args = ap.parse_args(argv)
    now = dt.datetime.now(dt.timezone.utc)

    if args.cmd == "due":
        import jobs
        items = due(now, jobs.load())
        for item in items:
            print(f"{item['channel']}  {item['id']}  {item['hours']} h  went live {_when(item['at'])}  {item['title'][:60]}")
        if not items:
            print("nothing is due a first-day check")
        return 0
    if args.cmd == "report":
        print(report_text())
        return 0

    found = lookup(args.id, now)
    slug = found[0] if found else next((s for s in channels.slugs() if load_record(s, args.id)), None)
    if not slug:
        print(f"{args.id}: not in any channel's snapshot or uploads register", file=sys.stderr)
        return 1
    if args.cmd == "judge":
        rec_ = load_record(slug, args.id)
        if not rec_:
            print(f"{args.id}: no reading recorded yet; use `record` first", file=sys.stderr)
            return 1
        print(judge_text(slug, rec_))
        return 0
    if args.cmd == "record":
        if not found:
            print(f"{args.id}: not in any channel's snapshot or uploads register", file=sys.stderr)
            return 1
        if (args.rank is None) != (args.of is None):
            ap.error("--rank and --of go together (\"N of 10\")")
        reading = {"hours": args.hours, "readAt": args.read_at or studio.iso(now), "by": args.by or None}
        reading.update({k: getattr(args, k) for k in FIGURES})

        def change():
            return save_record(slug, with_reading(load_record(slug, args.id), slug, found[1], reading, args.fault))

        err = _commit(change, f"first-day check: {args.id} at {args.hours} h ({args.views} views)", args.git)
    else:
        def change():
            rec_ = load_record(slug, args.id)
            if not rec_:
                raise SystemExit(f"{args.id}: no record to add a note to")
            rec_.setdefault("notes", []).append({"at": studio.iso(now), "by": args.by, "text": args.text.strip()})
            return save_record(slug, rec_)

        err = _commit(change, f"first-day check: what was done about {args.id}", args.git)
    if err:
        print(f"not saved: {err}", file=sys.stderr)
        return 1
    print(f"saved {record_path(slug, args.id).relative_to(channels.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
