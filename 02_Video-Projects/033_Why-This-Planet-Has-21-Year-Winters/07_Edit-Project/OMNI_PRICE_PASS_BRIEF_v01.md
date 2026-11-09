# 033 — Chief Price-Pass Brief: `OMNI (flag)` Rows `R29` & `R55` (`OMNI_PRICE_PASS_BRIEF_v01.md`)

- **Film:** `033_Why-This-Planet-Has-21-Year-Winters` (*Why This Planet Has 21-Year Winters*)
- **Job:** `J2256` (`033 Uranus: stills lock + OMNI R29/R55 price-pass brief from SHOT_LIST_v01 (no mint, £0)`)
- **Upstream Ref:** `SHOT_LIST_v01.md` (`d67daf94` / Chief `h94` planning PASS in `J2238`)
- **Spend in J2256:** **£0.00** (no Create, no Vertex/Flow/Omni calls, no plate marked KEEP)
- **Status:** **Parked for Chief (`gpt-6-astra`) price-pass / routing decision.**

---

## 1. Executive Summary for Chief

`SHOT_LIST_v01.md` contains exactly **two** `[ORBIT ACTS]` beats (`R29` and `R55`), well after minute 1 (`3:59.86` and `8:13.01`), meeting the `1–3` Orbit beats rule (`AGENTS.md` / `STUDIO_PLAYBOOK.md` §5):
- **Option A (Vertex `global` Omni Mint — 2 clips, `24.78 s` total):** Mint `omni_033_r29_orbit_21yr_night.mp4` (`12.44 s`, 3 sub-cuts) and `omni_033_r55_orbit_ice_skates.mp4` (`12.34 s`, 3 sub-cuts) via Vertex `global` using the canonical start frame `01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png` (SHA-256 `922298a14991f128482122ffd91ff48775f96d81ed838d69dc3009b3914f9472`), subject to the `£0.10` Vertex trial floor (`AGENTS.md`).
- **Option B (£0 Zero-Spend Fallback — 0 clips minted, £0.00):** Both `R29` and `R55` have complete, rule-compliant **£0 fallbacks** designed into `SHOT_LIST_v01.md` and `STILLS_LOCK_v01.md` that preserve:
  - No two `CODE` graphics back-to-back (`R28` and `R30` are both `NASA` rows, so `R29` can safely run as a bespoke `CODE` dial if £0; `R54` and `R56` are both `NASA` rows, so `R55` can safely run either as graded Voyager plates + gauge overlay or a bespoke `CODE` pressure gauge).
  - Every still `≤ 2` appearances across all 67 rows (`STILLS_LOCK_v01.md` §3A.5).
  - No non-Omni generator ever renders Orbit (`AGENTS.md` Standing Lesson 3: *"Orbit = Omni only"* — the £0 fallbacks depict the instrument dial / pressure gauge without rendering the robot character via non-Omni tools).

---

## 2. Extracted `OMNI (flag)` Rows (`R29` & `R55`)

### Row `R29` — `[ORBIT ACTS]` Beat 1: 21-Year Polar Night (`239.86–252.30 s`, `12.44 s`, 3 cuts)

| Field | Specification from `SHOT_LIST_v01.md` |
|---|---|
| **Row / Window** | `R29` · `239.86–252.30 s` (`3:59.86–4:12.30`) · Duration: `12.44 s` · Cuts: `3` (`4.15 s` / `4.15 s` / `4.14 s`) |
| **Spoken VO** | *"If Orbit were floating on the night side, the little orange robot would have to switch on his headlamp, wrap himself in a heated blanket, and wait twenty-one Earth years just to see the next sunrise."* |
| **Adjacent Rows** | Preceded by `R28` (`233.67–239.86 s`, `NASA` `PIA01391`) and followed by `R30` (`252.30–262.14 s`, `NASA` `PIA18182`). Neither neighbour is `CODE`. |
| **Target Filename (if Omni approved)** | `omni_033_r29_orbit_21yr_night.mp4` |
| **Canonical Start Frame** | `01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png` (`761,432` B, SHA-256 `922298a14991f128482122ffd91ff48775f96d81ed838d69dc3009b3914f9472`). **Start-frame rule:** Contains **no whole planet disc** (prevents planet drift per Standing Lesson 3). |
| **Routing / Prompt Spec** | Vertex `global` Omni only: Small orange robot Orbit floating in dark cyan starlight on Uranus's night side (`#050814` deep space, faint cyan limb horizon glow only, no whole planet disc in start frame):<br>• **Cut 1 (`239.86–244.01 s`):** Orbit clicks on his warm amber chest/forehead headlamp beam cutting through dark methane-blue mist.<br>• **Cut 2 (`244.01–248.16 s`):** Orbit pulls a silver-gold thermal foil blanket snugly around his shoulders.<br>• **Cut 3 (`248.16–252.30 s`):** Orbit glances wistfully at a holographic wrist timer counting `21 EARTH YEARS TO SUNRISE`. |
| **Edit Overlay & SFX** | Lower-third card (`0.4 s` fade-in at `248.0 s`, `3.5 s` hold): **`21 YEARS TO SUNRISE`** · SFX: `tick_ink.wav` at `248.00 s` (`-16 LU` rel VO). |
| **£0 Fallback (Zero Spend)** | **`code_graphic_033_r29_seasonal_dial.mp4`** (`12.44 s`, 3 internal camera stages `4.15 s` each): Bespoke animated 84-year Uranian seasonal clock dial over a graded Hubble `PIA01280` / `PIA01391` night-side limb composite showing the 21-year night quadrant ticking toward dawn (`21 YEARS TO SUNRISE`), with no non-Omni character generation. Sits cleanly between `R28` (`NASA`) and `R30` (`NASA`) with **0 back-to-back `CODE` graphics**. |

---

### Row `R55` — `[ORBIT ACTS]` Beat 2: No Solid Surface / Ice Skates (`493.01–505.35 s`, `12.34 s`, 3 cuts)

| Field | Specification from `SHOT_LIST_v01.md` & `STILLS_LOCK_v01.md` |
|---|---|
| **Row / Window** | `R55` · `493.01–505.35 s` (`8:13.01–8:25.35`) · Duration: `12.34 s` · Cuts: `3` (`4.11 s` / `4.11 s` / `4.12 s`) |
| **Spoken VO** | *"If Orbit packed a pair of ice skates and descended through those pale blue clouds looking for a frozen lake, he would sink straight through the mist into crushing dark heat before he ever found a floor."* |
| **Adjacent Rows** | Preceded by `R54` (`484.33–493.01 s`, `NASA` `PIA18182` + `weic2332a` subscribe beat) and followed by `R56` (`505.35–514.11 s`, `NASA` `PIA01361` + `PIA01354`). Neither neighbour is `CODE`. |
| **Target Filename (if Omni approved)** | `omni_033_r55_orbit_ice_skates.mp4` |
| **Canonical Start Frame** | `01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png` (`761,432` B, SHA-256 `922298a14991f128482122ffd91ff48775f96d81ed838d69dc3009b3914f9472`). **Start-frame rule:** Contains **no whole planet disc**. |
| **Routing / Prompt Spec** | Vertex `global` Omni only: Small orange robot Orbit holding a pair of silver ice skates tied by their laces over his shoulder as he descends into pale cyan-blue Uranian cloud decks:<br>• **Cut 1 (`493.01–497.12 s`):** Orbit looks down expectantly for a skating rink.<br>• **Cut 2 (`497.12–501.23 s`):** His feet sink straight through wispy cyan cloud layers with no solid ground.<br>• **Cut 3 (`501.23–505.35 s`):** His thruster boots flare warm orange to arrest his descent above deep amber-red high-pressure glow below. |
| **Edit Overlay & SFX** | Lower-third card (`0.4 s` fade-in at `498.5 s`, `3.5 s` hold): **`NO SOLID SURFACE`** · SFX: `whoosh_soft.wav` at `495.50 s` (`-15 LU` rel VO) + `tick_ink.wav` at `498.50 s` (`-16 LU` rel VO). |
| **£0 Fallback (Zero Spend)** | **Graded Voyager 2 Cloud-Deck Descent + Animated Pressure/Heat Crush Gauge Overlay (`12.34 s`, 3 sub-cuts):**<br>• **Cut 1 (`493.01–497.10 s`):** Graded Voyager 2 `PIA00141` (*Uranus Upper Atmosphere & High-Altitude Methane Haze Limb*, 1st of 2 appearances alongside `R62`).<br>• **Cut 2–3 (`497.10–505.35 s`):** Graded Voyager 2 `PIA01361` (*False-Colour Polar Haze Over Uranus South Pole*, flowing **contiguously** into `R56` Cut 1 `505.35–509.60 s` so `PIA01361` stays at 2 total appearances across the film) with an animated vertical pressure/temperature depth gauge (`NO SOLID SURFACE`) drawing in time with the VO. |

---

## 3. Note on the Three Optional `VEO (flag)` Rows (`R02`, `R51`, `R62`)

Per `SHOT_LIST_v01.md` §1, the three `VEO (flag)` rows (`R02` `6.22–13.09 s`, `R51` `453.80–465.28 s`, `R62` `570.42–582.89 s`) are already designed with **£0 NASA/archival plates as their primary zero-spend default** (`STILLS_LOCK_v01.md` §4A):
- **`R02` (`6.22–13.09 s`):** Uses `PIA18182` (`1720×1720` verified local/NAS) with `97.77° AXIAL TILT` overlay (`R08` uses `PIA00141`, keeping every still `≤ 2` appearances).
- **`R51` (`453.80–465.28 s`):** Uses `PIA17306` (Cut 1–2) + `PIA01356` (Cut 3) as real/archival plates with `4× STRONGER AT ONE POLE` lower-third (stays `source_type: "nasa_still"` so it never collides with `R52` `CODE`).
- **`R62` (`570.42–582.89 s`):** Uses `PIA01485` (Cut 1) + `PIA00032` (Cut 2–3) Voyager 2 Verona Rupes plates with the edit-level `12 MINUTES OF FREE FALL` counter overlay.

---

## 4. Requested Chief Decision (`J2256`)

1. **Approve Stills Lock (`STILLS_LOCK_v01.md` + `STILLS_POOL_STATUS_v01.json`)** and queue the £0 harvest job for the **38 missing pool IDs** (+ `PIA00271`).
2. **Choose `R29` / `R55` Routing:**
   - **Route 1 (£0 full build):** Proceed directly to £0 harvest + 10 bespoke `CODE` renders + £0 fallbacks on `R29` and `R55` (`£0.00` spend), OR
   - **Route 2 (Vertex `global` Omni mint for `R29` & `R55`):** Authorise a dedicated Omni generation job for `omni_033_r29_orbit_21yr_night.mp4` (`12.44 s`) and `omni_033_r55_orbit_ice_skates.mp4` (`12.34 s`) from `orbit-seedance-reference-16x9-v01.png` under the Vertex trial floor.
