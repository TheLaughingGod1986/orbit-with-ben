# J3400 Condition Verification Review — J0996 (`OWB 027: matching Earth long description after J0317 (J0980 ruling)`)

- **Verification Job:** `J3400` (`Verify condition for J0996`, `recheck_of: J0996`, `repo: owb`, `kind: review`, `needs: mini`, `open_claim: true`, `due: 2026-11-23T00:27:57+00:00`)
- **Parent Job:** `J0996` (`OWB 027: matching Earth long description after J0317 (J0980 ruling)`, `status: blocked`, `by: macbook-2`, `needs: mini`, `repo: owb`, `kind: studio`, `film: 027`, `stage: upload`, `after: J0317`, `hold.type: dependency`)
- **Prerequisite Job:** `J0317` (`027 Shorts (OVLv9dxTcpE, emwQsPxnRGM): set Related video to 6bbbvfCx6zY after Sun 22 Nov 18:00Z`, `status: done`, `by: macbook-2`, evidence PR `#1199` merged at `6f64f064cf`)
- **Verifier:** `gemini` (specialist worker on Mac mini; `chief_relay.py status` reports `Chief: Codex` — no Chief ruling, no PR merge, no hold release/reopen, no YouTube writes)
- **Checked At:** `2026-11-22T23:30Z` – `2026-11-22T23:33Z`
- **Spend & Side Effects:** `£0.00` (`0` credits; zero YouTube, Studio, Buffer, or NAS writes; no browser/WebSocket attach; no PR merged; no schedule, privacy, title, or A/B test changes; no audio or moving-video perception claimed)
- **Advisory Verdict (Parked for Elected Chief):** **CONDITION MET — ready on the Mac mini API route ONLY (NOT on the stalled MacBook Studio tab).** Recommend elected Chief Codex merge this review PR, **reopen `J0996` pinned to the Mac mini (`mini_only: true`) for description-only YouTube Data API execution via `07_Content-Ops/scripts/redescribe-videos.ts`** (with `due` ahead of `J3399`'s `2026-11-23T09:00:00Z` / target before `2026-11-23T11:30:00Z`), and close `J3400`. Parked `J3400` for Chief because reopening a held job, changing queue routing (`mini_only`), and merging PRs are protected Chief calls.

---

## 1. Why `J0996` Was Blocked and What `J3400` Verifies

1. `J0996` (`after: J0317`) was claimed by `macbook-2` at `2026-11-22T23:09Z` after `J0317` completed.
2. At `2026-11-22T23:27Z`, `macbook-2` cleanly aborted before clicking Save when Playwright `fill()` on `#description-textarea #textbox` introduced a trailing newline (`666` vs exact `665` chars), and the renderer for MacBook Studio tab `8A9E2F211C963F35D4B2E8AFFD33B157` subsequently stalled. `macbook-2` released the `027/upload` stage claim and blocked `J0996` (`parked for Chief`), recommending Mini API execution via `07_Content-Ops/scripts/redescribe-videos.ts` (`--mini-only`, no Studio needed).
3. Because `J0996` still carries `after: J0317` (which is `done`), `relay` automatically set `hold.type: dependency` (`Required predecessor is complete; verify remaining gates and approvals`) and queued `J3400`.

---

## 2. Independent Verification of Prerequisite `J0317` & Live YouTube State

1. **Prerequisite `J0317` Complete and Merged:**
   - `jobs/QUEUE.json` confirms `J0317` is `status: done` (`by: macbook-2`).
   - Owner-authored PR `#1199` (`1d8b5fbb7f`) was reviewed and merged by Acting Chief Codex (`J3397`, merge commit `6f64f064cf`, `jobs/reviews/J3397/REVIEW.md`).
   - `jobs/readbacks/J0317.json` records at `2026-11-22T23:06:11Z`–`23:06:21Z` on `Orbit With Ben` (`UC_esArsDKd3GJvOkeO0DUog`):
     - `6bbbvfCx6zY` verified `VIDEO_PRIVACY_PUBLIC`, live title `What If Earth Stopped Spinning? (It's Already Slowing Down)`.
     - `OVLv9dxTcpE` reloaded with `related_video_id: "6bbbvfCx6zY"` (`targetExternalVideoId: "6bbbvfCx6zY"`), `save_disabled: true`, `undo_disabled: true`, and all other fields unchanged (560-byte description, SHA-256 `016c84279071dee34756a343c620acad6ccdd9a8ce79b1fea3d9a121518f2369`).
     - `dM1OgGPAYvw` excluded and untouched (`excluded_video_untouched: true`).
2. **Fresh Read-Only YouTube Data API Verification on Mac Mini (`2026-11-22T23:31Z`):**
   - Authenticated cleanly via `07_Content-Ops/.env` `getYouTubeAccessToken()` (no secrets printed, zero write requests):
     - **Channel:** `Orbit With Ben` (`UC_esArsDKd3GJvOkeO0DUog`, `@orbitwithben`) — proves the Mini's YouTube Data API OAuth token is live right now.
     - **Long `6bbbvfCx6zY`:** `channelId: UC_esArsDKd3GJvOkeO0DUog`, `privacyStatus: public`, `uploadStatus: processed`, `publishAt: null`, live listing title **`What If Earth Stopped Spinning? (It's Already Slowing Down)`**, description `1,834` chars / `1,843` bytes, SHA-256 `a858107264b3c61025e24c98910f547cfcb6033c5d0b1a3f6a1351f0b7775474` (exact match to `J0317` receipt).
     - **Short `OVLv9dxTcpE`:** `channelId: UC_esArsDKd3GJvOkeO0DUog`, `privacyStatus: public`, `uploadStatus: processed`, `publishAt: null`, title **`What If Earth Stopped Spinning?`**, description **`560` chars / `560` UTF-8 bytes**, SHA-256 **`016c84279071dee34756a343c620acad6ccdd9a8ce79b1fea3d9a121518f2369`**.
   - **Zero Drift Confirmed:** Live `OVLv9dxTcpE` description is byte-identical to local `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/10_Shorts/lift_sudden_air/11_Upload-Package/PACKAGE_MANIFEST.json` (`560` bytes, SHA-256 `016c84279071dee34756a343c620acad6ccdd9a8ce79b1fea3d9a121518f2369`). Neither `6bbbvfCx6zY` nor the prefix is present yet.
3. **Exact Prepend Verification for `07_Content-Ops/scripts/redescribe-videos.ts`:**
   - **Prefix (`105` bytes):**
     `What If Earth Stopped Spinning? (It's Already Slowing Down)\nhttps://www.youtube.com/watch?v=6bbbvfCx6zY\n\n`
   - **Unique anchor (`find`):** `What If Earth Stopped Spinning?\n\nIf the ground stopped` — independently verified to occur **exactly `1` time** in the live `560`-byte description.
   - **Expected post-prepend description:** exact **`665` chars / `665` UTF-8 bytes**, SHA-256 **`1c3c392a7acc1fdbc1ed7b9ec286688d072a5d8ea166fdb76a5d0bcf7f38c4f8`**, preserving every existing byte after the prefix.
   - **Script safety verified (`07_Content-Ops/scripts/redescribe-videos.ts`):** uses `ensureDeskLock()`, sends only `videos.update?part=snippet` preserving `title`, `tags`, `categoryId`, `defaultLanguage`, and `defaultAudioLanguage`, never sends `status` (so privacy and `publishAt` stay untouched), skips if `replace` already exists or `find` is not unique, supports `--dry-run`, and writes a readback `_RESULT.json`.

---

## 3. Original Gates, Approvals & Film Stage Status Still Valid

| Item | Evidence | Status |
|---|---|---|
| `J0980` / `J0994` ruling (`9efc342c8`, 26 Oct 2026) | Acting Chief Codex authorised `J0996` description-only prepend on `OVLv9dxTcpE` once `J0317` completes and `6bbbvfCx6zY` reads Public; target before `23 Nov 11:30 London`; no retitle, privacy/schedule, media, upload, Test & Compare, pinned comment, or spend; `dM1OgGPAYvw` and standalone `vlkj8RQKmH8` excluded. | **Valid** |
| `027` long `6bbbvfCx6zY` | `J0834` (Ben OK `v01m`, `gate:episode PASS`, sha `499e8edc...`), `J2497` title/test lock, `J1272`/`J3393` Public/end-screen/pin receipt, `J0317` + live API `23:31Z` Public check. | **Valid** |
| `027` Short `OVLv9dxTcpE` | `J0940` (`earth_sudden_air_v05`, Chief PASS `#6395360875`, Ben OK `#6396903361`, sha `666ab5b1...`), `J0317` Related=`6bbbvfCx6zY` verified after reload, live API `23:31Z` Public + untouched `560`-byte description. | **Valid** |
| `027/upload` board linkage & claim | `J3397` (PR `#1200`) formally linked `J0996` to `film: 027`, `stage: upload`. `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/status.json` confirms `claims: []` (`macbook-2` released cleanly). | **Ready to claim** |
| Downstream `J3399` | Open (`after: J0996`, `due: 2026-11-23T09:00:00Z`) for `emwQsPxnRGM` Private/schedule reconciliation. Unblocks once `J0996` completes. | **Preserved** |
| Local `UPLOADS.json` note (non-blocking) | `00_Brand/Channel-Setup/social/UPLOADS.json` still lists `OVLv9dxTcpE.relatedVideoId: "VBaYRPp85Sw"` (`relatedJob: "J0975"`) from before `J0317`; no mutation made here (flag for clean record sync after `J0996` or inside `J3399`). | **Observed** |

---

## 4. Independently Confirmed Queue-Routing Risk (Requires Chief Action on Reopen)

- Independently evaluated `jobs.macbook_portable(J0996, data)` and `jobs.macbook_studio_ok(J0996, text)` against `jobs/QUEUE.json`:
  - `MACBOOK_CDP=""`: `portable=False`, `studio_ok=False`
  - `MACBOOK_CDP="9223"`: **`portable=True`, `studio_ok=True`**
  - With **`mini_only: true`** (`MACBOOK_CDP="9223"`): **`portable=False`**
- **Risk if reopened unchanged:** `J0996` currently has `needs: "mini"`, `kind: "studio"`, `mini_only` unset, and `remaining_action` saying `"in Studio"`. If Chief runs plain `jobs.py reopen J0996`, the MacBook worker can reclaim `J0996` and hit the stalled MacBook Studio tab `8A9E2F211C963F35D4B2E8AFFD33B157` again.
- **Clean fix on reopen:** Set **`mini_only: true`** on `J0996`, update `remaining_action` to the Mini API path (`07_Content-Ops/scripts/redescribe-videos.ts` dry-run + apply on `OVLv9dxTcpE`, verify `665`-byte live API readback SHA-256 `1c3c392a...`, sync `lift_sudden_air/11_Upload-Package/PACKAGE_MANIFEST.json`, and open evidence PR), and set `due: 2026-11-23T08:30:00Z` (ahead of `J3399`'s `09:00:00Z` and `J0996`'s `11:30 London` target). Because Related=`6bbbvfCx6zY` is already persisted by `J0317`, no Studio browser session is needed at all.

---

## 5. Low-Disk Offload Check (Mac Mini)

- Free disk on `/` is `13 GiB` (`13,285 MB`, under 20 GB).
- Checked existing detached offload before starting anything: tmux session `J3397-offload` (started `2026-11-22T23:24:46Z`) is still running; `/Users/benjaminoats/_desk/logs/J3397-offload.done` is absent. Did **not** start a duplicate offload; no NAS files deleted.

---

## 6. Recommended Chief Actions

1. **Merge this PR** (`gemini/J3400-j0996-verify`, `jobs/reviews/J3400/REVIEW.md`).
2. **Reopen `J0996` pinned to the Mac mini (`mini_only: true`)** with updated `remaining_action` for `07_Content-Ops/scripts/redescribe-videos.ts` (dry-run then apply on `OVLv9dxTcpE` only, exact `665`-byte readback SHA-256 `1c3c392a7acc1fdbc1ed7b9ec286688d072a5d8ea166fdb76a5d0bcf7f38c4f8`, sync `lift_sudden_air/11_Upload-Package/PACKAGE_MANIFEST.json`, preserve `dM1OgGPAYvw` and `vlkj8RQKmH8`, zero Studio writes/spend/schedule changes) and `due: 2026-11-23T08:30:00Z`.
3. **Close `J3400`** after reopening `J0996`.
