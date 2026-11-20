# Recursive Self-Improvement (RSI) Loop

*Established 20 Nov 2026 (Ben: "like RSI ... recursive self improvement" & "bring a RSI system to all channels we manage"; J3257).*

The studio improves both its **films** (per registered channel) and its **own operations** (studio-wide) every week, with every change measured against a declared bar and wired directly into the templates, rules, and checks agents actually run.

## Registry-driven across every channel

Nothing in the loop is written per channel. `scripts/channels.py` is the single source of truth:
- Every channel in `channels/channels.json` automatically receives:
  1. Experiment tracking in `05_Analytics/EXPERIMENTS.json` (max **3 live experiments per channel** at once).
  2. Automatic ingestion of `05_Analytics/<slug>/autopsy/<video_id>_<48h|7d>.md` fixes into candidate hypotheses (`scripts/rsi.py ingest-autopsies`).
  3. Its own weekly improvement cycle backlog item (`weekly-improvement-<slug>`, `every_h: 168`) generated automatically by `scripts/refill.py` (replaces the old `monthly-improvement-*` items).
  4. Its own row in the dashboard's **What the studio is learning** card (`board.learning`).
- A brand-new channel waits quietly until its analytics sign-in and first 48-hour read land (`rsi.channel_cycle_ready(slug)`), then its weekly cycle starts automatically with no code change.
- Rules and generator updates land in each channel's own repository (`channels.checkout(slug)`), **one PR per repo per cycle**, with a changelog line per change.

## The closed loop

1. **Experiment register (`05_Analytics/EXPERIMENTS.json`):**
   - Managed and validated by `python3 scripts/rsi.py validate`.
   - Every entry declares: `id`, `channel`, `status` (`candidate` / `running` / `decided` / `dropped`), `result` (`pending` / `pass` / `fail` / `inconclusive`), `hypothesis`, `change`, `applies_to`, `metric`, `expected_effect`, `min_sample`, `readout_date`, `evidence`, `revert_plan`.
   - At most **3 running experiments per channel** at once so effects remain attributable.
2. **Autopsy → Hypothesis (`scripts/rsi.py ingest-autopsies`):**
   - Each J3256 retention autopsy (`05_Analytics/<slug>/autopsy/<video_id>_<48h|7d>.md`) converts its concrete fixes into deduplicated candidate experiments:
     - **Live-video packaging fix** (`this video` / `packaging`): uses Studio Test & Compare (`test_type: "test_and_compare"`).
     - **Next-film production fix** (`next film` / `production`): applies to the next `N` films (`test_type: "next_n_films"`).
3. **Weekly improvement cycle (`weekly-improvement-<slug>`, `every_h: 168`):**
   - Runs `python3 scripts/rsi.py ingest-autopsies --channel <slug> --apply` and `python3 scripts/rsi.py cycle --channel <slug>`.
   - Reads every readout due:
     - **PASS** (requires `sample_observed >= min_sample` + evidence + revert plan): promote to `05_Analytics/LEARNINGS.md`, the channel's `studio/RULES.md` and playbook, **and update the generators agents actually use** (script templates, title shapes and scorer, thumbnail checks, picture-plan templates, prompts).
     - **FAIL**: revert the change and record why in `EXPERIMENTS.json`.
     - **INCONCLUSIVE**: extend `readout_date` once (+14 days); if still inconclusive on the second readout, drop it.
   - Promote top guardrailed candidates up to the 3-live cap (`scripts/rsi.py start`).
   - Open **one PR per repo per cycle** for the Chief, with one changelog line per change.
4. **Weekly Studio Ops Loop (`studio-ops-loop`, `every_h: 168`, `scripts/ops_loop.py`):**
   - Measures 6 studio-wide operational metrics over the trailing 7 days:
     1. Jobs done per day per machine
     2. Idle agent-hours with ready work
     3. Stall and park counts
     4. Chief FIX rate
     5. Median time from first film job to Ben-watch
     6. Credit spend per finished film
   - Names the **single biggest bottleneck**, queues one deduplicated £0 fix job, and re-measures the following week against `05_Analytics/ops_loop/history.jsonl` to prove whether the fix helped.
5. **Dashboard (`What the studio is learning` card & `#learning` page):**
   - Built by `scripts/board_publish.py` (`board["learning"]`) and rendered on Overview by `studio_app.js`.
   - Shows running experiments with readout dates per channel, last week's kept/reverted results, and the ops bottleneck of the week in plain words.

## Guardrails (enforced in code and review)

- The loop **never** changes:
  - Ben's gates (final UAT watch, live retitles, direct TikTok pause, overriding failed checks)
  - The Never list (`AGENTS.md` / `studio/RULES.md`)
  - Money, billing, credit top-ups, or paid overage
  - A channel's direction (e.g. Rule 34 item 7 for HOS, Ben's strategic plans in `studio/plan.json`)
  Any candidate touching these is flagged `needs_ben` and escalated to Ben in one line instead of starting or promoting.
- Every rule change carries its **evidence** and a **revert plan** (`revert_plan`).
- No rule promotes on fewer than the **`min_sample`** declared by the experiment (`scripts/rsi.py record` and `validate` both reject premature PASSes).
