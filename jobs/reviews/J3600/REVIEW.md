# J3600 Condition Verification Review — J3431 (`WW2:005` St Nazaire)

- **Reviewer:** `macbook` (advisory worker; parked for elected Chief)
- **Date:** 2026-11-24 UTC
- **Original held job:** `J3431` (`WW2:005` picture — top up archive photographs before edit)
- **Dependent edit job:** `J3432` (`WW2:005` edit, `after: J3431`; air Thu 3 Dec 17:00 London, Ben's watch due `2026-11-30T20:00:00Z`)
- **Waiting condition checked:**
  > J3449 brings film 5 to at least 50% real archive (rule 1 as changed 24 Nov, PR #59); then accept the picture stage and release J3432.
- **Advisory verdict:** **CONDITION NOT MET — keep `J3431` blocked and `J3432` dependent on `J3431`.** Do not accept the picture stage or start assembly.

---

## 1. Evidence Verified

1. **Rule in force (`ww2-channel` `studio/RULES.md` rule 1, merged PR `#59` `124d687`, `studio/LEARNINGS.md` #8):**
   - Real archive photographs must carry **at least half (50%)** of screen time, aiming for two-thirds; a film is never held for the stretch between half and two-thirds.
   - On film 5's `1,263.04 s` runtime basis, the **50% floor is `631.52 s`** (two-thirds aim: `842.03 s`).
2. **Completed `J3449` result (`done` by `codex` at `2026-11-23T20:39Z`, studio thread `#7113358323`, `ww2-channel` draft PR `#50` head `01d5f756d222175d051442e5de5468313b1bb5ce`):**
   - `J3449` returned **FIX**, not a ≥50% pass.
   - Independent check of `02_Video-Projects/005_St-Nazaire-Raid-HMS-Campbeltown-Dry-Dock/03_Picture/PICTURE_PLAN_J3431.json` on `origin/codex/J3431-archive`:
     - **50** unchanged narration paragraphs; **115** timed segments (**64** photo segments across **32** distinct photo IDs out of 60 verified inventory IDs); `5.58 s` interchapter non-photo residual.
     - Paragraph duration sum: `1,257.46 s` + `5.58 s` interchapter = **`1,263.04 s`**.
     - Photo-dominant sum (verified identically across both paragraph totals and individual segment durations): **`510.27 s`**.
     - Non-photo (code maps/diagrams/cards + interchapter) sum: **`747.19 s` + `5.58 s` = `752.77 s`**.
     - **Verified real-archive share: `510.27 / 1,263.04 s = 40.400%`**.
     - **Shortfall vs Rule 1's 50% floor (`631.52 s`): `121.25 s` short** (`331.76 s` short of the `842.03 s` two-thirds aim).
   - **Why `48.3%` in the 24 Nov 09:09Z queue note is superseded:** `48.3%` (`610.11 s`) was `J3431`'s earlier pre-review percentage estimate (`e9e9aba`). `J3449`'s phrase-anchored shot-by-shot audit removed unsupported contextual placements (unrelated depth-charge handling in P19, generic commando training for dock rehearsals, Sturgeon past identification, aftermath aerial during civilian shooting), lowering the defensible timed share to **`40.400%`**.
   - **Concentration & non-photo runs:** `C 2351` already carries `127.50 s` across 13 slots in 12 paragraphs; the longest consecutive non-photo runs are `174.56 s` (P28–35) and `106.33 s` (P39–43).
3. **Independent NAS file & SHA-256 verification (`/Volumes/data/studio-live/ww2/02_Video-Projects/005_St-Nazaire-Raid-HMS-Campbeltown-Dry-Dock/03_Picture/`):**
   - Verified all **60** primary photographs listed in `ARCHIVE_INVENTORY_J3431.json`: **60/60 present, 60/60 SHA-256 hashes match, 0 missing, 0 mismatches** (`49/60` primary files are `< 1,600 px` wide).
   - Directory counts confirmed on the shared film store: `archive/`: 10 files; `archive/J3431/`: 51 files (60 primary minus 10 existing plus 1 preserved excluded A13626 duplicate); `archive/J3431/larger_iwm/`: 39 files; `archive/larger_iwm/`: 2 files; `maps/`: 38 files.
4. **`ww2-channel` PR `#50` (`codex/J3431-archive`, `01d5f75`) status vs `origin/main` (`7de038c`):**
   - PR `#50` remains **OPEN / DRAFT** (retained as unfinished in `J3549` / `PR #90`).
   - Because `ww2-channel` PR `#90` merged `#20` and `#56` at `16:03Z` (after PR `#50` was last synced at `15:11Z`), PR `#50` now has a **merge conflict in `02_Video-Projects/005_St-Nazaire-Raid-HMS-Campbeltown-Dry-Dock/status.json`**: `main` holds all 7 stage entries (`topic`, `script`, `sources`, `vo`, `shots`, `picture`, `edit`), whereas PR `#50` holds only `picture` in `stages`. Any later sync or merge of PR `#50` must preserve all 7 stages from `main`.
   - `ww2-channel` `main` `status.json` accurately records `picture.state = "blocked"` (`40.400%`, awaiting Chief editorial decision) and `edit.state = "todo"`.

---

## 2. Editorial Options for Elected Chief (Updated for 24 Nov 50% Rule)

`J3449` recommended a **no-spend existing-VO paper recut** centred on dock engineering, originally calculating a `765.40 s` ceiling (`497.64 s` cut) against the old two-thirds bar. Under Rule 1 as amended in PR `#59` (**50% floor**):

- **Updated 50%-floor ceiling (keeping all `510.27 s` photo time):** `1,020.54 s` (`17:00.54`), requiring at least **`242.50 s` (~4 min 02.5 s)** trimmed using complete existing sentences from the 9 locked voice-over takes (`£0`, no new VO, no new sourcing). Each photo second lost lowers the 50%-compliant ceiling by `2.0 s`.
- Candidate non-photo detours already flagged by `J3449` (P6 Bismarck detour `24.29 s`, P16/P27–32 tide/route/signalling, P20–21/P41 repeated timer/charge, P46–47 awards/reporting) offer substantially more than `242.50 s` of non-photo runtime while preserving impact, demolitions, withdrawal/human cost, explosion, and dock/Tirpitz outcome.
- **Alternative Chief choices:**
  1. Queue that bounded no-spend existing-VO paper recut (`£0`, target ≥50% archive on retained runtime) so `J3432` can still aim for Ben's `30 Nov 20:00Z` watch / `Thu 3 Dec` air slot without rushing; **or**
  2. Queue a bounded documentary-context allocation pass (similar to `WW2:006` `J3454`) if Chief judges additional honest photo-dominant coverage (`+121.25 s` needed) exists without violating Rule 5; **or**
  3. Record an explicit Chief editorial ruling / Rule 1 disposition or defer film 5's `Thu 3 Dec` slot (per Rule 6: never rush a film; skip the slot and tell Ben if not ready).

---

## 3. Why `J3600` Is Parked for Elected Chief

`scripts/jobs.py` restricts `jobs.py wait --recheck` (`L603–604`) and hold release (`L1094–1095`) to the **elected Chief**, and refuses `jobs.py done` on a verification job (`L1595–1598`) until the parent hold records `last_recheck == J3600` or is reopened. As `macbook` (ordinary worker, outside the Chief chain), this review parks `J3600` for the elected Chief (`codex` currently per `chief_relay.py status`, or `claude` on return).

### Ready-to-run Chief commands (if retaining the hold)

```bash
# 1. Record failed condition check on J3431 (adjust --check-at and --condition to match chosen next job)
python3 scripts/jobs.py wait J3431 --agent <chief_id> \
  --condition "Chief editorial decision required: J3449 delivered 40.400% (510.27/1263.04s), 121.25s below Rule 1 50% floor (631.52s); commission no-spend existing-VO paper recut (>=242.50s cut for >=50% share) or alternative path, resolve PR #50 status.json conflict, then accept picture stage before releasing J3432" \
  --check-at "2026-11-25T12:00:00Z" \
  --type input \
  --recheck J3600 \
  --action "Decide J3449 editorial path for WW2:005 (40.400% < 50% floor) and resolve PR #50 before accepting picture stage" \
  --git

# 2. Reopen/claim/close J3600 once wait --recheck is recorded on J3431
```

---

## 4. Scope & Guards

- **Spend:** `£0`.
- **Changes made:** Review document only (`jobs/reviews/J3600/REVIEW.md` on branch `macbook/J3600`). No merges, no Chief PASS, no picture/edit approval, no `ww2-channel` edits, no YouTube/Studio mutations, no NAS writes or deletions.
- **Perception boundary:** Text, JSON arithmetic, git diff, and NAS file/SHA-256 verification only; no moving-video or audio playback claimed.
