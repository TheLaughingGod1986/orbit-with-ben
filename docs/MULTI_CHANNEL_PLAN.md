# Multi-channel studio: plan (5 Nov 2026)

Ben, 5 Nov 2026: "decouple the studio workflow system from the individual channel repos ... so we just plug in new
channels ... each channel can have a slightly different rule set, slightly different flow that can be stored in the
actual channel repo itself." A third channel is coming once the current two run smoothly.

Status: **draft for team review** (Codex for the code plan, Gemini for the risk). Nothing has moved yet.

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
