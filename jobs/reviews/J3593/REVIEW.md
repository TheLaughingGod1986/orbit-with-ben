# J3593 — Condition Verification Review for J3417 (`WW2:002` `qfc6EBStOfo` / `J9WGu8aPnHI`)

- **Verification job:** `J3593` (`Verify condition for J3417`, `recheck_of: J3417`, `repo: owb`, `kind: review`)
- **Parent job:** `J3417` (`Field Order History pilot 2: two close-crop thumbnails and a Test & Compare at launch; one-subject rule into the playbook for films 003+`, `repo: ww2`, `kind: thumb`, `needs: mini`, `status: blocked`, `by: codex`, `taskKeys: ["WW2:002"]`)
- **Verifier:** `gemini` (Mac mini specialist worker; **not** elected Chief — `chief_relay.py status` at `2026-11-24T17:39Z` shows **`Chief: Codex`** UP/ready, `gemini` UP/ready, `claude` down until `2026-11-24T17:50:00Z`)
- **Checked at:** `2026-11-24T17:40Z`–`2026-11-24T17:43Z`
- **Waiting condition checked:** `New approved v06 qfc6EBStOfo is Public and its saved B/C/D Thumbnail-only test reads Running. Old v05 J9WGu8aPnHI is retired Private with no schedule. Preserve both tests; never restart.` (`hold.type: public`)
- **Spend / mutations:** `£0.00` (zero YouTube/Studio edits, zero clicks on Save/Set/Stop/Delete, zero uploads/schedule/privacy/thumbnail/title changes, zero new browser tabs, zero NAS writes, zero public watch-page opens)
- **Capabilities note:** Read-only YouTube Data API v3 (`YOUTUBE_REFRESH_TOKEN_WW2`), YouTube public oEmbed, live YouTube Studio CDP `9224` (existing tab reused via `studio.youtube.com`, read-only DOM + visual screenshot inspection), NAS SHA-256 verification, and git/thread inspection. No `audio_input` or `moving_video_input` perception claimed or required.

---

## Advisory Verdict for Elected Chief (`codex`)

**CONDITION PROVEN SATISFIED — RECOMMEND ELECTED CHIEF (`codex`) REOPEN `J3417` WITH THIS EVIDENCE AND CLOSE `J3593`.**

Every element of `J3417`'s waiting condition is proven live (not inferred from the clock):

1. **New approved v06 `qfc6EBStOfo` is `Public`:**
   - **YouTube Data API v3** (`2026-11-24T17:42:10.085Z`, Field Order History `UCu94mInMFosxu3W0H6jlI6Q`): `privacyStatus: "public"`, `publishedAt: "2026-11-24T17:00:12Z"`, `publishAt: null`, `uploadStatus: "processed"`, `madeForKids: false`, `duration: "PT22M28S"`, `title: "How the U-Boats Lost Their Safest Hunting Ground"`.
   - **Public YouTube oEmbed** (`2026-11-24T17:40Z`): `HTTP 200` (`"title":"How the U-Boats Lost Their Safest Hunting Ground"`, `"author_name":"Field Order History"`).
   - **YouTube Studio CDP `9224`** (`2026-11-24T17:42:31.987Z`, `https://studio.youtube.com/video/qfc6EBStOfo/edit`, verified `CHANNEL_ID: UCu94mInMFosxu3W0H6jlI6Q`): `ytcp-video-metadata-visibility` reads **`Visibility / Public`**; Audience reads *"This video is set to not 'Made for Kids' (Set by you)"*; Playlist shows *"How WW2 Was Engineered, Supplied..."* (`PLPPi-oWEDYtA`).
2. **Saved B/C/D Thumbnail-only Test & Compare on `qfc6EBStOfo` reads `Running…`:**
   - **YouTube Studio CDP `9224`** (`2026-11-24T17:42:31.987Z`): `ytcp-thumbnails-experiment-editor` / `ytcp-creator-experiment-status` reads **`Running…`**.
   - **Visual & DOM arm verification:** All three saved Thumbnail-only arms are present in the native experiment strip (`mqdefault_custom_1.jpg`, `mqdefault_custom_2.jpg`, `mqdefault_custom_3.jpg`):
     - Arm 1 (**B**, house control): `LIBERATOR` (`ww2_002_thumb_B_liberator_v01.jpg`)
     - Arm 2 (**C**, `codex`): Flying Liberator BZ877 close crop, no text (`ww2_002_thumb_C_liberator_v03.jpg`)
     - Arm 3 (**D**, `codex`): British convoy ship close crop, no text (`ww2_002_thumb_D_convoy_v03.jpg`)
   - Single title field (`"How the U-Boats Lost Their Safest Hunting Ground"`) confirms Thumbnail-only mode. Test preserved untouched (`Save` / `Undo changes` disabled).
3. **Old v05 `J9WGu8aPnHI` is retired `Private` with no schedule, and its saved test is preserved:**
   - **YouTube Data API v3** (`2026-11-24T17:42:10.085Z`): `privacyStatus: "private"`, `publishAt: null`, `uploadStatus: "processed"`, `madeForKids: false`, `duration: "PT24M4S"`, `title: "How the Allies Closed the U-Boats' Safest Hunting Ground"`.
   - **Public YouTube oEmbed** (`2026-11-24T17:40Z`): `HTTP 403 Forbidden`.
   - **YouTube Studio CDP `9224`** (`2026-11-24T17:42:41.318Z`, `https://studio.youtube.com/video/J9WGu8aPnHI/edit`): `ytcp-video-metadata-visibility` reads **`Visibility / Private`** (no scheduled publish time); `ytcp-creator-experiment-status` reads **`Ineligible`** with all three saved B/C/D arms (`mqdefault_custom_1/2/3.jpg`) still intact and untouched.
4. **Pilot 1 `ek9F61FVYqY` guard preserved:**
   - **YouTube Data API v3** (`2026-11-24T17:42:10.085Z`): `privacyStatus: "public"`, `publishedAt: "2026-11-22T17:00:31Z"`, `publishAt: null`, `duration: "PT23M53S"`, `views: 32`, `likes: 1`, `comments: 1`.
   - **YouTube Studio CDP `9224`** (`2026-11-24T17:42:50.575Z`, `https://studio.youtube.com/video/ek9F61FVYqY/edit`): `Visibility / Public`, `ytcp-creator-experiment-status` reads **`Running…`** with all three Pilot 1 arms intact.
5. **Original gates, NAS media hashes, and Ben approvals remain valid:**
   - Ben's 23 Nov ~09:50 London instruction (*"YouTube is verified please make the changes you feel are needed"*) and 24 Nov ~08:35 London v06 watch approval remain valid. Studio thread `#954` scanned through `#7139557509` (`2026-11-24T17:41:13Z`): zero pause, cancellation, or override on `J3417` or pilot 2 (`qfc6EBStOfo`).
   - `J3417` steps 1–4 deliverables are already merged on `ww2-channel` `main` (`PR #38` merged at `658a126`, one-subject rule live in `00_Brand/PLAYBOOK.md` line 27, `PACKAGING_DECISION_v03.md` and `thumbnail_ab_receipt_v03.json` committed).
   - `J3466` (`done` by `codex`, `2026-11-24T09:06Z`, `#7126958329`) uploaded Ben-approved exact v06 (`SHA-256 1d8bc79a9573ef5cbc399e7d811575f9fa726119cc9828b9aa5f421d19f81d53`) as `qfc6EBStOfo`, saved the B/C/D Thumbnail-only test (`THUMBNAIL_TEST_v06.json`), and retired `J9WGu8aPnHI` Private with no schedule (`OLD_V05_RETIREMENT_v06.json`).

---

## Independent Verification Evidence

### 1. Live YouTube Data API v3 Read-Back (`2026-11-24T17:42:10.085Z`)

| Video ID | Role | Channel ID | Privacy | `publishedAt` | `publishAt` | Duration | Upload Status | Made for Kids | oEmbed HTTP |
|---|---|---|---|---|---|---|---|---|---|
| `qfc6EBStOfo` | Pilot 2 v06 (active) | `UCu94mInMFosxu3W0H6jlI6Q` | **`public`** | `2026-11-24T17:00:12Z` | `null` | `PT22M28S` | `processed` | `false` | `200` |
| `J9WGu8aPnHI` | Pilot 2 v05 (retired) | `UCu94mInMFosxu3W0H6jlI6Q` | **`private`** | `2026-11-21T01:29:56Z` | `null` | `PT24M4S` | `processed` | `false` | `403` |
| `ek9F61FVYqY` | Pilot 1 (guard check) | `UCu94mInMFosxu3W0H6jlI6Q` | **`public`** | `2026-11-22T17:00:31Z` | `null` | `PT23M53S` | `processed` | `false` | `200` |

### 2. Live YouTube Studio CDP `9224` Read-Back (`2026-11-24T17:42:31Z`–`17:42:50Z`)

Reused the single existing `studio.youtube.com` tab on port `9224` (0 new tabs opened; verified via `cdp_tabs.py list --port 9224`).

| Video ID | Inspected UTC | Studio Channel ID | Studio Visibility | Experiment Status | Arms Present | Mutations |
|---|---|---|---|---|---|---|
| `qfc6EBStOfo` | `2026-11-24T17:42:31.987Z` | `UCu94mInMFosxu3W0H6jlI6Q` | **`Public`** | **`Running…`** | 3-arm Thumbnail-only B/C/D (`mqdefault_custom_1/2/3.jpg`) | None |
| `J9WGu8aPnHI` | `2026-11-24T17:42:41.318Z` | `UCu94mInMFosxu3W0H6jlI6Q` | **`Private`** (no schedule) | **`Ineligible`** | 3-arm saved B/C/D preserved (`mqdefault_custom_1/2/3.jpg`) | None |
| `ek9F61FVYqY` | `2026-11-24T17:42:50.575Z` | `UCu94mInMFosxu3W0H6jlI6Q` | **`Public`** | **`Running…`** | 3-arm Pilot 1 B/C/D preserved | None |

### 3. Independent NAS SHA-256 Verification (`2026-11-24T17:42Z`)

Verified directly on `/Volumes/data/studio-live/ww2/02_Video-Projects/002_Closing-The-Atlantic-Black-Pit-May-1943/10_Thumbnail/`:

| File | Bytes | Computed SHA-256 | Matches `THUMBNAIL_TEST_v06.json` |
|---|---:|---|---|
| `ww2_002_thumb_B_liberator_v01.jpg` | `279,309` | `042cdca53c80dbbafef3095cdda1424229598595800648b4757306a8a000d36a` | Present on NAS (house control arm 1) |
| `ww2_002_thumb_C_liberator_v03.jpg` | `367,189` | `8a0a2b8a855f92df26da6655fe7c87a4f72db94e783c6db84a0ee0bd8a675012` | **EXACT MATCH** |
| `ww2_002_thumb_D_convoy_v03.jpg` | `226,282` | `b53116abce8a6c253e8943f5356efd0787951e9b51b920e9115cd6d9854161b7` | **EXACT MATCH** |
| `comparison_v03.png` | `662,338` | `60aa04c50c3661daf2910a0e2f297cfae711da7bf762e3ba9f7d1ba8d1eb78e8` | Present on NAS |

### 4. Remaining `J3417` Scope Note

On `ww2-channel` `main` (`7de038c`):
- `02_Video-Projects/002_Closing-The-Atlantic-Black-Pit-May-1943/status.json` still lists `release.state: "scheduled"` / `privacy: "private"` (from `J3466` pre-launch).
- `11_Upload-Package/THUMBNAIL_TEST_v06.json` still lists `observed_status: "Ineligible"` / `running: false` (from `J3466` pre-launch).
- `00_Brand/Channel-Setup/social/UPLOADS.json` still lists `qfc6EBStOfo.privacyStatus: "private"`.

Once `J3417` is reopened, its final completion step is purely updating those WW2 launch-verification records with the confirmed `Public` (`2026-11-24T17:00:12Z`) and `Running…` (`observed 2026-11-24T17:42:31.987Z`) read-back (preserving both tests; never deleting or restarting either test).

---

## Recommended Action for Elected Chief (`codex`)

1. Review and merge this verification record PR (`gemini/J3593`).
2. Reopen `J3417` with the verified live evidence note and close `J3593`:

```bash
python3 scripts/jobs.py reopen J3417 --agent codex \
  --note "Verified via J3593 (PR #<PR_NUM>, read-only API + Studio CDP 9224 at 2026-11-24T17:42Z): qfc6EBStOfo is Public (publishedAt 2026-11-24T17:00:12Z, oEmbed 200) and its saved 3-arm B/C/D Thumbnail-only test reads Running; old v05 J9WGu8aPnHI is retired Private with publishAt null (oEmbed 403) and its saved test is preserved Ineligible; pilot 1 ek9F61FVYqY Running test untouched; NAS thumb SHA-256 hashes match THUMBNAIL_TEST_v06.json; Ben approvals valid. Final step: record Public + Running observation in ww2-channel pilot 2 records without modifying or restarting any test." \
  --git

python3 scripts/jobs.py done J3593 --agent codex \
  --result "Chief PASS on J3593 (PR #<PR_NUM>): J3417 waiting condition proven satisfied live (qfc6EBStOfo Public 2026-11-24T17:00:12Z & B/C/D test Running at 17:42:31Z; J9WGu8aPnHI Private with no schedule & saved test preserved; ek9F61FVYqY Running untouched). J3417 reopened; zero spend or YouTube mutation." \
  --git
```
