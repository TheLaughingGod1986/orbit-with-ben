# J2192: 032 process overlay stills review (J2089 / PR491 `b3b950a17f`)

5 Nov 2026 · Gemini (`gemini-argon`, review lane) · £0.

Inspected all seven full-size transparent PNGs individually at `/Users/benjaminoats/_desk/cache/J2089/process_previews_v01/` (plus `process_previews.jpg`, `PROCESS_MANIFEST_v01.json`, `PROCESS_CHECKS_v01.json`, `PROCESS_VERIFICATION_v01.json`, and `process_graphics.py` at `b3b950a17f`) against `01_Script/titan_landing_script_master_v01.md`, `01_Script/SOURCES.md` (v01 governing table rows 1, 8, 9, 10, 14, 15), and `07_Edit-Project/SHOT_LIST_v04.md` (rows 21, 25, 29, 39, 40, 45).

This is an individual still-frame review only; it is not motion perception, composite contrast verification, or film-stage approval. J2177 retains its separate review of the 17 mechanism stills and the frame-0 / `PIA07232` source rulings.

## Verdict summary: 5 KEEP, 2 FIX

### KEEP (approved to render under `--review-ref J2192`)

1. **`r21_cycle_clouds` — KEEP** (`preview_sha256: 350876b0da640c6c9936328fdf5b8c419086b23729f8b1e2cbbbc824aecc51db`)
   - **Row / Source:** R21, `SOURCES.md` v01 row 8 (`"methane and ethane form clouds, rain, river channels and lakes"`).
   - **Check:** Side-by-side symbolic comparison (`EARTH` / `WATER` vs `TITAN` / `METHANE + ETHANE`) with cloud, falling rain streaks, surface line, and upward evaporation arrow. Full chemistry words avoid missing subscript glyphs; labels are 1–3 words each and match the locked line (`"methane and ethane play the part water plays on Earth: forming clouds, falling as rain..."`) without asserting equal rainfall rates or drawing flat planetary discs. Bounds `[197, 171, 1611, 808]` inside 5% safe area; entry/exit clear.
   - **Sequencing requirement:** Must be separated from `r21_cycle_lakes` by the real Huygens DISR channel mosaic (`PIA07236`, use 2 of 2) in R21.

2. **`r21_cycle_lakes` — KEEP** (`preview_sha256: 59e64e95361fa6ea576c1d4a38811e5716f4edcee4a31b6a201cada1535cd930`)
   - **Row / Source:** R21, `SOURCES.md` v01 row 8 (`"...carves river channels and fills great lakes with liquid natural gas"`).
   - **Check:** Symbolic process diagram (`RAIN` → branching `RIVER CHANNELS` → `LAKES` basin filling) with the gold drainage marker (`r = 8 px`) following the main channel polyline into the lake. Labels are 1–2 words each, clear of the lines and basin, and read with the sound off as a symbolic process rather than a geographic map. Bounds `[181, 161, 1601, 871]` inside 5% safe area; entry/exit clear.
   - **Sequencing requirement:** Insert real imagery (`PIA07236`) between `r21_cycle_clouds` and `r21_cycle_lakes`.

3. **`r25_heated_suit` — KEEP** (`preview_sha256: c35dcd9c320b6b8470c491fc92c97723248d46d8de662722a5bba71d24280c0c`)
   - **Row / Source:** R25, `SOURCES.md` v01 rows 1, 8, 9 (`"Stand on Titan's surface in a suit heated against the deep freeze..."`).
   - **Check:** Symbolic human suit outline with four animated horizontal gold heating bars inside the torso and a single 2-word label `HEATED SUIT` with pointer arrow. Does not prematurely introduce `"own oxygen"` (which is spoken later in R27), and uses no unsourced portrait or invented Orbit. Bounds `[334, 220, 1399, 902]` inside 5% safe area; entry/exit clear.
   - **Sequencing requirement:** In R25, `r25_heated_suit` and `r25_pressure` must NOT run back to back; place the real surface plate between them (`CODE heated-suit → real surface plate → CODE pressure`) once R25's `PIA07232` 3-use conflict is resolved under J2177/Chief.

4. **`r29_rain_comparison` — KEEP** (`preview_sha256: 336df80db8026107f36f575b849d0695091f68cc6acacac719efac8e7ece4efe`)
   - **Row / Source:** R29, `SOURCES.md` v01 row 10 (`"9.5 mm diameter vs 6.5 mm diameter" yet fall much more slowly "(1.6 m s−1 vs 9.2 m s−1)"`).
   - **Check:** Uses `BIGGEST DROPS` per J2150. `EARTH` (`6.5 MM`, `9.2 M/S`) and `TITAN` (`9.5 MM`, `1.6 M/S`, `≈ FALLING SNOWFLAKES`) use a common linear diameter scale (`r = diameter * 9`) and a common linear vertical speed scale (`y = 420 + speed * 10 * t`) with no modulo wrap during the 3.6 s window and no collision with the bottom text rows (`y = 850` and `y = 950`). Bounds `[161, 160, 1572, 989]` inside 5% safe area; entry/exit clear.
   - **Sequencing requirement:** Separated from `r29_rain` in R29 by the real Cassini radar dune strip (`PIA09182`, use 1 of 2).

5. **`r45_lift_mechanism` — KEEP** (`preview_sha256: 12e56e03532d8d217acb5f03aa8836c29ef62ada3511e8a33a9d900eea51f108`)
   - **Row / Source:** R45, `SOURCES.md` v01 row 15 (`"Lift comes from the air, and weight comes from gravity"`).
   - **Check:** Symbolic white airfoil section with four blue incoming airflow arrows (`AIR`) and upward `LIFT` arrow opposing downward gold `WEIGHT` arrow (`GRAVITY`). All four labels are 1 word each, verbatim from the spoken line, and clearly symbolic rather than a quantitative CFD/force simulation or planetary disc. Bounds `[214, 241, 1387, 864]` inside 5% safe area; entry/exit clear.
   - **Sequencing requirement:** In R45, do not run `r45_gravity` and `r45_lift_mechanism` back to back; separate every pair of code graphics in R45/R46 with real moving imagery.

---

### FIX (do not render until corrected)

6. **`r39_fire_partners` — FIX** (`preview_sha256: 650af628a13e9a1984b6d0337e80d562980faae0fdceb6ac00084fcfe84abe04`)
   - **Row / Source:** R39, `SOURCES.md` v01 rows 9, 14 (`"Fire needs two partners: fuel and oxygen"`).
   - **Problems found on full-size still:**
     1. **Detached flame triangle:** The two blue arrows from `FUEL` (`(320, 380)`) and `OXYGEN` (`(1030, 380)`) converge at `(800, 650)` and `(870, 650)` directly above `FIRE` (`(840, 740)`), leaving the convergence zone above `FIRE` empty while a right-angled yellow triangle (`x = 1120, y = 650`, spanning `x = 1070..1170`) floats ~250 px off to the right, unattached to either the arrows or the `FIRE` label.
     2. **Misaligned `OXYGEN` header:** `OXYGEN` is drawn at `(760, 260)` (spanning `x ≈ 760..965`), whereas its arrow starts to the right of the word at `(1030, 380)` (a leftover coordinate from the wider `ALMOST NO OXYGEN` header in `r40_fire_missing`).
   - **Exact changes required:**
     - Center the gold flame/fire symbol at the convergence point directly above `FIRE` (around `x = 880, y = 655`, matching the `(880, 660)` position of the `X` in `r40_fire_missing`) and give it a recognisable symmetric flame silhouette (e.g., outer + inner or multi-tip flame polygon) rather than a detached right-angled triangle at `x = 1120`.
     - Shorten both converging arrows so their arrowheads terminate cleanly just above/outside the flame symbol (e.g., `y = 585`) with zero overlap.
     - Align `OXYGEN` over its arrow start (e.g., `text(d, (860, 260), lines[1], 52, BLUE)` with arrow starting at `(960, 380)`).
     - Ensure real moving imagery separates `r39_fire_partners` and `r39_oxygen` in R39 (never two code graphics back to back).

7. **`r40_fire_missing` — FIX** (`preview_sha256: fd825761a6169f8cde92d250e739a23c7962d90964fd524f9f5b7b07eb55b0c6`)
   - **Row / Source:** R40, `SOURCES.md` v01 rows 9, 14 (`"Titan has lakes of fuel, and methane in its sky, but almost no oxygen... the fuel around you would not catch fire"`).
   - **Problems found on full-size still:**
     1. **Arrowhead collision with the `X`:** The right arrow from `ALMOST NO OXYGEN` ends at `(870, 650)`, placing its arrowhead directly on top of the upper-left diagonal stroke of the `DIM` grey `X` (`(830, 620)–(930, 700)` and `(930, 620)–(830, 700)`, centered at `(880, 660)`).
     2. **Bright blue arrow on greyed-out oxygen side:** `ALMOST NO OXYGEN` and the `X` are drawn in `DIM` grey (`(192, 210, 232, 235)`), but the arrow from `ALMOST NO OXYGEN` is drawn in bright `BLUE`, contradicting `SHOT_LIST_v04.md` R40 (`"with oxygen side greyed out"`).
   - **Exact changes required:**
     - Shorten both converging arrows so their arrowheads stop cleanly clear of the `X` (e.g., arrow tips ending at `(820, 595)` and `(940, 595)` above the `X` at `y = 625..705`, with `NO FIRE` at `y = 740`).
     - Draw the right arrow from `ALMOST NO OXYGEN` in `DIM` grey (matching its `DIM` label and `X`) so the missing-oxygen side reads immediately as absent/greyed out.
     - Ensure real moving imagery separates `r39_fire_partners`, `r40_fire_missing`, and `r40_airmix`.

---

## Render permission and preserved holds

- **Approved to render now under `--review-ref J2192` (5 of 7):**
  ```bash
  python3 process_graphics.py --out /Users/benjaminoats/_desk/cache/J2089/process_previews_v01 --render \
    --approved r21_cycle_clouds r21_cycle_lakes r25_heated_suit r29_rain_comparison r45_lift_mechanism \
    --review-ref J2192
  ```
- **Withheld until fixed (2 of 7):** `r39_fire_partners`, `r40_fire_missing`. After applying the exact coordinate/colour fixes above in `process_graphics.py` and verifying their full-size PNGs and `PROCESS_CHECKS_v01.json`, render them only after their fixed stills are confirmed.
- **Preserved holds (not released by this review):**
  1. **Frame-0 native motion:** ESA's colourized `HUYGENS_MOVIE_HIRES_SILENT.WMV` reconstruction remains excluded per J2150; compliant frame-0 real moving imagery remains unresolved under J2177 / Chief.
  2. **R25 `PIA07232` three-row reuse conflict:** Using `PIA07232` at R18, R20, and R25 exceeds the `≤ 2` still appearances cap; remains under J2177 / Chief.
  3. **JHUAPL Dragonfly animation rights:** Express written permission hold documented in `J2089_CHECKPOINT_v05.md` remains in force until Chief supplies permission or scopes a compliant replacement.
  4. **J2177 (17 mechanism stills):** Remains a separate open review job.
  5. **Composite & gate requirements:** All rendered transparent MOVs require reviewed, colour-graded moving real plates, subject-safe placement, real moving imagery between every pair of code graphics (including inside R21, R25, R29, R39, R40, and R45), measured composite contrast `≥ 4.5:1`, and passing `picture_qa.py` / `polish_gate.py`. No film-stage PASS is granted here.
