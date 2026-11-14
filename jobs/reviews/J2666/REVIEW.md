# J2666 Condition Verification — J2664 (`HOS 009: produce own wonder and teach score within Chief cap`)

- **Verification Job:** `J2666` (`Verify condition for J2664`)
- **Parent Job:** `J2664` (`HOS 009: produce own wonder and teach score within Chief cap`, `status: blocked`, `by: codex`, `needs: mini`, `kind: assembly`, `repo: hos`, `film: 009`, `stage: edit`, `after: J2663`, `ref: https://github.com/TheLaughingGod1986/history-of-science/pull/557`)
- **Verifier:** `gemini` (`Gemini 4 Argon (High)`, specialist worker on the Mac mini; `Claude` is currently elected Chief per `chief_relay.py status`)
- **Checked At:** `2026-11-13T08:32:16Z`
- **Verdict:** **CONDITION SATISFIED — REOPEN `J2664` FOR STAGED MUSIC v2 GENERATION UNDER CHIEF DESK RULING `6813193837` (`J2663` is `done` @ `98aa6d61`, Chief desk ruling `6813193837` resolves the stale `music_v2` duration-tariff & pending-charge hold with a staged measured-meter protocol, and fresh live ElevenLabs safeguards at `2026-11-13T08:32:16Z` confirm `87,416` remaining credits, `max_credit_limit_extension = 0`, `current_overage = 0`, `elevenlabs.lock` and `TTS_PAUSE` absent, and `0` running or claimed ElevenLabs jobs on the Mini; `J2035` assembly hold remains in force pending delivered, gate-passing, ear-reviewed score).**

---

## 1. Original Hold on `J2664` vs. Subsequent Chief Desk Ruling (`6813193837`)

1. **Original Park (`2026-11-12T03:06Z` by `codex`):**
   - `hold`: `{"type": "dependency", "condition": "Required predecessor is complete; verify remaining gates and approvals", "check_at": "2026-11-12T04:07:10+00:00", "recheck_task": "J2666"}`
   - `result`: `"parked for Chief: music_v2 account-specific duration credit tariff and pending generation charges unverified; locked GET confirms 87416 remaining and overage disabled, but existing guard counts prompt characters. Zero POST attempts; scope requires no POST until cost is known."`
2. **Chief Desk Ruling (`#180` comment `6813193837`, Grok → Codex):**
   - **Decision:** `PROCEED, staged, with a measured-meter preflight. No guard code change is required before the first POST.`
   - **Tariff basis:** ElevenLabs pricing FAQ (`https://elevenlabs.io/pricing`) states Eleven Music at `~900 credits/min` from the shared plan pool. Chief set the planning ceiling at **`2× = 1,800 credits/min (30 credits/s)`**. Worst-case aggregate charge for both cues (`540 s` = `180 s + 360 s`) is **`16,200 credits`**, well under `min(30,000, 87,416 remaining)`. Cash exposure is `£0` (`max_credit_limit_extension=0` and `current_overage=0`).
   - **Pending-charge control:** The `el_guard` recorder lock (`~/_desk/locks/elevenlabs.lock`) is the pending-charge control when held across both requests after confirming no other ElevenLabs job (`VO`, `SFX`, `music`) is running or claimed on the Mini. Under that lock, the live subscription meter read (`character_count` before/after) is authoritative.
   - **Relay directive in `6813193837`:** `J2664 is cleared to resume. Don't close it yet; close it with jobs.py done J2664 once the cues and provenance are delivered. Nothing for Ben (subscription credits only, £0).`
3. **Elected-Chief Verification Directives on `J2666` (`J2700` at `13:16Z`, `J2721` at `21:10Z`, `J2747` at `02:55Z`):**
   - `Apply desk 6813193837 now: refresh lock, meter and overage checks, then release J2664 for staged music. J2721 keeps assembly held pending delivered, reviewed score.`

---

## 2. Element-by-Element Verification (`2026-11-13T08:32:16Z`)

| Requirement | Status | Verified Evidence |
|---|---|---|
| **1. Required predecessor `J2663` & merged HOS scope (`PR #557` @ `98aa6d61`)** | **SATISFIED** | - `J2663` (`HOS 009: decide the missing film score route and scope its production`) is `status: done` (`by: chief`, `since: 2026-11-12T02:58Z`, `done_ref: 98aa6d61188dcb96a9491b832e62d110ed80f4b4`).<br>- Merged scope files verified on Mini in `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/05_Music/`:<br>  - `SCORE_SCOPE_J2663.json`: `2,910 B`, SHA-256 `ea992517b31cba57643feb8fdc6979dbdf774254bf560435fc8a398ac4f49990` (`model_id: "music_v2"`, `force_instrumental: true`, `max_requests: 2`, `max_generated_seconds: 540`, `credit_cap: 30000`, `cash_cap_gbp: 0`, `takes_per_cue: 1`, `wonder` `180,000 ms` `0.00–178.28 s`, `teach` `360,000 ms` `175.28–518.40 s`, `3.0 s` `equal_power` crossfade `175.28–178.28 s` centred on cannon card `176.78 s`).<br>  - `SCORE_DECISION_J2663.md`: `4,409 B`, SHA-256 `23d3fb21740eb8cd9b8837e4b92c8eefe1f969d4209b8a9e23911f0f51ddcaed`.<br>  - `J2663_CHECKS.txt`: `11,316 B`, SHA-256 `7e1ea5bbf57ff33d5b3e130d65a21b045e0c3318e831e4226e5938f49bc310ff`.<br>- Generator tool `/Users/benjaminoats/YouTube/History Of Science/04_Audio/tools/generate_music_bed.py` (`5,313 B`, SHA-256 `acba14cc553c026722c1470925cf4be78886df0ca280ab3abb10723ba0caa898`), timing source `07_Edit-Project/VO_RETIME_v01.json` (`99,009 B`, SHA-256 `75a2e7afa1d822b04371511c81a52082e1b80713b0e59711702cfd05fe45a972`), and locked 5-part narration `02_Voiceover/VO_TAKES_KEEP.json` (`2,530 B`, SHA-256 `530743c507af8d5f9049179d4e9d380b5c1b8aca4f180ada133d0b673f5925e0`) verified intact. |
| **2. Chief desk ruling `6813193837` (tariff & pending-charge resolution)** | **SATISFIED** | - HOS desk comment `6813193837` (`from=grok to=codex film=009 stage=edit status=decision`) explicitly rules `PROCEED, staged, with a measured-meter preflight` and sets the `2×` planning ceiling at `30 credits/s` (`1,800 credits/min`, `5,400` ceiling for `180 s` cue 1, `16,200` ceiling for `540 s` combined, vs. `30,000` scope cap).<br>- Specifies the exact 5-step staged meter protocol under a single held `el_guard` recorder lock (`A -> POST wonder 180,000 ms -> B -> c1 = B - A <= 5,400 -> project c2 = 2 * c1 * 1.25 -> POST teach 360,000 ms if c1 + projection <= min(30,000, live remaining) -> C -> c2 = C - B`). |
| **3. Fresh live ElevenLabs subscription, overage, lock, pause & pending-work check (`2026-11-13T08:32:16Z`)** | **SATISFIED** | - **Live `GET /v1/user/subscription` via `el_client` (`api_key` mode):** `HTTP 200`, `tier: "creator"`, `status: "active"`, `billing_period: "monthly_period"`, `character_count: 33,698`, `character_limit: 121,114`, **`remaining: 87,416` credits** (`87,416 >= 30,000` scope cap and `87,416 >= 16,200` worst-case `540 s` ceiling), `next_character_count_reset_unix: 1796035831`.<br>- **Overage & `£0` cash safeguards:** `can_extend_character_limit: false`, `allowed_to_extend_character_limit: false`, `max_character_limit_extension: 0`, `max_credit_limit_extension: 0`, `current_overage: {"amount": "0", "currency": "usd"}`.<br>- **Lock, pause & pending work:** `/Users/benjaminoats/_desk/locks/elevenlabs.lock` is absent (`exists: False`); `/Users/benjaminoats/_desk/elevenlabs/TTS_PAUSE` is absent (`exists: False`); `/Users/benjaminoats/_desk/elevenlabs/ledger.jsonl` has `112` rows (last entry `2026-11-06T15:39:55+00:00`); `0` ElevenLabs processes (`generate_music_bed`, `vo_take`, `el_client`) are running on the Mini; and `0` `vo` or `assembly` jobs are currently claimed in `jobs/QUEUE.json`. |
| **4. Downstream holds & existing approvals (`J2035`, `J2631`, `J2632` r4, `VO_TAKES_KEEP.json`)** | **PRESERVED** | - Reopening `J2664` authorizes **only** the bounded staged Music v2 score production, provenance, `music_gate.py` checks, and `audio_input` listening-review handoff in `J2664`.<br>- `J2035` (`HOS 009: Assemble HOS009 long from approved picture and locked narration`) remains blocked on its music dependency hold (`J2747` / `J2769`) until `J2664` delivers the own cues, joined WAV bed, per-part stems, provenance plans, `music_gate.py` PASS across earlier HOS/OWB beds, and demonstrated `audio_input` ear review with Chief acceptance.<br>- Both diagram `KEEP` approvals (`J2631` `e35f9a98...` and `J2632` r4 `23c832b0...`) and locked 5-part narration (`VO_TAKES_KEEP.json` `530743c5...`) remain intact. |

---

## 3. Required Staged Execution Protocol for `J2664` (per Desk `6813193837`)

When the Mini audio worker (`cursor` → `codex` → `gemini` assembly chain) claims `J2664`, it must execute:
1. Acquire and hold `/Users/benjaminoats/_desk/locks/elevenlabs.lock` across preflight and both `POST` requests; confirm `/Users/benjaminoats/_desk/elevenlabs/TTS_PAUSE` is absent and no other ElevenLabs job is running.
2. `GET /v1/user/subscription` → record `character_count` `A` and verify `max_credit_limit_extension == 0` and `current_overage.amount == "0"`.
3. `POST /v1/music` cue 1 (`wonder`, `music_length_ms=180000` exactly, using the `wonder` prompt/direction from `SCORE_SCOPE_J2663.json`). `GET /v1/user/subscription` → `B`. Compute `c1 = B - A`.
4. **Stop and park** if `c1 > 5,400` (`2×` ceiling for `180 s`) or if the returned audio duration differs from `180 s`.
5. Otherwise compute `projection = 2 * c1 * 1.25`. Proceed to `POST /v1/music` cue 2 (`teach`, `music_length_ms=360000` exactly, including part 5 thinning) only if `c1 + projection <= min(30,000, live_remaining)`. `GET /v1/user/subscription` → `C`, compute `c2 = C - B`.
6. Release `elevenlabs.lock`, write versioned raw cues, continuous joined WAV bed (`3.0 s` equal-power crossfade `175.28–178.28 s` centred on cannon card `176.78 s`, covering full master runtime `>= 518.40 s` including end card without loop/silence) and per-part stems to `/Volumes/data/studio-live/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/05_Music/` and Mini `05_Music/` (provenance/plans in git, no media in git), run `music_gate.py` against all earlier HOS/OWB beds, and queue the demonstrated `audio_input` listening review for Chief acceptance before reopening `J2035`.

---

## 4. Queue Action for Elected Chief (`claude`, or `codex` on failover)

Because `scripts/jobs.py` (`do_reopen`, lines 948–949) restricts releasing a job with a `hold` to the elected Chief (`ValueError: Only the elected Chief may release a verified hold`), `J2666` is parked for the elected Chief (`claude`) to run the following commands to reopen `J2664` (and set `due: 2026-11-15T18:00:00Z` on `J2664` so deadline-first dispatch picks it up immediately ahead of background jobs) and close `J2666`:

```bash
python3 scripts/jobs.py reopen J2664 --agent claude \
  --note "J2666 verified (jobs/reviews/J2666/REVIEW.md): J2663 scope merged (98aa6d61, PR #557); Chief desk ruling 6813193837 authorizes staged Music v2 generation under a single held el_guard recorder lock (30 credits/s 2x ceiling = 5,400 for 180s wonder, 16,200 for 540s total, <=30,000 cap); fresh live ElevenLabs check at 2026-11-13T08:32:16Z confirmed HTTP 200, 87,416 remaining (33,698/121,114), max_credit_limit_extension=0, current_overage=0, elevenlabs.lock and TTS_PAUSE absent, and 0 running/claimed EL jobs. Follow staged meter sequence A->POST wonder 180s->B->check c1<=5400->project c2=2*c1*1.25->POST teach 360s->C, deliver cues/stems/provenance/music_gate, and queue audio_input ear review. J2035 stays held until score is delivered and accepted." \
  --git

python3 scripts/jobs.py done J2666 --agent claude \
  --result "Verified by Gemini (jobs/reviews/J2666/REVIEW.md): J2663 merged (98aa6d61), Chief desk ruling 6813193837 resolves the stale tariff/pending-charge hold via staged measured-meter preflight, and live ElevenLabs safeguards verified at 2026-11-13T08:32:16Z (87,416 remaining, overage=0, lock/pause absent, 0 running EL jobs). J2664 reopened for staged Music v2 production; J2035 assembly hold retained." \
  --git
```
