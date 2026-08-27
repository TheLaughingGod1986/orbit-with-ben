#!/usr/bin/env python3
"""Lifetime vidIQ pull for the 25 Aug 2026 channel audit. Token from ~/.cursor/mcp.json."""
from __future__ import annotations

import json
import re
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"
START, END = "2026-07-27", "2026-08-25"
OUT = Path(__file__).resolve().parent / "vidiq_raw.json"

LONG_IDS = [
    "Mo93x0fxB1Q",  # Fermi
    "3xrxdmaOwJI",  # Black Hole
    "b8-X_FyJnHM",  # Alien Worlds
    "ziKBPJ6FY0U",  # JWST
    "REXYxuLOBoI",  # Last Star
    "NbW5G1BpPY0",  # Europa
    "Yk1tLh23rko",  # Neutron
]


def token() -> str:
    mcp = json.loads(Path.home().joinpath(".cursor/mcp.json").read_text())
    hdrs = mcp["mcpServers"]["vidIQ"]["headers"]
    auth = hdrs["Authorization"]
    return auth.split(" ", 1)[1]


def mcp_call(name: str, arguments: dict | None = None, retries: int = 3):
    payload = {
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000) % 1_000_000_000,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments or {}},
    }
    last_err = None
    for attempt in range(retries):
        req = urllib.request.Request(
            "https://mcp.vidiq.com/mcp",
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Bearer {token()}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                body = resp.read().decode()
            m = re.search(r"data:\s*(\{.*\})", body, re.S)
            if not m:
                raise RuntimeError(f"No SSE data for {name}: {body[:400]}")
            msg = json.loads(m.group(1))
            if "error" in msg:
                raise RuntimeError(f"{name} error: {msg['error']}")
            result = msg.get("result", {})
            if result.get("structuredContent") is not None:
                return result["structuredContent"]
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


def main() -> None:
    out: dict = {
        "channelId": CHANNEL,
        "pulled_at": datetime.now(timezone.utc).isoformat(),
        "window": {"start": START, "end": END},
    }
    print("balance…")
    out["balance"] = mcp_call("vidiq_balance")

    print("channel_stats…")
    out["channel_stats"] = mcp_call(
        "vidiq_channel_stats", {"channelId": CHANNEL, "from": START, "to": END}
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
                "startDate": START,
                "endDate": END,
                "maxResults": 50,
            },
        )

    print("daily_metrics…")
    out["daily_metrics"] = mcp_call(
        "vidiq_channel_analytics",
        {
            "channelId": CHANNEL,
            "startDate": START,
            "endDate": END,
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

    print("longs_by_ids…")
    out["longs_by_ids"] = mcp_call("vidiq_get_videos_by_ids", {"videoIds": LONG_IDS})

    # Retention on public longs only (skip if analytics empty)
    per_long = {}
    for vid in LONG_IDS[:5]:
        print(f"retention {vid}…")
        per_long[vid] = {
            "retention": mcp_call(
                "vidiq_channel_analytics",
                {
                    "channelId": CHANNEL,
                    "report": "audience_retention",
                    "startDate": START,
                    "endDate": END,
                    "filters": f"video=={vid}",
                },
            ),
            "traffic": mcp_call(
                "vidiq_channel_analytics",
                {
                    "channelId": CHANNEL,
                    "report": "traffic_sources",
                    "startDate": START,
                    "endDate": END,
                    "filters": f"video=={vid}",
                },
            ),
        }
    out["per_long"] = per_long

    shorts = (out.get("short_popular") or {}).get("videos") or []
    top_short_ids = [v["videoId"] for v in shorts[:6]]
    per_short = {}
    for vid in top_short_ids:
        print(f"short traffic {vid}…")
        per_short[vid] = mcp_call(
            "vidiq_channel_analytics",
            {
                "channelId": CHANNEL,
                "report": "traffic_sources",
                "startDate": START,
                "endDate": END,
                "filters": f"video=={vid}",
            },
        )
    out["per_short_traffic"] = per_short

    titles = [
        ("long", "Why Haven't We Found Aliens Yet? The Fermi Paradox Explained", "Mo93x0fxB1Q"),
        ("long", "What Happens If You Fall Into a Black Hole?", "3xrxdmaOwJI"),
        ("long", "These Galaxies Appeared Too Early", "ziKBPJ6FY0U"),
        ("long", "What Happens When the Last Star Dies?", "REXYxuLOBoI"),
        ("short", "Most of the Universe Gives Off No Light", "PV50PX-bE4g"),
        ("short", "We Found Planets Made of Diamond", "M-VN84HCNls"),
        ("short", "JWST Keeps Finding Galaxies Too Big, Too Soon", "68uTDP2esso"),
    ]
    scores = []
    for typ, title, vid in titles:
        print(f"score {title[:48]}…")
        args = {"title": title, "type": typ, "channelId": CHANNEL, "videoId": vid}
        scores.append({"type": typ, "title": title, "videoId": vid, "result": mcp_call("vidiq_score_title", args)})
    out["title_scores"] = scores

    for key, kw in [
        ("kw_neutron_star", "neutron star"),
        ("kw_europa", "europa moon"),
        ("kw_last_star", "heat death of the universe"),
        ("kw_jwst", "james webb space telescope"),
        ("kw_black_hole", "what happens if you fall into a black hole"),
    ]:
        print(f"keyword {key}…")
        out[key] = mcp_call(
            "vidiq_keyword_research",
            {"mode": "research", "keyword": kw, "includeRelated": True, "country": "GB"},
        )

    print("balance_after…")
    out["balance_after"] = mcp_call("vidiq_balance")
    OUT.write_text(json.dumps(out, indent=2))
    print("WROTE", OUT)
    print(
        "credits",
        out["balance"].get("totalCredits"),
        "→",
        out["balance_after"].get("totalCredits"),
    )


if __name__ == "__main__":
    main()
