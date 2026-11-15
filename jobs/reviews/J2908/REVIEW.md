# J2908 Condition Verification Review — J0124 (`026` Nearest Star Long `c5AdqQsnnys` Public Gate for `025` End-Screen Swap)

- **Verification Job:** `J2908` (`Verify condition for J0124`)
- **Target Job (`recheck_of`):** `J0124` (`025 Mars robot after go-public: Related video on 3 Shorts, pinned comment, Buffer check (rest of J0103)`)
- **Films:** `OWB:025` (*Could a Robot Survive on Mars? (One Lasted 14 Years)*, YouTube ID `Js6EQJ8qDi8`) and `OWB:026` (*How Far Is the Nearest Star? (You Can't See It, and It Has a Planet)*, YouTube ID `c5AdqQsnnys`)
- **Reviewer / Elected Acting Chief:** `gemini` (Gemini 4 Argon High)
- **Verified At:** `2026-11-15T18:31:16Z`
- **Verdict:** **KEEP / CONDITION SATISFIED — REOPEN `J0124`**
- **Spend / Publishing:** `£0.00` / `0` credits. Verification only (no upload, schedule, or Studio mutation).

---

## 1. Waiting Condition & Original Gate / Approval History

- **Waiting Condition on `J0124`:**
  - `hold.type`: `public`
  - `hold.condition`: `"026 nearest-star long c5AdqQsnnys reads Public (publishAt 2026-11-15T18:00:00Z); it is Private and scheduled as of 10 Nov 16:35Z"`
  - `remaining_action`: `"Swap the Mars long's end-screen video from the Jupiter film to the nearest-star long once it is public"`
- **Completed Steps on `J0124` & Linked Jobs:**
  - **Related video links on `025` Shorts:** Completed in `J2504` (`2026-11-10T14:06Z`, Studio CDP `9223` read-back verified on `iyvWYFP_ETA`, `B1z2dv7m7Vk`, `N42gKBbD7tE`, `bSjWiCbB7pY`), and preserved on the swapped Cuts `uhZSRcvngvE` (`J2519`) and `RT-ec4_GcOk` (`J2520`).
  - **Pinned comment on `025` long `Js6EQJ8qDi8`:** Completed in `J0124` step 1 (`2026-11-10T16:36Z`, comment `UgyioTqynJeuTyfp9qF4AaABAg` posted and pinned, commit `6ee3657ae`).
  - **Buffer posts for `025` Shorts:** Verified across `J0103`, `J2519` (`uhZSRcvngvE`), and `J2520` (`RT-ec4_GcOk`).
  - **Remaining item (Item 4 of `J0124`):** Swap `025` Mars long `Js6EQJ8qDi8`'s end-screen video element from `-jmMROGoZCM` (*Why You Can't Stand On Jupiter*) to `026` Nearest Star long `c5AdqQsnnys` now that `026` is public (as the `025` script hands off to `026`).
- **Original Approvals & Gates (`025` and `026`):**
  - **`025` Mars (`Js6EQJ8qDi8`):** Ben UAT approval on `v03f` (`2026-10-09T08:38Z`, ref `6077231242`); passed `picture_qa`, `music_gate`, `clip_check`, `polish_gate`, `gate:episode`; uploaded in `J0084` (`24075d9`), public since `2026-11-08T18:00:15Z` (`J2406` / `J2407`).
  - **`026` Nearest Star (`c5AdqQsnnys`):** Ben UAT approval on `22 Oct 2026` + acting-Chief final OK (`J0833`); uploaded Private and scheduled for `2026-11-15T18:00:00Z`; upload completion and Studio finish verified (`J1825` / `J1914` / `J1927`), thumbnail ruling retained (`J1944`).

---

## 2. Live Public Read-Back Evidence (`2026-11-15T18:31:16Z`)

Public status was verified directly from live YouTube responses at `2026-11-15T18:31:16Z` (not inferred from the `18:00Z` scheduled timestamp):

1. **YouTube Public oEmbed Endpoint (`https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=c5AdqQsnnys&format=json`):**
   - Returns **HTTP 200** with:
     - `"title"`: `"How Far Is the Nearest Star? (You Can't See It, and It Has a Planet)"`
     - `"author_name"`: `"Orbit With Ben"`
     - `"author_url"`: `"https://www.youtube.com/@OrbitWithBen"`
2. **YouTube Watch Page `ytInitialPlayerResponse` (`https://www.youtube.com/watch?v=c5AdqQsnnys`):**
   - `playabilityStatus.status`: `"OK"` (`reason`: `null`)
   - `videoDetails.videoId`: `"c5AdqQsnnys"`
   - `videoDetails.title`: `"How Far Is the Nearest Star? (You Can't See It, and It Has a Planet)"`
   - `videoDetails.channelId`: `"UC_esArsDKd3GJvOkeO0DUog"` (*Orbit With Ben*)
   - `videoDetails.lengthSeconds`: `"495"`
   - `videoDetails.isPrivate`: `false`
   - `videoDetails.isLiveContent`: `false`
   - `microformat.playerMicroformatRenderer.isUnlisted`: `false`
   - `microformat.playerMicroformatRenderer.isFamilySafe`: `true`
   - `microformat.playerMicroformatRenderer.publishDate`: `"2026-11-15T10:00:37-08:00"` (`2026-11-15T18:00:37Z`)
   - `microformat.playerMicroformatRenderer.uploadDate`: `"2026-11-15T10:00:37-08:00"`
3. **YouTube Public Channel Atom Feed (`https://www.youtube.com/feeds/videos.xml?channel_id=UC_esArsDKd3GJvOkeO0DUog`):**
   - Public-only feed lists `<id>yt:video:c5AdqQsnnys</id>`, `<title>How Far Is the Nearest Star? (You Can't See It, and It Has a Planet)</title>`, `<published>2026-11-15T18:00:37+00:00</published>`, `<updated>2026-11-15T18:00:39+00:00</updated>`.
4. **Target Video `025` (`Js6EQJ8qDi8`) Live Check:**
   - Also confirmed Public at `2026-11-15T18:31:16Z` (`oEmbed` HTTP 200, `playabilityStatus.status`: `"OK"`, `isPrivate`: `false`, `isUnlisted`: `false`, `published`: `2026-11-08T18:00:15+00:00`).

---

## 3. Action Applied

- Reopened `J0124` (`status: "open"`, hold cleared) with the live public read-back evidence note (`remaining_action`: `"Swap the Mars long's end-screen video from the Jupiter film to the nearest-star long once it is public"`).
- Closed `J2908` as `done`.
