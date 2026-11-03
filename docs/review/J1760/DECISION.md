# J1760 — FIX: HOS credit block misfiled on Europa

3 November 2026 · Codex, elected acting Chief; authority verified immediately before this correction.

Return OWB 006 Europa's picture state to `todo` (unverified) and release the record-correction claim. The blocked state belongs to a historical HOS task, not to Europa. This ruling fixes bookkeeping only: no media PASS, new production order, credit permission or release change.

## Evidence

- OWB commit `6dc82a888c7686aff168c43d788a063e56675af1` created Europa's status file on 12 October when Cursor claimed **J0160: HOS 006 picture P3:06 then Part 04 plates**. Its claim note explicitly names HOS.
- Commits `11115a422`, `f5006f2cb` and `10fc880c2` block, reclaim and block the same HOS task on Europa. The last leaves `picture.state = blocked`, with no reason or next action. There is no Europa picture submission in this status history.
- Later edits affected only an independently misfiled HOS edit claim, removed in `fbcb0f813`. They did not repair the picture block.
- J0160 already has `repo: hos`, `status: done`, and the original Chief result. Its metadata and full history remain unchanged.
- [Original Chief decision 6126300569](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6126300569), retrieved directly through GitHub: four HOS Part 04 plates KEEP; brewery P3:06 FAIL for fires and style drift; further takes subject to the credit margin and Flow routing. It explicitly directs J0160 to be marked done. None of this is an Europa approval or credit hold.
- HOS merge `b019df4bf20c2f6fc720a815d6d8ccfb5c64760e` records those HOS mint logs and credit readings. The current HOS PIPELINE record is for **The Willow Tree That Was Made of Air**, with picture already recorded done. This correction neither reevaluates nor alters that film's approvals, failed-take history, holds or schedule.

## Resolution

The erroneous Europa block is replaced by an explicitly unverified `todo` state with this decision as its reference. A missing Europa approval is not treated as a PASS. No new media review or generation job is warranted by a HOS credit block attached to the wrong film; a future Europa submission needs its own evidence and normal gates. The existing HOS job result and pipeline are preserved.

Verification: generated STATUS matches the corrected status, there is no remaining picture claim or blocked/review state on OWB 006, and the change is confined to this decision, Europa's picture record and the generated board. No spend, generation, upload, visibility change or NAS deletion.

Resume verification (3 November, 21:04 UTC): Codex re-read the original HOS desk decision and source commit, verified J1872 approval, and reapplied the prepared correction onto current main in a clean worktree. Only the affected Europa record and the regenerated board are changed.
