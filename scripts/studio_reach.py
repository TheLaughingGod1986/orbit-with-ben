#!/usr/bin/env python3
"""Monthly Studio Reach window and the 1st-of-month studio_ctr archive.

Read-only. Navigates YouTube Studio analytics and POSTs yta_web/get_screen.
It never saves a video, title, thumbnail, or setting.

The lifetime reader (jobs/backlog.json studio-ctr-daily) still writes
05_Analytics/<channel>/studio_ctr.json. On the 1st, `morning` copies that
file to studio_ctr_YYYY-MM-01.json and will not overwrite it later.

A closed calendar month is scraped as a dateIdRange (inclusive start,
exclusive end = the next day) into studio_reach_monthly_YYYY-MM.json:
longs get impressions and impressionsCtr; Shorts get stayedToWatch.
A closed file is never replaced. An open month-to-date file may be
replaced by a later read, including the closed read on the 1st.

  python3 scripts/studio_reach.py morning --channel both
  python3 scripts/studio_reach.py month --channel hos --start 2026-10-01 --end 2026-10-31
  python3 scripts/studio_reach.py seed-archive --channel hos --date 2026-11-01 --git-rev 251eaa53ba

Chief h47, J2202 / J2206. £0. No YouTube writes.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANNELS = {
    "hos": {"port": 9460, "channel_id": "UCXp7HkBIl1LgaznXuZHJyRg"},
    "owb": {"port": 9223, "channel_id": "UC_esArsDKd3GJvOkeO0DUog"},
}
LONG_TAB = "ANALYTICS_TAB_ID_REACH"
SHORT_TAB = "ANALYTICS_TAB_ID_ENGAGEMENT"


def date_id(day: dt.date) -> int:
    return day.year * 10000 + day.month * 100 + day.day


def parse_day(text: str) -> dt.date:
    return dt.date.fromisoformat(text)


def window_ids(start: dt.date, end: dt.date) -> tuple[int, int]:
    if end < start:
        raise ValueError(f"end {end} is before start {start}")
    return date_id(start), date_id(end + dt.timedelta(days=1))


def month_bounds(year: int, month: int) -> tuple[dt.date, dt.date]:
    start = dt.date(year, month, 1)
    if month == 12:
        next_first = dt.date(year + 1, 1, 1)
    else:
        next_first = dt.date(year, month + 1, 1)
    return start, next_first - dt.timedelta(days=1)


def previous_month(today: dt.date) -> tuple[int, int]:
    prev = today.replace(day=1) - dt.timedelta(days=1)
    return prev.year, prev.month


def is_closed_month(start: dt.date, end: dt.date) -> bool:
    bounds = month_bounds(start.year, start.month)
    return (start, end) == bounds


def morning_plan(today: dt.date) -> dict:
    if today.day != 1:
        return {"archive": False, "scrape_month": None}
    return {"archive": True, "scrape_month": previous_month(today)}


def as_number(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        text = value.replace(",", "").replace("%", "").strip()
        if not text:
            return None
        try:
            return float(text) if "." in text else int(text)
        except ValueError:
            return None
    return None


def _walk(node, visit):
    if isinstance(node, dict):
        visit(node)
        for value in node.values():
            _walk(value, visit)
    elif isinstance(node, list):
        for value in node:
            _walk(value, visit)


def key_metric_totals(payload: dict) -> dict:
    found = {}

    def visit(node):
        primary = node.get("primaryContent")
        if not isinstance(primary, dict):
            return
        metric = primary.get("metric")
        if metric and "total" in primary and metric not in found:
            number = as_number(primary.get("total"))
            if number is not None:
                found[metric] = number

    _walk(payload, visit)
    return found


def stayed_to_watch(payload: dict):
    found = []

    def visit(node):
        data = node.get("stackedBarCardData")
        if not isinstance(data, dict):
            return
        overview = data.get("overviewCardData") or {}
        columns = (overview.get("cardData") or {}).get("metricColumns") or []
        metric = None
        if columns and isinstance(columns[0], dict):
            metric = (columns[0].get("metric") or {}).get("type")
        values = overview.get("values") or []
        if metric == "SHORTS_FEED_IMPRESSIONS_VTR" and values:
            number = as_number(values[0])
            if number is not None:
                found.append(number)

    _walk(payload, visit)
    return found[0] if found else None


def response_windows(payload: dict) -> list:
    found = []

    def visit(node):
        if set(node) <= {"inclusiveStart", "exclusiveEnd"} and "inclusiveStart" in node:
            found.append((node["inclusiveStart"], node["exclusiveEnd"]))

    _walk(payload, visit)
    return found


def response_window(payload: dict):
    found = response_windows(payload)
    return found[0] if found else None


def long_row(payload: dict):
    totals = key_metric_totals(payload)
    row = {"format": "long"}
    if "VIDEO_THUMBNAIL_IMPRESSIONS" in totals:
        row["impressions"] = totals["VIDEO_THUMBNAIL_IMPRESSIONS"]
    if "VIDEO_THUMBNAIL_IMPRESSIONS_VTR" in totals:
        row["impressionsCtr"] = totals["VIDEO_THUMBNAIL_IMPRESSIONS_VTR"]
    return row if len(row) > 1 else None


def short_row(payload: dict):
    stayed = stayed_to_watch(payload)
    if stayed is None:
        return None
    return {"format": "short", "stayedToWatch": stayed}


def row_for(fmt: str, payload: dict):
    if fmt == "long":
        return long_row(payload)
    if fmt == "short":
        return short_row(payload)
    return None


def archive_name(day: dt.date) -> str:
    return f"studio_ctr_{day.isoformat()}.json"


def reach_name(start: dt.date) -> str:
    return f"studio_reach_monthly_{start.year:04d}-{start.month:02d}.json"


def channel_dir(root: Path, channel: str) -> Path:
    if channel not in CHANNELS:
        raise SystemExit(f"unknown channel {channel}")
    return root / "05_Analytics" / channel


def write_immutable(dest: Path, content: bytes) -> str:
    if dest.exists():
        return "kept"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(content)
    return "written"


def write_reach(path: Path, doc: dict) -> str:
    if path.exists():
        old = json.loads(path.read_text())
        if old.get("closed"):
            return "kept"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2) + "\n")
    return "written"


def archive_studio_ctr(root: Path, channel: str, day: dt.date) -> str:
    """Copy today's studio_ctr.json. Only the 1st is an archive day."""
    if day.day != 1:
        return "skipped"
    src = channel_dir(root, channel) / "studio_ctr.json"
    if not src.exists():
        return "missing"
    return write_immutable(channel_dir(root, channel) / archive_name(day), src.read_bytes())


def seed_archive(root: Path, channel: str, day: dt.date, rev: str) -> str:
    """Immutable copy of studio_ctr.json as it was committed on `day`."""
    rel = f"05_Analytics/{channel}/studio_ctr.json"
    content = subprocess.check_output(["git", "show", f"{rev}:{rel}"], cwd=root)
    doc = json.loads(content)
    read_at = str(doc.get("readAt") or "")
    if not read_at.startswith(day.isoformat()):
        raise SystemExit(f"refusing seed: {rev} readAt {read_at} is not {day.isoformat()}")
    if not content.endswith(b"\n"):
        content += b"\n"
    return write_immutable(channel_dir(root, channel) / archive_name(day), content)


def channel_videos(root: Path, channel: str) -> list[dict]:
    data = json.loads((root / "05_Analytics" / "dashboard" / "data.json").read_text())
    for entry in data["channels"]:
        if entry.get("channel") == channel:
            return [{"id": video["id"], "format": video.get("format")} for video in entry["videos"]]
    raise SystemExit(f"no {channel} channel in dashboard data")


def _capture_template(page, video_id: str) -> dict:
    captured = {}

    def on_request(request):
        if "yta_web/get_screen" in request.url and "raw" not in captured:
            headers = request.headers
            captured["url"] = request.url
            captured["authorization"] = headers.get("authorization", "")
            captured["client"] = headers.get("x-youtube-client-version", "")
            captured["raw"] = request.post_data

    page.on("request", on_request)
    page.goto("https://studio.youtube.com/", wait_until="domcontentloaded", timeout=20000)
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/analytics/tab-reach_viewers/period-lifetime",
        wait_until="domcontentloaded",
        timeout=25000,
    )
    page.wait_for_timeout(2000)
    page.remove_listener("request", on_request)
    if "raw" not in captured:
        raise SystemExit("Studio did not send yta_web/get_screen; the analytics page did not load")
    return captured


def _channel_id(page) -> str:
    return page.evaluate(
        """() => (window.ytcfg && window.ytcfg.get && window.ytcfg.get('CHANNEL_ID')) || ''"""
    )


def _post_screen(page, template: dict, video_id: str, tab: str, start_id: int, end_id: int) -> dict:
    body = json.loads(template["raw"])
    body["screenConfig"]["entity"] = {"videoId": video_id}
    body["screenConfig"]["timePeriod"] = {
        "dateIdRange": {"inclusiveStart": start_id, "exclusiveEnd": end_id}
    }
    body["desktopState"] = {"tabId": tab}
    text = page.evaluate(
        """async ({url, body, auth, client}) => {
          const response = await fetch(url, {
            method: 'POST',
            credentials: 'include',
            headers: {
              'content-type': 'application/json',
              'authorization': auth,
              'x-youtube-client-version': client,
            },
            body: JSON.stringify(body),
          });
          return JSON.stringify({status: response.status, text: await response.text()});
        }""",
        {
            "url": template["url"],
            "body": body,
            "auth": template["authorization"],
            "client": template["client"],
        },
    )
    wrapped = json.loads(text)
    if wrapped["status"] != 200:
        raise RuntimeError(f"get_screen HTTP {wrapped['status']} {wrapped['text'][:180]}")
    return json.loads(wrapped["text"])


def scrape_window(root: Path, channel: str, start: dt.date, end: dt.date) -> dict:
    """Read one Studio date window. Read-only. Returns the document and the write result."""
    sys.path.insert(0, str(root / "scripts"))
    from playwright.sync_api import sync_playwright
    from cdp_tabs import reuse_page

    info = CHANNELS[channel]
    videos = [video for video in channel_videos(root, channel) if video["format"] in ("long", "short")]
    if not videos:
        raise SystemExit(f"no videos for {channel}")
    start_id, end_id = window_ids(start, end)
    closed = is_closed_month(start, end)
    rows, errors, omitted = {}, [], []
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{info['port']}")
        page = reuse_page(browser.contexts[0], "studio.youtube.com")
        template = _capture_template(page, videos[0]["id"])
        seen = _channel_id(page)
        if seen != info["channel_id"]:
            raise SystemExit(f"{channel} Studio channel is {seen or 'unknown'}, expected {info['channel_id']}")
        for video in videos:
            tab = LONG_TAB if video["format"] == "long" else SHORT_TAB
            payload = None
            last_error = ""
            for _attempt in (1, 2):
                try:
                    payload = _post_screen(page, template, video["id"], tab, start_id, end_id)
                    break
                except Exception as exc:
                    last_error = str(exc)[:180]
                    time.sleep(0.4)
            if payload is None:
                errors.append({"id": video["id"], "error": last_error})
                print(channel, video["format"], video["id"], "ERROR", last_error, flush=True)
                continue
            got = response_windows(payload)
            if (start_id, end_id) not in got:
                errors.append({"id": video["id"], "error": f"window {got} != {(start_id, end_id)}"})
                print(channel, video["format"], video["id"], "WINDOW", got, flush=True)
                continue
            row = row_for(video["format"], payload)
            if row:
                rows[video["id"]] = row
                print(channel, video["format"], video["id"], row, flush=True)
            else:
                omitted.append(video["id"])
                print(channel, video["format"], video["id"], "OMITTED", flush=True)
            time.sleep(0.15)
    doc = {
        "readAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "channel": channel,
        "period": {
            "start": start.isoformat(),
            "end": end.isoformat(),
            "inclusiveStart": start_id,
            "exclusiveEnd": end_id,
        },
        "closed": closed,
        "source": "studio yta_web/get_screen dateIdRange (read-only)",
        "videos": rows,
        "omitted": omitted,
        "errors": errors,
    }
    path = channel_dir(root, channel) / reach_name(start)
    result = write_reach(path, doc)
    doc["path"] = str(path.relative_to(root))
    doc["write"] = result
    return doc


def selected_channels(name: str) -> list[str]:
    if name == "both":
        return ["hos", "owb"]
    if name not in CHANNELS:
        raise SystemExit(f"unknown channel {name}")
    return [name]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Monthly Studio Reach window (read-only)")
    parser.add_argument("--root", default=str(ROOT))
    sub = parser.add_subparsers(dest="cmd", required=True)

    morning = sub.add_parser("morning")
    morning.add_argument("--channel", required=True, choices=["hos", "owb", "both"])
    morning.add_argument("--today", default=dt.date.today().isoformat())

    month = sub.add_parser("month")
    month.add_argument("--channel", required=True, choices=["hos", "owb"])
    month.add_argument("--start", required=True)
    month.add_argument("--end", required=True)

    seed = sub.add_parser("seed-archive")
    seed.add_argument("--channel", required=True, choices=["hos", "owb"])
    seed.add_argument("--date", required=True)
    seed.add_argument("--git-rev", required=True)

    args = parser.parse_args(argv)
    root = Path(args.root)
    if args.cmd == "seed-archive":
        day = parse_day(args.date)
        result = seed_archive(root, args.channel, day, args.git_rev)
        print(args.channel, archive_name(day), result)
        return 0
    if args.cmd == "morning":
        today = parse_day(args.today)
        plan = morning_plan(today)
        print("plan", plan)
        for channel in selected_channels(args.channel):
            if plan["archive"]:
                print(channel, "archive", archive_studio_ctr(root, channel, today))
            if plan["scrape_month"]:
                year, month_number = plan["scrape_month"]
                start, end = month_bounds(year, month_number)
                doc = scrape_window(root, channel, start, end)
                print(channel, doc["path"], doc["write"], "videos", len(doc["videos"]), "omitted", len(doc["omitted"]), "errors", len(doc["errors"]))
        return 0
    start, end = parse_day(args.start), parse_day(args.end)
    doc = scrape_window(root, args.channel, start, end)
    print(doc["path"], doc["write"], "closed", doc["closed"], "videos", len(doc["videos"]), "omitted", len(doc["omitted"]), "errors", len(doc["errors"]))
    return 1 if doc["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
