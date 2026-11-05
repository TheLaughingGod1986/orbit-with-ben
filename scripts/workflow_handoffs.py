"""Read-only stage/queue reconciliation. Findings request decisions, never grant approvals."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import workflow_state as workflow


def records(films):
    for path in sorted(Path(films).glob('*/status.json')):
        try:
            record = json.loads(path.read_text())
            if not isinstance(record, dict) or not isinstance(record.get('stages', {}), dict):
                raise ValueError('invalid stage record')
            yield path.parent.name.split('_')[0], record
        except (OSError, ValueError) as error:
            yield path.parent.name.split('_')[0], {'record_error': str(error)}


WIP = Path(__file__).resolve().parents[1] / 'jobs' / 'WIP.json'


def waiting_films(path=WIP):
    """OWB films parked in the idea list by Ben's WIP limit (G, 4 Nov 2026): not in production, so not orphans."""
    try:
        return {f.split(':', 1)[1] for f in json.loads(Path(path).read_text()).get('next', []) if str(f).startswith('OWB:')}
    except (OSError, ValueError, AttributeError):
        return set()


def findings(data, film_records, at, exclude=(), waiting=None):
    rows = [j for j in data.get('jobs', []) if j.get('id') not in exclude]
    waiting = waiting_films() if waiting is None else set(waiting)
    out = []
    for film, record in film_records:
        if film in waiting:
            continue
        stages = record.get('stages', {})
        # Completed/published films may have legitimate follow-up work. Do not restart production.
        upload = stages.get('upload') or {}
        if isinstance(upload, dict) and upload.get('state') in ('done', 'skip'):
            continue
        linked = [j for j in rows if j.get('film') == film and j.get('repo', 'owb') == 'owb' and j.get('status') in workflow.LIVE]
        issues = []
        if record.get('record_error'):
            issues.append(('record', 'invalid-record'))
        for stage, value in stages.items():
            if not isinstance(value, dict):
                issues.append((stage, 'invalid-record'))
                continue
            state = value.get('state')
            active = [j for j in linked if j.get('stage') == stage]
            claims = [c for c in record.get('claims', []) if c.get('stage') == stage]
            # A live standalone stage claim also owns the handoff until its recorded lease ends.
            claimed = any(workflow.timestamp(c.get('eta')) and workflow.timestamp(c['eta']) > at for c in claims)
            if state in ('review', 'doing', 'blocked') and not active and not claimed:
                issues.append((stage, 'orphan-' + state))
        # Only advance recorded focus work; never turn the whole backlog into paid production.
        if film in data.get('focus', []) and not linked and not issues and stages and any(s.get('state') == 'done' for s in stages.values() if isinstance(s, dict)):
            if not any(workflow.timestamp(c.get('eta')) and workflow.timestamp(c['eta']) > at for c in record.get('claims', [])):
                issues.append(('pipeline', 'missing-next-step'))
        for stage, kind in issues:
            evidence = stages.get(stage, {})
            # Deliberately ignore ownership/heartbeat timestamps: they are not new production evidence.
            evidence = evidence if isinstance(evidence, dict) else {}
            meaningful = {k: evidence.get(k) for k in ('state','ref','lock','version','note','approval','ruling')}
            signature = hashlib.sha256(json.dumps([film,stage,kind,meaningful],sort_keys=True).encode()).hexdigest()[:20]
            out.append({'film':film,'stage':stage,'kind':kind,'signature':signature})
    return out


def reconcile(data, film_records, at, add):
    pending = findings(data, film_records, at)
    created = []
    for issue in pending:
        key = issue['signature']
        if any(j.get('handoff', {}).get('signature') == key and j.get('status') in workflow.LIVE for j in data['jobs']):
            continue
        task = add(data, title=f"Chief: resolve {issue['film']} {issue['stage']} {issue['kind']}",
                   needs='mini', kind='chief', by='relay', at=at,
                   body='Resolve recorded workflow gap: ' + json.dumps(issue) + '. Read the current film status, original job results, approval history and actual evidence. '
                   'Record a specific PASS/FIX or queue the missing next action with film/stage and dependencies. '
                   'Unknown records are not approvals. Never mark media approved from a filename, prose lock, or job completion alone. '
                   'If review needs media, verify on the Mini and perform required listening/viewing. '
                   'Preserve all Chief/Ben gates, focus priority, holds and scheduling. No paid generation, upload or visibility change is authorized by this repair task. '
                   'Before closing, resolve the stage state or create a linked successor/correction/review job; otherwise keep this task on a structured hold with a specific condition and next check.')
        # Repair tasks must not claim/release the broken stage: that would change the evidence they inspect.
        task['handoff'] = issue
        task['remaining_action'] = f"Chief resolves {issue['film']} {issue['stage']} handoff and records the next owner/action"
        created.append(task['id'])
    return created


def check_completion(task, data, film_records, at):
    issue = task.get('handoff')
    if not issue:
        return
    unresolved = findings(data, film_records, at, exclude=[task['id']])
    if any(x['film'] == issue['film'] and x['stage'] == issue['stage'] for x in unresolved):
        raise ValueError('Handoff still unresolved: record a stage ruling or linked successor, or keep the repair on a structured hold')


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    data = json.loads((args.root / 'jobs/queue.json').read_text())
    gaps = findings(data, list(records(args.root / '02_Video-Projects')), dt.datetime.now(dt.timezone.utc))
    print(json.dumps({'readOnly':True, 'count':len(gaps), 'findings':gaps}, indent=2))
    return 1 if gaps else 0


if __name__ == '__main__':
    raise SystemExit(main())
