# 026 Nearest Star v05c: NUMBER overlays (J0148)

Cursor (stand-in for Codex on a `chart` job), 12 Oct 2026. Advisory: Chief scores the gate.

- Rulings applied (Chief, #99 6122765281, 12 Oct): a to-scale graphic with no numeral does **not** count as NUMBER; "1 year" for the spoken "a year" is a WORDS **PASS**. So chapter 1's `lightyear` labels stay as they are, and the open and chapters 2, 3 and 5 get labels.
- Cut: `/private/tmp/026_NearestStar_v05c_PHONE.mp4` (sha256 in `SHA256.txt`). It is v05b's picture (`nearest026_rough_work_v05b/picture.mp4`, restored from the NAS scratch archive of 10 Oct and checked against its sha256 manifest) with the labels added; the audio stream is copied from the v05b master (`audio_v05c.json`). No cut, VO, bed or graphic change, no spend.
- Builder: `../_overlay_nearest_star_v05c.py` (`--plan` lists every label with its time, place and source check). Renders: `code_graphic_026_row<row>_<k>.png`, one per label (the timeline is a strip plus the date that drops onto it), listed per cut in `cuts_v05c.json` (`overlays`) and in `overlays_v05c.json`.
- Style: the chapter-card pill (navy 23,36,55 at 86%, white Arial Bold 72–84 px), in on the VO word's start with a 0.35 s fade and rise, out with a 0.3 s fade, never on screen more than 4 s. Every label is 4 words or fewer, the VO's own words, with spoken numbers as numerals. The timeline's new date is yellow and drops 40 px onto the strip; dates already said stay white.
- Gates: `picture_qa_v05c.txt` PASS (0 of 103 cuts fail), `polish_gate_v05c.txt` PASS (0 of 103). Audio md5 identical to v05b. Stills: `overlay_stills_v05c.jpg`. A first render put "1838" on the parallax graphic's white star and crowded 2031/2035 on the timeline; both were fixed and re-rendered before these gates.

## Every row of the prep table

| Film time | Chapter | Row | Label | Source check (`01_Script/SOURCES.md`) |
|---|---|---|---|---|
| 0:11.1 | Open | 2 | More than 4 years | light takes about 4.24 years |
| 3:02.6 | 2 | 14 | 1838 (WHEN, over `parallax`) | Bessel, 61 Cygni, 1838 |
| 3:14.3 | 2 | 14 | About 13 kilometers | 2 cm coin at about 13.2 km |
| 3:31.3 | 2 | 15 | More than a billion | Gaia DR3: 1.46 billion with parallax |
| 3:42.0 | 2 | 15 | About 5 kilometers | coin at about 5.4 km |
| 4:06.5 | 3 | 18 | About 15 meters | pinhead 15 m at 1 : 10¹⁰ |
| 4:29.6 | 3 | 20 | About 4,000 kilometers | Proxima about 4,000 km at 1 : 10¹⁰ |
| 5:00.3 | 3 | 22 | 1977 (WHEN) | Voyager 1 launched 5 Sep 1977 |
| 5:06.5 | 3 | 22 | About 2.5 kilometers | about 2.6 km at 1 : 10¹⁰ (VO "about two and a half") |
| 6:22.1 | 5 | 28 | timeline: 2016 | Anglada-Escudé et al. 2016 |
| 6:31.1 | 5 | 28 | Every 11 days | Proxima b orbits every 11.2 days |
| 7:14.9 | 5 | 31 | About 20 years | Starshot: about 20 years |
| 7:29.3 | 5 | 32 | timeline: 2016 · 2031 | message sent Oct 2026 arrives about Jan 2031 |
| 7:35.7 | 5 | 32 | timeline: 2016 · 2031 · 2035 | earliest reply about Apr 2035 |

Chapter 1 (`lightyear`, 1:52–2:02) and chapter 4 (`lightrace`, 6:02–6:18) already carry numeral labels and are unchanged.

## For Chief

1. **Five labels run across one cut** ("About 13 kilometers", "1977", "Every 11 days", "About 20 years", and the 2016 and 2035 timeline steps). Their own shot ends within a second of the spoken word, so a label held to the cut would be up for under a second. Each next shot was checked to leave the same space clear.
2. **No WHO card for Friedrich Bessel** (named at 3:05, row 14). His years aren't in `SOURCES.md`, and *Teach on screen* needs them sourced and through the Gemini claims pass first. Suggest a `facts` row (Bessel's birth and death years) and then a one-card overlay.
3. **"About 2.5 kilometers"** follows the VO's "about two and a half"; the source works out at about 2.6 km.
4. **The timeline** counts as chapter 5's one DATA moment (three dates). Its three steps are 67 s apart, so each shows as its own 3–3.5 s pass rather than one strip held on screen.
