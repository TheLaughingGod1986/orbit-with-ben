# Venus 023 Part01 rough v01

Built Ch0 + Ch1, rows 1–18, locked VO 0–142.22 s unchanged in timing. Runtime **142.232 s**, 1920×1080, 30 fps, H.264/AAC. Measured integrated loudness **-14.3 LUFS**. Music: `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/jupiter-music.mp3` (existing house bed, 14% level, starts 8 s into bed after quiet intro; 2 s acrossfade joins source 79.5 s to 86 s to remove its quiet break; acrossfade-loop support, full runtime). No spend, generation, downloads, posting, claims, commits or push.

Frame 0: PIA00254 pushing immediately; no title/fade/Orbit. Ch1 lower-third 43.74–46.24 s, aligned to first spoken word. 0.7 s chapter breath preserved. 0.4 s crossfades. Rows 8, 15a, 17 and 18 split internally; all picture cuts 4–6 s. Measured two-pass loudnorm after amix normalize=0. NASA stills colour graded, shadows lifted, 16:9 cover; no >2.35x source upscale. Credits: NASA/JPL; Earth NASA; transit NASA/SDO/SVS. Existing albedo video used continuously across 13c/14a, no replacement graphic.

## Substitutions
[
  {
    "row": "1",
    "reason": "Magellan flyover not harvested; mandated PIA00254 fallback"
  },
  {
    "row": "16b",
    "reason": "PIA00093 500x568 would exceed 2.35x upscale; PIA00159 harvested high-resolution Magellan substitute"
  },
  {
    "row": "17",
    "reason": "Unnamed Sedna/lava perspective unavailable; harvested PIA00246 perspective"
  },
  {
    "row": "18",
    "reason": "Unnamed low-plains/haze unavailable; harvested PIA00087 plains"
  },
  {
    "row": "15a part2",
    "reason": "Extra 4\u20136s cut uses harvested PIA00200 Magellan terrain; row15b starts later, alignment flag disclosed"
  }
]

## Checks and limitations
Detection FAIL rows: []. Alignment flags: ["15a", "15b"]. Pace exceptions after picture-only cut adjustments (seconds): []. These are reported for review; not a full-film ship approval. VO pauses are expected and listed independently of mixed audio gaps. Row 8 carries picture across breath to 43.58 s. Detector details and original logs included. Part ends directly at Ch1 boundary; no full-film outro inserted.

PIA23791 uses: 2; reserve at most one for rest of film. No Venera or Orbit. Thread status attempted; DNS unavailable, no thread read claimed.

Output: `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/023_Venus_Part01_rough_v01.mp4`

Final encoded NASA-still midpoint samples: maximum near-black area **0.804%**, all below 30% (luma <=25/255). SDO transit and the locked albedo retain their supplied dark backgrounds. These are midpoint samples, supported by full-runtime blackdetect; no claim of an every-pixel/every-frame area audit.

Output duration exceeds 142.22 s by **0.012357 s** for the final 30 fps frame; the locked last word ends 142.20 s and Ch2 starts 142.98 s. All detected VO pauses retained. Rows 15a/15b share a picture boundary at **105.10 s**, versus **102.80 s** in the shot list (+2.30 s); no spoken audio was moved.
