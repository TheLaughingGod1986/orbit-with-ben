#!/usr/bin/env python3
"""Same-day alarm for missed daily jobs and silent agents (Ben, 4 Nov 2026, monthly report rec. 6).

Buffer's daily mirror was silent from 11 Oct to 1 Nov and the Claude worker from 1 to 4 Nov before
anyone noticed. This checks, from git alone, that each scheduled job left its mark inside its window:

  tracker   "Channel tracker <date>" commit on main (launchd 06:40 London)   due every 26 h
  Detached engines additionally check each channel snapshot history independently.

  buffer    "Buffer check <date>" commit on main (launchd 07:05 London)      due every 26 h
  claude    claude-heartbeat branch heartbeat.json "at"                       due every 90 min
  mini      mini-heartbeat branch heartbeat.json "at"                         due every 75 min

  python3 scripts/missed_runs.py            # print misses (exit 1 if any)
  python3 scripts/missed_runs.py --post     # also post one line per miss to the studio thread,
                                            # at most once per 22 h per check (dedupe by marker)

Run it on the Mini (a Claude that is down can't report itself). Reads only; never restarts anything.
"""
import argparse, datetime as dt, json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import channels  # noqa: E402  the studio's own name, for the launchd label in the relay's fix line

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UTC = dt.timezone.utc

CHECKS = {
    "tracker": {"kind": "commit", "grep": "^Channel tracker 20", "max_h": 26,
                "fix": "check launchd dev.orbit.analytics-snapshot and ~/Library/Logs/orbit-analytics.log on the Mini"},
    "buffer": {"kind": "commit", "grep": "^Buffer check 20", "max_h": 26,
               "fix": "check launchd dev.orbit.buffer-check (launchctl print) and its log on the Mini"},
    "claude": {"kind": "beat", "branch": "claude-heartbeat", "max_h": 1.5,
               "fix": "Claude's hourly run is not beating: open the Claude session or check its scheduled task"},
    "mini": {"kind": "beat", "branch": "mini-heartbeat", "max_h": 1.25,
             "fix": f"the Mini relay is not beating: check {channels.studio_label('chief-relay')} and scripts/mini_repair.py"},
}
MARK = "[alarm {key}]"


def parse(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(UTC)


def git(*args, root=None):
    try:
        result = subprocess.run(["git", "-C", str(root or ROOT), *args],
                                capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def configured_checks():
    """Keep resident alarms; detached engines check every record owner separately."""
    checks = {key: dict(value) for key, value in CHECKS.items()}
    if channels.studio_slug():
        return checks
    checks['tracker'].update(grep=r'^Channel tracker( 20|: daily analytics records$)',
                             paths=('05_Analytics/dashboard',))
    for slug in channels.slugs():
        checks[f'tracker-{slug}'] = {
            'kind': 'commit', 'root': channels.checkout(slug),
            'grep': r'^Channel tracker( 20|: daily analytics records$)',
            'paths': (f'05_Analytics/{slug}/snapshots',), 'max_h': 26,
            'fix': f'check detached analytics collection and record publication for {slug}',
        }
    return checks


def last_seen(check, fetch=True):
    """UTC time the check last left its mark, or None."""
    if 'root' in check and check['root'] is None:
        return None
    root = check.get('root', ROOT)
    if check["kind"] == "commit":
        if fetch and git("fetch", "-q", "origin", "main", root=root) is None:
            return None
        out = git("log", "origin/main", "-1", "--format=%cI", "-E",
                  f"--grep={check['grep']}", "--since=14 days ago",
                  "--", *check.get('paths', ()), root=root)
        try:
            return parse(out) if out else None
        except (ValueError, TypeError):
            return None
    if fetch and git("fetch", "-q", "origin", check["branch"], root=root) is None:
        return None
    raw = git("show", f"origin/{check['branch']}:heartbeat.json", root=root)
    try:
        return parse(json.loads(raw)["at"])
    except Exception:
        return None


def misses(now, seen, checks=None):
    """seen: {key: datetime|None}. Returns [(key, age_h or None, max_h)] for every check out of its window."""
    out = []
    for key, c in (CHECKS if checks is None else checks).items():
        t = seen.get(key)
        age = None if t is None else (now - t).total_seconds() / 3600
        if age is None or age > c["max_h"]:
            out.append((key, age, c["max_h"]))
    return out


def line(key, age, max_h, checks=None):
    checks = CHECKS if checks is None else checks
    when = "no record available in 14 days (or Git read/fetch failed)" if age is None else f"last {age:.1f} h ago (window {max_h:g} h)"
    return f"{MARK.format(key=key)} {key} missed: {when}. Fix: {checks[key]['fix']}."


def already_posted(key, now, recent_bodies):
    tag = MARK.format(key=key)
    return any(tag in b for b in recent_bodies)


def main(argv=None):
    from engine_guard import require_active
    require_active(ROOT)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--post", action="store_true")
    ap.add_argument("--no-fetch", action="store_true")
    a = ap.parse_args(argv)
    now = dt.datetime.now(UTC)
    checks = configured_checks()
    seen = {k: last_seen(c, fetch=not a.no_fetch) for k, c in checks.items()}
    found = misses(now, seen, checks)
    for k, c in checks.items():
        print(f"{k:8} last {seen[k].isoformat() if seen[k] else '-'}")
    lines = [line(*m, checks=checks) for m in found]
    for l in lines:
        print(l)
    if a.post and found:
        import studio_thread as thread
        since = (now - dt.timedelta(hours=22)).strftime("%Y-%m-%dT%H:%M:%SZ")
        recent = [c.get("body", "") for c in thread.api("GET", f"/issues/{thread.PR}/comments?per_page=100&since={since}")
                  if thread.trusted(c)]
        for m, l in zip(found, lines):
            if not already_posted(m[0], now, recent):
                thread.api("POST", f"/issues/{thread.PR}/comments", {"body": l})
                print("posted", m[0])
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
