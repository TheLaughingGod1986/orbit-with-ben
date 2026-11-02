"""Read-only milestone/UAT forecast. No task percentages or default durations.

The graph ends at Chief QA, before Ben's watch and upload. Historical observations
are recorded stage transitions, separated by channel and format. Missing coverage,
unknown queue waits and manual gates suppress the calendar estimate.
"""
from datetime import datetime, timezone
from math import ceil
from statistics import median


PLAN = {
    'topic': (), 'script': ('topic',), 'sources': ('script',),
    'vo': ('sources',), 'shots': ('sources',), 'picture': ('shots',),
    'edit': ('picture', 'vo'), 'thumbs': ('picture',), 'qa': ('edit', 'thumbs'),
}
LABELS = dict(topic='Topic', script='Script', sources='Fact checks', vo='Voice',
              shots='Shot plan', picture='Picture', edit='Edit', thumbs='Packaging', qa='Chief QA')
DONE = {'done', 'skip', 'passed'}


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
                raw = stages.get(stage) or {}
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


def forecast(video, stages, jobs, samples, now):
    rows = []
    for key, deps in PLAN.items():
        raw = stages.get(key) or {}
        state = raw.get('state') or raw.get('status') or 'unknown'
        rows.append(dict(id=key, label=LABELS[key], state=state,
                         evidence=raw.get('ref') or raw.get('note') or raw.get('proof') or '',
                         dependsOn=list(deps)))
    result = dict(asOf=now.isoformat(), milestones=rows, completed=sum(r['state'] in DONE for r in rows), total=len(rows),
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
        if j.get('stage') not in PLAN:
            reasons.append(f'{name}: work is not mapped to a production milestone')
    agents = {}
    for j in relevant:
        if j.get('status') == 'claimed' and j.get('by'):
            agents.setdefault(j['by'], set()).add(j.get('stage'))
    if any(len(stages) > 1 for stages in agents.values()):
        reasons.append('Shared worker capacity: parallel stage timing is not confirmed')
    finishes, paths, counts = {}, {}, []
    for row in rows:
        key = row['id']
        if row['state'] in DONE:
            finishes[key], paths[key] = (0, 0), []
            continue
        if row['state'] in ('blocked', 'review', 'unknown'):
            reasons.append(f"{row['label']}: {row['state']} timing")
        observations = [v for v, film in samples.get((video['channel'], video['type'], key), []) if film != video['key']]
        row['sampleCount'] = len(observations)
        if len(observations) < 3:
            reasons.append(f"{row['label']}: fewer than 3 comparable historical stages")
            finishes[key], paths[key] = (0, 0), []
            continue
        values = sorted(observations)
        low, high = median(values), values[min(len(values)-1, ceil(.8 * len(values))-1)]
        counts.append(len(values))
        row['typicalMinutes'], row['upperMinutes'] = ceil(low), ceil(high)
        if row['state'] in ('doing', 'in_progress'):
            if not any(j.get('stage') == key and j.get('status') == 'claimed' for j in relevant):
                reasons.append(f"{row['label']}: no worker currently running this stage")
            start = date((stages.get(key) or {}).get('since'))
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
        deps = row['dependsOn']
        low_parent = max(deps, key=lambda d: finishes[d][0]) if deps else None
        high_parent = max(deps, key=lambda d: finishes[d][1]) if deps else None
        finishes[key] = (low + (finishes[low_parent][0] if low_parent else 0),
                         high + (finishes[high_parent][1] if high_parent else 0))
        paths[key] = (paths[high_parent] if high_parent else []) + [key]
    eta['reasons'] = list(dict.fromkeys(reasons))
    eta['criticalPath'] = paths.get('qa', [])
    if not reasons and not paths.get('qa'):
        reasons.append('Milestones complete; UAT handoff not confirmed')
        eta['reasons'] = reasons
    if not reasons:
        low, high = finishes['qa']
        eta.update(state='estimated', confidence='medium' if min(counts or [0]) >= 10 else 'low',
                   lowerMinutes=ceil(low), upperMinutes=ceil(high),
                   basedOn='Recorded stage transitions in Git; median–80th percentile; parallel branches use the longest path')
    return result


def attach(videos, hos, owb, alljobs, now):
    sources = {'HOS:' + str(f.get('id')): f.get('stages') or {} for f in hos.get('films') or []}
    sources.update({'OWB:' + str(f.get('film')): f.get('stages') or {} for f in owb})
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    samples = {}
    for status in (root / '02_Video-Projects').glob('*/status.json'):
        for bucket, values in history_samples(root, str(status.relative_to(root)), 'OWB').items():
            samples.setdefault(bucket, []).extend(values)
    hos_repo = root.parent / 'history-of-science'
    samples.update(history_samples(hos_repo, '00_Brand/Channel-Setup/PIPELINE.json', 'HOS'))
    for video in videos:
        # Parent-film stages cannot certify a Short or a synthetic approval card.
        stages = sources.get(video['key'], {}) if video.get('type') == 'long' else {}
        ids = {j['id'] for j in video.get('jobs') or []}
        jobs = [j for j in alljobs if j.get('id') in ids]
        dependencies = {j.get('after') for j in jobs}
        jobs += [j for j in alljobs if j.get('id') in dependencies and j not in jobs]
        video['production'] = forecast(video, stages, jobs, samples, now)
