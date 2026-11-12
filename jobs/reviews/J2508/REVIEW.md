# J2508 — Viewing & Listening Review of J2494 Re-Cut Shorts (`Pluto v02`, `Mon 16 v05`, `Wed 18 v06`)

1. `owb_sa_s7_pluto_heart_v02.mp4` (`gmzaCfJF1gA`, airs Sat 14 Nov 11:30Z): **KEEP**
2. `mon16_cant_see_nearest_star_v05.mp4` (`HZGTovJu_TQ`, airs Mon 16 Nov 11:30Z): **FIX** — end card is clean of `c5AdqQsnnys`, but `0:20.23–0:22.63` repeats the `0:00.00–0:02.40` opening Paranal shot immediately before the static end card (and the untouched locked VO lands its spoken surprise `"You can't see it"` at `0:04.28–0:05.69`, after `1.5 s`).
3. `wed18_robot_reach_nearest_star_v06.mp4` (`cwU_0WWeNZ4`, airs Wed 18 Nov 11:30Z): **FIX** — end card is clean of `c5AdqQsnnys`, but `0:13.45–0:16.55` (`3.10 s`, `"ESO star trails at Paranal"`) is a completely frozen still frame (`0.002/fr` median pixel change, zero zoom/pan), first-second motion is below the `10.0` floor (`motion = 9.01`, gate `warn`), and the untouched locked VO does not name `"Voyager 1"` until `0:02.60–0:04.07` or `"75,000 years"` until `0:14.20–0:15.85`.

**Watch-card guidance for Ben (`J2494` `awaits_ben`):**
- **Watch / KEEP:** Card 3 — *"Pluto Short for Sat 14 Nov (re-cut v02)"* (`owb_sa_s7_pluto_heart_v02.mp4`).
- **Skip pending Chief decision / re-cut:**
  - Card 1 — *"Nearest star Short for Mon 16 Nov (re-cut v05)"* (`mon16_cant_see_nearest_star_v05.mp4`) — skip if Chief wants `s06` (`0:20.23–0:22.63`) replaced with a non-repeating shot instead of repeating the opening Paranal clip before the end card.
  - Card 2 — *"Nearest star Short for Wed 18 Nov (re-cut v06)"* (`wed18_robot_reach_nearest_star_v06.mp4`) — skip because `0:13.45–0:16.55` holds a frozen still frame for `3.10 s` (and `0:00–0:01` warns `motion 9.0 < 10`).

---

## Detailed Notes by File

### 1. `owb_sa_s7_pluto_heart_v02.mp4` (`gmzaCfJF1gA`, Sat 14 Nov 11:30Z, `17.60 s`, SHA-256 `ab33a789dbb00411...`) — **KEEP**

- **First second (`0:00.00–0:01.50`):**
  - **Motion at frame 0:** Already moving at frame 0 (`0:00.00`, continuous pan+zoom across New Horizons `PIA19952` rich-colour Pluto heart mosaic; `f0diff = 4.48`, `motion_0_1s = 18.77`, `6.77/fr` median pixel step). First cut at `0:02.70` (`<= 3.0 s`) to `PIA21863`.
  - **9:16 framing:** Full-bleed `1080×1920` (`cover` mode across all 5 plates, `visor = 0.0`), no blurred or black band above or below.
  - **Hook text at frame 0:** `NO CRATERS` (`NO` white, `CRATERS` yellow `#FFD600`) is on screen from `0:00.00` to `0:02.20` (`y = 105`).
  - **Subject and surprise by `1.5 s`:** Spoken line 1 is `"Pluto's heart doesn't have a single crater."` (`0.10–2.62 s`): `"Pluto's"` (`0.10–0.60 s`), `"heart"` (`0.66–0.90 s`), `"doesn't"` (`1.08–1.34 s`), `"have"` (`1.38–1.48 s`), `"a"` (`1.52–1.60 s`), `"single"` (`1.70–2.04 s`), `"crater."` (`2.14–2.62 s`). The subject (`"Pluto's heart"`) and negation (`"doesn't have"`) land inside `1.48 s` alongside the frame-0 hook `NO CRATERS`, with the word `"crater."` completing at `2.14–2.62 s`.
- **On-screen text (every piece read):**
  - `0:00.00–0:02.20` (top): `NO CRATERS`
  - `0:02.90–0:05.85` (centre 16:9 band `y = 724`): `2015` (yellow) / `NEW HORIZONS` (white)
  - `0:09.00–0:14.00` (top `y = 172`): `Pluto's Heart Has` / `No Craters`
  - Lower-third captions (`y = 1497`, max width `68%` = `x 173..907`, clear of right-side phone buttons): `PLUTO'S HEART` (`0.10–1.08`), `DOESN'T HAVE` (`1.08–1.52`), `A SINGLE` (`1.52–2.14`), `CRATER` (`2.14–2.77`), `IN 2015` (`2.77–4.13`), `NEW HORIZONS` (`4.13–5.11`), `FLEW PAST` (`5.11–5.79`), `AND PHOTOGRAPHED` (`5.79–6.79`), `IT` (`6.79–7.39`), `ITS GREAT` (`7.39–7.95`), `PLAIN IS` (`7.95–8.67`), `FROZEN NITROGEN` (`8.67–10.03`), `GAS` (`10.03–10.75`), `NO CRATERS` (`10.75–11.61`), `ANYWHERE ON` (`11.61–12.19`), `IT` (`12.19–13.06`), `AND SOMEHOW` (`13.06–14.00`), `PLUTO'S HEART` (`14.00–14.92`), `STAYS PERFECTLY` (`14.92–15.86`), `SMOOTH` (`15.86–16.76`).
  - No end card, no raw video ID, no stray letters, no typo, no clipped edge. (Minor note: lower-third captions stay active during the `0:02.90–0:05.85` centre overlay and `0:09.00–0:14.00` top title at separate vertical positions without overlapping).
- **Sound (join at `~2.7 s` audited 3× in full mix and isolated `vo_v02.wav`):**
  - Sentence `"Stay, and I'll show you why that's strange."` was excised between `"crater."` (`ends 2.62 s`) and `"In 2015,"` (`starts 2.77 s`). Across three listens, there is **no click, pop, level jump, or clipped breath** at `2.62–2.77 s` (a clean `0.15 s` pause; `"In 2015"` enters briskly right after `"crater."`, with the soft overlay tick at `2.95 s`).
  - Voice is clear over the music bed (`-14.1 LUFS`, `-2.0 dBTP`); no sudden level change; last word `"smooth"` (`15.86–16.31 s`) is complete and unclipped, followed by a `1.29 s` music tail to `17.60 s`.
- **Picture & loop:**
  - All 5 New Horizons plates (`PIA19952` `0:00–0:02.70`, `PIA21863` `0:02.70–0:06.20`, `PIA20726` `0:06.20–0:09.80`, `PIA19936` `0:09.80–0:13.20`, `PIA19937` `0:13.20–0:16.39`) move smoothly (`3.0–7.5/fr` median step). No frozen frame, no flash frame, no mid-body shot repeat.
  - At `0:16.39–0:16.69` (`0.30 s` crossfade), picture blends into the pre-roll trajectory of `PIA19952` (`0:16.69–0:17.60`), stepping seamlessly from the last frame (`0:17.56`) into frame 0 (`0:00.00`).
- **Coherence after trims:**
  - Reads cleanly as one complete thought (*"Pluto's heart doesn't have a single crater. In 2015, New Horizons flew past and photographed it. Its great plain is frozen nitrogen gas, no craters anywhere on it, and somehow Pluto's heart stays perfectly smooth."*) and loops directly back into line 1.

---

### 2. `mon16_cant_see_nearest_star_v05.mp4` (`HZGTovJu_TQ`, Mon 16 Nov 11:30Z, `26.50 s`, SHA-256 `5a2a4c2af8fb2148...`) — **FIX**

- **First second (`0:00.00–0:01.50`):**
  - **Motion at frame 0:** Moving at frame 0 (`0:00.00`, ESO Paranal night-sky time-lapse `uhd_bt_paranal_07` with a `16%` push over `0.0–1.0 s`; `f0diff = 2.08`, `motion_0_1s = 26.34`, first cut at `0:02.40`).
  - **9:16 framing:** Full-bleed `1080×1920` (`visor = 0.0`) on all body plates (`0:00.00–0:22.63`).
  - **Hook text at frame 0:** `TOO` (white) / `FAINT` (yellow) on screen immediately (`0:00.00–0:02.00`).
  - **Subject and surprise by `1.5 s`:** Uses the untouched J0141 locked VO (`"The nearest star to the Sun is out there tonight. You can't see it."`). The subject `"The nearest star"` is spoken at `0:00.10–0:01.12` (`"to the Sun"` `0:01.12–0:01.94`, `"is out there tonight"` `0:01.94–0:03.79`), while the spoken surprise **`"You can't see it"` does not arrive until `0:04.28–0:05.69`** (though `TOO FAINT` is on screen at `0:00.00–0:02.00`).
- **On-screen text (every piece read, including end card `0:22.63–0:26.50`):**
  - `0:00.00–0:02.00` (top): `TOO` / `FAINT`
  - `0:09.00–0:14.00` (centre 16:9 band): `If You Can't See` / `the Nearest Star,` / `How Far Away` / `Is It?`
  - Lower-third captions (`y = 1334`): `THE NEAREST STAR` (`0.10–1.12`), `TO THE SUN` (`1.12–1.94`), `IS OUT THERE` (`1.94–2.78`), `TONIGHT` (`2.78–3.79`), `YOU CAN'T SEE` (`4.28–5.04`), `IT` (`5.04–5.69`), `IT'S CALLED PROXIMA` (`6.00–7.28`), `CENTAURI` (`7.28–8.41`), `A SMALL RED` (`8.66–9.00`, clears at `9.00 s` for the centre title), `OF THE SUN'S` (`14.00–14.52`), `LIGHT` (`14.52–15.33`), `ITS LIGHT STILL` (`15.84–16.84`), `TAKES MORE THAN` (`16.84–17.74`), `FOUR YEARS TO` (`17.74–18.90`), `REACH YOU` (`18.90–19.87`), `THE FULL FILM` (`20.94–22.13`).
  - **End card (`0:22.63–0:26.50`):**
    - 16:9 thumbnail in centre band reads `YOU CAN'T` (white) / `SEE IT` (yellow).
    - Below thumbnail (`y = 1018..1134`, inside the 16:9 band):
      `How Far Is`
      `the Nearest Star?`
      `Your two eyes are a ruler.`
    - **The raw YouTube video ID (`c5AdqQsnnys`) is completely removed.** No stray letters, no typo, no clipped edge, no text under the phone's buttons.
    - *(Note: the end card and spoken VO at `0:20.94–0:24.48` say `How Far Is the Nearest Star?`, the J0141 title when locked; the live YouTube long `c5AdqQsnnys` was later retitled `The Nearest Star Is One You Can't See (And It Has a Planet)`, and `jobs/reviews/J2494/REPORT.md` line 59 misstated what text was on the card).*
- **Sound:**
  - Untrimmed J0141 mix levelled to `-14.2 LUFS / -2.2 dBTP`. Voice is clear over the music bed, no clicks, jumps, or level shifts, and the last word `"star"` (`ends 24.48 s`) is unclipped with a `2.0 s` music fade to `26.50 s`.
- **Picture — why this is flagged `FIX`:**
  - **Repeat of the opening shot at `0:20.23–0:22.63` (`s06`):** To bring Cut 1 from `4.80 s` (`v01`) to `2.40 s` (`v05`), `_recut_026_first_second_J2494.py` split the `4.80 s` opening shot (`uhd_bt_paranal_07`, `98.17–102.97 s` of 026 v06 — the Paranal telescope roof silhouette in the bottom-right corner against the Milky Way) into `0:00.00–0:02.40` (`s01`, `98.17–100.57 s`) and **`0:20.23–0:22.63` (`s06`, `100.57–102.97 s`)**. Because the Short cuts at `0:22.63` to the `3.85 s` static thumbnail end card (`0:22.63–0:26.50`) rather than looping to frame 0, `0:20.23–0:22.63` visibly repeats the opening shot inside the body right before the end card.

---

### 3. `wed18_robot_reach_nearest_star_v06.mp4` (`cwU_0WWeNZ4`, Wed 18 Nov 11:30Z, `23.60 s`, SHA-256 `80e4c86df51417db...`) — **FIX**

- **First second (`0:00.00–0:01.50`):**
  - **Motion at frame 0:** Opens on the Milky Way time-lapse from `0.30–2.90 s` of 026 v06 (`f0diff = 1.89 >= 1.50`, Cut 1 at `0:02.60`), full-bleed `9:16` (`visor = 0.0`), with hook text `75,000` (white) / `YEARS` (yellow) on screen at `0:00.00–0:02.00`.
  - **Opening motion warning:** `gate_shorts_open.py` prints `warn  picture barely changes in the first second (motion 9.0 < 10) — trim the clip's ease-in so frame 0 is already mid-action` and `warn  open plate 13 bits from bSjWiCbB7pY (2026-11-13)`.
  - **Subject and surprise by `1.5 s`:** Uses the untouched J0141 locked VO (`"Our fastest robot leaving the solar system is Voyager 1. Could a robot like it reach the nearest star?"`). By `1.5 s`, the VO has only said `"Our fastest robot leaving..."` (`0.14–1.50 s`); `"Voyager 1"` lands at `0:02.60–0:04.07`, `"the nearest star?"` at `0:05.98–0:07.41`, and the spoken surprise `"75,000 years"` at `0:14.20–0:15.85` (though `75,000 YEARS` is on screen at `0:00.00–0:02.00`).
- **On-screen text (every piece read, including end card `0:19.75–0:23.60`):**
  - `0:00.00–0:02.00` (top): `75,000` / `YEARS`
  - `0:09.00–0:14.00` (centre 16:9 band): `If Voyager Needs` / `75,000 Years,` / `How Far Is the` / `Nearest Star?`
  - Lower-third captions (`y = 1334`): `OUR FASTEST ROBOT` (`0.14–1.28`), `LEAVING THE SOLAR` (`1.28–2.00`), `SYSTEM IS VOYAGER` (`2.00–3.54`), `1` (`3.54–4.07`), `COULD A ROBOT` (`4.42–5.10`), `LIKE IT REACH` (`5.10–5.98`), `THE NEAREST STAR?` (`5.98–7.41`), `VOYAGER MOVES 17` (`8.02–9.00`, clears at `9.00 s` for the centre title), `TAKE ABOUT 75,000` (`14.00–14.94`), `YEARS` (`14.94–15.85`), `AND VOYAGER ISN'T` (`16.04–17.18`), `EVEN HEADING THAT` (`17.18–18.02`), `WAY` (`18.02–18.71`), `THE FULL FILM` (`18.86–19.75`).
  - **End card (`0:19.75–0:23.60`):**
    - 16:9 thumbnail in centre band reads `YOU CAN'T` (white) / `SEE IT` (yellow).
    - Below thumbnail (`y = 1018..1134`, inside the 16:9 band):
      `How Far Is`
      `the Nearest Star?`
      `Could we ever go and look?`
    - **The raw YouTube video ID (`c5AdqQsnnys`) is completely removed.** No stray letters, no typo, no clipped edge, no text under the phone's buttons.
- **Sound:**
  - Untrimmed J0141 mix levelled to `-14.2 LUFS / -2.2 dBTP`. No clicks or pops; voice is clear over the music; last word `"star"` (`ends 21.60 s`) is unclipped with a `2.0 s` music fade to `23.60 s`.
- **Picture — why this is flagged `FIX`:**
  - **Frozen frame for `3.10 s` at `0:13.45–0:16.55` (`s05`, `"ESO star trails at Paranal"`):** Span `(346.50, 3.10)` lifted from `026_NearestStar_v06.mp4` is a **100% static frozen still image** (`0.002/fr` median background pixel difference, `0.39/255` total drift across `3.10 s`, zero zoom and zero pan because `_assemble_026_weekday_shorts_v01.py` only zooms `picture_span.mp4` during `t = 0.0–1.0 s`). In addition, `s04` cuts to this frozen still at `0:13.45`, `0.55 s` before the `9.0–14.0 s` centre title fades out.
  - **Very slow still pushes at `0:02.60–0:08.95` (`s02` and `s03`):** The two Voyager plates (`PIA17049` at `0:02.60–0:05.45` and `PIA14111` dish close-up against a grey gradient at `0:05.45–0:08.95`) have very slow drift (`0.15–0.19/fr`).
