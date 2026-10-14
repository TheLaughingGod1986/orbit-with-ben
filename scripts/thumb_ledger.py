#!/usr/bin/env python3
"""Thumbnail test ledger (Ben, 14 Oct 2026): "Using the data we collect, if we find Codex images perform better, let's
set that up in future."

Every YouTube Test & Compare on a thumbnail is one row in 05_Analytics/tests/THUMB_LEDGER.json: the video, who made A
and who made B, when it started, and, at read-back, YouTube's watch-time share per variant (Studio picks the winner on
watch-time share) plus impressions and CTR where Studio shows them. `verdict` adds up wins per maker and says when one
maker's thumbnails have earned the default.

  python3 scripts/thumb_ledger.py add --video 3xrxdmaOwJI --channel owb --title "What Happens If You Fall Into a Black Hole?" \
      --a-maker house --b-maker codex --b-file 00_Brand/.../blackhole_B_no_way_out.jpg --job J0243
  python3 scripts/thumb_ledger.py start T002                # the day the Studio test is armed
  python3 scripts/thumb_ledger.py result T003 --wt-a 38.5 --wt-b 61.5 [--ctr-a 2.1 --ctr-b 3.4 --impressions 1840] [--winner b]
  python3 scripts/thumb_ledger.py verdict          # wins per maker, and the call (default needs MIN_TESTS decided tests)

The rule: a maker becomes the house default when it has been one side of at least MIN_TESTS decided tests and won at
least WIN_SHARE of them. A test is decided when one side's watch-time share is WIN_MARGIN points or more ahead (or
Studio names a winner); otherwise it counts as a draw. Until a maker earns it, every new design goes in as B against
the live thumbnail.
"""
import argparse, datetime as dt, json, pathlib, sys

LEDGER = pathlib.Path(__file__).resolve().parent.parent / "05_Analytics" / "tests" / "THUMB_LEDGER.json"
MIN_TESTS = 4
WIN_SHARE = 0.75
WIN_MARGIN = 5.0   # watch-time share points


def load(path=LEDGER) -> dict:
    return json.loads(path.read_text()) if path.exists() else {"tests": []}


def save(d: dict, path=LEDGER) -> None:
    path.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def add(d: dict, **kw) -> dict:
    t = {"id": f"T{len(d['tests']) + 1:03d}", "status": "running",
         "started": kw.get("started") or dt.date.today().isoformat(),
         "channel": kw["channel"], "video": kw["video"], "title": kw.get("title", ""), "job": kw.get("job", ""),
         "a": {"maker": kw["a_maker"], "file": kw.get("a_file", "")}, "b": {"maker": kw["b_maker"], "file": kw.get("b_file", "")},
         "result": None}
    d["tests"].append(t)
    return t


def winner_of(r: dict) -> str:
    """'a', 'b' or 'draw' from a result."""
    if r.get("winner") in ("a", "b", "draw"):
        return r["winner"]
    wa, wb = r.get("wt_a"), r.get("wt_b")
    if wa is None or wb is None:
        return "draw"
    return "b" if wb - wa >= WIN_MARGIN else "a" if wa - wb >= WIN_MARGIN else "draw"


def result(d: dict, tid: str, **r) -> dict:
    t = next(x for x in d["tests"] if x["id"] == tid)
    t["result"] = {k: v for k, v in r.items() if v is not None}
    t["result"]["winner"] = winner_of(t["result"])
    t["status"] = "done"
    return t


def tally(d: dict) -> dict:
    """{maker: {"tests": n decided tests it was in, "wins": n, "draws": n}} over finished tests."""
    out: dict = {}
    for t in d["tests"]:
        if t["status"] != "done" or not t.get("result"):
            continue
        w = t["result"]["winner"]
        for side in ("a", "b"):
            m = t[side]["maker"]
            s = out.setdefault(m, {"tests": 0, "wins": 0, "draws": 0})
            if w == "draw":
                s["draws"] += 1
            else:
                s["tests"] += 1
                s["wins"] += w == side
    return out


def verdict(d: dict) -> tuple:
    """(default maker or None, lines)."""
    tl = tally(d)
    lines, best = [], None
    for m, s in sorted(tl.items()):
        share = s["wins"] / s["tests"] if s["tests"] else 0
        lines.append(f"{m}: won {s['wins']} of {s['tests']} decided tests ({share:.0%}), {s['draws']} draws")
        if m != "house" and s["tests"] >= MIN_TESTS and share >= WIN_SHARE and (best is None or share > best[1]):
            best = (m, share)
    running = sum(t["status"] == "running" for t in d["tests"])
    lines.append(f"{running} test(s) still running")
    if best:
        lines.append(f"CALL: {best[0]} has earned the default ({best[1]:.0%} of {tl[best[0]]['tests']} decided tests). "
                     f"Chief makes {best[0]}'s style the house thumbnail rule and new designs go to it first.")
    else:
        lines.append(f"CALL: no default yet (needs {MIN_TESTS}+ decided tests and {WIN_SHARE:.0%} wins); "
                     "keep testing every new design as B")
    return (best[0] if best else None), lines


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    for f in ("video", "channel", "a-maker", "b-maker"):
        a.add_argument("--" + f, required=True)
    for f in ("title", "a-file", "b-file", "job", "started"):
        a.add_argument("--" + f, default="")
    r = sub.add_parser("result")
    r.add_argument("id")
    for f in ("wt-a", "wt-b", "ctr-a", "ctr-b"):
        r.add_argument("--" + f, type=float)
    r.add_argument("--impressions", type=int)
    r.add_argument("--winner", choices=["a", "b", "draw"])
    r.add_argument("--read", default=dt.date.today().isoformat())
    s = sub.add_parser("start")
    s.add_argument("id")
    s.add_argument("--date", default=dt.date.today().isoformat())
    sub.add_parser("verdict")
    o = p.parse_args(argv)
    d = load()
    if o.cmd == "add":
        t = add(d, video=o.video, channel=o.channel, a_maker=o.a_maker, b_maker=o.b_maker, title=o.title,
                a_file=o.a_file, b_file=o.b_file, job=o.job, started=o.started)
        save(d)
        print(json.dumps(t, indent=2))
    elif o.cmd == "result":
        t = result(d, o.id, wt_a=o.wt_a, wt_b=o.wt_b, ctr_a=o.ctr_a, ctr_b=o.ctr_b, impressions=o.impressions,
                   winner=o.winner, read=o.read)
        save(d)
        print(json.dumps(t, indent=2))
    elif o.cmd == "start":
        t = next(x for x in d["tests"] if x["id"] == o.id)
        t.update(status="running", started=o.date)
        save(d)
        print(f"{o.id} running since {o.date}")
    else:
        print("\n".join(verdict(d)[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
