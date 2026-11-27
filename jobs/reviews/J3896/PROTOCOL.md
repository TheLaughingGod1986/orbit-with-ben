# Result and recovery boundary — J3896

Preparation only. Chief review and a separate coordination child are required before any live use. Parent J3012 remains 3/4. No live pause, service, marker, production ref or activation was changed here.

## Lifetime and trust

The coordinator prepares the private plan, then uses `macbook_cutover_control.py own-pause --plan <private-plan> --sha256 <digest>` instead of touching an empty pause. Exclusive creation refuses any pre-existing/user pause. Its exact content, device, inode and ctime are recorded privately. `macbook_cutover.py launch` registers the independent recovery job **before** detaching the supervisor. A failed registration refuses launch. The supervisor and recovery checks share an exclusive control lock; both slot locks must also be obtainable before any resume or recovery effect.

Preparation copies the reviewed helper, control module, engine guard, launcher renderer and template into a private digest-pinned bundle. Recovery uses that bundle, not a checkout that will return to main. Keep the private plan, bundle, originals and attempt evidence until Chief closes the migration. No dependency on a follow-up queue job, a working worker service, SSH, or the source checkout's branch.

The recovery job is a launchd `StartInterval` registration, not a resident daemon: every 180 seconds a one-shot parent runs a control check and exits. The parent caps its child at 75 seconds; external commands share a 60-second deadline and each has at most 30 seconds. launchd `TimeOut` is not relied on as a runtime cap. There is no KeepAlive, agent wake or queue execution. The registration deliberately survives the supervisor's deadline and worker bootstrap failure, so expiry does not strand the remote recovery route. After resume it only retries/read-backs the final sanitized receipt. Chief can retire the registration during a later ordinary maintenance job after observing that receipt. Neither failure nor expiry authorizes deleting it or resuming an old queue.

Only trusted, immutable GitHub User comments on the exact existing authority thread count. Original activation retains its exact-source/root-commit/queue/freshness/drain requirements. A control command is fresh for ten minutes, names the job, nonce, plan digest, production commit, activation ID and full activation digest, and explicitly attests the elected Chief identity and global freeze. The original activation must still be unchanged. Chief succession is explicit in `chief=`, and the receipt records it; a MacBook result is never parsed as Chief authority. As with the original activation, elected role/global freeze are trusted-author attestations, not inferred from a label or local heartbeat.

## Ordinary coordinator exit to Mini-observed result

1. A separately approved coordinator prepares and owns its pause, arms recovery, posts the exact original activation request information, marks itself terminal and exits. The supervisor waits for the owning PID/group/observed descendants, claims and both locks to drain. No ordinary worker is killed.
2. Installation leaves the migration pause intact and privately records the original service, loaded settings, replacement boundary and outcome. On its next bounded tick, recovery posts `[MacBook] MACBOOK-RESULT` followed by canonical JSON. Only status, identifiers, hashes and control attribution are emitted. Local paths, config, exception strings and process details never leave the machine.
3. Mini retrieves the result from the existing thread, confirms the author is OWNER/MEMBER/COLLABORATOR, type User, exact thread, no edits, and matches the coordinator's known job, nonce and plan. It saves the complete comment JSON as `result-comment.json` locally. The following exact sequence builds a command using structured JSON, with no report interpolation. Replace the chosen verb and elected role in the Python source; do not put report text into shell arguments.

```sh
# Read an observed result by its numeric comment ID, using the existing thread repo.
gh api repos/TheLaughingGod1986/orbit-with-ben/issues/comments/RESULT_COMMENT_ID > result-comment.json
python3 - <<'PY'
import json, re
from pathlib import Path
comment = json.loads(Path('result-comment.json').read_text())
assert comment['author_association'] in {'OWNER', 'MEMBER', 'COLLABORATOR'}
assert comment['user']['type'] == 'User'
assert comment['created_at'] == comment['updated_at']
thread = json.loads(Path('scripts/thread.json').read_text())
repo = thread['repo']
assert comment['issue_url'] == f"https://api.github.com/repos/{repo}/issues/{thread['number']}"
prefix = '[MacBook] MACBOOK-RESULT '
assert comment['body'].startswith(prefix)
r = json.loads(comment['body'][len(prefix):])
# Compare these identifiers with the coordinator's previously verified request.
assert re.fullmatch(r'J[0-9]+', r['job'])
assert re.fullmatch(r'[0-9a-f]+', r['nonce'])
for k in ('plan', 'activation_sha256', 'receipt_sha256', 'source_sha256'):
    assert re.fullmatch(r'[0-9a-f]{64}', r[k])
assert re.fullmatch(r'[0-9a-f]{40}', r['commit'])
assert isinstance(r['activation'], int)
verb, chief = 'STATUS', 'codex'  # elected Chief selects STATUS, RECOVER or RESUME
body = (f"[Chief] MACBOOK-{verb} coordinator={r['job']} nonce={r['nonce']} plan={r['plan']} "
        f"commit={r['commit']} activation={r['activation']} activation-sha256={r['activation_sha256']} "
        f"chief={chief} elected=confirmed global-freeze=confirmed")
Path('control-request.json').write_text(json.dumps({'body': body}))
Path('control-endpoint.txt').write_text(f"repos/{repo}/issues/{thread['number']}/comments")
PY
# Endpoint is read as data; the command body is never shell-evaluated.
python3 - <<'PY'
from pathlib import Path
import subprocess
subprocess.run(['gh','api','--method','POST',Path('control-endpoint.txt').read_text(),
                '--input','control-request.json'], check=True, timeout=30)
PY
```

4. STATUS returns an immutable receipt with the request comment ID. Rebuild with RESUME only after Mini observes `installed-paused` and Chief has reviewed its exact identifiers/digests. RESUME rechecks the immutable activation, fresh command, source pins, both production roots/heads/origins/main/cleanliness, exact production source bytes, current private parentless production main, installed plist and loaded arguments/environment, marker, engine guards, original owner/group/claims and exact pause ownership. It removes only that migration pause while holding both slot locks. The existing launcher then governs both slots, content roots, identities, heartbeats, mains and idle policy unchanged. It does not force either slot to run while its policy forbids it.
5. Observe a `resumed` receipt naming the exact request and elected role. A lost POST response is resolved by trusted immutable exact-body readback on the next tick. It never edits a receipt, and retry never repeats pause removal.

## Failure, partial switch and expired supervisor

A failed or expired supervisor leaves private originals and attempt evidence, keeps the pause and never restores the old queue. Recovery checks remain independently registered. The first receipt is `stopped-paused` or `expired-paused` with a digest over allowlisted private evidence; STATUS requests retrieve fresh receipt digests after the supervisor has exited. Raw rollback artifacts remain machine-local by design; the digest is the cross-machine evidence reference, not a claim that Mini has read their content.

If an activation was accepted, Chief can issue a **new**, fresh RECOVER through the same sequence even after the installation deadline. It runs under a new bounded invocation, both locks and the original drain checks. Only an exact originally staged head may advance, through the existing source/root/queue/no-reset checks. Only the original installed plist may be replaced with the pinned proposal; an already-installed exact proposal can be bootstrapped if the worker service failed to load. It never overwrites arbitrary drift. It can create the exact expected marker if missing, validates both engine guards, and reports `installed-paused`. It **retains** the pause. Chief then issues a separate fresh RESUME. Failure records an immutable failed request receipt; a repeated request does not repeat partial service effects. A new recovery attempt requires a new Chief comment.

If activation never arrived, expiry reports null activation/commit identifiers and cannot install or resume anything. The independent recovery tick can accept exactly one NEW original-format activation posted after the supervisor deadline, with the same job/nonce/plan pins and fresh trusted immutable Chief/global-freeze authority. It reports the bound activation but performs no installation. Chief then uses that new result in the sequence above to issue RECOVER, observes installed-paused, and separately issues RESUME. Thus even pre-activation expiry has a remote recovery route without unpausing an old queue or claiming a new job. Stale, edited or ambiguous activations refuse. A replaced/user pause, source drift, changed marker, arbitrary engine head or production drift always stays paused for Chief repair. No generic remote shell or arbitrary file-writing command is exposed.

## Evidence

`MOCK_RECEIPT.json` records this machine's mocked tests and exact source hashes. It is preparation evidence, not live installation acceptance. All process, service, Git and network effects in protocol/helper tests use fake adapters; temporary fixture files stand in for pauses, locks and markers. No rehearsal queue was run.
