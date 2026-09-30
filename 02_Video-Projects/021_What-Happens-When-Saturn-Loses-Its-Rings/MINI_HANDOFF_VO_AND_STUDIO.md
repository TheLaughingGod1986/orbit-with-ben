# Mini handoff — Saturn week (Ben 30 Sep 20:55 London)

Cloud Linux cannot reach Mac mini. **Re-run on environment `mac-mini`.**

Repo: `/Users/benjaminoats/YouTube/orbit-with-ben`  
Branch: `cursor/saturn-week-ben-orders-da79` (or `main` after PR #97 merges)  
UAT: `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT`

## Titles (Ben confirmed 30 Sep 20:57 — do not re-ask)

| Surface | Exact title |
|---|---|
| **LONG everywhere** | How Long Do Saturn's Rings Have Left? |
| **Mon Short listing title** | Saturn's Rings Are Already Falling |
| **Mon Short 9–14 s card + spoken end line** | How Long Do Saturn's Rings Have Left? |
| Fri Short listing | Why No Black Dwarf Exists Yet |
| Last Star live (after retitle) | What Happens When the Last Star Dies? |

## 1) Pull branch

```bash
cd /Users/benjaminoats/YouTube/orbit-with-ben
git fetch origin cursor/saturn-week-ben-orders-da79
git checkout cursor/saturn-week-ben-orders-da79
git pull origin cursor/saturn-week-ben-orders-da79
```

## 2) Retitle Last Star `REXYxuLOBoI`

```bash
cd 07_Content-Ops
# If live title ≠ expectCurrentTitle, edit the JSON to the actual live title first (only strip " | Orbit's Cosmic Journey").
npx tsx --env-file=.env scripts/retitle-videos.ts \
  --file ../00_Brand/Channel-Setup/audits/RETITLE_LAST_STAR_2026-09-30.json --dry-run
# Paste full dry-run stdout, then live:
npx tsx --env-file=.env scripts/retitle-videos.ts \
  --file ../00_Brand/Channel-Setup/audits/RETITLE_LAST_STAR_2026-09-30.json
```

## 3) Jupiter end screen (before Sun 4 Oct 18:00)

- Id `-jmMROGoZCM` — *What Would You See If You Fell Into Jupiter?*
- End screen: Last Star `REXYxuLOBoI` + Subscribe
- If Studio needs sign-in / CDP down: stop and report exact blocker

## 4) VO — Ben Orbit Narrator (`kDch6ACCIpqgQ0NsU9kk`)

Spoken text for the long is already regenerated in:
`02_Voiceover/parts/saturn_rings_vo_v01.txt` (locked script + Ben's two line fixes).

Prior repo VO was **STALE** (pre-rewrite). **Full regenerate** the long (not a two-line splice of the old take). Then Mon + Fri Shorts.

1. Long: `python3 02_Voiceover/_generate_vo_v01.py` (fix `TOOLS` path if needed to local `04_Audio/tools`)
2. Mon Short spoken lines from `10_Shorts/monday_saturn_tease/MONDAY_SATURN_SHORT_RINGS_ALREADY_FALLING.md` — end line must say **How Long Do Saturn's Rings Have Left?**
3. Fri Short from `005_…/FRIDAY_LAST_STAR_SHORT_BLACK_DWARF.md`

Copy to OWB UAT listen names:

- `…/OWB UAT/saturn_long_vo_v01_LISTEN.wav`
- `…/OWB UAT/monday_saturn_short_vo_v01_LISTEN.wav`
- `…/OWB UAT/friday_black_dwarf_short_vo_v01_LISTEN.wav`

Update `02_Voiceover/VO_STATUS.md` from STALE → DONE with duration + sha256 of the listen/master file.  
**Do not force-commit `.wav`/`.mp3`** (gitignored). Commit `VO_STATUS.md` + txt only. Report Mac paths.

## 5) Stills for Ben OK — then STOP

Per PLAN + CoS: after VO is ready for listen, make AI Studio stills (open plate, two science plates, Orbit ref) for Ben's OK. **Stop. No Veo/moving cut until he OKs the stills.**
