# 028 price review v02 (updated for J0850 live Flow read, 22 Oct 2026)

Gemini (`gemini`), 22 Oct 2026, J0850 (updating Cursor's 15 Oct J0321 / J0337 `PRICE_REVIEW_v02.md` with today's live Flow reading after HOS 007's J0352 mint). **No mint. No spend.** Parked for Chief (`parked for Chief: 028 Flow price pass`).

v01 files are unchanged. Rebuild with `python3 _build_plate_boards_v02.py`. Also written: `FLOW_PRICE_TABLE_J0850.md`.

## Readings this run (22 Oct 2026)

- Flow: **20950** credits at `2026-10-22T16:56:01Z` (`ai_spend_daily.py --dry-run --pools flow,vertex`, account picker, `benoats@googlemail.com`, CDP `:9222`). Down `2,790` net from the 15 Oct reading (`23,740`) after HOS 007 minted all `73/73` Flow rows in `J0352` (`46d59506`) for `2,890` credits (`24 Quality × 100 + 49 Fast × 10 = 2,890 cr`, 100% try-1 KEEP, plus two `+50` Flow allotment adjustments).
- Vertex promo: **£71.02** Available at `2026-10-22T16:56:01Z` (`Google Developer Program premium benefit - CREDIT_TYPE_MONTHLY`). Free Trial **£0.00 Used**. Usable **£70.02** after the £1.00 margin. No spend logged in this run.

## Remaining 028 picture rows to mint (`boards v02`)

All £0 rows are already built and PASS on `main`:
- **33 harvest rows** (21 NASA/ESA/ESO files): `J0350` PASS (`14566db2`), **0 Flow credits / £0.00**.
- **20 code graphics + subscribe card** (`19` code beats + `1` card in `code_graphics_v02`, plus `teaching_overlays_v01_pack`): `J0338` + `J0382` `20/20` PASS, **0 Flow credits / £0.00**.

Only **4 plates** remain on `PLATE_BOARDS_v02.json` (**2 Flow Veo** + **2 Vertex Omni**):

| Plate ID | Row | Ch | Span (`t_in–t_out`) | `use_s` | Route / Model | Clip s | Flow Try-1 | Flow Expected | Vertex Try-1 | Vertex Expected / Hold | Status |
|---|---:|---:|---|---:|---|---:|---:|---:|---:|---:|---|
| `r11_night_road` | 11 | 1 | `95.08–109.20 s` | `14.12 s` | **Flow · Veo 3.1 Quality** (`night_road_veo_v01`) | 8 s | **100 cr** | **259 cr** | £0.00 *(fallback £1.28)* | £0.00 *(fallback £3.32)* | Unminted (`generation_authorized: false`) |
| `r17_pitch` | 17 | 2 | `191.00–194.82 s` | `3.82 s` | **Flow · Veo 3.1 Fast** (`football_pitch_veo_v01`) | 8 s | **10 cr** | **20 cr** | £0.00 *(fallback £0.64)* | £0.00 *(fallback £1.25)* | Unminted (`generation_authorized: false`) |
| `r08_orbit_binoculars` | 8 | 1 | `58.64–66.52 s` | `7.88 s` | **Vertex `global` · `gemini-omni-flash-preview`** (`orbit_binoculars_omni_v01`) | 8 s | **0 cr** | **0 cr** | **£0.65** | **£0.65** *(+£0.65 retry hold)* | Unminted (`generation_authorized: false`) |
| `r23_orbit_ice` | 23 | 3 | `241.88–249.84 s` | `7.96 s` | **Vertex `global` · `gemini-omni-flash-preview`** (`orbit_ice_omni_v01`) | 8 s | **0 cr** | **0 cr** | **£0.65** | **£0.65** *(+£0.65 retry hold)* | Unminted (`generation_authorized: false`) |
| **Remaining Total (4 rows)** | | | | `33.78 s` | **1 Quality + 1 Fast (Flow) · 2 Omni (Vertex)** | | **110 cr** | **279 cr** | **£1.30** | **£1.30** *(£2.60 w/ retry)* | **Parked for Chief** |

*Note on `r11_night_road` (`14.12 s` span across 3 cuts in `SHOT_LIST_v01.md`):* `PLATE_BOARDS_v02.json` prices one 8 s Quality take (`100` try-1 / `259` expected). If Chief wants a second 8 s continuation clip (`r11_night_road_c1`) so the 14.12 s span needs no slow-stretch or cutaway, adding `+1 Fast` is `+10` try-1 / `+20` expected (`120` try-1 / `299` expected total), or `+1 Quality` is `+100` try-1 / `+259` expected (`210` try-1 / `538` expected total). All three options easily clear the `3,000` Flow floor by more than `+4,450` credits.

## What the ten J0310/J0321 rulings did

1. Night road stays **Quality**. Dusk pitch stays **Fast**. Both planned on Flow. Neither is authorised to mint.
2. Both Orbit Omni takes are priced at the Gemini Omni Flash list price, 720p with audio, 8 s: **£0.65** a take, **£1.30** for the pair. Late-billing room held equal to that pair (£1.30), on top of the £1 margin. £2.60 fits inside £70.02 usable. They stay Omni. No KEEP-pose fallback.
3. r35's Gliese-motion stretch is dropped. Five stretches remain (r01, r02, r12, r27, r38). The row is filled with the NTT time-lapse at La Silla.
4. K dwarf is a £0 Codex card (K dwarf vs Sun). The labelled Hubble chart stays out.
5. The Sun is an HMI continuum intensitygram (visible light), 2024-06-01 00:00 UTC. Crop the quick-look stamp in the black corner. The limb row is a second crop of that still. AIA 335 is unused.
6. The © Slawik Hale-Bopp image is rejected. r26 is a second framing of comet C/2023 A3. r28 cannot take a third comet still (NEOWISE is already at two), so it is a £0 comet-tail card. The Columbia frame sts083-410-009 was not used: its NASA record does not state public domain.
7. Hipparcos: the file is real and the page says Copyright: ESA, so it is not cleared. The row is a £0 code card. Oort: the NASA file is a labelled diagram, rejected. Oort and the row 20 shell are one £0 code beat. The Tafreshi fulldome bt_lasilla_fd2 stays dropped. r36 is the unused window of the Brunier La Silla lapse (17 s source, 7.32 s already used at r06).
8. WISE all-sky (PIA15481 small) has no axis labels and no readable text. Kept. Gaia motion, the Gliese encounter and the EDR3 sky are flagged for picture_qa as diagrams on purpose. Neptune's corner credit says green and orange filters. Juno's says colour-enhanced.
9. Code-graphic stacks are broken by merging each named stack into one beat. A second NGC 3603 crop sits between the row 4 beat and the row 5 beat. A second ISS sunrise crop sits between the path beat and the scale card, which was the other back-to-back pair (row 16 into row 17). A rebuild check refuses two code routes in a row.

## Flow balance after 028 & headroom for HOS

On 15 Oct (`J0337`), HOS 007 was reserved at `7,553` expected credits against `23,740` left, leaving `2,949` after 028 (`51` cr short of the `3,000` gate).
On 21 Oct (`J0352`, HOS `#351`), HOS 007 minted all `73/73` Flow rows on take 1 for **`2,890` actual credits** (all Chief KEEP; `full_join_v01` assembled in `J0827` with 0 new mints), freeing **`4,663` credits** vs the `7,553` reserve (plus `+100` cr net Flow adjustment).

| Pool / Film | Try-1 Credits | Expected Credits | Balance After (Try-1) | Balance After (Expected) | Notes |
|---|---:|---:|---:|---:|---|
| **Live Flow balance (22 Oct 16:56Z)** | — | — | **20,950** | **20,950** | `benoats@googlemail.com` (CDP `:9222`) |
| **HOS 006** | 0 | 0 | 20,950 | 20,950 | Done (`full_join_v03_teach` on HOS `main`, 0 Flow) |
| **HOS 007** | 0 | 0 | 20,950 | 20,950 | Done (`73/73` rows minted & KEEP in `J0352` for `2,890` cr, already deducted from `20,950`; `full_join_v01` in `J0827`) |
| **OWB 028 (if minted next)** | **110** | **279** | **20,840** | **20,671** | 1 Quality (`259` exp) + 1 Fast (`20` exp) |
| **HOS 008** (`PRICE_REVIEW_v03`) | 2,360 | 5605 | 18,480 | 15,066 | 15 Quality + 86 Fast (11 £0 code graphics done in `J0329`/`J0383`) |
| **HOS 009 tranche 1** (`PRICE_REVIEW_v04`/`v05`) | 2,910 | 7354 | **15,570** | **7712** | 26 Quality + 31 Fast (12 £0 code graphics done in `J0342`/`J0383`) |
| **Remaining HOS sum (`006–009 T1`)** | **5,270** | **12959** | 15,680 *(before 028)* | **7991** *(before 028)* | Leaves **7991 cr** before 028 |
| **After HOS (`006–009 T1`) + OWB 028 (`279`)** | **5,380** | **13238** | **15,570** | **7712** | **PASSES the 3,000 gate by +4712 cr** (`7712 >= 3,000`) |

*Deferred to the ~12 Nov AI Ultra renewal (not charged against today's `20,950` pool):*
- **HOS 009 tranche 2:** `5180` expected (`2,000` try-1, 20 Quality rows).
- **HOS 010 (`PRICE_REVIEW_v03`):** `12,393` expected (`4,810` try-1, 47 Quality + 11 Fast rows).
- **HOS 007–010 Shorts (`SHORTS_PRICE_REVIEW_v01`) & OWB 029 (`PRICE_REVIEW_v03`):** `0` Flow credits.

## Vertex (`£71.02` Available, `£70.02` Usable)

| Item | £ |
|---|---:|
| Promo available (`CREDIT_TYPE_MONTHLY`) | 71.02 |
| Margin | 1.00 |
| Usable | 70.02 |
| 028 Omni ×2 (`r08_orbit_binoculars`, `r23_orbit_ice`), one take each | 1.30 |
| Late-billing room (one retry of both takes) | 1.30 |
| Total held for 028 (incl. £1.00 margin) | 3.60 |
| **Usable promo remaining after 028 Omni hold** | **67.42** |

Omni **fits** (`£1.30` expected, `£2.60` with retry reserve vs `£70.02` usable). Veo stays on Flow (`279` expected credits). Nothing is authorised to generate until Chief passes `J0850`.

## Full-Film Totals (`PLATE_BOARDS_v02.json`)

| plates | Quality (Flow) | Fast (Flow) | Omni (Vertex) | code (£0) | card (£0) | harvest (£0) | Flow try-1 | Flow expected | Omni £ |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 57 | 1 | 1 | 2 | 19 | 1 | 33 | 110 | 279 | 1.30 |

`generation_authorized` is `false` on every plate. Parked for Chief (`parked for Chief: 028 Flow price pass`).
