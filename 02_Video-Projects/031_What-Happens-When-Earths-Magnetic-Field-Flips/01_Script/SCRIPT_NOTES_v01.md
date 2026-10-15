# 031 What Happens When Earth's Magnetic Field Flips? — script v01 notes (J0259)

Drafted by Gemini (`gemini-agy`, stand-in worker) for J0259, 15 Oct 2026. **Draft only.** The topic isn't locked (Chief locks it after the neighbour pass), and the script isn't locked (Chief's script review, then the Gemini facts pass and Claude's quote check before any VO). No spend.

## Result

- `npm run review:script`: **PASS 95.4 / 100** (v00 was 92.6 at 1,731 spoken words / 12.0 min). 1,300 spoken words (1,321 reviewer words, 8.8 min), 6 chapters.
- Subscribe beat at 38% of spoken words (11 words: *"New space mysteries every Sunday. Subscribe and they'll come to you."*).
- Markers: DATA 7 · SCALE 7 (SCALE count ≥ DATA count) · WHO 3 · WHEN 5 · FACT 4.
- First concrete answer (*"No. We will survive."*) lands by about 0:08. The main question (*"So why do satellites in orbit already have to shut down over the South Atlantic, how do we know Earth's compass can turn upside down, and what will the night sky look like when the poles trade places?"*) lands by about 0:25.

## Number object per chapter (per-chapter teaching gate)

| Chapter | Number object | People and dates |
|---|---|---|
| Hook | North magnetic pole path and speed bar (up to ~55 km/yr; scale: faster than a marathon every year) | WHEN 1830s → today |
| 1 The Backwards Lava | Rock-age bar snapping from Normal to Reversed at 780,000 years ago (scale: >2× modern human history) | WHO Bernard Brunhes (1867–1910), Motonori Matuyama (1884–1958); timeline starts (1906, 1929, 780,000 years ago) |
| 2 The Ocean of Liquid Iron | 183-reversals counter (in 83 million years) + 9% field-drop line chart since the 1830s (scale: phone battery 100% → 91%) | WHO Carl Friedrich Gauss (1777–1855); timeline + 83 million years ago, 1830s |
| 3 The Dent Over South America | Radiation-belt altitude comparison bar dipping from 1,000 km down to 200 km vs ISS at 400 km (scale: half ISS height) | timeline + 1970, 2013, 2016 |
| 4 The Tree That Remembered | Field-strength slider dropping from 100% down to 6% during the Laschamp event as radiocarbon spikes (scale: <1/10th shield inside one tree trunk) | timeline + 41,000 years ago |
| 5 Why Our Air Stays Put | Atmospheric shield scale comparing Earth's air column (~1,000 g/cm²) to 10 m of water overhead + flip duration bar (1,000–10,000 years) | — |
| 6 Eight Poles in the Sky | Multipole map lighting up from 2 poles to 4–8 poles during a 1,000–10,000 year transition (scale: 40–400 human generations of global auroras) | — |

The timeline builds across the film, so it counts as one DATA moment. No two code graphics run back to back; real moving imagery sits between them in every chapter.

## What changed from v00

- Spoken word count trimmed from 1,731 words (~12.0 min) to 1,300 words (~8.8 min), right on the 1,200–1,300 spoken-word lock while raising `review:script` from 92.6 to **95.4 / 100** (10/10 hook, 8/8 structure gates).
- The agenda line in the hook (*"In this film I will show you…"*) is cut per Lesson 7 (Codex's idea 5).
- Added WHO card and spoken attribution for **Carl Friedrich Gauss (1777–1855)** in Chapter 2 for the 1830s start of absolute magnetic field intensity measurements.
- Added real ocean-ridge footage between the Atlantic magnetic-barcode graphic and the 9% drop chart in Chapter 2 so no two code graphics run back to back.
- Every chapter opens cold and ends on the question that the next chapter answers; the midpoint twist (*"Wrong. We are not overdue"*) lands at ~60% (Chapter 4 open), followed by the scariest idea explained away with numbers in Chapter 5.

## Open items

1. **Chief:** the topic lock (needs the neighbour pass logged in `PRE_BUILD_VIDIQ_AUDIT.md`, plus decision on whether a Short runs first) and the script review.
2. **Gemini facts pass (`facts` job):** every row in `SOURCES.md` is marked `TO VERIFY` with candidate URLs and where to look; the `facts` pass must verify verbatim quotes on each linked page before `CLAUDE_QUOTE_CHECK_v01.md`.
3. **Archive portraits:** confirm public-domain portrait sources for Bernard Brunhes (1867–1910), Motonori Matuyama (1884–1958) and Carl Friedrich Gauss (1777–1855) before the shot list.
4. **Hand-off line:** Chapter 6 hands off to Titan (*"What Would Happen If You Landed on Titan?"*, #2 in `IDEAS_2026-10-15_J0251.md`); adjust if Chief picks a different 032 topic.
