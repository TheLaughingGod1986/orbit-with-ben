#!/usr/bin/env python3
"""Non-force, non-deleting push to the two studio repos; no arbitrary Git options."""
import argparse
import os
from pathlib import Path
import re
import subprocess

REPOS = {
    'owb': 'https://github.com/TheLaughingGod1986/orbit-with-ben.git',
    'hos': 'https://github.com/TheLaughingGod1986/history-of-science.git',
}


def command(argv=None):
    p = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    p.add_argument('--repo', choices=REPOS, required=True)
    p.add_argument('--worktree', type=Path, required=True)
    p.add_argument('--branch', required=True)
    p.add_argument('--dry-run', action='store_true')
    a = p.parse_args(argv)
    # Require a branch ref only. A leading +, colon, option or deletion cannot enter.
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._/-]*', a.branch):
        p.error('branch must be a plain branch name')
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.pop('PYTHONPATH', None)
    env.pop('PYTHONHOME', None)
    base = ['/usr/bin/git', '-C', str(a.worktree.resolve()), '-c', 'core.hooksPath=/dev/null',
            '-c', 'remote.origin.mirror=false']
    subprocess.run(base + ['check-ref-format', '--branch', a.branch], env=env,
                   check=True, stdout=subprocess.DEVNULL)
    rewrites = subprocess.run(base + ['config', '--get-regexp', r'^url\..*\.(insteadOf|pushInsteadOf)$'],
                              env=env, capture_output=True, text=True)
    if rewrites.returncode != 1:
        p.error('URL rewrite configuration must be reviewed before unattended push')
    # Explicit URL avoids trusting origin/pushurl. Destination is always a branch,
    # source always HEAD. -- prevents argument interpretation; no user refspec.
    return base + ['push'] + (['--dry-run'] if a.dry_run else []) + [
        '--no-follow-tags', '--no-force', '--no-mirror', '--recurse-submodules=no', '--', REPOS[a.repo], 'HEAD:refs/heads/' + a.branch], env


def main():
    cmd, env = command()
    return subprocess.run(cmd, env=env).returncode


if __name__ == '__main__':
    raise SystemExit(main())
