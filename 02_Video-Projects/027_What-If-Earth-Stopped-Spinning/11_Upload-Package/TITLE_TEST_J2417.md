# 027 title + thumbnail-text test (J2417, MacBook, 8 Nov 2026)

Shape: Orbitra's two hits (*"When Our Solar System Lost a Planet (And It Might Still Be Out There)"* 38k; *"Our Sun Had a Twin (And It's Still Out There)"* 21k). A lost thing, then why it still matters, in a bracketed tail. Every fact comes from the locked script `01_Script/earth_spin_script_master_v01.md`.

## Before (live on the private scheduled upload)

- YouTube id: `6bbbvfCx6zY` (Private, publishAt 2026-11-22T18:00Z)
- Title: **What If Earth Stopped Spinning?**
- Thumbnail: A set (`08_Thumbnail/abc_v01`)

## Candidates

| # | Title | Chars | Script line it rests on |
|---|---|---|---|
| 1 | **Earth Is Losing Its Spin (And the Moon Is Taking It)** | 52 | "Every day, a tiny amount of spin is lost. Where does it go? Into the Moon." |
| 2 | **Earth's Day Used to Be 22 Hours (And It's Still Getting Longer)** | 63 | "Back then, a day was only about twenty-two hours long." / "the day has been growing longer, by nearly two thousandths of a second every century" |
| 3 | Where Earth's Lost Spin Goes (And Why Your Clocks Noticed) | 57 | leap seconds: "timekeepers have added an extra second ... twenty-seven times" |

## Pick for Test & Compare

| Arm | Title | Thumbnail text (2-4 words, no title words) | One big object |
|---|---|---|---|
| A | Earth Is Losing Its Spin (And the Moon Is Taking It) | **4 CM A YEAR** | The Moon, huge and bright, edge-lit on black, Earth a thin crescent at the corner |
| B | Earth's Day Used to Be 22 Hours (And It's Still Getting Longer) | **CORALS KEPT COUNT** | One fossil coral, close-up, growth lines sharp, warm light on dark ground |

Why these two: A is the Moon story (where the spin goes), B is the deep-time clock (corals). Different objects, different colours (cold white vs warm), so the test can separate them.

Fact notes:
- B: "still getting longer" is the long-term trend the script states ("Earth is slowing down already, right now"). The script also says recent years ran a touch fast; the title claims the trend, not every year, which the film covers.
- A: the film is clear Earth will never stop; the title does not say it will.

No fear framing, no hedge, no hashtag, no series suffix.

## After (applied 2026-11-09T01:43Z, J2430)

- **Built thumbnails (`08_Thumbnail/j2417_v01`, `abc_*` untouched):**
  - **Arm A:** `027_j2417_A_4_cm_a_year_v01.jpg` (`SHA-256: dc1373490ab0ab37dd9c9d56dec2d33133191a3b393819c73ff9a6c0393ef8d0`, **4 CM A YEAR**, huge bright edge-lit Moon on dark blue-black with thin Earth crescent at corner, no Orbit) — `thumb_preview.py --score`: `PASS  027_j2417_A_4_cm_a_year_v01.jpg  saturation=161.3  near_black=2%`
  - **Arm B:** `027_j2417_B_corals_kept_count_v01.jpg` (`SHA-256: b7a2cc2875f950cbc9b79528572e098575f922a8c80dde4240db775fd7e0ad46a`, **CORALS KEPT COUNT**, Devonian fossil coral close-up with sharp growth lines in warm light on dark ground, no Orbit) — `thumb_preview.py --score`: `PASS  027_j2417_B_corals_kept_count_v01.jpg  saturation=218.6  near_black=3%`
  - **168×94 preview sheet:** `027_j2417_preview_sheet_v01.jpg` (`SHA-256: 8e89e3d6467362f858b032192973bf09c90231e18a672c6d8e4a24fb5c08c473`)
- **Applied in YouTube Studio (`6bbbvfCx6zY`, CDP 9223, `Title and thumbnail` Test & Compare, `T008` in `05_Analytics/tests/THUMB_LEDGER.json`):**
  - No prior test was running (`#ab-test-button` showed `"A/B testing"`).
  - **Slot 1 (Arm A):** Title `Earth Is Losing Its Spin (And the Moon Is Taking It)` + Thumbnail `027_j2417_A_4_cm_a_year_v01.jpg`
  - **Slot 2 (Arm B):** Title `Earth's Day Used to Be 22 Hours (And It's Still Getting Longer)` + Thumbnail `027_j2417_B_corals_kept_count_v01.jpg`
  - **Saved & Read Back (YouTube Data API v3):** `title: "Earth Is Losing Its Spin (And the Moon Is Taking It)"`, `privacyStatus: "private"`, `publishAt: "2026-11-22T18:00:00Z"`, `madeForKids: false`, `defaultLanguage: "en-GB"`, `defaultAudioLanguage: "en-GB"`, Studio `saveDisabled: true` (`Changes saved`).

Air: Sun 22 Nov 18:00 London.
