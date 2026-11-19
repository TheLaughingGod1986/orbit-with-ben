#!/usr/bin/env python3
"""Prepare a Mini service plist without installing or starting it.

Read the installed plist to preserve its scheduling, locks, logs and local environment.
Write only to a new, private staging file. Install during the drained cutover window.
"""
import argparse
import copy
import pathlib
import plistlib

SERVICES = {
    'com.owb.chief-relay': ('chief_relay.py', 'run'),
    'com.owb.board-publish': ('board_publish.py', '--quiet'),
}

SHELL_SERVICES = {
    'dev.orbit.buffer-check': '07_Content-Ops/launchd/buffer-check.sh',
}


def absolute(value):
    path = pathlib.Path(value)
    if not path.is_absolute():
        raise ValueError('runtime paths must be absolute')
    return str(path)


def render(source, engine, python, channel_paths):
    doc = copy.deepcopy(source)
    if doc.get('Label') not in SERVICES and doc.get('Label') not in SHELL_SERVICES:
        raise ValueError('only the relay, board publisher and Buffer timer are supported')
    engine, python = absolute(engine), absolute(python)
    if doc['Label'] in SHELL_SERVICES:
        target = pathlib.Path(engine) / SHELL_SERVICES[doc['Label']]
        argv = ['/bin/bash', str(target)]
    else:
        script, argument = SERVICES[doc['Label']]
        target = pathlib.Path(engine) / 'scripts' / script
        argv = [python, str(target), argument]
    if not target.is_file():
        raise ValueError('the staged engine lacks the service script')
    if not pathlib.Path(python).is_file():
        raise ValueError('the Python executable is missing')
    # An argv array avoids shell expansion and login-profile path overrides.
    doc.pop('Program', None)
    doc['ProgramArguments'] = argv
    doc['WorkingDirectory'] = engine
    env = doc.setdefault('EnvironmentVariables', {})
    env['STUDIO_REPO'] = engine
    for name, path in channel_paths.items():
        if name not in ('OWB_REPO', 'HOS_REPO', 'WW2_REPO'):
            raise ValueError('unsupported channel environment name')
        env[name] = absolute(path)
    return plistlib.dumps(doc, sort_keys=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ('source', 'engine', 'python', 'owb', 'hos', 'ww2', 'out'):
        ap.add_argument('--' + name, required=True)
    args = ap.parse_args()
    data = render(plistlib.loads(pathlib.Path(args.source).read_bytes()), args.engine, args.python,
                  {'OWB_REPO': args.owb, 'HOS_REPO': args.hos, 'WW2_REPO': args.ww2})
    # Installed plists can hold local secrets: never echo their contents or put them in Git.
    import os
    fd = os.open(args.out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as handle:
        handle.write(data)


if __name__ == '__main__':
    main()
