# J2829 — Worker Media-Capability Probe Results & Chief Proposal

**Date:** 2026-11-14 (`15:18Z–15:31Z`)
**Worker:** `macbook`
**Job:** `J2829`

---

## 1. Live Probe Measurements Across All Four Worker CLIs

All four worker CLIs in `routing.MINI_WORKERS` now have runners in `scripts/capability_probe.py` (`RUNNERS = {"gemini", "cursor", "codex", "claudecode"}`) and were probed live on freshly generated `say` speech clips (`clip_a.wav`) and `ffmpeg` 6-second moving-colour-square clips (`clip_v.mp4`) with shell/command execution forbidden (`FILE_TOOLS` only):

| Worker | CLI & Version | Audio Probe (`audio_input`) | Moving Video Probe (`moving_video_input`) |
|---|---|---|---|
| `gemini` | `agy 1.5.9` | **PASS** (`match 1.00`) — spoken: `'The gentle teapot borrowed seven kettles beside the silver glacier.'`; heard: `'The gentle teapot borrowed seven kettles beside the silver glacier.'` | **FAIL** — clip truth: `right_to_left` `red>blue>green`; worker answer: `watched=false`, `direction=none`, `colours_in_order=[]` |
| `cursor` | `agent 2026.11.13-eacade1` (`--model grok-4.7`; `cursor-auto` & `cursor-claude-opus-5-5` flagged out until `2026-12-09`) | **FAIL** (`match 0.00`) — spoken: `'The crooked teapot painted three orchards beside the crooked bakery.'`; heard: `''` (`heard=false`) | **FAIL** — clip truth: `right_to_left` `green>yellow>red`; worker answer: `watched=false`, `direction=none`, `colours_in_order=[]` |
| `claudecode` | `claude 2.1.318 (Claude Code)` (`--restricted --tools Read`) | **FAIL** (`match 0.00`) — spoken: `'The frozen orchard borrowed forty ladders beside the violet glacier.'`; heard: `''` (`heard=false`) | **FAIL** — clip truth: `right_to_left` `green>red>yellow`; worker answer: `watched=false`, `direction=none`, `colours_in_order=[]` |
| `codex` | `codex-cli 0.165.0` (`exec -s read-only`) | **FAIL** (`match 0.00`) — spoken: `'The frozen pebble followed seven lanterns beside the gentle lighthouse.'`; heard: `''` (CLI error: `You’ve hit your usage limit. ... try again at Nov 17th, 2026 11:22 PM.`) | **FAIL** — clip truth: `left_to_right` `blue>yellow>green`; worker answer: `None` (same usage-limit error until `Nov 17th, 2026 11:22 PM`) |

**Measured conclusion:**
- `audio_input` is **PASS** on `gemini` (`agy 1.5.9`).
- `moving_video_input` is **FAIL** on every installed worker CLI.

---

## 2. One Chief Ruling Proposed Today: Non-`moving_video_input` Review Standard

Because no worker CLI can natively watch moving `.mp4` files, keeping `required_capabilities: ["moving_video_input"]` on assembled-edit QA/review jobs leaves finished films blocked indefinitely ahead of Ben's UAT watch.

### Proposed Review Specification (at least as strict as `J2222` Journey + `J2614` Franklin splice + verified `audio_input`)

For assembled long and Short masters, replace `required_capabilities: ["moving_video_input"]` with `required_capabilities: ["audio_input"]` and require all five checks in the written review artefact before arming Ben's watch card:

1. **Automated gates PASS** on the exact master file(s):
   - **Longs:** `picture_qa`, `polish_gate`, `music_gate`, and `clip_check.py` (VO word ends vs shot cuts).
   - **Shorts:** `gate_shorts_open.py check <short.mp4> --air-date YYYY-MM-DD` (opening hook, safe zones, no padded-frame violation), `picture_qa`, and `polish_gate`.
2. **Half-second full-film frame grid (`0.5 s` interval, `2 fps`)** across the entire runtime with burned-in timestamps, inspected sheet by sheet for freezes, black/flash frames, aspect/letterbox bars, wrong celestial body/plate, text/card rendering faults, and character consistency.
3. **Every frame at every cut (`±3` frames across each cut boundary) AND every frame of the final `3.0 s`** (matching `J2614`'s frame-by-frame splice strip and covering `J2658`'s Supermoon ending tail), catching 1–2 frame flashes, mid-transition pops, and end-hold defects.
4. **Complete soundtrack heard end to end via verified `audio_input` (`gemini`)**, verifying narration clarity/pronunciation against the locked script, music/SFX ducking, clicks/pops, and clean tail fade.
5. **Ben's UAT watch** (`AGENTS.md` check-in rule: Ben watches every finished long and Short before scheduling/publish) remains the final human moving-picture sign-off.

### Immediate Dispatch Order for the Five Stuck Orbit Reviews (`for=gemini`, `required_capabilities=["audio_input"]`)

1. **`J2658`** — *Supermoon v04 ending check* (airs Thu 19 Nov; `J2478` waits on it; due before Mon 16 Nov) — est. ~10 min.
2. **`J2477`** — *032 Titan long master v02 review* (due `2026-11-14T18:00:00Z`) — est. ~20 min.
3. **`J2383`** — *034 Pluto long master v01 + Shorts 1 & 2 review* (waiting 6 days since 8 Nov) — est. ~25 min.
4. **`J2400`** — *033 Uranus Shorts 1 & 2 review* (waiting 6 days since 8 Nov) — est. ~15 min.
5. **`J2404`** — *033 Uranus long master v01 review* (waiting 6 days since 8 Nov) — est. ~20 min.

### Scope Ruling Across the Other Seven `moving_video_input` Jobs

| Job(s) | Channel & Type | Covered by this Ruling? | Action if Approved |
|---|---|---|---|
| `J2243` | HOS 008 Franklin master v04 QA & Chief review (`repo=hos`, `for=gemini`, waiting on `J2614` / `J2242`) | **Yes — Covered** | Apply the same gates + `0.5 s` grid + cut/tail frames + `audio_input` listen (`required_capabilities: ["audio_input"]`); HOS Chief (`grok` first on desk `#180`) rules on the HOS review. |
| `J2550` | OWB Three November Shorts padded-shot recuts (Voyager 17 Nov, Muons 21 Nov, ISS 25 Nov; `kind=assembly`) | **Yes — Covered** | Set `required_capabilities: ["audio_input"]`; verify each recut Short with `gate_shorts_open` + `0.5 s` grid + cut/last-3s frames + `audio_input` listen before arming `awaits_ben` watch cards. |
| `J2551` + `J2661` | OWB Four December Shorts padded-shot recuts (`J2551` blocked on capability hold; `J2661` is its `recheck_of` stub) | **Yes — Covered** | Reopen `J2551` with `required_capabilities: ["audio_input"]` under the same Short recut check and cancel synthetic recheck `J2661`. |
| `J0912` | HOS Backlog search-titled Short (`repo=hos`, `4/4` assembled, `hold.type=ben` for `HOS:ASK:J2699`) | **Already at Ben's UAT watch** | Keep `J0912` on its existing `ben` hold (`HOS:ASK:J2699` Short A v04); future runs of this backlog item use the same Short review standard. |
| `J2271` + `J2758` | HOS 010 independent review of twelve raw Veo Shorts plates (`repo=hos`, `for=codex`; `J2758` is its `recheck_of` stub) | **No — Separate HOS Chief call (`#180`)** | Raw Veo plates are silent (`0` audio streams) and are checked for native motion/morphing/anatomy before `KEEP`, not assembled over locked VO. HOS Chief on `#180` should rule separately whether dense `4 fps` frame strips + optical-flow/frame-diff checks satisfy `J2271` (and reroute off `codex`, which is out of quota until 17 Nov). |

---

## 3. Closing the 24-Hour Capability Trap (Code Change)

- **Where the check belongs:** **`scripts/refill.py` (`park_unshown_capabilities`, invoked inside `do_escalate` / `chief_relay.escalate_stale` right after `refresh_probes`)**, **not** `chief_relay.capped_runs_in_a_row` ("the stuck sweep").
  - *Why:* `capped_runs_in_a_row` only inspects a job *after* `select_dispatch()` picks it and a worker hits the 25-minute cap (`exit 124`). A job whose `required_capabilities` fail `workflow.capability_problem()` is never picked by `select_dispatch()` and never logs a run, so a post-dispatch stuck-runs check would never see it.
  - *How it works:* `chief_relay.record_capabilities` now persists `last_shown` per capability, `chief_relay.run_locked` runs `refresh_probes(at)` before `escalate_stale()`, and `refill.park_unshown_capabilities` parks any job whose required capability has not been demonstrated by any worker in 24 hours (once the job itself has waited 24 hours after creation / reopen / prerequisite completion), cancelling any open `recheck_of` capability stub and marking `capability_escalated` so `workflow_state.select_dispatch` and `chief_relay.pending_chief_reviews` deliver it to the Chief's inbox instead of filtering the Chief out on the same missing capability.

---

## 4. Codex Silence Check (`10:15Z` Onwards)

- **Confirmed still silent / out of quota:** Live invocation of `codex-cli 0.165.0` at `15:27Z` and `15:30Z` returned exit `1`:
  `You’ve hit your usage limit. Visit https://chatgpt.com/settings/usage to purchase more credits or try again at Nov 17th, 2026 11:22 PM.`
- **Impact:** `J2797`, `J2798`, and `J2532` (`for=codex`) remain waiting, and `scripts/credit_flags.json` does not yet have a `codex` entry until `2026-11-17T23:22:00Z`.
- **Recommended Chief action:** Record `codex` in `scripts/credit_flags.json` (`out_until: "2026-11-17T23:22:00Z"`) so the relay stops retrying Codex hourly, and reroute `J2797`, `J2798`, and `J2532` to `cursor` (`grok-4.7`) / `gemini`.
