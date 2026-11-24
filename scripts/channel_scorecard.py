#!/usr/bin/env python3
"""Monthly portfolio recommendations. Read-only; never changes a publishing schedule.

Channel totals use complete daily Analytics records. Format totals use differences
of per-video lifetime Analytics at exact reporting-month boundaries. Missing
boundaries/rows stay unknown. Cohort medians are views accumulated by month end,
not today's lifetime views. Watch hours are estimates, never qualified Earn hours.
"""
from __future__ import annotations
import datetime as dt
import json
from pathlib import Path
from statistics import median
from zoneinfo import ZoneInfo

LONDON = ZoneInfo('Europe/London')
FIRST_REVIEW = dt.date(2027, 1, 4)


def read(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return {}


def measure(value=None, reason='', source=''):
    return {'value': value, 'reason': reason if value is None else '', 'source': source}


def month_before(day):
    return (day.replace(day=1) - dt.timedelta(days=1)).replace(day=1)


def first_monday(day):
    first = day.replace(day=1)
    return first + dt.timedelta(days=(0 - first.weekday()) % 7)


def ratio(numerator, denominator):
    if numerator['value'] is None or denominator['value'] is None:
        return measure(reason='Numerator or denominator is unknown')
    if denominator['value'] <= 0:
        return measure(reason='No positive denominator in this month')
    return measure(numerator['value'] / denominator['value'])


def reporting_snapshot(snapshots, day):
    matches = [s for s in snapshots if (s.get('analytics') or {}).get('through') == day.isoformat()]
    return max(matches, key=lambda s: s.get('takenAt', ''), default={})


def monthly(start, daily, snapshots):
    end = (start.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    before = reporting_snapshot(snapshots, start - dt.timedelta(days=1))
    after = reporting_snapshot(snapshots, end)
    rows = {r.get('day'): r for r in daily}
    days = [(start + dt.timedelta(days=n)).isoformat() for n in range((end-start).days+1)]
    def daily_sum(field):
        if not all(isinstance(rows.get(day, {}).get(field), (float, int)) for day in days):
            return measure(reason='Daily Analytics does not cover every date in this calendar month')
        return measure(sum(rows[day][field] for day in days), source='Complete daily channel Analytics')
    subs = daily_sum('subsNet')
    views = daily_sum('views')
    # The snapshot catalogue includes public/private/scheduled rows; count only public
    # films already published by the end of the requested month.
    public = [v for v in after.get('videos', []) if v.get('privacy') == 'public'
              and v.get('publishedAt', '')[:10] <= end.isoformat() and v.get('publishedAt')]
    cohort = [v for v in public if v['publishedAt'][:10] >= start.isoformat()]
    def count(fmt):
        return measure(sum(v.get('format') == fmt for v in cohort), source='Public catalogue at month-end reporting snapshot') if after else measure(reason='Month-end reporting snapshot is missing')
    old = (before.get('analytics') or {}).get('lifetime') or {}
    new = (after.get('analytics') or {}).get('lifetime') or {}
    def delta(v, key):
        a = new.get(v['id'], {}).get(key)
        b = 0 if v['publishedAt'][:10] >= start.isoformat() else old.get(v['id'], {}).get(key)
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            return None
        return a-b  # preserve negative corrections; do not silently clamp them
    def format_sum(fmt, key):
        if not after or not before:
            return measure(reason='Exact Analytics reporting-month boundaries are missing')
        values = [delta(v, key) for v in public if v.get('format') == fmt]
        if any(v is None for v in values):
            return measure(reason='Per-video lifetime Analytics is missing for a public film at a month boundary')
        return measure(sum(values), source='Difference of month-boundary lifetime Analytics; public films only')
    hours = format_sum('long', 'minutes')
    if hours['value'] is not None:
        hours['value'] /= 60
    shorts = format_sum('short', 'views')
    longs_n, shorts_n = count('long'), count('short')
    made = measure(longs_n['value'] + shorts_n['value']) if after else count('long')
    def typical(fmt):
        selected = [v for v in cohort if v.get('format') == fmt]
        vals = [new.get(v['id'], {}).get('views') for v in selected]
        if not after or not vals or any(v is None for v in vals):
            return measure(reason='No complete month-end Analytics views for this publication cohort')
        return measure(median(vals), source='Median views by month end of public films published that month')
    score = measure(subs['value'] + hours['value']) if subs['value'] is not None and hours['value'] is not None else measure(reason='Net subscribers or public-long watch hours unknown')
    all_rate, short_rate = ratio(subs, views), ratio(subs, shorts)
    for rate in (all_rate, short_rate):
        if rate['value'] is not None:
            rate['value'] *= 1000
    return {'month': start.strftime('%Y-%m'), 'subscribers': subs, 'views': views, 'longHours': hours,
            'shortViews': shorts, 'subsPer1000': all_rate, 'subsPer1000ShortViews': short_rate,
            'longs': longs_n, 'shorts': shorts_n, 'films': made, 'returnPerFilm': ratio(score, made),
            'medianLong': typical('long'), 'medianShort': typical('short')}


def protection(slug, plans, now, snapshots):
    tests, until = [], []
    numbers = {v['id']: v for s in sorted(snapshots, key=lambda s: s.get('takenAt', '')) for v in s.get('videos', [])}
    for plan in plans:
        if plan.get('scope') == 'studio':
            for step in plan.get('steps', []):
                if step.get('id') == slug + '-counts' and step.get('when'):
                    until.append(step['when'][:10])
        if plan.get('channel') != slug:
            continue
        for step in plan.get('steps', []):
            test = step.get('test')
            if not test or not step.get('when'):
                continue
            # Use actual publish instant if the plan explicitly identifies its video,
            # otherwise retain the plan's read window. Never guess by fuzzy title.
            row = numbers.get(step.get('videoId'), {})
            published = row.get('publishedAt') if row.get('privacy') == 'public' else None
            start = dt.datetime.fromisoformat((published or step['when']).replace('Z', '+00:00'))
            if start.tzinfo is None:
                start = start.replace(tzinfo=LONDON)
            finish = start + dt.timedelta(days=int(test['days']))
            if start <= now < finish:
                tests.append({'film': step.get('name', ''), 'day': (now-start).days+1,
                              'days': test['days'], 'views': row.get('views'), 'keep': test['keep'],
                              'drop': test['drop'], 'finishes': finish.isoformat()})
    future = max((d for d in until if d >= now.date().isoformat()), default='')
    return tests, ('Tests come first: channel verdict counts from ' + future if future else
                   'Tests come first: a film is still inside its read window' if tests else '')


def ranking(rows, key):
    vals = [(r['channel'], r[key]['returnPerFilm']['value']) for r in rows]
    if len(vals) < 2 or any(v is None for _, v in vals):
        return None
    vals.sort(key=lambda x: x[1])
    if vals[0][1] == vals[1][1] or vals[-1][1] == vals[-2][1]:
        return None
    return vals[0][0], vals[-1][0]


def section(root, now=None, videos=None):
    root = Path(root)
    now = now or dt.datetime.now(dt.timezone.utc)
    now = now.astimezone(LONDON)
    start = month_before(now.date())
    plans = read(root / 'studio/plan.json') or []
    # Resolve plan films through the same explicit film/job keys as the plan card.
    # This honours real publish dates after slips without guessing from a title.
    from plan_board import _video_for
    queue = read(root / 'jobs/queue.json')
    jobs = {j['id']: j for j in queue.get('jobs', [])}
    for plan in plans:
        for step in plan.get('steps', []):
            video = _video_for(step, videos or [], jobs) or {}
            youtube = video.get('youtube') or {}
            if youtube.get('videoId'):
                step['videoId'] = youtube['videoId']
    policy_available = any(p.get('id') == 'studio-portfolio-2026-12' for p in plans)
    tracker = read(root / '05_Analytics/dashboard/data.json')
    rows = []
    for slug, name in [('owb', 'Orbit With Ben'), ('hos', 'History of Science'), ('ww2', 'Field Order History')]:
        base = root / ('channels/ww2/05_Analytics' if slug == 'ww2' else f'05_Analytics/{slug}')
        snapshots = [s for p in sorted((base/'snapshots').glob('*.json')) if (s := read(p))]
        channel = next((c for c in tracker.get('channels', []) if c.get('channel') == slug), {})
        daily = channel.get('daily', [])
        if not daily:
            daily = [{**r, 'subsNet': r['subsGained']-r['subsLost']} for r in read(base/'channel_daily.json').get('rows', []) if 'subsGained' in r and 'subsLost' in r]
        tests, protected = protection(slug, plans, now, snapshots)
        current = monthly(start, daily, snapshots)
        previous = monthly(month_before(start), daily, snapshots)
        m, p, rate = current['medianShort']['value'], previous['medianShort']['value'], current['subsPer1000ShortViews']['value']
        shorts = ('No Shorts published; keep this channel’s own schedule' if current['shorts']['value'] == 0 else
                  'U: need both cohort medians and subscribers per 1,000 Shorts views' if None in (m, p, rate) else
                  'Keep four Shorts a week' if m > p and rate >= 1 else 'Recommend two or three Shorts a week')
        if protected:
            shorts = 'Keep schedule while tests read: ' + protected
        previous_review = first_monday(now.date().replace(day=1) - dt.timedelta(days=1))
        _, prior_protection = protection(slug, plans, dt.datetime.combine(previous_review, dt.time(9), LONDON), snapshots)
        rows.append({'channel': slug, 'name': name, 'current': current, 'previous': previous, 'tests': tests,
                     'protection': protected, 'previousProtection': prior_protection, 'shortsVerdict': shorts})
    ranked, prior = ranking(rows, 'current'), ranking(rows, 'previous')
    for row in rows:
        verdict = 'U: ranking needs complete return-per-film figures for all channels and no tied extremes'
        if ranked:
            verdict = 'Keep schedule; not lowest on return per film'
            if row['channel'] == ranked[0]:
                top = next(r['name'] for r in rows if r['channel'] == ranked[1])
                repeat = prior and prior[0] == ranked[0] and not row['previousProtection'] and previous_review >= FIRST_REVIEW
                verdict = ('Recommend stopping new films; lowest again in consecutive monthly reviews. Delete nothing.' if repeat else
                           'Recommend halving next month’s schedule; give the capacity to ' + top)
        if now.date() < FIRST_REVIEW:
            verdict = 'Numbers only: first review is 4 Jan 2027'
        if row['protection']:
            verdict = row['protection'] + '; keep schedule'
        if not policy_available:
            verdict = 'U: portfolio plan unavailable; no schedule recommendation'
            row['shortsVerdict'] = verdict
        row['channelVerdict'] = verdict
    due = first_monday(now.date())
    if now.date() > due:
        due = first_monday((now.date().replace(day=28)+dt.timedelta(days=4)).replace(day=1))
    return {'month': start.strftime('%Y-%m'), 'previousMonth': month_before(start).strftime('%Y-%m'),
            'nextReview': max(due, FIRST_REVIEW).isoformat(), 'channels': rows,
            'note': 'Recommendations only; schedules change only when Ben says. Field Order History’s film-20 check stands. Net channel subscribers / Shorts views is a conversion proxy, not Shorts-attributed subscribers. Medians use views by month end, with unequal film ages. U means unknown; expand figures for coverage.'}
