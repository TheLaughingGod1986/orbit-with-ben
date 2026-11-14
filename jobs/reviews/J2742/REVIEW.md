# J2742 Condition Verification Report (`recheck_of: J2618`)

- **Verification Job:** `J2742` (`Verify condition for J2618`)
- **Parent Job:** `J2618` (`Decoupling, wave 2: chief_relay.py asks channels.py instead of naming a channel (79 lines, and 2 that assume a home repo, to 0)`, `status: blocked`, `by: macbook`, `needs: mini`, `kind: review`, `repo: owb`, `ref: https://github.com/TheLaughingGod1986/orbit-with-ben/pull/833`)
- **Verifier:** `macbook` (`Gemini 4 Argon (High)`, worker on the MacBook; `Codex` is currently elected Chief)
- **Checked At:** `2026-11-12T23:48Z` (`Thu 12 Nov 2026 23:48 London`)
- **Verdict:** **NOT YET MET (`HOLD` / `WAIT`) — `J2738` isolation repair and source-preservation regression coverage are delivered and verified in replacement PR `#869` (`macbook/J2738`, head `2312a8af2e2645d0b1a8984ee240d25b9c684ab7`), but elected-Chief review/merge of PR `#869` (superseding `#868` and `#833`) and the subsequent post-merge Mini relay cycle and board publish remain unfinished. Keep `J2618` blocked (`--type input --recheck J2742`, next check `2026-11-13T01:45:00Z`), or reopen `J2618` for the post-merge Mini relay cycle and board publish if the elected Chief merges `#869` in the same Chief duty pass.**
- **Spend:** `£0` (0 credits)

---

## 1. Recorded Waiting Condition on `J2618` (`2026-11-12T21:44Z`)

```text
CHANGES REQUIRED on PR868 head 16b8cc514: split dry-run placement follows destination file symlinks and overwrites original channel files; reproduced using temporary fixtures. J2738 must fix isolation and add source-preservation regression coverage, then elected Chief reviews the new head and full checks before merge. After merge observe one full Mini relay cycle and board publish before closing J2618. No merge approval; J2621/J2622 holds unchanged.
```

Remaining action recorded on `J2618`:
> *"Wait for the file-copy isolation repair in J2738, then review, merge and verify the relay and board"*

---

## 2. Element-by-Element Verification (`2026-11-12T23:48Z`)

| Requirement / Dependency | Status | Evidence Checked |
|---|---|---|
| **1. `J2738` destination-symlink isolation fix and source-preservation regression coverage** | **DELIVERED & VERIFIED IN PR `#869` (`2312a8af2e2645d0b1a8984ee240d25b9c684ab7`); AWAITING CHIEF REVIEW** | - `J2738` (*Fix split dry-run writes through destination symlinks before J2618 merge*) was completed by `macbook-2` at `2026-11-12T21:57Z` and parked (`status: blocked`, `parked for Chief`) with replacement PR **`#869`** (`macbook/J2738`, head `2312a8af2e2645d0b1a8984ee240d25b9c684ab7`), which adds commit `2312a8af2` (*Stop the studio split dry run writing through a destination symlink (J2738)*) on top of the 9 commits of PR **`#868`** (`16b8cc51447d901b0a1011482239334af6ce57d7`) / PR **`#833`** (`4ef9d89b604daf12ab252d3efb1f6b839c7fd6cf`).<br>- **Code fix (`scripts/studio_split.py`):** adds `_release_dest(dest)` to unlink any existing or dangling symlink at `dest` before `_place(src, dest)` writes or recreates a symlink, and unlinks an existing scratch regular file before `os.symlink(...)` when `src.is_symlink()`, preventing `shutil.copy2` from following a destination symlink into the real channel checkout.<br>- **Regression test (`scripts/test_studio_split.py`):** adds `Isolation.test_placing_a_channels_numbers_does_not_write_through_to_its_checkout`, sealing the simulated channel checkout read-only (`0o444`/`0o555`) and testing `split.build(...)` plus repeated `split._own_folder` + `split._place` across overlapping regular files (`05_Analytics/hos/sample.json`), nested directory symlinks (`05_Analytics/hos/nested/inner.json`), dangling symlinks (`05_Analytics/hos/dangling.json`), source symlinks (`05_Analytics/hos/via_link.json`), and same-target source symlinks (`05_Analytics/hos/same_target.json`), asserting original bytes and SHA-256 digests are unchanged and scratch files are independent non-symlinks.<br>- **Independent rebase & check verification (`2026-11-12T23:45Z–23:47Z`):** in an isolated detached worktree rebased cleanly onto `origin/main` (10 commits, `0` conflicts, rebased head `a95a47b0d`), ran `python3 -m unittest scripts/test_studio_split.py scripts/test_channel_ratchet.py scripts/test_chief_relay.py scripts/test_channels.py` (**214/214 OK**: `test_studio_split` 18/18, `test_channel_ratchet` 13/13 with `chief_relay.py` 0/0, `test_chief_relay` 113/113, `test_channels` 70/70), `python3 scripts/sync_rules.py --check` (`rules OK`), `python3 scripts/core_sync.py check` (`core OK (56 shared files)`), `python3 scripts/studio.py status --check` (`STATUS.md OK`), and `HOS_REPO=/Users/ben/_desk/worker/history-of-science python3 scripts/studio_split.py` (`studio 1771, Orbit With Ben 12118, History of Science 46, built 1`, `Tests in the new layout: run`, only `1` item remaining for `J2537` in `05_Analytics/ai_spend/ledger.jsonl`, and `git status -s` in `history-of-science` completely empty on `main`). |
| **2. Elected Chief review and merge of new head (`PR #869` `2312a8af2e2645d0b1a8984ee240d25b9c684ab7`)** | **NOT YET MET (`OPEN`, `mergedAt: null`)** | - `J2738` remains `status: blocked` (`parked for Chief`) in the Chief duty queue.<br>- `gh pr view 869`: `state: OPEN`, `mergedAt: null`, `headRefOid: 2312a8af2e2645d0b1a8984ee240d25b9c684ab7`, `latestReviews: []`, GitHub Actions `Rules check` `SUCCESS` (`2026-11-12T21:57:50Z`), `Studio core check` `SKIPPED`.<br>- Superseded PR `#868` (`16b8cc514`) and draft PR `#833` (`4ef9d89b6`) also remain `state: OPEN` (`mergedAt: null`). |
| **3. Post-merge observation of one full Mini relay cycle and board publish** | **NOT YET MET** | - Blocked behind the elected-Chief review and merge of PR `#869` into `main`. |
| **4. Original gates and `J2621` / `J2622` holds preserved** | **SATISFIED** | - `Thu 12 Nov 19:13 London` picture window remains closed (`0` active picture runs; `05_Analytics/ai_spend/ledger.jsonl` last modified `2026-11-12T18:01:16Z`).<br>- `history-of-science #535` remains merged on HOS `main` (`688046d4`), and `studio/channel.json` on HOS `main` matches `channels/hos/channel.json` on PR `#869` byte-for-byte.<br>- `J2621` (`status: blocked`) and `J2622` (`status: blocked`, held to `2026-11-13T00:45:00Z` per `J2726`; HOS PR `#548` `55b968787` draft/open) remain held unchanged. |

---

## 3. Queue Handoff for Elected Chief (`codex`)

Because `scripts/jobs.py` (`set_wait` line 529, `do_reopen` line 948, and `done` line 1426) restricts `wait --recheck J2742` and releasing a structured hold to the elected Chief (`codex`), `J2742` is parked for Chief with the two concrete options below:

### Option A — If PR `#869` is not yet merged (keep `J2618` blocked and record `--recheck J2742`)

```bash
python3 scripts/jobs.py wait J2618 --agent codex \
  --condition "J2738 isolation fix and source-preservation regression test are open and verified in PR #869 (head 2312a8af2e2645d0b1a8984ee240d25b9c684ab7 on top of PR #868; 214/214 targeted unit tests + studio_split dry run + zero HOS checkout writes verified in J2742). Still unmet: elected Chief review and merge of PR #869 (superseding #868 and #833), then observe one full Mini relay cycle and board publish before closing J2618. J2621/J2622 holds unchanged." \
  --check-at "2026-11-13T01:45:00Z" \
  --type input \
  --action "Await elected Chief review and merge of PR #869 (J2738/J2618), then observe one full Mini relay cycle and board publish before closing J2618" \
  --recheck J2742 --git && \
python3 scripts/jobs.py done J2742 --agent codex \
  --result "Verified J2618 condition at 2026-11-12T23:48Z (jobs/reviews/J2742/REVIEW.md): J2738 repair PR #869 (2312a8af2) is open and verified (destination symlink isolation fixed, Isolation test 18/18 + 214/214 targeted tests + studio_split dry run OK, HOS checkout untouched), but PR #869 is still OPEN awaiting elected-Chief review/merge plus one Mini relay cycle and board publish; updated J2618 hold (--recheck J2742, check 2026-11-13T01:45:00Z). £0." --git
```

### Option B — If the elected Chief reviews and merges PR `#869` in the same Chief duty pass (reopen `J2618` to observe the Mini relay cycle and board publish)

```bash
python3 scripts/jobs.py reopen J2618 --agent codex \
  --note "J2742 verified J2738 symlink isolation fix in PR #869 (2312a8af2, jobs/reviews/J2742/REVIEW.md) and Chief merged #869; reopen J2618 to observe one full Mini relay cycle and board publish before closing." --git && \
python3 scripts/jobs.py done J2742 --agent codex \
  --result "Verified J2618 condition met after J2738 fix in PR #869 (2312a8af2, jobs/reviews/J2742/REVIEW.md) and Chief merge; J2618 reopened for post-merge Mini relay cycle and board publish check. £0." --git
```
