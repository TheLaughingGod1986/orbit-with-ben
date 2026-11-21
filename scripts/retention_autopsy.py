#!/usr/bin/env python3
"""Retention autopsy for long videos at 48 h and 7 days across all studio channels.

Ben, 20 Nov 2026 ("if these films do bad how are we analysing the videos to improve them going forward, like RSI";
J3256): score every long against the channel's own median at the same age and against the niche's small-channel
outliers from search research, diagnose the funnel in strict order (showings -> click-through -> 0:30 hook ->
mid-film cliffs -> end screen/handoff), extract 40 s watch clips (20 s either side of the three steepest retention
drops) for Gemini 4 Neon to watch with moving video + audio, and produce the structured autopsy report.

    python3 scripts/retention_autopsy.py inspect <video_id> --window 48h|7d [--channel owb|hos|ww2]
    python3 scripts/retention_autopsy.py clips <video_id> --video <mp4> --out-dir <dir> [--window 48h|7d]

Read-only on YouTube and snapshots. £0.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import statistics
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import channels  # noqa: E402
import launch_check as lc  # noqa: E402
import studio  # noqa: E402

WINDOW_HOURS = {"48h": 48, "7d": 168}
WINDOW_AGE_BOUNDS = {"48h": (36.0, 72.0), "7d": (144.0, 204.0)}
MIN_BASELINE_N = 3
DROP_WINDOW_HALF_S = 20.0
DROP_MIN_GAP_S = 40.0

# Niche small-channel (<50k subs) outlier benchmarks grounded in repo search research:
# - owb: 05_Analytics/new_channel_research/SUMMARY.md (Stellar 29.2k median 4,964v, Simple Science 3.9k 1,631v,
#   Science Into Sleep 1.4k 1,323v, Orbitra 21k-38k) + LEARNINGS.md rules 10, 23, 34, 37.
# - hos: 05_Analytics/hos/search_research/2026-11-20.md (<50k outliers 1.5k-61.9k, Industrial Case Files 138 subs
#   4.7k, Counter Facts Lab 1.4k subs 1.5k) + HOS-2026-11-E2 (60% 0:30 retention bar).
# - ww2: ww2/00_Brand/PLAYBOOK.md (260-video vidIQ outlier study; 48h thresholds 1,000 impr / 3% CTR / 25% AVD) +
#   05_Analytics/new_channel_research/SUMMARY.md (WW2 Dossier 14.3k median 1,058v, WW2 Combat Files 3.6k 736v).
NICHE_BENCHMARKS: dict[str, dict[str, float | str]] = {
    "owb": {
        "impressions_48h": 25000.0,
        "impressions_7d": 80000.0,
        "ctr": 4.0,
        "views_48h": 1500.0,
        "views_7d": 5000.0,
        "avg_pct": 35.0,
        "r30": 60.0,
        "subs_per_1k": 10.0,
        "source": "05_Analytics/new_channel_research/SUMMARY.md & LEARNINGS.md rules 10/23/34/37 (<50k space/science outliers)",
    },
    "hos": {
        "impressions_48h": 25000.0,
        "impressions_7d": 80000.0,
        "ctr": 4.0,
        "views_48h": 1500.0,
        "views_7d": 4700.0,
        "avg_pct": 35.0,
        "r30": 60.0,
        "subs_per_1k": 10.0,
        "source": "05_Analytics/hos/search_research/2026-11-20.md (<50k discovery/history outliers 1.5k-61.9k) & HOS-2026-11-E2",
    },
    "ww2": {
        "impressions_48h": 20000.0,
        "impressions_7d": 70000.0,
        "ctr": 4.5,
        "views_48h": 1000.0,
        "views_7d": 3500.0,
        "avg_pct": 35.0,
        "r30": 60.0,
        "subs_per_1k": 10.0,
        "source": "ww2/00_Brand/PLAYBOOK.md (260-video outlier study) & 05_Analytics/new_channel_research/SUMMARY.md (WW2 <50k peers)",
    },
}

METRIC_ORDER = (
    ("impressions", "Showings", ""),
    ("ctr", "CTR", "%"),
    ("views", "Views", ""),
    ("avg_pct", "Avg%", "%"),
    ("r30", "0:30", "%"),
    ("subs_per_1k", "Subs/1k", ""),
)


def rsi(value: float | int | None, benchmark: float | int | None) -> int | None:
    """Bounded 0-100 Relative Strength Index: 50 = on benchmark, >50 = stronger, <50 = weaker.

    Formula: RS = value / benchmark; RSI = round(100 * RS / (1 + RS)) = round(100 * value / (value + benchmark)).
    Returns None if either input is missing or benchmark <= 0.
    """
    if value is None or benchmark is None:
        return None
    if isinstance(value, bool) or isinstance(benchmark, bool):
        return None
    if benchmark <= 0 or value < 0:
        return None
    if value == 0:
        return 0
    return round(100.0 * value / (value + benchmark))


def rsi_arrow(score: int | None) -> str:
    """Visual momentum arrow matching trading RSI zones."""
    if score is None:
        return "—"
    if score >= 70:
        return "↑↑"
    if score >= 55:
        return "↑"
    if score >= 45:
        return "→"
    if score >= 31:
        return "↓"
    return "↓↓"


def fmt_rsi(score: int | None) -> str:
    return f"{score}{rsi_arrow(score)}" if score is not None else "—"


def fmt_mmss(seconds: float) -> str:
    s = max(0, int(round(seconds)))
    return f"{s // 60}:{s % 60:02d}"


def _med(values) -> float | None:
    clean = [float(v) for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]
    return round(statistics.median(clean), 2) if len(clean) >= MIN_BASELINE_N else None


def _retention_at(curve: list[dict], duration_s: float, target_s: float) -> float | None:
    if not curve or not duration_s or duration_s <= 0:
        return None
    pt = min(curve, key=lambda p: abs(float(p.get("at", 0.0)) * duration_s - target_s))
    w = pt.get("watching")
    return round(float(w) * 100.0, 1) if isinstance(w, (int, float)) else None


def _snapshot_doc(path: pathlib.Path) -> dict | None:
    try:
        doc = json.loads(path.read_text())
        return doc if isinstance(doc, dict) else None
    except (OSError, ValueError):
        return None


def _all_snapshots(slug: str) -> list[tuple[dt.datetime, dict]]:
    out = []
    snap_dir = channels.analytics_dir(slug) / "snapshots"
    if not snap_dir.is_dir():
        return out
    for p in sorted(snap_dir.glob("*.json")):
        doc = _snapshot_doc(p)
        if not doc:
            continue
        taken = doc.get("takenAt") or f"{doc.get('date') or p.stem}T06:40:00Z"
        try:
            out.append((studio.parse(taken), doc))
        except (ValueError, TypeError):
            continue
    return out


def _views_at_window(snapshots: list[tuple[dt.datetime, dict]], vid: str, pub: dt.datetime, window: str) -> int | None:
    lo, hi = WINDOW_AGE_BOUNDS[window]
    target = WINDOW_HOURS[window]
    best: tuple[float, int] | None = None
    for taken, doc in snapshots:
        age_h = (taken - pub).total_seconds() / 3600.0
        if not (lo <= age_h <= hi):
            continue
        row = next((v for v in doc.get("videos") or [] if v.get("id") == vid), None)
        if row and isinstance(row.get("views"), (int, float)):
            diff = abs(age_h - target)
            if best is None or diff < best[0]:
                best = (diff, int(row["views"]))
    return best[1] if best is not None else None


def niche_benchmark(slug: str, window: str) -> dict[str, float | str]:
    raw = NICHE_BENCHMARKS.get(slug) or NICHE_BENCHMARKS["owb"]
    return {
        "impressions": float(raw[f"impressions_{window}"]),
        "ctr": float(raw["ctr"]),
        "views": float(raw[f"views_{window}"]),
        "avg_pct": float(raw["avg_pct"]),
        "r30": float(raw["r30"]),
        "subs_per_1k": float(raw["subs_per_1k"]),
        "source": str(raw["source"]),
    }


def channel_baseline(slug: str, window: str, exclude_vid: str = "", before_iso: str = "") -> dict:
    """Channel's own median for longs at the same age, with lifetime fallback when <3 same-age readings exist."""
    hours = WINDOW_HOURS[window]
    snaps = _all_snapshots(slug)
    latest_doc = snaps[-1][1] if snaps else {}
    studio_ctr = (lc._json(channels.analytics_dir(slug) / "studio_ctr.json") or {}).get("videos") or {}
    an = latest_doc.get("analytics") or {}
    lt_map = an.get("lifetime") or {}
    ret_map = an.get("retention") or {}

    # 1. Same-age launch records (for impressions, ctr, views, avg_pct)
    same_age_rows = []
    for rec in lc.records(slug):
        if rec.get("format") != "long" or rec["id"] == exclude_vid:
            continue
        if before_iso and (rec.get("wentLive") or "") >= before_iso:
            continue
        for r in rec.get("readings") or []:
            if r.get("hours") == hours:
                same_age_rows.append(r)

    # 2. Historical snapshots at the same age (for views across all earlier longs)
    snap_views = []
    all_longs = [
        v for v in (latest_doc.get("videos") or [])
        if v.get("format") == "long" and v.get("privacy") == "public" and v.get("id") != exclude_vid
        and (not before_iso or (v.get("publishedAt") or "") < before_iso)
    ]
    for v in all_longs:
        if v.get("publishedAt"):
            try:
                pub = studio.parse(v["publishedAt"])
            except (ValueError, TypeError):
                continue
            vw = _views_at_window(snaps, v["id"], pub, window)
            if vw is not None:
                snap_views.append(vw)

    # 3. Lifetime studio_ctr / snapshot fallbacks (clearly noted in `basis`)
    lt_impr = [studio_ctr[v["id"]].get("impressions") for v in all_longs if v["id"] in studio_ctr]
    lt_ctr = [
        studio_ctr[v["id"]].get("impressionsCtr")
        for v in all_longs
        if v["id"] in studio_ctr and (studio_ctr[v["id"]].get("impressions") or 0) >= 10
    ]
    lt_avg = [
        (studio_ctr.get(v["id"]) or {}).get("avgViewPct") or (lt_map.get(v["id"]) or {}).get("avgViewPct")
        for v in all_longs
    ]
    lt_views = [v.get("views") for v in all_longs]
    lt_r30 = [
        _retention_at(ret_map.get(v["id"]) or [], float(v.get("seconds") or 0), 30.0)
        for v in all_longs
    ]
    lt_sp1k = []
    for v in all_longs:
        lt = lt_map.get(v["id"]) or {}
        vw = lt.get("views") or v.get("views") or 0
        if vw > 0 and lt.get("subs") is not None:
            lt_sp1k.append(round(float(lt["subs"]) * 1000.0 / float(vw), 2))

    def pick(same_vals, fallback_vals, same_label, fb_label):
        m = _med(same_vals)
        if m is not None:
            return m, f"{same_label} (n={len([x for x in same_vals if isinstance(x, (int, float))])})"
        m = _med(fallback_vals)
        if m is not None:
            return m, f"{fb_label} (n={len([x for x in fallback_vals if isinstance(x, (int, float))])})"
        return None, "insufficient history (<3 earlier longs)"

    impr, impr_b = pick([r.get("impressions") for r in same_age_rows], lt_impr, f"same-age {window} launch", "lifetime Studio longs")
    ctr, ctr_b = pick([r.get("ctr") for r in same_age_rows], lt_ctr, f"same-age {window} launch", "lifetime Studio longs")
    views, views_b = pick(snap_views or [r.get("views") for r in same_age_rows], lt_views, f"same-age {window} snapshots", "lifetime public longs")
    avg_pct, avg_b = pick([r.get("avgPct") for r in same_age_rows], lt_avg, f"same-age {window} launch", "lifetime Studio/YTA longs")
    r30, r30_b = pick([], lt_r30, f"same-age {window}", "lifetime YTA curves")
    sp1k, sp1k_b = pick([], lt_sp1k, f"same-age {window}", "lifetime YTA longs")

    return {
        "values": {
            "impressions": impr,
            "ctr": ctr,
            "views": views,
            "avg_pct": avg_pct,
            "r30": r30,
            "subs_per_1k": sp1k,
        },
        "basis": {
            "impressions": impr_b,
            "ctr": ctr_b,
            "views": views_b,
            "avg_pct": avg_b,
            "r30": r30_b,
            "subs_per_1k": sp1k_b,
        },
    }


def video_context(slug: str, vid: str, window: str) -> dict:
    """Gather all metrics, retention curve, traffic sources, and metadata for one long video."""
    snaps = _all_snapshots(slug)
    if not snaps:
        raise ValueError(f"No snapshots found for channel {slug}")
    taken, latest_doc = snaps[-1]
    video = next((v for v in latest_doc.get("videos") or [] if v.get("id") == vid), None)
    if not video:
        raise ValueError(f"Video {vid} not found in latest {slug} snapshot")
    an = latest_doc.get("analytics") or {}
    lt = (an.get("lifetime") or {}).get(vid) or {}
    sources = (an.get("sources") or {}).get(vid) or {}
    curve = (an.get("retention") or {}).get(vid) or []
    studio_ctr = ((lc._json(channels.analytics_dir(slug) / "studio_ctr.json") or {}).get("videos") or {}).get(vid) or {}
    launch_rec = lc.load_record(slug, vid) or {}
    hours = WINDOW_HOURS[window]
    launch_at_window = next((r for r in launch_rec.get("readings") or [] if r.get("hours") == hours), None)

    pub = studio.parse(video["publishedAt"]) if video.get("publishedAt") else taken
    age_h = round((taken - pub).total_seconds() / 3600.0, 1)
    duration_s = float(video.get("seconds") or 0)

    # Prefer exact-window launch reading for 48h where impressions/CTR are cleaner, else latest Studio/snapshot
    win_views = _views_at_window(snaps, vid, pub, window)
    views = (
        launch_at_window.get("views")
        if (window == "48h" and launch_at_window and launch_at_window.get("views") is not None)
        else (win_views if win_views is not None else video.get("views"))
    )
    impressions = (
        launch_at_window.get("impressions")
        if (window == "48h" and launch_at_window and launch_at_window.get("impressions") is not None)
        else studio_ctr.get("impressions")
    )
    ctr = (
        launch_at_window.get("ctr")
        if (window == "48h" and launch_at_window and launch_at_window.get("ctr") is not None)
        else studio_ctr.get("impressionsCtr")
    )
    avg_pct = studio_ctr.get("avgViewPct")
    if avg_pct is None:
        avg_pct = lt.get("avgViewPct")
    if avg_pct is None and launch_at_window:
        avg_pct = launch_at_window.get("avgPct")
    avg_sec = studio_ctr.get("avgViewSeconds") or lt.get("avgViewSeconds")

    r30 = _retention_at(curve, duration_s, 30.0)
    end_ret = _retention_at(curve, duration_s, duration_s)
    subs = lt.get("subs")
    lt_views = lt.get("views") or video.get("views") or 0
    subs_per_1k = round(float(subs) * 1000.0 / float(lt_views), 2) if (subs is not None and lt_views > 0) else None

    return {
        "channel": slug,
        "id": vid,
        "title": video.get("title") or vid,
        "published_at": video.get("publishedAt") or "",
        "snapshot_date": latest_doc.get("date") or "",
        "analytics_through": an.get("through") or "",
        "age_hours": age_h,
        "duration_s": duration_s,
        "window": window,
        "metrics": {
            "impressions": impressions,
            "ctr": ctr,
            "views": views,
            "avg_pct": round(float(avg_pct), 2) if avg_pct is not None else None,
            "r30": r30,
            "subs_per_1k": subs_per_1k,
        },
        "latest_studio": studio_ctr,
        "launch_reading": launch_at_window,
        "lifetime": lt,
        "sources": sources,
        "retention": curve,
        "avg_view_seconds": avg_sec,
        "end_retention": end_ret,
    }


def score_metrics(metrics: dict, ch_base: dict, niche_base: dict) -> dict[str, dict]:
    out = {}
    ch_vals = ch_base.get("values") or {}
    for key, label, unit in METRIC_ORDER:
        val = metrics.get(key)
        c_bench = ch_vals.get(key)
        n_bench = niche_base.get(key)
        out[key] = {
            "label": label,
            "unit": unit,
            "value": val,
            "ch_median": c_bench,
            "ch_rsi": rsi(val, c_bench),
            "niche_bench": n_bench,
            "niche_rsi": rsi(val, n_bench),
        }
    return out


def rsi_summary_line(scores: dict[str, dict]) -> str:
    """Single-line RSI summary with arrows: `Metric chRSI/nicheRSI`."""
    parts = []
    for key, label, _ in METRIC_ORDER:
        s = scores[key]
        parts.append(f"{label} {fmt_rsi(s['ch_rsi'])}/{fmt_rsi(s['niche_rsi'])}")
    return "RSI (vs ch / niche): " + " · ".join(parts)


def steepest_drops(
    curve: list[dict],
    duration_s: float,
    count: int = 3,
    min_gap_s: float = DROP_MIN_GAP_S,
    avg_view_seconds: float | None = None,
) -> list[dict]:
    """Identify the 3 steepest non-overlapping drop points and their [t-20s, t+20s] watch windows.

    When YouTube suppresses the retention curve (empty list, typical under ~20 views), returns 3 explicit
    proxy watch windows (opening 0:00-0:40, around average view duration, and final 40 s end screen)
    marked `proxy=True` so Gemini still inspects the cut honestly without inventing curve points.
    """
    if not curve or len(curve) < 2 or duration_s <= 0:
        dur = max(40.0, float(duration_s or 40.0))
        mid_t = float(avg_view_seconds) if (avg_view_seconds and 25.0 <= avg_view_seconds <= dur - 55.0) else min(60.0, dur / 2.0)
        mid_start = max(40.0, round(mid_t - DROP_WINDOW_HALF_S))
        mid_end = min(dur - 40.0, mid_start + 40.0)
        if mid_end <= mid_start:
            mid_start, mid_end = max(0.0, dur / 2.0 - 20.0), min(dur, dur / 2.0 + 20.0)
        return [
            {
                "rank": 1,
                "proxy": True,
                "reason": "Opening hook (retention curve suppressed by YouTube at low views)",
                "drop_start_s": 0.0,
                "drop_end_s": 30.0,
                "delta_pp": None,
                "from_pct": None,
                "to_pct": None,
                "watch_start_s": 0.0,
                "watch_end_s": min(40.0, dur),
            },
            {
                "rank": 2,
                "proxy": True,
                "reason": f"Around typical exit ({fmt_mmss(mid_t)} avg view duration; curve suppressed)",
                "drop_start_s": mid_t,
                "drop_end_s": mid_t,
                "delta_pp": None,
                "from_pct": None,
                "to_pct": None,
                "watch_start_s": mid_start,
                "watch_end_s": mid_end,
            },
            {
                "rank": 3,
                "proxy": True,
                "reason": "End screen and next-video handoff (final 40 s; curve suppressed)",
                "drop_start_s": max(0.0, dur - 20.0),
                "drop_end_s": dur,
                "delta_pp": None,
                "from_pct": None,
                "to_pct": None,
                "watch_start_s": max(0.0, dur - 40.0),
                "watch_end_s": dur,
            },
        ][:count]

    candidates = []
    for i in range(1, len(curve)):
        prev, cur = curve[i - 1], curve[i]
        w0, w1 = float(prev.get("watching", 0.0)), float(cur.get("watching", 0.0))
        delta_pp = round((w1 - w0) * 100.0, 2)
        if delta_pp >= 0:
            continue
        t0 = float(prev.get("at", 0.0)) * duration_s
        t1 = float(cur.get("at", 0.0)) * duration_s
        mid = (t0 + t1) / 2.0
        candidates.append({
            "delta_pp": delta_pp,
            "drop_start_s": round(t0, 1),
            "drop_end_s": round(t1, 1),
            "mid_s": mid,
            "from_pct": round(w0 * 100.0, 1),
            "to_pct": round(w1 * 100.0, 1),
            "relative": cur.get("relative"),
        })
    candidates.sort(key=lambda c: (c["delta_pp"], c["drop_start_s"]))

    picked = []
    for cand in candidates:
        if all(abs(cand["mid_s"] - p["mid_s"]) >= min_gap_s for p in picked):
            w_start = max(0.0, round(cand["mid_s"] - DROP_WINDOW_HALF_S, 1))
            w_end = min(duration_s, round(cand["mid_s"] + DROP_WINDOW_HALF_S, 1))
            if w_end - w_start < 40.0 and duration_s >= 40.0:
                if w_start <= 0.0:
                    w_end = min(duration_s, 40.0)
                elif w_end >= duration_s:
                    w_start = max(0.0, duration_s - 40.0)
            picked.append({
                "rank": len(picked) + 1,
                "proxy": False,
                "reason": f"Steepest drop #{len(picked) + 1}: {cand['delta_pp']:+.1f} pp ({cand['from_pct']:.1f}% -> {cand['to_pct']:.1f}%)",
                "drop_start_s": cand["drop_start_s"],
                "drop_end_s": cand["drop_end_s"],
                "mid_s": cand["mid_s"],
                "delta_pp": cand["delta_pp"],
                "from_pct": cand["from_pct"],
                "to_pct": cand["to_pct"],
                "watch_start_s": w_start,
                "watch_end_s": w_end,
            })
            if len(picked) == count:
                break
    return picked


def diagnose_funnel(
    slug: str,
    window: str,
    metrics: dict,
    ch_base: dict,
    drops: list[dict],
    duration_s: float,
    end_retention: float | None = None,
    avg_view_seconds: float | None = None,
) -> dict:
    """Diagnose the funnel in strict priority order:
    1. Showings (topic / search)
    2. Click-through (title & thumbnail packaging)
    3. First 30 seconds (hook)
    4. Mid-film cliffs (pacing / picture)
    5. End (end screen & next-video handoff)
    """
    impr = metrics.get("impressions")
    ctr = metrics.get("ctr")
    avg_pct = metrics.get("avg_pct")
    r30 = metrics.get("r30")
    ch_impr = (ch_base.get("values") or {}).get("impressions")

    impr_floor = 1000 if slug == "ww2" else (200 if window == "48h" else 500)
    ctr_floor = 3.0 if slug == "ww2" else 2.5

    steps = []

    # 1. Showings -> topic or search problem
    if impr is None:
        s1_state = "UNMEASURED"
        s1_detail = "No impression count recorded yet; read Studio Reach before calling topic/search."
    elif impr < impr_floor or (ch_impr and impr < 0.4 * ch_impr):
        s1_state = "BOTTLENECK"
        med_note = f"; channel median {round(ch_impr)}" if ch_impr is not None else ""
        s1_detail = (f"Only {impr} impressions (below {impr_floor} floor{med_note}): "
                     "topic/search-demand or indexing problem; check search terms and results-page position.")
    else:
        s1_state = "OK"
        s1_detail = f"{impr} impressions meets the {impr_floor} floor."
    steps.append({"step": 1, "stage": "Showings (Topic / Search)", "state": s1_state, "detail": s1_detail})

    # 2. Click-through -> packaging (title and thumbnail)
    if ctr is None or (impr is not None and impr < 100):
        s2_state = "UNMEASURED"
        s2_detail = (f"CTR {ctr}% on {impr} impressions is too small a sample (<100 impressions) to blame packaging alone."
                     if ctr is not None else "No CTR recorded yet.")
    elif ctr < ctr_floor:
        s2_state = "BOTTLENECK"
        s2_detail = f"CTR {ctr}% on {impr} impressions is below the {ctr_floor}% bar: packaging problem (thumbnail first, then title)."
    else:
        s2_state = "OK"
        s2_detail = f"CTR {ctr}% on {impr} impressions meets or beats the {ctr_floor}% bar."
    steps.append({"step": 2, "stage": "Click-through (Packaging)", "state": s2_state, "detail": s2_detail})

    # 3. First 30 seconds -> hook
    early_drops = [d for d in drops if not d.get("proxy") and d["drop_start_s"] < 30.0 and (d["delta_pp"] or 0) <= -15.0]
    if r30 is not None:
        if r30 < 55.0 or early_drops:
            s3_state = "BOTTLENECK"
            s3_detail = f"0:30 retention is {r30}% (target >=60%)" + (f" with steep early drop {early_drops[0]['delta_pp']:+.1f} pp at {fmt_mmss(early_drops[0]['drop_start_s'])}" if early_drops else "") + ": hook problem."
        else:
            s3_state = "OK"
            s3_detail = f"0:30 retention is {r30}%."
    elif avg_view_seconds is not None and avg_view_seconds < 60:
        s3_state = "BOTTLENECK"
        s3_detail = f"0:30 curve suppressed, but average view duration is only {int(avg_view_seconds)} s: viewers leave in the opening."
    else:
        s3_state = "UNMEASURED"
        s3_detail = "0:30 retention suppressed by YouTube (low views); watch 0:00-0:40 directly to audit the hook."
    steps.append({"step": 3, "stage": "First 30 seconds (Hook)", "state": s3_state, "detail": s3_detail})

    # 4. Mid-film cliffs -> pacing or picture
    mid_drops = [
        d for d in drops
        if not d.get("proxy") and 30.0 <= d["drop_start_s"] <= max(30.0, duration_s - 30.0) and (d["delta_pp"] or 0) <= -5.0
    ]
    if mid_drops or (avg_pct is not None and avg_pct < 25.0):
        s4_state = "BOTTLENECK"
        bits = []
        if avg_pct is not None and avg_pct < 25.0:
            bits.append(f"average % viewed is {avg_pct}% (<25% floor)")
        if mid_drops:
            bits.append("mid-film drops at " + ", ".join(f"{fmt_mmss(d['drop_start_s'])} ({d['delta_pp']:+.1f} pp)" for d in mid_drops))
        s4_detail = "; ".join(bits) + ": pacing or picture problem."
    elif avg_pct is not None:
        s4_state = "OK"
        s4_detail = f"Average % viewed is {avg_pct}% with no mid-film cliff >=5 pp."
    else:
        s4_state = "UNMEASURED"
        s4_detail = "No average % viewed or mid-film curve yet."
    steps.append({"step": 4, "stage": "Mid-film cliffs (Pacing / Picture)", "state": s4_state, "detail": s4_detail})

    # 5. End -> end screen and next-video handoff
    late_drops = [d for d in drops if not d.get("proxy") and duration_s > 0 and d["drop_start_s"] > duration_s - 30.0 and (d["delta_pp"] or 0) <= -5.0]
    if late_drops or (end_retention is not None and end_retention < 10.0):
        s5_state = "BOTTLENECK"
        s5_detail = (f"End retention falls to {end_retention}%" if end_retention is not None else "Late drop in final 30 s") + ": inspect end screen and spoken next-video handoff."
    elif end_retention is not None:
        s5_state = "OK"
        s5_detail = f"End retention finishes at {end_retention}% (still verify spoken handoff matches end-screen target)."
    else:
        s5_state = "UNMEASURED"
        s5_detail = "End curve suppressed; watch final 40 s directly to verify spoken handoff and end-screen link."
    steps.append({"step": 5, "stage": "End (End Screen / Handoff)", "state": s5_state, "detail": s5_detail})

    primary = next((s for s in steps if s["state"] == "BOTTLENECK"), steps[0])
    secondary = [s for s in steps if s["state"] == "BOTTLENECK" and s is not primary]
    return {"primary": primary, "secondary": secondary, "steps": steps}


def extract_clips(video_path: pathlib.Path, drops: list[dict], out_dir: pathlib.Path, prefix: str = "drop") -> list[pathlib.Path]:
    """Cut lightweight 640px H.264+AAC MP4 watch clips for each drop window via ffmpeg."""
    if not video_path.is_file():
        raise FileNotFoundError(f"Master video not found: {video_path}")
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for d in drops:
        start = float(d["watch_start_s"])
        length = max(1.0, float(d["watch_end_s"]) - start)
        out_file = out_dir / f"{prefix}{d['rank']}_{int(start):04d}_{int(start + length):04d}.mp4"
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", f"{start:.2f}", "-i", str(video_path), "-t", f"{length:.2f}",
                "-vf", "scale=640:-2", "-c:v", "libx264", "-preset", "veryfast", "-crf", "28",
                "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(out_file),
            ],
            check=True,
        )
        written.append(out_file)
    return written


def inspect_text(slug: str, vid: str, window: str) -> str:
    ctx = video_context(slug, vid, window)
    ch_base = channel_baseline(slug, window, exclude_vid=vid, before_iso=ctx["published_at"])
    n_base = niche_benchmark(slug, window)
    scores = score_metrics(ctx["metrics"], ch_base, n_base)
    drops = steepest_drops(ctx["retention"], ctx["duration_s"], avg_view_seconds=ctx["avg_view_seconds"])
    diag = diagnose_funnel(slug, window, ctx["metrics"], ch_base, drops, ctx["duration_s"],
                           end_retention=ctx["end_retention"], avg_view_seconds=ctx["avg_view_seconds"])
    lines = [
        f"Autopsy inspection: \"{ctx['title']}\" ({vid}) · {channels.name(slug)} · {window}",
        f"Published: {ctx['published_at']} · Age at snapshot ({ctx['snapshot_date']}): {ctx['age_hours']} h · Duration: {fmt_mmss(ctx['duration_s'])} ({int(ctx['duration_s'])} s)",
        rsi_summary_line(scores),
        "",
        "| Metric | Film | Channel median | Basis | RSI (ch) | Niche outlier | RSI (niche) |",
        "|---|---:|---:|---|---:|---:|---:|",
    ]
    for key, label, unit in METRIC_ORDER:
        s = scores[key]
        fv = f"{s['value']}{unit}" if s["value"] is not None else "—"
        cm = f"{s['ch_median']}{unit}" if s["ch_median"] is not None else "—"
        nb = f"{s['niche_bench']}{unit}" if s["niche_bench"] is not None else "—"
        lines.append(f"| {label} | {fv} | {cm} | {ch_base['basis'][key]} | {fmt_rsi(s['ch_rsi'])} | {nb} | {fmt_rsi(s['niche_rsi'])} |")
    lines += [
        "",
        f"Primary bottleneck: Step {diag['primary']['step']} — {diag['primary']['stage']}",
    ]
    for st in diag["steps"]:
        lines.append(f"  {st['step']}. [{st['state']}] {st['stage']}: {st['detail']}")
    lines += ["", "Watch windows (20 s either side of steepest drops):"]
    for d in drops:
        tag = "PROXY" if d.get("proxy") else "CURVE"
        lines.append(f"  #{d['rank']} [{tag}] watch {fmt_mmss(d['watch_start_s'])}-{fmt_mmss(d['watch_end_s'])} ({d['watch_start_s']:.0f}-{d['watch_end_s']:.0f} s): {d['reason']}")
    lines += ["", f"Niche outlier source: {n_base['source']}"]
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    ins = sub.add_parser("inspect", help="compute RSI scores, funnel diagnosis and drop watch windows")
    ins.add_argument("id")
    ins.add_argument("--window", choices=("48h", "7d"), default="48h")
    ins.add_argument("--channel", default="", help="channel slug (auto-detected if omitted)")

    clp = sub.add_parser("clips", help="extract 40 s watch clips for Gemini 4 Neon")
    clp.add_argument("id")
    clp.add_argument("--video", required=True, help="path to local/NAS master mp4")
    clp.add_argument("--out-dir", required=True, help="folder to write 40 s mp4 clips")
    clp.add_argument("--window", choices=("48h", "7d"), default="48h")
    clp.add_argument("--channel", default="")

    args = ap.parse_args(argv)
    slug = args.channel
    if not slug:
        found = lc.lookup(args.id)
        if not found:
            print(f"{args.id}: not found in any channel snapshot", file=sys.stderr)
            return 1
        slug = found[0]
    if args.cmd == "inspect":
        print(inspect_text(slug, args.id, args.window))
        return 0
    ctx = video_context(slug, args.id, args.window)
    drops = steepest_drops(ctx["retention"], ctx["duration_s"], avg_view_seconds=ctx["avg_view_seconds"])
    paths = extract_clips(pathlib.Path(args.video), drops, pathlib.Path(args.out_dir), prefix=f"{slug}_{args.id}_drop")
    for p in paths:
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
