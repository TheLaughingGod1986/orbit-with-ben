"""Finite launchd recovery ticks for the cutover; never runs a studio queue.

The registration survives supervisor/service failure. Each invocation has a 90s
wall budget, enforced by launchd as well as subprocess deadlines. No resident
polling daemon, remote shell, or agent process is used.
"""
from __future__ import annotations
import argparse
import contextlib
import fcntl
import json
import os
from pathlib import Path
import plistlib
import re
import subprocess
import sys
import time
import uuid
import macbook_cutover as m

STATUSES = {'installed-paused', 'stopped-paused', 'expired-paused', 'resumed'}


def read_plan(path, expected):
    path = Path(path)
    m.require(not path.is_symlink() and path.stat().st_mode & 0o077 == 0, 'private plan required')
    raw = path.read_bytes()
    m.require(m.digest(raw) == expected, 'plan changed')
    plan = json.loads(raw)
    plan['plan_hash'] = expected
    for name, sha in plan.get('control_bundle', {}).items():
        p = path.parent / 'control' / name
        m.require(not p.is_symlink() and m.digest(p.read_bytes()) == sha, 'control bundle drift')
    return plan


def owned_pause(plan, directory):
    p = Path(plan['pause'])
    m.require(p.is_file() and not p.is_symlink(), 'pause absent or symlink')
    stat = p.stat()
    actual = {'device': stat.st_dev, 'inode': stat.st_ino, 'ctime': stat.st_ctime_ns,
              'hash': m.digest(p.read_bytes())}
    saved = json.loads((Path(directory) / 'pause-identity.json').read_bytes())
    m.require(actual == saved, 'pause ownership changed')
    token = m.canonical({'job': plan['job'], 'nonce': plan['nonce'], 'plan': plan['plan_hash']})
    m.require(p.read_bytes() == token, 'pause is not migration owned')
    return actual


def create_pause(plan, directory):
    # Called only by the separately authorized live coordinator. O_EXCL refuses
    # every pre-existing pause, including an empty user pause.
    p = Path(plan['pause'])
    m.private_write(p, m.canonical({'job': plan['job'], 'nonce': plan['nonce'], 'plan': plan['plan_hash']}))
    s = p.stat()
    m.private_write(Path(directory) / 'pause-identity.json', m.canonical({
        'device': s.st_dev, 'inode': s.st_ino, 'ctime': s.st_ctime_ns, 'hash': m.digest(p.read_bytes())}))


@contextlib.contextmanager
def control_lock(directory):
    p = Path(directory) / 'control.lock'
    m.require(not p.is_symlink(), 'symlink control lock')
    with p.open('a') as f:
        os.chmod(p, 0o600)
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise m.Refused('supervisor/control active') from None
        yield


def label(plan):
    return m.LABEL + '.cutover-' + plan['nonce']


def recovery_plist(plan_path, expected, plan):
    return plistlib.dumps({'Label': label(plan), 'ProgramArguments': [sys.executable,
        str(Path(plan_path).resolve().parent / 'control/macbook_cutover_control.py'), 'tick', '--plan', str(Path(plan_path).resolve()), '--sha256', expected],
        'StartInterval': 180, 'RunAtLoad': True, 'ProcessType': 'Background',
        'TimeOut': 90, 'ExitTimeOut': 5, 'AbandonProcessGroup': False,
        'StandardOutPath': '/dev/null', 'StandardErrorPath': '/dev/null'})


def arm(plan_path, expected, plan, io):
    directory = Path(plan_path).parent
    owned_pause(plan, directory)
    source_pins(plan)
    m.require(set(plan.get("control_bundle", {})) == {"macbook_cutover.py", "macbook_cutover_control.py", "engine_guard.py",
        "macbook/render_worker_plist.py", "macbook/" + m.render_worker_plist.TEMPLATE.name}, "missing recovery bundle")
    read_plan(plan_path, expected)
    # Durable, independently registered before the supervisor may replace the
    # worker service. It stays available on failure/expiry; no KeepAlive loop.
    p = directory / 'recovery.plist'
    m.private_write(p, recovery_plist(plan_path, expected, plan))
    io.run(['launchctl', 'bootstrap', f'gui/{os.getuid()}', str(p)])
    io.run(['launchctl', 'print', f'gui/{os.getuid()}/{label(plan)}'])
    m.private_write(directory / 'recovery-armed', m.canonical({'plan': expected}))


def immutable(c, plan, now):
    m.require(c.get('author_association') in {'OWNER', 'MEMBER', 'COLLABORATOR'}
              and c.get('user', {}).get('type') == 'User', 'untrusted control')
    m.require(c.get('issue_url') == plan['issue_url'], 'wrong control thread')
    m.require(c.get('created_at') == c.get('updated_at'), 'edited control')
    age = now - m.timestamp(c['created_at'])
    m.require(0 <= age <= 600 and m.timestamp(c['created_at']) >= plan['created'], 'stale control')


def command(c, plan, activation, now):
    immutable(c, plan, now)
    pattern = (r'\[Chief\] MACBOOK-(STATUS|RECOVER|RESUME) coordinator=' + re.escape(plan['job'])
        + ' nonce=' + re.escape(plan['nonce']) + ' plan=' + plan['plan_hash']
        + ' commit=' + activation['commit'] + ' activation=' + str(activation['id'])
        + ' activation-sha256=' + activation['hash']
        + r' chief=(claude|codex|gemini|chief) elected=confirmed global-freeze=confirmed')
    match = re.fullmatch(pattern, c.get('body', ''))
    m.require(match is not None, 'mismatched control')
    return match[1], match[2]


def activation_for(plan, directory, io):
    saved = json.loads((directory / 'activation.json').read_bytes())
    c = io.comment(plan, saved['id'])
    # Activation was fresh when accepted; expiry never grants new installation
    # authority. Recovery uses a NEW fresh command, original must stay immutable.
    actual = m.validate_activation(c, plan, plan['plan_hash'], m.timestamp(c['created_at']))
    m.require(actual == saved, 'activation changed')
    return saved


def source_pins(plan):
    for path, expected in plan['sources'].items():
        if path == plan['installed']:  # installed service intentionally replaced
            continue
        m.require(m.digest(Path(path).read_bytes()) == expected, 'source drift')


def not_cancelled(plan, io):
    # Cancellation is independent of the expired installation deadline. STATUS
    # remains available, but no recovery/resume effect may override a stop.
    p = Path(plan['cancel'])
    m.require(not p.exists() and not p.is_symlink(), 'cancelled locally')
    body = f"[Chief] MACBOOK-CANCEL J3892 coordinator={plan['job']} {plan['nonce']}"
    m.require(not any(row.get('body') == body
        and row.get('issue_url') == plan['issue_url']
        and row.get('author_association') in {'OWNER', 'MEMBER', 'COLLABORATOR'}
        and row.get('user', {}).get('type') == 'User'
        for row in io.comments(plan)), 'cancelled on thread')
    # Network reads can take time; also check the local stop afterwards.
    m.require(not p.exists() and not p.is_symlink(), 'cancelled locally')


def recovery_drained(plan, directory, io):
    owners = list(plan['owners'])
    for p in directory.glob('descendants-*.json'):
        m.require(re.fullmatch(r'descendants-[0-9a-f]+\.json', p.name) is not None,
                  'invalid descendant receipt name')
        m.require(not p.is_symlink() and p.is_file()
                  and p.stat().st_mode & 0o077 == 0, 'private descendant receipt required')
        rows = json.loads(p.read_bytes())
        m.require(isinstance(rows, list) and bool(rows), 'invalid descendant receipt')
        for row in rows:
            m.require(isinstance(row, dict) and set(row) == {'pid', 'pgid', 'start'},
                      'invalid descendant identity')
            m.require(all(type(row[k]) is int and row[k] > 0 for k in ('pid', 'pgid'))
                      and isinstance(row['start'], str) and bool(row['start'].strip()),
                      'invalid descendant identity')
        owners.extend(rows)
    m.drained(dict(plan, owners=owners), io.queue(plan), io.processes(), os.getpid())


def verify_install(plan, activation, directory, io, recover=False, authorize=lambda: None):
    not_cancelled(plan, io)
    owned_pause(plan, directory)
    recovery_drained(plan, directory, io)
    source_pins(plan)
    io.production(plan, activation)
    for root in plan['engines']:
        if recover and io.git(root, 'rev-parse', 'HEAD') != activation['commit']:
            # Only the exact originally staged head can be advanced, using the
            # original no-reset/source/root/queue/drain checks. Arbitrary drift
            # is refused, never repaired on trust.
            authorize()
            io.update_engine(Path(root), plan, activation, 'pre-recovery-' + uuid.uuid4().hex)
        m.require(io.git(root, 'rev-parse', 'HEAD') == activation['commit'], 'engine head drift')
        m.require(io.git(root, 'branch', '--show-current') == 'main', 'engine branch drift')
        m.require(not io.git(root, 'status', '--porcelain'), 'engine dirty')
        m.require(io.git(root, 'remote', 'get-url', 'origin') == plan['production_url'], 'engine origin drift')
        for name, expected in plan['production_sources'].items():
            m.require(m.digest(Path(root, name).read_bytes()) == expected, 'production source drift')
    proposed = Path(plan['installed']).read_bytes()
    if recover and m.digest(proposed) == plan['installed_hash']:
        m.require(not Path(plan['marker']).exists(), 'marker exists before replacement')
        m.loaded_matches(io.loaded().decode(), proposed)
        proposed = m.proposal(proposed, plan['engines'], plan['production_url'])
        m.require(m.digest(proposed) == plan['proposal_hash'], 'proposal drift')
        attempt = directory / ('attempt-' + uuid.uuid4().hex)
        attempt.mkdir(mode=0o700)
        m.private_write(attempt / 'installed.plist', Path(plan['installed']).read_bytes())
        m.private_write(attempt / 'proposed.plist', proposed)
        m.private_write(attempt / 'replacement-started', b'explicit recovery; retain pause\n')
        authorize()
        io.replace(plan, proposed, attempt.name)
        proposed = Path(plan['installed']).read_bytes()
    m.require(m.digest(proposed) == plan['proposal_hash'], 'installed service drift')
    try:
        loaded = io.loaded()
    except m.Refused:
        m.require(recover, 'installed service not loaded')
        # Explicit RECOVER only: bootstrap EXACT already-installed new service,
        # never restore old service, rewrite a branch or run the stale queue.
        authorize()
        io.run(['launchctl', 'bootstrap', f'gui/{os.getuid()}', plan['installed']])
        loaded = io.loaded()
    m.loaded_matches(loaded.decode(), proposed)
    marker = m.canonical({'version': 1, 'github': plan['production_repo']})
    p = Path(plan['marker'])
    if not p.exists() and recover:
        authorize()
        m.private_write(p, marker)
    m.require(not p.is_symlink() and p.read_bytes() == marker, 'marker drift')
    import engine_guard
    for root in plan['old_engines']:
        m.require(str(engine_guard.refusal(root, p)).startswith('This engine repository is retired;'), 'old engine guard drift')
    for root in plan['engines']:
        m.require(engine_guard.refusal(root, p) is None, 'new engine guard drift')
    owned_pause(plan, directory)
    recovery_drained(plan, directory, io)
    not_cancelled(plan, io)


def evidence(directory):
    # Hash only named private evidence; never relay its content or path.
    names = {'result.json', 'installed-original.plist', 'loaded-original.txt', 'original-metadata.json',
             'activation.json', 'pause-identity.json'}
    rows = []
    for p in directory.iterdir():
        if p.name in names and p.is_file():
            rows.append(m.digest(p.read_bytes()))
        elif p.is_dir() and re.fullmatch(r'attempt-[0-9a-f]+', p.name):
            for n in ('installed.plist', 'loaded-before.txt', 'proposed.plist', 'replacement-started', 'loaded-after.txt', 'success.json'):
                q = p / n
                if q.is_file(): rows.append(m.digest(q.read_bytes()))
    return m.digest(m.canonical(sorted(rows)))


def receipt(plan, activation, directory, status, request=0, chief=None):
    m.require(status in STATUSES, 'invalid public status')
    return {'status': status, 'job': plan['job'], 'nonce': plan['nonce'], 'plan': plan['plan_hash'],
        'commit': activation['commit'] if activation else None,
        'activation': activation['id'] if activation else None,
        'activation_sha256': activation['hash'] if activation else None,
        'source_sha256': m.digest(m.canonical(sorted(plan['sources'].values()))),
        'receipt_sha256': evidence(directory), 'request': request, 'chief': chief}


def deliver(plan, io, value):
    body = '[MacBook] MACBOOK-RESULT ' + m.canonical(value).decode()
    # An ambiguous POST response is resolved by an authenticated exact-body
    # readback on the next tick, not an unbounded retry or a mutable edit.
    def matches():
        return [c for c in io.comments(plan) if c.get('body') == body
            and c.get('issue_url') == plan['issue_url']
            and c.get('author_association') in {'OWNER', 'MEMBER', 'COLLABORATOR'}
            and c.get('user', {}).get('type') == 'User'
            and c.get('created_at') == c.get('updated_at')]
    if matches(): return
    io.post(plan, body)
    m.require(bool(matches()), 'receipt delivery unconfirmed')


def current_status(plan, directory):
    if (directory / 'resumed.json').exists(): return 'resumed'
    if (directory / 'verified-install.json').exists(): return 'installed-paused'
    p = directory / 'result.json'
    if p.exists():
        value = json.loads(p.read_bytes()).get('status')
        if value in {'installed-paused', 'stopped-paused'}: return value
    return 'expired-paused' if time.time() >= plan['deadline'] else 'stopped-paused'


def tick(plan_path, expected, io=None):
    directory = Path(plan_path).parent
    plan = read_plan(plan_path, expected)
    io = io or m.System(time.time() + 60)
    with control_lock(directory):
        activation = json.loads((directory / 'activation.json').read_bytes()) if (directory / 'activation.json').exists() else None
        if activation is None and time.time() >= plan['deadline']:
            # The install supervisor may expire before receiving authority.
            # A NEW immutable activation can bind recovery, but never itself
            # installs: Chief must then issue a separate fresh RECOVER command.
            candidates = []
            for row in io.comments(plan):
                try:
                    if m.timestamp(row['created_at']) < plan['deadline']: continue
                    candidates.append(m.validate_activation(row, plan, expected, time.time()))
                except (m.Refused, KeyError, ValueError):
                    continue
            m.require(len(candidates) <= 1, 'ambiguous recovery activation')
            if candidates:
                try:
                    owned_pause(plan, directory)
                    source_pins(plan)
                    not_cancelled(plan, io)
                except m.Refused:
                    pass  # Retain STATUS reporting without accepting authority.
                else:
                    activation = candidates[0]
                    m.private_write(directory / 'activation.json', m.canonical(activation))
        status = current_status(plan, directory)
        if activation is not None:
            try: activation_for(plan, directory, io)
            except m.Refused: status = 'stopped-paused'
        deliver(plan, io, receipt(plan, activation, directory, status))
        if status == 'resumed': return  # retry final delivery without replaying unlink
        if activation is None: return  # expired before activation: no authority to install
        for c in io.comments(plan):
            if not c.get('body', '').startswith('[Chief] MACBOOK-'): continue
            try:
                action, chief = command(c, plan, activation, time.time())
            except (m.Refused, KeyError, ValueError):
                continue
            done = directory / ('control-' + str(c['id']) + '.json')
            if done.exists():
                deliver(plan, io, json.loads(done.read_bytes()))
                continue
            fresh = io.comment(plan, c['id'])
            m.require(m.digest(m.canonical(fresh)) == m.digest(m.canonical(c)), 'control changed during read')
            action, chief = command(fresh, plan, activation, time.time())
            try:
                if action in {'RECOVER', 'RESUME'}:
                    with m.slot_locks(plan['locks']):
                        if action == 'RESUME':
                            m.require(current_status(plan, directory) == 'installed-paused', 'install not verified')
                        def authorize():
                            m.require(io.comment(plan, c['id']) == fresh, 'control changed before effect')
                            command(fresh, plan, activation, time.time())
                            activation_for(plan, directory, io)
                            owned_pause(plan, directory)
                            source_pins(plan)
                            io.production(plan, activation)
                            recovery_drained(plan, directory, io)
                            not_cancelled(plan, io)
                        authorize()
                        verify_install(plan, activation, directory, io, recover=action == 'RECOVER', authorize=authorize)
                        # Re-fetch immutable fresh command after all network checks.
                        m.require(io.comment(plan, c['id']) == fresh, 'control changed before effect')
                        command(fresh, plan, activation, time.time())
                        if action == 'RECOVER':
                            authorize()
                            p = directory / 'verified-install.json'
                            if not p.exists(): m.private_write(p, m.canonical({'request': c['id'], 'chief': chief}))
                            status = 'installed-paused'
                        else:
                            authorize()
                            owned_pause(plan, directory)
                            recovery_drained(plan, directory, io)
                            not_cancelled(plan, io)
                            Path(plan['pause']).unlink()
                            status = 'resumed'
                            m.private_write(directory / 'resumed.json', m.canonical({'request': c['id'], 'chief': chief}))
            except Exception as error:
                # No exception string is relayed. Keep private evidence and a
                # stable failed receipt; retries never repeat a partial effect.
                m.private_write(directory / ("failure-" + str(c["id"]) + ".json"),
                    m.canonical({"type": type(error).__name__}))
                status = "stopped-paused"
            value = receipt(plan, activation, directory, status, c['id'], chief)
            m.private_write(done, m.canonical(value))
            deliver(plan, io, value)
            if status == 'resumed': return


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('verb', choices=['tick', 'tick-run', 'own-pause'])
    ap.add_argument('--plan', type=Path, required=True)
    ap.add_argument('--sha256', required=True)
    args = ap.parse_args()
    plan = read_plan(args.plan, args.sha256)
    if args.verb == 'own-pause': create_pause(plan, args.plan.parent)
    elif args.verb == 'tick-run': tick(args.plan, args.sha256)
    else:
        # launchd TimeOut is not a runtime limit. A finite parent explicitly
        # enforces the child wall time; gh children have their own <=30s caps.
        subprocess.run([sys.executable, str(Path(__file__).resolve()), 'tick-run',
            '--plan', str(args.plan), '--sha256', args.sha256], timeout=75,
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == '__main__':
    try: main()
    except Exception:
        # Keep local diagnostics private. Future ticks retain the remote route.
        sys.exit(1)
