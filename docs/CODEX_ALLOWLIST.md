# Codex unattended allow-list — J2040, 4 November 2026

Partial implementation; **J2040 is not complete**. Ben authorised only the two studio repos, existing social R2 prefixes, Buffer create/read/update and the two channels' YouTube operations, retaining review for everything else.

Codex CLI on the Mini is 0.160.0. Official [OpenAI Rules documentation](https://learn.chatgpt.com/docs/agent-configuration/rules) confirms `.rules` files in `~/.codex/rules/`, prefix matching, the most restrictive matching decision, and `codex execpolicy check`. New files load at session startup; a fresh run is required to prove automatic loading. `match` and `not_match` are tests, not restrictions on trailing arguments. No approval policy or sandbox setting was changed.

## Installed Git slice

Exact rule copy: [codex/studio.rules](codex/studio.rules). Validating source: [../scripts/codex_scoped_push.py](../scripts/codex_scoped_push.py). Installed copies:

- `/Users/benjaminoats/.codex/rules/studio.rules`
- `/Users/benjaminoats/.codex/bin/studio-scoped-push.py`

Invoke with an absolute interpreter and isolated mode:

```sh
/opt/homebrew/bin/python3 -I /Users/benjaminoats/.codex/bin/studio-scoped-push.py --repo owb --worktree /private/tmp/j2040-wt --branch codex/j2040-permission-probe --dry-run
```

The rule permits only this installed gateway. It rejects unknown arguments, force/deletion/refspec syntax, invalid branch names and Git URL rewrite configuration. It strips inherited GIT_* variables, uses explicit HTTPS destinations, disables hooks, mirror/force/follow-tags and recursive submodule pushes, and pushes HEAD to one named branch. Git's normal non-fast-forward protection remains. The helper must receive ordinary code review before changes are reinstalled; a rule allowing a script trusts its installed contents. Existing `default.rules` was preserved, not audited or widened.

## Evidence and limits

- `codex execpolicy check --rules docs/codex/studio.rules -- <gateway invocation>`: `decision: allow`.
- Same check for `curl https://example.com`: `matchedRules: []`. This proves no allow from this file; it does **not** prove a live automatic-review refusal. A harmless curl can also execute inside the network-enabled sandbox without an escalation.
- Installed gateway dry-run returned 0 and reported `HEAD -> codex/j2040-permission-probe`. Git credential helper printed `failed to store: 100001`; Git still succeeded. No credentials were displayed.
- `git ls-remote --heads <explicit Orbit URL> refs/heads/codex/j2040-permission-probe` returned no refs. A dry-run creates no remote branch; no deletion was necessary or performed.
- Gateway validation tests pass; see `jobs/reviews/J2040/gateway-tests.txt`.
- No fresh Codex worker was started, so no claim is made that this running session reloaded the installed rule or that a subsequent push bypassed review because of it.
- J2007 is cancelled by Claude's 4 Nov WIP decision. Its recorded push was not retried.

## Remaining work (same J2040)

Do not allow broad `git push`, `npm run youtube:*`, `node`, `tsx`, `buffer-mirror.ts check`, Python or curl prefixes. Prefix rules cannot restrict appended flags, URLs, manifests or JSON bodies.

Before adding service rules, implement and test validating entry points in the repo's existing publishing path:

1. R2's restricted standalone gateway below now implements this slice. The ordinary mirror still uses `media-host-r2.ts`, which reads `R2_BUCKET` and exposes delete; its whole CLI remains outside the allow-list.
2. Buffer must pin the two configured organisations/channel sets, admit only create/read/update and preserve the existing scheduling/approval gates. `buffer-runner.ts` currently calls `deletePost` (line 139), rollback `deleteMedia` (224) and cleanup deletion (339). A blanket mirror/check rule therefore exceeds fix F.
3. YouTube must pin the channel, reject delete/auth/sign-in and unscheduled Public transitions, and retain package/gate checks. `youtube:auth` must never be included in a wildcard rule.
4. Test positive and negative payload/argument cases, install only the reviewed guarded commands, and verify loading in a subsequent ordinary worker run. Keep all other review behaviour unchanged. Test policy decisions rather than deliberately sending data to another host.

No film stage was approved or advanced. No service writes, uploads, publishing, account changes or spending occurred.

## Resume evidence — 4 November, 20:03 UTC

Added [registered-media R2 gateway](../07_Content-Ops/scripts/codex_r2_upload.py), installed as `/Users/benjaminoats/.codex/bin/studio-r2-upload.py`, and its separate prefix rule in [the exact rule copy](codex/studio.rules). Invocation:

```sh
/opt/homebrew/bin/python3 -I /Users/benjaminoats/.codex/bin/studio-r2-upload.py --channel owb --video buaOI3QGm7U --role media --dry-run
```

Only `--channel owb|hos`, `--video <11-character ID>`, `--role media|thumb|trailer` and optional `--dry-run` are accepted. Without `--dry-run` it uploads the registered asset. The fixed main-checkout `UPLOADS.json` supplies the asset; no caller path, key, URL, bucket, method or body is accepted. HOS accepts registered Shorts media only. The registered file must resolve inside either studio checkout or the archive and match an MP4/JPEG/PNG signature. Credentials come only from the fixed studio `.env`, parsed as literals; inherited R2 settings have no effect. The gateway pins bucket `owb-media`, constructs the correct channel prefix and a random object key, and uses a conditional PUT (`If-None-Match: *`) to refuse replacement. TLS verifies certificates; no redirect, proxy, delete, list or arbitrary request path exists.

- Ten R2 boundary tests pass; the three existing Git tests also pass. The fixed-date, fake-credential SigV4 result independently matches installed `aws4fetch` 1.0.20. Tests cover destination overrides, traversal, renamed text files, channel/role/ID rejection, extra flags, inherited settings, exact PUT and a dry run with zero network calls.
- Installed R2 dry run succeeded for registered `buaOI3QGm7U` media: 5,766,376 bytes, SHA-256 `eef2359b4aa791177be6a9b4312806de1a23b177fec5430fb7c965c1af87a86e`. No live PUT was attempted. Successful real upload and Buffer adoption of the returned URL remain unverified.
- `execpolicy check` allows the R2 gateway and leaves the outside-list curl unmatched. The R2 rule was installed during this session; automatic loading requires a later session. No claim of reload is made.
- This later session's installed Git gateway dry-run succeeded as an ordinary sandbox command, without requesting escalation. `ls-remote` confirmed the scratch branch does not exist, so no branch deletion is needed. Network access in the sandbox means success alone does not identify which policy rule permitted it.
- The harmless outside-list `curl --head --max-time 10 https://example.com` was explicitly submitted with `sandbox_permissions=require_escalated` and approved, returning HTTP 200. This is an approval-review request, **not a refusal**, and does not prove that a harmless curl could not run in the network-enabled sandbox. No broad curl rule was added.
- J2007 remains cancelled; no push was retried.
- Required NAS offload completed with no eligible folders (`moved: []`, `nas: ok`, 11,749 MB free after). Disk remains below 20 GB; do not claim recovery. No copy was left running by this session.

J2040 stays at **3/4**, unfinished. The next run must implement guarded Buffer create/read/update and channel-pinned YouTube entry points, preserving schedule/package checks and blocking deletion, sign-in and unscheduled Public transitions. Do not allow the existing broad mirror/package commands in the meantime. The installed gateways and all future trusted-code changes need Chief's normal code review; this worker has issued no PASS or final approval.

## Earlier handoff (superseded by the resume below)

Draft PR: https://github.com/TheLaughingGod1986/orbit-with-ben/pull/490. The installed gateway also completed the real push of `codex/j2040-allowlist` using a normal sandbox call, with no escalation requested for that call. This proves execution succeeded; it does not identify whether the current session loaded the new rule. Service rules and fresh-session negative review verification remain unfinished.

Required disk housekeeping was attempted at 14 GiB free. The sandbox attempt safely skipped due to NAS write permission; the escalated `nas_offload.py --apply` process PID 74781 remained running without a summary at handoff (exec session 74764). Do not start another copy while it exists. No offload completion or space recovery is claimed.

## Resume — 4 November, 23:45 UTC: guarded service reads

Added [service read gateway](../07_Content-Ops/scripts/codex_service_read.py), installed at `/Users/benjaminoats/.codex/bin/studio-service-read.py`, with its exact narrow prefix in [studio.rules](codex/studio.rules). The service gateway uses only Python's standard library and isolated mode. Examples:

```sh
/opt/homebrew/bin/python3 -I /Users/benjaminoats/.codex/bin/studio-service-read.py --channel owb --operation channel
/opt/homebrew/bin/python3 -I /Users/benjaminoats/.codex/bin/studio-service-read.py --channel hos --operation video --video AMSriTQ-lcQ
/opt/homebrew/bin/python3 -I /Users/benjaminoats/.codex/bin/studio-service-read.py --channel owb --operation analytics --start 2026-10-01 --end 2026-10-02
/opt/homebrew/bin/python3 -I /Users/benjaminoats/.codex/bin/studio-service-read.py --channel hos --operation buffer-status --video AMSriTQ-lcQ --network instagram
```

`--dry-run` validates argument shape without reading credentials or making network calls; it does **not** check remote availability or ledger registration. Live Buffer reads derive the post ID from the selected profile's fixed `BUFFER_POSTS.json` and use that profile's key. HOS supports registered Shorts only; Orbit TikTok is excluded. The only GraphQL document is a fixed status query. Caller-supplied post IDs, queries, URLs, tokens and bodies are absent.

YouTube reads refresh the **existing read-only** Analytics sign-in, check `channels?mine=true` against the selected hard-coded channel ID, and check video ownership before returning a video. Analytics has a fixed daily report and explicit pinned channel ID, with validated dates. Missing/expired sign-ins fail; no login, authorization-code flow or credential-file write exists. HTTP destinations and methods are fixed; redirects are not followed, response sizes are capped, and failures print no remote body or credential. Environment destination/token overrides have no effect.

Validation this run:

- 11 service boundary tests plus 10 existing R2 tests and 3 Git tests pass (24 total).
- Live channel reads succeeded for both OWB and HOS, using their existing read-only sign-ins.
- Live OWB daily Analytics read for 1–2 October succeeded.
- Live HOS Buffer status read returned `sent` for registered `AMSriTQ-lcQ` Instagram post `6ade37886887a2efc1169c75`.
- Installed Git gateway dry-run succeeded without requesting escalation. It creates no branch; the probe branch remains absent.
- `execpolicy check` allows the service gateway; `curl https://example.com` remains unmatched by `studio.rules`. This is a policy-file check, not proof of live refusal, and no claim is made that this running session reloaded newly installed rules.
- Installed source/rules match their committed copies; hashes and results are in `jobs/reviews/J2040/service-read-evidence.json`.
- NAS offload was attempted as required below 20 GB: it declined outside the 01:00–06:00 NAS window, reporting 8,853 MB free. No offload process remains. Unrelated checkout edits were untouched.

### Current handoff

J2040 remains at the existing **3/4**, with PR490 extended on `codex/j2040-allowlist` in `/private/tmp/j2040-wt`. This is a safe checkpoint in the original 120-minute job, not completion or Chief approval. The next implementation must handle **guarded Buffer create/update and YouTube writes** through existing mirror/package gates. It must validate destinations, current ownership, scheduled times and package state, keep ledger/lock handling, reject every deletion, refuse sign-in/account changes, and refuse immediate unscheduled Public transitions. Do not add broad npm/tsx/node/Python/curl rules. Existing mirror and package commands still go through ordinary approval review.

Keep the 4-step plan and completed Git/R2/read slices. Finish write gateways with adversarial payload tests before installation; then check the installed rules in a later worker session and report the exact distinction between policy match, sandbox execution and approval review. J2007 is cancelled; do not retry its old push. No service mutation, media upload, publishing, spend or Chief PASS occurred in this run.
