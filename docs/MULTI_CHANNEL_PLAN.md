# Multi-channel studio: plan (5 Nov 2026)

Ben, 5 Nov 2026: "decouple the studio workflow system from the individual channel repos ... so we just plug in new
channels ... each channel can have a slightly different rule set, slightly different flow that can be stored in the
actual channel repo itself." A third channel is coming once the current two run smoothly.

Ben, 10 Nov 2026: "there should be 3 GitHub repos. One for Studio, one for Orbit with Ben, and one for History of
Science ... one repo for the decoupled Studio, where we plug in the 2 repos ... We want a system that we can start
plugging in repos that will be channels." And: "recommend your findings and implement the best possible solution."

Status (10 Nov 2026): **phase 2 is done, phase 1 is part done, phases 3 and 4 are not started.**

- Done: `scripts/channels.py` (the loader), `channels/channels.json` (the registry), and each channel's own
  `studio/channel.json` in its repo, with a cached copy here for machines that lack that checkout.
- Part done: engine scripts asking the loader instead of naming a channel. `scripts/test_channel_ratchet.py` holds
  two counts per script in `scripts/channel_ratchet.json`. A ceiling can only go down, and a new script must have
  none.
  - **Names a channel:** 337 code lines in 22 scripts (362 in 32 before the first batch). The largest are
    `chief_relay.py`, `kanban_snapshot.py`, `approved_deliver.py`, `board_publish.py` and `video_tracker.py`; each
    of those gets its own change, because they run the live studio.
  - **Assumes the engine lives inside one channel's repo** (counted from 10 Nov): 40 code lines in 17 scripts. A
    call to `channels.home()`, or a path from the engine's root into channel content such as
    `ROOT / "02_Video-Projects"`.
- Some of what the first count holds is the engine's own name rather than a channel (`owb_thread.py`, `com.owb.*`
  launchd labels, `OWB_AGENT`). Those are renamed at the move in phase 3.
- Not started: the engine in its own repo (phase 3) and the one-command new channel (phase 4). Phase 3 does not
  start until both counts read zero for channel logic and the studio has run a clean week on it. The channel check
  and the template from phase 4 do not depend on the move and are being built now.

## Decisions, 10 Nov 2026 (changes to the plan below)

Three repos, as Ben says: `studio` (the engine), `orbit-with-ben` and `history-of-science` (channels). One queue,
one board and one thread, in the studio repo. On top of the 5 Nov plan:

1. **No home channel.** Today `orbit-with-ben` is "home": the engine sits in it and reads its films from its own
   root. In the studio repo there are no films. Orbit plugs in exactly as History of Science does, through the
   registry. The second count above tracks this.
2. **One progress format.** Orbit keeps one `status.json` per film. History of Science keeps one `PIPELINE.json`
   plus `STATUS.md` and a board page that are generated and then committed. On 10 Nov, 24 of its 69 open pull
   requests conflicted with `main`, most of them only on those three files. The standard for every channel is one
   status file per film, and no generated page is committed to a channel repo: the studio builds the board.
   History of Science moves to it with a converter before phase 3.
3. **The studio repo starts clean.** No copied history (this answers open question 3 the other way). The old
   history holds Google account addresses in 46 files here; a new repo with one first commit, and a pointer to
   the commit it was taken from, carries none. `orbit-with-ben` keeps the full history for anyone who needs it.
4. **Rules split.** `AGENTS.md` here mixes studio rules (the Ben gate, the Never list, sign-offs, who does what,
   the queue and the relay) with Orbit's own style rules (teach on screen, polish, packaging). The first set moves
   to the studio repo. Each channel keeps its own in `studio/RULES.md`. A channel can add a rule and can never
   remove a studio one.
5. **No copied tools.** `core_sync.py` and `studio-core/` keep 56 shared files identical in both channel repos.
   They retire when the engine has its own repo; a channel's CI checks out the studio repo instead.
6. **A check every channel passes.** `scripts/channel_check.py` reads a channel checkout and says whether the
   studio can drive it: `studio/channel.json` complete, the folder layout, the rules file. The same check runs in
   the channel's CI and before a channel is added to the registry.
7. **NAS folders by slug.** `studio-live/<slug>/`, not `studio-live/orbit-with-ben` and
   `studio-live/History Of Science`. The folder name goes in `studio/channel.json` meanwhile.
8. **The name is `studio` (Ben, 10 Nov 2026: "You can name it whatever you think's best. I'll let you handle on
   the naming front."). It will be private (Ben, 10 Nov 2026: "If you think private is best, let's do a private
   repo. ... as long as the .env files and all the keys and stuff are local on my machine, that's fine.").** Why
   private: the queue and the thread are how agents get their instructions, and nobody outside can post on a
   private repo. A slip in a report (an address, a list of devices) is also not published. A private repo can be
   opened later; a public one cannot be taken back. Ben's fallback stands: if the automatic checks cannot be kept
   inside the free monthly minutes, the repo is made public instead, and that is the Chief's call to bring to him
   with the numbers. Three things have to be true before a private repo works, and all three are jobs, not
   decisions:
   - **Check minutes.** A private repo has a monthly cap on free check minutes. Today the full suite runs on most
     queue commits (they touch `STATUS.md`), which would spend the cap in days. Queue-only commits must stop
     running it.
   - **The board reads public addresses.** The pages fetch `board.json` and the heartbeats straight from GitHub's
     public file addresses. In a private repo those answer nothing, so the site's own server has to read them
     (`api/ref.js` already does this for one small read). A page that reads private data must also ask who is
     looking: only a signed-in viewer (Ben's paired devices) gets the data, or the site would publish what the
     repo hides.
   - **Keys stay on the machines.** Checked on 10 Nov 2026: neither repo tracks a key, a token or a `.env` that
     holds a credential. History of Science tracks one `.env` with a cloud project name and a region and no key; it
     becomes an example file. The dry run fails if the tree it would move holds a key-shaped string or a `.env`
     that is not an example.
   The repo is not created until the dry run of the move (`scripts/studio_split.py`, J2524) has passed seven days in
   a row, and Ben is told the day before.

**Why it stalled, and how it finishes (10 Nov 2026).** Ben: "What else is blocking the development here? How can we
get this project moving and finished?" Nothing was blocked on a decision. None of the remaining work was in the job
queue, so it was done only by the cloud session between other things, while both MacBook slots sat idle. It is now
queued as jobs with ceilings that can only fall:

| Wave | What | Jobs |
|---|---|---|
| 1, now | Small scripts stop naming a channel (62 of 327 lines) and stop assuming the studio lives in one channel's repo (13 of 40) | J2521, J2522, J2523 (MacBook). In on 10 Nov: 327 to 285 and 40 to 27. What J2522 left is J2533 |
| 1, now | The dry run of the move, run daily: one number for what still stops it | J2524 (cloud) |
| 1, now | `video_tracker.py`, `macbook_worker.py`; the rule book split | J2525, J2526, J2527 (cloud) |
| 2, now | The four scripts that run the live studio, one change each: `board_publish.py`, `approved_deliver.py`, `kanban_snapshot.py`, `chief_relay.py` (203 lines) | Queued 11 Nov: J2615, J2616 (MacBook), J2617, J2618 (cloud). `board_publish.py` (J2615), `kanban_snapshot.py` (J2617) and `approved_deliver.py` (J2616) are in: 222 to 98. `chief_relay.py` (J2618) is written: its brief is put together from the channel files, and a channel's own desk is a `desk` field in its channel file. With it the first count is 0 |
| 2, now | The rest of the second count (`jobs.py`, `workflow_state.py`, `workflow_handoffs.py`, `studio.py`, `routing.py`); the studio's own name; no home channel and the 14 tests | J2619 is in (11 Nov): 20 to 5. J2620 (the studio's own name: `studio.prefix` in `channels/channels.json`, read with `channels.studio_prefix()`; the thread tool is `studio_thread.py`, with `owb_thread.py` kept as the same tool) takes the first count from 98 to 79, all of it `chief_relay.py`. J2621 is written (11 Nov): a home channel is optional. The registry alone says which channel, if any, lives in the studio's root; `channels.default()` is the registry's `studio.default_channel`; the relay, the MacBook worker and the board publisher ask the loader for the studio's own repo (`studio_repo()`, `studio_checkout()`, `studio_key()`) and treat every channel as one beside it when there is no home. The dry run now builds the new layout as a git repo with each channel's numbers in that channel's folder, and its `registry` and `tests` groups read 0. It rides on J2618's pull request and merges with it |
| 3 | History of Science to per-film status files; its own `studio/RULES.md` | The rule book is in (J2578, 11 Nov). Status files (J2622), in three steps so the board never breaks: (1) the studio learns to read a channel that keeps a status file per film exactly as it reads one pipeline file, with the channel's own stage weights, owners and kinds (written 11 Nov, changes nothing for either channel today); (2) History of Science's own pull request converts its one file into one per film, moves its stage list into its settings and stops committing its two built pages, reviewed and merged by Grok, not before Thu 12 Nov 19:13 London and not during a picture run; (3) the studio's cached copy of that channel's settings is refreshed |
| 3 | Ready for private (Ben said private on 10 Nov): check minutes, and the board reading through its own server | J2531, J2532 (queued 10 Nov) |
| 4 | A week in which the dry run passes every day, then the move in one planned window | Chief, with Ben told the day before |

The dry run replaces "a clean week" as a feeling with a number: the move happens after seven daily passes in a row.

**Two things the move itself still has to settle, found by J2621 (they do not count against the dry run):**

- The playbook and the Cursor rules copy go to the studio, and both quote the default channel's own
  `studio/RULES.md`. `sync_rules.py` finds that file through the loader, so it works wherever that channel is
  checked out. The studio repo's own check will not have a channel checked out: at the move either that check
  fetches the channel too, or those quoted sections move into a copy the channel owns.
- `STATUS.md` is built on every run and kept by nobody after the move, so `studio.py status --check` has nothing
  to compare in the studio repo. Its test is skipped there; the check itself goes at the move.

**Order of work:** finish phase 1 (both counts to zero) → the channel check and template → History of Science to
per-film status files → ready for private → seven daily passes of the dry run → the move (phase 3), one planned
window, old copies kept until a week of green.

The plan below is as written on 5 Nov.

## Where we are

- The engine lives inside `orbit-with-ben` under `scripts/`. It covers the job queue, the relay and Chief, the
  Mini and MacBook workers, the board, the review lane, refill and routing. The queue, WIP and backlog live in its
  `jobs/` folder.
- `history-of-science` carries a copy of the shared tools, kept identical by `core_sync.py` and the hash lock in
  `studio-core/`.
- About 16 engine scripts name a channel directly: `"OWB"`, `"HOS"`, `history-of-science`, `--repo {owb,hos}`, the
  WIP keys `next` and `next_hos`. The worst are `kanban_snapshot`, `video_tracker`, `capacity_caller`, `chief_relay`
  and `board_publish`.

  Because of this, a third channel today means editing all of those files, and a rule meant for one channel can
  leak into the other.

## Where we want to be

```
studio/                    NEW repo: the engine, and nothing about any one channel
  scripts/                 queue, relay, workers, board, review lane, refill, routing
  jobs/                    one studio-wide queue, WIP and backlog (the agents are shared, so the queue is too)
  channels.json            the registry: which channels are plugged in, and where their repos are
  AGENTS.md                studio-wide rules (Ben gate, never-list, sign-offs, who does what)

orbit-with-ben/            a channel repo: content, plus a studio/ folder
history-of-science/        the same shape
<third-channel>/           the same shape, made from a template in one command
  studio/channel.json      id, name, YouTube ids, repo, cadence (longs and Shorts a week, days, times),
                           WIP limit, folder layout, analytics paths
  studio/flow.json         this channel's stages and gates, in order, each with an optional command
                           (e.g. HOS: Flow Veo picture + gate_shorts_open; OWB: Studio stills + picture_qa)
  studio/RULES.md          this channel's extra rules for agents (title shapes, voice, picture, never-list additions)
  studio/backlog.json      this channel's recurring jobs (daily topics, Shorts from locked longs)
```

**Rule of the split:** the engine never says a channel's name. It reads `channels.json`, then each channel's
`studio/` folder. The channel decides **what** to make and **how its own stages run**. The engine decides **who
does it, when, and in what order**. Studio-wide rules always win over a channel's rules: a channel can add rules,
never remove one (no money, no deletes, Ben gate).

**Adding a channel then means:**
1. Run `python3 scripts/channel_new.py <slug>`. It makes the repo layout from the template, with `studio/` filled
   from questions.
2. Add one line to `channels.json`.
3. The board, WIP, refill and topic jobs pick it up on the next run.

Ben's only part is the YouTube sign-in and the voice, as now.

## Phases (each one ships on its own, with the studio running 24/7 throughout)

**1. Channel manifests, in place (no moves).**
- Add `channels/owb/` and `channels/hos/` with `channel.json`, `flow.json` and `backlog.json`, plus a small
  `scripts/channels.py` loader.
- Replace every hard-coded `OWB` and `HOS` in the 16 engine scripts with loader lookups:
  - `--repo` choices come from the registry;
  - WIP `next` / `next_hos` become `next: {owb: [...], hos: [...]}`;
  - board columns are made per channel.
- Add a test that fails if an engine script names a channel.
- Risk is low: the same repo and the same paths, so the Mini and MacBook change nothing.

**2. Manifests move into the channel repos.**
- `channels/owb/` becomes `orbit-with-ben/studio/`, and `channels/hos/` becomes `history-of-science/studio/`.
- The loader reads them from the checkouts named in `channels.json` (the Mini has both already).
- Each channel's `AGENTS.md` points at its `studio/RULES.md`.

**3. The engine moves to its own repo.**
- Create `studio` (private, free). Copy `scripts/` (engine files), `jobs/` and the board site with their history
  (`git filter-repo`).
- Leave a forwarding shim in `orbit-with-ben/scripts/` for a fortnight, so old launchd jobs and agents still work.
- Cut-over in one window, done by the Mini session:
  - point launchd at the new checkout;
  - re-point the Vercel board's root directory;
  - point the hourly cloud run at the new repo.
- The old copies stay untouched until a week of green, so this can be undone at every step. Nothing is deleted:
  old files move to `_archive/`.

**4. Plug-in ready.**
- Retire `core_sync.py` and the `studio-core/` copies (channels no longer carry engine code).
- Ship `channel_new.py` and the channel template.
- Write the third-channel checklist.

## What stays the same

- One queue and one board across channels. Agents are shared, and the per-channel WIP limits (rule G) keep one
  channel from starving another.
- Jobs keep their `repo` field. It is now any registered channel slug.
- Ben's three calls: watching finished cuts, real money, his own login, voice and device.

## Open questions for review

1. One queue for all channels, or one per channel? The plan says one, because the agents and credits are shared.
2. Should `flow.json` gate commands run inside the channel checkout (the plan says yes), and how is a channel's
   tool trusted? It's our own repos, but CI should lint `flow.json`.
3. Phase 3 history copy: filter-repo with history, or a fresh repo with a pointer commit? The plan says history.
4. Anything the Mini launchd and the MacBook worker need beyond a path change.
