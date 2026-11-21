# QA & Acting-Chief Sign-Off Report — `WW2:001` (`v43`)

- **Film:** `WW2:001` — *How Britain Built Two Harbours in Secret and Floated Them to Normandy*
- **Cut Reviewed:** `07_Edit-Project/integrated_v43/mulberry_scored_draft_v43.mp4`
- **Reviewer & Authority:** `gemini` — elected acting Chief (`chief_relay.py status` verified `2026-11-20T20:42Z`: Claude, Grok Bot, and Codex down; Gemini UP and elected Chief)
- **Date:** `2026-11-20`
- **Verdict:** **PASS TO BEN'S WATCH** (internal UAT & board watch handoff only; no YouTube upload until Ben watches and OKs)

---

## 1. Technical & Delivery Checks — PASS

| Check | Result | Measurement |
|---|---|---|
| Video stream | **PASS** | `1920×1080`, `25 fps`, H.264, `41,418` contiguous frames (`27:36.72`), `130,093,259` bytes |
| Full decode | **PASS** | Completed with `0` decode errors on NAS master |
| Audio stream | **PASS** | `48 kHz` stereo AAC (`mulberry_harbours_vo_v01` + 3-cue custom score `mulberry_score_timeline_draft_v01.wav`) |
| Loudness (`ebur128`) | **PASS** | Integrated **`-15.2 LUFS`**, LRA **`3.4 LU`**, True Peak **`-1.6 dBFS`** (zero clipping) |
| Black frames (`blackdetect d=0.5`) | **PASS** | **0** black frames detected across `27:36.72` |
| Silence gaps (`silencedetect -45dB d=2.5`) | **PASS** | **0** silence gaps detected |
| Voiceover audit (`J2992`) | **PASS** | `3,358` words (`20,431` chars, under `21,000` pilot cap); `99.88%` normalized Scribe match; `0` clipped words |

---

## 2. Archive Provenance, Picture Balance & Editorial Policy — PASS

- **Archive coverage:** **`47.66%`** (`102` archive scenes across `79` unique official US/UK wartime photographs; `52.34%` original code-drawn maps and engineering schematics). Longest non-archive stretch is `26.92 s` (pure engineering diagram explanation).
- **Licence & provenance:** Every photograph is individually logged with collection, ID, SHA-1/SHA-256, and licence in `03_Picture/ARCHIVE_PROVENANCE.md` and `03_Picture/archive_evidence_v43.json` — strictly US federal public domain (USN/USCG/US Army Signal Corps/NARA/NHHC/LoC) or UK Crown copyright expired (IWM Official Collections). Zero wire/agency photos (AP, Getty, Pathé), zero private donations, zero gore/shock framing, zero reused OWB/HOS assets, zero Veo clips.
- **Upscale check:** All v43 archive inserts `<= 1.377×`.

---

## 3. Direct Audio & Visual Watch-Through QA (`gemini`, 20 Nov 2026) — PASS

- **Capability honesty:** Direct `read_file` playback delivered **native continuous audio** (`audio_input`, recorded in `chief_relay.py capabilities`) and **1-fps synced visual frames** (`00:00..00:26`) across **14 review clips** covering all 6 chapters (`~310 s` sampled across the full `27:36.72` runtime):
  1. `00:00–00:25` — Cold Open (`IWM A 25799` tow, 150-tug schematic, `IWM C 4663` aerial mosaic, Spud/Whale cross-section)
  2. `01:58–02:20` — Dieppe raid (`IWM A 11234`, 29 Churchill tanks animation, 3-hour clock, `IWM C 3082` waterfront, flint cobbles)
  3. `05:05–05:25` — Chapter 1 transition (`05:09` cut, `IWM H 32129` Churchill at Quebec, "Piers for Use on Beaches")
  4. `08:18–08:40` — Garlieston trials (`IWM H 30925` Crusader III tanks on Spud pierhead, flexing Whale vs rigid Hippo scour animation)
  5. `09:45–10:05` — Chapter 2 transition (`09:48` cut, 5 interlocking rings schematic, `IWM A 25814` Bombardons, `IWM B 5726` Phoenix breakwater)
  6. `12:55–13:17` — Thames construction & concealment (`80-G-285141` Spud towers, `IWM H 36496` London docks Phoenix caisson)
  7. `13:54–14:14` — Chapter 3 transition (`13:57` cut, `IWM A 24117` Selsey Bill, pumping schematic)
  8. `15:12–15:34` — Channel tow chop (`IWM B 5689` Whale/Beetle under tow, dipping Beetle pontoon animation, 40% Omaha tow grid)
  9. `15:42–16:04` — Gooseberry blockships (`80-G-285123` Omaha line, 4 old warships highlight, `IWM A 24075` Arromanches survey ships)
  10. `18:34–18:54` — Chapter 4 storm onset (score crossfade at `18:33`, `26-G-2963` Omaha breakwater waves beside Centurion)
  11. `20:25–20:47` — Omaha scour failure (`SC 195880` pre-storm causeway, undertow scour animation)
  12. `22:44–23:04` — Chapter 5 verdict onset (Omaha-to-Arromanches Natural Earth map, score crossfade at `22:47`, `IWM A 24675` Port Winston)
  13. `24:10–24:35` — Operation PLUTO (`IWM T 32` Conundrum drum, `IWM T 31` welded pipe, `IWM T 36` Dungeness control centre, Bambi map)
  14. `27:10–27:36.72` — Finale & closing (`520,000 TONS / 220,000 TROOPS`, `IWM BU 1021`, `IWM A 24084`, `IWM BU 1024`, clean final cadence)
- **Audio findings:** Ben's narration is clear, steady, and natural throughout; zero clipping, clicks, or chapter-join glitches. Three-cue custom score (`engineering_v01`, `storm_v01`, `verdict_v01`) transitions smoothly at `18:33` and `22:47`, stays well beneath the voice, and supports the dramatic turns without competing with speech.
- **Visual & editorial findings:** Archive images match spoken claims and carry clean, legible credit lines; code maps and diagrams animate smoothly with honest explanatory disclaimers. **One package fix made:** Chapter 4 timestamp corrected from provisional `18:37` to verified **`18:33`** so it aligns with the exact sentence (*"48 hours later, the barometer plunged."*), scene cut (`1113.32 s`), and music crossfade (`1113.32 s`).
- **Continuous 25-fps motion note:** `read_file` on `.mp4` delivers 1-fps frames plus continuous audio rather than full 25-fps continuous visual playback; every cut is a deterministic linear still zoom or deterministic 25-fps Python-rendered graphic verified frame-contiguous (`41,418` frames, `0` decode errors). Ben's watch-through on the full moving file is the final sign-off before upload.

---

## 4. Packaging & Thumbnail — PASS

- **Title:** `How Britain Built Two Harbours in Secret and Floated Them to Normandy` (`69` chars, complies with `studio/RULES.md` §2).
- **Thumbnail:** Selected `B` (`FLOATING PORT`, `IWM BU 1024`, bright B&W aerial) verified readable at full size and `168×94` phone preview (`ww2_001_thumb_phone_v01.jpg`); `A` (archive-only) retained for Test & Compare.
- **Metadata:** `11_Upload-Package/metadata_v43.json` reconciled to all 79 archive IDs, 6 verified chapters, 6 primary sources, and honest how-made disclosure (`2,955` chars).

---

## 5. Acting Chief Decision

**PASS TO BEN'S WATCH (`WW2:001` v43).** Placed in `WW2 UAT`, uploaded to the private board watch store (`/api/watch?v=ww2-001-v43`), and listed on Ben's Studio board for his watch. **No YouTube upload or scheduling until Ben ticks OK.**
