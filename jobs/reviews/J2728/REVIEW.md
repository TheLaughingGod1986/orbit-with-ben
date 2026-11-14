# J2728 Condition Verification — J2649 (`Relay: a condition check for a job pinned to the Mini goes to the Mini, not the MacBook`)

- **Verification Job:** `J2728` (`Verify condition for J2649`)
- **Parent Job:** `J2649` (`Relay: a condition check for a job pinned to the Mini goes to the Mini, not the MacBook`, `status: blocked`, `by: claude`, `needs: cloud`, `for: claude`, `kind: studio`, `repo: owb`)
- **Verifier:** `macbook-2` (`Gemini 4 Argon (High)`, worker on the MacBook; `Codex` is currently elected Chief)
- **Checked At:** `2026-11-12T20:13Z` (`Thu 12 Nov 2026 20:13 London`)
- **Verdict:** **CONDITION NOT YET MET (`1 of 2` satisfied; keep `J2649` blocked until `orbit-with-ben #833` merges onto `main`)**
  1. **SATISFIED:** `Thu 12 Nov 19:13 London` picture window is closed (`20:13 London` / `20:13Z`, 60 minutes past `19:13 London`) with no active pre-window Flow run.
  2. **UNMET:** `orbit-with-ben #833` (`claude/youtube-channel-audit-pa4n3b`, head `4ef9d89b604daf12ab252d3efb1f6b839c7fd6cf`) is still `OPEN` (`isDraft: true`, `mergedAt: null`). Its three parent jobs (`J2618`, `J2621`, `J2622`) have had their post-`19:13 London` readiness verified in `J2724` (PR `#859`), `J2725` (PR `#860`), and `J2726` (PR `#861`), which are queued in the Chief duty inbox for the elected Chief (`codex` / `claude`) to reopen and merge `#833`. Because `J2649` explicitly requires building on top of `#833` once `#833` is merged into `main`, `J2649` remains blocked until `#833` merges.
- **Scope:** Verification task only (`£0` spend).

---

## 1. Recorded Waiting Condition and History on `J2649`

Recorded hold on `J2649`:
```text
Thu 12 Nov 19:13 London, when the picture window closes and 833 (which rewrites much of the relay) merges. This change goes on top of it
```

Recorded history on `J2649`:
- `2026-11-11T21:18Z` (`claude`): `added for claude`
- `2026-11-11T21:20Z` (`claude`): `not before the picture window closes: the relay wakes every worker on the Mini, and 833 already rewrites much of chief_relay.py and is held until then. This change is built on top of 833 once it is merged`
- `2026-11-11T21:20Z` (`claude`): `blocked: Waiting for: Thu 12 Nov 19:13 London, when the picture window closes and 833 (which rewrites much of the relay) merges. This change goes on top of it`
- `2026-11-11T21:20Z` (`claude`): `condition recorded; next verification 2026-11-12T19:30:00Z`
- `2026-11-12T19:40Z` (`relay`): `condition verification queued: J2728`

Recorded `remaining_action` on `J2649`:
> *"After 833 merges: condition checks take `needs` from the job they check; tests; pull request"*

---

## 2. Element-by-Element Verification (`2026-11-12T20:13Z`)

| Requirement / Gate | Status | Evidence Checked |
|---|---|---|
| **1. Picture window closed (`Thu 12 Nov 19:13 London` / `19:13Z`)** | **SATISFIED** | Checked at `2026-11-12T20:13Z` (`20:13 London`, GMT / `UTC+0`), 60 minutes after the `19:13 London` window closed. Per `J2720` (`#6832174516`), Chief rulings `#6831924778` & `#6831945212`, and `J2724`/`J2725`/`J2726` (PRs `#859`, `#860`, `#861`), all pre-`19:13Z` Flow picture runs stopped prior to the window close. |
| **2. `orbit-with-ben #833` merged into `main`** | **UNMET** | `gh pr view 833 --json number,state,mergedAt,mergeCommit` at `2026-11-12T20:08:53Z` returns `state: "OPEN"`, `mergedAt: null`, `mergeCommit: null` (branch `claude/youtube-channel-audit-pa4n3b`, head `4ef9d89b604daf12ab252d3efb1f6b839c7fd6cf`, `Rules check: SUCCESS`). Predecessor condition checks `J2724` (PR `#859`), `J2725` (PR `#860`), and `J2726` (PR `#861`) verified all pre-merge gates for `#833` (`J2618`, `J2621`, `J2622`) and are waiting in the Chief duty queue (`Chief duties: J2716, J2721, J2724, J2725, J2726, J2683, J2665`) for the elected Chief to reopen `J2618`/`J2621`/`J2622` and merge `#833`. |
| **3. Original scope & readiness for `J2649` after `#833` merges** | **VALID** | Confirmed on `J2535` (`recheck_of: J2449`), `J2569` (`recheck_of: J0275`), and `J2647` (`recheck_of: J2449`): all three parent jobs had `needs: "mini"` and `mini_only: true`, while `reconcile_holds` (`scripts/jobs.py` line 634, invoked from `scripts/chief_relay.py` via `jobs.py reconcile --git`) created each `"Verify condition for ..."` task with `needs="any"` and no pin. Once `#833` merges onto `main`, `J2649` is ready to build on top of it (`£0`). |

---

## 3. Queue Handoff for Elected Chief (`codex` / `claude`)

Because `scripts/jobs.py` restricts both `set_wait(..., recheck=...)` (lines 517 and 530: `Only the holder or elected Chief may update this hold` / `Only the elected Chief may record a condition check`) and `do_reopen` (line 948: `Only the elected Chief may release a verified hold`) to the elected Chief, and closing `J2728` (`recheck_of: "J2649"`) requires updating or releasing `J2649`'s hold first (line 1426), `J2728` is parked for the elected Chief (`codex`, or `claude` after `21:50Z`):

### Option A — If `#833` has NOT yet been merged when the Chief processes `J2728`:
Keep `J2649` blocked on its input hold (`orbit-with-ben #833` merged into `main`) with next check at `2026-11-12T22:00:00Z` (just after Claude's `21:50Z` usage window and after the `J2724`/`J2725`/`J2726` Chief duty pass):

```bash
python3 scripts/jobs.py wait J2649 --agent codex \
  --condition "orbit-with-ben #833 (head 4ef9d89b6, J2618/J2621/J2622) merged into main. The Thu 12 Nov 19:13 London picture window is closed and J2724/J2725/J2726 (PRs #859/#860/#861) verified #833 ready to merge; J2649 builds on top of #833 once merged" \
  --check-at "2026-11-12T22:00:00Z" \
  --type input \
  --action "After 833 merges: condition checks take needs from the job they check; tests; pull request" \
  --recheck J2728 \
  --git

python3 scripts/jobs.py done J2728 --agent codex \
  --result "Verified J2649 condition at 2026-11-12T20:13Z (jobs/reviews/J2728/REVIEW.md): 19:13 London picture window is closed, but OWB #833 (4ef9d89b6) is still OPEN awaiting Chief merge after J2724/J2725/J2726. Updated J2649 hold (--recheck J2728, next check 2026-11-12T22:00:00Z). £0." \
  --git
```

### Option B — If the Chief merges `#833` first in the same duty pass (after `J2724`/`J2725`/`J2726`):
Once `#833` is merged into `main`, both halves of `J2649`'s condition are satisfied and the Chief may reopen `J2649` directly:

```bash
python3 scripts/jobs.py reopen J2649 --agent codex \
  --note "J2728 verified 19:13 London window closed (jobs/reviews/J2728/REVIEW.md) and OWB #833 is now merged on main; ready to build J2649 on top of #833." \
  --git

python3 scripts/jobs.py done J2728 --agent codex \
  --result "Verified J2649 waiting condition met (jobs/reviews/J2728/REVIEW.md) after 19:13 London window close and OWB #833 merge; J2649 reopened. £0." \
  --git
```
