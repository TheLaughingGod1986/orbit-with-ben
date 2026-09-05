# FbRFvSApfOQ — opening remint (picture-first 0–3s)

**Ben unlock:** 5 Sep 2026 — opening remint only.  
**FAIL:** orange Orbit in first 3s on Europa ice + Jupiter.  
**House:** first 3s picture-only (no Orbit). Orbit after 3s OK.  
**Do not:** remint other Shorts · change Studio thumbs.

## Canonical cut (Mac disk)

```
02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/06_Final-Exports/europa_punch-01_ocean-we-cannot-see_v03_diamond.mp4
```

YouTube: `FbRFvSApfOQ` · Related long: `NbW5G1BpPY0`

## Remint (Mac mini)

```bash
cd ~/YouTube/orbit-with-ben
git pull
python3 02_Video-Projects/006_Could-Life-Exist-Under-The-Ice-Of-Europa/10_Shorts/_remint_fbrf_picture_first_open_v04.py
```

Writes:

- `…/06_Final-Exports/europa_punch-01_ocean-we-cannot-see_v04_picture-first-open.mp4`
- `…/06_Final-Exports/europa_punch-01_ocean-we-cannot-see_v04_picture-first-open.mp4.sha256`
- proof frames under `…/06_Final-Exports/_proof_FbRFvSApfOQ_open_v04/`
- refreshes `FbRF_OPEN_REMINT_STATUS.json` with path + sha256 + duration

## CoS → Creator Studio

Replace file on **existing** id `FbRFvSApfOQ` (do not mint a new id). Leave thumb listing alone.

## Cloud note (5 Sep)

Cloud sand/internal agents **cannot** attach to the Mac (`privateWorkerId` stays `null`). Several “remint on mac-mini” launches (including `bc-0edeb966-4479-504c-9791-dfa62496fdb8`) still booted a Linux VM with no disk mp4s. yt-dlp hits YouTube `LOGIN_REQUIRED`.

**Do not spawn another cloud remint agent.** Finish on a session that is actually on the Mac:

- worker `mac-mini` `b4eccfb5-11d8-487d-bd40-cad8dce9efa6`
- or `~/YouTube/orbit-with-ben @ Benjamin's Mac mini` `0db3ab41-e9a9-5ec5-ac19-c203de6b9eaa`

Then run the remint command above and write path + sha256 + duration into `FbRF_OPEN_REMINT_STATUS.json`.
