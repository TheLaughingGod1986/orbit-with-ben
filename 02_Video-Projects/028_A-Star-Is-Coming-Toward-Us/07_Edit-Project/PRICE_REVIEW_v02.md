# 028 price review v02

Cursor, 15 Oct 2026, J0321. Applies Chief's price PASS with conditions on PR #218 (comment 6199532687). **No mint. No spend. No merge.** Parked for Chief. Mint order stays the Chief's call.

v01 files are unchanged. Rebuild with `python3 _build_plate_boards_v02.py`.

## Readings this run

- Flow: **23740** credits at 2026-10-15T22:38:00Z. Account picker, the Ultra account, CDP :9222. No spend logged after it.
- Vertex promo: **£71.02** Available (Developer Program monthly). Free Trial **£0.00 Used**. Usable **£70.02** after the £1 margin. No spend logged after it.

## What the ten rulings did

1. Night road stays **Quality**. Dusk pitch stays **Fast**. Both planned on Flow. Neither is authorised to mint.
2. Both Orbit Omni takes are priced at the Gemini Omni Flash list price, 720p with audio, 8 s: **£0.65** a take, **£1.30** for the pair. Late-billing room held equal to that pair (£1.30), on top of the £1 margin. £2.60 fits inside £70.02 usable. They stay Omni. No KEEP-pose fallback.
3. r35's Gliese-motion stretch is dropped. Five stretches remain (r01, r02, r12, r27, r38). The row is filled with the NTT time-lapse at La Silla.
4. K dwarf is a £0 Codex card (K dwarf vs Sun). The labelled Hubble chart stays out.
5. The Sun is an HMI continuum intensitygram (visible light), 2024-06-01 00:00 UTC. Crop the quick-look stamp in the black corner. The limb row is a second crop of that still. AIA 335 is unused.
6. The © Slawik Hale-Bopp image is rejected. r26 is a second framing of comet C/2023 A3. r28 cannot take a third comet still (NEOWISE is already at two), so it is a £0 comet-tail card. The Columbia frame sts083-410-009 was not used: its NASA record does not state public domain.
7. Hipparcos: the file is real and the page says Copyright: ESA, so it is not cleared. The row is a £0 code card. Oort: the NASA file is a labelled diagram, rejected. Oort and the row 20 shell are one £0 code beat. The Tafreshi fulldome bt_lasilla_fd2 stays dropped. r36 is the unused window of the Brunier La Silla lapse (17 s source, 7.32 s already used at r06).
8. WISE all-sky (PIA15481 small) has no axis labels and no readable text. Kept. Gaia motion, the Gliese encounter and the EDR3 sky are flagged for picture_qa as diagrams on purpose. Neptune's corner credit says green and orange filters. Juno's says colour-enhanced.
9. Code-graphic stacks are broken by merging each named stack into one beat. A second NGC 3603 crop sits between the row 4 beat and the row 5 beat. A second ISS sunrise crop sits between the path beat and the scale card, which was the other back-to-back pair (row 16 into row 17). A rebuild check refuses two code routes in a row.

## Flow headroom

Expected credits already reserved, takes-per-KEEP (Quality 2.59, Fast 1.96), the same rates as v01:

| Film | Expected | Where it comes from |
|---|---:|---|
| HOS 006 | 3182 | 17 Fast and 11 Quality still unminted (J0138's 1,270 try-1). The five Vertex first-takes are not in this. |
| HOS 007 | 7553 | 55 Fast and 25 Quality (J0138's 3,050 try-1) |
| HOS 008 | 5605 | PRICE_REVIEW_v03 |
| HOS 009 | 13848 | boards v02. A later v03 would reserve more, not less. |
| **Sum** | **30188** | |
| OWB 028 | 279 | one Quality (259) and one Fast (20) |

Flow left 23740. After 006/007/008/009: **-6448**. After 028's 279: **-6727**.

The gate is 3,000 left after those spends. **It does not pass today.** The two Veo plates stay planned on Flow. They are not moved to Vertex, and they are not authorised to mint. Alone, 279 against 23740 would fit. The mint waits until a live reading leaves 3,000 after the earlier films' expected spend, which is the Chief's call on order.

A Flow retake of 006's five already-minted Vertex plates, if UAT rejects them, is not in the 3182. That would add about 337 expected credits and the headroom would be worse.

## Vertex

| | £ |
|---|---:|
| Promo available | 71.02 |
| Margin | 1.00 |
| Usable | 70.02 |
| Omni ×2, one take each | 1.30 |
| Late-billing room (one retry of both) | 1.30 |
| Held | 3.60 |

Omni **fits**. Veo stays on Flow. The two Flow rows still carry v01's Vertex fallback (£1.92 try-1, £4.57 expected). That is not the route, and it is not in the hold above. Nothing is authorised to generate.

## Totals

| plates | Quality | Fast | Omni | code | harvest | Flow try-1 | Flow expected | Omni £ |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 57 | 1 | 1 | 2 | 19 | 33 | 110 | 279 | 1.30 |

Holds, gaps and blocked rows from v01 are cleared or replaced. `generation_authorized` is false on every plate.
