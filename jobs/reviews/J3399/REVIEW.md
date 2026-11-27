# J3399 — Review Earth Equator Short Private/Schedule Discrepancy (`emwQsPxnRGM` vs `Dm4xsF1Ateg`)

- **Job:** `J3399` (`027 / upload`, `kind: review`)
- **Reviewer:** `macbook-2` (MacBook worker; read-only Studio check + records reconciliation)
- **Date:** `2026-11-24T12:12Z`
- **Channel:** Orbit With Ben (`UC_esArsDKd3GJvOkeO0DUog`)
- **Film / Stage:** `OWB:027` (*What If Earth Stopped Spinning?*, long `6bbbvfCx6zY`) — `upload`
- **Verdict:** **INTENTIONALLY PRIVATE / SUPERSEDED — NO PUBLISHING ACTION NEEDED**

---

## 1. Determination

`emwQsPxnRGM` (*Why Do You Weigh Less at Earth's Equator?*, `earth_equator_weight_v01`, 24 s) is **intentionally Private and unscheduled**. It is neither missing its intended slot nor carrying an unseen schedule.

On **5 November 2026**, after Ben's board OK and review-lane KEEP (`J2214`), job `J1100` (PR `#565`, commit `7d943c181`) uploaded the approved `v07` replacement cut as **`Dm4xsF1Ateg`** (`earth_equator_weight_v07`, 23 s) into the exact **Monday 23 November 2026 11:30 London (`2026-11-23T11:30:00Z`)** slot and intentionally unscheduled `emwQsPxnRGM` (leaving it Private per the Never list: never delete a video).

`Dm4xsF1Ateg` went Public on schedule at `2026-11-23T11:30:10Z`, had its missing Related video repaired to `6bbbvfCx6zY` by `J3439` (PR `#1221`, commit `b36198ea67`), and passed the `J3462` live listing audit (`05_Analytics/live_fixes/2026-11-24.md`, 10/10 pass).

**Root cause of the J3397 discrepancy:** `J0317`'s brief pre-dated the 5 Nov `J1100` swap and still cited `emwQsPxnRGM` with its pre-swap prose (`publishAt Monday 23 November 2026 11:30 London`). When `J0317` ran on 22 Nov (`jobs/readbacks/J0317.json`, PR `#1199`), Studio truthfully returned `VIDEO_PRIVACY_PRIVATE` with `scheduled_publishing_details: null` on the retired `emwQsPxnRGM`.

---

## 2. Reconciled Chronology & Records Evidence

| Date (UTC) | Job / Source | Concrete Evidence |
|---|---|---|
| `2026-10-22 22:30` | `J0853` (`J0853_READBACK.json`, `PACKAGE_UPLOAD_RESULT_2026-10-22T22-30-50-415Z.json`) | Original `earth_equator_weight_v01.mp4` (sha256 `9781e967acb55cc99418197a90f147184b2ea900927a176bbd40292d46f77767`, 24 s) uploaded as `emwQsPxnRGM`, Private, `publishAt: 2026-11-23T11:30:00Z`. |
| `2026-10-23` – `2026-11-05` | Daily snapshots (`05_Analytics/owb/snapshots/2026-10-23.json`..`2026-11-05.json`) | `emwQsPxnRGM` tracked as `privacy: private`, `publishAt: 2026-11-23T11:30:00Z`. |
| `2026-10-25` – `2026-11-05` | `J0936` / `J1032` / `J1100` / `J2214` (`jobs/reviews/J2214/REVIEW.md`) | Batch C re-cut fixed Ben's 28 Oct VO note (`v04` -> `v07`: single-take question pickup, instrumental-only bed cleared by ear/ASR, caption-free 1 s loop tail). `earth_equator_weight_v07.mp4` (sha256 `7d07deafbd4e242384aa35ffc8bf10d670c5e1f961c1f0c2ecc2b2159ea9c649`, 22.97 s) passed all automated gates and received `J2214` **KEEP** (`2026-11-05T12:37Z`) and Ben's board OK (`2026-11-05 12:52–12:53 London`). |
| `2026-11-05 23:38–23:40` | `J1100` swap (`v07-J1100/PACKAGE_UPLOAD_RESULT_2026-11-05T23-38-06-882Z.json`, `jobs/readbacks/J1100.json`, PR `#565` / `7d943c181`) | Uploaded replacement `Dm4xsF1Ateg` (`replaces: "emwQsPxnRGM"`) Private with `publishAt: 2026-11-23T11:30:00Z`. Unscheduled `emwQsPxnRGM` (`unscheduledAt: 2026-11-05T23:39:58Z`, `supersededBy: Dm4xsF1Ateg`). `jobs/readbacks/J1100.json` (`ok: true`, `problems: []`) verified `emwQsPxnRGM` = `private / publishAt: null` and `Dm4xsF1Ateg` = `private / publishAt: 2026-11-23T11:30:00Z`. `library.json` marked `emwQsPxnRGM` `retired` and added `Dm4xsF1Ateg`. |
| `2026-11-06` – `2026-11-23` | Daily snapshots (`2026-11-06.json`..`2026-11-23.json`) & `BUFFER_POSTS.json` | Every snapshot shows `emwQsPxnRGM` `private / publishAt: null` (0 views) and `Dm4xsF1Ateg` `private / publishAt: 2026-11-23T11:30:00Z`. Buffer mirrored only `Dm4xsF1Ateg` (IG `6afbfcb01fd23f2544491848`, FB `6afbfcb139b610d5918fbc82`, Threads `6afbfcb21fd23f254449208c`) for `2026-11-23T11:30:00.000Z`; zero Buffer posts exist for `emwQsPxnRGM`. |
| `2026-11-22 23:06` | `J0317` (`jobs/readbacks/J0317.json`, PR `#1199`) & `J3397` (`jobs/reviews/J3397/REVIEW.md`) | `J0317` executed against its pre-swap target list (`OVLv9dxTcpE` and `emwQsPxnRGM`), setting Related -> `6bbbvfCx6zY` on both and recording `emwQsPxnRGM` Private with `scheduled_publishing_details: null`. `J3397` flagged that discrepancy and queued `J3399`. |
| `2026-11-23 11:30–17:59` | `J3438` (`05_Analytics/owb/launch/Dm4xsF1Ateg.json`) & `J3439` (`jobs/readbacks/J3439.json`, PR `#1221` / `b36198ea67`) | `Dm4xsF1Ateg` went Public on schedule (`2026-11-23T11:30:10Z`). Six-hour check `J3438` caught `Related: None` (because `J0317` had targeted superseded `emwQsPxnRGM`). `J3439` repaired `Dm4xsF1Ateg` Related -> `6bbbvfCx6zY` at `17:47:18Z`, reconciled `UPLOADS.json`, and queued 24-hour reach follow-up `J3444` (`>= 2026-11-24T11:30:00Z`). |
| `2026-11-24 05:05–05:09` | `J3462` (`05_Analytics/live_fixes/2026-11-24.md`) & `2026-11-24.json` snapshot | Confirmed `Dm4xsF1Ateg` Public (`2026-11-23T11:30:10Z`, 28 views at snapshot), live Related pill = `6bbbvfCx6zY`, description byte-exact vs `v07-J1100/PACKAGE_MANIFEST.json`, all source/parent URLs HTTP 200; 10/10 pass, 0 live fixes. |
| `2026-11-24 11:56` | `J0996` (PR `#1249`, open for Chief merge) | Completed `OVLv9dxTcpE` matching-long description prepend on Mini (`560 -> 665` bytes) and released `027/upload`. |

---

## 3. Fresh Read-Only Studio Verification (`2026-11-24T12:12Z`)

- **Competing-writer check:** Queue claims verified before browser access — only `J3399` (`macbook-2`, `027/upload`), `J3520` (`macbook`, `064/script` review), and `J3528` (`gemini`, Mini condition check) were claimed. Zero competing Studio writers.
- **Route & browser hygiene:** MacBook Orbit Studio CDP port `9223` via `scripts/cdp_tabs.py` (`reuse_page(ctx, "studio.youtube.com")`). Single existing tab `1CB5D1BF23FE5973DCFB1E92839CC4AC` reused (`tabs_before == tabs_after == 1`, Chrome left running, zero clicks/saves, `save_disabled: true`, `undo_disabled: true`).
- **Channel identity verified:** `Orbit With Ben` (`UC_esArsDKd3GJvOkeO0DUog`) on dashboard at `2026-11-24T12:12:33.401Z`.
- **Readback receipt:** `jobs/readbacks/J3399.json`.
  - **`emwQsPxnRGM`** (`12:12:37.620Z`, screenshot `~/_desk/tmp/j3399/J3399_emwQsPxnRGM_readonly.png`, sha256 `866dfb022be0c487470342341736df618dd009c8f6eeaee67ef05c92043d58f5`):
    - `privacy`: `VIDEO_PRIVACY_PRIVATE`, `visibility_text`: `Visibility\nPrivate`
    - `scheduled_publishing_details`: `null`, `time_published_seconds`: `"0"`, `time_created_seconds`: `"1792708244"` (`2026-10-22T22:30:44Z`)
    - `length_seconds`: `"24"`, `related_video_id`: `"6bbbvfCx6zY"`, `description_sha256`: `c47030b30985b05c92b4721316a94f3dcc42309245cdd4d7814c1539d01a850d`
  - **`Dm4xsF1Ateg`** (`12:12:42.279Z`, screenshot `~/_desk/tmp/j3399/J3399_Dm4xsF1Ateg_readonly.png`, sha256 `564fc3c5921fd8781b7b222a7c23a01dd7c8ee7ec458976f7b334f8666b1668d`):
    - `privacy`: `VIDEO_PRIVACY_PUBLIC`, `visibility_text`: `Visibility\nPublic`
    - `scheduled_publishing_details`: `null`, `time_published_seconds`: `"1795433410"` (`2026-11-23T11:30:10Z`), `time_created_seconds`: `"1793921875"` (`2026-11-05T23:37:55Z`)
    - `length_seconds`: `"23"`, `related_video_id`: `"6bbbvfCx6zY"`, `description_sha256`: `c47030b30985b05c92b4721316a94f3dcc42309245cdd4d7814c1539d01a850d`

---

## 4. Internal Record Corrections Made (Supported by Concrete Evidence)

1. **`jobs/readbacks/J3399.json`** — Added fresh read-only MacBook CDP 9223 readback receipt for `emwQsPxnRGM` and `Dm4xsF1Ateg`.
2. **`jobs/reviews/J3399/REVIEW.md`** — Recorded full discrepancy reconciliation and evidence chain.
3. **`00_Brand/Channel-Setup/social/UPLOADS.json`** (`emwQsPxnRGM` only) — Corrected stale `"relatedStatus": "pending_studio"` to `"relatedStatus": "set"`, `"relatedVideoId": "6bbbvfCx6zY"`, `"relatedReadbackAt": "2026-11-24T12:12:37Z"` while preserving `"publishAt": null`, `"privacyStatus": "private"`, `"relatedJob": "J0317"`, `"supersededBy": "Dm4xsF1Ateg"`, and `"unscheduledAt": "2026-11-05T23:39:58Z"`. (`Dm4xsF1Ateg` was already accurately recorded by `J3439`; `OVLv9dxTcpE` and historical package manifests untouched.)
4. **`00_Brand/Channel-Setup/audits/shorts_open_library/library.json`** (`Dm4xsF1Ateg` only) — Updated via `gate_shorts_open.py status --id Dm4xsF1Ateg --status live` from `"scheduled"` to `"live"` (matching its `2026-11-23T11:30:10Z` live public status; `emwQsPxnRGM` remains `"retired"`).

---

## 5. Exact Intended Next Action & Explicit Owner (`027 / upload`)

- **Publishing action on `emwQsPxnRGM`:** **NONE.** Keep `emwQsPxnRGM` Private and unscheduled (superseded `v01`; never delete per Never list). Do not queue any scheduling or privacy change.
- **Publishing action on `Dm4xsF1Ateg`:** **NONE.** Live Public replacement with verified Related `6bbbvfCx6zY` and passing live listing audit (`J3462`).
- **Remaining `027 / upload` handoffs and owners:**
  1. **Elected Chief (`claude` / active Chief chain):** Review and merge this `J3399` reconciliation PR (`macbook/J3399`) and open `J0996` PR `#1249` (`OVLv9dxTcpE` description prepend + manifest sync).
  2. **Review lane -> Studio worker (`J3514` -> `J3444`, already queued):** `J3514` (open) verifies the `>= 2026-11-24T11:30:00Z` condition on `J3444` (`027 / upload`) so `J3444` can run the 24-hour read-only reach check on `Dm4xsF1Ateg`.

---

## 6. Guards Verified

- Zero YouTube uploads, schedules, privacy changes, title/description/Related edits, Test & Compare changes, or deletions.
- Zero Buffer changes.
- Zero media changes or historical manifest rewrites (`PACKAGE_MANIFEST.json` / `PACKAGE_UPLOAD_RESULT_*.json` untouched).
- Zero spend (`£0`).
- Zero duplication of `J0996` or `J0317` work.
