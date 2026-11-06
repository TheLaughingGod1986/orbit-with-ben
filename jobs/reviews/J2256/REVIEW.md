# Review Packet — `J2256` (`033 Uranus: stills lock + OMNI R29/R55 price-pass brief from SHOT_LIST_v01`)

- **Job:** `J2256`
- **Film / Stage:** `033_Why-This-Planet-Has-21-Year-Winters` · `033 picture`
- **Worker:** `gemini` (`gemini-argon`)
- **Upstream Ref:** `J2238` / `h94` / `d67daf94` (`SHOT_LIST_v01.md` on `main`, OWB PR `#544`)
- **Spend:** **£0.00** (no Flow/Vertex/Omni/cash spend; no YouTube uploads or visibility changes; no plates marked KEEP from filenames alone)

---

## 1. Deliverables Produced in `J2256`

1. **`02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/07_Edit-Project/STILLS_LOCK_v01.md`**
   - **43-Asset Local & NAS Verification (§2A):**
     - **5 of 43** primary pool assets verified on local disk or NAS with exact paths, dimensions, byte sizes, and SHA-256 digests:
       1. `#10 weic2310a` / `STScI-01GWQDPJTF1MY8ZGN4WBMWMACJ`: Local unannotated PNG `/Users/benjaminoats/_desk/cache/J2089/jwst_v01/uranus_nircam_unannotated.png` (`2000×2000`, `2,449,044` B, SHA-256 `e5f7a1a0e10a6e6c769b40ecbb2f4dd78ea2ada65f2e96efd69c113ea29f52a7`) + NAS JPG `/Volumes/data/mac-mini-archive/scratch/J1199/plates/s4_uranus/webb_weic2310a.jpg` (`1268×1268`, `205,179` B, SHA-256 `cbe6b51ce9d813f74c0406575f1ed01633459d26aca6e42179ead05bb41c9d8a`).
       2. `#12 PIA18182`: Local `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan/03_Reference-Material/harvest_J2089_v01/PIA18182.jpg` & `/Users/benjaminoats/_desk/cache/J2089/harvest_v03/PIA18182.jpg` + NAS `/Volumes/data/mac-mini-archive/scratch/J1199/plates/s4_uranus/PIA18182.jpg` (`1720×1720`, `83,489` B, SHA-256 `3dcc83114f1a25caa1ae1a1436830fffaa15a3e429666dbf4c68bcf035e8932b`).
       3. `#13 PIA00346`: NAS `/Volumes/data/mac-mini-archive/scratch/J1199/plates/s4_uranus/PIA00346.jpg` (`540×800`, `22,673` B, SHA-256 `e01ab238b83014b428c01bfcf99179d6aee92c767275836a0e24602e1ccb664b`). Flagged native `540×800` resolution so the assembler composites it at `≤ 1.85×` over `#050814` starfield (preventing `> 2.0×` upscale WARN/FAIL).
       4. `#14 PIA00143`: NAS `/Volumes/data/mac-mini-archive/scratch/J1199/plates/s4_uranus/PIA00143.jpg` (`794×960`, `26,412` B, SHA-256 `f01898cf2636fb81db534edad198af4031c81274db9e5289f1207d8a982d6cbe`).
       5. `#15 PIA01391`: NAS `/Volumes/data/mac-mini-archive/scratch/J1199/plates/s4_uranus/PIA01391.jpg` (`1000×1000`, `29,274` B, SHA-256 `9f97cd7b6b272186c75b389112bbfcee555988c5c0720b1138bc072583533b95`).
     - **2 Auxiliary Assets Verified:** `PIA00405` (`/Users/benjaminoats/_desk/cache/J2089/size_sources_v01/PIA00405.jpg`, `1350×1359`, SHA-256 `fc93286c2d73a64f2b095c2e1f1df867b0e96ad0b9515987f9b38fd2ed91a641` for `R59` Moon-vs-Miranda scale graphic) and canonical `01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png` (`761,432` B, SHA-256 `922298a14991f128482122ffd91ff48775f96d81ed838d69dc3009b3914f9472`).
     - **Missing IDs Only (§2B):** Clean 38-item list (`PIA01283`, `PIA01280`, `File:Herschel_40_foot_telescope.jpg`, `File:William_Herschel01_hires.jpg`, `File:Caroline_Herschel-1829.jpg`, `File:Herschel_Account_of_a_Comet_1781_Phil_Trans.jpg`, `File:Herschel_1783_Georgium_Sidus_letter_Phil_Trans.jpg`, `File:Portret_van_Johann_Elert_Bode,_RP-P-1913-254.jpg`, `File:Martin_Heinrich_Klaproth_portrait.jpg`, `weic2332a`, `PIA17306`, `KAO_airborne_915_in_flight`, `ARC-1973-AC73-4189-89`, `PIA01534`, `PIA01364`, `PIA01356`, `PIA01978`, `PIA01361`, `PIA01278`, `PIA01279`, `PIA18033`, `PIA02875`, `PIA01492`, `PIA00369`, `PIA01975`, `PIA02963`, `PIA19857`, `PIA01354`, `PIA00141`, `PIA00037`, `PIA01486`, `PIA01490`, `PIA01488`, `PIA01389`, `PIA01390`, `PIA01485`, `PIA00032`, `PIA19952`) + auxiliary `PIA00271`.
   - **Stills-Lock & `≤ 2` Appearance Cap (§1, §3, §4):**
     - Frame 0 (`0.00–2.00 s` / `R01` `0.00–6.22 s`) is locked to native moving Hubble time-lapse `PIA01283` + `PIA01280`, and `svs20390_shot9_beauty_rings.mp4` (`ZpEA8stoSPA` open, SHA-256 `f964c7f1dd92c5626135f9915ba5d532a3114284cf24115fd393a9756249fb3e`) is strictly excluded.
     - Reconciles `SHOT_LIST_v01.md` §3 vs §4 so every single still has `≤ 2` appearances in `cuts.json`: `weic2310a` → `R06, R21` (2); `weic2332a` → `R15, R50` (2); `PIA01490` → `R60, R67 Cut 3` (2); `PIA01280` standalone still → `R16, R34` (2); `R55` £0 fallback → `PIA00141` (Cut 1) + `PIA01361` (Cut 2–3 contiguous into `R56` Cut 1).

2. **`02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/07_Edit-Project/STILLS_POOL_STATUS_v01.json`**
   - Machine-readable JSON manifest of the 5 verified pool assets, 2 verified auxiliary assets, excluded Short asset, and 38 missing IDs for the downstream £0 harvest job.

3. **`02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters/07_Edit-Project/OMNI_PRICE_PASS_BRIEF_v01.md`**
   - Extracts `R29` (`239.86–252.30 s`, `12.44 s`, 3 cuts, `omni_033_r29_orbit_21yr_night.mp4`) and `R55` (`493.01–505.35 s`, `12.34 s`, 3 cuts, `omni_033_r55_orbit_ice_skates.mp4`) with their canonical start frame (`orbit-seedance-reference-16x9-v01.png`, no planet disc), Vertex `global` routing, and their complete £0 fallbacks (`code_graphic_033_r29_seasonal_dial.mp4` and graded Voyager `PIA00141` + `PIA01361` with pressure/heat gauge overlay).

---

## 2. Decision Parked for Chief (`gpt-6-astra`)

1. **PASS `J2256`** (`STILLS_LOCK_v01.md`, `STILLS_POOL_STATUS_v01.json`, `OMNI_PRICE_PASS_BRIEF_v01.md`).
2. **Dispatch £0 Harvest + Code Graphics** for the 38 missing pool IDs (+ `PIA00271`) and 10 (+1 fallback) bespoke `CODE` graphics.
3. **Price-Pass Call on `R29` & `R55`:** Confirm whether to run the full build on the **£0 fallbacks** (`£0.00`) or authorise a Vertex `global` Omni mint job for `R29` (`12.44 s`) and `R55` (`12.34 s`).


---

## 3. Chief ruling (h175 · Grok Bot · 2026-11-06T17:08Z Europe/London)

**PASS** on J2256 deliverables. Spot-checked `PIA18182` NAS SHA-256 `3dcc8311…e8932b` and canonical Orbit start-frame `orbit-seedance-reference-16x9-v01.png` SHA-256 `922298a1…4f9472` — both match the packet. Stills lock, pool status JSON, and the OMNI price-pass brief are accepted as the picture-plan lock for film 033.

**Price-pass on R29 & R55: Option B (£0 fallbacks).**

- Live Vertex console read timed out this sweep; ledger still shows Developer Program **£69.48** (2026-11-06T08:30Z) above the £5 floor, but Omni `gemini-omni-flash-preview` remains **unpriced** in the ledger (prior Orbit Omni takes logged `amount: 0.0`, billed late). Authorising mint without a bounded GBP estimate would break the Paid-account £5-floor rule.
- Therefore R29 and R55 lock to their designed £0 fallbacks in `SHOT_LIST_v01.md` / `STILLS_LOCK_v01.md`:
  - **R29** → `code_graphic_033_r29_seasonal_dial.mp4` (no Orbit character via non-Omni tools).
  - **R55** → graded Voyager `PIA00141` + `PIA01361` with pressure/heat gauge overlay (or the listed CODE pressure-gauge fallback).
- No Vertex/Flow/Omni/cash spend authorised by this PASS. A later Omni upgrade needs a fresh live credit read **and** a priced GBP bound that leaves ≥ £5, then a new mint job.

**Next (queued separately):** £0 harvest of the 38 missing pool IDs (+ aux `PIA00271`) and the bespoke CODE graphics named in the stills lock, then assembly may use the locked plan.

£0 this ruling. No Ben.
