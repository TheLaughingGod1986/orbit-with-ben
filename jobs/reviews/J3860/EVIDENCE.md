# J3860: Field Order History Channel Totals Read (`2026-11-27`)

Gemini covering (worker; Codex is Chief for Field Order History). Read-only, £0.

- **Channel verification:** Reused the existing YouTube Studio tab (`F9A00B70676F11B46A78B3EC5CC2BF34`) on CDP port `9223` (which holds the Field Order History Studio session since 26 Nov per Claude's reopen note and J3919; CDP port `9224` showed permission denied on the Orbit/HOS account) via direct page-target CDP WebSocket (zero new tabs created). Verified `ytcfg.get('CHANNEL_ID') === 'UCu94mInMFosxu3W0H6jlI6Q'` and sidebar channel label `Field Order History` before and after navigation. No account switching, setting saves, sign-ins, or public changes occurred.
- **Studio view & period:** Channel insights / Analytics Overview (`https://studio.youtube.com/channel/UCu94mInMFosxu3W0H6jlI6Q/analytics/hub_overview`), Key metrics period explicitly switched from `28 days` via `More` to **`Lifetime`** (`18 Nov 2026` – `26 Nov 2026`, `aria-selected="true"` on `Lifetime`).
- **Observed totals (`readAt`: `2026-11-27T16:45:40Z`):**
  - **Total subscribers:** `1` (`Subscribers` Lifetime card: `+1`; `Total subscribers` card: `1`)
  - **Total watch time (hours):** `5.0` (`Watch time (hours)` Lifetime card: `5.0`; `Views` Lifetime card: `129`)
- **Import & rebuild:** Imported `jobs/reviews/J3860/studio_read_channel_totals_2026-11-27.json` with `07_Content-Ops/scripts/field-order-studio-import.ts`, updating `channels/ww2/05_Analytics/studio_read.json` (`channelTotals` and `channelTotalsReadAt`, preserving prior `eligibleWatchHours`, channel `missing`, `whenViewersTimezone`, and `ek9F61FVYqY` 48h window) and rebuilding `channels/ww2/05_Analytics/board.json` and `channels/ww2/05_Analytics/READS.md`.
