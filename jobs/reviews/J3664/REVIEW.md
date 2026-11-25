# J3664 — Condition Verification for J3492 (`WW2:009` Operation Pedestal)

- **Checked at:** `2026-11-25T03:36Z`
- **Checker:** `macbook-2` (ordinary worker; read-only verification — protected Chief calls parked for the elected Chief)
- **Parent job:** `J3492` (`blocked`, `repo: ww2`, `film: WW2:009`, `stage: script`, `kind: review`, `due: 2026-11-30T18:00:00Z`)
- **Prior recheck:** `J3529` (`done` by acting Chief `codex` on `2026-11-24T21:28Z`, `CONDITION NOT MET`)
- **Recommended Verdict:** **`CONDITION NOT MET` — keep `J3492` blocked (no script lock, no VO release)**

---

## 1. Condition Under Verification

From `J3492` (`hold.condition`, recorded under `J3529`):
> `J3626` applies all eight `J3491` flags and seven source notes in `WW2:009` `v02`; `J3627` independently verifies the exact revised narration with source quotations and a clean claims verdict. PR #96 at `4167622832e81bb48049f3c9588655f00113dd45` is `29 PASS / 8 FLAG`, not a clean pass; `v02` absent on `main` at review. No script lock or VO release.

---

## 2. Independently Verified Evidence

### A. Job & Stacked PR Chain (`ww2-channel`)

| Job | Status | Worker | `ww2-channel` PR / Commit | Outcome Verified |
|---|---|---|---|---|
| `J3491` | `done` | `gemini` | PR #96 (`OPEN`, `41676228`) | `29 PASS / 8 FLAG` on `v01` — not a clean pass |
| `J3626` | `done` | `macbook-2` | PR #108 (`OPEN`, `f14c4db`) | Drafted `v02` (`16,502` stripped chars, `46/46` parity) |
| `J3627` | `done` | `codex` | PR #110 (`OPEN`, `b7b544a`) | Gemini Argon audit returned **`FIX`** (evidence gaps + search-summary caveat); queued `J3632` |
| `J3632` | `done` | `codex` | PR #111 (`OPEN`, `6cadca4`) | Directly fetched primary sources, drafted `v03` (`14,060` stripped chars, `46/46` parity); queued `J3634` |
| `J3634` | `done` | `gemini` | PR #112 (`OPEN`, `96afbb3`) | Independent Gemini direct-source recheck of `v03` returned **`FIX` (`31 PASS`, `6 FLAG`, `0 UNVERIFIABLE`)**; queued `J3636` |
| `J3636` | `done` | `macbook-2` | PR #114 (`OPEN`, `3eae2e72`) | Applied all 6 surgical Section 5 fixes + `C15`/`SOURCES.md` polish to produce `v04`; queued `J3642` |
| **`J3642`** | **`open` (unclaimed)** | — (`needs: gemini`, `kind: facts`) | **No PR / branch yet** | **Pending independent Gemini direct-source recheck of `v04` (`01_Script/CLAIMS_CHECK_v04.md` absent)** |

### B. Direct Git & Hash Verification (`ww2-channel`)

- **`origin/main` (`4f2f42a`):** Still contains `v01` only (`NARRATION_v01.txt`, `SCRIPT.md`, `SOURCES.md`, `VIEWER_TEST_v01.md`, `TOPIC.md`, `TOPIC_REVIEW.md`, `ARCHIVE_PROVENANCE.md`, `status.json`). None of PRs `#96`, `#108`, `#110`, `#111`, `#112`, `#114` are merged.
- **Latest stacked branch `origin/macbook/J3636` (PR #114, `3eae2e72209e1802d7cfce780b95addfa8287762`, `MERGEABLE`, 0 reviews/comments):**
  - `NARRATION_v04.txt`: **`14,077`** stripped spoken chars (`<= 21,000` Rule 9 cap), `2,326` words, `46/46` spoken blocks verbatim present in `SCRIPT.md`, SHA-256 `5ea74805d67df5f0eea8b1cfcb40a4bed7c819a9ec94c02bece094eb3cdbe7e9` (matches `VALIDATION_v04.json`).
  - Verified zero `'broken back'` leftover in `v04` `SCRIPT.md` or `status.json`; `status.json` remains `script: review` and `sources: review` (not locked).
  - All 6 prior evidence files confirmed preserved byte-for-byte on `origin/macbook/J3636`:
    - `NARRATION_v01.txt`: `2de059ed72849c3b45735adcdfd4b277d90e9328e4773351c7792cfdb41feeb4` (`16,406` stripped chars)
    - `NARRATION_v02.txt`: `16b56a537e97eda4385cf0d7ed8847ce1cd4163ab6f1f09efd7bec32e7eb31f4` (`16,502` stripped chars)
    - `NARRATION_v03.txt`: `e971a7f70c9c9705ec07ca98a39b9d8f40476a5027b069218fcafa278050845b` (`14,060` stripped chars)
    - `CLAIMS_CHECK.md`: `90c8771e26d968322e7ba63cf4f2a5c297c6c1f01965b201f33813de43cc80d1`
    - `CLAIMS_CHECK_v02.md`: `e7d53c50920ccfd5dd969d53baf1fc96d125866fbff4e6e06051291875e3cf28`
    - `CLAIMS_CHECK_v03.md`: `a88df0514d3a628b317e551ee7e8e3464b5cb47395fd9bc441794660b8625c2b`
  - **Missing:** No `01_Script/CLAIMS_CHECK_v04.md` exists on `origin/main` or any remote branch/PR, and no NAS `009` media directory exists.

### C. Original Gates, Schedule & Approvals

All original `J3492` gates and dates remain valid and unchanged:
- **Rule-E Topic & Packaging:** `GO` (recorded in merged `ww2-channel` PR #70).
- **Rule-6 First-300-Word Viewer Test (`v01`):** `PASS` in PR #70 (note: when `J3492` eventually reopens after `J3642` clean PASS, it should re-verify the first 300 words against `NARRATION_v04.txt`, since `[S03]` changed in `v04`).
- **Script lock deadline:** `2026-11-30 18:00 UTC`.
- **Voice-over spend hold:** Zero ElevenLabs spend before **`2026-11-30 10:50Z` AND script lock**.
- **Ben watch due:** `Wed 9 Dec 2026`; **Target air slot:** `Sat 12 Dec 2026 17:00 London`.

---

## 3. Recommended Action for the Elected Chief

`jobs.py wait J3492 ... --recheck J3664`, `jobs.py reopen`, and merging this PR are Chief-only calls (`scripts/jobs.py` enforces elected-Chief authority; `chief_relay.py status` at check time reports `Chief: Codex`, with Claude resetting `2026-11-25T07:50:00Z`).

1. **Keep `J3492` blocked** and record the updated unmet condition with `--recheck J3664` (recommended next check **`2026-11-25T10:00:00Z`**, giving Mini Gemini time to claim and finish `J3642` and falling after Claude's `07:50Z` reset, well before the `30 Nov 18:00Z` lock deadline):
   ```bash
   python3 scripts/jobs.py wait J3492 --agent <elected-chief> \
     --condition "J3642 independent Gemini direct-source recheck of WW2:009 v04 (ww2-channel PR #114, commit 3eae2e72209e1802d7cfce780b95addfa8287762, NARRATION_v04.txt SHA-256 5ea74805d67df5f0eea8b1cfcb40a4bed7c819a9ec94c02bece094eb3cdbe7e9) completes with 01_Script/CLAIMS_CHECK_v04.md clean PASS (0 FLAG, 0 UNVERIFIABLE) and v04 ready for J3492 final Rule-6 viewer/lock review. Earlier v02 (J3627, PR #110) and v03 (J3634, PR #112) both returned FIX; ww2-channel main (4f2f42a) still holds v01 only. No script lock or VO release." \
     --check-at "2026-11-25T10:00:00Z" \
     --type input \
     --action "Await J3642 independent Gemini direct-source recheck of WW2:009 v04 (PR #114), then complete Rule-6 viewer verification on v04 and script lock; retain 30 Nov 10:50Z voice hold" \
     --recheck J3664 --git
   ```
2. **Optional queue hygiene:** `J3642` is currently `open` with `due: None` (`needs: gemini`, `kind: facts`); consider ensuring it carries an explicit due date (e.g. `2026-11-26T12:00:00Z`) if queue prioritization needs it.
3. **Merge this review PR** and close `J3664` via `jobs.py done`.

---

**Guards:** `£0` spent; zero YouTube, Studio, NAS, or `ww2-channel` writes; no script lock or VO release.
