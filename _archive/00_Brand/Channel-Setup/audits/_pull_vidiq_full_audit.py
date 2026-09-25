#!/usr/bin/env python3
"""Full Orbit with Ben vidIQ MCP pull (HTTP). Writes raw JSON for channel audit."""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

TOKEN = os.environ.get("VIDIQ_MCP_TOKEN")
if not TOKEN:
    raise SystemExit("Set VIDIQ_MCP_TOKEN (Bearer token from Cursor mcp.json vidIQ server)")
BASE = "https://mcp.vidiq.com/mcp"
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"
VIDEO_IDS = [
    "Mo93x0fxB1Q",  # V001 long
    "z-DLqoSoEBo",  # S01
    "UWwNKYf_aU8",  # S02
    "MO19iXYCu0c",  # S03
    "--CxhjNqtSY",  # S04
]
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup/audits/"
    "CHANNEL_AUDIT_2026-08-01_pm/vidiq_raw.json"
)


def mcp_call(name: str, arguments: dict | None = None, retries: int = 3):
    payload = {
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000) % 1_000_000_000,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments or {}},
    }
    data = json.dumps(payload).encode()
    last_err = None
    for attempt in range(retries):
        req = urllib.request.Request(
            BASE,
            data=data,
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                body = resp.read().decode()
            # SSE: event: message\ndata: {...}
            m = re.search(r"data:\s*(\{.*\})", body, re.S)
            if not m:
                raise RuntimeError(f"No SSE data for {name}: {body[:300]}")
            msg = json.loads(m.group(1))
            if "error" in msg:
                raise RuntimeError(f"{name} error: {msg['error']}")
            result = msg.get("result", {})
            if "structuredContent" in result and result["structuredContent"] is not None:
                return result["structuredContent"]
            # fallback text JSON
            for c in result.get("content") or []:
                if c.get("type") == "text":
                    try:
                        return json.loads(c["text"])
                    except Exception:
                        return {"raw_text": c["text"]}
            return result
        except Exception as e:
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Failed {name}: {last_err}")


def main():
    pulled_at = datetime.now(timezone.utc).isoformat()
    out: dict = {
        "channelId": CHANNEL,
        "pulled_at": pulled_at,
        "source": "vidiq MCP HTTP direct",
    }
    print("balance…")
    out["balance"] = mcp_call("vidiq_balance")

    print("channel_stats…")
    out["channel_stats"] = mcp_call(
        "vidiq_channel_stats",
        {"channelId": CHANNEL, "from": "2026-07-27", "to": "2026-08-01"},
    )

    for key, fmt, popular in [
        ("long_recent", "long", False),
        ("short_recent", "short", False),
        ("long_popular", "long", True),
        ("short_popular", "short", True),
    ]:
        print(f"{key}…")
        out[key] = mcp_call(
            "vidiq_channel_videos",
            {"channelId": CHANNEL, "videoFormat": fmt, "popular": popular},
        )

    start, end = "2026-07-27", "2026-08-01"
    for key, report in [
        ("top_videos", "top_videos"),
        ("traffic_sources", "traffic_sources"),
        ("audience_demographics", "audience_demographics"),
        ("audience_geography", "audience_geography"),
        ("shorts_vs_longform", "shorts_vs_longform_split"),
    ]:
        print(f"analytics {key}…")
        out[key] = mcp_call(
            "vidiq_channel_analytics",
            {
                "channelId": CHANNEL,
                "report": report,
                "startDate": start,
                "endDate": end,
            },
        )

    print("daily_metrics…")
    out["daily_metrics"] = mcp_call(
        "vidiq_channel_analytics",
        {
            "channelId": CHANNEL,
            "startDate": start,
            "endDate": end,
            "dimensions": ["day"],
            "metrics": [
                "views",
                "estimatedMinutesWatched",
                "subscribersGained",
                "subscribersLost",
                "likes",
                "comments",
                "averageViewPercentage",
                "averageViewDuration",
            ],
        },
    )

    print("subscriber_insights…")
    out["subscriber_insights"] = mcp_call(
        "vidiq_subscriber_insights",
        {"channelId": CHANNEL, "timezoneOffset": "+01:00", "limit": 25},
    )

    out["video_ids"] = VIDEO_IDS
    print("videos_by_ids…")
    out["videos_by_ids"] = mcp_call(
        "vidiq_get_videos_by_ids", {"videoIds": VIDEO_IDS}
    )

    per_video = {}
    for vid in VIDEO_IDS:
        print(f"per_video {vid}…")
        entry = {}
        entry["retention"] = mcp_call(
            "vidiq_channel_analytics",
            {
                "channelId": CHANNEL,
                "report": "audience_retention",
                "startDate": start,
                "endDate": end,
                "filters": f"video=={vid}",
            },
        )
        entry["traffic"] = mcp_call(
            "vidiq_channel_analytics",
            {
                "channelId": CHANNEL,
                "report": "traffic_sources",
                "startDate": start,
                "endDate": end,
                "filters": f"video=={vid}",
            },
        )
        entry["hourly"] = mcp_call(
            "vidiq_video_stats",
            {
                "videoId": vid,
                "granularity": "hourly",
                "from": "2026-07-30T00:00:00Z",
                "to": "2026-08-01T23:59:59Z",
            },
        )
        per_video[vid] = entry
    out["per_video"] = per_video

    for key, kw in [
        ("kw_fermi_paradox", "fermi paradox"),
        ("kw_black_hole", "black hole"),
        ("kw_alien_worlds", "alien worlds"),
        ("kw_space_documentary", "space documentary"),
        ("kw_are_we_alone", "are we alone"),
        ("kw_great_filter", "great filter"),
        ("kw_jwst", "james webb space telescope"),
    ]:
        print(f"keyword {key}…")
        out[key] = mcp_call(
            "vidiq_keyword_research",
            {"mode": "research", "keyword": kw, "includeRelated": True, "country": "GB"},
        )

    print("outliers…")
    out["outliers_fermi"] = mcp_call(
        "vidiq_outliers",
        {
            "keyword": "fermi paradox",
            "contentType": "all",
            "publishedWithin": "thisMonth",
            "language": "en",
            "limit": 15,
        },
    )
    out["outliers_black_hole"] = mcp_call(
        "vidiq_outliers",
        {
            "keyword": "black hole",
            "contentType": "all",
            "publishedWithin": "thisMonth",
            "language": "en",
            "limit": 15,
        },
    )
    out["outliers_shorts_space"] = mcp_call(
        "vidiq_outliers",
        {
            "keyword": "space",
            "contentType": "short",
            "publishedWithin": "thisWeek",
            "language": "en",
            "maxSubscribers": 50000,
            "limit": 20,
        },
    )

    # Title scores
    titles = [
        ("long", "Why Haven't We Found Aliens Yet? The Fermi Paradox Explained | Orbit's Cosmic Journey", "Mo93x0fxB1Q"),
        ("short", "Where Is Everybody? The Fermi Paradox #Space #Shorts", "z-DLqoSoEBo"),
        ("short", "Where Is Everybody? The Fermi Paradox", None),
        ("short", "Why haven't we found aliens yet? The answer is terrifying", None),
        ("long", "What Happens If You Fall Into a Black Hole? | Orbit's Cosmic Journey", None),
        ("long", "Alien Worlds: The Strangest Planets We've Ever Found | Orbit's Cosmic Journey", None),
        ("short", "Space Is Rude About Distance", "UWwNKYf_aU8"),
        ("short", "What If Aliens Are Watching Us?", "MO19iXYCu0c"),
        ("short", "What If the First Alien Clue Is Already Here?", "--CxhjNqtSY"),
    ]
    title_scores = []
    for typ, title, vid in titles:
        print(f"score_title {title[:50]}…")
        args = {"title": title, "type": typ, "channelId": CHANNEL}
        if vid:
            args["videoId"] = vid
        title_scores.append({"type": typ, "title": title, "videoId": vid, "result": mcp_call("vidiq_score_title", args)})
    out["title_scores"] = title_scores

    print("balance_after…")
    out["balance_after"] = mcp_call("vidiq_balance")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print("WROTE", OUT)
    print("credits before", out["balance"].get("totalCredits"), "after", out["balance_after"].get("totalCredits"))


if __name__ == "__main__":
    main()
