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

1. R2 must pin bucket `owb-media` and the two existing `social/` / `social/hos/` scopes; reject bucket/host overrides, traversal, deletes and unrelated keys. `media-host-r2.ts` currently reads `R2_BUCKET` and exposes delete.
2. Buffer must pin the two configured organisations/channel sets, admit only create/read/update and preserve the existing scheduling/approval gates. `buffer-runner.ts` currently calls `deletePost` (line 139), rollback `deleteMedia` (224) and cleanup deletion (339). A blanket mirror/check rule therefore exceeds fix F.
3. YouTube must pin the channel, reject delete/auth/sign-in and unscheduled Public transitions, and retain package/gate checks. `youtube:auth` must never be included in a wildcard rule.
4. Test positive and negative payload/argument cases, install only the reviewed guarded commands, and verify loading in a subsequent ordinary worker run. Keep all other review behaviour unchanged. Test policy decisions rather than deliberately sending data to another host.

No film stage was approved or advanced. No service writes, uploads, publishing, account changes or spending occurred.
