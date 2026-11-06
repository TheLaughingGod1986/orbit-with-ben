#!/usr/bin/env python3
"""J2040: restore house disclosure/audience flags on registered private schedules.

Default is a live plan. No caller metadata, date, URL, token or payload. No
upload/delete/public transition. This does not replace package or UAT gates.
"""
import argparse
import datetime as dt
import hashlib
import http.client
import importlib.util
import json
from pathlib import Path
import re
from urllib.parse import urlencode

ROOT = Path('/Users/benjaminoats/YouTube/orbit-with-ben')
HOS = Path('/Users/benjaminoats/YouTube/History Of Science')
READ = Path('/Users/benjaminoats/.codex/bin/studio-service-read.py')
SCHEDULE = Path('/Users/benjaminoats/.codex/bin/studio-buffer-reschedule.py')
READ_SHA = '6635f535eeebe047dee175acbe81d26eb99abb985ad9e4860276ed838f260335'
SCHEDULE_SHA = '6a78c3509966f3a23d9db79888b8de8072ff6dd36eee778114b828cd508a66c9'
CHANNELS = {'owb': 'UC_esArsDKd3GJvOkeO0DUog', 'hos': 'UCXp7HkBIl1LgaznXuZHJyRg'}
MUTABLE = {'privacyStatus', 'publishAt', 'license', 'embeddable', 'publicStatsViewable',
           'selfDeclaredMadeForKids', 'containsSyntheticMedia'}
READ_ONLY = {'uploadStatus', 'failureReason', 'rejectionReason', 'madeForKids'}


def dependency(path, expected, name):
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise ValueError('Installed dependency changed')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def settings(channel):
    values = {}
    root = ROOT if channel == 'owb' else HOS
    for line in (root / '07_Content-Ops/.env').read_text().splitlines():
        key, sep, value = line.strip().partition('=')
        if sep and key in {'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'YOUTUBE_REFRESH_TOKEN'}:
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            values[key] = value
    return values


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError('Missing schedule')
    result = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('Timezone required')
    return result.astimezone(dt.timezone.utc)


def body_for(video, channel, video_id):
    if (video.get('id') != video_id or video.get('snippet', {}).get('channelId') != CHANNELS[channel]
            or not isinstance(video.get('etag'), str) or not video['etag']):
        raise ValueError('Video ownership or version missing')
    status = video['status']
    if set(status) - MUTABLE - READ_ONLY:
        raise ValueError('Unknown status fields; review before updating')
    if (status.get('privacyStatus') != 'private' or status.get('uploadStatus') != 'processed'
            or timestamp(status.get('publishAt')) <= dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=10)):
        raise ValueError('Requires processed private schedule over ten minutes ahead')
    if status.get('license') not in {'youtube', 'creativeCommon'}:
        raise ValueError('License missing')
    for field in ('embeddable', 'publicStatsViewable'):
        if type(status.get(field)) is not bool:
            raise ValueError('Existing writable status missing')
    # Preserve ALL writable status fields; YouTube deletes omitted properties.
    target = {key: value for key, value in status.items() if key in MUTABLE}
    target.update(selfDeclaredMadeForKids=False, containsSyntheticMedia=True)
    return {'id': video_id, 'status': target}


def update(access, body, etag):
    # Private method, called only with the validated live body; fixed endpoint.
    connection = http.client.HTTPSConnection('www.googleapis.com', timeout=30)
    try:
        connection.request('PUT', '/youtube/v3/videos?part=status', json.dumps(body),
                           {'Authorization': 'Bearer ' + access, 'Content-Type': 'application/json', 'If-Match': etag})
        response = connection.getresponse()
        if response.status != 200:
            raise ValueError('YouTube update failed')
        raw = response.read(1048577)
        if len(raw) > 1048576:
            raise ValueError('Response too large')
        return json.loads(raw)
    finally:
        connection.close()


def run(args, reader, cfg):
    folder = ROOT / reader.SOCIAL / ('hos' if args.channel == 'hos' else '')
    registered = json.loads((folder / 'UPLOADS.json').read_text())['videos'][args.video]
    if registered.get('kind') not in {'short', 'long'}:
        raise ValueError('Video must be registered')
    # Refresh the EXISTING writer sign-in only; never interactive login or save.
    access = reader.request('oauth2.googleapis.com', '/token', 'POST', urlencode({
        'client_id': cfg['GOOGLE_CLIENT_ID'], 'client_secret': cfg['GOOGLE_CLIENT_SECRET'],
        'refresh_token': cfg['YOUTUBE_REFRESH_TOKEN'], 'grant_type': 'refresh_token'}),
        {'Content-Type': 'application/x-www-form-urlencoded'}).get('access_token')
    if not isinstance(access, str) or not access:
        raise ValueError('No existing writer sign-in')
    mine = reader.youtube_get(access, 'channels', {'part': 'id', 'mine': 'true'})
    if [v.get('id') for v in mine.get('items', [])] != [CHANNELS[args.channel]]:
        raise ValueError('Writer sign-in belongs to another channel')
    def live():
        items = reader.youtube_get(access, 'videos', {'part': 'snippet,status', 'id': args.video}).get('items', [])
        if len(items) != 1:
            raise ValueError('Video missing')
        return items[0]
    video = live()
    body = body_for(video, args.channel, args.video)
    changed = any(video['status'].get(k) != body['status'][k] for k in ('selfDeclaredMadeForKids', 'containsSyntheticMedia'))
    if args.apply and changed:
        current = live()
        if current != video:
            raise ValueError('Video changed during preflight')
        body_for(current, args.channel, args.video)  # schedule still safely future
        result = update(access, body, current['etag'])
        if result.get('id') != args.video or any(result.get('status', {}).get(k) != v for k, v in body['status'].items()):
            raise ValueError('Update response mismatch; inspect live state before retry')
        confirmed = live()
        if body_for(confirmed, args.channel, args.video) != body or any(
                confirmed['status'].get(k) != body['status'][k] for k in ('selfDeclaredMadeForKids', 'containsSyntheticMedia')):
            raise ValueError('Read-back mismatch; inspect live state before retry')
    return {'channel': args.channel, 'video': args.video, 'apply': args.apply, 'change': changed,
            'privacyStatus': 'private', 'publishAt': body['status']['publishAt'],
            'selfDeclaredMadeForKids': False, 'containsSyntheticMedia': True}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--channel', choices=tuple(CHANNELS), required=True)
    parser.add_argument('--video', required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args(argv)
    try:
        if not re.fullmatch(r'[A-Za-z0-9_-]{11}', args.video):
            raise ValueError('Invalid video ID')
        reader = dependency(READ, READ_SHA, 'studio_read')
        scheduler = dependency(SCHEDULE, SCHEDULE_SHA, 'studio_schedule')
        with scheduler.desk_lock():
            print(json.dumps(run(args, reader, settings(args.channel))))
        return 0
    except (ValueError, KeyError, TypeError, AttributeError, OSError, http.client.HTTPException):
        print('YouTube defaults refused or failed; inspect live state before retry. No raw service errors printed.')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
