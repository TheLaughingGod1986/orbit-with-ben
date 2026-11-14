# J2829 — Acting Chief Ruling (14 Nov 2026)

**Date:** 2026-11-14T20:16:00Z  
**Acting Chief:** `gemini` (`chief_relay.py status` elected Chief for both OWB and HOS; `claude`, `chief`/`grok`, and `codex` all marked down)  
**Job:** `J2829`  
**PR:** `#928` (`macbook/J2829`)

---

## 1. Root-Cause Findings from Chief Verification

1. **Bug in `scripts/capability_probe.py` (`make_video` drew off-screen black frames):**
   - `make_video()` previously used `drawbox=x='20+t*90':y=140:w=80:h=80:color=...:t=fill:enable='...'`.
   - In `ffmpeg`'s `drawbox` filter, `t` in coordinate expressions is **box thickness** (`t=fill` sets `t=360`), **not** frame timestamp in seconds (`t` is only timestamp inside timeline `enable` expressions). Thus `x='20+t*90'` evaluated to `x=32420` on a `640x360` canvas, producing a **100% solid black video (`YMAX=16, SATMAX=0`)** on every probe since 5 Nov.
   - Replacing `drawbox` with `overlay` of `80x80` lavfi colour sources (`overlay=x='20+t*90':y=140:enable='...'`, where `overlay` evaluates `t` as frame time in seconds) fixes `make_video()`.
   - **Live probe result with fixed `make_video()` on `gemini` (`agy 1.5.9`):**
     - `audio_input`: **PASS** (`match 0.93` — spoken `'The crooked button buried forty harbours beside the violet bakery.'`; heard `'The crooked button buried forty harbors beside the violet bridge.'`)
     - `moving_video_input`: **PASS** (`truth left_to_right red>yellow>blue`; `answer left_to_right red>yellow>blue`; file tools only)
     - Recorded via `chief_relay.py capabilities --agent gemini --available 'audio_input,moving_video_input'`.
   - `cursor` (`agent 2026.11.13-eacade1`), `claudecode` (`claude 2.1.318`), and `codex` (`codex-cli 0.165.0`, also out of quota until `2026-11-17T23:22Z`) still have no native audio or moving-video file viewer (`FAIL` on both).

2. **Empirical Payload Limit on Full-Resolution Master `.mp4` Files in `agy`:**
   - While `agy 1.5.9` natively perceives `.wav`/`.mp3` audio and compact `640x360` `.mp4` clips via `read_file`, calling `read_file` directly on a full-resolution production export (`43 MB` `owb_dated_2026_11_24_supermoon_v04.mp4` or `372 MB` `032` Titan master v02) exceeds the single-call multimodal payload limit (`Error: model output error`).
   - Therefore, even with `gemini` passing the 6-second `moving_video_input` probe, full-film and Short reviews **must not** call `read_file` on raw `>10 MB` master `.mp4` files, and jobs must not sit blocked if `moving_video_input` lease expires between runs.

---

## 2. Chief Ruling

1. **Merge PR #928 (with the `make_video` `overlay` fix and non-black pixel regression test):**
   - Ships `RUNNERS` for all four Mini workers (`gemini`, `cursor`, `codex`, `claudecode`) in `scripts/capability_probe.py`.
   - Ships the `make_video()` `overlay` fix + `test_make_video_draws_visible_coloured_square` (`SATMAX > 0`).
   - Ships the 24-hour unshown-capability escalation (`park_unshown_capabilities` inside `scripts/refill.py` `do_escalate`, `last_shown` tracking in `scripts/chief_relay.py`, and Chief delivery bypass in `scripts/workflow_state.py`).

2. **Approve the Strict Combined Review Standard & Re-scope All Waiting Reviews:**
   - Every assembled long and Short review (`J2658`, `J2477`, `J2383`, `J2400`, `J2404`, `J2243`, `J2550`, `J2551`) is re-scoped to `required_capabilities: ["audio_input"]` and must verify all five gates in its written review artefact before arming Ben's UAT watch card:
     1. **Automated gates PASS** on the exact master (`picture_qa`, `polish_gate`, `music_gate`, `clip_check` for longs; `gate_shorts_open.py`, `picture_qa`, `polish_gate` for Shorts).
     2. **Full-film `0.5 s` (`2 fps`) contact-sheet grid** with burned-in timestamps inspected across the full runtime.
     3. **Every frame at every cut (`±3` frames) AND every frame of the final `3.0 s`** (`J2614` splice-strip standard).
     4. **Complete soundtrack heard via verified `audio_input` (`gemini`)** on extracted `.wav`/`.mp3` audio when the `.mp4` exceeds `10 MB`.
     5. **Compact `640x360` `.mp4` proxy clips (`<= 5 MB` per clip, e.g. the 3-second tail clip for `J2658`)** opened via `read_file` when running on `gemini` — never passing a raw `>10 MB` master `.mp4` to `read_file`. Ben's own UAT watch remains the final check before scheduling/publish.
   - **Queue priority & order for the 5 Orbit reviews (`for=gemini`):**
     1. `J2658` (*Supermoon v04 ending check*, urgent `10`, due `2026-11-15T12:00:00Z` ahead of Mon 16 Nov / Thu 19 Nov air date)
     2. `J2477` (*032 Titan long master v02 review*, urgent `9`)
     3. `J2383` (*034 Pluto long master v01 + Shorts 1 & 2 review*, urgent `8`)
     4. `J2400` (*033 Uranus Shorts 1 & 2 review*, urgent `8`)
     5. `J2404` (*033 Uranus long master v01 review*, urgent `8`)
   - **Ruling on the other 7 `moving_video_input` jobs:**
     - `J2243` (HOS 008 Franklin master v04 review, waiting on `J2614`): re-scoped to `required_capabilities: ["audio_input"]` under the same 5-part standard.
     - `J2550` (OWB Three November Shorts padded-shot recuts): re-scoped to `required_capabilities: ["audio_input"]` under the same Short recut check.
     - `J2551` + `J2661` (OWB Four December Shorts padded-shot recuts): `J2551` reopened with `required_capabilities: ["audio_input"]`; synthetic recheck stub `J2661` cancelled.
     - `J0912` (HOS backlog search-titled Short): remains on its existing `ben` UAT hold (`HOS:ASK:J2699`); `required_capabilities` updated to `["audio_input"]` for future backlog cycles.
     - `J2271` + `J2758` (HOS 010 twelve silent raw Veo Shorts plates, `0` audio streams): reopened and rerouted from `codex` (out of quota until `2026-11-17T23:22Z`) to `gemini` with `required_capabilities: []` (verified via dense `4 fps` frame strips + compact `640x360` `<= 5 MB` proxy clips on `gemini`), and synthetic recheck stub `J2758` cancelled.

3. **Codex Quota Flag (`until 2026-11-17T23:22:00Z`) & Waiting Codex Board Jobs:**
   - Record `codex` in `scripts/credit_flags.json` (`out_until: "2026-11-17T23:22:00Z"`) and mark `chief_relay.py down codex --until 2026-11-17T23:22:00Z` so the relay does not waste hourly probes/dispatches on Codex before its reset.
   - Reroute open board job `J2532` from `codex` to `cursor` (`grok-4.7`) so it does not sit blocked behind Codex's quota reset.
