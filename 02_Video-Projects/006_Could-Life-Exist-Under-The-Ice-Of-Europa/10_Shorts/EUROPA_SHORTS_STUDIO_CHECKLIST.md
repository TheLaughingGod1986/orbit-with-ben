# Europa Shorts — Studio checklist (2 Sep 2026)

**Long:** `NbW5G1BpPY0` · Premiere **Thu 3 Sep 18:00 London**  
**Related pill on every Short:** `NbW5G1BpPY0` only  
**Thumb UAT:** yellow highlight on hook word(s) · white on the rest · vertical-centre stack · no Orbit · no all-white titles

Cloud agent **cannot** open Studio (no Google login / YouTube OAuth in this environment). Covers are built locally under `08_Thumbs/yellow_white_v01/`. Apply them in Studio (or re-run with OAuth).

## Canonical schedule (current order)

| # | YouTube id | UK schedule | Hook (yellow words in **bold**) | Cover file |
|---|------------|-------------|----------------------------------|------------|
| 01 | `FbRFvSApfOQ` | Thu **3 Sep 20:00** | **MORE WATER** / THAN EARTH | `cover_FbRFvSApfOQ.jpg` |
| 02 | `EcsunqhN0jQ` | Fri **4 Sep 11:30** | THIS OCEAN / **SHOULDN'T EXIST** | `cover_EcsunqhN0jQ.jpg` |
| 03 | `k0PjH2I0OxY` | Sat **5 Sep 11:30** | WHAT WOULD / **LIFE EAT?** | `cover_k0PjH2I0OxY.jpg` |
| 04 | `0eqTVgrlU-s` | Sun **6 Sep 11:30** | LIFE / **WITHOUT SUNLIGHT** | `cover_0eqTVgrlU-s.jpg` |
| 05 | `Fv-lSwB_Z-o` | Mon **7 Sep 11:30** | AN **OCEAN** / IN **SPACE** | `cover_Fv-lSwB_Z-o.jpg` |
| 06 | `KPO68c-U42E` | Tue **8 Sep 11:30** | **ALREADY** / **FLYING** | `cover_KPO68c-U42E.jpg` |
| 07 | `gN2qAv8m9Wc` | Wed **9 Sep 11:30** | COULD WE / **KILL IT?** | `cover_gN2qAv8m9Wc.jpg` |
| 08 | `TE_HDKAnqms` | Thu **10 Sep 11:30** | **LIFE UNDER** / ICE | `cover_TE_HDKAnqms.jpg` |

Source: Aug 25 live registry dump + `SHORTS_UPLOAD_INDEX.json` (restored). All eight were present as **private / scheduled** then.

## Studio pass (per Short)

1. Content → Short → confirm **Schedule** matches the table (Europe/London).
2. Details → **Thumbnail** → upload matching `cover_{id}.jpg` from `08_Thumbs/yellow_white_v01/`.
3. Confirm **Related video** = `NbW5G1BpPY0` (Europa long).
4. Confirm no Orbit on thumb; yellow+white centre stack reads in details preview + Shorts-list crop.
5. Do **not** remint cuts. Thumb + schedule only.

## Reconcile notes

- House bible proof id `8Bym-yrYhGc` (THIS OCEAN / SHOULDN'T EXIST) may be a later replacement for punch-02 `EcsunqhN0jQ`. If Studio shows `8Bym-yrYhGc` live, use that id for #02 and keep the same hook/date.
- Bible lists Related prefixes `1glQ` · `Xza_` · `VE0f` · `D3KS` · `eVp9` — resolve against live Studio; Aug 25 dump had the eight ids above instead.
- Bible also lists `TE_HDKAnqms` on **19 Sep** as an extra Related PASS; Aug 25 schedule had it **10 Sep 11:30**. Prefer **10 Sep** in the launch cluster unless Ben moved it — do not change dates while only swapping thumbs unless Ben asks.

## Rebuild covers

```bash
python3 00_Brand/Channel-Setup/tools/build_europa_yellow_white_short_thumbs.py
```

Requires plate: `08_Thumbs/plates/long_maxres.jpg` (from Europa long maxres).
