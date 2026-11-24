# J3529 — Condition Verification for J3492 (WW2:009)

- **Checked at:** `2026-11-24T12:38Z–12:40Z`
- **Checker:** `macbook` (`kind: review` specialist worker; non-Chief)
- **Original held job:** `J3492` (*WW2 film 009: Claude Rule-6 viewer test (first 300 words), Rule E lock & queue VO*)
- **Waiting condition:** `J3491 (independent Gemini claims check on WW2:009 PR #68) completes with 01_Script/CLAIMS_CHECK.md PASS or v02 fixes applied`
- **Verdict (recommended to Elected Chief):** **CONDITION NOT MET — keep `J3492` blocked**

## Evidence Checked

1. **Queue state (`jobs/QUEUE.json` @ `5dd829eae`):**
   - `J3491` (`needs: gemini`, `kind: facts`, `film: WW2:009`, `stage: sources`, `due: 2026-11-30T12:00:00Z`) is **`open` and unclaimed** (`by: ""`, `result: ""`). Its only history entry is `2026-11-24T10:00Z by macbook: added`.
   - `J3492` (`needs: mini`, `kind: review`, `film: WW2:009`, `stage: script`, `due: 2026-11-30T18:00:00Z`) is **`blocked` by `macbook`** at step 3/4 with `hold.type: dependency` and `hold.recheck_task: J3529`.
   - `J3474` (drafting PR #68) is **`done`**. No other job in `QUEUE.json` covers `WW2:009` claims checking.
2. **`ww2-channel` repository and PRs (fetched at `12:38Z`, checked PRs through `#77`):**
   - **PR `#68`** (`macbook/J3474`, commit `ebb960010286650df703b4b6f013373f3364de9d`): `OPEN` (unmerged). Contains `TOPIC_REVIEW.md`, `03_Picture/ARCHIVE_PROVENANCE.md` (41 official UK IWM A/GM PD IDs), `01_Script/SCRIPT.md`, `01_Script/NARRATION_v01.txt` (`16,406` stripped spoken chars, `2,716` words, SHA-256 `2de059ed72849c3b45735adcdfd4b277d90e9328e4773351c7792cfdb41feeb4`), `01_Script/SOURCES.md` (37 claims `C01`–`C37`, 4 flagged items `F1`–`F4`), and `status.json`.
   - **PR `#70`** (`macbook/J3492`): `OPEN` (unmerged). Stacked on PR `#68`; adds `01_Script/VIEWER_TEST_v01.md` (Rule-6 first-300-word viewer test `PASS` with 1 minor `P02` wording polish; Rule-E topic/packaging `GO`; Rule-9 voice budget `PASS`) and updates `status.json`, leaving `SCRIPT.md`, `NARRATION_v01.txt`, and `SOURCES.md` unchanged for `J3491`.
   - **No `01_Script/CLAIMS_CHECK*.md` exists** on `main`, `origin/macbook/J3474`, `origin/macbook/J3492`, any other remote branch or PR in `ww2-channel`, or `/Volumes/data/studio-live`.
   - **No `v02` script fixes** have been applied.
3. **Original gates and guards remain valid:**
   - Script lock deadline: `2026-11-30T18:00:00Z` (target air slot: Sat 12 Dec 2026 17:00 London; Ben's watch due Wed 9 Dec 2026).
   - ElevenLabs spend guard: **no voice spend before `2026-11-30 10:50Z`** (`£0` spent).
   - Studio thread read to `#7131682495` (up to date; no separate `J3491` claims report posted).
4. **Why `J3529` is parked for Elected Chief:**
   - `scripts/jobs.py` (`set_wait` lines 603–604 and `done` lines 1595–1598) restricts `jobs.py wait J3492 --recheck J3529` to the elected Chief (`chief_relay.elected_for`) and refuses `jobs.py done J3529` until `J3492.hold.last_recheck == "J3529"` (or `J3492` is reopened).
   - `chief_relay.py status` at `12:39Z` reports **Chief: Codex** (`claude` out of usage until `2026-11-24T12:50:00Z`, `chief` down). `macbook` is a specialist worker and never impersonates Chief (`AGENTS.md`).

## Recommended Action for Elected Chief

`J3491` is the sole open `needs: gemini` job in the queue (`gemini` checker is `UP`). Recommend keeping `J3492` blocked with a 6-hour recheck at `2026-11-24T18:30:00Z` (well ahead of the `2026-11-30T18:00:00Z` lock deadline):

```bash
python3 scripts/jobs.py wait J3492 --agent <chief_id> \
  --condition "J3491 (independent Gemini claims check on WW2:009 PR #68) completes with 01_Script/CLAIMS_CHECK.md PASS or v02 fixes applied (J3491 still open/unclaimed as of 2026-11-24T12:40Z)" \
  --check-at "2026-11-24T18:30:00Z" \
  --type input \
  --recheck J3529 \
  --action "Verify J3491 CLAIMS_CHECK.md, fold P02 polish + any fixes into v02, lock WW2:009 script (<=30 Nov 18:00Z), and queue post-reset VO (>30 Nov 10:50Z); viewer test in ww2#70" \
  --git

python3 scripts/jobs.py done J3529 --agent <chief_id> \
  --result "Verified unmet at 2026-11-24T12:40Z (J3491 still open/unclaimed; no CLAIMS_CHECK.md in ww2-channel PR #68/#70 or main); recorded J3492 wait --recheck J3529 to 2026-11-24T18:30:00Z" \
  --git
```

*(Optional Chief note: `J3491` currently has `needs: gemini` whereas later WW2 claims checks `J3523`/`J3525` use `needs: any`. If the Mini Gemini checker does not claim `J3491` before `18:30Z`, Chief may consider widening `J3491` or checking the Mini `agy` worker.)*
