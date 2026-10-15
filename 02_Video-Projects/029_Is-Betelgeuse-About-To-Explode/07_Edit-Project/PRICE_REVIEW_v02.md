# 029 price review v02

Cursor, 16 Oct 2026, J0330. Applies Chief's price PASS with conditions on PR #223 (comment 6202235397). **No mint. No spend. No merge.**

Locked VO and shot list are unchanged. This table only replaces plates and prices.

## Readings (this run)

- Flow: **23740** credits at 2026-10-15T23:46:58Z. `ai_spend_daily.py --dry-run`.
- Vertex promo: **£71.02** at 2026-10-15T23:46:58Z. Usable **£70.02** after the £1 margin. Free Trial is £0.

## The nine rulings

1. **Omni ×2** priced at list, **£0.65** a take, **£1.30** for the pair, plus **£1.30** late-billing room. £2.60 fits inside £70.02. They stay Omni. Not authorised. No KEEP-pose fallback.
2. **eso1726a stays rejected.** Rows 2 and 5 use eso2109a. The page title names Betelgeuse's surface. Two framings, the still cap.
3. **Super-K** is not used. The IceCube gallery does not state a monetised-use licence, so row 24 is two windows of the Chajnantor Milky Way film. No mint.
4. **noirlab2523b** stays on the Orion-context beats, recorded as Collage not Chart. **noirlab2523c** stays on the companion-only beat. 2523a and 2523f stay rejected.
5. **Gaps.** EPIC is DSCOVR `e000678`, not Suomi. JWST Pillars are weic2216a, not Hubble. Cas A is PIA03519. Neutron and black-hole plates are NASA Goddard stills (confirm they are not labelled charts at harvest; the neutron orig is 37 KB). The half Moon is a NASA first-quarter still. Gemini night, dome and the earth-and-sky photograph are NOIRLab photographs. Spans C–E, row 6 and row 30 are five windows of the La Silla star-trail film (28 s). That page is not Paranal and does not name Orion. Spans F–G and the astrolabe are one £0 code beat: the Met API is 410, and the Commons astrolabe found is CC BY-SA, so it was not used. Row 23 and the Song object are £0 code for the same reason. The 007 hero file was not pinned.
6. **Return.** `vlttimelapseorion` is row 1 only. The hold uses a later window of the 17 s La Silla Milky Way lapse (source 5.50–14.26 s), which covers 508.50–517.26. Not a third stretch of the 6 s rise.
7. **SDO** is the HMI continuum, full disk then a limb crop. AIA 335 is not used, so no ultraviolet credit.
8. **Stacks merged** into one beat each: rows 3–4; the row 10–11 dip; rows 17–20 shells; row 31 shells and twins. No two code beats sit together.
9. **Licences re-read.** ESO copyright page: CC BY 4.0. NOIRLab copyright page: CC BY 4.0, written on every NOIRLab plate. ESA/Webb: CC BY 4.0 on the Pillars.

## Totals

| plates | Quality | Fast | Omni | code | harvest | card | hold | gap | Flow expected | Omni £ |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 63 | 0 | 0 | 2 | 13 | 47 | 1 | 0 | 0 | 0 | 1.30 |

Flow expected stays **0**. No gap was moved to Flow, so no new price pass is required for a Flow mint. Nothing is authorised to generate.

## Headroom

J0337's table, not a new sum of those films: 006 = 0, 007 = 7,553, 008 = 5,605, 009 tranche 1 = 7,354. Sum **20512**. Flow 23740 leaves **3228** before 028. After 028's 279: **2949**, which misses the 3,000 floor by 51. 029 adds nothing to that. Mint order stays the Chief's call.

`generation_authorized` is false on every plate.

Files: `SOURCE_POOL_v02.json`, `PLATE_BOARDS_v02.json`. Rebuild with `python3 _build_plate_boards_v02.py`.
