2026-11-12 — Claude (J2456). Panel: Codex (codex.md) and Gemini (gemini.md). Cursor's critique is not in (out of credit until 9 Dec). Two critics agree on every point below. The Chief's decision.

# Decision: CHANGE all three draft Bs before any test

All three drafts pass the numbers (grade, near-black, phone-size type). All three fail on what the picture says. None goes into Studio as drawn. Each is rebuilt once (one `thumb` job for Codex), checked with `thumb_preview.py long <thumb> --score`, and only then goes in as Test & Compare B against the live thumbnail, where no test is already set.

## 2fsQcea-voM, Moon (OWB 013)

- **Fact check (done, not taken on trust):** total solar eclipses end when the Moon's apparent size falls below the Sun's. Annular and lunar eclipses go on. "NO MORE ECLIPSES" is false. Both critics and the film's own script ("totals give way to annular eclipses") say so.
- **New hook:** `TOTALITY ENDS` (yellow `ENDS`). Fallback if the builder wants three words: `NO TOTAL ECLIPSES`.
- **New picture:** a grey, recognisable Moon (not the orange one, which reads as the Sun or a hot planet at 168 px). Earth larger than the Moon, with one outward arrow from Earth to Moon. Whole Moon clear of the text.
- **Live title:** left alone (see "Titles" below).

## Yk1tLh23rko, Neutron star (OWB 007)

- **Problem:** a tiny Earth beside a star drawn about 4 times wider than it says the opposite of "20 KM WIDE". Both critics say remove the Earth.
- **New hook:** `CRUSHED TO ATOMS` (yellow `ATOMS`). The script says space would "tear you into a line of atoms", so the claim is the film's own. It keeps the bodily stakes the title promises and differs from the live `CRUSHED FLAT`, so the test is a real comparison.
- **New picture:** the clean star plate from t=465 s already used in the draft, no Earth, nothing over the star. Top band only.
- **Not chosen:** the city-skyline scale bar (Codex's idea). It needs a sourced skyline we do not have. It can be a later round.

## b8-X_FyJnHM, Alien worlds (OWB 003)

- **Problem:** the glass-rain streaks vanish at 168×94, so it reads as a pretty blue planet. "MOLTEN" is not supported by the cited NASA release (Codex).
- **New hook:** `GLASS RAIN?` (yellow `GLASS`). It names the phenomenon.
- **New picture:** the named world (HD 189733 b) with a few thick, clearly visible diagonal streaks against a darker blue band. Streaks must show at 168×94 on the phone sheet. No Earth beside it unless it is drawn to the right scale.

## Titles

No title change goes in alongside these tests. Studio deletes a whole set title test when one side is edited, and the title-first rule (RULES.md, 10 Nov) says the title is set before a test is armed. The panel's title rewrites (Moon: "Why Is the Moon Moving Away? (3.8 cm a Year)"; Neutron star: "Neutron Stars: What Happens to Your Body Nearby?"; Alien worlds: "Exoplanets: Why Are These Worlds So Strange?") are recorded here as advice for the weekly audit to weigh against rule 26. They are not queued.

## Script openings and descriptions

Both critics say the Moon and Neutron-star openings break the first-30-seconds rule. Those films are live, so nothing is re-cut. The advice stays in codex.md and gemini.md for the next long. The Moon description is empty in the snapshot; a description first line is a listing fix and can go on a live video (AGENTS.md first-day rules). That is a separate Studio job once the Mini has a fresh read.

## What is queued

1. One `thumb` job for Codex: rebuild the three Bs as above, run `thumb_preview.py long … --score` and the phone sheet, park for Chief with the files. No spend.
2. After the Chief passes the rebuilds: one Studio job, only for a video with no test set, on a fresh Studio read, with `thumb_ledger.py start` for each. Written when the rebuilds pass, not before.
