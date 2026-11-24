# Condition Verification Review — J3640 (for J3430)

- **Verification Job:** `J3640` (`recheck_of: J3430`, `kind: review`)
- **Held Parent Job:** `J3430` (`WW2 film 004: edit, captions, three thumbnails and upload package, to Ben's watch`)
- **Film:** `WW2:004` (`004_Why-US-Submarine-Torpedoes-Failed-21-Months`)
- **Verifier:** `macbook` (ordinary worker; read-only verification)
- **Verified At (UTC):** `2026-11-24T23:02Z`
- **Verdict:** **CONDITION UNMET — KEEP `J3430` BLOCKED**
- **Authority Note:** `scripts/jobs.py` restricts `wait --recheck <id>` to the elected Chief (`"Only the holder or elected Chief may update this hold"` / `"Only the elected Chief may record a condition check"`). Because `macbook` is an ordinary worker outside the Chief chain, `J3640` is parked for the elected Chief to merge this evidence PR, update `J3430`'s hold with `--type input --recheck J3640`, and close `J3640`.

---

## 1. Waiting Condition Under Review

From `J3430` (`jobs/QUEUE.json`) and `J3625` (`ww2-channel` PR #113, merged at `0ebdbd4`, `07_Edit/CHIEF_RULING_J3625.md`, studio thread `#7146836105`):

> `J3625` elected-Chief ruling: `v01` HELD (not passed / not staged to `WW2 UAT/`) due to `J3624` visual QA blockers (`00:06.8` Rule 3 spoiler, tofu glyph `□` + leaked internal boilerplate on 15+ slides, 14 frozen empty-box holds of `21–38 s`, missing Chapter 3 card at `06:35.9`, 17 `<60 s` repeats, 3 `<2 s` flashes, 2 stray dips-to-black, SRT cue 253 `"a target"` -> `"the target"`). Wait for zero-spend `v02` repair (`J3637`), full `v02` private audiovisual QA (`J3638`), and elected-Chief `v02` approval & Ben-watch staging (`J3639`). Adopted Rule-2 title: `Mark 14 Torpedo: Why Perfect Hits Failed` (40 chars). Watch due `2026-11-28T20:00Z`; planned air `2026-12-01T17:00Z`.

---

## 2. Independent Evidence Checked

1. **Queue State (`jobs/QUEUE.json`, pulled at `2026-11-24T23:02Z`):**
   - `J3430`: `status: blocked`, `by: gemini`, `due: 2026-11-28T20:00:00Z`, `after: J3429` (`done`), `progress: 3/4` (`v01` rendered only; not staged to `WW2 UAT/`).
   - `J3624` (`WW2 004: full private audiovisual quality review`): `status: done` by `gemini` (`ww2-channel` PR #109, merged at `4caccb5`). Found blocking visual defects on `v01` and recommended HOLD / zero-spend `v02` repair.
   - `J3625` (`WW2 004: decide repaired delivery and stage Ben watch`): `status: done` by `gemini` as elected acting Chief (`ww2-channel` PR #113, merged at `0ebdbd4`). Held `v01`, adopted Rule-2 title `Mark 14 Torpedo: Why Perfect Hits Failed`, and queued `J3637 -> J3638 -> J3639`.
   - **`J3637`** (`WW2 004: v02 zero-spend visual/graphic repair, Rule-2 title package and render`, due `2026-11-26T12:00:00Z`): **`status: claimed` by `gemini`** (claimed `2026-11-24T22:58Z`, `eta: 2026-11-25T00:58Z`, currently at **step `1/6`** as of `2026-11-24T23:01Z` — auditing repeats/flashes/holds/Chapter 3 card and `J3447` rows). **Not done.**
   - **`J3638`** (`WW2 004: full private audiovisual QA of v02 master`, `--after J3637`, `--requires audio_input,moving_video_input`, due `2026-11-27T12:00:00Z`): **`status: open`**, unclaimed, waiting on `J3637`. **Not done.**
   - **`J3639`** (`WW2 004: Chief decision on v02 delivery and stage Ben watch`, `--after J3638`, due `2026-11-28T12:00:00Z`): **`status: open`**, unclaimed, waiting on `J3638`. **Not done.**
2. **`ww2-channel` Repo & PR State (`main` at `0ebdbd4`):**
   - `02_Video-Projects/004_Why-US-Submarine-Torpedoes-Failed-21-Months/07_Edit/CHIEF_RULING_J3625.md` and `status.json` are on `main` (`0ebdbd4`), preserving all 6 prior `done` stages (`topic`, `script`, `sources`, `vo`, `shots`, `picture`), `edit: doing` waiting on `J3637 -> J3638 -> J3639`, and adopted title `Mark 14 Torpedo: Why Perfect Hits Failed`.
   - Checked `gh pr list --state all --limit 15` on `ww2-channel`: no `v02` repair PR (`J3637`) or `v02` audiovisual QA PR (`J3638`) exists yet (latest PRs are `#113` `J3625` Chief ruling and `#114` unrelated `WW2:009` `J3636`).
3. **NAS `studio-live` & `WW2 UAT/` Check:**
   - Checked `/Volumes/data/studio-live/ww2/02_Video-Projects/004_Why-US-Submarine-Torpedoes-Failed-21-Months/07_Edit`: contains only `J3430_prep_v01` and `v01_master`. No `v02_master` directory or `ww2_004_torpedoes_v02.mp4` exists yet.
   - Checked Ben's `WW2 UAT/` folder: contains `001`, `002`, `003`, and `00_Channel-Kit` only — no `004_Why-US-Submarine-Torpedoes-Failed-21-Months` folder staged (correctly absent while `v01` is held).
4. **Studio Thread Read (`studio_thread.py status` / `read`):**
   - Read to `#7146836105` (`[Chief] [Gemini]` `J3625` ruling at `2026-11-24T22:57:05Z`). No superseding Chief decision or Ben approval overrides the `v01` HOLD.

---

## 3. Root Cause of Premature `J3640` Trigger

`J3625` recorded `J3430`'s hold at `2026-11-24T22:54Z` with `next verification 2026-11-28T12:00:00Z`, but used `--type dependency` (with no `last_recheck`). Because `J3430` still carries its legacy `"after": "J3429"` (which is `"done"`), `scripts/workflow_state.py:132-134` (`hold_due`) evaluates:

```python
if hold.get("type") == "dependency" and not hold.get("last_recheck"):
    if j.get("after") and by_id.get(j["after"], {}).get("status") == "done":
        return True
```

This caused the relay to queue `J3640` two minutes later (`22:56Z`) and overwrite `check_at` with `+1h`. Recording the updated hold with **`--type input`** and **`--recheck J3640`** prevents another premature trigger while keeping `J3430` safely blocked until `2026-11-28T12:00:00Z` (or until `J3639` completes earlier and stages `J3430 awaits` directly).

---

## 4. Recommended Action for Elected Chief

1. Merge this evidence PR (`macbook/J3640`) to `orbit-with-ben` `main`.
2. Keep `J3430` blocked and record the verified hold (retaining `J3625`'s original retry time `2026-11-28T12:00:00Z`, 8 hours before Ben's watch deadline `2026-11-28T20:00:00Z`):
   ```bash
   python3 scripts/jobs.py wait J3430 --agent <elected-chief-id> \
     --condition "J3625 elected-Chief ruling (ww2 PR #113, 0ebdbd4): v01 HELD (not passed/not staged to WW2 UAT) due to J3624 visual QA blockers. Wait for zero-spend v02 repair (J3637, claimed by gemini step 1/6, due 2026-11-26T12:00Z), full v02 private audiovisual QA (J3638, open after J3637, due 2026-11-27T12:00Z), and elected-Chief v02 approval & Ben-watch staging (J3639, open after J3638, due 2026-11-28T12:00Z). Adopted Rule-2 title: Mark 14 Torpedo: Why Perfect Hits Failed (40 chars). Watch due 2026-11-28T20:00Z; planned air 2026-12-01T17:00Z." \
     --check-at "2026-11-28T12:00:00Z" \
     --type input \
     --recheck J3640 \
     --action "Hold J3430 pending v02 zero-spend visual repair (J3637), v02 full audiovisual QA (J3638), and Chief v02 watch staging (J3639)" \
     --git
   ```
3. Close `J3640` with `jobs.py done J3640 --agent <elected-chief-id> --result "..." --git`.

---

## 5. Guards Confirmed

- £0 spent; no VO, generation, render, upload, schedule change, or `WW2 UAT/` copy performed.
- No files modified on NAS or in `ww2-channel` / `history-of-science`.
- Ben's approval requirement before any upload remains intact.
