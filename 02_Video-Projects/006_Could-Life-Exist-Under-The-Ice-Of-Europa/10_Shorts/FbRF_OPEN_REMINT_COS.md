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

This cloud VM has no disk mp4s (`disk_only: true`). Self-hosted **mac-mini** worker `b4eccfb5-11d8-487d-bd40-cad8dce9efa6` was online/idle but this run could not target it (`privateWorkerId: null`). Redispatch on **mac-mini** to finish sha256 delivery.
