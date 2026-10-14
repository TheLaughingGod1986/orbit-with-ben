# 027 What If Earth Stopped Spinning? SHOT_LIST v02: the first answer before 0:30 (Claude, 9 Oct 2026)

**Why.** On most OWB longs, half or more of viewers have gone by 0:30 (tracker, 9 Oct). In v01 the opening lists what the film will cover (23.80–39.50 s), and the first answer, the sudden stop, only starts at 111.92 s. Codex's idea 5, adopted: give the first answer straight after the question.

**What changes.** This is a re-order of the **recorded VO** (`earth_spin_vo_v01`); no new voice is needed. Every row keeps its v01 picture, sources and rules unless noted. The rows are cut from the VO at their v01 spans and laid in the order below, with the usual 0.7 s gap at each chapter card.

| New order | v01 row(s) | VO span (s, from v01) | Note |
|---:|---|---|---|
| 1 | 1–2 | 0.16–16.02 | The hook as v01. Frame 0 lock unchanged. |
| 2 | 3 | 17.36–22.56 | "So what would happen if Earth stopped spinning? Not slowly. All at once." `speed` as v01. |
| — | 4 | 23.80–39.50 | **Cut.** The agenda line ("In this film I will show you…"). Its promise beat graphics go with it. |
| 3 | card | — | **[CHAPTER CARD: The Sudden Stop]**, moved up. |
| 4 | 10 | 111.92–120.28 | "Now imagine the impossible. Earth's rock stops turning in an instant. But the air does not…" **Picture change:** real ISS/NOAA footage of high cirrus streaming (from v01 row 11), not `air`, so two code graphics never run back to back in the first 30 s. |
| 5 | 11 | 121.06–132.84 | "At the equator the atmosphere would keep going east…" **Picture change:** `air` 0–14 s (the globe stops, the air keeps going). |
| 6 | 12–15 | 133.70–181.46 | As v01 (sea spray, Britain, Orbit at the North Pole, the energy in the spin). |
| 7 | card | — | **[CHAPTER CARD: The Speed You Cannot Feel]**, now second. |
| 8 | 5–9 | 40.38–111.08 | As v01 (cabin pour, orbital sunrise, star trails, `speed` → `bulge`, Foucault). The bulge still comes before chapter 3's "Remember that bulge at the equator?" |
| 9 | 16–17 | 182.42–192.02 | The subscribe beat, then "So a sudden stop is a thought experiment. What about a slow one?" These now close chapter 1, straight into chapter 3. |
| 10 | 18–37 | 192.84–460.34 | Unchanged from v01. |

**Result.** The first answer starts at about **24 s** (was 112 s), and the film runs about 15.7 s shorter (≈ 444 s + the end hold).

**First 30 seconds (AGENTS.md, 9 Oct):** real (EPIC/ISS) → real (jet, night city) → `speed` → **card** → real (cirrus) → `air`. That's one code graphic at a time, with real moving imagery between.

**Checks before picture:** the sentence sheet (J0086) on this order. `clip_check.py` with every cut still in a VO pause. Chapter cards land after the sentence ends.
