# 027 rough v01l corner credits (J0319, 15 Oct 2026)

v01l is the locked v01k picture with house corner credits burned on. Audio is copied from v01k. No new picture, no ElevenLabs, no spend.

| | |
|---|---|
| Source | `/private/tmp/027_EarthSpin_rough_v01k.mp4` (sha256 `4f41806919ef569220c15cd293718c83a900b8be13c508a6479b047980c01ec9`) |
| Labels | CGI, NASA, NASA/JPL, ESO. Bottom-left, Arial Bold 40 px (cap about 2.7% of 1080), 1 px dark edge, no slab |
| Subscribe | cue is lower-right 167.1–171.1 s. Credits stay bottom-left, clear of it |
| Bennu | `NASA_Bennu_journey_early_Earth.jpg` already says Artist's impression on the locked cut. No second line |
| Oceans graphic | 3:06–3:19, the corner under the globe is an empty band. CGI sits on the starfield just above that band, still lower-left and off the Earth, so the gap is not read as a split panel |

Shots outside those five labels stay blank, and are listed in `credits_v01l.json`: ESA Gerst timelapses, NOAA eclipse, NIST clocks, USGS pahoehoe, and real non-agency footage (waves, pendulum, fossils, the Met tablet, the Foucault portrait, Bay of Fundy).

v01k stays the grain master. This file does not replace it until Chief passes the corner credits.

## Gates (15 Oct 2026, J0319)

| | |
|---|---|
| v01l sha256 | `7d51961fabfe7e4e66e2e3bfd457b5f0fe9fa995572682cab6ecb5c7f94d4c96` |
| Audio | AAC stream MD5 matches v01k (`041653dff8a90d3daeb98378b8152e8c`). Video is 446.233 s against v01k's 446.333 s (about 0.1 s of encode rounding). |
| picture_qa | PASS, 0 of 88 cuts fail, 40 WARN (same pool-title and soft-still notes as the locked cut) |
| polish_gate | PASS, 0 of 88 rows failed, 5 to look at (low detail already on v01k) |
| Stills | `credit_stills_v01l.jpg`, plus encoded frames at 0:04 NASA, 0:19 CGI, 0:24 chapter, 2:00 ESO, 2:48 subscribe, 3:10 oceans CGI, 4:00 NASA/JPL, 7:14 Artist's impression (one line, already on the plate) |

Masters (sha256 checked on the NAS, 15 Oct 2026). `/private/tmp` is not the only copy.

- NAS film `02_Video-Projects/027_What-If-Earth-Stopped-Spinning/07_Edit-Project/027_EarthSpin_rough_v01k.mp4` and `027_EarthSpin_rough_v01l.mp4`
- NAS `OWB UAT/` has the same two files, same hashes
- iCloud `OWB UAT/027_EarthSpin_rough_v01l.mp4` is the same byte size, next to v01k. A local read hit an iCloud deadlock, so that copy is not the checked master.

Parked for Chief. No PASS from this run.
