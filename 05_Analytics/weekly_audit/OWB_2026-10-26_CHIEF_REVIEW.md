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

## J1044 Acting-Chief Condition Verification (27 October 2026)

**Verified by:** Gemini (`gemini`, elected acting Chief under Ben's 26 Oct 2026 order while Grok, Claude and Codex are down).

1. **Predecessor `J1002` (`45ef75589`) verified complete (`5/5` steps):**
   - **Item 1 (Studio readings & small-sample/preliminary framing):** Verified `05_Analytics/owb/studio_ctr.json` (`readAt: 2026-10-26T15:31:25Z`, `period: lifetime`) in `OWB_2026-10-26.md` and `OWB_2026-10-26_EVIDENCE.md`: `vlkj8RQKmH8` (`848` Studio / `849` live views, `32.1%` stayed `MISS`, `76.2%` avg viewed `PASS`), `y-SPHQ0-VjQ` (`109` views, `56.8%` stayed `WATCH`, `78.6%` avg viewed `PASS`), `2e-giqFmfy8` (`81` Studio / `59` YTA views, `34.3%` stayed, `58.3%` Studio / `62.1%` YTA viewed — `<100` Studio views, explicitly labeled *too few to judge / descriptive only, not causal proof*), and `OVLv9dxTcpE` (absent from `15:31:25Z` Studio read; `5.6 h` `832` live views treated as preliminary only, with mature 48h Studio read tracked in `J1003` at `≥28 Oct 11:30Z`). Standing Chief rules are explicitly separated from this week's observations.
   - **Item 2 (AVD / missing curves / edit timelines):** Verified all AVD/swipe-share exit inferences are removed; `vlkj8RQKmH8` and the 8 other curveless Shorts are marked `Biggest drop: Unavailable (no YTA curve)` (`0:16` AVD noted as a mean duration across views preceding the `17.44–20.44 s` silent tail, not a viewer exit timestamp), and edit timelines are kept separate from measured 100-point YTA curves across `OWB_2026-10-26.md`, `OWB_2026-10-26_EVIDENCE.md`, and `05_Analytics/LEARNINGS.md`.
   - **Item 3 (Payoff-start math & surprise-word timing):** Verified start-of-answer payoff ratios against `0.70 × runtime`: Earth `OVLv9dxTcpE` `13.80 / 21.84 = 63.2% < 70%` (`13.28 / 21.50 = 61.8%` in `earth_sudden_air_v05_meta.json`), Sun `y-SPHQ0-VjQ` `17.92 / 26.34 = 68.0% < 70%`, Mercury `vlkj8RQKmH8` `14.00 / 20.44 = 68.5% < 70%` — all three marked `FAIL` on start-of-answer timing (answer completion does not pass the start check). Verified exact `OVLv9dxTcpE` word timestamps (`"stops"` `0.84–1.10 s ≤ 1.50 s`, `"turning"` `1.16–1.68 s > 1.50 s` [`1.74 s` prior table], `"instant"` `1.96–2.50 s > 1.50 s`) and pre-Keeper build date (`25 Oct 2026`) with no retroactive recut or new exemption.
   - **Item 4 (Reproducible sanitized evidence & window reconciliation):** Verified `05_Analytics/weekly_audit/evidence_2026-10-26_owb_reconciled.json` (zero secrets, valid JSON, 15 window reconciliations, 35 retention curve queries, 5-channel 30-day vs back-catalogue competitor metadata and thumbnail URLs). Confirmed exact day-level reconciliation against `05_Analytics/owb/channel_daily.json` and `OWB_2026-10-19.md`: `17–23 Oct` (`1,276` cached / `141` min vs `1,273` live YTA / `140` day-sum / `144` un-dim min due to `2026-10-19` `84/25 → 81/24` revision), `10–16 Oct` (`358` cached & in `OWB_2026-10-19.md` / `50` day-sum min vs `359` live YTA / `53` un-dim min due to `2026-10-16` `87 → 88` revision), and `26 Sep–23 Oct` (`2,664` cached / `397` min vs `2,652` live YTA / `400` day-sum / `414` un-dim min). Generated tracker files remain untouched.
   - **Item 5 (One-page summary & bounded tests):** Verified `OWB_2026-10-26.md` is compressed to a one-page decision summary with detailed tables in `OWB_2026-10-26_EVIDENCE.md`, `60%` stayed floor (`70%` stretch) and `70%` average-viewed targets kept distinct, 3 bounded cohort tests named, and no new rule promoted to `proven`.
   - **Item 6 (Current queue owners & stage caches):** Verified current owners and holds are recorded (`J0956` after `J0988`, `J0974` after `J0990`/`J0989`, `1 Nov` Sun hold, no blanket `024–029` recut / `033` rename / `062–064` topic lock). Re-verified `gate_upcoming.staged()` live against `00_Brand/Channel-Setup/social/UPLOADS.json` and `~/_desk/cache/gate-media`: all three staged caches (`6dcL5rBmHPM` `6de9961a...`, `VfDm3E2bUgU` `433ce60e...`, `hZH0C7fpCk4` `09e5e663...`) resolve and match master SHA256.
2. **Queue disposition (`J0985` & `J1044`):**
   - `J0985` is a completed 5/5 worker job (`owb-weekly-audit`) authored by `gemini`, and `J1002` (`45ef75589`, also authored by `gemini`) explicitly requires `never self-approve J0985`. Furthermore, reopening `J0985` to `"status": "open"` would clear its `5/5` progress and re-queue the weekly audit worker run from step 0, while closing it prematurely before `J1003` would free `refill.py` (`busy("owb-weekly-audit")`).
   - Therefore, `J0985` is kept `blocked` via `jobs.py wait J0985 --recheck J1044` (6-hour retry `2026-10-28T02:05:00Z`; mature Earth Short `OVLv9dxTcpE` 48h follow-up `J1003` scheduled at `2026-10-28T11:35:00Z`), recording that `J1002` (`45ef75589`) is verified complete and `J0985` awaits non-author Chief (`chief`/`claude`/`codex`) closure. No spend, upload, or schedule change.

## J1003 Mature Earth Short Measurement (30 October 2026)

**Completed by:** Gemini (`gemini`, worker on `J1003`; no final Chief OK/PASS on `J0985`).

1. **First Post-48h Studio Lifetime Capture (`05_Analytics/owb/studio_ctr.json`, `readAt: 2026-10-29T07:13:31.819902Z`, `period: lifetime`, commit `022575da5` / `J1179`, SHA256 `7568944bf7424220523a74136121f23d91d5835850e7385a8f12113f1329e1b2`):**
   - `OVLv9dxTcpE` released at `2026-10-26T11:30:15Z` (scheduled `11:30:00Z`; 48h threshold `2026-10-28T11:30:00Z`). The `2026-10-28T07:51:04.461913Z` capture (`44h 21m`) fell below 48 hours and was excluded.
   - At `2026-10-29T07:13:31.819902Z` (`67h 43m` post-release), `OVLv9dxTcpE` recorded **`887` Studio views** (`≥ 100` views), **`30.7%` `stayedToWatch`** (`69.3%` swiped -> **`MISS`** vs `60%` floor / `70%` stretch), and **`75.3%` `avgViewPct`** (`avgViewSeconds: 16` s -> **`PASS`** vs `70%` target).
   - Same capture for comparison Shorts: `vlkj8RQKmH8` (`850` Studio views, `32.1%` `stayedToWatch` `MISS`, `76.1%` `avgViewPct` `PASS` / `15 s` AVD), `y-SPHQ0-VjQ` (`109` Studio views, `56.8%` `stayedToWatch` `WATCH`, `78.6%` `avgViewPct` `PASS` / `21 s` AVD).
2. **Separate Reporting Windows (YTA `2026-10-18..2026-10-28` vs Live Data API v3 `2026-10-30T07:05Z`):**
   - `OVLv9dxTcpE`: **`887` YTA views** (all on `2026-10-26`), `90` min, `281` engaged views, `16 s` AVD, `75.33%` avg viewed, `6` likes (`SHORTS` `873` = `98.4%` **FED**, `YT_SEARCH` `8`, `YT_OTHER_PAGE` `5`, `NOTIFICATION` `1`); **`891` live Data API v3 views & `7` likes** (`29–30 Oct`).
   - `vlkj8RQKmH8`: **`851` YTA views** (`847` on `24 Oct`, `2` on `25 Oct`, `2` on `26 Oct`), `89` min, `286` engaged views, `15 s` AVD, `76.07%` avg viewed, `5` likes (`SHORTS` `810` = `95.2%` **FED**); **`851` live views & `5` likes**.
   - `y-SPHQ0-VjQ`: **`109` YTA views**, `19` min, `52` engaged views, `21 s` AVD, `78.59%` avg viewed, `1` like (`YT_SEARCH` `79` = `72.5%`, `SHORTS` `25` = `22.9%`); **`109` live views & `1` like**.
3. **100-Bucket Retention Curve & Cut/VO Mapping (`endDate: 2026-10-28`, stored in `evidence_2026-10-26_owb_reconciled.json`):**
   - `OVLv9dxTcpE` (`887` YTA views): steepest single-bucket drop is **`0.20->0.21` (`4.30–4.51 s` on `21.50 s` `meta.json` / `4.37–4.59 s` on `21.84 s`: `115.66% -> 110.68%`, `−4.98 pp`)**, preceded by **`0.19->0.20` (`4.08–4.30 s`: `119.57% -> 115.66%`, `−3.91 pp`)**, falling **`−20.99 pp` across `0.19->0.26` (`4.08–5.59 s`: `119.57% -> 98.58%`)** during restatement sentence 2 (*"Nothing has told it to stop"*, `3.92–5.32 s`) over `s02_iss` (`2.50–5.48 s`). Holds **`58.36% -> 42.35%` across `13.12–21.50 s`** (`90.64%` relative retention at `21.50 s`) during the equator payoff (`s06_air` `13.28–16.73 s`, `s07_spin` `16.73–20.18 s`, `s08_loop_epic` `20.18–21.48 s`).
   - `vlkj8RQKmH8` (`851` YTA views, settled curve now returned by YTA): steepest single-bucket drop is **`0.18->0.19` (`3.68–3.88 s`: `128.08% -> 122.33%`, `−5.76 pp`)**, falling **`−29.26 pp` across `0.16->0.23` (`3.27–4.70 s`: `133.96% -> 104.70%`)** across `s01 -> s02_orbit` (`3.60 s`).
4. **Descriptive 3-Short Comparison (No Causal Proof):**
   - Reported in `OWB_2026-10-26.md` §1–2, `OWB_2026-10-26_EVIDENCE.md` §1A/§2/§3, and `05_Analytics/LEARNINGS.md` (Learnings #1, #2, #3, #6, #7 and `## Shorts lab`). Both `OVLv9dxTcpE` (`98.4%` Shorts feed) and `vlkj8RQKmH8` (`95.2%` Shorts feed) achieved **`PASS`** on `avgViewPct` (`75.3%` and `76.1%`) while missing the `60%` `stayedToWatch` floor (`30.7%` and `32.1%`); `y-SPHQ0-VjQ` (`56.8%` `stayedToWatch`, `78.6%` `avgViewPct`) drew `72.5%` of its `109` views from YouTube Search. Because the three Shorts differ simultaneously in traffic source, runtime, format, and open type, no causal or proven rule conclusion is drawn from this 3-Short comparison.


