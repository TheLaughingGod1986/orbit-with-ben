#!/usr/bin/env python3
"""Weekly public audit — run every Monday (25 Sep 2026; see IMPROVEMENTS_BACKLOG.md).

Reads the public channel pages only (no Studio, no login) and writes
  00_Brand/Channel-Setup/audits/weekly/<YYYY-MM-DD>/PUBLIC_SNAPSHOT.json
  00_Brand/Channel-Setup/audits/weekly/<YYYY-MM-DD>/REPORT.md

Checks
  - subscribers, total Short and long views, and the change since the last snapshot
  - every upload that is new since the last snapshot
  - frame 0 of each new Short (i.ytimg.com/vi/<id>/frame0.jpg): Orbit at frame 0, or a
    dark frame 0 (THUMBNAIL_AND_TITLE_RULES.md §3 — world first-frames median 86.5 views,
    Orbit 23.5, dark cards 16.5). The three Orbit-first labelled test Shorts
    (FAMILIAR_DANGER_STRATEGY.md; Claude #99 6036942792) are not counted as
    Orbit-at-frame-0 breaches — they stay public and unchanged on purpose.
  - titles: hashtags, hedged claims, and duplicate titles across the channel
Cannot check from public pages: stayed-to-watch, CTR, or a silent soundtrack. Those stay
Studio / `gate_shorts_open.py check` jobs.

Usage
  python3 weekly_public_audit.py [--date YYYY-MM-DD] [--handle OrbitWithBen]
Needs ffmpeg for the frame-0 checks; without it those checks are skipped and the report says so.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
import urllib.request
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gate_shorts_open as gate  # noqa: E402  (orbit_score / raw_frame / VISOR_FAIL)

ROOT = HERE.parents[2]
WEEKLY = ROOT / "00_Brand/Channel-Setup/audits/weekly"
UA = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-GB"}
# Frame 0 counts as mostly dark when under 10% of pixels are brighter than grey 60. Set on the
# live frames: text cards 3.7–4.6% · black card 1.3% · a dark space shot (3.8 cm, 253 views) 5.8% ·
# world openings 29–74%. A dark space shot can still work, so this is a look-at-it flag.
BRIGHT_LEVEL = 60
DARK_BRIGHT_FRAC = 0.10
HEDGE = re.compile(r"\b(?:we|it|they|this|you|scientists)\s+(?:may|might|could)\b|\bmay have\b|\bmight\b|^what if\b", re.I)
# Orbit-first labelled test Shorts (FAMILIAR_DANGER_STRATEGY.md). Claude #99 6036942792:
# leave them public/unchanged; do not count Orbit at frame 0 as a breach in reports.
# youtube:package and gate_upcoming.py still block Orbit at frame 0 on every other Short.
ORBIT_FIRST_TEST_IDS = frozenset({
    "Ih2zhZTbIR0",  # Fri 2 Oct
    "dQlOgsDGmtA",  # Mon 5 Oct Moon cover
    "pL339HhjDwo",  # Wed 7 Oct
})


def frame0_breach_flags(vid: str, flags: list[str] | None) -> list[str] | None:
    """Flags that count as breaches. Orbit-first labelled tests keep Orbit at frame 0 on purpose."""
    if flags is None:
        return None
    if vid in ORBIT_FIRST_TEST_IDS:
        return [f for f in flags if f != "Orbit at frame 0"]
    return list(flags)


# ----------------------------------------------------------------------------- fetch
def fetch(url: str) -> str:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def initial_data(html: str) -> dict:
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S)
    if not m:
        raise RuntimeError("ytInitialData not found — YouTube page layout changed")
    return json.loads(m.group(1))


def walk(o, key):
    if isinstance(o, dict):
        if key in o:
            yield o[key]
        for v in o.values():
            yield from walk(v, key)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v, key)


def count(text: str | None) -> int:
    if not text:
        return 0
    m = re.search(r"([\d.,]+)\s*([KkMm]?)", text)
    if not m or "No views" in text:
        return 0
    n = float(m.group(1).replace(",", ""))
    return int(n * {"k": 1_000, "m": 1_000_000}.get(m.group(2).lower(), 1))


def parse_longs(d: dict) -> list[dict]:
    out = []
    for lv in walk(d, "lockupViewModel"):
        vid = lv.get("contentId")
        meta = lv.get("metadata", {}).get("lockupMetadataViewModel", {})
        title = meta.get("title", {}).get("content")
        parts = [part.get("text", {}).get("content", "") for row in walk(meta, "metadataParts") for part in row]
        badge = next(iter(walk(lv, "thumbnailBadgeViewModel")), {}).get("text")
        if vid and title and not vid.startswith("PL"):
            out.append({"id": vid, "title": title, "views": count(parts[0] if parts else None),
                        "age": parts[1] if len(parts) > 1 else None, "length": badge})
    return out


def parse_shorts(d: dict) -> list[dict]:
    out = []
    for s in walk(d, "shortsLockupViewModel"):
        vid = s.get("onTap", {}).get("innertubeCommand", {}).get("reelWatchEndpoint", {}).get("videoId")
        om = s.get("overlayMetadata", {})
        if vid:
            out.append({"id": vid, "title": om.get("primaryText", {}).get("content"),
                        "views": count(om.get("secondaryText", {}).get("content"))})
    return out


def subscribers(html: str) -> int | None:
    m = re.search(r"([\d.,]+[KkMm]?) subscribers", html)
    return count(m.group(1)) if m else None


# ----------------------------------------------------------------------------- checks
def frame0_flags(vid: str) -> list[str]:
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / f"{vid}.jpg"
        with urllib.request.urlopen(urllib.request.Request(f"https://i.ytimg.com/vi/{vid}/frame0.jpg", headers=UA), timeout=60) as r:
            p.write_bytes(r.read())
        flags = []
        if gate.orbit_score(p, None)["visor_frac"] >= gate.VISOR_FAIL:
            flags.append("Orbit at frame 0")
        g = gate.raw_frame(p, 36, 64, None, "gray")
        if sum(1 for x in g if x > BRIGHT_LEVEL) / len(g) < DARK_BRIGHT_FRAC:
            flags.append("mostly dark frame 0 (check the subject is visible)")
        return flags


def cell(text: str | None) -> str:
    return (text or "").replace("|", "\\|")


def norm(title: str) -> str:
    t = re.sub(r"#\w+", "", title.lower())
    return re.sub(r"[^a-z0-9 ]+", "", t).strip()


def title_flags(title: str) -> list[str]:
    flags = []
    if "#" in title:
        flags.append("hashtag in title")
    if HEDGE.search(title):
        flags.append("hedged claim")
    return flags


def previous(today: str) -> dict | None:
    if not WEEKLY.exists():
        return None
    older = sorted(p for p in WEEKLY.iterdir() if p.is_dir() and p.name < today and (p / "PUBLIC_SNAPSHOT.json").exists())
    return json.loads((older[-1] / "PUBLIC_SNAPSHOT.json").read_text()) if older else None


# ----------------------------------------------------------------------------- report
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--handle", default="OrbitWithBen")
    ns = ap.parse_args()

    base = f"https://www.youtube.com/@{ns.handle}"
    vhtml = fetch(f"{base}/videos")
    shtml = fetch(f"{base}/shorts")
    snap = {
        "captured": ns.date,
        "subs": subscribers(vhtml),
        "longs": parse_longs(initial_data(vhtml)),
        "shorts": parse_shorts(initial_data(shtml)),
        "note": "Shorts tab lists the newest 48 public Shorts; older ones are not in this file.",
    }
    prev = previous(ns.date)
    prev_views = {v["id"]: v["views"] for v in (prev["longs"] + prev["shorts"])} if prev else {}

    can_frames = bool(shutil.which("ffmpeg"))
    # The Shorts tab is newest first, and only the newest 48 are listed. So a Short is new only
    # if it sits above the newest one last week's list had; an unseen one further down fell
    # outside last week's 48 and has only come back into view (it isn't new).
    new_shorts, returning = [], []
    if prev:
        for i, s in enumerate(snap["shorts"]):
            if s["id"] in prev_views:
                returning = [x for x in snap["shorts"][i:] if x["id"] not in prev_views]
                break
            new_shorts.append(s)
    else:
        new_shorts = snap["shorts"][:7]
    for s in new_shorts:
        s["frame0_flags"] = frame0_flags(s["id"]) if can_frames else None

    everything = [dict(v, kind="long") for v in snap["longs"]] + [dict(v, kind="short") for v in snap["shorts"]]
    seen: dict[str, list[dict]] = {}
    for v in everything:
        seen.setdefault(norm(v["title"] or ""), []).append(v)
    dupes = [vs for vs in seen.values() if len(vs) > 1]
    flagged = [(v, title_flags(v["title"] or "")) for v in everything]
    flagged = [(v, f) for v, f in flagged if f]

    out_dir = WEEKLY / ns.date
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "PUBLIC_SNAPSHOT.json").write_text(json.dumps(snap, indent=1, ensure_ascii=False) + "\n")

    s_views = sum(s["views"] for s in snap["shorts"])
    l_views = sum(v["views"] for v in snap["longs"])
    lines = [f"# Weekly public audit — {ns.date}", ""]
    if prev:
        # Like for like: Shorts in both lists, plus the new ones. Shorts that only came back
        # into the 48-item window would otherwise count as growth.
        s_gain = sum(s["views"] - prev_views[s["id"]] for s in snap["shorts"] if s["id"] in prev_views)
        s_gain += sum(s["views"] for s in new_shorts)
        l_gain = sum(v["views"] - prev_views.get(v["id"], 0) for v in snap["longs"])
        lines += [f"Compared with {prev['captured']}.", "",
                  "| | Now | Change |", "|---|---:|---:|",
                  f"| Subscribers | {snap['subs']} | {(snap['subs'] or 0) - (prev.get('subs') or 0):+d} |",
                  f"| Views, newest 48 Shorts | {s_views:,} | {s_gain:+,} (like for like) |",
                  f"| Views, longs | {l_views:,} | {l_gain:+,} |", ""]
    else:
        lines += ["First snapshot — no comparison yet.", "",
                  f"Subscribers {snap['subs']} · newest 48 Shorts {s_views:,} views · longs {l_views:,} views.", ""]

    lines += ["## New since last week", ""]
    new_longs = [v for v in snap["longs"] if prev and v["id"] not in prev_views]
    if not new_shorts and not new_longs:
        lines += ["Nothing new.", ""]
    else:
        lines += ["| Type | Id | Title | Views | Frame 0 |", "|---|---|---|---:|---|"]
        for v in new_longs:
            lines.append(f"| long | `{v['id']}` | {cell(v['title'])} | {v['views']} | — |")
        for s in new_shorts:
            raw = s.get("frame0_flags")
            breach = frame0_breach_flags(s["id"], raw)
            if raw is None:
                f0 = "not checked (no ffmpeg)"
            elif s["id"] in ORBIT_FIRST_TEST_IDS and raw and "Orbit at frame 0" in raw:
                rest = [f for f in (breach or [])]
                f0 = ", ".join(["Orbit-first labelled test (not a breach)"] + rest)
            else:
                f0 = ", ".join(breach or []) or "ok"
            lines.append(f"| short | `{s['id']}` | {cell(s['title'])} | {s['views']} | {f0} |")
    if returning:
        lines += ["", f"Back in the newest-48 list (older, not new): {', '.join('`' + x['id'] + '`' for x in returning)}."]
        lines.append("")

    if prev:
        movers = sorted(((v["views"] - prev_views[v["id"]], v) for v in everything if v["id"] in prev_views), key=lambda x: -x[0])[:5]
        lines += ["## Biggest gains this week", "", "| Gain | Views | Title |", "|---:|---:|---|"]
        lines += [f"| {g:+d} | {v['views']} | {cell(v['title'])} |" for g, v in movers]
        lines.append("")

    lines += ["## Flags", ""]
    if not dupes and not flagged:
        lines += ["None.", ""]
    for vs in dupes:
        lines.append("- **Duplicate title:** " + " · ".join(f"`{v['id']}` ({v['kind']}, {v['views']} views)" for v in vs) + f" — *{vs[0]['title']}*")
    for v, f in flagged:
        lines.append(f"- **{', '.join(f).capitalize()}:** `{v['id']}` *{v['title']}*")
    for s in new_shorts:
        breach = frame0_breach_flags(s["id"], s.get("frame0_flags"))
        if breach:
            lines.append(f"- **{', '.join(breach).capitalize()}:** `{s['id']}` *{s['title']}* (THUMBNAIL_AND_TITLE_RULES.md §3)")
    lines += ["", "## Still needs Studio",
              "", "Public pages cannot show stayed-to-watch, CTR or a silent soundtrack. Add stayed-to-watch at 48 h for each new Short to `could-orbit-survive/TEST_LOG.md`, and run `gate_shorts_open.py check` on every export before upload.", ""]
    (out_dir / "REPORT.md").write_text("\n".join(lines))
    print(out_dir / "REPORT.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
