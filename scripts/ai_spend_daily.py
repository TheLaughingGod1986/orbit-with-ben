#!/usr/bin/env python3
"""Daily AI credit readings for the AI spend month (J0052, Ben 8 Oct 2026). Runs on the Mini at 08:30 London.

  python3 scripts/ai_spend_daily.py --dry-run          # read every pool, print, record nothing
  python3 scripts/ai_spend_daily.py --git              # read and record one `ai_spend.py record` per pool, push
  python3 scripts/ai_spend_daily.py --pools elevenlabs,vertex --git

Pools:
- elevenlabs: API `/v1/user/subscription` (character_count / character_limit). Key via el_client; never printed.
- flow:       the Flow page in the Mini's CDP Chrome (:9222), "N credits" text, as the HOS mint scripts read it.
- vertex:     Cloud Billing > Credits (all) in the same Chrome. Free Trial is `--left`; every credit line goes in --note.
- cursor:     cursor.com/dashboard/spending in the same Chrome: percent of the Cursor Models pool left this cycle
              (the page shows % used per pool and no $ since 12 Oct); Cursor Models and Grok Bot weekly go in --note.
              Since November 2026 the page shows one "Weekly included usage" figure with who used it: `left` is then
              the percent of that week left, and the note says so.
- codex:      the Codex CLI's own usage limits, from the newest `rate_limits` in ~/.codex/sessions (what /status shows):
              % of the weekly limit left, with the 5-hour window and both reset times in --note. No sign-in, no network.
              `--codex-pool codex-macbook` records the MacBook's separate account (scripts/macbook_worker.py does).
- claude:     claude.ai/settings/usage in the CDP Chrome (:9222): % of the weekly limit left, with the current session
              and weekly % used + reset times in --note.
- gemini:     the Antigravity `agy -p /usage` quota output on the Mini: % of the Gemini Models weekly limit left, with
              the 5-hour session and weekly % used + reset times in --note.

A pool whose read fails records nothing; the reason goes to the log (and stdout). Never guess a number.
Log: ~/Library/Logs/owb-ai-spend.log (launchd).

What the exit code means (J2564). Exit 1 says a spending figure is missing: a SPEND pool (elevenlabs, flow, vertex)
could not be read, or a reading could not be written. The usage pages (cursor, codex, claude, gemini) are a percent
of a plan's limit, not money: one that cannot be read is printed as UNREAD with its likely cause, what the page
shows now and when the pool was last recorded, and the run still exits 0. For three days the run ended in an error
over three usage pages while every spending figure was read, which hides the day a spending figure really is missing.
`--strict` also exits 1 for an unread usage page: the MacBook worker asks for one pool and must know if it was recorded.

The Flow page belongs to a picture run while one is going. The run and this reading find the same tab
(`cdp_tabs.reuse_page`), so the reading takes the runs' own lock first (FLOW_LOCK) and, when a run holds it, leaves
the tab alone and prints BUSY: the run records the balance itself.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import channels  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CDP = "http://127.0.0.1:9222"
BILLING_URL = "https://console.cloud.google.com/billing/0124D1-E6EFD6-40F6DA/credits/all?project=gen-lang-client-0538779324"
FLOW_URL = "https://flow.google.com/"
CURSOR_URL = "https://cursor.com/dashboard/spending"
CLAUDE_URL = "https://claude.ai/settings/usage"
ALL = ("elevenlabs", "flow", "vertex", "cursor", "codex", "claude", "gemini")
SPEND = ("elevenlabs", "flow", "vertex")  # credit or money: one of these unread fails the run. The rest are usage pages.
# The picture runs hold this lock for a whole batch (the channel's Flow runners, `SharedFlowAccounting`).
FLOW_LOCK = Path.home() / "_desk" / "state" / "flow" / "shared" / "writer.lock"
SEEN = {"url": "", "text": "", "links": []}  # the last page read in the CDP Chrome, kept so a failed reading can say what it showed
CODEX_HOME = Path.home() / ".codex"
CODEX_MAX_AGE_H = 72  # an older reading says nothing about this week's limit
CODEX_MAX_LOGS = 60


def voice_tools() -> Path:
    """The ElevenLabs helpers (el_auth, vo_take): the studio's own copy when its root has one (the voice tools are
    shared and move with the studio), else the first channel checkout that has them."""
    for base in (channels.ROOT, *(channels.checkout(slug) for slug in channels.slugs())):
        if base and base.joinpath("04_Audio", "tools", "el_auth.py").is_file():
            return base.joinpath("04_Audio", "tools")
    raise RuntimeError("neither the studio nor a channel checkout on this machine has 04_Audio/tools/el_auth.py")


def read_elevenlabs() -> dict:
    sys.path.insert(0, str(voice_tools()))
    from el_auth import load_token  # noqa: E402
    from vo_take import credits  # noqa: E402
    token, mode = load_token(prefer_api_key=True)
    c = credits(token, mode)
    if c["remaining"] is None:
        raise RuntimeError("subscription response had no character_count/character_limit")
    return {"left": c["remaining"], "total": c["limit"], "note": f"API subscription: used {c['used']} of {c['limit']}"}


def _page_text(url: str, wait_text: str | None, settle_ms: int = 3000, then=None) -> str:
    """Body text of `url` in the CDP Chrome. `then(page, text)` may click and return new text."""
    from playwright.sync_api import sync_playwright
    sys.path.insert(0, str(ROOT / "scripts"))
    from cdp_tabs import reuse_page, site  # noqa: E402
    with sync_playwright() as p:
        br = p.chromium.connect_over_cdp(CDP)
        page = reuse_page(br.contexts[0], site(url))
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        if wait_text:
            page.get_by_text(wait_text).first.wait_for(timeout=45000)
        page.wait_for_timeout(settle_ms)
        text = page.inner_text("body")
        SEEN.update(url=page.url, text=text)
        if then:
            text = then(page, text)
            SEEN.update(url=page.url, text=text)
        return text


class Busy(RuntimeError):
    """The page is in use by a picture run. Nothing was read, and nothing is wrong."""


@contextlib.contextmanager
def flow_page_free(lock: Path | None = None):
    """Hold the picture runs' lock while the Flow page is read; raise Busy when a run already holds it.

    A run that starts during the reading is refused by its own guard and can be started again a moment later; that is
    cheaper than a reading that navigates the tab a run is generating in."""
    lock = lock or FLOW_LOCK
    if not lock.parent.is_dir():  # no picture run has ever used this machine
        yield
        return
    import fcntl
    with open(lock, "a+") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Busy("a picture run holds the Flow page (the shared writer lock); it records the balance itself") from None
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


# The studio Ultra account, by fingerprint: no address sits in a tracked file (AGENTS.md Never list, J2537).
FLOW_ACCOUNT_SHA256 = "81a01c9d841483f444008cd69e98b26019e032ed75b5e33e17409a76c6525ce9"
FLOW_ACCOUNT_NAME = "the studio Ultra account"
# The account chip that opens the picker with the credit count, as the HOS Flow minters click it.
FLOW_PICKER = ('[aria-label*="Account details" i]', '[aria-label*="Google Account" i]',
               'button:has-text("ULTRA")', "text=ULTRA")
CREDITS_RE = re.compile(r"([\d,]{1,7})\s*(?:Google\s+Flow\s+|AI\s+)?credits", re.I)
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@(?:gmail|googlemail)\.com", re.I)


def is_flow_account(address: str) -> bool:
    return hashlib.sha256(address.strip().lower().encode()).hexdigest() == FLOW_ACCOUNT_SHA256


def flow_account_shown(text: str) -> bool:
    return any(is_flow_account(e) for e in EMAIL_RE.findall(text))


def parse_flow(text: str) -> int:
    hits = [int(m.group(1).replace(",", "")) for m in CREDITS_RE.finditer(text)]
    if not hits:
        raise RuntimeError("no 'N credits' text on the Flow page or its account picker (signed out, or the picker moved)")
    return hits[0]


def _flow_picker(page, text: str) -> str:
    """Open the account picker so the credit count and signed-in account are on the page."""
    if CREDITS_RE.search(text) and flow_account_shown(text):
        return text
    for sel in FLOW_PICKER:
        loc = page.locator(sel).first
        try:
            if loc.count() == 0:
                continue
            loc.click(timeout=2500)
        except Exception:  # noqa: BLE001
            continue
        page.wait_for_timeout(1500)
        aria = page.evaluate("() => [...document.querySelectorAll('[aria-label]')]"
                             ".map(e => e.getAttribute('aria-label') || '').join('\\n')") or ""
        text = page.inner_text("body") + "\n" + aria
        page.keyboard.press("Escape")
        break
    return text


def read_flow() -> dict:
    with flow_page_free():
        text = _page_text(FLOW_URL, None, settle_ms=8000, then=_flow_picker)
    if re.search(r"sign in to continue|you.?re not signed in", text, re.I):
        raise RuntimeError("Flow is signed out in the CDP Chrome")
    emails = {e.lower() for e in EMAIL_RE.findall(text)}
    ours = flow_account_shown(text)
    if emails and not ours:
        raise RuntimeError(f"Flow is signed in as another account ({len(emails)} seen, not the Ultra one)")
    who = FLOW_ACCOUNT_NAME if ours else "account not shown"
    return {"left": parse_flow(text), "note": f"Flow account picker credits ({who}, CDP :9222)"}


def _credit_status(cell: str) -> str:
    """The row's own status cell. Since 12 Oct 2026 an active credit near its end date reads "Expiring in N days"."""
    for word, status in (("Expired", "Expired"), ("Used", "Used"), ("Available", "Available")):
        if re.search(rf"\b{word}\b", cell):
            return status
    m = re.search(r"Expiring in \d+ days?", cell, re.I)
    return f"Available ({m.group(0).lower()})" if m else "?"


def parse_billing(text: str) -> tuple[float, str]:
    rows = [ln.strip() for ln in text.splitlines() if ln.strip()]
    lines, trial = [], None
    for i, ln in enumerate(rows):
        if re.fullmatch(r"(Free Trial|.*Developer Program.*|.*credit.*)", ln, re.I) and len(ln) < 90:
            window = " ".join(rows[i:i + 8])
            m = re.search(r"£([\d,]+\.\d\d)", window)
            if not m or ln.lower().startswith("credit application type") or re.search(r"CreditId|Credit-", ln):
                continue
            amt = float(m.group(1).replace(",", ""))
            status = _credit_status(" ".join(rows[i + 1:i + 3]))
            lines.append(f"{ln}: £{amt:.2f} {status}")
            if status.startswith("Available"):
                # Ben, 12 Oct 2026 23:51: the pool is every active promo credit (Free Trial + Developer Program
                # monthly), all scoped to Vertex on billing account 0124D1. Used/Expired rows count nothing.
                trial = (trial or 0.0) + amt
    if trial is None:
        raise RuntimeError("could not read an Available credit row on Cloud Billing > Credits")
    return round(trial, 2), "; ".join(dict.fromkeys(lines))


def read_vertex() -> dict:
    trial, lines = parse_billing(_page_text(BILLING_URL, "Free Trial", settle_ms=2500))
    return {"left": trial, "note": f"promo pool (all Available credits; jobs stop at £1 margin) · Cloud Billing > Credits: {lines}"}


CURSOR_POOLS = {"cursor models": "Cursor Models", "other models": "Other Models", "weekly usage": "Grok Bot weekly"}
# Up to six short "<who> N%" lines: the split of the week's usage the billing page shows since November 2026.
CURSOR_SPLIT = r"(?:[ \t]*\n[ \t]*[A-Za-z][A-Za-z .&-]{0,30}?[ \t]+\d{1,3}%[ \t]*){0,6}"


def parse_cursor(text: str) -> dict:
    """The /dashboard/spending page (12 Oct 2026): a percent used per pool, no $ figure.

    `left` is the percent left of Cursor Models, the pool the Mini's Cursor runs on (Auto, Composer): when it fills,
    usage overflows into Other Models, which also carries Claude-in-Cursor. Until 14 Oct `left` was Other Models, so the
    board read "Cursor 0%" while Cursor's own models were 86% free (Ben, 14 Oct 2026: "plenty left in cursor").
    Other Models (Claude-in-Cursor, flagged in scripts/credit_flags.json when used up) and the reset dates go in the note."""
    rows = [ln.strip() for ln in text.splitlines() if ln.strip()]
    used: dict[str, int] = {}
    label = None
    for ln in rows:
        key = next((k for k in CURSOR_POOLS if ln.lower().startswith(k)), None)
        if key:
            label = key
            continue
        m = re.fullmatch(r"(\d{1,3})%\s+used", ln, re.I)
        if m and label and label not in used:
            used[label] = int(m.group(1))
            label = None
    if "other models" not in used and "cursor models" not in used:
        # 11 Nov 2026 (J2580): the page now lists who used the week between the figure and its label, one per line
        # ("30%", "used", "x", "Grok Bot 29%", "Cursor 1%", "Weekly included usage"). Those lines are read, not skipped.
        m_wk = re.search(
            r"(?:(\d{1,3})%\s+used(?:\s+\S)?(" + CURSOR_SPLIT + r")\s+Weekly included usage|Weekly included usage\s+(\d{1,3})%\s+used)"
            r"(?:\s*(?:x\s+)?[·•]?\s*Resets\s+([^\n(]+))?",
            text,
            re.I,
        )
        if not m_wk:
            raise RuntimeError("no 'Cursor Models' or 'Other Models · N% used' line on the Cursor spending page (signed out, or the page changed)")
        pct = int(m_wk.group(1) or m_wk.group(3))
        split = [(name.strip(), int(n)) for name, n in re.findall(r"([A-Za-z][A-Za-z .&-]*?)[ \t]+(\d{1,3})%", m_wk.group(2) or "")]
        used["weekly included usage"] = pct
        used.update({name.lower(): n for name, n in split})
        by = " (" + ", ".join(f"{name} {n}%" for name, n in split) + ")" if split else ""
        bits = [f"Weekly included usage {pct}% used{by}"]
        if m_wk.group(4):
            bits.append(f"weekly resets {m_wk.group(4).strip()}")
        m_mo = re.search(r"(\$[\d,]+(?:\.\d\d)?)\s+used this month(?:\s+Resets\s+([^\n(]+))?", text, re.I)
        if m_mo:
            bits.append(f"{m_mo.group(1)} used this month" + (f" (resets {m_mo.group(2).strip()})" if m_mo.group(2) else ""))
        m_cr = re.search(r"Credits available\s+(\$[\d,]+(?:\.\d\d)?)", text, re.I)
        if m_cr:
            bits.append(f"credits available {m_cr.group(1)}")
        return {"left": max(0, 100 - pct), "total": 100, "used": used, "note": "; ".join(bits), "of": "the weekly included usage"}
    reset = re.search(r"Usage limits reset on ([^\n(]+?)\s*(?:\(|\n|$)", text)
    weekly = re.search(r"Weekly usage\s+\d{1,3}%\s+used\s+Resets ([^\n(]+?)\s*(?:\(|\n|$)", text)
    bits = [f"{CURSOR_POOLS[k]} {used[k]}% used" for k in CURSOR_POOLS if k in used]
    if reset:
        bits.append(f"limits reset {reset.group(1).strip()}")
    if weekly:
        bits.append(f"weekly resets {weekly.group(1).strip()}")
    return {"left": 100 - used.get("cursor models", used.get("other models", 0)), "total": 100, "used": used,
            "note": "; ".join(bits)}


def _cursor_settle(page, text: str) -> str:
    """Wait for the client-side redirect from cursor.com/dashboard/spending to grok.com/dashboard/billing to render."""
    for _ in range(2):
        if re.search(r"\d{1,3}%\s+used", text, re.I):
            return text
        if "grok.com" not in page.url:
            page.goto("https://grok.com/dashboard/billing", wait_until="domcontentloaded", timeout=30000)
        try:
            page.get_by_text("Weekly included usage").first.wait_for(timeout=12000)
        except Exception:  # noqa: BLE001
            pass
        page.wait_for_timeout(2000)
        text = page.inner_text("body")
    return text


def read_cursor() -> dict:
    text = _page_text(CURSOR_URL, None, settle_ms=8000, then=_cursor_settle)
    if re.search(r"\bsign in\b|\blog in\b", text[:2000], re.I) and not re.search(r"\d{1,3}%\s+used", text, re.I):
        raise RuntimeError("Cursor dashboard is signed out in the CDP Chrome")
    r = parse_cursor(text)
    return {"left": r["left"], "total": r["total"],
            "note": f"Cursor spending page, % of {r.get('of', 'Cursor Models')} left: {r['note']} (CDP :9222)"}


def flow_refill(r: dict, last_left: float | None) -> dict:
    """A Flow balance above the last recorded one is the monthly refill: record it as --total (J0052 step 2)."""
    if last_left is not None and r.get("total") is None and r["left"] > last_left:
        return {**r, "total": r["left"], "note": f"{r['note']}; refill from {last_left:g} (monthly allotment)"}
    return r


def last_left(pool: str) -> float | None:
    sys.path.insert(0, str(ROOT / "scripts"))
    from ai_spend import load  # noqa: E402
    rows = [x for x in load() if x.get("kind") == "record" and x.get("pool") == pool and x.get("left") is not None]
    return float(rows[-1]["left"]) if rows else None


def _window(w: dict, at: datetime) -> tuple[float, str]:
    """(used %, reset time UTC) of one Codex rate-limit window; newer CLIs give resets_at, older resets_in_seconds."""
    used = float(w["used_percent"])
    if w.get("resets_at") is not None:
        reset = datetime.fromtimestamp(float(w["resets_at"]), timezone.utc)
    elif w.get("resets_in_seconds") is not None:
        reset = at + timedelta(seconds=float(w["resets_in_seconds"]))
    else:
        return used, ""
    return used, reset.strftime("%a %d %b %H:%MZ")


def parse_codex(lines, now: datetime | None = None) -> dict:
    """The newest Codex `rate_limits` reading among session log lines, as a pool reading (weekly % left of 100)."""
    now = now or datetime.now(timezone.utc)
    best = None
    mentions = 0
    for line in lines:
        if '"rate_limits"' not in line:
            continue
        mentions += 1
        try:
            row = json.loads(line)
        except ValueError:
            continue
        payload = row.get("payload") or row.get("msg") or row
        rl = payload.get("rate_limits") or (payload.get("info") or {}).get("rate_limits")
        if not isinstance(rl, dict) or not rl.get("secondary") and not rl.get("primary"):
            continue
        try:
            at = datetime.fromisoformat(str(row.get("timestamp", "")).replace("Z", "+00:00"))
        except ValueError:
            continue
        if best is None or at > best[0]:
            best = (at, rl)
    if best is None:
        raise ValueError("no rate_limits reading in the Codex session logs "
                         f"(lines with rate_limits: {mentions}; none holds a limit window)")
    at, rl = best
    if now - at > timedelta(hours=CODEX_MAX_AGE_H):
        raise ValueError(f"newest Codex reading is {(now - at).total_seconds() / 3600:.0f} h old")
    weekly = rl.get("secondary") or rl.get("primary")
    used, reset = _window(weekly, at)
    note = f"weekly {used:g}% used" + (f", resets {reset}" if reset else "")
    if rl.get("secondary") and rl.get("primary"):
        u5, r5 = _window(rl["primary"], at)
        note += f"; 5-hour {u5:g}% used" + (f", resets {r5}" if r5 else "")
    note += f"; read from the Codex log at {at:%d %b %H:%MZ}"
    return {"left": round(max(0.0, 100 - used), 1), "total": 100.0, "note": note}


def read_codex(home: Path | None = None) -> dict:
    sessions = sorted((home or CODEX_HOME).glob("sessions/**/*.jsonl"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not sessions:
        raise ValueError(f"no Codex session logs under {home or CODEX_HOME}")
    lines = []
    oldest = datetime.now(timezone.utc).timestamp() - CODEX_MAX_AGE_H * 3600
    # Every run inside the window, newest first: a short run can end without a limit reading, so five was too few.
    for f in [s for s in sessions if s.stat().st_mtime >= oldest][:CODEX_MAX_LOGS] or sessions[:1]:
        lines += [ln for ln in f.read_text(errors="replace").splitlines() if '"rate_limits"' in ln]
    return parse_codex(lines)


def _claude_block(text: str, start_re: str, stop_re: str) -> tuple[int, str] | None:
    m = re.search(start_re, text, re.I | re.M)
    if not m:
        return None
    tail = text[m.end():]
    end = re.search(stop_re, tail, re.I | re.M)
    chunk = tail[:end.start()] if end else tail[:600]
    m_pct = re.search(r"(\d{1,3})%\s*used", chunk, re.I)
    if not m_pct:
        return None
    # The time sits on the "Resets" line. With no session running the line is bare, and reading on into the next
    # line gave "resets 0% used" in the ledger notes of 6 to 8 Nov 2026.
    m_res = re.search(r"Resets[ \t]+(?:on[ \t]+|at[ \t]+)?([^\n(·•]+)", chunk, re.I)
    reset = m_res.group(1).strip().rstrip(".") if m_res else ""
    if re.fullmatch(r"\d{1,3}%\s*used", reset, re.I):
        reset = ""
    return int(m_pct.group(1)), reset


def parse_claude(text: str) -> dict:
    """The claude.ai/settings/usage page: % used of the current session and the weekly limit, and their reset times."""
    m_sess = re.search(r"^\s*Current\s+session\b", text, re.I | re.M)
    if not m_sess:
        raise RuntimeError("no 'Current session' or weekly 'N% used' line on the Claude usage page (signed out, or the page changed)")
    sess = _claude_block(
        text[m_sess.start():],
        r"^\s*Current\s+session\b",
        r"^\s*(?:This\s+week|Current\s+week|Weekly\s+limits?|All\s+models|Sonnet\s+only|Limit\s+resets|Usage\s+credits|Extra\s+usage|Monthly\s+spend\s+limit|Spend\s+limit)\b",
    )
    wk = _claude_block(
        text[m_sess.end():],
        r"^\s*(?:This\s+week\s*(?:\(all\s+models\))?|Current\s+week\s*(?:\(all\s+models\))?|All\s+models|Weekly\s+limits?)\b",
        r"^\s*(?:This\s+week\s*\(Sonnet|Current\s+week\s*\(Sonnet|Sonnet\s+only|Limit\s+resets|Usage\s+credits|Claude\s+Code|Extra\s+usage|Monthly\s+spend\s+limit|Spend\s+limit|On-demand)\b",
    )
    if not sess or not wk:
        raise RuntimeError("no 'Current session' or weekly 'N% used' line on the Claude usage page (signed out, or the page changed)")
    s_pct, s_res = sess
    w_pct, w_res = wk
    s_part = f"{s_pct}% used" + (f" (resets {s_res})" if s_res else "")
    note = f"{s_part} session; weekly {w_pct}% used" + (f", resets {w_res}" if w_res else "")
    return {
        "left": max(0, 100 - w_pct),
        "total": 100,
        "used": {"session": s_pct, "weekly": w_pct},
        "note": note,
    }


CLAUDE_PATH = "/settings/usage"


def settings_links(hrefs, limit: int = 12) -> list[str]:
    """The links on a page that mention settings or usage, as paths: no host, no query, no repeats. Kept so that a
    reading that was sent to another page can say where the usage page may have gone (J2580)."""
    out = []
    for h in hrefs or []:
        path = re.sub(r"^https?://[^/]+", "", re.sub(r"[?#].*$", "", str(h or "")))[:80]
        if path and re.search(r"settings|usage", path, re.I) and path not in out:
            out.append(path)
    return out[:limit]


def _links(page) -> list[str]:
    try:
        return settings_links(page.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href') || '')"))
    except Exception:  # noqa: BLE001
        return []


def _claude_settle(page, text: str) -> str:
    """Wait for the usage figures. On 11 Nov 2026 the usage address ended on the new-chat page with no figures
    (J2566): if the browser is not on the usage page, note the links that page offers and ask for the usage address
    once more, since the app can land on the new-chat page on a cold start."""
    for _ in range(2):
        if re.search(r"\d{1,3}%\s*used", text, re.I) or "login" in page.url:
            return text
        if CLAUDE_PATH not in page.url:
            SEEN["links"] = _links(page) or SEEN.get("links") or []
            try:
                page.goto(CLAUDE_URL, wait_until="domcontentloaded", timeout=30000)
            except Exception:  # noqa: BLE001
                pass
        try:
            page.get_by_text("Current session").first.wait_for(timeout=10000)
        except Exception:  # noqa: BLE001
            pass
        page.wait_for_timeout(2000)
        text = page.inner_text("body")
    if CLAUDE_PATH not in page.url:
        SEEN["links"] = _links(page) or SEEN.get("links") or []
    return text


def claude_sent_elsewhere(url: str, text: str) -> bool:
    """The browser asked for the usage page and ended on another one, with no usage figure on it."""
    return bool(url) and CLAUDE_PATH not in url and not re.search(r"\d{1,3}%\s*used", text, re.I)


def read_claude() -> dict:
    text = _page_text(CLAUDE_URL, None, settle_ms=6000, then=_claude_settle)
    if re.search(r"continue with google|continue with email|\bsign in\b|\blog in\b", text[:2000], re.I) and not re.search(r"\d{1,3}%\s*used", text, re.I):
        raise RuntimeError("claude.ai is signed out in the CDP Chrome")
    if claude_sent_elsewhere(SEEN["url"], text):
        raise RuntimeError(f"the Claude usage address sent the browser to {page_address(SEEN['url'])}, not to the usage page")
    r = parse_claude(text)
    return {"left": r["left"], "total": r["total"], "note": r["note"]}


GEMINI_LIMIT_RE = re.compile(
    r"Gemini\s+Models\s+(Weekly|Five\s+Hour)\s+Limit\s+(Remaining|Used)\s+(\d{1,3})%(?:\s+([^\n]+))?",
    re.I,
)


def _gemini_reset(raw: str, time_only: bool = False) -> str:
    s = raw.strip()
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M GMT", "%Y-%m-%d %H:%M UTC"):
        try:
            dt = datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
            return dt.strftime("%H:%MZ" if time_only else "%a %d %b %H:%MZ")
        except ValueError:
            continue
    return s


def parse_gemini(text: str) -> dict:
    """The Antigravity `agy -p /usage` quota output for Gemini Models (weekly + 5-hour % remaining and reset times)."""
    windows: dict[str, tuple[int, str]] = {}
    for line in text.splitlines():
        m = GEMINI_LIMIT_RE.search(line)
        if not m:
            continue
        kind = "weekly" if m.group(1).lower().startswith("week") else "five_hour"
        pct = int(m.group(3))
        left_pct = pct if m.group(2).lower() == "remaining" else max(0, 100 - pct)
        reset_raw = (m.group(4) or "").strip()
        windows[kind] = (left_pct, reset_raw)
    if "weekly" not in windows:
        raise RuntimeError("no 'Gemini Models · Weekly Limit' line in agy /usage output")
    w_left, w_res_raw = windows["weekly"]
    w_used = max(0, 100 - w_left)
    w_res = _gemini_reset(w_res_raw, time_only=False) if w_res_raw else ""
    used = {"weekly": w_used}
    if "five_hour" in windows:
        f_left, f_res_raw = windows["five_hour"]
        f_used = max(0, 100 - f_left)
        f_res = _gemini_reset(f_res_raw, time_only=True) if f_res_raw else ""
        used["five_hour"] = f_used
        sess = f"5-hour {f_used}% used" + (f" (resets {f_res})" if f_res else "")
        note = f"{sess} session; weekly {w_used}% used" + (f", resets {w_res}" if w_res else "")
    else:
        note = f"weekly {w_used}% used" + (f", resets {w_res}" if w_res else "")
    return {"left": w_left, "total": 100, "used": used, "note": note}


def _agy_bin() -> str:
    for cand in (os.environ.get("AGY_BIN"), shutil.which("agy"), str(Path.home() / ".local" / "bin" / "agy")):
        if cand and Path(cand).is_file():
            return str(cand)
    raise RuntimeError("agy CLI not found on PATH or ~/.local/bin/agy")


def read_gemini() -> dict:
    p = subprocess.run([_agy_bin(), "-p", "/usage", "--print-timeout", "30s"],
                       capture_output=True, text=True, timeout=45)
    out = (p.stdout or "") + "\n" + (p.stderr or "")
    if p.returncode != 0 and "Gemini Models" not in out:
        raise RuntimeError(f"agy -p /usage exited {p.returncode}: {out.strip()[:200]}")
    r = parse_gemini(out)
    return {"left": r["left"], "total": r["total"], "note": r["note"]}


READERS = {"elevenlabs": read_elevenlabs, "flow": read_flow, "vertex": read_vertex, "cursor": read_cursor,
           "codex": read_codex, "claude": read_claude, "gemini": read_gemini}


SIGN_IN_RE = re.compile(r"\bsign in\b|\blog in\b|continue with google|continue with email", re.I)
ANY_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PRIVATE_LINE_RE = re.compile(r"\bcard\b|visa|mastercard|amex|billing address|invoice|payment method|[•*]{4}", re.I)


def likely_cause(err: str, page: str = "") -> str:
    """Why a reading failed, in words the log's reader can act on. `page` is what the page showed, when there was one."""
    e = err.lower()
    if "signed out in the cdp chrome" in e or "signed in as another account" in e:
        return "signed out in this machine's browser; it needs Ben's sign-in"
    if "sent the browser to" in e:
        return ("signed in, but the site sent the browser to another page: the usage page has moved, or it opens "
                "another way now; the reader needs the new address (the page's own links are below)")
    if "the page changed" in e or "picker moved" in e:
        if not page.strip():
            return "the page came back empty; signed out, or it did not load"
        if SIGN_IN_RE.search(page[:2000]):
            return "the page shows a sign-in screen; it needs Ben's sign-in"
        return "signed in, but the page's wording is not what the reader expects; the reader needs a fix (the page's text is below)"
    if "no codex session logs" in e:
        return "Codex has not run on this machine"
    if "no rate_limits reading" in e:
        return "the Codex runs on this machine in the last three days wrote no limit reading"
    if "h old" in e and "codex" in e:
        return "Codex has not run on this machine for three days"
    if "agy cli not found" in e:
        return "the Antigravity command-line tool is not installed on this machine"
    if "econnrefused" in e or "connect_over_cdp" in e or "connection refused" in e:
        return "this machine's browser is not answering on its debugging port"
    if "timeout" in e:
        return "the page did not load in time"
    return "not known; the error above is all there is"


def page_excerpt(text: str, limit: int = 25) -> list[str]:
    """The first lines of a page, safe to keep in a log: no email address, no payment line."""
    out = []
    for ln in (x.strip() for x in text.splitlines()):
        if not ln or PRIVATE_LINE_RE.search(ln):
            continue
        out.append(ANY_EMAIL_RE.sub("<email>", ln)[:120])
        if len(out) == limit:
            break
    return out


def page_address(url: str) -> str:
    """Host and path only: a query string can carry an account or project id."""
    m = re.match(r"https?://([^/?#]+)([^?#]*)", url or "")
    return (m.group(1) + m.group(2)) if m else ""


def last_record(pool: str) -> dict | None:
    sys.path.insert(0, str(ROOT / "scripts"))
    from ai_spend import load  # noqa: E402
    rows = [x for x in load() if x.get("kind") == "record" and x.get("pool") == pool and x.get("left") is not None]
    return rows[-1] if rows else None


def last_recorded(pool: str, now: datetime | None = None) -> str:
    """When the pool was last recorded and by whom, so an unread page says whether the board's figure is fresh."""
    try:
        row = last_record(pool)
    except Exception as e:  # noqa: BLE001  (the ledger being unreadable must not hide the reading's own failure)
        return f"the ledger could not be read ({type(e).__name__})"
    if not row:
        return "never recorded"
    try:
        at = datetime.fromisoformat(str(row.get("at", "")).replace("Z", "+00:00"))
        if at.tzinfo is None:
            at = at.replace(tzinfo=timezone.utc)
    except ValueError:
        return f"last recorded {row.get('at')} by {row.get('by') or '?'}"
    hours = ((now or datetime.now(timezone.utc)) - at).total_seconds() / 3600
    age = f"{hours:.0f} h ago" if hours < 48 else f"{hours / 24:.0f} days ago"
    return f"last recorded {at:%d %b %H:%MZ} by {row.get('by') or '?'} ({age})"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pools", default=",".join(ALL))
    ap.add_argument("--by", default="mini-daily")
    ap.add_argument("--codex-pool", default="codex", help="pool the codex reading is recorded as (codex-macbook on the MacBook)")
    ap.add_argument("--git", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 for a usage page that was not read too (for a caller that asked for one pool and must know)")
    a = ap.parse_args(argv)
    read, failed, unread, busy = [], [], [], []
    for pool in [p.strip() for p in a.pools.split(",") if p.strip()]:
        SEEN.update(url="", text="", links=[])
        recorded_as = a.codex_pool if pool == "codex" else pool
        try:
            r = READERS[pool]()
            if pool == "flow":
                r = flow_refill(r, last_left("flow"))
        except Busy as e:  # the page is a picture run's for now: not a failure of anything
            busy.append(pool)
            print(f"BUSY {pool}: {e} · {last_recorded(recorded_as)}", flush=True)
            continue
        except Exception as e:  # one pool failing never blocks the others
            err = f"{type(e).__name__}: {str(e)[:300]}"
            cause = likely_cause(err, SEEN["text"])
            if pool in SPEND:
                failed.append(pool)
                print(f"FAIL {pool}: {err} · likely cause: {cause}", flush=True)
            else:
                unread.append(pool)
                print(f"UNREAD {pool}: {err} · likely cause: {cause} · {last_recorded(recorded_as)}", flush=True)
            if SEEN["text"].strip():
                print(f"  page address: {page_address(SEEN['url'])}", flush=True)
                for ln in page_excerpt(SEEN["text"]):
                    print(f"  page shows: {ln}", flush=True)
                for link in SEEN.get("links") or []:
                    print(f"  page links to: {link}", flush=True)
            continue
        read.append(pool)
        print(f"READ {pool}: left={r['left']} total={r.get('total')} · {r['note']}", flush=True)
        if a.dry_run:
            continue
        cmd = [sys.executable, str(ROOT / "scripts" / "ai_spend.py"), "record", "--pool", a.codex_pool if pool == "codex" else pool,
               "--left", str(r["left"]), "--note", r["note"], "--by", a.by]
        if r.get("total") is not None:
            cmd += ["--total", str(r["total"])]
        if a.git:
            cmd.append("--git")
        if subprocess.run(cmd, cwd=ROOT).returncode != 0:
            failed.append(f"{pool} (read, but the reading could not be written)")
            print(f"FAIL {pool}: the reading could not be written to the ledger", flush=True)
    parts = [f"{len(read)} read"]
    if busy:
        parts.append("left alone for a picture run: " + ", ".join(busy))
    if unread:
        parts.append("usage pages not read (no spending figure is missing): " + ", ".join(unread))
    if failed:
        parts.append("SPENDING FIGURE MISSING: " + ", ".join(failed))
    elif any(p in SPEND for p in read):
        parts.append("every spending figure read was recorded" if not a.dry_run else "every spending figure asked for was read")
    print("SUMMARY " + "; ".join(parts), flush=True)
    return 1 if failed or (a.strict and unread) else 0


if __name__ == "__main__":
    sys.exit(main())
