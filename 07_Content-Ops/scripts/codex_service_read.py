#!/usr/bin/env python3
"""Restricted read-only Buffer/YouTube entry point for J2040.

Install outside the checkout and run with Python -I. No caller URL, HTTP method,
query, JSON body, token or post ID is accepted. Publishing routes are absent.
"""
import argparse
import datetime as dt
import http.client
import json
from pathlib import Path
import re
from urllib.parse import urlencode

ROOT = Path('/Users/benjaminoats/YouTube/orbit-with-ben')
CHANNELS = {'owb': 'UC_esArsDKd3GJvOkeO0DUog', 'hos': 'UCXp7HkBIl1LgaznXuZHJyRg'}
NETWORKS = {'owb': {'instagram', 'facebook', 'threads'}, 'hos': {'instagram', 'facebook', 'tiktok'}}
SOCIAL = Path('00_Brand/Channel-Setup/social')
GET_POST = 'query StudioGetPost($input: PostInput!) { post(input: $input) { id status } }'


def settings():
    wanted = {'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'YT_ANALYTICS_REFRESH_TOKEN_OWB',
              'YT_ANALYTICS_REFRESH_TOKEN_HOS', 'BUFFER_API_KEY', 'BUFFER_HOS_API_KEY'}
    values = {}
    for line in (ROOT / '07_Content-Ops/.env').read_text().splitlines():
        key, sep, value = line.strip().partition('=')
        if sep and key in wanted:
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            values[key] = value
    return values


def request(host, path, method='GET', body=None, headers=None):
    # Fail closed even if a future caller accidentally introduces a new route.
    permitted = (host == 'oauth2.googleapis.com' and path == '/token' and method == 'POST' or
                 host == 'www.googleapis.com' and method == 'GET' and
                 path.split('?')[0] in ('/youtube/v3/channels', '/youtube/v3/videos') or
                 host == 'youtubeanalytics.googleapis.com' and method == 'GET' and
                 path.split('?')[0] == '/v2/reports' or
                 host == 'api.buffer.com' and path == '/' and method == 'POST')
    if not permitted:
        raise ValueError('Request outside permitted read routes')
    if host == 'api.buffer.com':
        payload = json.loads(body)
        if payload.get('query') != GET_POST:
            raise ValueError('Buffer mutations are not allowed')
    connection = http.client.HTTPSConnection(host, timeout=30)
    try:
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        if response.status != 200:
            raise ValueError('Service request failed')
        raw = response.read(4 * 1024 * 1024 + 1)
        if len(raw) > 4 * 1024 * 1024:
            raise ValueError('Response exceeds limit')
        value = json.loads(raw)
        if not isinstance(value, dict) or value.get('errors') or value.get('error'):
            raise ValueError('Invalid service response')
        return value
    finally:
        connection.close()


def token(cfg, channel):
    # Existing read-only sign-ins only. A missing/expired login fails; never start
    # an interactive authorization flow or alter credential files.
    refresh = cfg['YT_ANALYTICS_REFRESH_TOKEN_' + channel.upper()]
    body = urlencode({'client_id': cfg['GOOGLE_CLIENT_ID'], 'client_secret': cfg['GOOGLE_CLIENT_SECRET'],
                      'refresh_token': refresh, 'grant_type': 'refresh_token'})
    result = request('oauth2.googleapis.com', '/token', 'POST', body,
                     {'Content-Type': 'application/x-www-form-urlencoded'})
    access = result.get('access_token')
    if not isinstance(access, str) or not access:
        raise ValueError('Access token missing')
    return access


def youtube_get(access, endpoint, params):
    return request('www.googleapis.com', '/youtube/v3/' + endpoint + '?' + urlencode(params),
                   headers={'Authorization': 'Bearer ' + access})


def validate(args):
    if args.channel not in CHANNELS:
        raise ValueError('Unknown channel')
    if args.video is not None and not re.fullmatch(r'[A-Za-z0-9_-]{11}', args.video):
        raise ValueError('Invalid video ID')
    if args.operation == 'buffer-status':
        if not args.video or args.network not in NETWORKS[args.channel] or args.start or args.end:
            raise ValueError('Buffer requires a registered video and supported network only')
    elif args.operation == 'video':
        if not args.video or args.network or args.start or args.end:
            raise ValueError('Video requires only a video ID')
    elif args.operation == 'channel':
        if any((args.video, args.network, args.start, args.end)):
            raise ValueError('Channel takes no additional selection')
    elif args.operation == 'analytics':
        if args.video or args.network or not args.start or not args.end:
            raise ValueError('Analytics requires dates only')
        for date in (args.start, args.end):
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', date):
                raise ValueError('Expected ISO date')
            dt.date.fromisoformat(date)
        if not args.start <= args.end <= dt.datetime.now(dt.timezone.utc).date().isoformat():
            raise ValueError('Invalid analytics date interval')
    else:
        raise ValueError('Unknown operation')


def execute(args, cfg):
    validate(args)
    if args.operation == 'buffer-status':
        folder = ROOT / SOCIAL / ('hos' if args.channel == 'hos' else '')
        entry = json.loads((folder / 'BUFFER_POSTS.json').read_text())['videos'][args.video]
        if args.channel == 'hos' and entry.get('kind') != 'short':
            raise ValueError('HOS accepts only Shorts')
        post = entry['channels'][args.network]['postId']
        if not isinstance(post, str) or not re.fullmatch('[a-f0-9]{24}', post):
            raise ValueError('Invalid registered post ID')
        key = cfg['BUFFER_HOS_API_KEY' if args.channel == 'hos' else 'BUFFER_API_KEY']
        response = request('api.buffer.com', '/', 'POST', json.dumps({'query': GET_POST, 'variables': {'input': {'id': post}}}),
                           {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
        result = response['data']['post']
        if result is None:
            return {'channel': args.channel, 'video': args.video, 'postId': post, 'status': None}
        if result.get('id') != post or not isinstance(result.get('status'), str):
            raise ValueError('Unexpected Buffer post response')
        return {'channel': args.channel, 'video': args.video, 'postId': post, 'status': result['status']}
    access = token(cfg, args.channel)
    mine = youtube_get(access, 'channels', {'part': 'id', 'mine': 'true'})
    if [item.get('id') for item in mine.get('items', [])] != [CHANNELS[args.channel]]:
        raise ValueError('Read-only login does not match selected channel')
    if args.operation == 'channel':
        return youtube_get(access, 'channels', {'part': 'snippet,statistics,contentDetails', 'id': CHANNELS[args.channel]})
    if args.operation == 'video':
        response = youtube_get(access, 'videos', {'part': 'snippet,statistics,contentDetails,status', 'id': args.video})
        items = response.get('items', [])
        if len(items) != 1 or items[0].get('id') != args.video or items[0].get('snippet', {}).get('channelId') != CHANNELS[args.channel]:
            raise ValueError('Video does not belong to selected channel')
        return response
    params = {'ids': 'channel==' + CHANNELS[args.channel], 'startDate': args.start, 'endDate': args.end,
              'dimensions': 'day', 'sort': 'day', 'metrics': 'views,estimatedMinutesWatched,subscribersGained,subscribersLost'}
    return request('youtubeanalytics.googleapis.com', '/v2/reports?' + urlencode(params),
                   headers={'Authorization': 'Bearer ' + access})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--channel', choices=tuple(CHANNELS), required=True)
    parser.add_argument('--operation', choices=('channel', 'video', 'analytics', 'buffer-status'), required=True)
    parser.add_argument('--video')
    parser.add_argument('--network')
    parser.add_argument('--start')
    parser.add_argument('--end')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)
    try:
        validate(args)
        if args.dry_run:
            print(json.dumps({'dryRun': True, 'channel': args.channel, 'operation': args.operation}))
            return 0
        print(json.dumps(execute(args, settings())))
        return 0
    except (ValueError, KeyError, TypeError, AttributeError, OSError, http.client.HTTPException):
        # No response bodies, credential values, URLs or exception interpolation.
        print('Service read refused or failed; check registration and existing read-only sign-in.')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
