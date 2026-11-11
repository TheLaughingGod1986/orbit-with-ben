#!/usr/bin/env python3
"""The board's Channels section: one card of facts for each channel plugged into the studio.

    python3 scripts/channel_cards.py        print the cards, and how ready the studio is for another, as JSON

Ben, 10 Nov 2026: "is there a small part on the dashboard we can show what repos are plugged in ... and the ability
that we can just add another repo if we want, for example a brand new channel". `board_publish.py` puts these cards
in `board.json` under `channels`; the Studio app draws them at the foot of the Overview and on `/#channels`.

Each card is the channel's own settings (`studio/channel.json`, read through `channels.py`) plus the answer of
`channel_check.py`: can the studio drive it, and what is still to do. Nothing here names a channel, so a third one
shows up the moment it is registered. A channel whose checkout is not on this machine is reported as not checked;
that is not an error (the MacBook and the cloud sessions hold only some of them).

How many films a channel has in production and its last video to go live are not here: the page counts them from
the same video list as its Producing number, so the two can never disagree.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import channel_check  # noqa: E402
import channels  # noqa: E402

KEEP = ("slug", "label", "name", "short", "home")   # what the page already reads; never drop one
MAX_LINES = 8                                       # a card lists this many things at most


def repo_name(url) -> str:
    """`owner/name` from a GitHub address, '' when the channel has no repo yet."""
    m = re.search(r"github\.com[:/]+([^/\s]+/[^/\s]+?)(?:\.git)?/?$", str(url or "").strip())
    return m.group(1) if m else ""


def card(c: dict, root=None) -> dict:
    """`root`: where to read the channel's files. The board publisher passes its own fresh copy of the channel's
    main branch; without one, the channel's working checkout on this machine is read."""
    out = {k: c.get(k) for k in KEEP}
    out["handle"] = str((c.get("youtube") or {}).get("handle") or "")
    out["repo"] = repo_name((c.get("repo") or {}).get("url"))
    limit = (c.get("wip") or {}).get("limit")
    out["wip"] = limit if isinstance(limit, int) and not isinstance(limit, bool) else None
    root = root or channels.checkout(c["slug"])
    if root is None:
        out.update(here=False, ready=None, must=[], todo=[], rules=None)
        return out
    must, todo = channel_check.check(root)
    out.update(here=True, ready=not must, must=must[:MAX_LINES], todo=todo[:MAX_LINES],
               rules=(pathlib.Path(root) / channel_check.RULES).is_file())
    return out


def cards(roots: dict | None = None) -> list[dict]:
    """One card per registered channel, in the registry's order. A channel that cannot be read still gets its name.

    `roots`: {slug: folder} for channels whose files should be read from somewhere other than the working checkout.
    The board publisher reads its own fresh copies of each channel's main branch: a working checkout can be on a job's
    branch, or behind (10 Nov 2026: on the Mini the second channel read "not checked here" for that reason)."""
    out = []
    for c in channels.all_channels():
        try:
            out.append(card(c, (roots or {}).get(c["slug"])))
        except Exception as e:  # noqa: BLE001  one bad channel must not take the others off the board
            out.append({**{k: c.get(k) for k in KEEP}, "here": None, "ready": None, "must": [],
                        "todo": [], "rules": None, "error": str(e)[:160]})
    return out


ROOM_FROM = 367   # both counts on the morning of 10 Nov 2026, before this work went into the job queue (327 + 40)


def room() -> dict:
    """Is the studio ready for another channel? `left` is how many code lines still assume today's channels: both
    counts of scripts/channel_ratchet.json added together. Zero means a new channel can be run, not only prepared."""
    r = json.loads((HERE / "channel_ratchet.json").read_text())
    return {"left": int(r["total"]) + int(r["home_total"]), "from": ROOM_FROM}


def main() -> int:
    print(json.dumps({"channels": cards(), "channelRoom": room()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
