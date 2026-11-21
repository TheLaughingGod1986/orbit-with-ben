#!/usr/bin/env python3
"""Queue one daily all-channel sweep and deduplicated urgent Chief fixes. No YouTube writes."""
from __future__ import annotations
from datetime import datetime, timedelta
import json
from pathlib import Path
import sys
from zoneinfo import ZoneInfo
import channels

ROOT = Path(__file__).resolve().parent.parent


def queue_daily(data, at):
    import jobs
    day = at.astimezone(ZoneInfo('Europe/London')).date().isoformat()
    # Incomplete sweeps stay visible and retryable rather than creating duplicate work.
    existing = [j for j in data['jobs'] if j.get('scheduled_gate_sweep')]
    if any(j.get('scheduled_gate_sweep') == day or j.get('status') in ('open', 'claimed', 'blocked') for j in existing):
        return []
    j = jobs.do_add(data, title='Check every scheduled video in the next fourteen days', needs='mini',
        body='Run python3 scripts/scheduled_gates.py --apply --git. Re-run current blocking gates on every registered channel, Shorts and longs. No uploads, schedule or privacy changes. Report missing inputs as coverage failures; do not call them PASS.',
        by='refill', at=at, kind='assembly', action='Run the all-channel fourteen-day scheduled-video gate sweep',
        due=(at + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%MZ'))
    j['scheduled_gate_sweep'] = day
    j['plain'] = 'Check that every video due in the next two weeks is ready to air'
    return [j['id']]


def queue_fixes(data, findings, at):
    import jobs
    added = []
    for row in findings:
        when = datetime.fromisoformat(row['publishAt'].replace('Z', '+00:00'))
        if row['ok'] or not at <= when <= at + timedelta(days=7):
            continue
        key = f"{row['channel']}:{row['id']}"
        if any(j.get('scheduled_gate_fix') == key and j.get('status') in ('open', 'claimed', 'blocked') for j in data['jobs']):
            continue
        j = jobs.do_add(data, title=f"Urgent scheduled-video gate fix: {row['channel']} {row['id']}",
            needs='any', kind='chief', repo=row['channel'], by='refill', at=at,
            due=min(when, at + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%MZ'),
            action='Resolve the scheduled video gate findings before it airs',
            body=f"Airs {row['publishAt']}. Current blocking checks failed or could not run.\n{row['output']}\n"
                 'Chief: assign the repair immediately. If a new finished cut is needed, use the existing awaits_ben watch/alert flow with its actual deadline. Metadata, missing inputs or waivers alone do not alert Ben. No automatic privacy or schedule change.')
        j['scheduled_gate_fix'] = key
        j['plain'] = 'Fix a readiness problem on a video airing this week'
        added.append(j['id'])
    return added


def sweep():
    import importlib.util
    path = ROOT / '00_Brand/Channel-Setup/tools/gate_upcoming.py'
    spec = importlib.util.spec_from_file_location('scheduled_upcoming', path)
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    findings = []
    for slug in channels.slugs():
        repo = channels.repo_path(slug)
        data = channels.analytics_dir(slug)
        snapshots = sorted((data / 'snapshots').glob('*.json'))
        uploads = channels.uploads_file(slug)
        if channels.get(slug).get('launch_state') == 'prelaunch' and not snapshots:
            continue
        if not repo or not snapshots or not uploads or not uploads.is_file():
            raise RuntimeError(f'{slug}: missing checkout, snapshot or upload register; sweep incomplete')
        latest = snapshots[-1]
        # Never claim current schedule coverage from an old snapshot.
        now = datetime.now().astimezone()
        taken = datetime.fromisoformat(json.loads(latest.read_text()).get('takenAt', '').replace('Z', '+00:00'))
        if not taken.tzinfo or not 0 <= (now - taken).total_seconds() <= 36 * 3600:
            raise RuntimeError(f'{slug}: snapshot older than 36 hours; sweep incomplete')
        report = data / 'UPCOMING_PUBLISHING_GATES.md'
        result = gate.main(['--snapshot', str(latest), '--uploads', str(uploads), '--media-root', str(repo), '--out', str(report)])
        if result:
            raise RuntimeError(f'{slug}: sweep failed')
        findings += [dict(r, channel=slug) for r in json.loads(report.with_suffix('.json').read_text())]
    return findings


def main():
    import argparse
    import jobs
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--apply', action='store_true')
    p.add_argument('--git', action='store_true')
    a = p.parse_args()
    findings = sweep()
    print(json.dumps(findings, indent=2))
    if a.apply:
        at = jobs.now()
        if a.git:
            _, err = jobs.with_git(lambda d: (queue_fixes(d, findings, at), None, []), 'jobs: urgent scheduled-video gate findings')
            if err:
                raise RuntimeError(err)
        else:
            data = jobs.load()
            queue_fixes(data, findings, at)
            jobs.save(data)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
