#!/usr/bin/env python3
"""Stage a reviewed remote Cursor wrapper; never install or execute it.

The source can contain local credential setup. Outputs must stay outside Git.
The expected hash binds the proposal to the separately inspected source.
"""
import argparse
import hashlib
import os
from pathlib import Path
import shlex
import subprocess

ROOTS = ('STUDIO_REPO', 'OWB_REPO', 'HOS_REPO', 'WW2_REPO')


def render(source, expected_sha256, roots):
    if hashlib.sha256(source).hexdigest() != expected_sha256:
        raise ValueError('source changed since inspection')
    if set(roots) != set(ROOTS):
        raise ValueError('all four repository roots are required')
    for value in roots.values():
        if not Path(value).is_absolute() or any(c in value for c in '\n\r\0'):
            raise ValueError('roots must be absolute single-line paths')
    text = source.decode('utf-8')
    marker = 'exec /usr/bin/caffeinate -dims \\\n'
    tail = '  start --verbose\n'
    if text.count(marker) != 1 or not text.endswith(tail):
        raise ValueError('unreviewed worker wrapper shape')
    prefix, invocation = text.split(marker)
    args = shlex.split(invocation.replace('\\\n', ''))
    if args[:3] != ['$AGENT', 'worker', '--computer-use']:
        raise ValueError('unreviewed worker command')
    if args[-2:] != ['start', '--verbose']:
        raise ValueError('unreviewed worker action')
    options = args[3:-2]
    allowed = {'--name', '--idle-release-timeout', '--data-dir', '--worker-dir'}
    if len(options) % 2 or any(options[i] not in allowed for i in range(0, len(options), 2)):
        raise ValueError('unreviewed worker options')
    dirs = [options[i+1] for i in range(0, len(options), 2) if options[i] == '--worker-dir']
    if not dirs or any(not Path(p).is_absolute() for p in dirs):
        raise ValueError('worker roots must be explicit absolute paths')
    # Appending keeps the first root: Cursor uses it as assignment identity.
    if roots['STUDIO_REPO'] in dirs:
        raise ValueError('engine root is already exposed')
    exports = ''.join('export ' + k + '=' + shlex.quote(roots[k]) + '\n' for k in ROOTS)
    added = '  --worker-dir ' + shlex.quote(roots['STUDIO_REPO']) + ' \\\n'
    result = prefix + exports + marker + invocation[:-len(tail)] + added + tail
    checked = subprocess.run(['/bin/bash', '-n'], input=result.encode(), capture_output=True)
    if checked.returncode:
        raise ValueError('proposal failed shell syntax check')
    return result.encode()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ('source', 'expected-sha256', 'engine', 'owb', 'hos', 'ww2', 'out'):
        ap.add_argument('--' + name, required=True)
    a = ap.parse_args()
    roots = dict(zip(ROOTS, (a.engine, a.owb, a.hos, a.ww2)))
    data = render(Path(a.source).read_bytes(), a.expected_sha256, roots)
    # Exclusive creation prevents replacing source, installed wrapper or earlier proposal.
    fd = os.open(a.out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as f:
        f.write(data)


if __name__ == '__main__':
    main()
