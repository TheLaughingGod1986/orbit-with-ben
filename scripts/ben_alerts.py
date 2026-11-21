#!/usr/bin/env python3
"""Direct urgent alerts to Ben when a same-day video is pulled or his watch is needed within 12 hours (J3292).

Triggers (on any registered channel):
  (a) A video airing within 24 hours is pulled, unscheduled or replaced.
  (b) A job needs Ben's watch (`awaits_ben` UAT) and its deadline is within 12 hours.

Rate limit & lifecycle:
  - One alert per event when first triggered.
  - Repeat ONCE at half the remaining time (`firstSentAt + (deadlineAt - firstSentAt) / 2`) if still not done.
  - Never more than two sends per event; stops immediately when the job/watch is done, ticked, refilled or passed.

Delivery (£0):
  - Phone push (recommended 1-step £0 route, proposed to Ben via Claude in chat before any setup):
    ntfy subscription (`~/_desk/state/alerts/config.json` -> `{"ntfyUrl": "https://ntfy.sh/<private-topic>"}`
    or env `BEN_ALERT_NTFY_URL`), or an optional local command (`webhookCmd` / `BEN_ALERT_CMD`).
    Secrets and topics are NEVER stored in git.
  - Until phone delivery is configured (and always alongside it):
    active alerts are published into `board.json` (`board["alerts"]`) as a red banner at the top of every page
    on the board site, and posted to the studio thread (`chief_relay.notify`).

CLI:
  python3 scripts/ben_alerts.py check [--dry-run]
  python3 scripts/ben_alerts.py status
  python3 scripts/ben_alerts.py record-pull --channel CH --video-id VID --title "..." --slot ISO [--reason "..."]
  python3 scripts/ben_alerts.py resolve <event_id>
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import json
import os
import pathlib
import re
import shlex
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import board_site  # noqa: E402
import channels  # noqa: E402
import video_tracker  # noqa: E402

HOME = pathlib.Path.home()
LONDON = ZoneInfo("Europe/London")
PULL_WINDOW_S = 24 * 3600
WATCH_WINDOW_S = 12 * 3600
MAX_SENDS = 2
MIN_REPEAT_GAP_S = 60
PHONE_PROPOSAL = (
    "For £0 instant phone alerts with one setup step, install the free ntfy app and subscribe to one private "
    "topic stored only on the Mini (never in git) — OK to set that up?"
)
UPLOADS_REL = pathlib.Path("00_Brand", "Channel-Setup", "social", "UPLOADS.json")
SOCIAL_DIR_REL = pathlib.Path("00_Brand", "Channel-Setup", "social")
JOB_ID_RE = re.compile(r"\bJ\d{3,5}\b")


def state_path(override: pathlib.Path | None = None) -> pathlib.Path:
    if override is not None:
        return pathlib.Path(override)
    return pathlib.Path(os.environ.get("BEN_ALERTS_STATE", str(HOME / "_desk" / "state" / "alerts" / "state.json")))


def config_path(override: pathlib.Path | None = None) -> pathlib.Path:
    if override is not None:
        return pathlib.Path(override)
    return pathlib.Path(os.environ.get("BEN_ALERTS_CONFIG", str(HOME / "_desk" / "state" / "alerts" / "config.json")))


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def iso(t: dt.datetime) -> str:
    return t.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_iso(raw) -> dt.datetime | None:
    if not raw:
        return None
    try:
        t = dt.datetime.fromisoformat(str(raw).strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if t.tzinfo is None:
        t = t.replace(tzinfo=dt.timezone.utc)
    return t.astimezone(dt.timezone.utc)


def _read_json(path: pathlib.Path, default):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return default


def _write_json_atomic(path: pathlib.Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")
    tmp.replace(path)


@contextlib.contextmanager
def _state_lock(path: pathlib.Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_file = path.with_suffix(".lock")
    with open(lock_file, "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def _empty_state() -> dict:
    return {"version": 1, "seededAt": "", "known_scheduled": {}, "pulls": {}, "events": {}}


def load_state(path: pathlib.Path | None = None) -> dict:
    p = state_path(path)
    raw = _read_json(p, None)
    if not isinstance(raw, dict):
        return _empty_state()
    return {
        "version": 1,
        "seededAt": str(raw.get("seededAt") or ""),
        "known_scheduled": dict(raw.get("known_scheduled") or {}),
        "pulls": dict(raw.get("pulls") or {}),
        "events": dict(raw.get("events") or {}),
    }


def load_config(path: pathlib.Path | None = None) -> dict:
    cfg = _read_json(config_path(path), {})
    if not isinstance(cfg, dict):
        cfg = {}
    out = dict(cfg)
    if os.environ.get("BEN_ALERT_NTFY_URL"):
        out["ntfyUrl"] = os.environ["BEN_ALERT_NTFY_URL"].strip()
    if os.environ.get("BEN_ALERT_CMD"):
        out["webhookCmd"] = os.environ["BEN_ALERT_CMD"].strip()
    return out


def format_london_time(target: dt.datetime, reference: dt.datetime) -> str:
    tl = target.astimezone(LONDON)
    rl = reference.astimezone(LONDON)
    hhmm = tl.strftime("%H:%M")
    if tl.date() == rl.date():
        return hhmm
    if tl.date() == rl.date() + dt.timedelta(days=1):
        return f"tomorrow {hhmm}"
    return f"{tl.strftime('%a')} {tl.day} {tl.strftime('%b')} {hhmm}"


def format_slot_phrase(slot: dt.datetime, reference: dt.datetime) -> str:
    sl = slot.astimezone(LONDON)
    rl = reference.astimezone(LONDON)
    hhmm = sl.strftime("%H:%M")
    if sl.date() == rl.date():
        return f"today's {hhmm} slot"
    if sl.date() == rl.date() + dt.timedelta(days=1):
        return f"tomorrow's {hhmm} slot"
    return f"{sl.strftime('%a')} {sl.day} {sl.strftime('%b')} {hhmm} slot"


def short_reason(raw: str) -> str:
    s = str(raw or "").strip()
    if not s:
        return ""
    low = s.lower()
    if "music_gate" in low or ("music" in low and ("fail" in low or "reused" in low)):
        return "music failed a check"
    if "gate_shorts_open" in low or "full_bleed" in low or "blurred band" in low:
        return "video failed a check"
    if "silent" in low or "loudness" in low:
        return "audio failed a check"
    first = re.split(r"[.;\n]", s, maxsplit=1)[0].strip()
    first = JOB_ID_RE.sub("", first)
    first = re.sub(r"\bunder\b\s*:?", "", first, flags=re.I)
    first = re.sub(r"\s{2,}", " ", first).strip(" :-")
    if len(first) > 72:
        first = first[:71].rstrip() + "…"
    return first


def _title_from_file(file_path: str) -> str:
    """Derive a readable video name from an upload filename like hos_005_s07_heart_pulse_v05.mp4."""
    raw = pathlib.Path(str(file_path or "").strip()).stem
    if not raw:
        return ""
    s = re.sub(r"^(?:hos|owb|ww2)[_-]+", "", raw, flags=re.I)
    s = re.sub(r"^(?:\d{3}|sa|j\d+|sleep\d+)[_-]+", "", s, flags=re.I)
    s = re.sub(r"^(?:s\d+|short[_-]?[a-z0-9]+|backcat)[_-]+", "", s, flags=re.I)
    parts = [p for p in re.split(r"[_-]+", s) if p]
    if not parts:
        return ""
    out: list[str] = []
    for p in parts:
        if re.fullmatch(r"v\d+[a-z]?", p, flags=re.I):
            out.append(p.lower())
        else:
            out.append(p.capitalize())
    return " ".join(out)


def _resolve_title(explicit: str, *, meta: dict | None = None, videos: list[dict] | None = None,
                   channel: str = "", vtype: str = "short", video_id: str = "",
                   slot_dt: dt.datetime | None = None) -> str:
    """Find a real video name (never just the channel) from explicit title, tracker videos, social copy or filename."""
    t = str(explicit or "").strip()
    if t:
        return t
    meta = meta if isinstance(meta, dict) else {}
    mt = str(meta.get("title") or "").strip()
    if mt:
        return mt
    ch = str(channel or "").upper()
    vid = str(video_id or "").strip()
    vt = "short" if str(vtype or "").lower() == "short" else "long"
    if videos:
        for v in videos:
            if not isinstance(v, dict):
                continue
            yt = v.get("youtube") or {}
            if vid and str(yt.get("videoId") or "").strip() == vid:
                if str(v.get("title") or "").strip():
                    return str(v["title"]).strip()
        if slot_dt and ch:
            for v in videos:
                if not isinstance(v, dict):
                    continue
                if str(v.get("channel") or "").upper() != ch:
                    continue
                v_kind = "short" if str(v.get("type") or "").lower() == "short" else "long"
                if v_kind != vt:
                    continue
                v_pub = parse_iso((v.get("youtube") or {}).get("publishAt"))
                if v_pub and abs((v_pub - slot_dt).total_seconds()) <= 300 and str(v.get("title") or "").strip():
                    return str(v["title"]).strip()
    social = meta.get("social") if isinstance(meta.get("social"), dict) else {}
    q = str(social.get("question") or "").strip()
    if q:
        return q
    from_file = _title_from_file(str(meta.get("file") or ""))
    if from_file:
        return from_file
    return ""


def video_label(title: str, vtype: str, channel: str = "", number: str = "", video_id: str = "") -> str:
    t = str(title or "").strip()
    fmt = "Short" if str(vtype or "").lower() == "short" else "Long"
    if not t:
        bits = [b for b in (channel, number, fmt) if b]
        base = " ".join(bits) or f"Video {fmt}"
        vid = str(video_id or "").strip()
        return f"{base} ({vid})" if vid else base
    if len(t) > 58:
        t = t[:57].rstrip() + "…"
    if fmt.lower() not in t.lower():
        return f"{t} {fmt}"
    return t


def _site_base(site_url: str | None = None) -> tuple[str, str]:
    full = (site_url or board_site.site_url()).rstrip("/")
    display = re.sub(r"^https?://", "", full)
    return full, display


def format_message(event: dict, at: dt.datetime, *, is_repeat: bool = False, site_url: str | None = None) -> tuple[str, str]:
    """Return (full_text_with_link, banner_text_without_trailing_url)."""
    full_base, display_base = _site_base(site_url)
    href = str(event.get("href") or "#review")
    if not href.startswith("#"):
        href = "#" + href.lstrip("/")
    display_link = f"{display_base}/{href}"
    name = video_label(
        event.get("title", ""), event.get("type", ""), event.get("channel", ""),
        event.get("number", ""), event.get("videoId", ""),
    )
    prefix = "Reminder: " if is_repeat else ""
    deadline_dt = parse_iso(event.get("deadlineAt"))
    slot_dt = parse_iso(event.get("slotAt"))
    by_text = format_london_time(deadline_dt, at) if deadline_dt else ""
    slot_text = format_slot_phrase(slot_dt, at) if slot_dt else ""
    slot_when = format_london_time(slot_dt, at) if slot_dt else ""
    still = "still " if is_repeat else ""

    if event.get("kind") == "pulled":
        verb = str(event.get("change") or "pulled")
        why = short_reason(event.get("reason", ""))
        why_part = f" ({why})" if why else ""
        if event.get("hasWatch") and by_text:
            head = f"{name} {verb}{why_part}."
            keep = f" to keep {slot_text}" if slot_text else ""
            tail = f"The fixed version {still}needs your watch by {by_text}{keep}"
        elif event.get("action"):
            head = f"{name} {verb}{why_part}."
            act = str(event["action"]).strip().rstrip(".")
            tail = f"{act}" + (f" by {by_text}" if by_text and by_text not in act else "")
        elif event.get("nothingNeeded") or verb == "replaced":
            rep = str(event.get("replacementName") or event.get("supersededBy") or "").strip()
            det_dt = parse_iso(event.get("detectedAt"))
            on_day = ""
            if det_dt and det_dt.astimezone(LONDON).date() < at.astimezone(LONDON).date():
                on_day = f" on {det_dt.astimezone(LONDON).strftime('%A')}"
            if rep:
                head = f"{name} was replaced{on_day}{why_part};"
                tail = f"{rep} airs {slot_when}. Nothing needed." if slot_when else f"{rep} takes the slot. Nothing needed."
            else:
                head = f"{name} was replaced{on_day}{why_part}."
                tail = f"Replacement airs {slot_when}. Nothing needed." if slot_when else "Nothing needed."
        elif verb == "unscheduled":
            if slot_text:
                head = f"{name} was taken off {slot_text}{why_part}."
                tail = "Open the schedule to pick a replacement or leave the slot open"
            else:
                head = f"{name} was unscheduled{why_part}."
                tail = "Open the schedule to pick a replacement or leave the slot open"
        else:
            head = f"{name} {verb}{why_part}."
            if slot_text:
                tail = f"Open the schedule to pick a replacement for {slot_text} or leave it open"
            else:
                tail = "Open the schedule to check the slot or pick a replacement"
        body = f"{prefix}{head} {tail}"
    else:
        keep = f" to keep {slot_text}" if slot_text else ""
        ver = f" ({event['version']})" if event.get("version") and event["version"] not in name else ""
        if by_text:
            body = f"{prefix}{name}{ver} {still}needs your watch by {by_text}{keep}"
        else:
            body = f"{prefix}{name}{ver} {still}needs your watch{keep}"
    body = re.sub(r"\s+", " ", body).strip()
    return f"{body.rstrip('.')}: {display_link}", body


def _ask_answered(entry: dict, checks: dict) -> bool:
    cid = video_tracker.ask_check_id(entry)
    tick = (checks or {}).get(cid)
    if not isinstance(tick, dict):
        return False
    ver = entry.get("version") or ""
    tver = str(tick.get("version") or "")
    same = not ver or not tver or tver == ver
    return bool(same and tick.get("verdict") in ("ok", "change"))


def _matching_card_key(entry: dict, videos: list[dict]) -> str:
    card = entry.get("card") or ""
    keys = {str(v.get("key") or "") for v in (videos or []) if isinstance(v, dict)}
    if card and card in keys:
        return card
    ask_id = entry.get("id") or ""
    for v in videos or []:
        if isinstance(v, dict) and isinstance(v.get("ask"), dict) and v["ask"].get("id") == ask_id:
            if v.get("key"):
                return str(v["key"])
    return ""


def _slot_key(channel: str, vtype: str, slot_dt: dt.datetime) -> tuple[str, str, str]:
    return (str(channel or "").upper(), "short" if str(vtype or "").lower() == "short" else "long",
            slot_dt.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M"))


def _collect_current_schedule(videos: list[dict], uploads: dict[str, dict]) -> tuple[dict, dict, dict]:
    """Return (scheduled_by_id, public_ids, slots_map)."""
    scheduled: dict[tuple[str, str], dict] = {}
    public_ids: set[tuple[str, str]] = set()
    slots: dict[tuple[str, str, str], set[str]] = {}

    for v in videos or []:
        if not isinstance(v, dict):
            continue
        yt = v.get("youtube") or {}
        vid = str(yt.get("videoId") or "").strip()
        if not vid:
            continue
        ch = str(v.get("channel") or "").upper()
        vtype = "short" if str(v.get("type") or "").lower() == "short" else "long"
        state = str(yt.get("state") or "").lower()
        privacy = str(yt.get("privacy") or "").lower()
        pub_dt = parse_iso(yt.get("publishAt"))
        if state == "live" or privacy == "public":
            public_ids.add((ch, vid))
            if pub_dt:
                slots.setdefault(_slot_key(ch, vtype, pub_dt), set()).add(vid)
        elif state == "scheduled" and pub_dt:
            rec = {
                "channel": ch,
                "videoId": vid,
                "title": str(v.get("title") or ""),
                "type": vtype,
                "publishAt": iso(pub_dt),
                "film": str(v.get("number") or ""),
                "key": str(v.get("key") or ""),
            }
            scheduled[(ch, vid)] = rec
            slots.setdefault(_slot_key(ch, vtype, pub_dt), set()).add(vid)

    for ch_label, vid_map in (uploads or {}).items():
        ch = str(ch_label or "").upper()
        if not isinstance(vid_map, dict):
            continue
        for vid, meta in vid_map.items():
            if not isinstance(meta, dict):
                continue
            vid = str(vid).strip()
            vtype = "short" if str(meta.get("kind") or "").lower() == "short" else "long"
            privacy = str(meta.get("privacyStatus") or "").lower()
            pub_dt = parse_iso(meta.get("publishAt"))
            if privacy == "public":
                public_ids.add((ch, vid))
                scheduled.pop((ch, vid), None)
                if pub_dt:
                    slots.setdefault(_slot_key(ch, vtype, pub_dt), set()).add(vid)
                continue
            if meta.get("supersededBy") or meta.get("unscheduledAt") or meta.get("pulledAt") or ("publishAt" in meta and meta.get("publishAt") is None):
                scheduled.pop((ch, vid), None)
                continue
            if pub_dt:
                resolved_title = _resolve_title(
                    "", meta=meta, videos=videos, channel=ch, vtype=vtype, video_id=vid, slot_dt=pub_dt,
                )
                rec = scheduled.get((ch, vid)) or {
                    "channel": ch,
                    "videoId": vid,
                    "title": resolved_title,
                    "type": vtype,
                    "publishAt": iso(pub_dt),
                    "film": "",
                    "key": "",
                }
                rec["publishAt"] = iso(pub_dt)
                if meta.get("title"):
                    rec["title"] = str(meta["title"])
                elif resolved_title and not rec.get("title"):
                    rec["title"] = resolved_title
                scheduled[(ch, vid)] = rec
                slots.setdefault(_slot_key(ch, vtype, pub_dt), set()).add(vid)

    return scheduled, public_ids, slots


def load_channel_uploads(channel_roots: dict[str, pathlib.Path], studio_root: pathlib.Path | None = None) -> dict[str, dict]:
    """Load UPLOADS.json for every registered channel without hard-coding channel names."""
    out: dict[str, dict] = {}
    for slug, root in (channel_roots or {}).items():
        label = channels.label(slug)
        merged: dict = {}
        candidates = [pathlib.Path(root) / UPLOADS_REL]
        if studio_root is not None:
            candidates.append(pathlib.Path(studio_root) / SOCIAL_DIR_REL / slug / "UPLOADS.json")
        for p in candidates:
            raw = _read_json(p, None)
            if isinstance(raw, dict) and isinstance(raw.get("videos"), dict):
                for vid, meta in raw["videos"].items():
                    if isinstance(meta, dict):
                        merged[vid] = meta
        if merged:
            out[label] = merged
    return out


def _pull_id(channel: str, video_id: str, slot_dt: dt.datetime) -> str:
    return f"pull:{str(channel or '').upper()}:{video_id}:{slot_dt.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M')}"


def _detect_pulls(at: dt.datetime, state: dict, scheduled: dict, public_ids: set, slots: dict,
                  uploads: dict[str, dict], videos: list[dict] | None = None) -> None:
    """Detect newly pulled, unscheduled or replaced videos airing within 24 h and update state['pulls'] & known_scheduled."""
    known = state.setdefault("known_scheduled", {})
    pulls = state.setdefault("pulls", {})
    events = state.setdefault("events", {})
    is_first_run = not state.get("seededAt") and not known and not pulls and not events

    if is_first_run:
        # First run seeds what is scheduled without alerting, and marks pre-existing pull entries as seen
        # so old pulls are not announced as new on this run or the next one.
        state["seededAt"] = iso(at)
        for ch_label, vid_map in (uploads or {}).items():
            ch = str(ch_label or "").upper()
            if not isinstance(vid_map, dict):
                continue
            for vid, meta in vid_map.items():
                if not isinstance(meta, dict):
                    continue
                prev_pub = parse_iso(meta.get("previousPublishAt") or meta.get("wasScheduledFor"))
                unsched_at = parse_iso(meta.get("unscheduledAt") or meta.get("pulledAt"))
                if not prev_pub or not unsched_at:
                    continue
                vtype = "short" if str(meta.get("kind") or "").lower() == "short" else "long"
                pid = _pull_id(ch, str(vid), prev_pub)
                if pid not in pulls:
                    slot_holders = slots.get(_slot_key(ch, vtype, prev_pub), set()) - {str(vid)}
                    superseded_by = str(meta.get("supersededBy") or "")
                    pulls[pid] = {
                        "id": pid,
                        "channel": ch,
                        "videoId": str(vid),
                        "title": _resolve_title(str(meta.get("title") or ""), meta=meta, videos=videos,
                                                channel=ch, vtype=vtype, video_id=str(vid), slot_dt=prev_pub),
                        "type": vtype,
                        "film": "",
                        "slotAt": iso(prev_pub),
                        "change": "replaced" if (superseded_by or slot_holders) else "pulled",
                        "reason": str(meta.get("pullReason") or meta.get("containment") or ""),
                        "detectedAt": iso(unsched_at),
                        "supersededBy": superseded_by or (sorted(slot_holders)[0] if slot_holders else ""),
                        "job": "",
                        "resolvedAt": iso(at),
                        "resolution": "replaced in the same slot" if slot_holders else "seeded on initial run",
                    }
        for (ch, vid), rec in scheduled.items():
            pub_dt = parse_iso(rec.get("publishAt"))
            if pub_dt and pub_dt > at:
                known[f"{ch}:{vid}"] = rec
        return

    if not state.get("seededAt"):
        state["seededAt"] = iso(at)
    seeded_dt = parse_iso(state.get("seededAt"))

    # 1. Compare previously known scheduled videos against current state.
    for key_str, prev in list(known.items()):
        if not isinstance(prev, dict):
            known.pop(key_str, None)
            continue
        prev_pub = parse_iso(prev.get("publishAt"))
        if not prev_pub or prev_pub <= at:
            known.pop(key_str, None)
            continue
        ch = str(prev.get("channel") or "").upper()
        vid = str(prev.get("videoId") or "")
        vtype = "short" if str(prev.get("type") or "").lower() == "short" else "long"
        if (ch, vid) in public_ids:
            known.pop(key_str, None)
            continue
        cur = scheduled.get((ch, vid))
        cur_pub = parse_iso(cur.get("publishAt")) if cur else None
        still_same_slot = bool(cur_pub and abs((cur_pub - prev_pub).total_seconds()) <= 300)
        if still_same_slot:
            continue
        rem_s = (prev_pub - at).total_seconds()
        if 0 < rem_s <= PULL_WINDOW_S:
            meta = ((uploads or {}).get(ch) or {}).get(vid) or {}
            slot_holders = slots.get(_slot_key(ch, vtype, prev_pub), set()) - {vid}
            superseded_by = str(meta.get("supersededBy") or "")
            if superseded_by or slot_holders:
                change = "replaced"
            elif meta.get("unscheduledAt") or meta.get("pulledAt") or meta.get("containment") or meta.get("pullReason"):
                change = "pulled"
            else:
                change = "unscheduled"
            pid = _pull_id(ch, vid, prev_pub)
            if pid not in pulls:
                rec = {
                    "id": pid,
                    "channel": ch,
                    "videoId": vid,
                    "title": _resolve_title(str(meta.get("title") or prev.get("title") or ""), meta=meta,
                                            videos=videos, channel=ch, vtype=vtype, video_id=vid, slot_dt=prev_pub),
                    "type": vtype,
                    "film": str(prev.get("film") or ""),
                    "slotAt": iso(prev_pub),
                    "change": change,
                    "reason": str(meta.get("pullReason") or meta.get("containment") or ""),
                    "detectedAt": iso(at),
                    "supersededBy": superseded_by or (sorted(slot_holders)[0] if slot_holders else ""),
                    "job": "",
                }
                # A pulled video whose slot already holds another scheduled video of the same channel and kind
                # is "replaced" and raises no banner.
                if slot_holders:
                    rec["resolvedAt"] = iso(at)
                    rec["resolution"] = "replaced in the same slot"
                pulls[pid] = rec
        known.pop(key_str, None)

    # 2. Explicit pull metadata in UPLOADS.json for new pulls recorded after seeding.
    for ch_label, vid_map in (uploads or {}).items():
        ch = str(ch_label or "").upper()
        if not isinstance(vid_map, dict):
            continue
        for vid, meta in vid_map.items():
            if not isinstance(meta, dict):
                continue
            if str(meta.get("privacyStatus") or "").lower() == "public":
                continue
            prev_pub = parse_iso(meta.get("previousPublishAt") or meta.get("wasScheduledFor"))
            unsched_at = parse_iso(meta.get("unscheduledAt") or meta.get("pulledAt"))
            if not prev_pub or not unsched_at or at >= prev_pub:
                continue
            if not (0 < (prev_pub - unsched_at).total_seconds() <= PULL_WINDOW_S):
                continue
            vtype = "short" if str(meta.get("kind") or "").lower() == "short" else "long"
            pid = _pull_id(ch, str(vid), prev_pub)
            if pid not in pulls:
                slot_holders = slots.get(_slot_key(ch, vtype, prev_pub), set()) - {str(vid)}
                superseded_by = str(meta.get("supersededBy") or "")
                rec = {
                    "id": pid,
                    "channel": ch,
                    "videoId": str(vid),
                    "title": _resolve_title(str(meta.get("title") or ""), meta=meta, videos=videos,
                                            channel=ch, vtype=vtype, video_id=str(vid), slot_dt=prev_pub),
                    "type": vtype,
                    "film": "",
                    "slotAt": iso(prev_pub),
                    "change": "replaced" if (superseded_by or slot_holders) else "pulled",
                    "reason": str(meta.get("pullReason") or meta.get("containment") or ""),
                    "detectedAt": iso(unsched_at),
                    "supersededBy": superseded_by or (sorted(slot_holders)[0] if slot_holders else ""),
                    "job": "",
                }
                if slot_holders:
                    rec["resolvedAt"] = iso(at)
                    rec["resolution"] = "replaced in the same slot"
                elif seeded_dt and unsched_at < seeded_dt:
                    rec["resolvedAt"] = iso(at)
                    rec["resolution"] = "pre-existing pull before seed"
                pulls[pid] = rec

    # 3. Record all currently scheduled future videos for future transition detection.
    for (ch, vid), rec in scheduled.items():
        pub_dt = parse_iso(rec.get("publishAt"))
        if pub_dt and pub_dt > at:
            known[f"{ch}:{vid}"] = rec


def _match_watch_for_pull(pull: dict, watches: list[dict]) -> dict | None:
    p_job = str(pull.get("job") or "")
    p_ch = str(pull.get("channel") or "").upper()
    p_film = str(pull.get("film") or "")
    p_slot = parse_iso(pull.get("slotAt"))
    for w in watches:
        if p_job and w.get("job") == p_job:
            return w
    for w in watches:
        if str(w.get("channel") or "").upper() != p_ch:
            continue
        w_airs = parse_iso(w.get("slotAt"))
        if p_slot and w_airs and abs((w_airs - p_slot).total_seconds()) <= 3600:
            if not p_film or not w.get("film") or p_film == w.get("film") or w.get("film", "").startswith(p_film):
                return w
    return None


def _job_is_finished(job: dict | None, checks: dict) -> bool:
    if not isinstance(job, dict):
        return False
    status = str(job.get("status") or "").lower()
    if status in ("cancelled", "dropped"):
        return True
    if status != "done":
        return False
    raw = job.get("awaits_ben")
    if not raw:
        return True
    entries = video_tracker.ask_entries([job])
    return all(_ask_answered(e, checks) for e in entries)


def deliver_alert(message: str, *, title: str = "Studio urgent alert", url: str = "",
                  config: dict | None = None, notify_fn=None, post_fn=None) -> dict:
    """Send one alert via configured £0 phone route (ntfy or command) plus studio thread. Never logs secrets."""
    cfg = config if config is not None else load_config()
    phone_ok = False
    phone_route = "unconfigured"

    ntfy_url = str(cfg.get("ntfyUrl") or "").strip()
    webhook_cmd = str(cfg.get("webhookCmd") or "").strip()

    if ntfy_url:
        phone_route = "ntfy"
        headers = {
            "Title": title.encode("ascii", "replace").decode("ascii")[:120],
            "Priority": "high",
            "Tags": "rotating_light",
            "Content-Type": "text/plain; charset=utf-8",
        }
        if url:
            headers["Click"] = url
        try:
            if post_fn is not None:
                phone_ok = bool(post_fn(ntfy_url, message, headers))
            else:
                req = urllib.request.Request(ntfy_url, data=message.encode("utf-8"), headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=15) as resp:
                    phone_ok = 200 <= getattr(resp, "status", 200) < 300
        except (OSError, urllib.error.URLError, ValueError):
            phone_ok = False
    elif webhook_cmd:
        phone_route = "custom"
        try:
            r = subprocess.run(shlex.split(webhook_cmd) + [message], capture_output=True, text=True, timeout=30)
            phone_ok = r.returncode == 0
        except (OSError, subprocess.SubprocessError):
            phone_ok = False

    thread_ok = False
    thread_text = f"[Alert] {message}"
    try:
        if notify_fn is not None:
            thread_ok = bool(notify_fn(thread_text))
        else:
            import chief_relay as relay
            thread_ok = bool(relay.notify(thread_text))
    except Exception:  # noqa: BLE001
        thread_ok = False

    return {"phone": phone_ok, "phoneRoute": phone_route, "thread": thread_ok}


def evaluate(*, at: dt.datetime | None = None, jobs: list[dict] | None = None, checks: dict | None = None,
             videos: list[dict] | None = None, uploads: dict[str, dict] | None = None,
             state_file: pathlib.Path | None = None, config_file: pathlib.Path | None = None,
             deliver: bool = True, notify_fn=None, post_fn=None, site_url: str | None = None) -> dict:
    """Evaluate all urgent alert triggers, fire/repeat due alerts, persist state, and return board payload."""
    at = at or now_utc()
    jobs = list(jobs or [])
    checks = dict(checks or {})
    videos = list(videos or [])
    uploads = dict(uploads or {})
    jobs_by_id = {str(j.get("id") or ""): j for j in jobs if isinstance(j, dict) and j.get("id")}
    p = state_path(state_file)
    cfg = load_config(config_file)
    full_base, _ = _site_base(site_url)

    sent_now: list[dict] = []
    with _state_lock(p):
        state = load_state(p)
        scheduled, public_ids, slots = _collect_current_schedule(videos, uploads)
        _detect_pulls(at, state, scheduled, public_ids, slots, uploads, videos=videos)

        # Collect active watch candidates (trigger b: awaits_ben UAT with deadline within 12 h).
        watch_candidates: list[dict] = []
        for entry in video_tracker.ask_entries(jobs):
            if _ask_answered(entry, checks):
                continue
            job = jobs_by_id.get(entry.get("job") or "")
            if job and str(job.get("status") or "").lower() in ("cancelled", "dropped"):
                continue
            due_dt = parse_iso(entry.get("due") or (job or {}).get("due"))
            if not due_dt or due_dt <= at:
                continue
            if (due_dt - at).total_seconds() > WATCH_WINDOW_S:
                continue
            airs_dt = parse_iso(entry.get("airs"))
            card_key = _matching_card_key(entry, videos)
            href = f"#uat={urllib.parse.quote(card_key, safe='')}" if card_key else "#review"
            wid = f"watch:{entry['id']}:{entry.get('version') or 'v0'}:{due_dt.strftime('%Y-%m-%dT%H:%M')}"
            watch_candidates.append({
                "id": wid,
                "kind": "watch",
                "channel": entry.get("channel") or "",
                "title": entry.get("title") or entry.get("what") or "",
                "type": entry.get("type") or "short",
                "number": entry.get("number") or "",
                "film": entry.get("number") or (job or {}).get("film") or "",
                "version": entry.get("version") or "",
                "job": entry.get("job") or "",
                "deadlineAt": iso(due_dt),
                "slotAt": iso(airs_dt) if airs_dt else "",
                "href": href,
                "url": f"{full_base}/{href}",
                "shortTitle": video_label(entry.get("title") or entry.get("what") or "", entry.get("type") or "short",
                                          entry.get("channel") or "", entry.get("number") or ""),
            })

        # Build active pull candidates (trigger a: video airing within 24 h pulled, unscheduled or replaced).
        active_events: list[dict] = []
        consumed_watch_ids: set[str] = set()
        for pid, pull in list((state.get("pulls") or {}).items()):
            if not isinstance(pull, dict) or pull.get("resolvedAt"):
                continue
            slot_dt = parse_iso(pull.get("slotAt"))
            if not slot_dt or at >= slot_dt:
                pull["resolvedAt"] = iso(at)
                continue
            # Check resolution by linked job or refilled slot.
            p_job_id = str(pull.get("job") or "")
            if p_job_id and p_job_id in jobs_by_id and _job_is_finished(jobs_by_id[p_job_id], checks):
                pull["resolvedAt"] = iso(at)
                continue
            ch = str(pull.get("channel") or "").upper()
            vid = str(pull.get("videoId") or "")
            vtype = "short" if str(pull.get("type") or "").lower() == "short" else "long"
            if (ch, vid) in public_ids:
                pull["resolvedAt"] = iso(at)
                continue
            other_in_slot = slots.get(_slot_key(ch, vtype, slot_dt), set()) - {vid}
            if other_in_slot:
                pull["change"] = "replaced"
                if not pull.get("supersededBy"):
                    pull["supersededBy"] = sorted(other_in_slot)[0]
                pull["resolvedAt"] = iso(at)
                pull["resolution"] = "replaced in the same slot"
                continue

            matched_watch = _match_watch_for_pull(pull, watch_candidates)
            if matched_watch:
                consumed_watch_ids.add(matched_watch["id"])
                deadline_dt = parse_iso(matched_watch["deadlineAt"]) or slot_dt
                href = matched_watch["href"]
                has_watch = True
            else:
                watch_due_dt = parse_iso(pull.get("watchDueAt"))
                deadline_dt = watch_due_dt if (watch_due_dt and at < watch_due_dt <= slot_dt) else slot_dt
                href = str(pull.get("href") or ("#review" if pull.get("watchDueAt") else "#schedule"))
                has_watch = bool(pull.get("watchDueAt"))

            pull_meta = ((uploads or {}).get(ch) or {}).get(vid) or {}
            resolved_title = _resolve_title(
                str(pull.get("title") or (matched_watch or {}).get("title") or ""),
                meta=pull_meta, videos=videos, channel=ch, vtype=vtype, video_id=vid, slot_dt=slot_dt,
            )
            active_events.append({
                "id": pid,
                "kind": "pulled",
                "change": str(pull.get("change") or "pulled"),
                "channel": ch,
                "videoId": vid,
                "title": resolved_title,
                "type": vtype,
                "number": str(pull.get("film") or (matched_watch or {}).get("number") or ""),
                "reason": str(pull.get("reason") or ""),
                "action": str(pull.get("action") or ""),
                "hasWatch": has_watch,
                "job": p_job_id or (matched_watch or {}).get("job") or "",
                "deadlineAt": iso(deadline_dt),
                "slotAt": iso(slot_dt),
                "detectedAt": str(pull.get("detectedAt") or ""),
                "supersededBy": str(pull.get("supersededBy") or ""),
                "href": href,
                "url": f"{full_base}/{href}",
                "shortTitle": video_label(resolved_title, vtype, ch, pull.get("film") or "", video_id=vid),
            })

        for w in watch_candidates:
            if w["id"] not in consumed_watch_ids:
                active_events.append(w)

        active_events.sort(key=lambda e: (e.get("deadlineAt") or "9999", e["id"]))
        active_ids = {e["id"] for e in active_events}

        events_state = state.setdefault("events", {})
        # Resolve any previously active events that are no longer active (job done, ticked, refilled, expired).
        for eid, rec in events_state.items():
            if isinstance(rec, dict) and not rec.get("resolvedAt") and eid not in active_ids:
                rec["resolvedAt"] = iso(at)

        board_active: list[dict] = []
        for ev in active_events:
            rec = events_state.get(ev["id"])
            if not isinstance(rec, dict):
                rec = {"id": ev["id"], "kind": ev["kind"], "sendCount": 0, "deliveries": []}
                events_state[ev["id"]] = rec
            if rec.get("resolvedAt"):
                continue

            deadline_dt = parse_iso(ev["deadlineAt"])
            if not deadline_dt or at >= deadline_dt:
                rec["resolvedAt"] = iso(at)
                continue

            send_count = int(rec.get("sendCount") or 0)
            repeat_dt = parse_iso(rec.get("repeatAt"))
            should_send = False
            is_repeat = False
            if send_count == 0:
                should_send = True
                is_repeat = False
            elif send_count == 1 and repeat_dt and at >= repeat_dt:
                should_send = True
                is_repeat = True

            full_msg, banner_msg = format_message(ev, at, is_repeat=is_repeat, site_url=full_base)
            if should_send and send_count < MAX_SENDS:
                delivery = {"phone": False, "phoneRoute": "dry-run", "thread": False}
                if deliver:
                    delivery = deliver_alert(
                        full_msg,
                        title=("Reminder: " if is_repeat else "") + ev["shortTitle"],
                        url=ev["url"],
                        config=cfg,
                        notify_fn=notify_fn,
                        post_fn=post_fn,
                    )
                rec["sendCount"] = send_count + 1
                rec["lastSentAt"] = iso(at)
                rec["lastMessage"] = full_msg
                if not is_repeat:
                    rec["firstSentAt"] = iso(at)
                    rem_s = max(float(MIN_REPEAT_GAP_S), (deadline_dt - at).total_seconds())
                    rec["repeatAt"] = iso(at + dt.timedelta(seconds=rem_s / 2.0))
                else:
                    rec["repeatedAt"] = iso(at)
                rec.setdefault("deliveries", []).append({"at": iso(at), "repeat": is_repeat, **delivery})
                sent_now.append({"id": ev["id"], "kind": ev["kind"], "repeat": is_repeat, "message": full_msg,
                                 "delivery": delivery})

            # Display text for the board banner always reflects current wording (without "Reminder:" duplication).
            display_full, display_banner = format_message(ev, at, is_repeat=False, site_url=full_base)
            rec["deadlineAt"] = ev["deadlineAt"]
            rec["href"] = ev["href"]
            board_active.append({
                "id": ev["id"],
                "kind": ev["kind"],
                "channel": ev["channel"],
                "title": ev["shortTitle"],
                "message": display_banner,
                "text": display_full,
                "href": ev["href"],
                "url": ev["url"],
                "deadlineAt": ev["deadlineAt"],
                "deadlineLondon": format_london_time(deadline_dt, at),
                "slotAt": ev.get("slotAt", ""),
                "sendCount": int(rec.get("sendCount") or 0),
                "firstSentAt": rec.get("firstSentAt", ""),
                "repeatAt": rec.get("repeatAt", ""),
                "repeatedAt": rec.get("repeatedAt", ""),
            })

        # Prune resolved records older than 14 days so state stays tiny.
        cutoff = at - dt.timedelta(days=14)
        for bucket in ("pulls", "events"):
            for k, rec in list((state.get(bucket) or {}).items()):
                res_dt = parse_iso((rec or {}).get("resolvedAt")) if isinstance(rec, dict) else None
                if res_dt and res_dt < cutoff:
                    state[bucket].pop(k, None)

        if deliver or sent_now or not p.exists():
            _write_json_atomic(p, state)

    phone_route = "ntfy" if cfg.get("ntfyUrl") else ("custom" if cfg.get("webhookCmd") else "unconfigured")
    return {
        "sent": sent_now,
        "board": {
            "updatedAt": iso(at),
            "phoneConfigured": phone_route != "unconfigured",
            "phoneRoute": phone_route,
            "proposedRoute": "ntfy",
            "active": board_active,
        },
    }


def record_pull(*, channel: str, video_id: str, title: str, slot_at: str, reason: str = "",
                change: str = "pulled", vtype: str = "short", film: str = "", job: str = "",
                watch_due: str = "", action: str = "", href: str = "",
                at: dt.datetime | None = None, state_file: pathlib.Path | None = None) -> dict:
    """Explicitly record a pulled/unscheduled/replaced video airing within 24 h so the next evaluation alerts immediately."""
    at = at or now_utc()
    slot_dt = parse_iso(slot_at)
    if not slot_dt:
        raise ValueError(f"invalid slot ISO time: {slot_at!r}")
    ch = str(channel or "").upper()
    pid = _pull_id(ch, video_id, slot_dt)
    rec = {
        "id": pid,
        "channel": ch,
        "videoId": str(video_id),
        "title": str(title or ""),
        "type": "short" if str(vtype or "").lower() == "short" else "long",
        "film": str(film or ""),
        "slotAt": iso(slot_dt),
        "change": change if change in ("pulled", "unscheduled", "replaced") else "pulled",
        "reason": str(reason or ""),
        "action": str(action or ""),
        "watchDueAt": iso(parse_iso(watch_due)) if parse_iso(watch_due) else "",
        "href": str(href or ""),
        "job": str(job or ""),
        "detectedAt": iso(at),
    }
    p = state_path(state_file)
    with _state_lock(p):
        state = load_state(p)
        if not state.get("seededAt"):
            state["seededAt"] = iso(at)
        state.setdefault("pulls", {})[pid] = rec
        _write_json_atomic(p, state)
    return rec


def resolve_event(event_id: str, *, at: dt.datetime | None = None, state_file: pathlib.Path | None = None,
                  resolution: str = "") -> bool:
    """Mark a pull or alert event resolved so repeats stop and the red board banner clears."""
    at = at or now_utc()
    p = state_path(state_file)
    changed = False
    with _state_lock(p):
        state = load_state(p)
        for bucket in ("pulls", "events"):
            rec = (state.get(bucket) or {}).get(event_id)
            if isinstance(rec, dict) and not rec.get("resolvedAt"):
                rec["resolvedAt"] = iso(at)
                if resolution:
                    rec["resolution"] = resolution
                changed = True
        if changed:
            _write_json_atomic(p, state)
    return changed


def has_due_work(at: dt.datetime | None = None, state_file: pathlib.Path | None = None) -> bool:
    """True when a stored event's half-time repeat is due or a newly recorded pull hasn't alerted yet."""
    at = at or now_utc()
    state = load_state(state_file)
    events = state.get("events") or {}
    for pid, pull in (state.get("pulls") or {}).items():
        if not isinstance(pull, dict) or pull.get("resolvedAt"):
            continue
        slot_dt = parse_iso(pull.get("slotAt"))
        if slot_dt and at < slot_dt and pid not in events:
            return True
    for rec in events.values():
        if not isinstance(rec, dict) or rec.get("resolvedAt"):
            continue
        if int(rec.get("sendCount") or 0) == 1:
            rep = parse_iso(rec.get("repeatAt"))
            dl = parse_iso(rec.get("deadlineAt"))
            if rep and at >= rep and (not dl or at < dl):
                return True
    return False


def check_from_disk(at: dt.datetime | None = None, *, deliver: bool = True,
                    state_file: pathlib.Path | None = None, config_file: pathlib.Path | None = None,
                    notify_fn=None, post_fn=None) -> dict:
    """Run an evaluation directly from the local studio checkout, board state and channel checkouts."""
    at = at or now_utc()
    studio_slug = channels.studio_slug()
    channel_roots = {s: channels.repo_path(s, HOME) for s in channels.slugs()}
    studio_root = channel_roots[studio_slug] if studio_slug else channels.studio_checkout(HOME)
    q = _read_json(studio_root / "jobs" / "queue.json", {}) or {}
    jobs = q.get("jobs") or []
    board_state_dir = pathlib.Path(os.environ.get("BOARD_STATE", str(HOME / "_desk" / "state" / "board")))
    last_board = _read_json(board_state_dir / "board.json", {}) or {}
    checks = last_board.get("checks") or {}
    videos = ((last_board.get("tracker") or {}).get("videos")) or []
    uploads = load_channel_uploads(channel_roots, studio_root=studio_root)
    return evaluate(
        at=at,
        jobs=jobs,
        checks=checks,
        videos=videos,
        uploads=uploads,
        state_file=state_file,
        config_file=config_file,
        deliver=deliver,
        notify_fn=notify_fn,
        post_fn=post_fn,
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="evaluate triggers and send due alerts")
    c.add_argument("--dry-run", action="store_true")
    sub.add_parser("status", help="show active alerts and phone delivery status")
    rp = sub.add_parser("record-pull", help="record a same-day pulled/unscheduled/replaced video")
    rp.add_argument("--channel", required=True)
    rp.add_argument("--video-id", required=True)
    rp.add_argument("--title", required=True)
    rp.add_argument("--slot", required=True, help="ISO UTC publishAt slot")
    rp.add_argument("--reason", default="")
    rp.add_argument("--change", default="pulled", choices=("pulled", "unscheduled", "replaced"))
    rp.add_argument("--type", dest="vtype", default="short", choices=("short", "long"))
    rp.add_argument("--film", default="")
    rp.add_argument("--job", default="")
    rp.add_argument("--watch-due", default="")
    rp.add_argument("--action", default="")
    rp.add_argument("--href", default="")
    rs = sub.add_parser("resolve", help="mark an alert event done/resolved")
    rs.add_argument("event_id")

    a = ap.parse_args(argv)
    if a.cmd == "check":
        res = check_from_disk(deliver=not a.dry_run)
        print(json.dumps({"sent": len(res["sent"]), "active": len(res["board"]["active"]),
                          "phoneRoute": res["board"]["phoneRoute"]}, ensure_ascii=False))
        for item in res["sent"]:
            print(item["message"])
        return 0
    if a.cmd == "status":
        st = load_state()
        cfg = load_config()
        active = [v for v in (st.get("events") or {}).values() if isinstance(v, dict) and not v.get("resolvedAt")]
        route = "ntfy" if cfg.get("ntfyUrl") else ("custom" if cfg.get("webhookCmd") else "unconfigured")
        print(json.dumps({"phoneRoute": route, "proposedRoute": "ntfy", "activeCount": len(active),
                          "active": active}, ensure_ascii=False, indent=2))
        return 0
    if a.cmd == "record-pull":
        rec = record_pull(
            channel=a.channel, video_id=a.video_id, title=a.title, slot_at=a.slot,
            reason=a.reason, change=a.change, vtype=a.vtype, film=a.film, job=a.job,
            watch_due=a.watch_due, action=a.action, href=a.href,
        )
        print(json.dumps(rec, ensure_ascii=False))
        return 0
    if a.cmd == "resolve":
        ok = resolve_event(a.event_id)
        print("resolved" if ok else "not found")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
