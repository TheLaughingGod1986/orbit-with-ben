#!/usr/bin/env python3
"""Claude's heartbeat (Ben, 14 Oct 2026: "If ever an agent like yourself is down, out of usage for a few hours, make sure
we add a flag that you are out of usage ... and then when you are back online, it switches back to you automatically").

Every Claude run (the hourly studio run, and any session doing studio work) runs this first. It writes heartbeat.json
to the `claude-heartbeat` branch as a single commit, so main isn't touched. The Mac mini's relay (chief_relay.py) reads
it. If there has been no beat for CHIEF_CLAUDE_STALE_MIN (150 min, i.e. two missed hourly runs), Claude counts as out of
usage: its jobs walk down their chains (Cursor on the Claude model, Gemini, Codex), and the next one down runs as Chief.
The first fresh beat after that brings Claude back: unstarted jobs are handed back to it and it is Chief again.

  python3 scripts/claude_beat.py                                   # "I'm up"
  python3 scripts/claude_beat.py --note "hourly studio run"
  python3 scripts/claude_beat.py --out --until 2026-10-15T03:00:00Z --reason "5-hour limit"   # out, with the reset
"""
import argparse, datetime as dt, json, subprocess, sys

BRANCH = "claude-heartbeat"


def git(*a, inp=None):
    return subprocess.run(["git", *a], input=inp, capture_output=True, text=True, check=True).stdout.strip()


def beat(note: str = "", out: bool = False, until: str = "", reason: str = "") -> dict:
    hb = {"at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "who": "claude", "note": note}
    if out:
        hb.update(out=True, until=until, reason=reason)
    return hb


def push(hb: dict, remote: str = "origin") -> str:
    """One parentless commit holding heartbeat.json, force-pushed to the heartbeat branch."""
    blob = git("hash-object", "-w", "--stdin", inp=json.dumps(hb, indent=1) + "\n")
    tree = git("mktree", inp=f"100644 blob {blob}\theartbeat.json\n")
    commit = git("-c", "user.name=Claude", "-c", "user.email=noreply@anthropic.com", "commit-tree", tree, "-m",
                 f"claude heartbeat {hb['at']}" + (" (out of usage)" if hb.get("out") else ""))
    for i in range(4):
        r = subprocess.run(["git", "push", "-q", "-f", remote, f"{commit}:refs/heads/{BRANCH}"], capture_output=True, text=True)
        if r.returncode == 0:
            return commit
        import time
        time.sleep(2 ** (i + 1))
    raise SystemExit(f"heartbeat push failed: {r.stderr.strip()[-300:]}")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--note", default="")
    p.add_argument("--out", action="store_true", help="Claude is out of usage (give --until, the reset, in UTC)")
    p.add_argument("--until", default="")
    p.add_argument("--reason", default="")
    o = p.parse_args(argv)
    hb = beat(o.note, o.out, o.until, o.reason)
    push(hb)
    print(json.dumps(hb))
    return 0


if __name__ == "__main__":
    sys.exit(main())
