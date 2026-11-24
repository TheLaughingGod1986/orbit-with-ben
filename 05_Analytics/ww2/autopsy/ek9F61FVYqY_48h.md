# Retention Autopsy (48 h) — Field Order History · `ek9F61FVYqY`

- **Film:** `WW2:001` (Pilot 1) — *The Secret Floating Harbours of D-Day* *(launched as "How Britain Built Two Harbours in Secret and Floated Them to Normandy"; retitled `2026-11-23T13:51:35Z` under `J3424`)* (`ek9F61FVYqY`)
- **Published:** `2026-11-22T17:00:31Z` · **Live duration:** `23:52` / `PT23M53S` (`1,432.06 s`, after `J3419` live Studio Editor trim removing the `3:44.64` Dieppe detour `01:27:20–05:12:11` on `2026-11-23T13:11:33Z`; uploaded `v43` master was `27:37` / `1,656.72 s`)
- **Autopsy date:** `2026-11-24` (`J3591`; 48 h Studio read `J3590` collected `2026-11-24T17:17–17:21Z` on CDP `9224`, recorded in `05_Analytics/ww2/launch/ek9F61FVYqY.json`; `05_Analytics/ww2/snapshots/` has no daily API snapshot yet)
- **Reviewer:** Gemini (`gemini`, specialist worker; Gemini 4 Neon moving video + audio verified via `read_file` on five H.264+AAC watch clips cut from `/Volumes/data/studio-live/ww2/02_Video-Projects/001_Mulberry-Harbours-Floating-Ports-D-Day/07_Edit-Project/integrated_v43/mulberry_scored_draft_v43.mp4`)

---

## 1. Relative-Strength Score (RSI)

> **RSI (vs ch / configured reference):** `Showings —/8↓↓ · CTR —/15↓↓ · Views —/3↓↓ · Avg% —/31↓ · 0:30 —/— · Subs/1k —/76↑↑*`

*(Scale: `0–100` where `50→` = on benchmark; `70+ ↑↑` strong, `55–69 ↑` above, `45–54 →` inline, `31–44 ↓` below, `0–30 ↓↓` weak. Formula: `100 × value / (value + benchmark)`. Pilot 1 is Field Order History's first public film, so channel-median RSI is `—` across all six metrics (`n=0 < 3` earlier longs). \*`Subs/1k` is a tiny-sample `n=1` subscriber on `32` views.)*

| Metric | Film (48 h Studio read `J3590`) | Channel median (`ww2`) | Baseline basis | RSI (ch) | Configured reference target (not measured peers) | RSI (reference) |
|---|---:|---:|---|---:|---:|---:|
| Showings (Impressions) | `1,699` *(Overview `1.6k`; funnel `1.5k`)* | `—` | insufficient history (`n=0 < 3`) | `—` | `20,000` | `8↓↓` |
| Click-through (CTR) | `0.8%` *(raw `0.82%`; funnel `0.9%`)* | `—` | insufficient history (`n=0 < 3`) | `—` | `4.5%` | `15↓↓` |
| Views | `32` *(Content list `33`; `2.4` watch h)* | `—` | insufficient history (`n=0 < 3`) | `—` | `1,000` | `3↓↓` |
| Average % viewed | `15.4%` *(raw `15.41%`; Overview `4:00`/15%, Eng. `4:09`)* | `—` | insufficient history (`n=0 < 3`) | `—` | `35.0%` | `31↓` |
| 0:30 retention | `—` *(suppressed: `"Not enough data"` at 32 views)* | `—` | insufficient history (`n=0 < 3`) | `—` | `60.0%` | `—` |
| Subscribers / 1,000 views | `31.25` *(`+1` sub / `32` views; `n=1` caveat)* | `—` | insufficient history (`n=0 < 3`) | `—` | `10.0` | `76↑↑*` |

- **Reference provenance checked (J3596):** `05_Analytics/ww2/niche_benchmarks.json` configures these numbers. Its cited `ww2/00_Brand/PLAYBOOK.md` reports packaging/outlier multiples and a 1,000-impression/3% action threshold; `05_Analytics/new_channel_research/SUMMARY.md` reports public channel/search counts. Neither supplies measured same-age peer impressions, CTR, retention or subscriber conversion supporting the exact table targets. These are configured reference targets, not measured niche medians or validated outlier benchmarks. The RSI arithmetic remains reproducible, but cannot establish relative peer performance. Rule 8’s 2% CTR / 60% at 0:30 / 25% average viewed are separate channel targets.
- **Traffic sources (`Since published`, `J3590`):** Suggested videos `78.8%` (`26` views, predominantly off-niche), Direct or unknown `18.2%` (`6` views, including confirmed pre-launch/signed-out studio checks from `AUDIT_001_2026-11-23.md`), Playlists `3.0%` (`1` view), Browse `0.0%`. Reach funnel (`1.5k` impressions -> `0.9%` CTR -> `14` engaged views -> **`7:17` AVD / `30.5%` of live runtime** -> `1.7` watch hours).
- **Mid-window changes already live (context for 48 h read):**
  - `2026-11-23T09:11:55Z` (`J3411`): Three-arm Thumbnail-only Test & Compare (`B v02` vs `C` vs `D`) started — still **Running untouched** at `24 Nov 17:21Z`.
  - `2026-11-23T13:11:33Z` (`J3419`): Live Studio trim removed `01:27:20–05:12:11` (`224.64 s` Dieppe detour), shortening runtime from `27:37` to `23:52`. Post-trim views (`+13` since `23 Nov 12:45Z`) lifted overall AVD from `3:26` (`12%`) at 20 h to `4:09` (`15.4%`) at 48 h.
  - `2026-11-23T13:51:35Z` (`J3424`): Retitled to *"The Secret Floating Harbours of D-Day"* (40 chars), still omitting `"Mulberry"` (`~6,600` searches/mo) and echoing Real Engineering's `973K` title.

---

## 2. Funnel Diagnosis (Strict Priority Order)

**Primary bottleneck: Step 2 — Click-through (Packaging — Title & Thumbnail)** *(with Step 1 off-niche Suggested traffic mix caveat and Step 4 Pacing/Picture secondary bottleneck, with visual friction observed in the mapped clips; its effect on retention remains unproven).*

1. **Showings (Topic / Search) — `OK ON VOLUME (1,699 >= 1,000 floor), MIX CAVEAT`:** `1,699` impressions in 48 h clears `retention_autopsy.py`'s `1,000`-impression WW2 floor (`RSI — / 8↓↓` vs 20k configured reference). However, the traffic mix is cold-start Suggested (`78.8%` of views, `97.4%` of closed-batch impressions) beside off-niche videos (Nikola Tesla, police drama, theme parks, LA Olympics), with `0.0%` Browse and minimal Search (`14` closed-batch search impressions, `0` clicks). The missing `"Mulberry"` title term is a plausible search-discovery hypothesis. These 32 views do not establish that it caused off-niche recommendations or that YouTube has failed to index the film.
2. **Click-through (Packaging) — `PRIMARY BOTTLENECK`:** **`0.8%` CTR (`0.82%` raw) on `1,699` impressions** (`RSI — / 15↓↓`) sits far below both `retention_autopsy.py`'s `3.0%` WW2 bar and `ww2/studio/RULES.md` Rule 8's `2.0%` first-month bar. Off-niche Suggested placement may contribute to low CTR; causation is unproven. Even in the best hours (`AUDIT_001`), hourly CTR only reached `1.7%–2.3%`. **Guard:** Three-arm Thumbnail Test & Compare (`B v02 / C / D`) is currently **Running** — **never touch or replace it**. The already-queued `J3540` title update (adding `"Mulberry"`, proven safe alongside a Thumbnail-only test by `J3424`) and `J3542` Mulberry Short are the right non-disruptive levers.
3. **First 30 seconds (Hook) — `UNMEASURED (curve suppressed) — WATCH-FLAGGED VISUAL DRAG`:** YouTube suppressed `0:30` retention (`"Not enough data"` at `32` views). Watching `0:00–1:28` directly shows a solid spoken hook (concrete dawn/tug image at `0:00`, stakes by `0:34`, Dieppe detour already removed at `1:27.8`), **undercut visually by an 11-second flat schematic hold at `0:06–0:17`**, a **12-second blank three-box slide at `0:35–0:47`**, visible internal production footers (`Locked J2991 narration`), and wide beige borders shrinking every archive photo.
4. **Mid-film cliffs (Pacing / Picture) — `SECONDARY BOTTLENECK`:** **`15.4%` average viewed** (`4:00` Overview / `4:09` Engagement; `RSI — / 31↓`; below Rule 8's `25%` floor), though engaged funnel viewers held **`7:17` (`30.5%` of live runtime)**. Watching the mapped live `3:49–4:29` overall-AVD proxy window and `6:57–7:37` engaged-AVD proxy window exposes concrete mid-film friction: immediate visual repeats (`IWM A 25814` shown twice 4 s apart; `6,044 TONS` schematic shown twice 11 s apart), text-only beige filler slides with a creeping red underline (`Garlieston, Wigtown Bay` for `10+ s` with no map; `Crew Quarters + Bofors`), visible `J2991` / `Inherited sources` / `locations not reconstructed` compliance boilerplate, and 8 stacked numbers in 35 s (`7:00–7:35`).
5. **End (End Screen / Handoff) — `UNMEASURED (curve suppressed) — WATCH-FLAGGED HANDOFF GAP`:** End retention is suppressed (`—`). End screen (`Subscribe + Best for viewer`) is confirmed intact at `23:32:02–23:52:01`, and the narration lands a strong closing line (*"They brought their harbour with them"*), but the final `20 s` opens with a `12 s` static hold (`IWM A 24084` with upside-down scan ink at top-right) and **zero spoken next-video handoff** (expected on Pilot 1 when no second film was live, but must be fixed once Pilot 2 airs and written into future scripts).

---

## 3. Gemini 4 Neon Watch Notes (Moving Video + Audio)

**Evidence limit:** AVD is a mean, not a measured exit time or cliff. The two AVD-centred windows are inspection proxies; no retention drop location is measured while the curve is suppressed. Five clips comprise four 40-second clips and one 48-second extended opening (208 seconds total). Gemini’s original mapped observations below are preserved; J3596 did not repeat the watch. The live/source mapping is established by `TRIM_RECEIPT_v01.md`, not by ffprobe: source v43 is 27:37, live cut 23:52; after live 01:27.8, add 224.64 seconds to locate the source time. Source ffprobe alone cannot locate a live end screen or live AVD window.

YouTube Analytics returned `0` retention-curve points at `32` views (`"Not enough data"`). Rather than guessing from text or stills, Gemini 4 Neon watched **five** lightweight H.264+AAC MP4 clips cut from `mulberry_scored_draft_v43.mp4` (`27:37`) with full moving video and audio via `read_file`, mapped precisely to the **live trimmed `23:52` timeline** (`v43` timestamps after `01:27.8` shift `-224.64 s` per `TRIM_RECEIPT_v01.md`):

1. **Window 1 — `0:00–0:40` (Opening hook; identical in `v43` and live `23:52` cut; inspection proxy for the opening, not measured `0:30` retention):**
   - **`0:00–0:05`:** Archive photo `IWM A 25799` (tug towing Phoenix caisson, framed inside wide beige margins taking ~45% of screen area; bottom caption + credit). Calm ambient piano/strings bed; narrator opens crisply at `~0:00.2`: *"At dawn on the 7th of June 1944, a day after the first Allied troops landed in Normandy..."* Strong concrete opening.
   - **`0:06–0:17` (11-second sparse schematic hold):** Flat beige/light-blue diagram `BRINGING A HARBOUR TO NORMANDY` (`150 OCEAN TUGS` -> `BARELY FOUR KNOTS` at `0:12`) with four tiny dark tug-and-box silhouettes drifting slowly and visible internal/legalistic footers: `Own explanatory schematic | Not a reconstruction or surveyed route` and **`Locked J2991 narration | Full factual sources in the film package`**. Narrator describes thrilling imagery (*"150 ocean tugs appeared on the horizon... straining on steel hawsers at barely four knots"*), while the screen looks like an internal compliance slide.
   - **`0:18–0:23`:** Archive photo `IWM C 4663` (high-altitude grey aerial mosaic of Mulberry B, boxed in beige margins) over *"hollow concrete blocks, six stories high"* — distant aerial mosaic does not visually sell six-story scale.
   - **`0:24–0:28`:** Animated `A PIER THAT FOLLOWS THE TIDE` schematic (waterline rises/falls with `HINGED WHALE SPANS`, `BEETLE PONTOONS`, `SPUD`, `FIXED LEGS`) — clean teaching visual, though still stamped `J2991: ICE, The Civil Engineer in War, vol. 2 (1948)`.
   - **`0:29–0:34`:** Archive photo `IWM A 24159` (`Blockship line at high tide`, distant horizon silhouettes in beige border).
   - **`0:35–0:40`:** Cuts to `TWO ARMIES NEED DAILY SUPPLIES` — **three completely empty outline boxes** (`FUEL`, `AMMUNITION`, `RATIONS`) on beige with `Combined daily supplies; not 12,000 tons of each category / Locked J2991 narration`.

2. **Window 1b (Extended opening) — `0:40–1:28` (Post-hook setup up to the `1:27.8` live trim splice; identical in `v43` and live cut):**
   - **`0:40–0:47`:** Continues the **three empty outline boxes** (now headed `12,000 TONS EVERY DAY`) — **12 consecutive seconds** (`0:35–0:47`) staring at blank rectangles while VO details daily fuel, ammunition, and rations.
   - **`0:48–0:53`:** Strong archive photo `IWM A 24678` (DUKW unloading cargo net at crane, boxed in wide beige margins).
   - **`0:54–1:05` (12-second flat box schematic):** `THE PORTS ARE WIRED FOR DEMOLITION` (six identical empty rectangles + three red crosses) -> `BUILD THE PORTS IN BRITAIN` (same six empty rectangles + red arrow).
   - **`1:06–1:11`:** Strong archive photo `IWM H 35379` (Phoenix construction in Britain).
   - **`1:12–1:24` (13-second flat box schematic):** `HIDE THE PIECES UNDER WATER` (five empty squares in blue) -> `1.5 MILLION TONS OF CONCRETE AND STEEL` (six empty rectangles + red arrow — near-duplicate of `1:01`), again carrying `Locked J2991 narration`.
   - **`1:25–1:28`:** Repeats `IWM A 25799` (exact opening tug photo from `0:00`, reused 85 s later) over *"across 100 miles of mined sea."* In the live cut, `1:27.8` splices cleanly to Churchill `IWM H 32129` (`TRIM_RECEIPT_v01.md`). **Totals:** `48` of the first `88` seconds (`54.5%`) are sparse PowerPoint-style schematics.

3. **Window 2 — Live `3:49–4:29` (`v43` `7:34–8:14`; centered on `4:00–4:09` Studio average view duration):**
   - **`3:49–3:56`:** Tail of `A PIER THAT FOLLOWS THE TIDE`, then portrait photo `IWM A 25826` (Commander Robert Lochner at drafting table — narrow vertical photo surrounded by ~65% empty beige pillarboxes).
   - **`3:57–4:00`:** `WAVE ENERGY NEAR THE SURFACE` (three sine lines; footer `Inherited sources: J2991 S5 (ICE, 1948); S6 (Hartcup, Code Name Mulberry)`).
   - **`4:01–4:07`:** Archive photo `IWM A 25814` (`Bombardon experiments | Weymouth Bay, April 1944`) while VO introduces the 200-foot floating steel cross.
   - **`4:08–4:11`:** `LOWER ARM FLOODED` cross schematic.
   - **`4:12–4:18` (Immediate 4-second repeat):** Cuts right back to the **exact same archive photo `IWM A 25814`**, now captioned `Bombardon experiments | Weymouth Bay, April 1944 | not the test results`.
   - **`4:19–4:29` (10+ second text-only filler slide):** Plain beige slide with **no map, no photo, and no diagram** — just text `GARLIESTON, WIGTOWN BAY / Secret experimental port | Southwest Scotland` (`4:19–4:27`) -> `THE CONDITIONS HAD TO MATCH / Tides, mudflats and gales` (`4:28+`) with a thin red line creeping across the bottom while VO describes Scotland vs Normandy's tides. Ambient piano music remains completely flat across the entire segment.

4. **Window 2b (Engaged-viewer exit) — Live `6:57–7:37` (`v43` `10:42–11:22`; centered on Reach funnel `7:17` engaged AVD):**
   - **`6:57–6:59`:** `A PIER THAT FOLLOWS THE TIDE` schematic reused for a **third** time.
   - **`7:00–7:05`:** Strong archive photo `IWM A 25792` (Phoenix caissons under construction, Southampton).
   - **`7:06–7:12`:** Animated grid counter (`65` -> `212` caissons filling in; clean visual, marred by `Inherited J2991 sources... | Locked narration unchanged`).
   - **`7:13–7:22`:** `A CONCRETE GIANT THAT COULD FLOAT` (`204 feet long`, `60 ft`, `6,044 TONS`) -> `56 FEET 3 INCHES` plain square.
   - **`7:23–7:28`:** Strong archive photo `IWM H 40320` (Phoenix construction with cranes).
   - **`7:29–7:33` (Immediate 11-second repeat):** Shows the **exact same `A CONCRETE GIANT THAT COULD FLOAT` (`6,044 TONS`) schematic again** (`11 s` after it left screen).
   - **`7:34–7:37` (Text-only disclaimer slide):** Plain beige text slide `CREW QUARTERS + BOFORS / Equipment named in the narration; locations not reconstructed` with creeping red line. **Figure stacking:** VO packs **8 separate figures in 35 seconds** (`147`, `65`, `212`, `204 ft`, `56 ft 3 in`, `60 ft`, `6,044 tons`, `40 mm`).

5. **Window 3 — Live `23:12–23:52` (`v43` `26:56.7–27:36.7`; final `40 s` including `23:32–23:52` end-screen window):**
   - **`23:12–23:26`:** Alternates `FOUR MILLION TONS OF SUPPLIES` (`2.5M+ men / 500k vehicles / 4M tons`, footer `Values inherited from locked J2991 narration`), archive photo `IWM B 7236` (coaster unloading at Spud pierhead), and `220,000 TROOPS ON ITS ROADWAYS` text slide (`Different units shown separately | No proportional comparison intended`).
   - **`23:27–23:32`:** Archive photo `IWM BU 1021` (Mulberry B aerial, Sept 1944).
   - **`23:33–23:44` (12-second static hold inside end-screen window):** Archive photo `IWM A 24084` (Phoenix caisson towed into position, with visible upside-down handwritten scan markings at top-right).
   - **`23:45–23:52` (Final 7 s):** Archive photo `IWM BU 1024` (Mulberry B aerial) over closing line *"...an invading army no longer had to capture a harbour to liberate Europe. They brought their harbour with them."* Clean audio close, **zero spoken handoff** to a next video or playlist.

---

## 4. Concrete Fixes (Max 3)

1. **[this video — Title & Short handoff; keep running Thumbnail Test & Compare untouched]:** Do **not** touch, pause, or replace the running three-arm Thumbnail Test & Compare (`B v02 / C / D`, live since `23 Nov 09:12Z`). Execute the already-queued `J3540` title update to put `"Mulberry"` (`~6,600` searches/mo) into the title via API (proven non-disruptive to the Thumbnail-only test by `J3424`) and ship the already-queued `J3542` Mulberry Short pointing to `ek9F61FVYqY`. Once Pilot 2 (`WW2:002`) is public, point `ek9F61FVYqY`'s `Best for viewer` end-screen card directly at Pilot 2.
2. **[next film — Picture & On-Screen Graphics Hygiene (films 003–006+ edits)]:** Strip every internal job ID and production disclaimer (`J2991`, `Locked narration`, `Inherited sources`, `locations not reconstructed`) from on-screen graphics before render. Ban blank-box and text-only beige filler slides (`0:35–0:47` empty outlines, `4:19–4:29` text-only `Garlieston` slide, `7:34–7:37` `Crew Quarters`): replace location call-outs with real code-drawn maps and replace repeated spec cards with full-bleed / wider-framed archive photographs. Enforce a `≥60 s` cooldown against repeating the same archive photo or schematic (`IWM A 25814` repeated in `4 s`; `6,044 TONS` schematic repeated in `11 s`).
3. **[next film — Pacing, Figure Density & Spoken End-Screen Bridge]:** Enforce `ww2/studio/RULES.md` Rule 4 (*one figure at a time, rounded*) across middle engineering chapters as well as openings (avoid 8 stacked figures in 35 s as at `7:00–7:35`), introduce subtle music dynamics at chapter turns, and script a concise 10–15 s spoken bridge into the next Field Order History film or playlist across the final 20 s end-screen window instead of ending on a 12 s static hold with no handoff.

---

## 5. Repeatable Lesson for `LEARNINGS.md`

- Logged as **Row #10** in Field Order History's own ledger (`ww2/studio/LEARNINGS.md`, opened via PR for Chief Codex review): direct Gemini 4 Neon moving-video + audio watch of `ek9F61FVYqY` (`48 h`: `1,699` impressions, `0.8%` CTR, `32` views, `15.4%` avg viewed) demonstrated that internal job-ID footers (`Locked J2991 narration`), blank/text-only beige filler slides (`54.5%` of `0:00–1:28`, plus `10+ s` text-only `Garlieston` in the `4:09` AVD inspection proxy), wide beige matte borders, and `4–16 s` visual repeats were judged visually distracting; the overall average viewed was below 25% (not a measured mid-film retention point), with no established causal link even after the `3:45` opening detour was trimmed.
