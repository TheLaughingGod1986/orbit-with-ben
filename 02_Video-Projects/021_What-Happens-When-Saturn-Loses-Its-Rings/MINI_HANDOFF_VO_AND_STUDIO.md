# Mini handoff — Saturn week (Ben orders 30 Sep 20:50 London)

Cloud agent on managed Linux cannot reach Mac mini (no SSH, no `07_Content-Ops/.env`, no ElevenLabs session, no Studio CDP, no iCloud). **Re-run this file on environment `mac-mini`.**

Repo: `/Users/benjaminoats/YouTube/orbit-with-ben`  
UAT: `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT`

## Done in repo (merge Ben's docs PR first, or pull this branch)

- Mon Short rev 3 OK; listing title **How Long Do Saturn's Rings Have Left?**
- Long title stays **What Happens When Saturn Loses Its Rings?**
- Fri 16 Oct = `FRIDAY_LAST_STAR_SHORT_BLACK_DWARF.md` (not LAST_LIGHT)
- 022 Sun air → Sun **18 Oct** 18:00 UK
- Retitle pack: `00_Brand/Channel-Setup/audits/RETITLE_LAST_STAR_2026-09-30.json`
- PR #96 (18 Oct new-stars shortlist) **parked** for a later week

## 1) Retitle Last Star `REXYxuLOBoI`

```bash
cd /Users/benjaminoats/YouTube/orbit-with-ben/07_Content-Ops
# If live title differs from expectCurrentTitle, fix the JSON to the actual live title first (only strip " | Orbit's Cosmic Journey").
npx tsx --env-file=.env scripts/retitle-videos.ts \
  --file ../00_Brand/Channel-Setup/audits/RETITLE_LAST_STAR_2026-09-30.json --dry-run
# Paste dry-run stdout, then:
npx tsx --env-file=.env scripts/retitle-videos.ts \
  --file ../00_Brand/Channel-Setup/audits/RETITLE_LAST_STAR_2026-09-30.json
# Paste live stdout.
```

Target title: **What Happens When the Last Star Dies?**

## 2) Jupiter end screen (before Sun 4 Oct 18:00)

- Video: **What Would You See If You Fell Into Jupiter?** id `-jmMROGoZCM`
- End screen: **Last Star** `REXYxuLOBoI` + **Subscribe**
- Use Desktop Studio CDP helpers under `scripts/` if available
- If Studio needs sign-in: stop and report exact blocker (do not fake success)
- Upload result currently has `"end_screen": false`

## 3) VO — Ben Orbit Narrator only (`kDch6ACCIpqgQ0NsU9kk`)

Stop after listen files. No picture / Veo / Omni.

1. Long: `02_Voiceover/_generate_vo_v01.py` (text in `parts/saturn_rings_vo_v01.txt`)
2. Mon Short: spoken lines only from `10_Shorts/monday_saturn_tease/MONDAY_SATURN_SHORT_RINGS_ALREADY_FALLING.md`
3. Fri Short: spoken lines only from `005_…/friday_2026-10-16_last_star/FRIDAY_LAST_STAR_SHORT_BLACK_DWARF.md`

Copy listen files to OWB UAT, e.g.:

- `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_long_vo_v01_LISTEN.wav`
- `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/monday_saturn_short_vo_v01_LISTEN.wav`
- `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/friday_black_dwarf_short_vo_v01_LISTEN.wav`

Report those exact paths + durations. Then STOP for Ben's listen (sign-off 4).
