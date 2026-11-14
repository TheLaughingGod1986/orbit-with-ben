#!/usr/bin/env python3
"""J2040: reconcile existing Buffer schedules to live YouTube, never create/delete.

No caller post ID, time, text, URL, GraphQL or payload is accepted. Default is a
read-only plan. --apply changes only dueAt/mode for registered scheduled posts.
"""
import argparse
from contextlib import contextmanager
import datetime as dt
import hashlib
import http.client
import importlib.util
import json
import os
from pathlib import Path
import re
import tempfile

READ = Path('/Users/benjaminoats/.codex/bin/studio-service-read.py')
READ_SHA = '6635f535eeebe047dee175acbe81d26eb99abb985ad9e4860276ed838f260335'
LOCK = Path('/Users/benjaminoats/_desk/locks/youtube-buffer.lock')
CHANNELS = {
    'owb': {'instagram': '6ab920b2ea19ca0bde03abff', 'facebook': '6ab92149ea19ca0bde03af77', 'threads': '6ab92127ea19ca0bde03aead'},
    'hos': {'instagram': '6ac36d3c6a5c39ccb61d3b5f', 'facebook': '6ac369f16a5c39ccb61d223b', 'tiktok': '6ac381bc6a5c39ccb61dd8aa'},
}
GET = 'query StudioSchedulePost($input: PostInput!) { post(input: $input) { id status dueAt channelId } }'
EDIT = '''mutation StudioScheduleEdit($input: EditPostInput!) { editPost(input: $input) {
 __typename ... on PostActionSuccess { post { id status dueAt channelId } }
 ... on MutationError { message } } }'''


def read_gateway():
    # Never import a checkout or caller-supplied module. Fail closed on changes.
    if hashlib.sha256(READ.read_bytes()).hexdigest() != READ_SHA:
        raise ValueError('Read gateway changed; review and reinstall together')
    spec = importlib.util.spec_from_file_location('studio_read', READ)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def instant(value):
    if not isinstance(value, str):
        raise ValueError('Expected timestamp')
    parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Timestamp must have a timezone')
    return parsed.astimezone(dt.timezone.utc)


@contextmanager
def desk_lock():
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    # No stale-lock reclamation, force, alternate root or inherited-lock bypass.
    LOCK.mkdir()
    try:
        (LOCK / 'owner.txt').write_text(f'pid={os.getpid()}\ncmd=studio-buffer-reschedule\n')
        yield
    finally:
        (LOCK / 'owner.txt').unlink()
        LOCK.rmdir()


def buffer_call(key, query, payload):
    if query == GET:
        if set(payload) != {'id'} or not re.fullmatch('[a-f0-9]{24}', payload['id']):
            raise ValueError('Invalid read')
    elif query == EDIT:
        if (set(payload) != {'id', 'mode', 'dueAt'} or payload['mode'] != 'customScheduled'
                or not re.fullmatch('[a-f0-9]{24}', payload['id'])):
            raise ValueError('Invalid schedule edit')
        instant(payload['dueAt'])
    else:
        raise ValueError('Unsupported operation')
    conn = http.client.HTTPSConnection('api.buffer.com', timeout=30)
    try:
        conn.request('POST', '/', body=json.dumps({'query': query, 'variables': {'input': payload}}),
                     headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
        response = conn.getresponse()
        if response.status != 200:
            raise ValueError('Buffer request failed')
        raw = response.read(1048577)
        if len(raw) > 1048576:
            raise ValueError('Response too large')
        result = json.loads(raw)
        if result.get('errors') or not isinstance(result.get('data'), dict):
            raise ValueError('Buffer response failed')
        return result['data']
    finally:
        conn.close()


def checked_post(post, post_id, channel_id):
    if (not isinstance(post, dict) or post.get('id') != post_id
            or post.get('channelId') != channel_id or post.get('status') != 'scheduled'):
        raise ValueError('Post ownership/status mismatch')
    instant(post.get('dueAt'))
    return post


def atomic_ledger(file, ledger):
    fd, name = tempfile.mkstemp(prefix='.codex-schedule-', dir=file.parent)
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(ledger, stream, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, file)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def run(args, reader, cfg):
    folder = reader.ROOT / reader.SOCIAL / ('hos' if args.channel == 'hos' else '')
    file = folder / 'BUFFER_POSTS.json'
    ledger = json.loads(file.read_text())
    entry = ledger['videos'][args.video]
    registered = json.loads((folder / 'UPLOADS.json').read_text())['videos'][args.video]
    if (entry.get('kind') not in ('short', 'long') or entry.get('kind') != registered.get('kind')
            or args.channel == 'hos' and entry['kind'] != 'short'):
        raise ValueError('Unregistered or incompatible kind')
    if entry.get('mode') != 'customScheduled' or not entry.get('channels'):
        raise ValueError('Only existing scheduled posts may be reconciled')
    # Reader verifies the existing sign-in and the live video's channel ownership.
    read_args = argparse.Namespace(channel=args.channel, operation='video', video=args.video,
                                   network=None, start=None, end=None)
    video = reader.execute(read_args, cfg)['items'][0]
    due = video.get('status', {}).get('publishAt')
    now = dt.datetime.now(dt.timezone.utc)
    if (video.get('status', {}).get('privacyStatus') != 'private'
            or not now + dt.timedelta(minutes=5) < instant(due) <= now + dt.timedelta(days=7)):
        raise ValueError('Requires existing private YouTube schedule 5 minutes to 7 days ahead')
    key = cfg['BUFFER_HOS_API_KEY' if args.channel == 'hos' else 'BUFFER_API_KEY']
    plan = []
    # Validate every registered post before making the first edit.
    for network, receipt in entry['channels'].items():
        channel_id = CHANNELS[args.channel][network]
        post_id = receipt['postId']
        post = checked_post(buffer_call(key, GET, {'id': post_id}).get('post'), post_id, channel_id)
        plan.append({'network': network, 'postId': post_id, 'oldDueAt': post['dueAt'], 'dueAt': due,
                     'change': instant(post['dueAt']) != instant(due)})
    if args.apply:
        for item in plan:
            if not item['change']:
                continue
            # Recheck remote post and live YouTube immediately before each mutation.
            current = checked_post(buffer_call(key, GET, {'id': item['postId']}).get('post'),
                                   item['postId'], CHANNELS[args.channel][item['network']])
            live = reader.execute(read_args, cfg)['items'][0]['status']
            if (live.get('privacyStatus') != 'private' or instant(live.get('publishAt')) != instant(due)
                    or instant(due) <= dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=5)
                    or instant(current['dueAt']) != instant(item['oldDueAt'])):
                raise ValueError('Schedule changed during reconciliation')
            response = buffer_call(key, EDIT, {'id': item['postId'], 'mode': 'customScheduled', 'dueAt': due})
            action = response.get('editPost', {})
            if action.get('__typename') != 'PostActionSuccess':
                raise ValueError('Schedule edit failed')
            post = checked_post(action.get('post'), item['postId'], CHANNELS[args.channel][item['network']])
            if instant(post['dueAt']) != instant(due):
                raise ValueError('Schedule edit did not match')
            # Persist each confirmed edit, so partial failures have a durable receipt.
            entry['channels'][item['network']]['scheduleReconciledAt'] = dt.datetime.now(dt.timezone.utc).isoformat()
            entry['channels'][item['network']]['dueAt'] = due
            atomic_ledger(file, ledger)
        entry['dueAt'] = due
        atomic_ledger(file, ledger)
    return {'channel': args.channel, 'video': args.video, 'applied': args.apply, 'posts': plan}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--channel', choices=tuple(CHANNELS), required=True)
    parser.add_argument('--video', required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args(argv)
    try:
        if not re.fullmatch(r'[A-Za-z0-9_-]{11}', args.video):
            raise ValueError('Invalid video ID')
        reader = read_gateway()
        with desk_lock():
            result = run(args, reader, reader.settings())
        print(json.dumps(result))
        return 0
    except (ValueError, KeyError, TypeError, AttributeError, OSError, http.client.HTTPException):
        print('Buffer schedule refused or failed. Check ledger receipts before retry; no raw service errors are printed.')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
