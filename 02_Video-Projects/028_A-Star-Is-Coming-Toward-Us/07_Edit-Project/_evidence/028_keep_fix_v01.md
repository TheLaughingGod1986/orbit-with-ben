# 028 Gliese 710 — Minted Plates KEEP/FIX Review Sheet (`J0850`, 22 Oct 2026)

Prepared by Gemini (`gemini`) after Chief's `J0850` price PASS (`3aa96ea53`, 22 Oct 2026). **Parked for Chief (`parked for Chief: 028 picture KEEP/FIX pass`).**

- **Combined contact sheet:** `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/_evidence/028_keep_fix_v01_contact.jpg`
- **Omni report:** `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/omni_gen_report_8_23_v01.json`
- **Flow report:** `02_Video-Projects/028_A-Star-Is-Coming-Toward-Us/07_Edit-Project/flow_gen_report_11_17_v01.json`

---

## 1. Existing Orbit Omni Reuse Check (before minting)

Audited all 17 existing Orbit Omni clips across `023`–`027` (`orbit_venus_omni`, `orbit_probe_heat_omni`, `orbit_photon_race_omni`, `orbit_time_dilation_omni`, `orbit_curiosity_ridge_omni`, `orbit_dust_panel_omni`, `orbit_mars_sunset_omni`, `orbit_alpha_pair_omni`, `orbit_bessel_split_omni`, `orbit_laser_moon_omni`, `orbit_voyager_lookback_omni`, `orbit_northpole_omni`, `orbit_sunset_omni`, etc.). None shows Orbit sweeping a night sky with binoculars on a dark hill (`r08_orbit_binoculars`) or Orbit floating among dark Oort ice lumps (`r23_orbit_ice`). Per Chief's ruling, composited canonical `ORBIT_REF` start frames (`_composite_028_orbit_starts_v01.py`, with `.orbit_source.json` sidecars and no planet in frame) and minted 1 take each on Vertex `global` (`gemini-omni-flash-preview`).

---

## 2. Minted Plates Summary & Self-Audit (4 / 4 rows minted on Take 1)

| Row | Plate ID | Chapter & Span (`use_s`) | Engine / Model | Spend (Take 1) | Duration | Freezes (`>=0.8s`) | SHA-256 (first 16) | Self-Score & Notes for Chief |
|---:|---|---|---|---|---:|---:|---|---|
| **8** | `r08_orbit_binoculars` | Ch 1 (`58.64–66.52 s`, `7.88 s`) | Vertex `global` · `gemini-omni-flash-preview` | **£0.65** est. (promo) | `8.0 s` | `0` | `a7793cfce266c192` | **CANDIDATE KEEP** — Canonical matte-orange Orbit (1 body, curved black visor, 2 cream eyes, stubby arms, 3-finger hands, glowing antenna bulb, underside glow, NO LEGS) hovers over dark hill under starfield (no planet), lifts binoculars to visor, sweeps sky toward faint orange star, lowers them, tilts visor thoughtfully. Silent stripped. |
| **11** | `r11_night_road` | Ch 1 (`95.08–109.20 s`, `14.12 s`) | Flow CDP `:9222` · `Veo 3.1 - Quality` | **100 cr** (`20,950 -> 20,850`) | `8.0 s` | `0` | `6dfb64f683998705` | **CANDIDATE KEEP** — Straight empty country road at night under stars; one car's warm headlights approach straight down the lane and grow brighter. No number plate, no brand logo, no road signs, no text, no people. Covers `"like a car on a long, straight road at night. Its headlights do not move left or right. They just grow."` (`101.00–109.20 s`), with `95.08–101.00 s` covered by the planned star cutaway per Chief's ruling. Silent stripped. |
| **17** | `r17_pitch` | Ch 2 (`191.00–194.82 s`, `3.82 s`) | Flow CDP `:9222` · `Veo 3.1 - Fast` | **10 cr** (`20,850 -> 20,840`) | `8.0 s` | `0` | `d224e0445967665e` | **CANDIDATE KEEP w/ CROP (or FIX 10 cr)** — Empty green grass pitch at dusk, no players, no text/logos. Note: in the middle (`1.5–6.2 s`) the camera pulls back behind and then passes through the goal net, and empty stadium stands/floodlights sit on the left/right edges. Row `r17_pitch` only needs `3.82 s` (`191.00–194.82 s`): we can either (a) use a clean turf crop (`6.0–8.0 s` + `0.0–1.5 s` or centre turf crop) for £0/0 cr, or (b) mint 1 Fast retake (`10 cr`) if Chief marks FIX. |
| **23** | `r23_orbit_ice` | Ch 3 (`241.88–249.84 s`, `7.96 s`) | Vertex `global` · `gemini-omni-flash-preview` | **£0.65** est. (promo) | `8.0 s` | `0` | `8c509d86cc18dbed` | **CANDIDATE KEEP** — Canonical matte-orange Orbit (1 body, black visor, cream eyes, 3-finger hands, antenna bulb, underside glow, NO LEGS) floats in deep space beside dark grey craggy Oort ice lumps on a starfield (no planet, no ground), reaches out and gently taps the ice lump, watches it turn slowly. Silent stripped. |

---

## 3. Pool Balances After Mint

- **Flow (`benoats@googlemail.com`, CDP `:9222`):**
  - Before `J0850` mint: **20,950** credits
  - Spent in `J0850`: **110** credits (`100` cr Quality `r11_night_road` + `10` cr Fast `r17_pitch` — **169 cr under** the `279` cr expected reserve)
  - Live Flow balance after `J0850`: **20,840** credits
  - Remaining HOS (`008` `5,605` exp + `009` tranche 1 `7,354` exp = `12,959` exp): leaves **7,881** expected credits after HOS `008` + `009 T1` (**+4,881 cr above** the `3,000` floor).
- **Vertex (`Google Developer Program premium benefit - CREDIT_TYPE_MONTHLY`):**
  - Available before `J0850`: **£71.02** (`£70.02` usable after £1.00 margin; Free Trial `£0.00 Used`)
  - Estimated `J0850` Omni spend: **£1.30** (`2 × £0.65`, 0 retries used, well within the `£2.60` cap)
  - Usable remaining after `028` Omni: **~£68.72**
