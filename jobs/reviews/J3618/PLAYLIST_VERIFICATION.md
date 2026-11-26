# J3618 — OWB 027 (`6bbbvfCx6zY`) Series Playlist Verification & Add

- **Date (UTC):** `2026-11-24T20:57Z–21:02Z`
- **Agent:** `macbook-2` (MacBook worker, Gemini 4 Neon)
- **Trigger:** `J3616` acting-Chief ruling (`jobs/reviews/J3616/CHIEF_RULING.md`) following `05_Analytics/owb/autopsy/6bbbvfCx6zY_48h.md`
- **Channel verified in Studio (CDP port `9223`, existing `studio.youtube.com` tab reused):** **Orbit With Ben** (`UC_esArsDKd3GJvOkeO0DUog`)
- **Video:** OWB `027` — *What If Earth Stopped Spinning? (It's Already Slowing Down)* (`6bbbvfCx6zY`, Public, published `22 Nov 2026`, `7:27`)
- **Public playback:** None (`youtube.com/watch` never opened; all checks and the single playlist edit were performed inside `studio.youtube.com`)
- **Spend / upload / recut:** £0 · none

---

## 1. Pre-Change Verification (Read-Only)

Verified directly in YouTube Studio (`UC_esArsDKd3GJvOkeO0DUog`, Orbit With Ben) before any write:

1. **Channel playlists (`studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/content/playlists`):** exactly **2** playlists exist on the channel:
   - `PLdoEpeiktw_Y` — **Real Worlds: Solar System, Moons and Alien Planets Explained** (*"Real places and real observations, told with real imagery."*, Public, last updated `21 Nov 2026`, `12` videos). Checked `studio.youtube.com/playlist/PLdoEpeiktw_Y/videos`: **`6bbbvfCx6zY` absent** (`VBaYRPp85Sw`, `55AEQwvs36g`, `Js6EQJ8qDi8`, `ziKBPJ6FY0U`, `NbW5G1BpPY0`, `h8HGfyShEHI`, `-jmMROGoZCM`, `b8-X_FyJnHM`, `13q4_EoLEN4`, `ileYnHpLLCU`, `oASsmqZfWU4`, `c5AdqQsnnys`).
   - `PLOw2VKzGCOWU` — **What Would Happen If…: Black Holes, Neutron Stars and Extreme Space** (*"Scenario films: what would happen if you stood on, fell into, or travelled through these places."*, Public, Default video order: `Manually sorted in YouTube`, last updated `15 Nov 2026`, `11` videos, `2` views). Checked `studio.youtube.com/playlist/PLOw2VKzGCOWU/videos`: **`6bbbvfCx6zY` absent** (`REXYxuLOBoI`, `Yk1tLh23rko`, `rVqgtkBV3jc`, `Js6EQJ8qDi8`, `-jmMROGoZCM`, `2fsQcea-voM`, `ojk-dfOpAmw`, `Mo93x0fxB1Q`, `3xrxdmaOwJI`, `m09jUdwC5hk`, `T3cBBss1F60`).
2. **Video Details (`studio.youtube.com/video/6bbbvfCx6zY/edit`, read-only):**
   - Playlists trigger text: `Select` (confirming `6bbbvfCx6zY` was in **zero** playlists live, not merely `playlistId: null` in `PACKAGE_MANIFEST.json`).
   - Visibility: `Public`.
   - Running Test & Compare `T028`: `A/B testing titles` -> `Running…` (`What If Earth Stopped Spinning? (It's Already Slowing Down)` / `Earth's Day Used to Be 22 Hours (And It's Still Getting Longer)`); Thumbnail section -> `Running…`.
3. **Playlist ownership & series fit:** Confirmed `PLOw2VKzGCOWU` belongs to `UC_esArsDKd3GJvOkeO0DUog` (Orbit With Ben), is the existing verified *What Would Happen If…* scenario series playlist (matching `05_Analytics/PLAYLIST_AUDIT_2026-11.md` and `jobs/reviews/J2460/PLAYLIST_REFS.md`), and matches OWB `027` (*What If Earth Stopped Spinning?*).

---

## 2. Authorised Action Applied (`2026-11-24T21:00:49Z`)

Per the `J3618` brief (absent from the existing verified series playlist -> add **only** `6bbbvfCx6zY` to `PLOw2VKzGCOWU` without touching Video Details, `T028`, titles, thumbnails, privacy, schedule, end screen, or pinned comment):

- Navigated to `studio.youtube.com/channel/UC_esArsDKd3GJvOkeO0DUog/videos/upload` (verified `channelId: UC_esArsDKd3GJvOkeO0DUog`, `Orbit With Ben`).
- Selected **only** `6bbbvfCx6zY` (`1 selected` in bulk bar) -> clicked **Add to playlist** -> verified both playlist checkboxes were unchecked (`Real Worlds` `false`, `What Would Happen If…` `false`) -> ticked **only** `What Would Happen If…: Black Holes, Neutron Stars and Extreme Space` (`checkbox-1: true`, `checkbox-0: false`) -> clicked **Save**.
- Studio issued **`POST https://studio.youtube.com/youtubei/v1/browse/edit_playlist` -> HTTP `200`** (`2026-11-24T21:00:49.806Z`). No video-metadata, A/B test, end-screen, or comment write endpoint was called.

---

## 3. Post-Change Read-Back Verification

1. **Target playlist (`studio.youtube.com/playlist/PLOw2VKzGCOWU/videos`):**
   - `channelId`: `UC_esArsDKd3GJvOkeO0DUog` (Orbit With Ben)
   - `videoCount`: **`12`** (was `11`), Public, last updated `24 Nov 2026`
   - Confirmed member order (`containsTarget: true`):
     `REXYxuLOBoI`, `Yk1tLh23rko`, `rVqgtkBV3jc`, `Js6EQJ8qDi8`, `-jmMROGoZCM`, `2fsQcea-voM`, `ojk-dfOpAmw`, `Mo93x0fxB1Q`, `3xrxdmaOwJI`, `m09jUdwC5hk`, `T3cBBss1F60`, **`6bbbvfCx6zY`**
2. **Other channel playlist (`studio.youtube.com/playlist/PLdoEpeiktw_Y/videos`) & Playlists list:**
   - Still exactly **2** playlists on the channel (`PLOw2VKzGCOWU` `12` videos, `PLdoEpeiktw_Y` `12` videos); no new playlist created.
   - `PLdoEpeiktw_Y` unchanged (`12` videos, `6bbbvfCx6zY` absent).
3. **Preserved video state (`studio.youtube.com/video/6bbbvfCx6zY/edit`, read-only):**
   - **Playlists field:** `What Would Happen If…: Black Holes, Neutron Stars and Extreme Space` (was `Select`).
   - **Running `T028` (Titles & Thumbnails):** `A/B testing titles` -> `Running…`, Arm A `What If Earth Stopped Spinning? (It's Already Slowing Down)` present, Arm B `Earth's Day Used to Be 22 Hours (And It's Still Getting Longer)` present; Thumbnail section `Running…`.
   - **Visibility / Schedule:** `Public` (published `22 Nov 2026`, unchanged).
   - **Description line 1:** unchanged (`What if Earth stopped spinning? Right now the ground carries you east at 1,000 km/h — and Earth is already slowing down as the Moon pulls on it.`).
   - **End screen (opened `#endscreen-editor-link` read-only, navigated away without saving):** `What Happened to Venus?` + `Subscribe` (`7:06–7:26`) present.
   - **Comments (`studio.youtube.com/video/6bbbvfCx6zY/comments/inbox`, read-only):** `Published: 1` / `Creator activity: 1` unchanged (same count `1` as before the playlist edit; no comment endpoint touched).

---

## 4. Follow-Up Schedule

- The uploaded `PACKAGE_MANIFEST.json` was left untouched per the studio manifest immutability rule.
- The **7-day retention autopsy** for `6bbbvfCx6zY` remains due **29 Nov 2026 after 18:00Z** under normal automatic queueing and is not delayed by this task.
