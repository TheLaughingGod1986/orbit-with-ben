# J2406 Condition Verification Review — J0123 (`025` Mars Long `Js6EQJ8qDi8` Public Gate)

- **Verification Job:** `J2406` (`Verify condition for J0123`)
- **Target Job (`recheck_of`):** `J0123` (`025 date gate: mark done on/after Sun 8 Nov 18:00Z once Js6EQJ8qDi8 is public`)
- **Downstream Dependent Jobs (`--after J0123`):**
  - `J0124` (`025 Mars robot after go-public: Related video on 3 Shorts, pinned comment, Buffer check (rest of J0103)`)
  - `J0135` (`025 length-test Short (J0134): set Related to Js6EQJ8qDi8 once the long is public, before Thu 12 Nov 11:30 London`)
- **Film:** `OWB:025` (*Could a Robot Survive on Mars?*, YouTube ID `Js6EQJ8qDi8`)
- **Reviewer / Agent:** `macbook-2` (`gemini-argon`, Rule-H review lane)
- **Verified At:** `2026-11-08T23:28:50Z`
- **Verdict:** **KEEP / CONDITION SATISFIED — REOPEN `J0123`**
- **Spend / Publishing:** `£0.00` / `0` credits. Verification only (no upload, schedule, or Studio mutation).

---

## 1. Waiting Condition & Original Gate / Approval History

- **Waiting Condition on `J0123`:**
  - `hold.type`: `public`
  - `hold.condition`: `"Mars long Js6EQJ8qDi8 must read back Public"`
  - Date gate rule in `J0123` brief: *"Mark this job done **only on or after Sun 8 Nov 2026 18:00Z**, once 025's long `Js6EQJ8qDi8` shows as public. Not before: the Mini job waiting on it (`--after`) needs the long public."*
- **Original Approvals & Gates (`J0084` / `J0103`):**
  - **Ben Final Watch (UAT) Approval:** Ben watched the `v03f` phone copy (`OWB UAT/025_MarsRobot_full_rough_v03f.mp4`) and approved it ("Looks good" on the board on `2026-10-09T08:38Z`, ref `6077231242`).
  - **Master & Tool Gates:** `02_Video-Projects/025_Could-A-Robot-Survive-On-Mars/09_Final-Export/025_MarsRobot_full_rough_v03f.mp4` (`490.2 s`, SHA-256 `cce6268cbd571f1f404ee98b86e089bbe3cabed15017113bd9559951ee36e09f`) passed `picture_qa`, `music_gate` (own bed `v02`), `clip_check`, `polish_gate`, `gate:episode`, and package review (`c27ec4d`).
  - **Upload & Studio Finish:** Uploaded Private + Scheduled (`publishAt: 2026-11-08T18:00:00Z`) in `J0084` (`24075d9`, registered in `00_Brand/Channel-Setup/social/UPLOADS.json` with matching SHA-256 `cce6268cbd571f1f404ee98b86e089bbe3cabed15017113bd9559951ee36e09f`); Test & Compare thumbnails A, C, B armed (`6088767763`); Studio end screen (`Subscribe` + `-jmMROGoZCM` *Why You Can't Stand On Jupiter* at `7:50–8:10`) and video card (`-jmMROGoZCM` at `6:50`) applied and verified in `J0103`.

---

## 2. Live Public Read-Back Evidence (`2026-11-08T23:28:50Z`)

Public status was verified directly from live YouTube responses (not inferred from the scheduled date; note that the morning analytics snapshot `05_Analytics/owb/snapshots/2026-11-08.json` ran at `06:46Z` prior to the `18:00Z` release):

1. **YouTube Watch Page `ytInitialPlayerResponse` (`https://www.youtube.com/watch?v=Js6EQJ8qDi8`):**
   - `playabilityStatus.status`: `"OK"`
   - `videoDetails.videoId`: `"Js6EQJ8qDi8"`
   - `videoDetails.title`: `"Could a Robot Survive on Mars?"`
   - `videoDetails.channelId`: `"UC_esArsDKd3GJvOkeO0DUog"` (*Orbit With Ben*)
   - `videoDetails.lengthSeconds`: `"490"`
   - `videoDetails.isPrivate`: `false`
   - `microformat.playerMicroformatRenderer.isUnlisted`: `false`
   - `microformat.playerMicroformatRenderer.publishDate`: `"2026-11-08T10:00:15-08:00"` (`2026-11-08T18:00:15Z`)
   - `microformat.playerMicroformatRenderer.uploadDate`: `"2026-11-08T10:00:15-08:00"`
2. **YouTube Public Channel Atom Feed (`https://www.youtube.com/feeds/videos.xml?channel_id=UC_esArsDKd3GJvOkeO0DUog`):**
   - Public-only feed lists `<id>yt:video:Js6EQJ8qDi8</id>`, `<title>Could a Robot Survive on Mars?</title>`, `<published>2026-11-08T18:00:15+00:00</published>`, `<updated>2026-11-08T18:00:17+00:00</updated>`.
3. **YouTube Public oEmbed Endpoint (`https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=Js6EQJ8qDi8&format=json`):**
   - Returns HTTP 200 with `"title": "Could a Robot Survive on Mars?"`, `"author_name": "Orbit With Ben"`, `"author_url": "https://www.youtube.com/@OrbitWithBen"`.
4. **Live Listing Audit (`05_Analytics/live_fixes/2026-11-08.md`, commit `ef4041a14b`, `J2412`):**
   - Confirmed `Js6EQJ8qDi8` is live and public since `2026-11-08T18:00:15Z`, passing chapters (`0:00`..`6:57`), 6-source `Sources:` line, NASA/JPL/MSSS/KSC credits, and live end screen elements.

---

## 3. Action Applied

- Reopened `J0123` (`status: "open"`, hold cleared) with the live public read-back evidence note and updated `remaining_action` (`"Mark J0123 done now that Mars long Js6EQJ8qDi8 is verified Public (live since 2026-11-08T18:00:15Z) so dependent jobs J0124 and J0135 can proceed"`).
- Closed `J2406` as `done`.
