# J3395 Condition Verification Review — J0317 (`027 Shorts (OVLv9dxTcpE, emwQsPxnRGM): set Related video to 6bbbvfCx6zY after Sun 22 Nov 18:00Z`)

- **Verification Job:** `J3395` (`Verify condition for J0317`, `recheck_of: J0317`, `repo: owb`, `kind: review`, `needs: mini`, `open_claim: true`, `due: 2026-11-22T22:53:19+00:00`)
- **Parent Job:** `J0317` (`027 Shorts (OVLv9dxTcpE, emwQsPxnRGM): set Related video to 6bbbvfCx6zY after Sun 22 Nov 18:00Z`, `status: blocked`, `by: codex`, `needs: mini`, `repo: owb`, `kind: studio`, `after: J3394`, `hold.type: dependency`)
- **Prerequisite Job:** `J3394` (`Restore responsive Orbit Studio access for Earth Shorts Related links`, `status: done`, `by: macbook-2`, completed `2026-11-22T21:52Z`, evidence PR `#1195` open for Chief)
- **Verifier:** `macbook-2` (ordinary MacBook worker, outside the Chief succession chain; `chief_relay.py status` at check time reports `Chief: Codex` — no Chief ruling, no PR merge, no hold release/reopen, no YouTube writes)
- **Checked At:** `2026-11-22T21:58Z` – `2026-11-22T22:01Z`
- **Spend & Side Effects:** `£0.00` (`0` credits; zero YouTube, Studio, Buffer, or NAS writes; no WebSocket/Playwright browser attach; no PR merged; no schedule, privacy, title, or A/B test changes)
- **Advisory Verdict (Parked for Elected Chief):** **CONDITION MET — recommend Chief merge PR `#1195` (`J3394` evidence) and this PR, reopen `J0317` with MacBook queue routing (`needs=macbook` or removing the passive `Buffer` word that triggers `STUDIO_BLOCK`), and close `J3395`.** Parked `J3395` for the elected Chief because PR merges and releasing a verified hold (`jobs.py reopen J0317` — code-enforced in `scripts/jobs.py` `do_reopen`) are protected Chief actions.

---

## 1. Recorded Waiting Condition on `J0317`

Acting-Chief Codex ruling (`2026-11-22T21:43Z`, studio thread `#7086270901`, `hold.type: dependency`, `recheck_task: J3395`) held `J0317` after four Mini CDP 9223 WebSocket attachment timeouts (`18:59`, `19:28`, `19:43`, `20:11Z`; worker report `#7085022021`) with no saved Related link verified. Required condition before reopening `J0317`:

1. `J3394` establishes responsive Orbit Studio access (existing Mini session or already signed-in MacBook Orbit Studio session) and records timestamped responsive DOM and exact channel/video identity evidence (HTTP target listing alone is insufficient; no Chrome shutdown, duplicate tabs, repeated unchanged probes, or YouTube metadata edits).
2. Elected Chief verifies the evidence and reopens `J0317` for fresh long-Public verification plus save/reload readback of Related video -> `6bbbvfCx6zY` on `OVLv9dxTcpE` and `emwQsPxnRGM` only (`dM1OgGPAYvw` excluded).

---

## 2. Independent Verification of Prerequisite `J3394` & Evidence PR `#1195`

1. **Queue & Thread State:**
   - `jobs/QUEUE.json` shows `J3394` is `status: done` (`by: macbook-2`, `2026-11-22T21:52Z`).
   - Studio thread `#954` read through `#7086391643` (`2026-11-22T21:53:28Z`): `#7086375617` (`2026-11-22T21:52:12Z`) posts the full `J3394` completion report; no later comment supersedes `J3394` or alters `J0317`'s scope.
2. **Evidence PR `#1195` Integrity:**
   - PR `#1195` (`https://github.com/TheLaughingGod1986/orbit-with-ben/pull/1195`, branch `macbook/J3394`, head `51ef0a4389ab1a1e7d2f3b6cc59866d8993de920`, `state: OPEN`, `baseRefName: main`, `isCrossRepository: false`, author `TheLaughingGod1986`).
   - Single file added: `jobs/readbacks/J3394.json` (68 lines, git blob `49f6f332717e8b1620450a2cd3b2206dd2b64171`, SHA-256 `8f6bde036226af521655ff93b0b63d0578f1f800085f87345000daf35b0a7954`).
3. **Required Evidence Fields Confirmed in `jobs/readbacks/J3394.json`:**
   - **Machine & Browser:** MacBook, CDP port `9223`, `Chrome/157.0.8103.79`, `left_running: true`, `profiles_altered: false`, `tabs_before_count: 3`, `tabs_after_count: 3`, `same_tab_ids: true`, reused existing Studio tab `8A9E2F211C963F35D4B2E8AFFD33B157` via `cdp_tabs.reuse_page`, zero competing writers (`port_9223_clients_before: LISTEN only`, `other_macbook_slots_active: false`).
   - **Timestamp & Responsive DOM Probe:** Verified at `2026-11-22T21:47:56Z` via Playwright `1.60.0` `connect_over_cdp` (`0.575 s`) -> `cdp_tabs.reuse_page` (`0.617 s`) -> settled read-only `page.evaluate` (`2.633 s` total, after ~2 s sleeping-tab wake settle; no worker-initiated navigation).
   - **Exact Channel & Video Identity:** Channel `Orbit With Ben` (`UC_esArsDKd3GJvOkeO0DUog`, `/channel/UC_esArsDKd3GJvOkeO0DUog`), URL `https://studio.youtube.com/video/6bbbvfCx6zY/edit` (`Video details - YouTube Studio`, `readyState: complete`), video `6bbbvfCx6zY` (`What If Earth Stopped Spinning? (It's Already Slowing Down)`), `visibility_text_observed: Public`, A/B title test observed running and untouched, `save_disabled: true`, `undo_disabled: true`, `has_unsaved_edits: false`.
   - **Guards Honoured:** `youtube_mutations_sent: false`, `excluded_video_untouched: dM1OgGPAYvw`, `spend_gbp: 0`.
4. **Passive Read-Only Corroboration (`2026-11-22T22:00Z`):**
   - Local read-only HTTP check on MacBook CDP `9223` (`/json/version`, `/json/list` — no WebSocket attach, no tab wake, no navigation) confirmed `Chrome/157.0.8103.79` remains running with `3` page tabs and the same Orbit Studio page tab `8A9E2F211C963F35D4B2E8AFFD33B157` at `https://studio.youtube.com/video/6bbbvfCx6zY/edit` (`Video details - YouTube Studio`). (Passive HTTP listing is corroboration only; responsive DOM evidence is recorded in `J3394` / PR `#1195`.)

---

## 3. Original Gates, Video Identities & Approvals Still Valid

| Video ID | Role | Records Checked | Status |
|---|---|---|---|
| `6bbbvfCx6zY` | 027 long (`What If Earth Stopped Spinning? (It's Already Slowing Down)`) | `J0834` (done `2026-10-22`, Ben OK `v01m` 22 Oct, `gate:episode PASS`, sha `499e8edc...`), `UPLOADS.json` matches; `J2497` title/test lock; `J3389` (Public verified `2026-11-22T20:44:03Z`, published `18:00:06Z`); `J1272` + `J3393` (merged PR `#1193`, `jobs/readbacks/J1272.json`: Public verified `21:09:05Z`, end screen + approved pinned comment `Ugzhyw_0SXE88nIZ1fR4AaABAg` verified). | Valid. (`05_Analytics/owb/snapshots/2026-11-22.json` was captured before `18:00Z` go-live, so it still shows `private` / `publishAt: 2026-11-22T18:00:00Z`; `J0317` still owns a fresh Public check immediately before saving Related links.) |
| `OVLv9dxTcpE` | Short 1 (`What If Earth Stopped Spinning?`, `earth_sudden_air_v05`) | `J0940` (done `2026-10-25`, Chief PASS `#6395360875`, Ben OK `#6396903361`, readback `#6399541354`, sha `666ab5b1...` in `UPLOADS.json`); snapshot `2026-11-22.json` shows `public`, `publishedAt: 2026-10-26T11:30:15Z`, `892` views. | Valid target for Related -> `6bbbvfCx6zY`. |
| `emwQsPxnRGM` | Short 2 (`Why Do You Weigh Less at Earth's Equator?`, `earth_equator_weight_v01`) | `J0853` (done `2026-10-22`, sha `9781e967...` in `UPLOADS.json`, Private, `publishAt: 2026-11-23T11:30:00Z`); snapshot `2026-11-22.json` shows `private`. | Valid target for Related -> `6bbbvfCx6zY`. Airs **Mon 23 Nov 11:30Z** — reopen and run before `10:30Z`. |
| `dM1OgGPAYvw` | Superseded Short 1 (`v02`, sha `4ab2b658...`) | `J0940` left Private and unscheduled; snapshot `2026-11-22.json` confirms `private`, `publishAt: None`. | **EXCLUDED — never touch.** |

---

## 4. Independently Confirmed Queue-Routing & Open-PR Details for Chief

1. **Confirmed `macbook_studio_ok(J0317) == False` False Positive (`scripts/jobs.py`):**
   - Independently evaluated `jobs.macbook_studio_ok(J0317, text)` and `jobs.macbook_portable(J0317, data)` with `MACBOOK_CDP=9223`: both return `False`.
   - Exact cause: after `STUDIO_PROHIBITION` stripping, `STUDIO_BLOCK` matches `['Buffer']` on the passive sentence `"Buffer still waits until each Short is public, then points at the full film."` in `J0317`'s body.
   - **Operational risk if reopened unchanged:** `J0317` currently has `needs: "mini"`. If Chief simply runs `jobs.py reopen J0317`, the MacBook worker cannot claim `J0317`, and the Mini (where CDP 9223 failed 4 consecutive times on 22 Nov) will reclaim it and stall again.
   - **Fix on reopen:** Route `J0317` to the verified MacBook Orbit Studio session by setting `needs: "macbook"` on `J0317` (or removing/negating the passive `"Buffer"` sentence so `macbook_studio_ok` returns `True` — `needs: "macbook"` also prevents the Mini from racing for it). Setting a deadline of `2026-11-23T10:30:00Z` (matching `J3394`) ensures it runs ahead of `emwQsPxnRGM`'s `11:30Z` go-live.
2. **Open PR `#1194` (`codex/J3393`) & `J3396`:**
   - PR `#1194` (open) sets `"film": "027", "stage": "upload"` on `J0317` in `jobs/queue.json` (currently `""`/`""` on `main`, which triggered `J3396`: `Chief: resolve 027 upload orphan-blocked`). Merging PR `#1194` (or setting those fields alongside reopening `J0317`) resolves that linkage cleanly.

---

## 5. Recommended Chief Actions

1. **Merge PR `#1195`** (`macbook/J3394`, head `51ef0a4389ab1a1e7d2f3b6cc59866d8993de920`, `jobs/readbacks/J3394.json`) and **this PR** (`macbook/J3395`, `jobs/reviews/J3395/REVIEW.md`), plus PR `#1194` if desired for `027/upload` linkage.
2. **Reopen `J0317` and route to MacBook** (`needs: "macbook"`, due `2026-11-23T10:30:00Z`), noting:
   - Verified evidence: `J3394` / PR `#1195` (`2026-11-22T21:47:56Z` MacBook CDP `9223` responsive DOM read on `Orbit With Ben` `UC_esArsDKd3GJvOkeO0DUog`, tab `8A9E2F211C963F35D4B2E8AFFD33B157`).
   - Runner note: wait ~2 s for tab-wake settle after `cdp_tabs.reuse_page()`, freshly verify `6bbbvfCx6zY` is `Public`, set Related video -> `6bbbvfCx6zY` on `OVLv9dxTcpE` and `emwQsPxnRGM` only with save/reload persistence readback on each, never touch `dM1OgGPAYvw`, and make no uploads, privacy/schedule changes, title/A/B-test edits, or Buffer changes.
3. **Close `J3395`** (`jobs.py reopen J3395`, claim, `jobs.py done J3395 --agent <chief> --ref <PR URL> --git`) after reopening `J0317`.
