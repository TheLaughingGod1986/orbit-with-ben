# J3437 Condition Verification Review — J3429 (`WW2 film 004: top up the archive photographs to about two-thirds of screen time before the edit`)

- **Verification Job:** `J3437` (`Verify condition for J3429`, `recheck_of: J3429`, `repo: owb`, `kind: review`, `needs: mini`, `open_claim: true`, `due: 2026-11-23T17:41:11+00:00`)
- **Parent Job:** `J3429` (`WW2 film 004: top up the archive photographs to about two-thirds of screen time before the edit`, `status: blocked`, `by: codex`, `repo: ww2`, `film: WW2:004`, `stage: picture`, `kind: image`, `due: 2026-11-26T18:00:00Z`, `hold.type: input`)
- **Verifier:** `macbook-2` (MacBook worker; `chief_relay.py status` elects **Chief: Codex (`codex` UP)** while `claude` is out of usage until `2026-11-23T17:50:00Z` and `chief` / Grok Bot is down — no Chief ruling, no PR merge, no hold release/reopen, no spend, no NAS writes, no YouTube/Studio changes)
- **Checked At:** `2026-11-23T16:45Z` – `2026-11-23T16:50Z`
- **Spend & Side Effects:** `£0.00` (`0` credits spent; read-only HTTP binary verification and SHA-256 checks; downloaded test bytes decoded in ephemeral temp dir and discarded; zero NAS/YouTube/schedule writes; no PR merged)
- **Advisory Verdict (Parked for Elected Chief `codex`):** **CONDITION SATISFIED (MET) — recommend elected Chief merge this PR, reopen `J3429` (`jobs.py reopen J3429 --agent codex --note "..." --git`), and close `J3437`.** Parked `J3437` for the elected Chief because PR merges and releasing a verified hold (`scripts/jobs.py` `do_reopen`: `"Only the elected Chief may release a verified hold"`) are protected Chief actions.

---

## 1. Recorded Waiting Condition on `J3429`

At `2026-11-23T15:49Z` (studio thread `#7106174560`, draft `ww2-channel` PR `#49` commit `dab29f8`), `codex` preserved the 41-paragraph picture plan and 50 provenance records (9 existing hash-verified NAS photos + 41 catalogued candidates) and placed `J3429` on a typed `input` hold:

> *"Public archive binary delivery must work again: Commons original and standard 1920-pixel thumbnail downloads returned HTTP 429; Flickr original returned 429 and resized image 403; NHHC direct pages returned 404 on 23 Nov. Nine existing NAS photos hash-verified. Resume draft ww2 PR 49, retrieve and inspect 41 additional distinct photographs (replace failed candidates), then finalise the 41-paragraph plan. Current 57.6% is proposed only and 123 seconds below two-thirds. No new files delivered and no stage PASS."*

---

## 2. Independent Verification of Public Archive Binary Delivery (`2026-11-23T16:46Z–16:49Z`)

First verified `origin/codex/J3429-archive:02_Video-Projects/004_Why-US-Submarine-Torpedoes-Failed-21-Months/03_Picture/ARCHIVE_CANDIDATES_J3429.json`:
- **Total records:** `50` (`9` hash-verified on NAS + `41` `candidate only` records).
- **Candidate host breakdown (41 candidates):**
  - `commons.wikimedia.org` / `upload.wikimedia.org`: **`22`** candidates (`C01`–`C22`)
  - `www.flickr.com` (`photos/national_museum_of_the_us_navy`): **`19`** candidates (`C23`–`C41`)
  - Direct NHHC (`www.history.navy.mil`) download dependencies: **`0`** candidates.

### 2.1 Wikimedia Commons (Originals + 1920px Thumbnails) — **PASS (HTTP 200)**

Using a Wikimedia-policy-compliant descriptive `User-Agent` (`FieldOrderHistoryArchiveVerifier/1.0 (https://github.com/TheLaughingGod1986/ww2-channel)`, no email address) with polite 1.5 s pacing:

| Candidate / Endpoint | HTTP | Size / Type | Image Verification (`sips` / magic) |
|---|---:|---|---|
| **C01 original** (`upload.wikimedia.org/.../Aerial_view_of_Gould_Island_(Rhode_Island)_on_29_March_1943.jpg`) | **200** | `9,420,822 B` (`image/jpeg`) | Full download decoded: **`5711×3938` JPEG**, SHA-256 `83842833363b1afa...` |
| **C01 1920px thumb** (`thumb.wikimedia.org/.../1920px-...jpg` via API) | **200** | `489,153 B` (`image/jpeg`) | Valid JPEG header (`ffd8ffe2...`) |
| **C01 1920px thumb** (`upload.wikimedia.org/.../thumb/.../1920px-...jpg`) | **200** | `489,153 B` (`image/jpeg`) | Valid JPEG header (`ffd8ffe2...`) |
| **C02 original** (`upload.wikimedia.org/.../NARA_-_520834.tif`) | **200** | `6,309,281 B` (`image/tiff`) | Valid TIFF header (`49492a00...`) |
| **C02 1920px thumb** (`thumb.wikimedia.org/.../lossy-page1-1920px-...tif.jpg`) | **200** | `1,173,083 B` (`image/jpeg`) | Full download decoded: **`1920×2739` JPEG**, SHA-256 `bc13872ec9168821...` |
| **C03 original** (`upload.wikimedia.org/.../NARA_-_520835.tif`) | **200** | `7,056,282 B` (`image/tiff`) | Valid TIFF header (`49492a00...`) |
| **C04 original** (`upload.wikimedia.org/.../NARA_-_520829.tif`) | **200** | `8,955,282 B` (`image/tiff`) | Valid TIFF header (`49492a00...`) |
| **C05 original** (`upload.wikimedia.org/.../RADM_Ralph_W_Christie_and_LCDR_Walter_T_Griffith_on_USS_Bowfin.png`) | **200** | `11,222,753 B` (`image/png`) | Valid PNG header (`89504e47...`) |

**Root-cause diagnostic on Wikimedia `User-Agent` (Range `bytes=0-1023` on C01 original at `16:49Z`):**
- `curl/8.7.1` → **HTTP 429** (`Retry-After: 120`, Wikimedia Error page).
- Default `Python-urllib` → **HTTP 403** (`Please set a user-agent and respect our robot policy https://w.wiki/4wJS`, T400119).
- Descriptive project `User-Agent` → **HTTP 206 OK** (`1024 B`) immediately.

### 2.2 Flickr (`national_museum_of_the_us_navy` Originals `_o.jpg` + Resized `_b.jpg`) — **PASS (HTTP 200)**

| Candidate / Endpoint | HTTP | Size / Type | Image Verification (`sips` / magic) |
|---|---:|---|---|
| **C23 (`15091267159`)** photo page + `_b.jpg` resized | **200** | `image/jpeg` | Valid JPEG header (`ffd8ffff...`) |
| **C23 (`15091267159`)** `/sizes/o/` + `live.staticflickr.com/..._ba20f98fae_o.jpg` | **200** | `1,800,458 B` (`image/jpeg`) | Full download decoded: **`1796×2448` JPEG** (≥1,600 px), SHA-256 `7872f5f51070a321...` |
| **C24 (`15091268389`)** photo page + `_b.jpg` + `/sizes/o/` + `..._f55f9054de_o.jpg` | **200** | `1,545,498 B` (`image/jpeg`) | Valid JPEG header (`ffd8ffe1...`) |
| **C25 (`20517630820`)** `/sizes/o/` + `live.staticflickr.com/..._8bdf252a90_o.jpg` | **200** | `2,013,082 B` (`image/jpeg`) | Full download decoded: **`2839×2120` JPEG** (≥1,600 px), SHA-256 `84b7e19bd4ff3c50...` |

Range check on Flickr `C23` `_o.jpg` returned **HTTP 206** across all three UAs (default `Python-urllib`, `curl/8.7.1`, descriptive UA).

### 2.3 NHHC & Auxiliary Public Archives — **Status Note (Non-Blocking)**

- **NHHC (`www.history.navy.mil`):** Both `80-G-K-1016.html` and `our-collections/photography.html` still return **HTTP 404** via `curl` (system trust store). Because **0 of 41** PR #49 candidates depend on direct NHHC downloads (all 41 are hosted on Commons or Flickr US Navy official collections), NHHC 404 does **not** block J3429 completion.
- **NARA Catalog Search API (`catalog.archives.gov/proxy/records/search?q=520834&limit=1`):** Returns **HTTP 200** (`application/json`).
- **Library of Congress (`/photos/?fo=json`):** Returned **HTTP 403**; not required for the 41 PR #49 candidates.

---

## 3. Existing Gates, Approvals & NAS Integrity Check

| Check | Evidence | Status |
|---|---|---|
| **Ben's authorisation & rules** | Ben, Mon 23 Nov ~14:15 London (recorded in `J3429` brief): build WW2 films 3–6 properly to `ww2-channel/studio/RULES.md` (rules 1–6, 12). Guards (`£0`, no AI pictures, narration & title untouched) unchanged. | **VALID** |
| **Upstream `J3000`, `J3206`, `J3207`, `J3427`** | All `status: done`. `ww2-channel` PR `#13` (`J3207`), `orbit-with-ben` PR `#1010` (`J3000`), and draft `ww2-channel` PR `#49` (`codex/J3429-archive`, `dab29f8`) remain open and intact. | **VALID** |
| **Downstream `J3430` (edit)** | `status: open`, `after: J3429`, `due: 2026-12-02T20:00:00Z`. Properly waiting on `J3429`. | **ALIGNED** |
| **Existing 9 NAS photographs** | Independently re-hashed all 9 files under `/Volumes/data/studio-live/ww2/02_Video-Projects/004_Why-US-Submarine-Torpedoes-Failed-21-Months/03_Picture/archive/`: `A09`, `N01`, `N02`, `N03`, `N04`, `N07`, `N08`, `N11`, `N12` — **`9/9` exact SHA-256 matches** against PR `#49` `ARCHIVE_CANDIDATES_J3429.json`. | **VERIFIED** |

---

## 4. Recommended Chief Actions & Next-Worker Notes

1. **Merge this evidence PR** (`macbook/J3437`, `jobs/reviews/J3437/REVIEW.md`).
2. **Reopen `J3429`** (`jobs.py reopen J3429 --agent codex --note "J3437 verified (2026-11-23T16:46Z-16:49Z): Commons originals (C01-C05, e.g. C01 5711x3938 JPG) and 1920px thumbs (C01/C02) return HTTP 200 with descriptive project User-Agent (curl/8.7.1 triggers HTTP 429 and default urllib triggers HTTP 403); Flickr national_museum_of_the_us_navy /sizes/o/ originals (C23 1796x2448, C24, C25 2839x2120) and _b.jpg resized return HTTP 200; 0/41 PR #49 candidates depend on NHHC (still 404). 9/9 NAS photos SHA-256 verified; upstream J3000/J3206/J3207/J3427 done and Ben authorisation intact. Resume draft ww2 PR #49 with descriptive User-Agent and polite pacing." --git`).
3. **Close `J3437`** (`jobs.py reopen J3437`, claim, `jobs.py done J3437 --agent codex --ref <PR URL> --git`) after reopening `J3429`.
4. **Operational notes for the worker resuming `J3429` on `ww2-channel` PR `#49`:**
   - **Always set a descriptive project `User-Agent`** (no email address) on every Wikimedia Commons request and pace fetches (~1.5–2 s delay, single-threaded) — default `curl` UA hits Wikimedia `HTTP 429` and default `Python-urllib` hits `HTTP 403`.
   - For Flickr `national_museum_of_the_us_navy` candidates, resolve the original `_o.jpg` URL from each photo's `/sizes/o/` page so images meet the ≥1,600 px target where available.
   - Note that these HTTP probes ran from the MacBook (`macbook-2`); if the Mini ever hits a transient per-IP throttle on Wikimedia, respect `Retry-After` and keep the descriptive `User-Agent`.
   - Remember that PR `#49`'s provisional 50-record plan is currently `57.6%` (`~123 s` short of two-thirds); visually inspect every downloaded photo on a contact sheet, replace any failed/unusable candidates, and either top up additional genuine US federal public domain / UK Crown expired photos to reach ~two-thirds or state plainly where the archive gap remains.
