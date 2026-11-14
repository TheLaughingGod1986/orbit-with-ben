#!/usr/bin/env python3
"""J2040: upload one registered social asset to the existing R2 bucket only.

Installed with Python isolated mode. No caller URLs, keys, bucket, HTTP method,
environment overrides or executable imports. No deletion or overwrite route.
"""
import argparse
import datetime as dt
import hashlib
import hmac
import http.client
import json
from pathlib import Path
import re
import secrets

ROOT = Path('/Users/benjaminoats/YouTube/orbit-with-ben')
HOS = Path('/Users/benjaminoats/YouTube/History Of Science')
SOCIAL = Path('00_Brand/Channel-Setup/social')
TYPES = {'.mp4': 'video/mp4', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png'}


def settings():
    # Parse literal dotenv values only; never execute/source the file. Inherited
    # environment deliberately has no influence on credentials or destination.
    wanted = {'R2_ACCOUNT_ID', 'R2_ACCESS_KEY_ID', 'R2_SECRET_ACCESS_KEY', 'R2_PUBLIC_URL', 'R2_BUCKET'}
    values = {}
    for line in (ROOT / '07_Content-Ops/.env').read_text().splitlines():
        key, sep, value = line.strip().partition('=')
        if sep and key in wanted:
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            values[key] = value
    if not re.fullmatch('[a-f0-9]{32}', values.get('R2_ACCOUNT_ID', '')):
        raise ValueError('R2 account configuration is invalid')
    if values.get('R2_BUCKET', 'owb-media') != 'owb-media':
        raise ValueError('Only bucket owb-media is authorised')
    if not re.fullmatch(r'https://[a-zA-Z0-9-]+\.r2\.dev/?', values.get('R2_PUBLIC_URL', '')):
        raise ValueError('Expected the existing R2 public hostname')
    if not values.get('R2_ACCESS_KEY_ID') or not values.get('R2_SECRET_ACCESS_KEY'):
        raise ValueError('R2 credentials unavailable')
    return values


def asset(channel, video, role):
    if channel not in ('owb', 'hos') or not re.fullmatch(r'[A-Za-z0-9_-]{11}', video):
        raise ValueError('Invalid channel or YouTube id')
    if role not in ('media', 'thumb', 'trailer'):
        raise ValueError('Invalid asset role')
    folder = ROOT / SOCIAL / ('hos' if channel == 'hos' else '')
    entry = json.loads((folder / 'UPLOADS.json').read_text())['videos'][video]
    if channel == 'hos' and (entry.get('kind') != 'short' or role != 'media'):
        raise ValueError('HOS social only supports registered Shorts media')
    if role == 'media' and entry.get('kind') != 'short':
        raise ValueError('Longs use the registered trailer or thumbnail')
    raw = entry.get('file' if role == 'media' else role)
    if not isinstance(raw, str) or not raw:
        raise ValueError('Requested asset is not registered')
    file = Path(raw)
    file = (file if file.is_absolute() else (HOS if channel == 'hos' else ROOT) / file).resolve()
    roots = (ROOT, HOS, Path('/Volumes/data/mac-mini-archive'))
    if not any(file.is_relative_to(root.resolve()) for root in roots):
        raise ValueError('Registered asset is outside the studio media roots')
    if file.suffix.lower() not in TYPES or not file.is_file():
        raise ValueError('Registered asset is not supported media')
    # Refuse a renamed text/secret file even if a record accidentally names one.
    with file.open('rb') as stream:
        head = stream.read(16)
    ext = file.suffix.lower()
    valid = (ext == '.mp4' and head[4:8] == b'ftyp' or
             ext in ('.jpg', '.jpeg') and head.startswith(b'\xff\xd8\xff') or
             ext == '.png' and head.startswith(b'\x89PNG\r\n\x1a\n'))
    if not valid:
        raise ValueError('Media signature does not match extension')
    suffix = '' if role == 'media' else '-' + role
    prefix = 'social/hos/' if channel == 'hos' else 'social/'
    return file, prefix + video + suffix + '-' + secrets.token_hex(16) + ext


def signature(cfg, key, digest, now):
    host = cfg['R2_ACCOUNT_ID'] + '.r2.cloudflarestorage.com'
    stamp, day = now.strftime('%Y%m%dT%H%M%SZ'), now.strftime('%Y%m%d')
    uri = '/owb-media/' + key
    # key is built exclusively from validated IDs, fixed prefixes and hex.
    headers = {'host': host, 'if-none-match': '*', 'x-amz-content-sha256': digest, 'x-amz-date': stamp}
    names = ';'.join(sorted(headers))
    canonical = ''.join(k + ':' + headers[k] + '\n' for k in sorted(headers))
    request = '\n'.join(('PUT', uri, '', canonical, names, digest))
    scope = day + '/auto/s3/aws4_request'
    to_sign = '\n'.join(('AWS4-HMAC-SHA256', stamp, scope, hashlib.sha256(request.encode()).hexdigest()))
    derived = ('AWS4' + cfg['R2_SECRET_ACCESS_KEY']).encode()
    for value in (day, 'auto', 's3', 'aws4_request'):
        derived = hmac.new(derived, value.encode(), hashlib.sha256).digest()
    signed = hmac.new(derived, to_sign.encode(), hashlib.sha256).hexdigest()
    headers['Authorization'] = ('AWS4-HMAC-SHA256 Credential=' + cfg['R2_ACCESS_KEY_ID'] + '/' + scope +
                                ', SignedHeaders=' + names + ', Signature=' + signed)
    return host, uri, headers


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--channel', choices=('owb', 'hos'), required=True)
    parser.add_argument('--video', required=True)
    parser.add_argument('--role', choices=('media', 'thumb', 'trailer'), required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)
    try:
        file, key = asset(args.channel, args.video, args.role)
        cfg = settings()
        # One file descriptor for hashing and transfer avoids pathname swaps.
        with file.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
            size = stream.tell()
            stream.seek(0)
            if args.dry_run:
                print(json.dumps({'dryRun': True, 'bucket': 'owb-media', 'key': key, 'sha256': digest, 'bytes': size}))
                return 0
            host, uri, headers = signature(cfg, key, digest, dt.datetime.now(dt.timezone.utc))
            headers.update({'Content-Type': TYPES[file.suffix.lower()], 'Content-Length': str(size)})
            # HTTPSConnection uses normal CA verification, no proxy/redirect or
            # arbitrary destination. Conditional PUT prevents object replacement.
            connection = http.client.HTTPSConnection(host, timeout=120)
            try:
                connection.request('PUT', uri, body=stream, headers=headers)
                response = connection.getresponse()
                if not 200 <= response.status < 300:
                    raise ValueError('R2 upload failed with HTTP ' + str(response.status))
            finally:
                connection.close()
        print(json.dumps({'url': cfg['R2_PUBLIC_URL'].rstrip('/') + '/' + key, 'sha256': digest, 'bytes': size}))
        return 0
    except (ValueError, KeyError, OSError, http.client.HTTPException):
        # Never print remote bodies or exception text containing credentials.
        print('R2 upload refused or failed; check registration, media and R2 configuration.')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
