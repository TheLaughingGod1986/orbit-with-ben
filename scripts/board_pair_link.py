#!/usr/bin/env python3
"""Mint Ben's one-time "link this phone" link for the Studio Kanban buttons (25 Oct 2026, Ben: "Just need to approve no
need for code"). Opening it once on a phone sets the board's studio_ben cookie there, after which Approve / Request
changes post with one tap and never ask for a code (05_Analytics/kanban/board_site/benauth.js, api/pair.js).

    python3 scripts/board_pair_link.py [--days 7] [--out PATH]

The link is written to PATH (default ~/.config/studio-kanban/ben_pair_link, mode 0600) and is NEVER printed: it is a
credential until it's used. It works once (the nonce is recorded on first use) and expires after --days (max 7).
Signed with a key derived from WATCH_LINK_SECRET (env or ~/.config/studio-kanban/watch_link_secret, same as Play links).
Hand it to Ben only in his private chat; never in git, a GitHub comment, a log or the board.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import os
import secrets
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kanban_snapshot import watch_link_secret  # noqa: E402

SITE = "https://studio-kanban.vercel.app"
DEFAULT_OUT = Path.home() / ".config" / "studio-kanban" / "ben_pair_link"


def sign(secret: str, n: str, e: int) -> str:
    key = hmac.new(secret.encode(), b"studio-pair-v1", hashlib.sha256).digest()
    mac = hmac.new(key, f"{n}.{e}".encode(), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(mac).rstrip(b"=").decode()


def pair_link(secret: str, days: float = 7, now: float | None = None, nonce: str | None = None) -> tuple[str, int]:
    now = time.time() if now is None else now
    e = int(now + min(days, 7) * 86400) - 60   # stay inside the server's 7-day window
    n = nonce or secrets.token_urlsafe(18)
    return f"{SITE}/api/pair?n={n}&e={e}&s={sign(secret, n, e)}", e


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--days", type=float, default=7)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    a = ap.parse_args()
    secret = watch_link_secret()
    if not secret:
        print("no WATCH_LINK_SECRET on this machine", file=sys.stderr)
        return 1
    link, e = pair_link(secret, a.days)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(a.out, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(link + "\n")
    os.chmod(a.out, 0o600)
    when = time.strftime("%a %d %b %H:%M", time.localtime(e))
    print(f"one-time link written to {a.out} (0600, not shown); works once, expires {when} local")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
