"""Read-only milestone/UAT forecast. No task percentages or default durations.

The graph ends at Chief QA, before Ben's watch and upload. Historical observations
are recorded stage transitions, separated by channel and format. Missing coverage,
unknown queue waits and manual gates suppress the calendar estimate.
"""
from datetime import datetime, timezone
from math import ceil
from statistics import median
import re


PLAN = {
    'topic': (), 'script': ('topic',), 'sources': ('script',),
    'vo': ('sources',), 'shots': ('sources',), 'picture': ('shots',),
    'edit': ('picture', 'vo'), 'thumbs': ('picture',), 'qa': ('edit', 'thumbs'),
}
LABELS = dict(topic='Topic', script='Script', sources='Fact checks', vo='Voice',
              shots='Shot plan', picture='Picture', edit='Edit', thumbs='Packaging', qa='Chief QA')
DONE = {'done', 'skip', 'passed'}
STAGE_ALIASES = {'sources': 'facts', 'thumbs': 'thumbnails'}


def canonical_stage(key):
    return next((canonical for canonical, alias in STAGE_ALIASES.items() if key == alias), key)


def stage_record(stages, key):
    """Read equivalent recorded HOS keys without inventing missing stages.

    An explicit canonical record (including unknown/pending) wins over an alias.
    HOS's upload-package scaffold is not the complete Packaging milestone.
    """
    return (stages.get(key) if key in stages else stages.get(STAGE_ALIASES.get(key))) or {}


def date(value):
    try:
        result = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
        return result.astimezone(timezone.utc) if result.tzinfo else None
    except (TypeError, ValueError):
        return None


def learn_documents(snapshots, channel):
    """Observe actual stage transitions, not completion of individual jobs.

    snapshots is chronological (timestamp, {video key: {stage: record}}).
    An already-running stage at the oldest snapshot has an unknown start.
    """
    samples, previous, started = {}, {}, {}
    for at, films in snapshots:
        if not at:
            continue
        for film, stages in films.items():
            for stage in PLAN:
                raw = stage_record(stages, stage)
                state = raw.get('state') or raw.get('status') or 'unknown'
                key = (film, stage)
                old = previous.get(key)
                # Explicit boundaries can also be emitted by future workers.
                start, end = date(raw.get('startedAt')), date(raw.get('completedAt'))
                if state == 'doing' and old is not None and old != 'doing':
                    started.setdefault(key, at)
                if state == 'done' and old != 'done':
                    start = start or started.get(key)
                    end = end or at
                    if start and start < end <= at:
                        bucket = (channel, 'long', stage)
                        samples.setdefault(bucket, []).append(((end-start).total_seconds()/60, film))
                    started.pop(key, None)
                previous[key] = state
    # Several rework cycles of one film are one comparable observation.
    for bucket, rows in samples.items():
        by_film = {}
        for minutes, film in rows:
            by_film[film] = by_film.get(film, 0) + minutes
        samples[bucket] = [(minutes, film) for film, minutes in by_film.items()]
    return samples


def history_samples(repo, relative, channel):
    """Bounded Git observation; shallow/missing history cannot fabricate starts."""
    import json
    import subprocess
    try:
        log = subprocess.run(['git', '-C', str(repo), 'log', '-80', '--format=%H %cI',
                              '--', relative], capture_output=True, check=True, timeout=15).stdout.decode().splitlines()
        revisions = [line.split(' ', 1) for line in reversed(log)]
        # One cat-file process for every historical blob, keeping the minute publisher cheap.
        specs = ''.join(f'{sha}:{relative}\n' for sha, _ in revisions)
        data = subprocess.run(['git', '-C', str(repo), 'cat-file', '--batch'], input=specs.encode(),
                              capture_output=True, check=True, timeout=15).stdout
        import io
        stream, snapshots = io.BytesIO(data), []
        for _, at in revisions:
            header = stream.readline().decode().split()
            if len(header) != 3 or header[1] != 'blob':
                continue
            doc = json.loads(stream.read(int(header[2])))
            stream.read(1)
            if channel == 'HOS':
                films = {'HOS:' + str(f['id']): f.get('stages') or {} for f in doc.get('films') or []}
            else:
                films = {'OWB:' + str(doc.get('film')): doc.get('stages') or {}}
            snapshots.append((date(at), films))
        return learn_documents(snapshots, channel)
    except (OSError, ValueError, KeyError, subprocess.SubprocessError):
        return {}


def milestone_rows(stages, jobs):
    """Presentation metadata only. Keep the source state and notes unchanged."""
    rows = []
    seen = {}
    for job in jobs:
        seen.setdefault(job.get('id'), job)
    for key, deps in PLAN.items():
        raw = stage_record(stages, key)
        related = [j for j in seen.values() if canonical_stage(j.get('stage')) == key]
        live = [j for j in related if j.get('status') in ('claimed', 'blocked', 'open')]
        live.sort(key=lambda j: {'blocked': 0, 'claimed': 1, 'open': 2}[j['status']])
        state = raw.get('state') or raw.get('status') or 'unknown'
        approval = raw.get('approval') or {}
        approval_pending = (state == 'review' or (isinstance(approval, dict) and approval.get('status') in ('pending', 'requested'))
            or any(j.get('status') == 'blocked' and ((j.get('hold') or {}).get('type') in ('approval', 'chief')
                or re.search(r'(?:parked|awaiting|waiting) for (?:the )?Chief.*(?:PASS|approval)|Chief.*(?:PASS|approval).*pending',
                             str((j.get('hold') or {}).get('condition') or j.get('result') or ''), re.I)) for j in live))
        display = 'review' if approval_pending else 'blocked' if state not in DONE and any(j.get('status') == 'blocked' for j in live) else state
        evidence = raw.get('note') or raw.get('proof') or raw.get('ref') or ''
        texts = [str(evidence)] + [str(j.get('result') or '') for j in related]
        note = ' '.join(texts)
        summary = ''
        steps = raw.get('steps')
        if (key == 'picture' and isinstance(steps, list) and len(steps) == 2
                and all(isinstance(n, int) and not isinstance(n, bool) for n in steps)
                and 0 <= steps[0] <= steps[1] and steps[1] > 0
                and re.search(r'\brows\b', str(raw.get('steps_unit') or ''), re.I)):
            summary = f'{steps[0]}/{steps[1]} picture rows recorded'
        shots = re.search(r'\b(\d+)\s*/\s*(\d+)\s+Flow\b', note, re.I)
        if not summary and shots and key == 'picture' and re.search(r'minted|generated', note, re.I):
            summary = f'{shots[1]}/{shots[2]} Flow shots generated'
        duration = re.search(r'\b(\d+(?:\.\d+)?)\s*s\b', str(evidence)) if key == 'vo' else None
        if duration:
            seconds = round(float(duration[1]))
            summary = f'{seconds//60}m {seconds%60:02d}s recorded voice'
        version = raw.get('version') or next(iter(re.findall(r'\bv\d+[a-z]?\b', str(evidence), re.I)), '')
        reviewer = raw.get('reviewer') or ((approval.get('by') or approval.get('owner')) if isinstance(approval, dict) else '') or ''
        if not reviewer and approval_pending:
            explicit_chief_hold = any(j.get('status') == 'blocked' and re.search(r'Chief', str((j.get('hold') or {}).get('condition') or ''), re.I) for j in live)
            if explicit_chief_hold or re.search(r'(?:parked|awaiting|waiting).*Chief', str(evidence), re.I):
                reviewer = 'chief'
        row = dict(id=key, label=LABELS[key], state=state, displayState=display,
                   awaitingApproval=approval_pending, dependsOn=list(deps), evidence=evidence,
                   summary=summary, reviewer=reviewer,
                   owner=raw.get('owner') or raw.get('by') or next((j.get('by') for j in live if j.get('by')), ''),
                   version=version, jobs=[{k: j.get(k) for k in ('id', 'status', 'by', 'title', 'remaining_action', 'hold', 'result', 'progress', 'claimedAt')} for j in related],
                   source={k: raw[k] for k in ('note', 'proof', 'ref', 'version', 'score', 'durationSeconds', 'startedAt', 'completedAt', 'since', 'updatedAt', 'approval', 'progress', 'steps', 'steps_unit') if k in raw})
        rows.append(row)
    return rows


def select_current(rows, critical_path=()):
    """Active workflow evidence first; never choose the first incomplete stage."""
    by_id = {r['id']: r for r in rows}
    def descendants(key):
        return sum(key in dependency_chain(other['id'], by_id) for other in rows if other['displayState'] not in DONE)
    active = [r for r in rows if r['displayState'] not in DONE and (r['displayState'] in ('doing', 'in_progress', 'blocked', 'review')
              or any(j['status'] in ('claimed', 'blocked') for j in r['jobs']))]
    active.sort(key=lambda r: (0 if r['displayState'] in ('blocked', 'review') else 1,
                               0 if r['id'] in critical_path else 1, -descendants(r['id']), list(PLAN).index(r['id'])))
    if not active:
        # Queued work is a candidate only when all its milestone prerequisites are recorded complete.
        active = [r for r in rows if any(j['status'] == 'open' for j in r['jobs'])
                  and all(by_id[d]['displayState'] in DONE for d in r['dependsOn'])]
    return [r['id'] for r in active]


def dependency_chain(key, rows):
    direct = rows[key]['dependsOn']
    return set(direct).union(*(dependency_chain(k, rows) for k in direct)) if direct else set()


def forecast(video, stages, jobs, samples, now):
    rows = milestone_rows(stages, jobs)
    result = dict(asOf=now.isoformat(), milestones=rows,
                  completed=sum(r['displayState'] in DONE for r in rows), total=len(rows),
                  activeStages=select_current(rows), partialEstimates=[],
                  eta=dict(state='unavailable', confidence='unavailable', reasons=[], criticalPath=[]))
    eta = result['eta']
    if video.get('lane') == 'ready' and video.get('readyFor') == 'Ben':
        eta.update(state='ready', reasons=['Finished cut awaiting your UAT'])
        return result
    if video.get('lane') in ('approved', 'done'):
        eta.update(state='complete', reasons=['UAT handoff already passed'])
        return result
    reasons = eta['reasons']
    if video.get('lane') == 'changes':
        reasons.append('Requested changes need a fresh QA pass')
    relevant = [j for j in jobs if j.get('status') in ('open', 'claimed', 'blocked') and j.get('stage') != 'upload']
    for j in relevant:
        name = j.get('id', 'Job')
        hold = j.get('hold') or {}
        if j.get('status') == 'blocked':
            reasons.append(f"{name}: {hold.get('condition') or j.get('remaining_action') or j.get('result') or 'blocked'}")
        if j.get('needs') in ('manual', 'flow') or j.get('manual') or 'flow' in str(j.get('title', '')).lower():
            reasons.append(f'{name}: manual Flow/operator timing is unbounded')
        if j.get('status') == 'open':
            reasons.append(f'{name}: queue start not confirmed')
        if j.get('after') and not any(x.get('id') == j['after'] and x.get('status') == 'done' for x in jobs):
            reasons.append(f"{name}: dependency {j['after']} has not completed")
        if canonical_stage(j.get('stage')) not in PLAN:
            reasons.append(f'{name}: work is not mapped to a production milestone')
    agents = {}
    for j in relevant:
        if j.get('status') == 'claimed' and j.get('by'):
            agents.setdefault(j['by'], set()).add(canonical_stage(j.get('stage')))
    shared_capacity = any(len(stages) > 1 for stages in agents.values())
    if shared_capacity:
        reasons.append('Shared worker capacity: parallel stage timing is not confirmed')
    finishes, paths, counts, variability = {}, {}, [], []
    for row in rows:
        key = row['id']
        if row['displayState'] in DONE:
            finishes[key], paths[key] = (0, 0), []
            continue
        if row['displayState'] in ('blocked', 'review', 'unknown'):
            reasons.append(f"{row['label']}: {row['displayState']} timing")
        observations = [v for v, film in samples.get((video['channel'], video['type'], key), []) if film != video['key']]
        row['sampleCount'] = len(observations)
        if len(observations) < 3:
            reasons.append(f"{row['label']}: fewer than 3 comparable historical stages")
            finishes[key], paths[key] = (0, 0), []
            continue
        values = sorted(observations)
        low, high = median(values), values[min(len(values)-1, ceil(.8 * len(values))-1)]
        counts.append(len(values))
        variability.append(high / low if low else float('inf'))
        row['typicalMinutes'], row['upperMinutes'] = ceil(low), ceil(high)
        before_reasons = len(reasons)
        if row['displayState'] in ('doing', 'in_progress'):
            if not any(j.get('stage') == key and j.get('status') == 'claimed' for j in relevant):
                reasons.append(f"{row['label']}: no worker currently running this stage")
            start = date(stage_record(stages, key).get('since'))
            # A task's latest claim is not necessarily the start of the stage.
            if not start or start > now:
                reasons.append(f"{row['label']}: stage start not recorded")
            else:
                elapsed = (now-start).total_seconds()/60
                if elapsed >= high:
                    reasons.append(f"{row['label']}: taking longer than historical range")
                low, high = max(0, low-elapsed), max(0, high-elapsed)
        elif not any(j.get('stage') == key for j in relevant):
            reasons.append(f"{row['label']}: remaining work not queued")
        stage_jobs = [j for j in relevant if j.get('stage') == key]
        if (row['displayState'] in ('doing', 'in_progress') and len(reasons) == before_reasons
                and not shared_capacity and stage_jobs and all(j.get('status') == 'claimed' and not j.get('after')
                    and not j.get('manual') and j.get('needs') not in ('flow', 'manual')
                    and 'flow' not in str(j.get('title', '')).lower() for j in stage_jobs)):
            result['partialEstimates'].append(dict(stage=key, label=row['label'], lowerMinutes=ceil(low),
                upperMinutes=ceil(high), confidence='low', sampleCount=len(values)))
        deps = row['dependsOn']
        low_parent = max(deps, key=lambda d: finishes[d][0]) if deps else None
        high_parent = max(deps, key=lambda d: finishes[d][1]) if deps else None
        finishes[key] = (low + (finishes[low_parent][0] if low_parent else 0),
                         high + (finishes[high_parent][1] if high_parent else 0))
        paths[key] = (paths[high_parent] if high_parent else []) + [key]
    eta['reasons'] = list(dict.fromkeys(reasons))
    eta['criticalPath'] = paths.get('qa', [])
    result['activeStages'] = select_current(rows, eta['criticalPath'])
    if not reasons and not paths.get('qa'):
        reasons.append('Milestones complete; UAT handoff not confirmed')
        eta['reasons'] = reasons
    if not reasons:
        low, high = finishes['qa']
        eta.update(state='estimated', confidence='medium' if min(counts or [0]) >= 10 and max(variability or [99]) <= 2 else 'low',
                   lowerMinutes=ceil(low), upperMinutes=ceil(high),
                   basedOn='Recorded stage transitions in Git; median–80th percentile; parallel branches use the longest path')
    return result


def attach(videos, hos, owb, alljobs, now):
    scope_records = {'HOS:' + str(f.get('id')): f.get('milestoneScope') or {} for f in hos.get('films') or []}
    scope_records.update({'OWB:' + str(f.get('film')): f.get('milestoneScope') or {} for f in owb})
    sources = {'HOS:' + str(f.get('id')): f.get('stages') or {} for f in hos.get('films') or []}
    sources.update({'OWB:' + str(f.get('film')): f.get('stages') or {} for f in owb})
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    samples = {}
    for status in (root / '02_Video-Projects').glob('*/status.json'):
        for bucket, values in history_samples(root, str(status.relative_to(root)), 'OWB').items():
            samples.setdefault(bucket, []).extend(values)
    import os
    candidates = [Path(os.environ.get('HOS_REPO', ''))] if os.environ.get('HOS_REPO') else []
    candidates += [root.parent / name for name in ('hos', 'history-of-science', 'History Of Science')]
    hos_repo = next((p for p in candidates if (p / '00_Brand/Channel-Setup/PIPELINE.json').exists()), root.parent / 'hos')
    samples.update(history_samples(hos_repo, '00_Brand/Channel-Setup/PIPELINE.json', 'HOS'))
    for video in videos:
        # Parent-film stages cannot certify a Short or a synthetic approval card.
        project_stages = sources.get(video['key'], {})
        recorded_scope = scope_records.get(video['key'], {})
        watch_version = (video.get('watch') or {}).get('version') or video.get('version')
        exact_scope = isinstance(recorded_scope, dict) and recorded_scope.get('type') == 'cut' and bool(video.get('version')) and watch_version == video.get('version') and recorded_scope.get('version') == video.get('version') and recorded_scope.get('format') == video.get('type')
        mixed_scope = not exact_scope and bool(video.get('cutFormatCorrected') or (video.get('watch') and any(
            re.match(r'\s*AR cohort:', str(s.get('note') or ''), re.I) for s in project_stages.values())))
        stages = project_stages if video.get('type') == 'long' or exact_scope else {}
        ids = {j['id'] for j in video.get('jobs') or []}
        jobs = [j for j in alljobs if j.get('id') in ids]
        dependencies = {j.get('after') for j in jobs}
        jobs += [j for j in alljobs if j.get('id') in dependencies and j not in jobs]
        production = forecast(video, stages, jobs, samples, now)
        if exact_scope:
            production.update(scope='cut', scopeVersion=recorded_scope['version'])
        if mixed_scope:
            history = forecast(video, project_stages, jobs, samples, now)
            production = forecast(video, {}, [], samples, now)
            production.update(scope='unconfirmed_cut', projectHistory=history,
                scopeReason='Recorded project milestones include related production work; progress for this exact cut is unconfirmed.')
            if production['eta']['state'] not in ('ready', 'complete'):
                production['eta'] = dict(state='unavailable', confidence='unavailable', reasons=[production['scopeReason']])
                production['partialEstimates'] = []
        owners = {j.get('by') for j in jobs if j.get('status') == 'claimed' and j.get('by')}
        competing = [j for j in alljobs if j.get('id') not in ids and j.get('status') == 'claimed' and j.get('by') in owners]
        if competing and production['eta']['state'] not in ('ready', 'complete'):
            production['eta'].update(state='unavailable', confidence='unavailable')
            production['eta']['reasons'].append('Assigned agents have other claimed work; calendar capacity is unconfirmed')
            production['eta'].pop('lowerMinutes', None)
            production['eta'].pop('upperMinutes', None)
            production['partialEstimates'] = []
        video['production'] = production
