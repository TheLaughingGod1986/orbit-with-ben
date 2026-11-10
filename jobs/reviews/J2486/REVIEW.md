# J2486 — Design review: 023 Venus thumbnail B "465°C" (`VBaYRPp85Sw`)

**Verdict: FIX.** Do not arm the test with this file. Fix job **`J2487`** has been queued, and **`J1198` stays waiting** until the fixed thumbnail passes a fresh design review.

- **Reviewed files:**
  - Full-size thumbnail (`1280×720`, `291,606` bytes): `02_Video-Projects/023_What-Happened-To-Venus/08_Thumbnail/tc_B_465c/venus_tc_B_465c_VBaYRPp85Sw.jpg` (`SHA256: b580d47539dee75bcb19867377ddfd3384453bbf880ddf42c5675a8eabc31568`, verified against `SHA256.txt` and present on both NAS mirrors `/Volumes/data/studio-live/...` and `/Volumes/data/mac-mini-archive/...`)
  - Phone-size preview sheets (`168×94` and `426×240`): `venus_tc_B_465c_preview_sheet.jpg` and `venus_tc_A_vs_B_465c_sheet.jpg` (side-by-side with live `A: MELTS LEAD` and ended `B: EARTH'S TWIN`)
  - Base plate (`1376×768`, `911,250` bytes): `venus_surface_glowing_lander_plate.jpg` (`SHA256: 8f5f2b84fcbf27e7ec891343b64e23c1effc18542b5474d1be5ffb5e30de2aac`)
- **Reviewers:** `macbook-2` (initial visual pass by Claude on `macbook/J2486` commit `4fe4d8483`; completed with competitor comparisons, transcript provenance verification, SHA256/NAS checks, and queue updates by Gemini 4 Argon on `macbook-2`, 10 Nov 2026).
- **Studio / Spend:** Nothing changed in YouTube Studio. **£0.**

---

## 1. Rubric (`THUMBNAIL_AND_TITLE_RULES.md` §2.B), judged by eye

| Check | Result | Visual findings |
|---|---|---|
| **HOOK** | **PASS** | `"465°C"` (one token, 1 word) adds concrete physical furnace stakes to the title *What Happened to Venus?* without repeating any word of the title, and is the exact hook specified for the `J1198` draw branch. |
| **BAND** | **PASS** | Sits cleanly in the top-left sky band (`bbox = [68, 34, 462, 138]`, cap height `86 px` = `11.94%` of `720p`) over hazy cloud only. No letter touches the lander on the right (`x >= 605`) or the mountain peak (`y >= 165`). House `Arial Black`, yellow `(255, 230, 0)`, heavy `9 px` black stroke + drop shadow, clear of the bottom-right duration corner. |
| **GRADE** | **FAIL (visual) / PASS (numeric)** | Numerically `thumb_preview.py long --score` prints `PASS` (`saturation=245.5 >= 120`, `near_black=15% <= 30%`), but visually the colour grade is blown out and neon-red on the lower lander and ground (see Items 2 & 3). |
| **PHONE** | **PASS with caveat** | At `168×94` on `venus_tc_A_vs_B_465c_sheet.jpg`, `"465°C"` is crisp and readable, and the Venera-style lander silhouette reads clearly against the volcanic landscape. However, the lower hull collapses into a clipped neon red-orange fireball at `168×94`. |

---

## 2. Saturation (`245.5 / 255`): rich or blown out and garish?

**Verdict: Blown out and garish — FIX.**

`59.4%` of all pixels in `venus_tc_B_465c_VBaYRPp85Sw.jpg` are pinned at `HSV saturation >= 250/255`. Measured side-by-side against the channel's other long thumbnails and top search competitors for *"What Happened to Venus?"*:

| Thumbnail | Source | Mean HSV Saturation (`0–255`) | Pixels pinned at `S >= 250` | Near-black (`luma < 16`) | Visual read |
|---|---|---:|---:|---:|---|
| **`venus_tc_B_465c_VBaYRPp85Sw.jpg` (`465°C`)** | **023 Test B (under review)** | **245.5** | **59.4%** | **2.1% (RGB) / 15% (sheet)** | **Blown out / neon-red clipping on lower lander & basalt shadows** |
| `venus_surface_glowing_lander_plate.jpg` | 023 ungraded base plate | 203.8 | 10.8% | 12.0% | Warm amber sky, but lower lander already self-luminous |
| `venus_thumb_A_melts-lead.png` (`MELTS LEAD`) | 023 Live A | 161.8 | 2.6% | 11.7% | Rich orange-gold globe on dark starfield |
| `venus_tc_B_earths-twin_VBaYRPp85Sw.jpg` (`EARTH'S TWIN`) | 023 Ended Test B | 154.1 | 8.6% | 15.0% | Balanced blue Earth vs warm orange Venus |
| `sun_tc_B_10pct-hotter_h8HGfyShEHI.jpg` (`10% HOTTER`) | 022 Sun Test B | 186.5 | — | 17.9% | Strong solar orange without full-frame clipping |
| `light_speed_thumb_A_7-years-gone.jpg` (`7 YEARS GONE?`) | 024 Light Speed A | 169.6 | 7.8% | 8.5% | Clean deep-blue contrast |
| `blackhole_B_no_way_out.jpg` (`NO WAY OUT?`) | 006 Black Hole B | 164.0 | 16.0% | 19.3% | Rich accretion-disk orange against dark space |
| `saturn_B_rings_vanishing.jpg` (`RINGS VANISHING`) | 021 Saturn B | 148.0 | 12.4% | 23.4% | Rich warm gold |
| `jupiter_B_no_solid_ground.jpg` (`NO SOLID GROUND?`) | 020 Jupiter B | 139.0 | 17.1% | 15.3% | Natural warm bands |
| *What the Hell Happened to Venus?* (`bfVJBZJjcYg`, 1.26M views) | Competitor: **Cool Worlds** | 119.2 | — | 0.9% | Real Venera 13 surface panorama; pale sulfur-yellow sky, dark grey-brown basalt slabs |
| *Why NASA won't send humans to Venus* (`tsBAozoyYZw`, 8.03M views) | Competitor: **Insider Tech** | 125.7 | — | 23.1% | Warm amber-orange Venus globe behind astronaut |
| *What They Found on Venus Is Terrifying* (`XZJfHBc4-0w`, 1.44M views) | Competitor: **Astrum** | 208.0 | — | 0.3% | High-saturation sulfuric yellow-green haze + lightning, no clipped red metal |

Because `_grade_venus_lander_plate()` in `build_venus_tc_b_465c_j2484.py` applies `ImageEnhance.Color(1.42)` plus additive red boosts (`thermal_boost * 48`, `sphere_glow * 34`, `dark_lift * 36` on R) on top of a plate whose mean saturation is already `203.8`, almost 60% of the frame hits the saturation ceiling (`250–255`), crushing shadow colour separation and making the foreground look radioactive red.

---

## 3. Accuracy (`465°C` vs glowing/molten metal): **FIX**

At `465°C`, metal does not glow visibly (the Draper point where solids begin to emit a dull red incandescence is `~525°C`, and bright orange-yellow incandescence requires `~850–1000°C`), nor do Venus's solid basalt plains have glowing molten lava cracks.

In `venus_tc_B_465c_VBaYRPp85Sw.jpg` (and already in `venus_surface_glowing_lander_plate.jpg`):
- The entire lower section of the lander beneath the scalloped aerodynamic brake collar (the lower hull, landing ring, and struts) glows bright incandescent red-orange with yellow-white hot spots (`max RGB = [255, 238, 157]` in the graded thumb and `[255, 217, 167]` in the base plate; `31.4%` of the lower hull region `x=700..960, y=420..560` has `R >= 250` and `10.5%` has `R >= 245, G >= 120`), casting a bright red pool of light onto the rocks underneath it.
- The fractured basalt rocks around the landing ring show glowing red lava/ember seams.
- The upper spherical pressure vessel also has an artificial red-hot patch (`sphere_glow` in `build_venus_tc_b_465c_j2484.py`).

This reads as **melting / self-luminous internal combustion**, not `465°C` atmospheric heat.

**Required fix (`J2487`):**
- Remove the lander's self-glow, the red-lit ground pool underneath it, and the glowing lava cracks in the basalt rocks.
- Keep the dense, oppressive warm orange-amber cast from Venus's sky lighting the metallic lander from above/around so it reads as solid metal baking in a `465°C` oven rather than glowing white-hot or melting.

---

## 4. Provenance of `venus_surface_glowing_lander_plate.jpg`: **ESTABLISHED & RECORDED IN `META.json`**

We traced the exact provenance of `venus_surface_glowing_lander_plate.jpg` (`SHA256: 8f5f2b84fcbf27e7ec891343b64e23c1effc18542b5474d1be5ffb5e30de2aac`, `1376×768`, `911,250` bytes):
- **Tool:** Antigravity CLI built-in `image-generator` subagent (`generate_image` tool), invoked by `macbook-2` during `J2484` in parent session `a6954191-23b5-4450-888f-0153442d6226` (step 179, `2026-11-10T04:43:38Z`) -> subagent session `be87b190-eca3-4a5f-8f61-640c279f65d9` (step 1, completed `2026-11-10T04:43:59Z`).
- **Output path:** `/Users/ben/.gemini/antigravity-cli/brain/a6954191-23b5-4450-888f-0153442d6226/venus_surface_glowing_lander_plate_1794285839136.jpg` (embedded C2PA manifest: *"Created by Google Generative AI"*, `trainedAlgorithmicMedia`, SynthID watermark, signed by Google C2PA Media Services at `2026-11-10T04:43:59Z`).
- **Cost:** **£0** marginal spend (included in the Antigravity / Google AI Ultra subscription; no Vertex, OpenAI API, or paid overage billed).
- **Recorded:** Full provenance (`tool`, `model_provider`, `parent_conversation_id`, `subagent_conversation_id`, `generated_at_utc`, `source_path`, `cost_gbp: 0`, `cost_basis`, and exact `prompt`) is now written into `02_Video-Projects/023_What-Happened-To-Venus/08_Thumbnail/tc_B_465c/META.json` under `plate_provenance`.
- Note: The prompt used in `J2484` explicitly asked for *"intensely incandescent, glowing bright cherry red-orange ... and faint glowing molten red-orange thermal fractures in the rock"*, which caused the accuracy issue in Item 3.

---

## 5. Orbit character, extra words, bottom-right corner: **PASS**

- **No Orbit character:** Confirmed (no robot anywhere in frame, §2.8).
- **No extra words:** Only `"465°C"` appears in the frame.
- **Clear of bottom-right corner:** Text sits in the top-left sky band (`[68, 34, 462, 138]`); the bottom-right duration badge region is dark basalt rock with no text or critical detail.

---

## FIX List (queued as **`J2487`**)

1. **Accuracy (`465°C` heat, not melting):** Remove the self-luminous red-orange/white-hot glow on the lander's lower hull, landing ring, and struts, the red-lit ground pool underneath it, and the glowing red lava cracks in the basalt rocks (either by generating a new £0 text-free plate without incandescent metal/lava cracks or by re-grading/attenuating the hot spots so the underside is in natural shadow). Keep the warm amber-orange atmospheric sky cast.
2. **Saturation (`~165–195` target):** Bring mean HSV saturation down from `245.5` into the `165–195` range (in line with the channel's `139–186.5` range and Venus search competitors), eliminating the `59.4%` saturation clipping while keeping `near_black <= 30%`.
3. **Provenance (`META.json`):** Preserve or update the `plate_provenance` block in `META.json` with the exact tool, model, prompt, timestamp, and `£0` cost basis for the plate used.
4. **Gate, sheets, SHA256, and NAS mirror:** Re-run `thumb_preview.py long --score`, rebuild `venus_tc_B_465c_preview_sheet.jpg` and `venus_tc_A_vs_B_465c_sheet.jpg`, update `SHA256.txt`, and copy all updated files to the NAS mirror (`/Volumes/data/studio-live/...` and `/Volumes/data/mac-mini-archive/...`).
5. **Fresh design review:** Queue a fresh independent design review before reopening `J1198`. Leave `J1198` waiting until that review returns `KEEP`.
