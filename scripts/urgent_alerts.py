"""Urgent watch/schedule alerts. Called under board_publish's single-writer lock.

No phone setup is performed here. Optional ntfy URL is read only from the
publisher environment, after Claude has relayed the proposal to Ben.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

UTC = dt.timezone.utc
LONDON = ZoneInfo('Europe/London')


def parse(value):
    try:
        value = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
        return value if value.tzinfo else value.replace(tzinfo=UTC)
    except (ValueError, TypeError):
        return None


def identity(*parts):
    return hashlib.sha256(json.dumps(parts, sort_keys=True).encode()).hexdigest()[:24]


def evaluate(board, jobs, state, now, site):
    """Return active banners and delivery slots; reserve each slot before I/O.

    A missing card is unknown, never evidence that a video was pulled. A first
    run establishes the schedule baseline. History survives restarts so neither
    a resolved event nor a failed/ambiguous network call floods the phone.
    """
    state.setdefault('events', {})
    previous = state.setdefault('videos', {})
    videos = (board.get('tracker') or {}).get('videos') or []
    job_map = {j['id']: j for j in jobs}
    active = {}
    watches = [v for v in videos if v.get('ask') and
               job_map.get(v['ask'].get('job'), {}).get('status') not in ('done', 'cancelled')]
    current = {}
    for v in videos:
        key = v.get('key')
        if not key:
            continue
        yt = v.get('youtube') or {}
        current[key] = {'youtube': dict(yt), 'title': v.get('title') or key, 'channel': v.get('channel')}
        ask = v.get('ask') or {}
        due = parse(ask.get('due'))
        job = job_map.get(ask.get('job'))
        if ask and job and job.get('status') not in ('done', 'cancelled') and due:
            if due <= now + dt.timedelta(hours=12):
                eid = identity('watch', ask.get('job'), key, ask.get('version'), ask.get('file'), ask.get('due'))
                active[eid] = {'kind': 'watch', 'key': key, 'due': due.isoformat(),
                    'message': f"{v.get('title') or key} needs your watch by {due.astimezone(LONDON):%a %d %b %H:%M} London.",
                    'url': site + '/#uat=' + urllib.parse.quote(key, safe='')}
        old = previous.get(key, {})
        was = old.get('youtube') or {}
        air = parse(was.get('publishAt'))
        changed = bool(yt) and (yt.get('videoId') != was.get('videoId') or yt.get('publishAt') != was.get('publishAt')
                   or yt.get('state') not in ('scheduled', 'live'))
        if was.get('state') == 'scheduled' and air and now <= air <= now + dt.timedelta(hours=24) and changed and yt.get('state') != 'live':
            eid = identity('schedule', key, was, yt)
            watch = next((w for w in watches if w.get('key') == key), None)
            if watch is None:
                watch = next((w for w in watches if w.get('channel') == v.get('channel') and
                              w.get('key', '').split(':S:')[0] == key.split(':S:')[0]), None)
            watch_due = parse((watch or {}).get('ask', {}).get('due'))
            instruction = (f"The fixed version needs your watch by {watch_due.astimezone(LONDON):%a %d %b %H:%M} London."
                           if watch_due else "Open the board for the replacement and watch instructions.")
            active[eid] = {'kind': 'schedule', 'key': key, 'originalId': was.get('videoId'), 'watchJob': (watch or {}).get('ask', {}).get('job'), 'due': min(air, watch_due or air).isoformat(), 'slot': air.isoformat(),
                'message': f"{v.get('title') or key} was pulled, unscheduled or replaced before {air.astimezone(LONDON):%a %d %b %H:%M} London. {instruction}",
                'url': site + ('/#uat=' + urllib.parse.quote(watch['key'], safe='') if watch else '/#review')}
    # Keep an observed schedule change visible until its original slot, unless
    # the same cut regains that slot or a replacement is scheduled there.
    for eid, event in state['events'].items():
        if event.get('kind') != 'schedule' or parse(event.get('due')) <= now:
            continue
        if event.get('watchJob') and job_map.get(event['watchJob'], {}).get('status') in ('done', 'cancelled'):
            continue
        restored = any(parse((v.get('youtube') or {}).get('publishAt')) == parse(event.get('slot') or event['due']) and
                       (v.get('youtube') or {}).get('state') in ('scheduled', 'live') and
                       v.get('channel') == previous.get(event['key'], {}).get('channel') and
                       (v.get('key') != event['key'] or (v.get('youtube') or {}).get('videoId') == event.get('originalId')) for v in videos)
        if not restored:
            active.setdefault(eid, {k: event[k] for k in ('kind', 'key', 'due', 'message', 'url', 'originalId', 'watchJob', 'slot')})
    state['videos'] = {**previous, **current}
    banners, deliveries = [], []
    for eid, event in active.items():
        saved = state['events'].setdefault(eid, {**event, 'first': now.isoformat(), 'sent': 0})
        due = parse(saved['due'])
        half = parse(saved['first']) + max(due - parse(saved['first']), dt.timedelta()) / 2
        # An overdue watch still raises its first alert, but has no remaining
        # time in which to send a useful reminder.
        send = saved['sent'] == 0 or (saved['sent'] == 1 and now >= half and now < due)
        banners.append({**event, 'id': eid})
        if send:
            saved['sent'] += 1
            deliveries.append({**event, 'id': eid, 'reminder': saved['sent'] == 2})
    return banners, deliveries


def deliver(event, root):
    text = ('Reminder: ' if event['reminder'] else '') + event['message'] + ' ' + event['url']
    phone = os.environ.get('STUDIO_URGENT_NTFY_URL', '')
    result = {}
    if phone:
        # Fixed free service only; no arbitrary endpoints or billing fallback.
        if not phone.startswith('https://ntfy.sh/') or '?' in phone or '#' in phone:
            result['phone'] = 'invalid configuration'
        else:
            try:
                req = urllib.request.Request(phone, data=text.encode(), method='POST',
                    headers={'Title': 'Studio needs your attention', 'Click': event['url']})
                with urllib.request.urlopen(req, timeout=10) as response:
                    result['phone'] = str(response.status)
            except Exception:
                result['phone'] = 'delivery unconfirmed; no automatic retry'
    else:
        result['phone'] = 'not configured; board and thread fallback'
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', dir=root / 'jobs', delete=False) as f:
            f.write('[MacBook/Studio alert] ' + text)
            path = Path(f.name)
        try:
            r = subprocess.run([sys.executable, str(root / 'scripts/studio_thread.py'), 'post', '-f', str(path)],
                               capture_output=True, timeout=30)
            result['thread'] = 'posted' if r.returncode == 0 else 'delivery unconfirmed'
        finally:
            path.unlink(missing_ok=True)
    except Exception:
        result['thread'] = 'delivery unconfirmed'
    return result


def update(board, jobs, path, now, site, root, dry_run=False):
    try:
        state = json.loads(path.read_text())
    except FileNotFoundError:
        state = {}
    banners, events = evaluate(board, jobs, state, now, site)
    board['urgentAlerts'] = banners
    if dry_run:
        return
    # Reserve before sending: at most two attempts per event, even on a crash.
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(state))
    tmp.replace(path)
    for event in events:
        state['events'][event['id']]['delivery'] = deliver(event, root)
    tmp.write_text(json.dumps(state))
    tmp.replace(path)
