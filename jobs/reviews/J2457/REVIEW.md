# J2457 — Studio Read-Only Check: Thumbnail & Title Test and Compare Status

- **Checked at:** `2026-11-10T02:46Z`
- **Agent:** `macbook-2`
- **Mode:** Strictly read-only in YouTube Studio (`reuse_page(ctx, "studio.youtube.com")` via `scripts/cdp_tabs.py`; modals closed via `Escape`; no edits, saves, replacements, or new tests started).
- **Channel verification:**
  - **CDP `9223`:** Verified channel `Orbit With Ben` (`window.ytcfg.get('CHANNEL_ID') === 'UC_esArsDKd3GJvOkeO0DUog'`) before opening video pages.
  - **CDP `9222`:** Verified channel `History of Science` (`window.ytcfg.get('CHANNEL_ID') === 'UCXp7HkBIl1LgaznXuZHJyRg'`) before opening video pages.

---

## Summary Table (One Row per Video)

| Waiting Job | Channel & Video | Test Inspected | Running or Ended | End Date / Time Remaining | Winner or No Winner | Impressions per Arm (& Video Reach Totals) | Verdict |
|---|---|---|---|---|---|---|---|
| **J0275** | **OWB** `55AEQwvs36g` (*How Long Do Saturn's Rings Have Left?*) | Thumbnail-only A vs B (`HOW LONG?` house vs `RINGS ARE FALLING` cursor, armed 27 Oct by `J0189` / `T013`) | **Still running** (`Test running…`) | Ends **`2026-11-10` ~`22:02Z`** (`Estimated time remaining: 19 hours 16 minutes…` at `02:46Z`) | **No winner yet** (`Not enough information to display data. Please check back later.`; watch-time share: A = `—`, B = `—`) | Per-arm impressions **not shown** by Studio (`3 views since test start` in modal header). Video Reach (`11 Oct – 8 Nov`): `1.3k` impressions, `2.1%` CTR, `217` views, `26` engaged views. | **CONDITION UNMET** (look again **`2026-11-11`**) |
| **J1198** | **OWB** `VBaYRPp85Sw` (*What Happened to Venus?*) | Thumbnail-only `T011` A vs B (`MELTS LEAD` house vs `EARTH'S TWIN` gemini, armed 26 Oct by `J0962`) | **Ended** (`Results ready` / `Test finished`) | Ended **`2026-11-09` at `01:10`** (`Ran from 26 October 2026 at 00:12 to 9 November 2026 at 01:10`) | **No winner** (`Not enough impressions to declare a winner`; A `Now visible to all viewers`; watch-time share: A = `—`, B = `—`) | Per-arm impressions **not shown** by Studio (`229 views during test period` in modal header). Video Reach (`25 Oct – 8 Nov`): `1.3k` impressions, `2.0%` CTR, `230` views, `26` engaged views, `0.73h` watch time. | **CONDITION MET (reopen)** |
| **J1130** | **HOS** `AL_-qlWko_g` (*How Did We Discover the Periodic Table?*) | Thumbnail-only `T023` A vs B (`HOW DID WE DISCOVER THE PERIODIC TABLE?` house vs `THE MISSING ELEMENT` v02 cursor, armed 29 Oct by `J1129`) | **Still running** (`Test running…`) | Ends **`2026-11-12` ~`00:00Z`** (`Estimated time remaining: 1 day 21 hours…` at `02:46Z`) | **No winner yet** (`Not enough information to display data. Please check back later.`; watch-time share: A = `—`, B = `—`) | Per-arm impressions **not shown** by Studio. Video Reach (`17 Sept – 8 Nov` lifetime): `1.1k` impressions, `3.5%` CTR, `161` views, `39` engaged views (`246` impr / `5.28%` CTR in 28d). | **CONDITION UNMET** (look again **`2026-11-13`**, day after test ends) |
| **J0978** | **HOS** `GHZDsiH7L7A` (*What's Really Inside an Atom?*) | Title & thumbnail A/B/C (`What's Really Inside an Atom?` vs `Why Is the Periodic Table in This Order?` vs `How Small Can You Cut Gold?`, `J0280`) | **Ended** (`View test report` / `Test finished`) | Ended **`2026-10-29` at `17:54`** (`Ran from 15 October 2026 at 18:00 to 29 October 2026 at 17:54`) | **No winner** (`Not enough impressions to declare a winner`; A `What's Really Inside an Atom?` `Now visible to all viewers`; watch-time share: A = `—`, B = `—`, C = `—`) | Per-arm impressions **not shown** by Studio. Video Reach (`15 Oct – 8 Nov`): `816`–`817` impressions, `1.2%` CTR, `24` views, `10` engaged views, `0.35h` watch time. | **CONDITION MET (reopen)** |

*(Context note on `J0275`'s other video, OWB Jupiter `-jmMROGoZCM`: its `T003` thumbnail test `NO FLOOR?` vs `NO SOLID GROUND?` was already armed on 27 Oct 2026 and is also still `Test running…` with `Estimated time remaining: 16 hours 17 minutes…` at `02:46Z`, ending `2026-11-10` ~`19:03Z`, watch-time share A = `—`, B = `—`, 58 lifetime impressions / 5.2% CTR.)*

---

## Verdicts by Waiting Job

- **J0275 (`55AEQwvs36g` Saturn thumbnail test `J0189` / `T013`):** **CONDITION UNMET** — look again on **`2026-11-11`** (test is still running with ~19h 16m left as of `2026-11-10T02:46Z`, ending ~`2026-11-10T22:02Z`).
- **J1198 (`VBaYRPp85Sw` Venus thumbnail test `T011`):** **CONDITION MET (reopen)** — `T011` ended on **`2026-11-09` at `01:10`** with no winner (`Not enough impressions to declare a winner`; watch-time share `—` on both A and B; A `MELTS LEAD` remains visible to all viewers). Ready to record `T011` in `THUMB_LEDGER.json` and proceed per `J1198`'s draw/no-winner branch.
- **J1130 (`AL_-qlWko_g` HOS Periodic Table thumbnail test `J1129` / `T023`):** **CONDITION UNMET** — look again on **`2026-11-13`** (test is still running with ~1d 21h left as of `2026-11-10T02:46Z`, ending ~`2026-11-12`, and `J1130` specifies starting the day after the thumbnail test has ended).
- **J0978 (`GHZDsiH7L7A` HOS Atom title Test and Compare `J0280`):** **CONDITION MET (reopen)** — `J0280` ended on **`2026-10-29` at `17:54`** with no winner (`Not enough impressions to declare a winner`; watch-time share `—` on all three arms; A `What's Really Inside an Atom?` remains visible to all viewers). Note for Chief: earlier readbacks (`J1269`/`J1630`) noted that the YouTube Data API `videos.update` returned `Precondition check failed` while the finished Studio title-test widget remained attached, and `J2397` also queued a Studio title-only Test & Compare B on `GHZDsiH7L7A`.

---

## Verbatim Studio Modal & Reach Readbacks

### 1. J0275 — OWB Saturn `55AEQwvs36g` (`CDP 9223`)
- **Video details > Thumbnail status:** `Running…` (`A/B testing · 3 views since test start`)
- **Test & Compare modal text:**
  > `Thumbnail only` / `A/B test report` / `3 views since test start`
  > `Test running…`
  > Option A (`How Long Do Saturn's Rings Have Left?`): `— Watch-time share`
  > Option B (`How Long Do Saturn's Rings Have Left?`): `— Watch-time share`
  > `Estimated time remaining: 19 hours 16 minutes…`
- **Analytics > Reach (`11 Oct – 8 Nov 2026`):**
  > `A/B test`: `Not enough information to display data. Please check back later. 19 hours 17 minutes left…`
  > `Thumbnail impressions`: `1.3k` (`96.0% from YouTube recommending your content`) · `2.1% thumbnail click-through rate` · `26` engaged views · `1:27` avg view duration · `0.63` watch time (hours).

### 2. J1198 — OWB Venus `VBaYRPp85Sw` (`CDP 9223`)
- **Video details > Thumbnail status:** `Results ready` (`A/B testing · 229 views during test period`)
- **Test & Compare modal text:**
  > `Thumbnail only` / `A/B test report` / `229 views during test period`
  > `Not enough impressions to declare a winner`
  > Option A (`What Happened to Venus?` — `MELTS LEAD`): `Now visible to all viewers` · `— Watch-time share`
  > Option B (`What Happened to Venus?` — `EARTH'S TWIN`): `— Watch-time share`
  > `Test finished. Ran from 26 October 2026 at 00:12 to 9 November 2026 at 01:10.`
- **Analytics > Reach (`25 Oct – 8 Nov 2026`):**
  > `A/B test`: `Test finished. Ran from 26 October 2026 at 00:12 to 9 November 2026 at 01:10.`
  > `Thumbnail impressions`: `1.3k` (`96.0% from YouTube recommending your content`) · `2.0% thumbnail click-through rate` · `26` engaged views · `1:40` avg view duration · `0.73` watch time (hours).

### 3. J1130 — HOS Periodic Table `AL_-qlWko_g` (`CDP 9222`)
- **Video details > Thumbnail status:** `Running…`
- **Test & Compare modal text:**
  > `Thumbnail only` / `A/B test report`
  > `Test running…`
  > Option A (`How Did We Discover the Periodic Table?`): `— Watch-time share`
  > Option B (`How Did We Discover the Periodic Table?` — `THE MISSING ELEMENT` v02): `— Watch-time share`
  > `Estimated time remaining: 1 day 21 hours…`
- **Analytics > Reach (`17 Sept – 8 Nov 2026`):**
  > `A/B test`: `Not enough information to display data. Please check back later. 1 day 22 hours left…`
  > `Thumbnail impressions`: `1.1k` (`76.2% from YouTube recommending your content`) · `3.5% thumbnail click-through rate` · `39` engaged views · `1:58` avg view duration · `1.28` watch time (hours).

### 4. J0978 — HOS Atom `GHZDsiH7L7A` (`CDP 9222`)
- **Video details > Title status:** `A/B testing titles` · `What's Really Inside an Atom?` · `View test report`
- **Test & Compare modal text:**
  > `Title and thumbnail` / `A/B test report`
  > `Not enough impressions to declare a winner`
  > Option A (`What's Really Inside an Atom?`): `Now visible to all viewers` · `— Watch-time share`
  > Option B (`Why Is the Periodic Table in This Order?`): `— Watch-time share`
  > Option C (`How Small Can You Cut Gold?`): `— Watch-time share`
  > `Test finished. Ran from 15 October 2026 at 18:00 to 29 October 2026 at 17:54.`
- **Analytics > Reach (`15 Oct – 8 Nov 2026`):**
  > `A/B test`: `Test finished. Ran from 15 October 2026 at 18:00 to 29 October 2026 at 17:54.`
  > `Thumbnail impressions`: `816` (`817` on top card; `84.3% from YouTube recommending your content`) · `1.2% thumbnail click-through rate` · `10` engaged views · `2:06` avg view duration · `0.35` watch time (hours).
