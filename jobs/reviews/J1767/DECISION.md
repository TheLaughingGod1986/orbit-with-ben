# J1767 — OWB 026 upload workflow FIX

3 November 2026; Codex, elected acting Chief (chief_relay status checked).

Decision: FIX the stale upload review record. Upload completion remains blocked on linked successor **J1825**, after J1767, due 14 November 18:00 London. This is a records/finish decision, not a new media PASS.

## Verified evidence

- Ben's actual comment [6337324360](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/99#issuecomment-6337324360) says: “[Ben] OK 026 v06: watched it, looks good.” Posted through the board on 22 October. J0794 records the preceding Chief media PASS; J0833 authorises the Private upload.
- Successful long upload result `PACKAGE_UPLOAD_RESULT_2026-10-22T10-03-47-020Z.json` identifies c5AdqQsnnys and CFR18 SHA-256 `6e587bb5ac33552cef55ac897d89f5516a90acef9473155254dd313fc73e09d3`, thumbnail set. Manifest distinguishes this from approved VFR v06 SHA-256 `624562255a580a3b0473db7fd9b2aec32f74156a764b65c1869525a302aa79d5`. No re-render or new media approval is inferred here.
- J0851 records the original three-Short Chief PASS and upload. J1101 has Ben's replacement approval and acting-Chief PASS. [PR313](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/313) is MERGED, 28 October 23:35:10Z, merge 8285a0cedd0c923f6e1e6730aa4c3902719bb57b. Its 61248b47d evidence includes the verified replacement master and old/new readbacks.
- Fresh read-only YouTube evidence is in LIVE_READBACK.json: all five IDs are on Orbit, processed and not made for kids. Long c5AdqQsnnys is Private for 15 November 18:00Z. Shorts HZGTovJu_TQ, cwU_0WWeNZ4 and aAUgIGEuPwQ are Private for 16/18/20 November 11:30Z. Retired A6TW_6CXhcs is Private with no publishAt. The board's old Friday ID was stale.
- CAPTIONS_READBACK.json confirms the long has only an automatic `en` ASR track, serving; the approved package's manual en-GB SRT is absent. The videos.list caption flag alone was not treated as proof.
- The successful long upload result still lists end screen/cards pending Studio. No subsequent completion evidence was found in the current queue/readbacks. Their actual Studio state is unverified, not asserted absent.

## Required continuation

J1825 installs the already-approved en-GB SRT if still absent, verifies serving status, and reads back the Studio finish items. Missing end screen/card choices return to elected Chief with exact proposed targets and timing before mutation. It does not authorise a video upload, visibility or schedule change, new media, or new Test & Compare.

J0861 remains held until the long reads Public, with next verification 15 November 18:05Z. It already targets the replacement Friday ID and owns the Related links and pinned comment. J1823 remains the separate thumbnail correction/review; thumb A is preserved and no Test & Compare is started during Shorts week. Existing Buffer timing remains unchanged.

No media was newly viewed/listened to or approved in this records repair. No YouTube state changed, no credit spent, and nothing was deleted. Mini free space was about 4 GB at start; prescribed NAS offload dry run found no scratch eligible under the 48-hour rule.
