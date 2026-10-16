# 028 harvest v01 (J0350)

£0. No Flow, Vertex, Omni, Veo or ElevenLabs. `generation_authorized` stays false.

33 harvest plates, 21 files in `nasa_pool_v01/028_harvest_v01/`, 0 rejected, 0 licence FLAGs.
Media is gitignored. This note, the JSON and the SHA-256 list are the record.

| Asset | Plates | Licence check | SHA-256 |
|---|---|---|---|
| gaia_motion_1_6my | r01_stars_streaming, r02_gaia_span_2, r12_stars_move, r27_leaving, r38_return | PASS | `54335c011585` |
| gaia_edr3_sky | r03_serpens_sky, r34_sky_wide | PASS | `a831d1a88ce6` |
| ngc3603 | r05_cluster_break, r37_cluster | PASS | `8db315eb8ecf` |
| eso_mw_lasilla | r06_milky_way, r36_night_2 | PASS | `41a034531e9b` |
| sdo_hmi_continuum | r07_sun, r30_sun_limb | PASS | `003641c2b2b4` |
| gaia_gliese_encounter | r10_gliese_approach | PASS | `b356744b06f0` |
| proxima | r12_proxima | PASS | `163774dc4204` |
| eso_startrails | r13_star_trails | PASS | `d60dd20c7bef` |
| gaia_craft | r15_gaia_craft | PASS | `de1a96add15e` |
| iss_sunrise | r16_sunrise_break, r24_sunrise | PASS | `796f9cc636f8` |
| neptune | r17_neptune | PASS | `97b57802f44b` |
| neowise_dc | r22_neowise, r38_neowise_2 | PASS | `eb4b3582ca82` |
| comet_a3 | r26_hale_bopp, r26_a3 | PASS | `49791e5be78d` |
| jupiter_juno | r28_jupiter | PASS | `693f8b87032c` |
| saturn | r28_saturn | PASS | `1095bbfe968c` |
| eso_chajnantor | r29_night | PASS | `b3bc5b77bc8d` |
| conjunction | r29_twilight | PASS | `b978f27bcdce` |
| moon_lro | r30_moon, r31_moon_2 | PASS | `07b0c21e9115` |
| wise_sky | r32_wise_sky | PASS | `1ff04de1a971` |
| wise_craft | r33_wise_craft | PASS | `cf7a6f956d6a` |
| eso_lasilla_ntt | r35_lasilla_ntt | PASS | `979ddc71b993` |

Proxima Centauri (`potw1343a`) has no larger Hubble rendition. The large jpeg is 604×592, so the edit scales it to frame height (under 2.35×) and fills the sides.


## Higher rendition from the same page

- **gaia_motion_1_6my**: stored `https://dlmultimedia.esa.int/download/public/videos/2020/12/004/orig-2012_004_AR_EN.mp4` (3840×2160). Boarded file was `https://dlmultimedia.esa.int/download/public/videos/2020/12/004/2012_004_AR_EN.mp4`.
- **gaia_gliese_encounter**: stored `https://dlmultimedia.esa.int/download/public/videos/2017/08/022/orig-1708_022_AR_EN.mov` (1920×1080). Boarded file was `https://dlmultimedia.esa.int/download/public/videos/2017/08/022/1708_022_AR_EN.mp4`.
- **eso_chajnantor**: stored `https://cdn.eso.org/videos/hd_and_apple/chajnantormilkyway.m4v` (1280×720). Boarded file was `https://cdn.eso.org/videos/medium_podcast/chajnantormilkyway.m4v`.

## Notes carried from the boards

- **gaia_motion_1_6my**: data film; diagram on purpose Data animation. picture_qa flag: diagram on purpose. Five stretches in v02 (r35 dropped): r01_stars_streaming, r02_gaia_span_2, r12_stars_move, r27_leaving, r38_return
- **gaia_edr3_sky**: data film; diagram on purpose EDR3 colour sky, not a DR3 chemistry or radial-velocity map (those are labelled). Confirm pixel size at harvest. No DSS2.
- **sdo_hmi_continuum**:  HTTP 200 on the 4096 file. The 1024 preview shows the visible-light disk and a bottom-left stamp, 'SDO/HMI Quick-Look Continuum: 20240601_000000'. Crop that stamp. sdo.gsfc.nasa.gov/data/rules.php was showing a storage-failure banner this run, so the licence line is NASA's media policy, not a quote from that page. Two uses: full disk (r07) and a limb crop (r30).
- **gaia_gliese_encounter**: data film; diagram on purpose The Gliese 710 flyby. Not the annotated 'Tracking stellar motions' cut (that one draws a circle and a line).
- **gaia_craft**:  Artist's impression (WARN). Background is Brunier's Milky Way still, not the Brunier video.
- **neptune**:  Green and orange filters, not true colour. Say so in the corner credit.
- **neowise_dc**:  C/2020 F3. Second use is a new crop only.
- **jupiter_juno**:  Juno, colour-enhanced, not true colour. Say so in the corner credit.
- **saturn**:  Cassini natural-colour portrait. Chosen over PIA14922, which puts Titan in front.
- **moon_lro**:  Second use is a crop. That is the twice-still cap.
- **wise_craft**:  Artist's concept (WARN). It is the WISE spacecraft, which flew the NEOWISE mission.

## Seen at harvest

- **ngc3603**: no caption text on the file.
- **sdo_hmi_continuum**: the SDO/HMI Quick-Look stamp is in the bottom-left. Crop it at the edit.
- **gaia_gliese_encounter**: this is the flyby film (a year counter over moving stars), not the circle-and-line cut. ESA and Gaia logos and the year line are burned in.
- **eso_chajnantor**: the opening frames are an ESO slate. The Milky Way is on screen by about 8 seconds. Use that window.
- **gaia_motion_1_6my** and **gaia_edr3_sky**: data films, diagram on purpose, as the boards already flag.
