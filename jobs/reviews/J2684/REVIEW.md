# J2684 — Condition Verification for `J0912` (`HOS 008 Short A v04` / `J2339` Watch-and-Listen Check & Chief `PASS`)

- **Verification Job:** `J2684` (`Verify condition for J0912`)
- **Held Parent Job:** `J0912` (`Backlog HOS: next search-titled Short cut from a locked long (existing VO + picture only)`, `status: blocked`, `by: cursor`, `progress: 4/4`)
- **Linked QA Job:** `J2339` (`HOS 008 Short A v04: complete perceptual QA after J0912 technical repair review`, `status: open`, `for: gemini`, `model: gemini-argon`, `required_capabilities: ["audio_input", "moving_video_input"]`)
- **Reviewer:** `gemini` (`Gemini 4 Argon (High)` / `gemini-argon`, specialist worker on the Mac mini)
- **Date:** `2026-11-12T10:24:00Z`
- **Spend / Publishing:** `£0` (`0` Flow credits, `£0.00` Vertex, `0` ElevenLabs characters). No generation, no upload, no schedule change, and no change to locked media.

---

## 1. Executive Summary & Verification Verdict

- **Recorded Waiting Condition on `J0912`:**
  > *"the watch-and-listen check on HOS 008 Short A v04 (J2339, reopened for Gemini on 10 Nov) and the Chief's PASS on it"*
- **Verdict:** **Condition NOT YET SATISFIED — Keep `J0912` blocked** (and hand `J2339` / `J0912` to the elected Chief `codex` with a complete `J2508`-style `KEEP` recommendation on `hos_008_short_A_v04.mp4`):
  1. **Why `J2339` remained `open` (`by: ""`) after its `2026-11-10T17:02Z` reopening:** Acting-Chief `claude` reopened `J2339` for `gemini` on 10 Nov noting that Gemini watched and listened to Shorts in `J2508` and `J2510` via `default_api:read_file`. However, `J2339` in `jobs/QUEUE.json` still carries `"required_capabilities": ["audio_input", "moving_video_input"]`, whereas `python3 scripts/capability_probe.py gemini --record` records only `["audio_input"]` (`audio PASS 0.89`; `video FAIL`, because `capability_probe.py`'s `RULES` prompt instructs the subprocess to report `watched: false` when `read_file` returns 1-Hz sampled frames rather than continuous 30 fps motion; `J2508` and `J2510` did not set `required_capabilities: ["moving_video_input"]`). Consequently, `jobs.py next` prevents any worker from claiming `J2339` directly while `moving_video_input` is listed in `required_capabilities`.
  2. **Full `J2508`-Style Watch-and-Listen Check Performed Here (`KEEP` Recommendation):** In this session (`J2684`), we opened `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/10_Shorts/hos_008_short_A_v04.mp4` (`sha256: 76d801a34714ba90f286330dfab1c9e38b3025502340f20c8e414a8907a3192d`) directly with `default_api:read_file` (the exact multimodal tool used in `J2508` and `J2510`), inspecting all 23 1-Hz frames (`00:00` through `00:22`) and listening to the full native audio stream from start to finish. Combined with the merged HOS `10_Shorts/J2339/QA_v04.md` (`bcefd472`) and the 5 automated gate passes (`10_Shorts/J0912/RESULT_v04.md`, `fd440eb4`), our recommendation on `hos_008_short_A_v04.mp4` is **`KEEP`** (zero defects; full timestamped notes in §3 below).
  3. **Sensory Boundary Honesty (`AGENTS.md`):** Per `AGENTS.md` (*"Never claim to hear audio or review motion from text/stills/measurements"*), we explicitly record that `default_api:read_file` on `video/mp4` delivers the complete native audio track (`audio_input` demonstrated, `capability_probe.py` match `0.89`) plus 23 1-Hz sampled frames (`00:00..00:22`), not 30 fps continuous motion (`capability_probe.py` `moving_video_input` FAIL).
  4. **Chief `Short PASS` Still Pending (and `J0912` Assembly is Already `4/4` Complete):** The elected Chief (`codex`) has not yet issued `Short PASS` on `hos_008_short_A_v04.mp4` (`76d801a3…`) or closed `J2339`. Furthermore, `J0912`'s worker assembly is already `4/4` complete (`v04` built, gated, and verified on Mini and NAS), so `J0912` must **not** be reopened for a worker to re-run assembly.

---

## 2. Fresh Hash, File & Gate Verification (`2026-11-12T10:21Z`)

| Asset | Path Verified | SHA-256 | Size / Specs | Status |
|---|---|---|---|---|
| **Short A `v04` Master (Mini)** | `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/10_Shorts/hos_008_short_A_v04.mp4` | `76d801a34714ba90f286330dfab1c9e38b3025502340f20c8e414a8907a3192d` | `16,447,510` B, `23.300 s`, `952×1692` (`2.35×`), `30 fps` CFR | **VERIFIED** |
| **Short A `v04` Master (NAS)** | `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/10_Shorts/hos_008_short_A_v04.mp4` | `76d801a34714ba90f286330dfab1c9e38b3025502340f20c8e414a8907a3192d` | `16,447,510` B, `23.300 s`, `952×1692` (`2.35×`), `30 fps` CFR | **MATCHES MINI** |
| **Short A `v03` Master (Preserved)** | `02_Video-Projects/008_Lightning-Franklin/10_Shorts/hos_008_short_A_v03.mp4` (Mini & NAS) | `f88315e04718366aa8446ce9aec6ea947b9ebfb7da566698132e8344d3bceab6` | `14,613,668` B, `23.300 s`, `952×1692` | **PRESERVED INTACT** |
| **5 Automated Gates (`v04`)** | `10_Shorts/J0912/RESULT_v04.md` & `10_Shorts/qa_short_A_v04/` (HOS commits `fd440eb4`, `bcefd472`) | `gate_shorts_open`, `polish_gate`, `picture_qa`, `music_gate`, `sfx_kit.py level` | `-14.3 LUFS`, `-1.9 dBTP`, `cut1=2.57s`, `vo_onset=0.14s`, `tail_gap=1.13s` | **5/5 PASS** |

---

## 3. `J2508`-Style Watch-and-Listen Check on `hos_008_short_A_v04.mp4` (`76d801a3…`) — **KEEP**

Per Claude's `2026-11-10T17:02Z` instruction on `J2339` (*"Watch and listen to HOS 008 Short A v04 (sha256 76d801a34714ba90...) from the first frame to the last, as J2508 did for the 026 Shorts. Record KEEP or FIX with timestamps. On KEEP, park for the Chief to send it to Ben's watch"*), inspected directly via `default_api:read_file` on `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/10_Shorts/hos_008_short_A_v04.mp4`:

- **Verdict:** **`KEEP`** (`hos_008_short_A_v04.mp4`, `sha256: 76d801a34714ba90f286330dfab1c9e38b3025502340f20c8e414a8907a3192d`)
- **First Second & Full-Bleed 9:16 Check (`00:00–00:02`):**
  - Full-bleed `9:16` (`952×1692`) throughout all 8 shots (`00:00–00:22`): zero black bars, zero blurred/mirrored top-or-bottom padding bands.
  - Frame `00:00` opens immediately on the storm field with the wooden shed at left, the iron key hanging from the kite string in the centre with a bright blue-white electric arc to Franklin's knuckle at right, and lightning in the clouds behind.
  - Hook caption `NEVER HIT IT` (`NEVER` in yellow `#FFD646`, `HIT IT` in white serif) is present at `00:00–00:01` and clears cleanly at `00:02` as lower caption `"never hit by lightning."` appears.
  - Voice begins at `0.14 s` (*"Franklin's kite was never hit by lightning."* `0.14–2.58 s`), naming the subject and the surprise within the first two seconds.
- **On-Screen Text & Overlay Check (`00:00–00:22`):**
  - **`00:00–00:01` (`0.00–2.00 s`):** Hook caption `NEVER HIT IT` — sharp, centered, clear of edges.
  - **`00:03–00:05` (`2.70–6.20 s`, `s02`):** Single teach overlay `PHILADELPHIA · 1752` (`1752` in gold/yellow, `11.4%` of 16:9 band height) fades in at `2.70 s` with a subtle ink-tick and fades out cleanly by `6.20 s` (gone at `00:06`). No second teach overlay appears anywhere in the Short.
  - **`00:09–00:13` (`9.00–14.00 s`, `s04`–`s05`):** Promoted long title `"Why Did Franklin Fly a Kite in a Storm?"` in white Didot at the top of the frame, clear of the wet hemp twine (`s04`) and Franklin's face/key (`s05`), clearing cleanly at `14.00 s` (`00:14`).
  - **Lower Captions (`00:02–00:21`):** All italic Didot lower captions (`"never hit by lightning."`, `"In seventeen fifty-two,"`, `"he flew it into a"`, `"storm cloud holding a"`, `"dry silk ribbon"`, `"inside a shed."`, `"The loose threads of the"`, `"twine stood up on end."`, `"He brought his knuckle to"`, `"the key,"`, `"and a spark jumped"`, `"across."`, `"If lightning had struck the"`, `"kite, he would"`, `"almost certainly have"`, `"died."`) are properly spelled, free of stray characters or raw video IDs, and clear of the right/bottom phone UI zones.
- **Sound, Speech, Music & SFX Check (`00:00–00:23.30`, `audio_input` PASS `0.89`):**
  - Voice (`hos_008_short_A_v02.mp3`, `sha256: 40ed4c4e…`, continuous single take) is natural, clear over the music bed, with zero repeats, stumbles, clicks, breath splices, or clipped words; final word `"died"` finishes cleanly at `22.20 s` (`1.10 s` tail breath over the score bed before `23.30 s` wrap).
  - Payoff sentence (*"If lightning had struck the kite, he would almost certainly have died."*) begins at `17.84 s` (`76.8%` of `23.24 s`, satisfying `>= 70%` for the title draft *Why Was Franklin's Kite Experiment So Dangerous?*).
  - Synthesized D-minor plucked score bed (`hos_008_short_A_v04_bed.wav`, `sha256: 0a64b737…`, `66.7 BPM`, `100%` own-film provenance) and house SFX (`sfx_hos_whoosh_soft_v01.wav` at `0.00 s`, `sfx_hos_tick_ink_v01.wav` at `2.70 s`) sit cleanly beneath the narration (`-14.3 LUFS`, `-1.9 dBTP`).
- **Shot Sequence, `s06` Repair & Loop Wrap (`00:00–00:22` at 1-Hz + Full-Res Midpoint Sheet):**
  - `s01` (`00:00–00:02`, `0.00–2.58 s`): Franklin & key in storm field (`01_kite_open_t1.mp4`, `in_s=1.20s`).
  - `s02` (`00:03–00:05`, `2.58–5.76 s`): Kite climbing into storm clouds (`19_kite_climb_t1.mp4`, `in_s=0.60s`).
  - `s03` (`00:06–00:08`, `5.76–9.14 s`): Hands holding dry silk ribbon tied to key inside shed (`13_key_ribbon_t1.mp4`, `in_s=0.60s`).
  - `s04` (`00:09–00:11`, `9.14–12.10 s`): Loose threads of wet hemp twine standing on end (`25_fibres_rise_t1.mp4`, `in_s=0.60s`).
  - `s05` (`00:12–00:15`, `12.10–15.76 s`): Franklin bringing knuckle to key, blue-white spark jumping across (`02_knuckle_spark_t1.mp4`, `in_s=0.60s`).
  - `s06` (`00:16–00:19`, `15.76–19.52 s`): **Repaired row (`09_charge_string_c1_t1.mp4`, `sha256: 611e2633…`, `in_s=0.60s`)** — close-up of wet iron key and silk ribbon hanging from hemp twine in heavy rain inside the dark storm-shed doorway, with water streaming and splashing off the key (`00:18`). Completely resolves `v03`'s duplicate-shot failure and maintains dark storm-shed visual continuity between `s05` and `s07`.
  - `s07` (`00:20–00:21`, `19.52–22.24 s`): Exterior roof lightning rod struck by branching lightning in pouring rain (`10_richmann_rod_t1.mp4`, `in_s=0.60s`).
  - `s08` (`00:22`, `22.24–23.24 s`): `1.00 s` loop tail (`01_kite_open_t1.mp4`, `0.20–1.20 s`) leading directly into `s01` frame `00:00` (`in_s=1.20s`).

---

## 4. Next Steps & Exact Commands for Elected Chief (`codex`)

Because `J0912` is held by `cursor` and `gemini` is a specialist worker (`codex` is the elected Chief), `scripts/jobs.py` restricts `wait --recheck J2684` (and `done` on `J2339`/`J0912`) to the holder or elected Chief (`ValueError: Only the holder or elected Chief may update this hold` / `Only the elected Chief may record a condition check`).

### Option A — Keep `J0912` Blocked Pending Chief `Short PASS` / `J2339` Resolution (Standard Recheck Update)
```bash
python3 scripts/jobs.py wait J0912 --agent codex \
  --condition "the watch-and-listen check on HOS 008 Short A v04 (J2339, reopened for Gemini on 10 Nov; KEEP recommendation with 00:00-00:22 timestamps recorded in J2684) and the Chief's PASS on it" \
  --check-at "2026-11-12T16:30:00Z" \
  --type input \
  --recheck J2684 \
  --action "Elected Chief resolves J2339 and decides Short PASS on HOS 008 Short A v04 (76d801a3)" \
  --git

python3 scripts/jobs.py done J2684 --agent codex \
  --result "Verified J0912 condition (jobs/reviews/J2684/REVIEW.md): J2339 remains open (gated by moving_video_input in QUEUE.json) and Chief Short PASS on HOS 008 Short A v04 (76d801a3) is still pending; recorded full 00:00-00:22 watch-and-listen KEEP review in J2684 and kept J0912 blocked" \
  --git
```

### Option B — If Chief `codex` Accepts `J2339/QA_v04.md` + `J2684` Watch-and-Listen `KEEP` Review as Completing `J2339`
If the elected Chief (`codex`) rules that `10_Shorts/J2339/QA_v04.md` (`bcefd472`) + the `00:00–00:22` `default_api:read_file` watch-and-listen `KEEP` check in §3 above satisfies `J2339` (as in `J2508` and `J2510`) and grants `Short PASS` on `hos_008_short_A_v04.mp4` (`76d801a3…`), Chief can close `J2339`, record `Short PASS` on `J0912` (or stage `hos_008_short_A_v04.mp4` for Ben's watch), and close `J2684`.
