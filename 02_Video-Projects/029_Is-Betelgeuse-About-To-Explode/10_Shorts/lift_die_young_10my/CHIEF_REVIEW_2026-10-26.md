# J0979 — changes required, v01 held

Acting Chief: codex, 26 October 2026. `chief_relay.py status` confirmed Codex elected immediately before this ruling. This is a Short review only; the approved 029 long is unchanged.

## Ruling

**CHANGES REQUIRED. No Short PASS, Ben-watch handoff or upload approval.** Keep v01 held. The completed assembly is still 4/4; completed production is not editorial approval.

The title asks “Why Is Betelgeuse Already Dying at Just 10 Million Years Old?” but the first VO line states “Betelgeuse is only about ten million years old, and it is already near the end of its life.” This fails the 26 October Keeper requirement in `FAMILIAR_DANGER_STRATEGY.md` (Short hook), `STUDIO_PLAYBOOK.md` §3 and `.cursor/rules/orbit-build-shorts.mdc`. The later “Why so fast?” does not repair line 1. This is a 67.62–91.94 s chapter lift, not Test A's opening 30–38 s; its exemption does not apply. No earlier Ben-approved scheduled cut exemption is evidenced.

## Evidence checked

- Queue body, result and complete history; production commit `72672cebe`; README, transcript, word-timing metadata, assembler and saved gate reports.
- Local master SHA-256 verified: `dc6bd3ccf387ecfdcc4bfa8483dec5f94026662a50ac1717b1bb3fee85c532fc`, matching the committed manifest.
- Contact sheet visually inspected at 0, 0.5, 1.8, 4.2, 6.8, 10.2, 12.8, 15.8, 19.2 and 21.7 s. Frame 0 puts a small star/radius comparison in a large star field. It does not meet the close, subject-filling opening requirement; a radius/orbit diagram also does not explain the spoken age. Reframe existing subject picture and reserve the single teaching graphic for the quantity actually spoken.
- Saved opening gate PASS: 22.40 s, onset 0.092 s, first cut 2.97 s, tail 1.44 s, no opening-gate warnings. Saved SFX, picture, polish and music reports say PASS. These do not check the title/first-line semantic rule. Picture/polish retain a low-detail warning at approximately 0:04, and music comparison logs contain unreadable-reference warnings; do not describe the whole pack as warning-free.
- Metadata contains an end-card and mass-callout definition, but the inspected final compositor does not overlay those inputs. Do not infer those extra cards appear in the export from metadata alone. Regenerate accurate metadata for any revision.

This is a rejection based on verified blocking defects, not a full moving-picture/audio acceptance review. Full frame, sound and phone review remains necessary on a corrected cut.

## Concrete next step

Queue a no-spend `review` specialist task to inspect existing locked 029 VO and return an edit decision list with exact source times: one complete subject-naming opening question matching the title, a coherent answer, 22–27 s, and no newly written or generated speech. Do not merely move the anaphoric “Why so fast?” to frame 0. Check existing Shorts for duplicate ideas. If 029 cannot supply this, assess another eligible locked long under the original fewest-Shorts brief and document the choice; preserve Sun/date/credit/Ben holds.

The task must return either a feasible existing-media plan for a separately assigned assembly revision, or an evidenced recommendation to cancel this reserve candidate. It must not mint VO, spend credit, render speculative replacements, upload or schedule. Return the plan to the elected Chief. J0979 stays blocked with that task as its dependency; there is no external wait or arbitrary retry date. The proposed 18 December slot remains provisional and must be checked again before any later approval.

---

## Acting-Chief Verification (`J1042`, 27 October 2026)

Acting Chief: `gemini` (`chief_relay.py status` confirmed Gemini elected immediately before this ruling).

1. **Predecessor `J1000` verified complete (`92a775ee8`):** [`J1000_EXISTING_VO_AUDIT_2026-10-27.md`](J1000_EXISTING_VO_AUDIT_2026-10-27.md) audited all `108` sentences (`12` questions) of `029_Is-Betelgeuse-About-To-Explode` locked VO (`betelgeuse_words_list.json`) and all other pre-26-Oct locked/live OWB longs (`021`–`028`) under the fewest-Shorts brief and active Keeper/Sun/Saturn/date/credit holds:
   - In `029`, 9 of the 12 questions are anaphoric or omit `Betelgeuse` (`s03`, `s14`, `s27`, `s34`, `s41`, `s72`, `s80`, `s84`, `s103`), and the only 3 questions naming `Betelgeuse` (`s02`, `s28`, `s98`) either collide with the parent long's exact listing title (*"Is Betelgeuse About to Explode?"*, `vP1BbqZ_dnM`) and `fri11_opening_testA`, or are already used in `wed09_great_dimming`.
   - Across `021`–`028` (each scripted and recorded on or before 8 Oct 2026, with 5–9 Shorts already built), zero unused, self-contained, non-anaphoric, subject-naming spoken questions exist in line 1 (`0–2.5 s`).
2. **Decision on `J0979` & `029_short_lift_die_young_10my_v01`:**
   - **Release conditions NOT satisfied for pre-26-Oct locked longs (`021`–`029`).** `029_short_lift_die_young_10my_v01` remains permanently shelved (no Short PASS, no Ben-watch handoff, no upload or scheduling; `029` already has its complete 3-Short release week in `wed09_great_dimming`, `fri11_opening_testA`, and `mon14_half_moon_daylight`, and the provisional `2026-12-18` slot stays open).
   - **`J0979` (`owb-short-from-locked`) stays blocked (`wait --recheck J1042`)** until after the 30 Oct 2026 ElevenLabs credit reset (`2026-10-31T09:00:00Z` next verification) when a post-26-Oct OWB long (`031+`) locks its VO and picture with an unused Keeper-compliant subject-naming question opening. Keeping `J0979` blocked on this condition also holds the `owb-short-from-locked` backlog key in `refill.py` so no duplicate no-spend existing-VO Short job is spawned against `021`–`029` in the interim.
