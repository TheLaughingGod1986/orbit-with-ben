# J0985 Chief review — 26 October 2026

**Ruling: FIX.** Codex, elected acting Chief; review tracked as J1001. Original J0985 remains blocked pending correction J1002. This is a completed review decision, not an approval of the audit or any film stage. No spend or YouTube change.

## Evidence checked

Reviewed J0985 body/result/full history, audit commit `0cb8eb54a`, the 19 and 26 October reports, LEARNINGS.md, current Shorts rules, Studio source, channel daily source, UPLOADS.json, gate cache resolver and master hashes, and current swap dependencies. The audit commit contains only the report and LEARNINGS.md, not its fetched Analytics queries, retention buckets or competitor metadata. Those observations need a durable source appendix to be reproducible; this review does not independently certify competitor numbers.

Studio `05_Analytics/owb/studio_ctr.json`, readAt **2026-10-26T15:31:25Z**, period **lifetime**, confirms:

| Short | Studio views | Stayed | Average viewed | Interpretation |
|---|---:|---:|---:|---|
| vlkj8RQKmH8 | 848 | 32.1% | 76.2% | MISS / PASS; mature read |
| y-SPHQ0-VjQ | 109 | 56.8% | 78.6% | WATCH / PASS |
| 2e-giqFmfy8 | 81 | 34.3% | 58.3% | Too few to judge |
| OVLv9dxTcpE | absent | unavailable | unavailable | Launch view count cannot establish either target |

Current `channel_daily.json` sums for 17–23 October are 1,276 views / 141 minutes; 10–16 October 358 / 50; 26 September–23 October 2,664 / 397. Audit gives 1,273 / 144, 359 / 53, and 2,652 / 414. The prior week's report explicitly says **358**, not the asserted matching 359. Revisions, aggregation and rounding may explain differences: require query scope and capture times, not a silent overwrite or a declaration that every differing total is false.

## Required corrections

1. Remove causal/proven and fastest-launch claims unsupported by comparable evidence. The 5.6-hour Earth launch is preliminary; the 59-view Sun retention sample is descriptive. Existing Chief rules remain in force, independently of whether this audit proves them.
2. AVD does not locate a viewer exit or the steepest retention drop. Mercury's purported 16-second exit during a tail beginning at 17.44 seconds is also internally inconsistent. Mark its missing curve unavailable, keeping the edit timeline separate from measurements.
3. Apply the payoff threshold to the start of the answer consistently: Earth **13.80/21.84 = 63.2%**, Sun **17.92/26.34 = 68.0%**, Mercury **14.00/20.44 = 68.5%**. None reaches 70% on those stated timestamps. Resolve the claimed `1.74 <= 1.5` surprise PASS against actual word timing. These audit corrections do not authorize retroactive changes to approved/public cuts or create exceptions for new cuts.
4. Persist sanitized query parameters, timestamps, raw curves, competitor metadata/thumbnail links and cut/VO references. Keep one-page findings with detail in an appendix, at most three learning changes/tests, and distinguish 60% stayed floor from 70% stretch. No new rule promotion from this review.

## Decisions on proposed actions

- **Neptune:** J0956 remains blocked after J0988; failed loudness gate is not waived. Preserve the existing 27 October 10:30 review cutoff, upload/readback limits and scheduled-v01 fallback. J0216 stays unlinked.
- **Apophis:** J0974 remains blocked after J0990, following audio repair J0989. Preserve Ben's existing content approval, fresh exact-hash/gate review, 28 October deadlines and scheduled-v05 fallback. No duplicate swap job or renewed request for Ben's existing OK.
- **Media paths:** reject the proposed repo-copy/path repair as obsolete. The existing `gate_upcoming.staged()` resolver returns usable exports/meta for 6dcL5rBmHPM, VfDm3E2bUgU and hZH0C7fpCk4; independently hashed masters equal UPLOADS.json SHA256 respectively `6de9961ac45d70f244be5acdb8a261416752ad046cf91481673f310632842f03`, `433ce60e09d4e6c31f7f44e501cc5de9baf710dc162186ca745f041d4ad48f77`, `09e5e66332fea5ac22f07143a41a79beb6ca2b47b653276d33499946c34a2745`. Cache records are already dated 26 October 08:54–08:55Z. This verifies cache resolution/hash, not a new full-film gate PASS. Retain NAS masters and canonical paths; stage again only if a future cache misses.
- **Production:** no blanket 024–029 recut, 033 rename, new topic lock, or new generation authorized. Apply existing rules at each next production gate; proposals for 031/033/049 and ideas 062–064 need their normal script/topic evidence and review. Preserve already-approved cuts, standalone/Test A exceptions, existing Studio job ownership and the 1 November Sun test hold.

## Follow-up

J1002 (Gemini review lane) corrects the audit and OWB learnings now, then returns evidence for elected-Chief re-review of J0985. A separate read-only Earth measurement waits for a Studio capture at or after **28 October 11:30Z**; first retry **28 October 11:35 London**, then **29 October 16:00 London** if the mature source is unavailable. Neither maturity nor other-channel work blocks the corrections already possible. Queue records name the follow-up and preserve J0985's original blocked state.
