# J0810 — OWB 021 Short `saturn_ten_metres_thin_v01` Upload Package & Slot Proposal

- **Master verified:** `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_ten_metres_thin_j0771/saturn_ten_metres_thin_v01.mp4`
- **SHA-256:** `8337555099d673140e119a09f281e4f82947a7823fbd0b9231e8e2ffaba11ccf` (matches J0771 PASS `5366e207`)
- **Duration / words / mix:** `26.87s` · `57 words` · `-14.6 LUFS`
- **Cover:** `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_ten_metres_thin_j0771/saturn_ten_metres_thin_v01_cover.jpg` (`SATURN'S RINGS` / `10 METRES THICK`, derived from contact frame 0 plate, `thumb_preview.py short` PASS inside 16:9 centre band)
- **Title (positive search-question rule):** `How Thin Are Saturn's Rings?`
- **Parent long / Related video:** `How Long Do Saturn's Rings Have Left?` (`https://www.youtube.com/watch?v=55AEQwvs36g`, `relatedVideoId: "55AEQwvs36g"`)
- **AI / synthetic disclosure:** `containsSyntheticMedia: true` in API payload + explicit `Pictures:` / `Facts:` disclosure and `Sources:` line in description.

## Next Free OWB Short Slot Proposal (No Collisions)

Checked against `00_Brand/Channel-Setup/social/UPLOADS.json`, `05_Analytics/owb/snapshots/2026-10-21.json`, `05_Analytics/owb/UPCOMING_SHORTS_GATE.md`, and all repo `PACKAGE_MANIFEST.json` files:

| Date (London) | Status | Scheduled Video |
|---|---|---|
| Thu 22 Oct 2026 11:30 | Booked | `82Ao0v5XiQI` — *Are Saturn's Rings Younger Than Saturn?* |
| Fri 23 Oct 2026 11:30 | Booked | `2e-giqFmfy8` — *Why Didn't Earth Freeze Under a Dimmer Young Sun?* |
| Sat 24 Oct 2026 11:30 | Booked | `vlkj8RQKmH8` — *A Day on Mercury Lasts Two Years* (Standalone S1) |
| Sun 25 Oct 2026 18:00 | Booked (Long) | `VBaYRPp85Sw` — *What Happened to Venus?* |
| Mon 26 Oct 2026 11:30 | Booked | `dM1OgGPAYvw` — *What If Earth Stopped Spinning?* |
| Tue 27 Oct 2026 11:30 | Booked | `oyRcrFTYyDY` — *The Wind on Neptune Is Supersonic* (Standalone S2) |
| Wed 28 Oct 2026 11:30 | Booked | `BbsyFrV8kCY` — *An Asteroid Will Skim Past Earth on Friday the 13th* |
| Thu 29 Oct 2026 11:30 | Booked | `Jcuiy0a9BFI` — *Why Venus Melts Lead* |
| **Fri 30 Oct 2026 11:30** (`2026-10-30T11:30:00.000Z`) | **FREE (Proposed #1)** | **No OWB Short or long scheduled** (7 non-Saturn Shorts since `82Ao0v5XiQI` on 22 Oct) |
| Sat 31 Oct 2026 11:30 | Booked | `XKlq0TK1OVA` — *Astronauts See 16 Sunrises Every Day* (Standalone S3) |
| **Mon 2 Nov 2026 11:30** (`2026-11-02T11:30:00.000Z`) | **FREE (Fallback #2)** | Next free weekday Short slot if 30 Oct is used for another Short |

## Gate & Dry-Run Output

```
PASS  saturn_ten_metres_thin_v01.mp4  dur=26.87s  audio=-17.9dB  motion=14.66  dhash=6994e4c03c050010  visor=0.0
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/orbit_shorts_gate/saturn_ten_metres_thin_v01_open_sheet.jpg
```

`npm run youtube:package -- --package ../02_Video-Projects/021_What-Happens-When-Saturn-Loses-Its-Rings/10_Shorts/lift_ten_metres_thin/11_Upload-Package --video "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT/saturn_ten_metres_thin_j0771/saturn_ten_metres_thin_v01.mp4" --dry-run`:
- `ok: true`, `dryRun: true`
- `scheduledFor: "2026-10-30T11:30:00.000Z"`
- `sha256: "8337555099d673140e119a09f281e4f82947a7823fbd0b9231e8e2ffaba11ccf"`
- `responseSummary: {"title":"How Thin Are Saturn's Rings?","privacyStatus":"private","publishAt":"2026-10-30T11:30:00.000Z","madeForKids":false,"containsSyntheticMedia":true,"categoryId":"28","contentFormat":"shorts"}`

No upload, no Studio change, and no Buffer post were run. Parked for Chief final OK.
