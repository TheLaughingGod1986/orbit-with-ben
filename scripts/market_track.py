#!/usr/bin/env python3
"""Market intelligence tracker for Field Order History (ww2), Orbit With Ben (owb) and History of Science (hos).

Tracks a Data-API-verified watchlist of ~90 rising and benchmark channels across our three niches:
  - daily:   reads uploads playlists (`playlistItems.list`) and video stats (`videos.list`, batches of 50),
             computes per-channel 20-long median, snapshots views at ~6h / 24h / 72h, flags breakouts
             (>= 3x channel median at 24h, or 100k+ views within 72h on <20k-sub channels), separates
             long-form (>4 min) from Shorts, filters AI content farms into a separate list, enforces a
             hard 1,500-unit daily YouTube Data API quota cap (never `search.list` daily), rolls up
             daily snapshots older than 14 days into weekly JSONs, and updates `05_Analytics/market/board.json`.
  - weekly:  tags breakout titles and thumbnails (from thumbnail image URLs only, 168 px phone metrics +
             optional vision model), writes `05_Analytics/market/weekly/<YYYY-MM-DD>.md` with one
             "angle we could take" line per breakout, and refreshes `05_Analytics/market/board.json`.
  - discover: first-Monday monthly discovery sweep (hard cap <= 40 vidIQ credits, never buys credits)
             proposing watchlist swaps in `05_Analytics/market/proposals/<YYYY-MM>.md`.

Guards:
  - Read-only YouTube Data API metadata and thumbnail image URLs only; never opens or plays any video.
  - No revenue estimates. No edits to any YouTube channel. GBP 0 beyond existing subscriptions.
  - Never prints or commits API keys, OAuth tokens, emails or private network addresses.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import io
import json
import os
import pathlib
import re
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable

try:
    from PIL import Image, ImageFilter, ImageStat
except ImportError:  # pragma: no cover - Pillow is installed on the Mini & CI
    Image = ImageFilter = ImageStat = None

ROOT = pathlib.Path(__file__).resolve().parents[1]
MARKET_DIR = ROOT / "05_Analytics" / "market"
WATCHLIST_PATH = MARKET_DIR / "watchlist.json"
DAILY_DIR = MARKET_DIR / "daily"
WEEKLY_DIR = MARKET_DIR / "weekly"
PROPOSALS_DIR = MARKET_DIR / "proposals"
STATE_PATH = MARKET_DIR / "state.json"
FARMS_PATH = MARKET_DIR / "farms.json"
QUOTA_PATH = MARKET_DIR / "quota.json"
BOARD_PATH = MARKET_DIR / "board.json"
DEFAULT_ENV_PATH = ROOT / "07_Content-Ops" / ".env"

DAILY_QUOTA_CAP = 1500
MONTHLY_VIDIQ_CAP = 40
LONG_MIN_SECONDS = 240  # strictly over 4 minutes (> 240 s)
BREAKOUT_MULTIPLE = 3.0
SMALL_CHANNEL_SUBS = 20_000
SMALL_BREAKOUT_VIEWS = 100_000
SMALL_BREAKOUT_HOURS = 72.0
RISING_MAX_AGE_DAYS = 183
RISING_MAX_SUBS = 20_000
FARM_LIKE_RATIO_MIN = 0.015
FARM_MIN_VIEWS_FOR_RATIO = 200
DAILY_RETENTION_DAYS = 14
TRACK_WINDOW_HOURS = 168.0  # keep active tracking for 7 days
YT_API_BASE = "https://www.googleapis.com/youtube/v3"

NICHE_META = {
    "ww2": {"slug": "ww2", "label": "WW2", "channel": "Field Order History"},
    "owb": {"slug": "owb", "label": "Space", "channel": "Orbit With Ben"},
    "hos": {"slug": "hos", "label": "History of Science", "channel": "History of Science"},
}

FARM_TITLE_PATTERNS = [
    re.compile(r"^\s*what\s+.+\s+(?:said|did|found|discovered|saw|told|heard|revealed)\s+when\b", re.I),
    re.compile(r"^\s*what\s+happened\s+when\s+.+", re.I),
    re.compile(r"^\s*when\s+.+\s+(?:saw|opened|found|captured|heard|witnessed|discovered)\b", re.I),
    re.compile(r"^\s*what\s+(?:stunned|shocked|haunted|terrified|baffled)\s+.+", re.I),
    re.compile(r"\bthey\s+couldn'?t\s+believe\s+what\b", re.I),
]

VAGUE_OPENERS = {
    "what", "why", "how", "when", "where", "who", "this", "these", "that", "those",
    "the", "a", "an", "you", "we", "they", "i", "is", "are", "was", "were", "can",
    "could", "would", "should", "did", "do", "does", "top", "inside", "secret",
    "secrets", "untold", "hidden", "crazy", "insane", "terrifying", "shocking",
}

HOW_WHY_RE = re.compile(r"^\s*(?:how|why)\b", re.I)
WHAT_WHEN_RE = re.compile(r"^\s*(?:what|when)\b", re.I)
NUMBER_RE = re.compile(r"\b\d[\d,\.]*\b")
ISO_DUR_RE = re.compile(r"^P(?:(?P<d>\d+)D)?(?:T(?:(?P<h>\d+)H)?(?:(?P<m>\d+)M)?(?:(?P<s>\d+)S)?)?$")


class QuotaError(RuntimeError):
    """Raised when a YouTube Data API call would exceed the daily cap or call a forbidden endpoint."""


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def iso_utc(t: dt.datetime) -> str:
    return t.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_iso_utc(s: str | None) -> dt.datetime | None:
    if not s:
        return None
    try:
        t = dt.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        return t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)
    except ValueError:
        return None


def parse_iso_duration(duration: str | None) -> int:
    if not duration:
        return 0
    m = ISO_DUR_RE.match(duration.strip())
    if not m:
        return 0
    days = int(m.group("d") or 0)
    hours = int(m.group("h") or 0)
    mins = int(m.group("m") or 0)
    secs = int(m.group("s") or 0)
    return days * 86400 + hours * 3600 + mins * 60 + secs


def classify_format(duration_s: int, title: str = "") -> str:
    """Long-form is strictly over 4 minutes (> 240 s); shorter videos are flagged as short."""
    if duration_s > LONG_MIN_SECONDS:
        return "long"
    return "short"


def channel_long_median(videos: list[dict[str, Any]], limit: int = 20) -> float:
    """Median views of a channel's most recent `limit` long uploads (> 4 minutes)."""
    longs = [v for v in videos if int(v.get("duration_s", 0) or 0) > LONG_MIN_SECONDS]
    longs.sort(key=lambda v: str(v.get("published_at") or ""), reverse=True)
    recent = [int(v.get("views", 0) or 0) for v in longs[:limit]]
    if not recent:
        return 0.0
    return float(statistics.median(recent))


def snapshot_bucket(age_hours: float) -> str | None:
    """Map upload age in hours to the nearest tracking window (6h, 24h, 72h)."""
    if 3.0 <= age_hours <= 12.0:
        return "6h"
    if 18.0 <= age_hours <= 36.0:
        return "24h"
    if 60.0 <= age_hours <= 96.0:
        return "72h"
    return None


def is_farm_video(video: dict[str, Any]) -> tuple[bool, str]:
    """Identify likely AI content farms by low like ratio (< 0.015) or templated titles."""
    title = str(video.get("title") or "")
    for pat in FARM_TITLE_PATTERNS:
        if pat.search(title):
            return True, "templated_title"
    views = int(video.get("views", 0) or 0)
    likes = video.get("likes")
    if views >= FARM_MIN_VIEWS_FOR_RATIO and likes is not None:
        ratio = float(likes) / float(views)
        if ratio < FARM_LIKE_RATIO_MIN:
            return True, f"low_like_ratio:{ratio:.4f}"
    return False, ""


def evaluate_breakout(
    video: dict[str, Any],
    channel: dict[str, Any],
    age_hours: float,
    snapshots: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Score a video against breakout thresholds and the farm filter."""
    views = int(video.get("views", 0) or 0)
    likes = video.get("likes")
    duration_s = int(video.get("duration_s", 0) or 0)
    fmt = classify_format(duration_s, str(video.get("title") or ""))
    median = float(channel.get("median_long_views", 0.0) or 0.0)
    subs = int(channel.get("subscribers", 0) or 0)
    snaps = snapshots or {}

    age_safe = max(float(age_hours), 0.5)
    vph = round(views / age_safe, 1)
    multiple = round(views / median, 2) if median > 0 else None

    farm, farm_reason = is_farm_video(video)

    views_24h = None
    if isinstance(snaps.get("24h"), dict) and snaps["24h"].get("views") is not None:
        views_24h = int(snaps["24h"]["views"])
    elif 18.0 <= age_hours <= TRACK_WINDOW_HOURS:
        views_24h = views

    views_72h = None
    if isinstance(snaps.get("72h"), dict) and snaps["72h"].get("views") is not None:
        views_72h = int(snaps["72h"]["views"])
    elif age_hours <= SMALL_BREAKOUT_HOURS:
        views_72h = views

    reasons: list[str] = []
    if median > 0 and views_24h is not None and (views_24h / median) >= BREAKOUT_MULTIPLE:
        reasons.append("3x_median_24h")
    if subs < SMALL_CHANNEL_SUBS and views_72h is not None and views_72h >= SMALL_BREAKOUT_VIEWS:
        reasons.append("100k_72h_small")

    is_breakout = bool(reasons) and not farm
    like_ratio = round(float(likes) / float(views), 4) if (likes is not None and views > 0) else None
    return {
        "video_id": video.get("video_id") or video.get("id", ""),
        "title": str(video.get("title") or ""),
        "channel_id": channel.get("id", ""),
        "channel_title": channel.get("title", ""),
        "channel_subscribers": subs,
        "channel_tier": channel.get("tier", "benchmark"),
        "niche": channel.get("niche", ""),
        "published_at": video.get("published_at", ""),
        "duration_s": duration_s,
        "format": fmt,
        "views": views,
        "likes": likes,
        "like_ratio": like_ratio,
        "age_hours": round(float(age_hours), 1),
        "views_per_hour": vph,
        "channel_median": round(median, 1),
        "multiple": multiple,
        "snapshots": snaps,
        "thumbnail_url": video.get("thumbnail_url")
        or (f"https://i.ytimg.com/vi/{video.get('video_id') or video.get('id', '')}/hqdefault.jpg"),
        "is_farm": farm,
        "farm_reason": farm_reason,
        "is_breakout": is_breakout,
        "breakout_reasons": reasons if is_breakout else [],
    }


class QuotaGuard:
    """Hard daily unit cap (<= 1,500/day) and strict daily search.list prohibition."""

    def __init__(
        self,
        daily_cap: int = DAILY_QUOTA_CAP,
        allow_search: bool = False,
        state_path: pathlib.Path | None = None,
        today: str | None = None,
    ) -> None:
        self.daily_cap = min(int(daily_cap), DAILY_QUOTA_CAP)
        self.allow_search = bool(allow_search)
        self.state_path = state_path
        self.today = today or utc_now().date().isoformat()
        self.used = 0
        self.by_endpoint: dict[str, int] = {}
        self._history: dict[str, dict[str, Any]] = {}
        if state_path and state_path.exists():
            try:
                raw = json.loads(state_path.read_text())
                if isinstance(raw, dict):
                    self._history = raw.get("days") or {}
                    day = self._history.get(self.today) or {}
                    self.used = int(day.get("used", 0) or 0)
                    self.by_endpoint = dict(day.get("by_endpoint") or {})
            except (OSError, ValueError):
                pass

    @property
    def remaining(self) -> int:
        return max(0, self.daily_cap - self.used)

    def consume(self, endpoint: str, cost: int) -> None:
        if endpoint == "search.list" and not self.allow_search:
            raise QuotaError("search.list is forbidden in daily market tracking")
        if cost < 0:
            raise ValueError("cost must be non-negative")
        if self.used + cost > self.daily_cap:
            raise QuotaError(
                f"daily YouTube Data API quota cap exceeded: {self.used} + {cost} > {self.daily_cap}"
            )
        self.used += cost
        self.by_endpoint[endpoint] = self.by_endpoint.get(endpoint, 0) + cost

    def save(self) -> None:
        if not self.state_path:
            return
        self._history[self.today] = {"used": self.used, "cap": self.daily_cap, "by_endpoint": self.by_endpoint}
        # Keep only the latest 30 days to keep git compact.
        kept_keys = sorted(self._history.keys())[-30:]
        trimmed = {k: self._history[k] for k in kept_keys}
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(
            json.dumps({"schema_version": 1, "daily_cap": self.daily_cap, "days": trimmed}, indent=2) + "\n"
        )

    def summary(self) -> dict[str, Any]:
        return {
            "date": self.today,
            "used": self.used,
            "cap": self.daily_cap,
            "remaining": self.remaining,
            "by_endpoint": dict(self.by_endpoint),
        }


def resolve_env_path(path: pathlib.Path | None = None) -> pathlib.Path:
    if path and path.is_file():
        return path
    env_override = os.environ.get("MARKET_ENV_FILE", "").strip()
    if env_override and pathlib.Path(env_override).is_file():
        return pathlib.Path(env_override)
    if DEFAULT_ENV_PATH.is_file():
        return DEFAULT_ENV_PATH
    fallback = pathlib.Path(os.environ.get("ORBIT_REPO", str(pathlib.Path.home() / "YouTube" / "orbit-with-ben"))) / "07_Content-Ops" / ".env"
    return fallback if fallback.is_file() else (path or DEFAULT_ENV_PATH)


def load_env_file(path: pathlib.Path = DEFAULT_ENV_PATH) -> dict[str, str]:
    target = resolve_env_path(path)
    out: dict[str, str] = {}
    if not target.is_file():
        return out
    for line in target.read_text().splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


class YouTubeDataClient:
    """Read-only YouTube Data API v3 client backed by API key or Mini OAuth refresh token."""

    def __init__(self, quota: QuotaGuard, env_path: pathlib.Path = DEFAULT_ENV_PATH) -> None:
        self.quota = quota
        self.env_path = env_path
        self._api_key = os.environ.get("YOUTUBE_API_KEY", "").strip()
        self._bearer: str | None = None
        if not self._api_key:
            env = load_env_file(env_path)
            self._api_key = env.get("YOUTUBE_API_KEY", "").strip()
            self._env = env
        else:
            self._env = {}

    def _get_bearer(self) -> str:
        if self._bearer:
            return self._bearer
        cid = os.environ.get("GOOGLE_CLIENT_ID") or self._env.get("GOOGLE_CLIENT_ID", "")
        csec = os.environ.get("GOOGLE_CLIENT_SECRET") or self._env.get("GOOGLE_CLIENT_SECRET", "")
        rtok = (
            os.environ.get("YT_ANALYTICS_REFRESH_TOKEN_OWB")
            or self._env.get("YT_ANALYTICS_REFRESH_TOKEN_OWB")
            or os.environ.get("YOUTUBE_REFRESH_TOKEN")
            or self._env.get("YOUTUBE_REFRESH_TOKEN", "")
        )
        if not (cid and csec and rtok):
            raise RuntimeError("Missing YouTube Data API key or OAuth credentials in environment / 07_Content-Ops/.env")
        data = urllib.parse.urlencode({
            "client_id": cid,
            "client_secret": csec,
            "refresh_token": rtok,
            "grant_type": "refresh_token",
        }).encode()
        req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.loads(resp.read())
        self._bearer = str(body["access_token"])
        return self._bearer

    def _get(self, resource: str, endpoint_name: str, params: dict[str, Any], cost: int = 1) -> dict[str, Any]:
        self.quota.consume(endpoint_name, cost)
        q = dict(params)
        headers: dict[str, str] = {"User-Agent": "studio-market-tracker/1"}
        if self._api_key:
            q["key"] = self._api_key
        else:
            headers["Authorization"] = f"Bearer {self._get_bearer()}"
        url = f"{YT_API_BASE}/{resource}?{urllib.parse.urlencode(q)}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=25) as resp:
            return json.loads(resp.read())

    def channels_by_ids(self, ids: list[str]) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        unique = list(dict.fromkeys(i for i in ids if i))
        for i in range(0, len(unique), 50):
            batch = unique[i : i + 50]
            res = self._get(
                "channels",
                "channels.list",
                {"part": "id,snippet,statistics,contentDetails", "id": ",".join(batch)},
                cost=1,
            )
            items.extend(res.get("items") or [])
        return items

    def playlist_items(self, playlist_id: str, max_results: int = 25) -> list[dict[str, Any]]:
        if not playlist_id:
            return []
        res = self._get(
            "playlistItems",
            "playlistItems.list",
            {"part": "contentDetails,snippet", "playlistId": playlist_id, "maxResults": min(50, max_results)},
            cost=1,
        )
        return list(res.get("items") or [])

    def videos_by_ids(self, ids: list[str]) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        unique = list(dict.fromkeys(i for i in ids if i))
        for i in range(0, len(unique), 50):
            batch = unique[i : i + 50]
            res = self._get(
                "videos",
                "videos.list",
                {"part": "id,snippet,contentDetails,statistics", "id": ",".join(batch)},
                cost=1,
            )
            items.extend(res.get("items") or [])
        return items


def tag_title(title: str, niche: str = "") -> dict[str, Any]:
    """Tag title patterns for weekly packaging intelligence."""
    clean = " ".join((title or "").split())
    words = clean.split()
    first_word = re.sub(r"[^A-Za-z0-9'-]", "", words[0]).lower() if words else ""
    how_why = bool(HOW_WHY_RE.match(clean))
    what_when = bool(WHAT_WHEN_RE.match(clean))
    has_num = bool(NUMBER_RE.search(clean))
    is_q = "?" in clean

    # Check if the title leads with a concrete searched subject/entity (proper noun, colon head, or specific term)
    colon_head = clean.split(":", 1)[0].strip() if ":" in clean else ""
    starts_searched = False
    if colon_head and len(colon_head.split()) <= 5 and first_word not in VAGUE_OPENERS:
        starts_searched = True
    elif words and first_word not in VAGUE_OPENERS and not how_why and not what_when:
        starts_searched = True

    if how_why:
        opener = "how_why"
    elif starts_searched:
        opener = "searched_name"
    elif what_when:
        opener = "what_when"
    elif words and NUMBER_RE.match(words[0]):
        opener = "number"
    else:
        opener = "other"

    return {
        "starts_with_searched_name": starts_searched,
        "how_why_opener": how_why,
        "has_number": has_num,
        "word_count": len(words),
        "char_count": len(clean),
        "is_question": is_q,
        "opener": opener,
    }


def analyze_thumbnail_image(img_bytes: bytes) -> dict[str, Any]:
    """Deterministic phone-size (168x94) thumbnail pixel metrics: grade and estimated subject fill %."""
    if Image is None:
        return {"grade": "unknown", "frame_fill_pct_168px": None, "mean_luma": None, "mean_saturation": None}
    with Image.open(io.BytesIO(img_bytes)) as im:
        rgb = im.convert("RGB").resize((168, 94))
        gray = rgb.convert("L")
        hsv = rgb.convert("HSV")
        mean_luma = round(float(ImageStat.Stat(gray).mean[0]), 1)
        mean_sat = round(float(ImageStat.Stat(hsv).mean[1]), 1)
        if mean_luma >= 125.0:
            grade = "bright"
        elif mean_luma >= 70.0:
            grade = "normal"
        else:
            grade = "dark"
        # Estimate foreground / salient subject area at 168x94 by comparing local contrast/edge + colour delta vs border.
        edges = gray.filter(ImageFilter.FIND_EDGES)
        px_e = list(edges.get_flattened_data() if hasattr(edges, "get_flattened_data") else edges.getdata())
        px_rgb = list(rgb.get_flattened_data() if hasattr(rgb, "get_flattened_data") else rgb.getdata())
        w, h = rgb.size
        border = [
            px_rgb[y * w + x]
            for y in range(h)
            for x in range(w)
            if y < 6 or y >= h - 6 or x < 6 or x >= w - 6
        ]
        bg_r = sum(p[0] for p in border) / max(len(border), 1)
        bg_g = sum(p[1] for p in border) / max(len(border), 1)
        bg_b = sum(p[2] for p in border) / max(len(border), 1)
        fg = 0
        for e_val, (r, g, b) in zip(px_e, px_rgb):
            dist = abs(r - bg_r) + abs(g - bg_g) + abs(b - bg_b)
            if e_val >= 28 or dist >= 95:
                fg += 1
        fill_pct = round(100.0 * fg / max(w * h, 1), 1)
        return {
            "grade": grade,
            "frame_fill_pct_168px": fill_pct,
            "mean_luma": mean_luma,
            "mean_saturation": mean_sat,
        }


def fetch_thumbnail_bytes(url: str) -> bytes | None:
    if not url or not url.startswith("https://"):
        return None
    req = urllib.request.Request(url, headers={"User-Agent": "studio-market-tracker/1"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read()
    except (OSError, urllib.error.URLError):
        return None


def tag_thumbnail(
    thumb_url: str,
    vision_fn: Callable[[bytes, str], dict[str, Any]] | None = None,
    fetcher: Callable[[str], bytes | None] = fetch_thumbnail_bytes,
) -> dict[str, Any]:
    """Tag a breakout thumbnail from its image URL (image analysis only, never opens video)."""
    result: dict[str, Any] = {
        "thumbnail_url": thumb_url,
        "main_subject": None,
        "frame_fill_pct_168px": None,
        "words_on_thumb": None,
        "has_face": None,
        "grade": "unknown",
        "vision_tagged": False,
    }
    raw = fetcher(thumb_url)
    if not raw:
        return result
    metrics = analyze_thumbnail_image(raw)
    result.update({k: v for k, v in metrics.items() if v is not None})
    if vision_fn is not None:
        vdata = vision_fn(raw, thumb_url) or {}
        for k in ("main_subject", "frame_fill_pct_168px", "words_on_thumb", "has_face", "grade"):
            if k in vdata and vdata[k] is not None:
                result[k] = vdata[k]
        result["vision_tagged"] = True
    return result


def suggest_angle(breakout: dict[str, Any]) -> str:
    """One concrete angle line tailored to the matching channel's format and rules."""
    niche = breakout.get("niche", "")
    title = str(breakout.get("title") or "").strip()
    short_topic = re.sub(r"\s*[\|\-—:]\s*.*$", "", title).strip()
    if len(short_topic) > 48:
        short_topic = " ".join(short_topic.split()[:7])
    fmt = breakout.get("format", "long")
    if niche == "ww2":
        if fmt == "short":
            return f"Field Order Short: 45s archive-photo engineering fact on '{short_topic}', linked to a matching long."
        return f"Field Order long: archive-photo + code-map engineering/logistics breakdown of '{short_topic}' (searched name first, <=50 chars, distinct wording)."
    if niche == "owb":
        if fmt == "short":
            return f"Orbit Short: 22-27s wonder-led question on '{short_topic}', real space imagery at frame 0 (no Orbit at 0:00)."
        return f"Orbit long: real NASA/ESA + animated data-scale explainer on '{short_topic}' (searched phrase first, wonder not dread)."
    if fmt == "short":
        return f"HOS Short: 16-19s 3D cartoon apparatus hook on '{short_topic}', looping last line into first."
    return f"HOS long: 3D cartoon discovery story + proof apparatus behind '{short_topic}' (searched name first, adult US/UK framing)."


def summarize_patterns(breakouts: list[dict[str, Any]]) -> dict[str, Any]:
    """Build compact 'patterns this week' summary from tagged breakouts."""
    n = len(breakouts)
    if n == 0:
        return {
            "count": 0,
            "title_openers": [],
            "thumbnail_traits": [],
            "avg_word_count": 0.0,
            "pct_searched_name": 0.0,
            "pct_how_why": 0.0,
            "pct_has_number": 0.0,
        }
    openers: collections.Counter[str] = collections.Counter()
    grades: collections.Counter[str] = collections.Counter()
    searched = how_why = has_num = faces = face_checked = 0
    word_counts: list[int] = []
    fills: list[float] = []
    for b in breakouts:
        tt = b.get("title_tags") or tag_title(b.get("title", ""), b.get("niche", ""))
        openers[tt.get("opener", "other")] += 1
        if tt.get("starts_with_searched_name"):
            searched += 1
        if tt.get("how_why_opener"):
            how_why += 1
        if tt.get("has_number"):
            has_num += 1
        word_counts.append(int(tt.get("word_count", 0) or 0))
        th = b.get("thumb_tags") or {}
        if th.get("grade") and th.get("grade") != "unknown":
            grades[str(th["grade"])] += 1
        if th.get("frame_fill_pct_168px") is not None:
            fills.append(float(th["frame_fill_pct_168px"]))
        if th.get("has_face") is not None:
            face_checked += 1
            if th["has_face"]:
                faces += 1

    opener_labels = {
        "searched_name": "Searched subject first",
        "how_why": "How / Why opener",
        "what_when": "What / When opener",
        "number": "Number opener",
        "other": "Other opener",
    }
    title_openers = [
        {"key": k, "label": opener_labels.get(k, k), "count": c, "pct": round(100.0 * c / n, 1)}
        for k, c in openers.most_common()
    ]
    thumb_traits: list[dict[str, Any]] = []
    for g, c in grades.most_common():
        thumb_traits.append({"label": f"{g.capitalize()} grade", "count": c, "pct": round(100.0 * c / n, 1)})
    if fills:
        thumb_traits.append({"label": f"Avg 168px subject fill {round(sum(fills)/len(fills), 1)}%", "count": len(fills), "pct": None})
    if face_checked:
        thumb_traits.append({"label": f"Face present ({faces}/{face_checked})", "count": faces, "pct": round(100.0 * faces / face_checked, 1)})

    return {
        "count": n,
        "title_openers": title_openers,
        "thumbnail_traits": thumb_traits,
        "avg_word_count": round(sum(word_counts) / n, 1),
        "pct_searched_name": round(100.0 * searched / n, 1),
        "pct_how_why": round(100.0 * how_why / n, 1),
        "pct_has_number": round(100.0 * has_num / n, 1),
    }


def rollup_daily_snapshots(
    daily_dir: pathlib.Path = DAILY_DIR,
    weekly_dir: pathlib.Path = WEEKLY_DIR,
    today: dt.date | None = None,
    keep_days: int = DAILY_RETENTION_DAYS,
) -> list[pathlib.Path]:
    """Fold daily snapshot JSON files older than `keep_days` into compact ISO-week rollup JSONs."""
    today = today or utc_now().date()
    cutoff = today - dt.timedelta(days=keep_days)
    if not daily_dir.is_dir():
        return []
    groups: dict[str, list[tuple[dt.date, pathlib.Path]]] = collections.defaultdict(list)
    for path in sorted(daily_dir.glob("*.json")):
        try:
            d = dt.date.fromisoformat(path.stem)
        except ValueError:
            continue
        if d < cutoff:
            iso_yr, iso_wk, _ = d.isocalendar()
            groups[f"{iso_yr}-W{iso_wk:02d}"].append((d, path))

    written: list[pathlib.Path] = []
    weekly_dir.mkdir(parents=True, exist_ok=True)
    for wk, entries in sorted(groups.items()):
        rollup_path = weekly_dir / f"rollup-{wk}.json"
        existing: dict[str, Any] = {}
        if rollup_path.is_file():
            try:
                existing = json.loads(rollup_path.read_text())
            except (OSError, ValueError):
                existing = {}
        days_seen = set(existing.get("days") or [])
        by_vid: dict[str, dict[str, Any]] = {
            b["video_id"]: b for b in (existing.get("breakouts") or []) if b.get("video_id")
        }
        farms_seen: dict[str, dict[str, Any]] = {
            f["video_id"]: f for f in (existing.get("farms") or []) if f.get("video_id")
        }
        quota_total = int(existing.get("quota_units_total", 0) or 0)
        for d, p in entries:
            ds = d.isoformat()
            try:
                doc = json.loads(p.read_text())
            except (OSError, ValueError):
                continue
            if ds not in days_seen:
                days_seen.add(ds)
                quota_total += int((doc.get("quota") or {}).get("used", 0) or 0)
            for b in doc.get("breakouts") or []:
                vid = b.get("video_id")
                if not vid:
                    continue
                prev = by_vid.get(vid)
                if not prev or int(b.get("views", 0) or 0) >= int(prev.get("views", 0) or 0):
                    by_vid[vid] = b
            for f in doc.get("farms") or []:
                vid = f.get("video_id")
                if vid:
                    farms_seen[vid] = f
            p.unlink(missing_ok=True)

        merged = {
            "schema_version": 1,
            "week": wk,
            "rolled_up_at": iso_utc(utc_now()),
            "days": sorted(days_seen),
            "quota_units_total": quota_total,
            "breakout_count": len(by_vid),
            "farm_count": len(farms_seen),
            "breakouts": sorted(
                by_vid.values(),
                key=lambda x: (0 if x.get("format") == "long" else 1, -(x.get("multiple") or 0), -(x.get("views") or 0)),
            ),
            "farms": list(farms_seen.values()),
        }
        rollup_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n")
        written.append(rollup_path)
    return written


def write_weekly_report(
    breakouts: list[dict[str, Any]],
    out_path: pathlib.Path,
    report_date: str,
    patterns: dict[str, Any],
) -> pathlib.Path:
    """Write `05_Analytics/market/weekly/<date>.md` with top breakouts per niche and angle lines."""
    lines = [
        f"# Market Intelligence Weekly Digest ({report_date})",
        "",
        f"- **Breakouts tracked (last 7 days):** {len(breakouts)} (long-form first; AI content farms excluded)",
        f"- **Title patterns:** {patterns.get('pct_searched_name', 0)}% searched subject first · "
        f"{patterns.get('pct_how_why', 0)}% How/Why opener · "
        f"{patterns.get('pct_has_number', 0)}% contain a number · "
        f"avg {patterns.get('avg_word_count', 0)} words",
        "",
    ]
    if patterns.get("thumbnail_traits"):
        traits = " · ".join(
            f"{t['label']} ({t['pct']}%)" if t.get("pct") is not None else t["label"]
            for t in patterns["thumbnail_traits"]
        )
        lines.append(f"- **Thumbnail traits (168 px phone read):** {traits}")
        lines.append("")

    for niche in ("ww2", "owb", "hos"):
        meta = NICHE_META[niche]
        items = [b for b in breakouts if b.get("niche") == niche]
        items.sort(key=lambda x: (0 if x.get("format") == "long" else 1, -(x.get("multiple") or 0), -(x.get("views") or 0)))
        lines.append(f"## {meta['label']} ({meta['channel']})")
        lines.append("")
        if not items:
            lines.append("_No verified non-farm breakouts crossed the threshold in the last 7 days._")
            lines.append("")
            continue
        for b in items[:15]:
            tt = b.get("title_tags") or tag_title(b.get("title", ""), niche)
            th = b.get("thumb_tags") or {}
            mult = f"{b['multiple']:.1f}x" if b.get("multiple") is not None else "n/a"
            fmt = "Long" if b.get("format") == "long" else "Short"
            subs = f"{int(b.get('channel_subscribers', 0)):,}"
            fill = f"{th['frame_fill_pct_168px']}%" if th.get("frame_fill_pct_168px") is not None else "n/a"
            face = "yes" if th.get("has_face") is True else ("no" if th.get("has_face") is False else "untagged")
            lines.extend([
                f"### {b.get('title', '')} (`{b.get('video_id', '')}`)",
                f"- **Channel:** {b.get('channel_title', '')} ({subs} subs · {b.get('channel_tier', 'benchmark')}) · "
                f"**{fmt}** · **{int(b.get('views', 0)):,} views** ({b.get('views_per_hour', 0):,.0f}/hr · **{mult}** median · {b.get('age_hours', 0)}h old)",
                f"- **Title tags:** opener=`{tt.get('opener')}` · searched_name={tt.get('starts_with_searched_name')} · "
                f"how_why={tt.get('how_why_opener')} · number={tt.get('has_number')} · {tt.get('word_count')} words",
                f"- **Thumbnail (168 px):** grade=`{th.get('grade', 'unknown')}` · fill={fill} · "
                f"face={face} · words={th.get('words_on_thumb') if th.get('words_on_thumb') is not None else 'untagged'} · "
                f"subject={th.get('main_subject') or 'untagged'}",
                f"- **The angle we could take:** {b.get('angle') or suggest_angle(b)}",
                "",
            ])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines).rstrip() + "\n")
    return out_path


def build_board_payload(
    watchlist: dict[str, Any],
    breakouts: list[dict[str, Any]],
    farms: list[dict[str, Any]],
    generated_at: str,
    weekly_md_rel: str | None = None,
    quota: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compact JSON published via board_publish.py -> board.json['market'] for the Studio Market tab."""
    ordered = sorted(
        breakouts,
        key=lambda x: (0 if x.get("format") == "long" else 1, -(x.get("multiple") or 0), -(x.get("views_per_hour") or 0)),
    )
    items = []
    for b in ordered[:60]:
        tt = b.get("title_tags") or tag_title(b.get("title", ""), b.get("niche", ""))
        th = b.get("thumb_tags") or {}
        items.append({
            "videoId": b.get("video_id", ""),
            "niche": b.get("niche", ""),
            "format": b.get("format", "long"),
            "title": b.get("title", ""),
            "thumbnail": b.get("thumbnail_url", ""),
            "channel": b.get("channel_title", ""),
            "channelId": b.get("channel_id", ""),
            "subscribers": int(b.get("channel_subscribers", 0) or 0),
            "tier": b.get("channel_tier", "benchmark"),
            "publishedAt": b.get("published_at", ""),
            "ageHours": b.get("age_hours", 0),
            "views": int(b.get("views", 0) or 0),
            "viewsPerHour": b.get("views_per_hour", 0),
            "channelMedian": b.get("channel_median", 0),
            "multiple": b.get("multiple"),
            "reasons": b.get("breakout_reasons") or [],
            "angle": b.get("angle") or suggest_angle(b),
            "titleTags": {
                "opener": tt.get("opener", "other"),
                "searchedName": bool(tt.get("starts_with_searched_name")),
                "howWhy": bool(tt.get("how_why_opener")),
                "number": bool(tt.get("has_number")),
                "words": int(tt.get("word_count", 0) or 0),
            },
            "thumbTags": {
                "grade": th.get("grade", "unknown"),
                "fillPct": th.get("frame_fill_pct_168px"),
                "words": th.get("words_on_thumb"),
                "hasFace": th.get("has_face"),
                "subject": th.get("main_subject"),
            },
        })
    patterns = summarize_patterns(ordered)
    channels = watchlist.get("channels") or []
    by_niche = {
        n: {
            "label": NICHE_META[n]["label"],
            "channel": NICHE_META[n]["channel"],
            "watchlist": sum(1 for c in channels if c.get("niche") == n),
            "rising": sum(1 for c in channels if c.get("niche") == n and c.get("tier") == "rising"),
            "breakouts": sum(1 for x in items if x["niche"] == n),
        }
        for n in ("ww2", "owb", "hos")
    }
    return {
        "schemaVersion": 1,
        "updatedAt": generated_at,
        "watchlistTotal": len(channels),
        "farmFilteredCount": len(farms),
        "weeklyReport": weekly_md_rel or "",
        "quota": quota or {},
        "niches": by_niche,
        "patterns": patterns,
        "breakouts": items,
    }


def load_recent_breakouts(
    daily_dir: pathlib.Path = DAILY_DIR,
    days: int = 7,
    today: dt.date | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Load unique breakouts and farms across the last `days` daily snapshots (latest stats win)."""
    today = today or utc_now().date()
    cutoff = today - dt.timedelta(days=days - 1)
    by_vid: dict[str, dict[str, Any]] = {}
    farms_by_vid: dict[str, dict[str, Any]] = {}
    if not daily_dir.is_dir():
        return [], []
    for p in sorted(daily_dir.glob("*.json")):
        try:
            d = dt.date.fromisoformat(p.stem)
        except ValueError:
            continue
        if d < cutoff:
            continue
        try:
            doc = json.loads(p.read_text())
        except (OSError, ValueError):
            continue
        for b in doc.get("breakouts") or []:
            vid = b.get("video_id")
            if vid:
                by_vid[vid] = b
        for f in doc.get("farms") or []:
            vid = f.get("video_id")
            if vid:
                farms_by_vid[vid] = f
    return list(by_vid.values()), list(farms_by_vid.values())


def run_daily(
    watchlist_path: pathlib.Path = WATCHLIST_PATH,
    market_dir: pathlib.Path = MARKET_DIR,
    client: Any = None,
    now: dt.datetime | None = None,
    env_path: pathlib.Path = DEFAULT_ENV_PATH,
) -> dict[str, Any]:
    """Run the daily read-only YouTube Data API sweep within the 1,500-unit quota cap."""
    now = now or utc_now()
    today_str = now.date().isoformat()
    daily_dir = market_dir / "daily"
    weekly_dir = market_dir / "weekly"
    state_path = market_dir / "state.json"
    farms_path = market_dir / "farms.json"
    quota_path = market_dir / "quota.json"
    board_path = market_dir / "board.json"

    watchlist = json.loads(watchlist_path.read_text())
    channels = watchlist.get("channels") or []
    quota = QuotaGuard(daily_cap=DAILY_QUOTA_CAP, allow_search=False, state_path=quota_path, today=today_str)
    yt = client or YouTubeDataClient(quota=quota, env_path=env_path)

    state: dict[str, Any] = {}
    if state_path.is_file():
        try:
            state = json.loads(state_path.read_text())
        except (OSError, ValueError):
            state = {}
    tracked: dict[str, dict[str, Any]] = dict(state.get("tracked_videos") or {})
    channel_medians: dict[str, float] = dict(state.get("channel_medians") or {})
    farm_registry: dict[str, dict[str, Any]] = {}
    if farms_path.is_file():
        try:
            raw_farms = json.loads(farms_path.read_text())
            farm_registry = {f["video_id"]: f for f in (raw_farms.get("videos") or []) if f.get("video_id")}
        except (OSError, ValueError):
            farm_registry = {}

    # 1. Refresh subscriber counts in batches of 50 (2 units for ~90 channels).
    by_cid = {c["id"]: dict(c) for c in channels if c.get("id")}
    if quota.remaining >= 4:
        for it in yt.channels_by_ids(list(by_cid.keys())):
            cid = it.get("id")
            if cid in by_cid:
                st = it.get("statistics") or {}
                if st.get("subscriberCount") is not None:
                    by_cid[cid]["subscribers"] = int(st["subscriberCount"])
                uploads = ((it.get("contentDetails") or {}).get("relatedPlaylists") or {}).get("uploads")
                if uploads:
                    by_cid[cid]["uploads_playlist"] = uploads

    # 2. Read each channel's uploads playlist (1 unit/channel) to collect last 25 uploads.
    playlist_vids_by_ch: dict[str, list[str]] = {}
    all_vids_needed: list[str] = []
    for cid, ch in by_cid.items():
        pl = ch.get("uploads_playlist")
        if not pl or quota.remaining <= 10:
            continue
        try:
            items = yt.playlist_items(pl, max_results=25)
        except (OSError, urllib.error.URLError, QuotaError):
            continue
        vids = []
        for it in items:
            vid = (it.get("contentDetails") or {}).get("videoId")
            if vid:
                vids.append(vid)
                all_vids_needed.append(vid)
        playlist_vids_by_ch[cid] = vids

    # Also keep polling any tracked videos still inside the 96h snapshot window.
    for vid, rec in list(tracked.items()):
        pub = parse_iso_utc(rec.get("published_at"))
        if pub and (now - pub).total_seconds() / 3600.0 <= TRACK_WINDOW_HOURS:
            all_vids_needed.append(vid)
        else:
            tracked.pop(vid, None)

    # 3. Fetch video stats in batches of 50 (1 unit per 50 videos).
    video_map: dict[str, dict[str, Any]] = {}
    unique_vids = list(dict.fromkeys(all_vids_needed))
    max_batches = max(0, quota.remaining)
    capped_vids = unique_vids[: max_batches * 50]
    for it in yt.videos_by_ids(capped_vids):
        vid = it.get("id")
        if not vid:
            continue
        sn = it.get("snippet") or {}
        st = it.get("statistics") or {}
        cd = it.get("contentDetails") or {}
        thumbs = sn.get("thumbnails") or {}
        thumb_url = (
            (thumbs.get("high") or {}).get("url")
            or (thumbs.get("medium") or {}).get("url")
            or f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
        )
        video_map[vid] = {
            "video_id": vid,
            "channel_id": sn.get("channelId", ""),
            "title": sn.get("title", ""),
            "published_at": sn.get("publishedAt", ""),
            "duration_s": parse_iso_duration(cd.get("duration")),
            "views": int(st.get("viewCount", 0) or 0),
            "likes": int(st["likeCount"]) if st.get("likeCount") is not None else None,
            "thumbnail_url": thumb_url,
        }

    # 4. Compute per-channel median of last 20 long uploads & evaluate recent uploads.
    breakouts_today: list[dict[str, Any]] = []
    farms_today: list[dict[str, Any]] = []
    recent_checked = 0

    for cid, ch in by_cid.items():
        ch_videos = [video_map[v] for v in playlist_vids_by_ch.get(cid, []) if v in video_map]
        med = channel_long_median(ch_videos, limit=20)
        if med > 0:
            channel_medians[cid] = med
        ch["median_long_views"] = channel_medians.get(cid, 0.0)

        for v in ch_videos:
            pub = parse_iso_utc(v.get("published_at"))
            if not pub:
                continue
            age_h = max(0.0, (now - pub).total_seconds() / 3600.0)
            if age_h > TRACK_WINDOW_HOURS:
                continue
            recent_checked += 1
            vid = v["video_id"]
            rec = tracked.get(vid) or {"published_at": v["published_at"], "channel_id": cid, "snapshots": {}}
            bucket = snapshot_bucket(age_h)
            if bucket and bucket not in rec["snapshots"]:
                rec["snapshots"][bucket] = {"at": iso_utc(now), "age_hours": round(age_h, 1), "views": v["views"]}
            tracked[vid] = rec

            scored = evaluate_breakout(v, ch, age_h, rec["snapshots"])
            if scored["is_farm"]:
                compact_farm = {
                    "video_id": vid,
                    "channel_id": cid,
                    "channel_title": ch.get("title", ""),
                    "niche": ch.get("niche", ""),
                    "title": scored["title"],
                    "reason": scored["farm_reason"],
                    "views": scored["views"],
                    "like_ratio": scored["like_ratio"],
                }
                farms_today.append(compact_farm)
                farm_registry[vid] = {**compact_farm, "seen_at": iso_utc(now)}
            elif scored["is_breakout"]:
                scored["title_tags"] = tag_title(scored["title"], scored["niche"])
                scored["angle"] = suggest_angle(scored)
                breakouts_today.append(scored)

    breakouts_today.sort(
        key=lambda x: (0 if x["format"] == "long" else 1, -(x.get("multiple") or 0), -(x.get("views_per_hour") or 0))
    )
    quota.save()

    # 5. Persist compact daily snapshot, state, farms registry, weekly roll-up & board payload.
    daily_dir.mkdir(parents=True, exist_ok=True)
    daily_doc = {
        "schema_version": 1,
        "date": today_str,
        "generated_at": iso_utc(now),
        "channels_scanned": len(playlist_vids_by_ch),
        "recent_videos_checked": recent_checked,
        "quota": quota.summary(),
        "breakouts": breakouts_today,
        "farms": farms_today,
    }
    (daily_dir / f"{today_str}.json").write_text(json.dumps(daily_doc, indent=2, ensure_ascii=False) + "\n")

    state_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "updated_at": iso_utc(now),
                "channel_medians": channel_medians,
                "tracked_videos": tracked,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )

    # Keep latest 200 farm records in farms.json so it never bloats.
    kept_farms = sorted(farm_registry.values(), key=lambda x: str(x.get("seen_at") or ""), reverse=True)[:200]
    farms_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "updated_at": iso_utc(now),
                "note": "Excluded from breakouts and never used as packaging models.",
                "videos": kept_farms,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )

    rollup_daily_snapshots(daily_dir=daily_dir, weekly_dir=weekly_dir, today=now.date())

    week_breakouts, week_farms = load_recent_breakouts(daily_dir=daily_dir, days=7, today=now.date())
    existing_weekly = sorted(weekly_dir.glob("20*.md"))
    latest_weekly_rel = f"05_Analytics/market/weekly/{existing_weekly[-1].name}" if existing_weekly else ""
    board_doc = build_board_payload(
        watchlist=watchlist,
        breakouts=week_breakouts,
        farms=week_farms,
        generated_at=iso_utc(now),
        weekly_md_rel=latest_weekly_rel,
        quota=quota.summary(),
    )
    board_path.write_text(json.dumps(board_doc, indent=2, ensure_ascii=False) + "\n")
    return daily_doc


def run_weekly(
    watchlist_path: pathlib.Path = WATCHLIST_PATH,
    market_dir: pathlib.Path = MARKET_DIR,
    now: dt.datetime | None = None,
    vision_fn: Callable[[bytes, str], dict[str, Any]] | None = None,
    fetcher: Callable[[str], bytes | None] = fetch_thumbnail_bytes,
) -> pathlib.Path:
    """Tag last 7 days' breakouts (title + 168px thumbnail analysis) and write weekly/<date>.md + board.json."""
    now = now or utc_now()
    today_str = now.date().isoformat()
    daily_dir = market_dir / "daily"
    weekly_dir = market_dir / "weekly"
    board_path = market_dir / "board.json"
    quota_path = market_dir / "quota.json"

    watchlist = json.loads(watchlist_path.read_text())
    breakouts, farms = load_recent_breakouts(daily_dir=daily_dir, days=7, today=now.date())
    tagged: list[dict[str, Any]] = []
    for b in breakouts:
        item = dict(b)
        item["title_tags"] = tag_title(item.get("title", ""), item.get("niche", ""))
        item["thumb_tags"] = tag_thumbnail(item.get("thumbnail_url", ""), vision_fn=vision_fn, fetcher=fetcher)
        item["angle"] = suggest_angle(item)
        tagged.append(item)

    patterns = summarize_patterns(tagged)
    out_md = weekly_dir / f"{today_str}.md"
    write_weekly_report(tagged, out_md, today_str, patterns)

    quota_summary: dict[str, Any] = {}
    if quota_path.is_file():
        try:
            qdoc = json.loads(quota_path.read_text())
            days = qdoc.get("days") or {}
            if days:
                last_day = sorted(days.keys())[-1]
                quota_summary = {"date": last_day, **days[last_day]}
        except (OSError, ValueError):
            pass

    board_doc = build_board_payload(
        watchlist=watchlist,
        breakouts=tagged,
        farms=farms,
        generated_at=iso_utc(now),
        weekly_md_rel=f"05_Analytics/market/weekly/{today_str}.md",
        quota=quota_summary,
    )
    board_path.write_text(json.dumps(board_doc, indent=2, ensure_ascii=False) + "\n")
    return out_md


def monthly_discovery_plan(
    watchlist: dict[str, Any],
    out_dir: pathlib.Path = PROPOSALS_DIR,
    month_str: str | None = None,
    credit_budget: int = MONTHLY_VIDIQ_CAP,
    farms_path: pathlib.Path = FARMS_PATH,
    vidiq_fn: Callable[[str, int], list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """First-Monday monthly discovery sweep capped strictly at <= 40 vidIQ credits (never buys credits)."""
    if credit_budget > MONTHLY_VIDIQ_CAP or credit_budget < 0:
        raise ValueError(f"Monthly vidIQ discovery budget must be 0..{MONTHLY_VIDIQ_CAP} credits, got {credit_budget}")
    month_str = month_str or utc_now().strftime("%Y-%m")
    channels = watchlist.get("channels") or []

    # Identify swap-out candidates (channels repeatedly appearing in farms.json or very low upload count).
    farm_counts: collections.Counter[str] = collections.Counter()
    if farms_path.is_file():
        try:
            for f in (json.loads(farms_path.read_text()).get("videos") or []):
                if f.get("channel_id"):
                    farm_counts[f["channel_id"]] += 1
        except (OSError, ValueError):
            pass

    drop_candidates = [
        {
            "id": c["id"],
            "title": c.get("title", ""),
            "niche": c.get("niche", ""),
            "reason": f"farm_flags={farm_counts[c['id']]}" if farm_counts[c["id"]] >= 2 else "stale_or_inactive",
        }
        for c in channels
        if farm_counts[c["id"]] >= 2 or int(c.get("video_count", 0) or 0) < 3
    ]

    # Allocate <= 40 vidIQ credits across the three niches (15 ww2 / 15 owb / 10 hos, scaled to credit_budget).
    base_alloc = [("ww2", 15), ("owb", 15), ("hos", 10)]
    alloc: dict[str, int] = {}
    remaining = credit_budget
    for niche, want in base_alloc:
        take = min(want, remaining)
        alloc[niche] = take
        remaining -= take

    credits_used = 0
    proposals: list[dict[str, Any]] = []
    for niche, cap in alloc.items():
        if cap <= 0:
            continue
        if vidiq_fn is not None:
            found = vidiq_fn(niche, cap) or []
            for cand in found:
                cost = int(cand.get("credits_used", 0) or 0)
                if credits_used + cost > credit_budget:
                    break
                credits_used += cost
                proposals.append({**cand, "niche": niche})
        else:
            # Record exact bounded query plan for the vidIQ MCP session (0 credits spent here).
            proposals.append({
                "niche": niche,
                "status": "planned_for_vidiq_mcp",
                "credit_cap": cap,
                "calls": [
                    f"vidiq_outliers (niche={niche}, maxSubs=20000, minMultiple=5, 5 credits)",
                    f"vidiq_similar_channels (top rising {niche} channel, 5 credits)",
                ],
            })

    doc = {
        "schema_version": 1,
        "month": month_str,
        "generated_at": iso_utc(utc_now()),
        "credit_budget": credit_budget,
        "credits_used": credits_used,
        "never_buy_credits": True,
        "allocation": alloc,
        "drop_candidates": drop_candidates,
        "proposals": proposals,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{month_str}.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")

    md_lines = [
        f"# Monthly Watchlist Discovery Proposal ({month_str})",
        "",
        f"- **vidIQ credit budget:** {credits_used} / {credit_budget} credits used (hard cap {MONTHLY_VIDIQ_CAP}; never buy credits).",
        f"- **Allocation:** WW2 {alloc.get('ww2', 0)} cr · Space {alloc.get('owb', 0)} cr · History of Science {alloc.get('hos', 0)} cr.",
        "",
        "## Channels flagged for swap-out review",
        "",
    ]
    if not drop_candidates:
        md_lines.append("_None flagged this month._")
    else:
        for d in drop_candidates:
            md_lines.append(f"- `{d['id']}` **{d['title']}** ({d['niche']}): {d['reason']}")
    md_lines.extend(["", "## Discovery sweep / proposed additions", ""])
    for p in proposals:
        if p.get("status") == "planned_for_vidiq_mcp":
            md_lines.append(f"- **{NICHE_META[p['niche']]['label']}** (cap {p['credit_cap']} cr): " + "; ".join(p["calls"]))
        else:
            md_lines.append(f"- **{p.get('niche')}** · `{p.get('id', '')}` **{p.get('title', '')}** ({p.get('subscribers', '?')} subs)")
    (out_dir / f"{month_str}.md").write_text("\n".join(md_lines).rstrip() + "\n")
    return doc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("daily", help="Run daily Data API tracking sweep (<= 1,500 units, no search.list)")
    sub.add_parser("weekly", help="Tag last 7 days' breakouts and write weekly markdown + board.json")
    disc = sub.add_parser("discover", help="Monthly vidIQ discovery proposal (<= 40 credits)")
    disc.add_argument("--budget", type=int, default=MONTHLY_VIDIQ_CAP)
    sub.add_parser("rollup", help="Roll up daily snapshots older than 14 days into weekly JSONs")
    args = ap.parse_args(argv)

    if args.cmd == "daily":
        res = run_daily()
        print(
            f"market daily {res['date']}: scanned={res['channels_scanned']} "
            f"recent={res['recent_videos_checked']} breakouts={len(res['breakouts'])} "
            f"farms={len(res['farms'])} quota={res['quota']['used']}/{res['quota']['cap']}"
        )
        return 0
    if args.cmd == "weekly":
        out = run_weekly()
        print(f"market weekly wrote {out}")
        return 0
    if args.cmd == "discover":
        wl = json.loads(WATCHLIST_PATH.read_text())
        doc = monthly_discovery_plan(wl, credit_budget=args.budget)
        print(f"market discover {doc['month']}: credits={doc['credits_used']}/{doc['credit_budget']} drops={len(doc['drop_candidates'])}")
        return 0
    if args.cmd == "rollup":
        rolled = rollup_daily_snapshots()
        print(f"market rollup: updated {len(rolled)} weekly files")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
