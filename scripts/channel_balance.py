#!/usr/bin/env python3
"""Which channel gets the work and the credits first (Ben, 9 Oct 2026: "each channel has 4 videos a month ... if we
have 4 videos already set up on Orbit and complete, then we need to work on History of Science ... allocate credits
accordingly").

  python3 scripts/channel_balance.py --hos <history-of-science checkout> [--today YYYY-MM-DD] [--months 3] [--json]

For each channel and each month from this one on, it counts the long videos airing that month and how many are
**complete** (the edit has passed: OWB `status.json` stage `edit` done, HOS PIPELINE.json stage `edit` done).
The target is 4 a month.

**Priority:** the channel whose earliest month is short of 4 complete goes first. A month with fewer than 4 films
planned counts as short too, because those films still have to be made (from next month on: this month's aired films
drop out of the records). If both channels are short in the same
month, the one further from 4 goes first; if that's equal too, the one whose next unfinished film airs sooner.
Every credit spend (ElevenLabs, Vertex, Flow) and every job pick follows this. The other channel's work still runs
when the priority channel has nothing an agent can do right now, so no one sits idle."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

TARGET = 4
REPO = Path(__file__).resolve().parent.parent
NAMES = {"owb": "Orbit With Ben", "hos": "History of Science"}


def owb_films(repo: Path = REPO) -> list[dict]:
    out = []
    for p in sorted((repo / "02_Video-Projects").glob("[0-9][0-9][0-9]_*/status.json")):
        d = json.loads(p.read_text())
        st = d.get("stages") or {}
        if not d.get("air"):
            continue
        out.append(dict(id=str(d.get("film") or p.parent.name[:3]), title=d.get("title", ""), air=d["air"][:10],
                        complete=(st.get("edit") or {}).get("state") == "done"))
    return out


def hos_films(hos: Path) -> list[dict]:
    d = json.loads((hos / "00_Brand/Channel-Setup/PIPELINE.json").read_text())
    out = []
    for f in d.get("films", []):
        if not f.get("air"):
            continue
        out.append(dict(id=str(f["id"]), title=f.get("title", ""), air=f["air"][:10],
                        complete=(f.get("stages", {}).get("edit") or {}).get("status") == "done"))
    return out


def months_from(today: dt.date, n: int) -> list[str]:
    y, m, out = today.year, today.month, []
    for _ in range(n):
        out.append(f"{y:04d}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def tally(films: list[dict], months: list[str]) -> dict:
    res = {}
    for mo in months:
        fs = sorted((f for f in films if f["air"].startswith(mo)), key=lambda f: f["air"])
        done = sum(f["complete"] for f in fs)
        # This month's films that already aired drop out of the records, so a gap in the current month counts only
        # when one of its films is still unfinished; a missing film is only planned for from next month on.
        current = mo == months[0]
        short = max(0, min(TARGET, len(fs)) - done) if current else max(0, TARGET - done)
        res[mo] = dict(planned=len(fs), complete=done, short=short, unplanned=0 if current else max(0, TARGET - len(fs)),
                       films=[f"{f['id']}{'' if f['complete'] else '*'}" for f in fs])
    return res


def priority(owb: list[dict], hos: list[dict], today: dt.date, n: int = 3) -> dict:
    months = months_from(today, n)
    t = {"owb": tally(owb, months), "hos": tally(hos, months)}

    def key(ch: str, films: list[dict]):
        first = next((i for i, mo in enumerate(months) if t[ch][mo]["short"] > 0), len(months))
        short = t[ch][months[first]]["short"] if first < len(months) else 0
        nxt = min((f["air"] for f in films if not f["complete"] and f["air"] >= today.isoformat()), default="9999")
        return (first, -short, nxt)

    k = {"owb": key("owb", owb), "hos": key("hos", hos)}
    first = min(k, key=lambda c: k[c])
    other = "hos" if first == "owb" else "owb"
    why_month = months[k[first][0]] if k[first][0] < len(months) else None
    if why_month:
        a, b = t[first][why_month], t[other][why_month]
        why = (f"{NAMES[first]} has {a['complete']} of {TARGET} complete for {why_month}"
               f" ({a['planned']} planned); {NAMES[other]} has {b['complete']} of {TARGET} ({b['planned']} planned).")
    else:
        why = f"Both channels have {TARGET} complete for every month checked."
    return dict(today=today.isoformat(), target=TARGET, months=months, first=first, first_name=NAMES[first],
                why=why, channels=t)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hos", type=Path, required=True)
    ap.add_argument("--today", default=None)
    ap.add_argument("--months", type=int, default=3)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    res = priority(owb_films(), hos_films(a.hos), today, a.months)
    if a.json:
        print(json.dumps(res, indent=2))
        return 0
    print(f"First: {res['first_name']}. {res['why']}")
    for ch in ("owb", "hos"):
        row = "  ".join(f"{mo}: {v['complete']}/{TARGET} complete, {v['planned']} planned [{' '.join(v['films'])}]"
                        for mo, v in res["channels"][ch].items())
        print(f"  {NAMES[ch]:<20} {row}")
    print("  (* = not complete yet)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
