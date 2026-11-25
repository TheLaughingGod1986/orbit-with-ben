# J3682: Field Order History Channel Totals Read (`2026-11-25`)

Gemini covering (elected acting Chief for Field Order History). Read-only, £0.

- **Channel verification:** Reused the existing YouTube Studio tab (`172EFA2B00ECF24FD255662A998ED48B`) on configured CDP port `9224` via direct page-target CDP WebSocket (zero new tabs created). Verified `ytcfg.get('CHANNEL_ID') === 'UCu94mInMFosxu3W0H6jlI6Q'` (Field Order History) before and after navigation. No account switching, setting saves, sign-ins, or public changes occurred.
- **Studio view & period:** Channel insights / Analytics Overview (`https://studio.youtube.com/channel/UCu94mInMFosxu3W0H6jlI6Q/analytics/hub_overview`), Key metrics period explicitly switched from `28 days` to **`Lifetime`** (`18 Nov 2026` – `23 Nov 2026`, `aria-selected="true"` on `Lifetime`).
- **Observed totals (`readAt`: `2026-11-25T07:08:34Z`):**
  - **Total subscribers:** `1` (`Subscribers` Lifetime card: `+1`; `Total subscribers` card: `1`)
  - **Total watch time (hours):** `2.4` (`Watch time (hours)` Lifetime card: `2.4`; `Views` Lifetime card: `32`)
- **Import & rebuild:** Imported `jobs/reviews/J3682/studio_read_channel_totals_2026-11-25.json` with `07_Content-Ops/scripts/field-order-studio-import.ts`, updating `channels/ww2/05_Analytics/studio_read.json` (`channelTotals` and `channelTotalsReadAt`, preserving prior `eligibleWatchHours`, channel `missing`, `whenViewersTimezone`, and `ek9F61FVYqY` 48h window) and rebuilding `channels/ww2/05_Analytics/board.json` and `channels/ww2/05_Analytics/READS.md`.
