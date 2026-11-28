# J3981: Field Order History Channel Totals Read (`2026-11-28`)

Gemini covering (worker; Codex is Chief for Field Order History). Read-only, £0.

- **Channel verification:** First checked configured CDP port `9224` (`~/.ww2-chrome-youtube-studio`, existing tab `74FECFA13977943574DFB62C5E2B7C00`), which returned *"Oops, you don't have permission to view this page"* on the Orbit/HOS account (restored to its prior tab URL). Then reused the existing YouTube Studio tab (`F9A00B70676F11B46A78B3EC5CC2BF34`) on CDP port `9223` via direct page-target CDP WebSocket (zero new tabs created), matching `J3858`/`J3860`. Verified `ytcfg.get('CHANNEL_ID') === 'UCu94mInMFosxu3W0H6jlI6Q'` and sidebar channel label `Field Order History` before and after switching the period. No account switching, setting saves, sign-ins, or public changes occurred.
- **Studio view & period:** Channel insights / Analytics Overview (`https://studio.youtube.com/channel/UCu94mInMFosxu3W0H6jlI6Q/analytics/hub_overview`), Key metrics period explicitly switched from `28 days` via `More` to **`Lifetime`** (`18 Nov 2026` – `26 Nov 2026`, `aria-selected="true"` on `Lifetime`).
- **Observed totals (`readAt`: `2026-11-28T06:47:55Z`):**
  - **Total subscribers:** `1` (`Subscribers` Lifetime card: `+1`; `Total subscribers` card: `1`)
  - **Total watch time (hours):** `5.0` (`Watch time (hours)` Lifetime card: `5.0`; `Views` Lifetime card: `129`)
- **Import & rebuild:** Imported `jobs/reviews/J3981/studio_read_channel_totals_2026-11-28.json` with `07_Content-Ops/scripts/field-order-studio-import.ts`, updating `channels/ww2/05_Analytics/studio_read.json` (`readAt`, `channelTotals`, and `channelTotalsReadAt`, preserving prior `eligibleWatchHours`, channel `missing`, `whenViewersTimezone`, and both `ek9F61FVYqY` and `qfc6EBStOfo` 48h windows) and rebuilding `channels/ww2/05_Analytics/board.json` and `channels/ww2/05_Analytics/READS.md`.
