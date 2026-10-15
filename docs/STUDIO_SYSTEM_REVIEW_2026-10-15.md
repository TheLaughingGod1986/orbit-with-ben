# Studio system review: unify OWB + HOS, clean up, optimise (15 Oct 2026)

Status: **a proposal for Chief, not a rule.** Ben asked (15 Oct 2026): "go through the full workflow, unify HOS and OWB but keeping their own rules, clean up and optimise the full system including the data collection and the ad hoc board, a smooth well-oiled machine for a YouTube and social studio." Chief owns `AGENTS.md` and the Never list, so each rule change below goes to Chief on #99 first. Code changes that fix a fault shipped straight away and are listed at the end.

## 1. What the evidence says (queue, repos, today's incidents)

**Queue (288 jobs):** 253 done (Cursor 149, Chief 62, Claude 24, Codex 9, Gemini 9), 17 cancelled, 13 blocked, 4 open, 1 claimed. The work gets done; the waste is in how jobs wait.
- **Churn.** J0103 (85 claim/release/reopen events), J0096 (77), J0167 (42), J0138 (41), J0140 (36). Today Cursor claimed and released the Saturn/Jupiter thumbnail job six times with nothing to do ("both tests still running"), and the Germs one the same. A job that waits on a date, a running test or a go-public time should not be open.
- **Dead claims.** Gemini held J0258 for 3 h past its ETA. The queue allows a takeover but the relay never reroutes a stalled claim, and the board showed it as running.
- **Gemini** did 9 of 253 jobs and stalled today; Cursor does 59% of everything. Routing leans on one worker.

**Two repos, one studio, drifting copies.** About 60% of the tooling is shared in intent but copied by hand:
| Item | OWB | HOS | Diff |
|---|---|---|---|
| `gate_shorts_open.py` | 575 lines | 402 | 233 changed lines |
| `youtube-package-upload.ts` | 282 | 248 | 164 |
| `STUDIO_PLAYBOOK.md` | 466 | 460 | 730 |
| `THUMBNAIL_AND_TITLE_RULES.md` | 110 | 89 | 171 |
| `weekly_public_audit.py`, `thumb_preview.py`, `retitle`, `pinned-comment`, `sync_rules.py` | | | 16–64 each |
| `gate-episode`, `review-script`, `import-performance-data`, `create-export-package` etc. | | | identical |
`07_Content-Ops/src` has 44 files in OWB and 155 in HOS. Every fix has to be made twice and one copy gets missed. The AGENTS.md files share the same machinery sections (job queue, relay, board, NAS, Stop-and-ask, Never) but each repo carries its own copy of the text.

**Single points of failure found today:**
1. **Vercel Blob Hobby store suspended** (usage limit). It carries the board's Approve/Request-changes ticks and the Buffer media host. Result: no new ticks saved, no social posts (Apophis, Saturn, Venus Shorts). The same store is used for two unrelated jobs.
2. **NAS NFS hard mount** hung the Mini (an unmount stuck uninterruptibly; two HOS jobs stopped). It also blocks masters, staging and J0175.
3. **Manual data collection.** The daily Studio read (impressions, CTR, avg % viewed) is a hand-run job (J0210 open; J0263 done by hand). The API snapshot has no 14 Oct file (the disk-full day) and nothing alerts on a missing day.
4. **ElevenLabs** is one account with no live reading on the board for the account Ben was looking at; the "83%" mismatch cost an hour.

**Board.** Data reaches it through `board_publish.py` → `board-data` branch → page. Gaps fixed today: stale lease shown as "Now", Short approvals not reaching Chief, no next-step view. Still open: board ticks depend on Blob; `/api/checks` 500s when the newest snapshot is unreadable.

## 2. Target design: one studio core, two channel packs

**Studio core** (shared, one copy, versioned): job queue and relay, Chief chain, board and tracker, analytics collector, gates that are channel-neutral (episode gate, script review, package upload, retitle, pinned comment, Buffer mirror, NAS rules), credit ledger, thumbnail ledger. Parametrised by a channel config file.

**Channel packs** (kept separate, owned by each channel; nothing in core overrides them): strategy, thumbnail and title rules, playbook sections that differ (Orbit Omni and no-Orbit-on-thumb rules; HOS Flow plates, Explorer, 7–9 minute shape), the contract rules (`hos-contract/rules.ts` and the OWB equivalent), Never-list lines that name a channel, `CHANNEL_META.json`.

Mechanically: core lives in a third small repo (`orbit-studio-core`), or a `core/` folder in OWB mirrored to HOS by `sync_rules.py`-style check in CI. Each channel imports core and supplies `channel.json` (ids, rules module, gate thresholds, paths). The duplicated gates become one gate with per-channel thresholds (Shorts length cap, open-hook rules, frame 0 rule).

**AGENTS.md** becomes three layers: `STUDIO_CORE.md` (workflow, jobs, relay, board, NAS, Stop-and-ask, shared Never), then per-channel `AGENTS.md` (strategy, packaging, production locks, channel Never). Docs-in-force order stays; core slots in below each channel's strategy and packaging docs so a channel rule always wins.

## 3. Plan, in order (each step shippable alone)

| # | Step | Who signs off |
|---|---|---|
| 1 | **Shipped today:** stalled claim reroute, board stale-lease, Shorts approvals, lanes view, NAS staging rule | done |
| 2 | **Waiting work is blocked, never open.** Rule: a job that waits on a date, a test, a go-public or a credit reset is blocked `waits for input: …` with the end time, and a Chief date-gate job reopens it. Add `jobs.py gate` to do both in one command; relay refuses to wake a worker on a job released 3 times in a day with the same note. | Chief |
| 3 | **Replace the Blob dependency.** Ticks: move to a free store the Mini can also read (GitHub-backed file via a token with repo contents scope, or a Supabase table). Social media host: keep until Blob returns or use a second free host. Either needs Ben's OK if it is a new account. | Ben (new service), Chief |
| 4 | **Data collection that cannot miss a day.** One daily collector (API snapshot, Studio read, spend readings, credit pools) with a freshness row on the board (green/amber/red per source), a catch-up run on the next wake, and an alert line on #99 when any source is over 26 h old. Turns J0210/J0263 into the same collector. | Chief |
| 5 | **Mini health.** Mount NAS with `soft,timeo,retrans` (or autofs) so a hang times out instead of freezing; relay checks `ls` with a 10 s timeout before any NAS job and blocks the job instead of hanging a tmux. | Ben (Mini change), Chief |
| 6 | **Worker balance.** Gemini only for facts/listing reads with a 25 min lease and auto-reroute (done); Codex for graphics and quick assembly; Cursor default. Track per-worker stall rate in the daily stats. | Chief |
| 7 | **Unify the shared tooling** (section 2). Start with the four identical scripts, then `gate_shorts_open.py` (merge to one, thresholds in channel.json), then the upload and retitle scripts. A CI check fails if a core file differs between repos. | Chief |
| 8 | **Docs.** Split AGENTS.md into core + channel; move superseded text to `_archive/`; one "state of the studio" page (`STATUS.md`) generated from the board. | Chief |
| 9 | **Board.** One data path (no Blob), lanes view (done), Approve for any item, data-freshness strip, a "what changed since I last looked" line. | Claude owns the page |

## 4. Shipped with this review (code, tested)
- `chief_relay.stalled_claims()`: a Mini claim more than 45 min past its ETA walks to the next worker in its chain (test added; AGENTS.md relay section updated).
- Board: expired claims no longer show as running; Shorts approvals post to Chief and show with a next step; lanes view.
