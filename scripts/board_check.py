#!/usr/bin/env python3
"""Board self-check (Ben, 25 Oct 2026: the cuts waiting on his OK weren't on the board, and nobody noticed).

Compares the queue's jobs waiting on Ben (`awaits_ben` on a job, see `jobs.py awaits` and video_tracker.ask_entries)
with the cards actually published on the board-data branch, and checks the live site:
  - every entry that still asks Ben has a card in Ready for OK (or Changes, if he asked for changes)
  - that card has a Play link, the cut's file is on the Mini, and the signed link answers 302 (it opens the video)
  - every cut Ben OK'd that is still on its way (`approved_from` on the delivering job, `jobs.py approved`) has a card in
    "Approved, on its way" for that job (Ben, 25 Oct 14:13), unless the upload already read back (then it's in Done)
  - the live site (studio-kanban.vercel.app) answers 200

Result, every run (for a routine to watch): ~/_desk/state/board/board_check.json
  {"at", "ok": true|false, "expected": n, "problems": [...], "cards": [...]}
plus ~/_desk/state/board/BOARD_CHECK_FLAG, one line: "OK <time>" or "FAIL <time>: <first problem>".
Nothing is ever deleted. When the same problems are seen on two runs in a row (a fresh `awaits` needs one publish to
show), it posts one short "[Chief] board-check" note on orbit-with-ben #264 with `gh` (at most once per problem set,
and again after 6 h if it's still broken). That note never starts with "[Ben]".

  python3 scripts/board_check.py            # check, write the result, post if needed
  python3 scripts/board_check.py --no-post  # check and write only
board_publish.py starts it in the background after a run, at most every CHECK_EVERY_S.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import video_tracker as vt  # noqa: E402

HOME = pathlib.Path.home()
ROOT = HERE.parent
OWB = pathlib.Path(os.environ.get("OWB_REPO", str(HOME / "YouTube" / "orbit-with-ben")))
STATE = pathlib.Path(os.environ.get("BOARD_STATE", str(HOME / "_desk" / "state" / "board")))
SITE = os.environ.get("BOARD_SITE_URL", "https://studio-kanban.vercel.app").rstrip("/")
BRANCH = os.environ.get("BOARD_BRANCH", "board-data")
THREAD = ("TheLaughingGod1986/orbit-with-ben", 264)
ICLOUD = HOME / "Library" / "Mobile Documents" / "com~apple~CloudDocs"
CHECK_EVERY_S = 5 * 60
REPOST_S = 6 * 3600
RESULT = STATE / "board_check.json"
FLAG = STATE / "BOARD_CHECK_FLAG"


def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def iso(t: dt.datetime) -> str:
    return t.isoformat().replace("+00:00", "Z")


def published_board() -> dict:
    """board.json as it is on the board-data branch now (what the site reads), not the Mini's local copy."""
    subprocess.run(["git", "-C", str(OWB), "fetch", "-q", "origin", BRANCH], capture_output=True, timeout=120, check=True)
    out = subprocess.run(["git", "-C", str(OWB), "show", f"FETCH_HEAD:board.json"], capture_output=True, text=True,
                         timeout=60, check=True).stdout
    return json.loads(out)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):  # noqa: D401 - report the 302 itself; never download the video
        return None


def status_of(url: str, follow: bool = True) -> int:
    opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, method="GET", headers={"user-agent": "studio-kanban board_check"})
    try:
        with opener.open(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:  # noqa: BLE001
        return 0


def file_on_mini(rel: str) -> bool:
    if not rel:
        return False
    p = pathlib.Path(rel)
    for c in ([p] if p.is_absolute() else [ICLOUD / rel, ROOT / rel, OWB / rel]):
        if c.is_file():
            return True
    return False


def duplicate_slots(vids: list[dict]) -> list[str]:
    """Problems for two Short cards of one film scheduled for the same publishAt (OK/ask cards don't count)."""
    slots: dict = {}
    for v in vids:
        yt = v.get("youtube") or {}
        if v.get("type") != "short" or ":S:" not in str(v.get("key") or "") or yt.get("state") != "scheduled":
            continue
        slot = (str(v.get("parent") or v.get("key")).split(":S:")[0], str(yt.get("publishAt") or "")[:16])
        slots.setdefault(slot, []).append(yt.get("videoId") or v.get("key"))
    return [f"{film}: {len(ids)} Shorts scheduled for {at}Z ({', '.join(ids)}); a swap's old copy must be unscheduled"
            for (film, at), ids in sorted(slots.items()) if len(ids) > 1]


def check(queue_jobs: list[dict], board: dict, site_status=status_of) -> dict:
    checks = board.get("checks") or {}
    expected = [e for e in vt.ask_entries(queue_jobs) if vt.ask_live(e, checks)]
    vids = ((board.get("tracker") or {}).get("videos")) or []
    by_ask = {(v.get("ask") or {}).get("id"): v for v in vids if v.get("ask")}
    problems, cards = [], []
    for e in expected:
        v = by_ask.get(e["id"])
        row = {"id": e["id"], "job": e["job"], "what": e["what"], "due": e.get("due", ""), "file": e.get("file", "")}
        if not v:
            problems.append(f"{e['id']}: no card on the published board ({e['what'][:80]})")
            cards.append({**row, "card": "missing"})
            continue
        row.update(card=v.get("key"), lane=v.get("lane"), readyFor=v.get("readyFor"))
        if v.get("lane") not in ("ready", "changes", "approved"):
            problems.append(f"{e['id']}: card is in {v.get('lane')}, not Ready for OK")
        url = (v.get("watch") or {}).get("url") or ""
        if not file_on_mini(e.get("file", "")):
            problems.append(f"{e['id']}: Play file not found on the Mini: {e.get('file') or '(none named)'}")
        if not url:
            problems.append(f"{e['id']}: card has no Play link")
        elif v.get("lane") == "ready":
            code = site_status(url, follow=False)
            row["play"] = code
            if code not in (301, 302, 303, 307, 308, 200, 206):
                problems.append(f"{e['id']}: Play link answers {code or 'no response'}")
        cards.append(row)
    # Approved, on its way: every delivering job not yet read back as Private + scheduled has its card there.
    by_job = {(v.get("approved") or {}).get("job"): v for v in vids if v.get("lane") == "approved" and v.get("approved")}
    by_key = {v.get("key"): v for v in vids}
    approved = vt.approved_entries(queue_jobs)
    for e in approved:
        card = by_key.get(e.get("card") or "") or by_key.get(f"{e['channel']}:OK:{e['job']}")
        if vt.read_back(e, card) or e.get("jobStatus") == "cancelled":
            continue  # on YouTube (Done), or cancelled: that card carries its own warning while it's shown
        v = by_job.get(e["job"])
        row = {"id": e["job"], "job": e["job"], "what": e.get("what") or e.get("title"), "approved": True}
        if not v:
            problems.append(f"approved {e['job']}: no card in Approved, on its way ({(e.get('what') or e.get('title'))[:70]})")
            cards.append({**row, "card": "missing"})
            continue
        row.update(card=v.get("key"), lane=v.get("lane"), state=(v.get("approved") or {}).get("state"))
        if not (v.get("watch") or {}).get("url"):
            problems.append(f"approved {e['job']}: card has no Play link")
        cards.append(row)
    # A long its pipeline calls scheduled must read back from YouTube (Done), never sit in In progress because a job
    # only waits for it to go public (HOS 005, Ben 25 Oct 2026 22:54: "Why is it in progress on the board").
    hos = (board.get("hos") or {}).get("pipeline") or board.get("hos") or {}
    for f in hos.get("films") or []:
        st = ((f.get("stages") or {}).get("scheduled") or {}).get("status")
        key = f"HOS:{f.get('id')}"
        v = by_key.get(key)
        working = v and v.get("lane") == "progress" and (v.get("youtube") or {}).get("videoId") and any(j.get("status") in vt.ACTIVE_STATUSES for j in v.get("jobs") or [])
        if st == "done" and v and v.get("lane") not in ("done", "approved") and not working:
            problems.append(f"{key}: scheduled in PIPELINE but the card is in {v.get('lane')}; "
                            "no YouTube read-back (add the long to HOS UPLOADS.json)")
    # A film on YouTube with a job claimed or open shows in In progress, not Done (Ben, 26 Oct 2026 00:15: "Can't see
    # these jobs in the in progress lane"); blocked jobs don't count.
    for v in vids:
        live = [j.get("id") for j in v.get("jobs") or [] if j.get("status") == "claimed"]
        if v.get("lane") == "done" and live:
            problems.append(f"{v.get('key')}: {', '.join(live)} claimed but the card is in Done, not In progress")
    # One scheduled copy per Short slot: a swap's old copy must read back unscheduled (26 Oct 2026: Earth
    # dM1OgGPAYvw and its swap OVLv9dxTcpE both showed "Private, scheduled Mon 26 Oct 11:30").
    problems.extend(duplicate_slots(vids))
    code = site_status(SITE + "/", follow=True)
    if code != 200:
        problems.append(f"live site {SITE}/ answers {code or 'no response'}, not 200")
    return {"ok": not problems, "expected": len(expected), "approved": len(approved), "problems": problems, "cards": cards, "site": code,
            "boardPublishedAt": board.get("publishedAt", "")}


def note_text(res: dict) -> str:
    lines = [f"[Chief] board-check: {len(res['problems'])} problem(s) with the Studio Kanban's Ready for OK cards "
             f"({res['expected']} job(s) waiting on Ben)."]
    lines += [f"- {p}" for p in res["problems"][:12]]
    lines += ["", f"Result file on the Mini: {RESULT}. Re-check: `python3 scripts/board_check.py --no-post`."]
    text = "\n".join(lines)
    assert not text.startswith("[Ben]")
    return text


def post(text: str) -> str:
    if text.lstrip().startswith("[Ben]"):
        return "refused: a board-check note never starts with [Ben]"
    r = subprocess.run(["gh", "issue", "comment", str(THREAD[1]), "--repo", THREAD[0], "--body", text],
                       capture_output=True, text=True, timeout=60)
    return "posted" if r.returncode == 0 else f"not posted: {(r.stderr or r.stdout).strip()[:160]}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-post", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    at = now()
    STATE.mkdir(parents=True, exist_ok=True)
    try:
        prev = json.loads(RESULT.read_text())
    except (OSError, ValueError):
        prev = {}
    try:
        jobs = json.loads((ROOT / "jobs" / "queue.json").read_text())["jobs"]
        res = check(jobs, published_board())
    except Exception as e:  # noqa: BLE001 - the check itself failing is a problem to report too
        res = {"ok": False, "expected": 0, "problems": [f"board check could not run: {e!r}"[:300]], "cards": [], "site": 0}
    res["at"] = iso(at)
    sig = hashlib.sha256(json.dumps(sorted(res["problems"])).encode()).hexdigest()[:12] if res["problems"] else ""
    res["sig"] = sig
    res["posted"] = prev.get("posted", "")
    res["postedSig"] = prev.get("postedSig", "")
    if sig and sig == prev.get("sig") and not a.no_post:  # seen twice in a row
        last = vt._parse_iso(res["posted"])
        if sig != res["postedSig"] or not last or (at - last).total_seconds() > REPOST_S:
            out = post(note_text(res))
            res["postResult"] = out
            if out == "posted":
                res["posted"], res["postedSig"] = iso(at), sig
    RESULT.write_text(json.dumps(res, indent=1) + "\n")
    FLAG.write_text((f"OK {iso(at)}" if res["ok"] else f"FAIL {iso(at)}: {res['problems'][0]}") + "\n")
    if not a.quiet:
        print(json.dumps({k: res[k] for k in ("ok", "expected", "problems", "site")}, indent=1))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
