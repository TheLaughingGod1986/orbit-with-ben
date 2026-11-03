# J1758 — FIX: cross-channel thumbnail review record

3 November 2026 · Codex, elected acting Chief (chief_relay.py status checked immediately before correction).

The OWB 004 JWST thumbnail review is a bookkeeping error, not a submitted JWST asset awaiting approval. Correct J0146 to `repo: hos` and return the erroneous OWB thumbnail state to `todo` (unverified). This decision approves only the record correction. It grants no media PASS and changes no HOS film stage, approval, hold, schedule or live test.

## Evidence

- OWB commit `131e20d83a098d1c86bc357ae830418b172f4cd7` created the JWST `status.json` when Cursor claimed **J0146 HOS 004: add thumb C v07b**. Its claim note names HOS. The other pre-J1758 status commits are J0146 block, reclaim and done (`deb6c099d`, `9745f5866`, `5aa4332c4`). No OWB thumbnail submission occurs in that history.
- J0146 was recorded `repo: owb`, `film: 004`, `stage: thumbs`, despite its HOS title and result. Its result names HOS commit `77bf286` and the Atom thumbnail variants.
- [Chief review 6119854326](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6119854326), read directly through GitHub: HOS 004 C v07b PASS; THE HIDDEN NUMBER, Te/I tiles. This is not a JWST review.
- [Chief exception 6120597964](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6120597964), read directly through GitHub: one-off J0146 permission on HOS `GHZDsiH7L7A`; no extension of that exception is made here.
- HOS commit `77bf286cdc489aaeb68dca80e55ea624624aa807` updates `004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule/TC_ARMED_2026-10-09.md`, documenting the three saved variants and screenshot paths. The recorded local screenshot directory is absent now. This correction does not assert the current Studio test state or reapprove those images.

## Resolution and verification

J0146 keeps its original completion, result and approval history, with an appended dated correction. The spurious OWB review is replaced by an explicitly unverified `todo` state and the J1758 stage claim is released. No new production or review job is warranted by a HOS task incorrectly attached to JWST; a genuine future JWST submission must carry its own assets and approval evidence.

Verify the queue difference is confined to J0146 repo/history; the board is generated from status.json; the handoff checker no longer detects the OWB:004 thumbs orphan review; all other job states and film stages are unchanged. No spend, generation, YouTube mutation or NAS deletion.
