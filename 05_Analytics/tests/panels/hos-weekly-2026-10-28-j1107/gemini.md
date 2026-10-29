2026-10-28 — gemini (Packaging panel critic, J1124)

# HOS Weekly Audit Packaging Critique: Periodic Table v12 & Later Title Drafts

## 1. Title — **6 / 10**
- **Live title (held fixed for the thumbnail test):** `How Did We Discover the Periodic Table?` (39 chars)
  - Carries the primary neighbour phrase (`periodic table`, 55.6% Suggested share from TED-Ed's Mendeleev video) and fits under 60 characters, but uses the generic textbook formula `How Did We Discover X?` that `THUMBNAIL_AND_TITLE_RULES.md` §1.4 and §1.11 warn against ("Catalogue labels fail").
- **Proposed later title-B drafts (`DESIGN_HANDOFF.md`, one variable per test):**
  - **Periodic Table:** `Periodic Table: How Mendeleev Predicted Missing Metals` (54 chars) — keeps both neighbour phrases (`Periodic Table`, `Mendeleev`) and names the concrete prediction payoff, but opens with a flat encyclopedia colon label (`Periodic Table:`).
  - **X-rays:** `X-rays: The Accident That Revealed Our Bones` (44 chars) — strong (8/10); pairs the search noun (`X-rays`) with a familiar body noun (`Our Bones`) and the accidental-discovery shape.
  - **Atom:** `Atoms: Why Gold Foil Sent Particles Back` (40 chars) — keeps the neighbour noun and names Rutherford's anomaly, but leading with `Atoms:` is dry and "Sent Particles Back" states the lab mechanic without the shocking implication (that solid gold is mostly empty space).
- **One concrete rewrite (for the later Periodic Table title-only test):**
  `How Mendeleev's Periodic Table Predicted Missing Metals` (55 chars — drops the stiff colon prefix while keeping both neighbour keywords in the first four words and leading with an active discovery clause).

## 2. Thumbnail at phone size (168×94) — **6 / 10**
- **Candidate reviewed:** `hos_002_thumb_B_vacant_card_slot_v12.jpg` (`VACANT CARD SLOT`)
- **Visual execution (9/10):** At 168×94 (`existing_B_v12_phone.jpg`), the 3-word cream/gold serif stack in the upper-left is crisp, high-contrast, and completely off the glowing amber gap on the right. The Explorer is small lower-left, the bottom-right duration badge zone is clear, and the warm painted wooden grid fits the live HOS family (`existing_B_v12_family.jpg`) while replacing the ambiguous silver gallium arch on live A.
- **Hook-copy flaw (4/10):** `VACANT CARD SLOT` has almost no curiosity pull. It labels the literal wooden prop texture like a filing-cabinet or ATM error rather than naming the scientific mystery. It only exists because late build rounds (`v10`–`v12`) kept avoiding words already used on earlier approved renders.
- **One concrete rewrite (requiring zero new builds under J0777):**
  Instead of `v12` (`VACANT CARD SLOT`), arm existing Chief-approved **`hos_002_thumb_B_empty_on_purpose_v06.jpg` (`EMPTY ON PURPOSE`)** or **`hos_002_thumb_B_missing_element_v02.jpg` (`THE MISSING ELEMENT`)** from the same `08_Thumbnail/Selected/` folder on the identical glowing-slot plate.

## 3. Title + thumbnail together — **7 / 10**
- **Assessment:** Live A wastes half the package by painting the 7-word title verbatim (`HOW DID WE DISCOVER THE PERIODIC TABLE?`). Pairing the fixed live title `How Did We Discover the Periodic Table?` with the glowing-gap plate fixes the verbatim repeat: the title names the familiar subject and the picture shows the hole in the grid. However, `VACANT CARD SLOT` fails to bridge "Periodic Table" to a human dare or paradox; a casual viewer sees a wooden slot rather than a deliberate scientific prediction.
- **One concrete rewrite:**
  Pair the fixed live title `How Did We Discover the Periodic Table?` with existing approved **`EMPTY ON PURPOSE` (`v06`)** (or test 3-way thumbnail-only: Live A vs `EMPTY ON PURPOSE` v06 vs `PREDICTED BEFORE FOUND` v04) so the title supplies the search noun and the thumbnail supplies the paradox.

## 4. First 30 seconds / Short hook — **6 / 10**
- **Long opening (`periodic_table_script_master_v01.md`, live cut locked):** Opens with five rhetorical questions in the first four paragraphs (*"What if the stuff of your world came with a secret seating plan… Would you risk a century on a map with holes in it?… Could a wrong list of matter waste a generation…"*), leaning on the abstract "empty chairs / seating plan" metaphor before naming Mendeleev, 1869, or a single metal.
- **Short covers in weekly audit (`2026-10-28.md`):** Correctly preserves the 6 `J1113` scheduled covers and isolates the 16 unprotected legacy mismatches (film-frame subtitles, 5–7 word captions, and abstract hooks like `What other table has empty chairs?` at 0.0% CTR and `What happens if you keep cutting gold in half?` at 1,121 impressions / 0.9% CTR which omits the subject noun "atom").
- **One concrete rewrite:**
  Keep the live 002 long cut locked, but on future scripts replace multi-question throat-clearing with the dated physical proof in line one (*"In 1869, Dmitri Mendeleev left an empty box in his periodic table and wrote down the exact weight of a metal nobody had ever found"*); for the first legacy Short cover batch, prioritise `29bpGAI0wb8` (1,121 impressions, 0.9% CTR) with a 3-word cover hook that names the subject (`CUT GOLD TO ATOMS?`).

## 5. Description first line and chapters — **7 / 10**
- **Assessment:** The description opening (*"Why did Mendeleev leave gaps in the periodic table? Because he trusted his pattern more than the list of known elements. In 1869 he left spaces for metals nobody had found, and predicted what they'd weigh. Then gallium, scandium and germanium turned up and fitted."*) puts both neighbour phrases (`periodic table`, `Mendeleev`) in sentence one, but sentence four spoils the Act 5 payoff inside the search preview. Meanwhile, the five chapter titles (`0:00 A zoo of names`, `1:25 First patterns`, `2:49 A ruler for atoms`, `4:21 Empty chairs`, `6:31 The guests arrive`) are poetic metaphors with zero searchable nouns or names.
- **One concrete rewrite:**
  Trim the spoiler fourth sentence from the above-the-fold opening (*"Why did Mendeleev leave gaps in the periodic table? Because in 1869 he trusted his pattern enough to leave blank spaces for undiscovered metals—and wrote down their exact weight and melting point in advance."*) and rename the chapters for search without giving away the ending: `0:00 The Four-Element Trap` / `1:25 Triads and Newlands' Octaves` / `2:49 1860 Karlsruhe: Weighing Atoms` / `4:21 Mendeleev's 1869 Gaps` / `6:31 Testing the Predicted Metals`.

---

**Which would you click, and why?**
I would click the glowing-gap periodic table card grid over the live melting-gallium arch because the glowing hole visually explains *how* the table worked at a glance, whereas the live silver blob looks like an unidentifiable chrome hook and repeats the 7-word title verbatim.

**The single change that would most raise CTR:**
Without building any new images under J0777, swap candidate `v12` (`VACANT CARD SLOT`) for existing approved `hos_002_thumb_B_empty_on_purpose_v06.jpg` (`EMPTY ON PURPOSE`) or `hos_002_thumb_B_missing_element_v02.jpg` (`THE MISSING ELEMENT`) on the same glowing-slot plate so the 3-word hook states a scientific mystery instead of labelling a wooden filing slot.
