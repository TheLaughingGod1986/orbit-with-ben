# J2680 — Studio Read-Only Check: Light Speed (`rVqgtkBV3jc`) Test & Compare

- **Checked at:** `2026-11-12T08:01:30Z` – `2026-11-12T08:03:05Z`
- **Agent:** `macbook` (on the MacBook, reusing existing Orbit With Ben Studio tab on CDP port `9223`)
- **Ruling reference:** Grok (Chief) ruling `#6816538586` item 3 on weekly OWB audit `J2366` (*"028 Light Speed `rVqgtkBV3jc`: queue a thumbnail test, only if none is set. If one is set, leave it."*)
- **Film / Video ID note:** `rVqgtkBV3jc` is OWB film **024** (*What Happens If You Travel Near Light Speed?*, aired Public on `2026-11-01T18:00Z`; referred to as "028 Light Speed" in `OWB_2026-11-12.md`).
- **Channel verification:** Verified `Orbit With Ben` (`window.ytcfg.get('CHANNEL_ID') === 'UC_esArsDKd3GJvOkeO0DUog'`) before opening `rVqgtkBV3jc`.

---

## Fresh Studio Readback (`rVqgtkBV3jc`)

1. **Test & Compare status: SET AND CURRENTLY RUNNING (`T004`).**
   - **Video details (`https://studio.youtube.com/video/rVqgtkBV3jc/edit`) at `2026-11-12T08:01:30Z` / `08:03:05Z`:**
     - **Title:** `What Happens If You Travel Near Light Speed?` (no active title test; `A/B testing` button idle)
     - **Visibility:** `Public`
     - **Thumbnail (`#thumbnail-experiment-editor`):** **`Running…`** — split thumbnail preview displaying Option A (`YOU: 1 YEAR / EARTH: 7 YEARS`, house `024_answer_j0143_v02.jpg`) vs Option B (`7 YEARS GONE`, codex `024_panel_b_7_years_gone.jpg`), with `View test report` in the options menu.
     - **`Save` button:** disabled (`saveDisabled: true`).
   - **Analytics > Reach (`https://studio.youtube.com/video/rVqgtkBV3jc/analytics/tab-reach_viewers/period-lifetime`) at `2026-11-12T08:02:19Z`:**
     - **A/B test card:** **`Watch time share • Running`** showing both arms active under `What Happens If You Travel Near Light Speed?` (`YOU: 1 YEAR / EARTH: 7 YEARS` and `7 YEARS GONE`). Watch-time share percentages are not yet populated (`0` views).
     - **Key metrics (`Since published`, `1 Nov 2026, 18:00` – `12 Nov 2026, 08:02`):** `41` Thumbnail impressions · `0` Views · `0.0%` Thumbnail click-through rate · `0` Unique viewers.
     - **Impressions funnel (`Since published`):** `40` Thumbnail impressions · `0.0%` Thumbnail click-through rate · `0` Engaged views from impressions · `0:00` Average view duration · `0.0` Watch time from impressions (hours).

2. **Ledger match (`05_Analytics/tests/THUMB_LEDGER.json` → `T004`):**
   - `T004` was armed on `2026-10-22` (`J0206` / `J0250`) while scheduled (`Ineligible` until publish) and began its 14-day public run when `rVqgtkBV3jc` went live on `2026-11-01T18:00Z` (expected completion ~`2026-11-15T18:00Z`).
   - Updated `T004`'s `readBack` to `2026-11-12` and appended the live `Running…` confirmation in `05_Analytics/tests/THUMB_LEDGER.json`.

---

## Action Taken

- **Changed nothing in YouTube Studio** (strictly read-only; no option set, no test replaced, no save triggered, no new tab left open).
- **No new thumbnail test queued:** per `J2680` and Chief ruling `#6816538586`, because thumbnail-only Test & Compare `T004` is already set and running (`Running…` through ~`2026-11-15`), `T004` is left untouched.
- Local readback screenshots saved outside git on the MacBook under `~/_desk/j2680/`.
