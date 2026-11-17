# WW2 Documentary Channel — Default Upload Template (`J2999`)

> Governed by `studio/RULES.md` and `00_Brand/PLAYBOOK.md` (written fresh on 17 Nov 2026 — do **not** apply Orbit With Ben or History of Science upload rules here).

---

## 1. Studio Upload Defaults (Set Once in YouTube Studio → *Settings → Upload defaults*)

| Setting | Default Value | Why |
|---|---|---|
| **Title** | *(Leave blank in global defaults — written & scored per film before scripting)* | `45–70` chars (`≤ 50` chars preferred when natural), plain Title Case `How`/`Why` sentence, zero colons (`:`), zero em-dashes (`—`), zero pipes (`|`), never series suffixes or `"Full Documentary"`. |
| **Description** | Paste `templates/default_upload_description.txt` skeleton | Keeps `Chapters`, `Series playlist`, `Sources:`, and `Archive photography & maps:` ready on every upload. |
| **Visibility** | **Private** | Studio uploads Private first, verifies checks and arms Thumbnail Test & Compare, then schedules for `Tue 17:00` or `Sat 17:00` London (`12:00` New York). Never Premiere. |
| **Category** | **Education** (`categoryId: 27`) | Matches archival history documentaries (`Imperial War Museums`, `The Operations Room`, `Real Engineering`) and carries strong long-form RPM. |
| **Video language** | **English (United Kingdom)** (`en-GB`) | Matches Ben's British narration and UK spelling. |
| **Title & description language** | **English (United Kingdom)** (`en-GB`) | Keeps metadata consistent across YouTube search and captions. |
| **Audience (Channel-level)** | **No, set this channel as not 'Made for Kids'** | Set permanently under *Settings → Channel → Advanced settings*. |
| **Automatic chapters** | **Unchecked** (*Off*) | Every WW2 film supplies exact manual `00:00` story-beat chapters (`studio/RULES.md` rule 3); unchecking prevents YouTube overriding them. |
| **Automatic places & concepts** | **Checked** (*On*) | Helps YouTube index named wartime harbours, ships, and engineering concepts. |
| **Comments** | **On** (*Hold potentially inappropriate comments for review*) | Every upload gets a **pinned comment** with the primary sources list + one specific historical/engineering question for viewers (`PLAYBOOK.md` §4). |
| **Licence** | **Standard YouTube Licence** | Protects our original narration, script, and code-drawn maps. |

---

## 2. Per-Film Description Layout

Copy from `templates/default_upload_description.txt` and fill in exact order:

1. **Lines 1–2 (Above the Fold, `150–220` characters):**
   - State the concrete wartime engineering, logistics, or operational problem and what hung in the balance, weaving natural search terms (`World War 2`, the named hardware/operation, the theatre).
   - **Never** start with *"In this video…"*, never repeat the title verbatim, and never put hashtags at the top.
2. **Chapters (`00:00` mandatory on every film):**
   - Must start at `00:00`, with at least 3 timestamps ≥ 10 seconds apart.
   - Name chapters as **story beats and operational turning points** (`00:00 The Shingle Lesson at Dieppe`, `17:30 The Worst June Gale in 40 Years`), never textbook labels (`00:00 Introduction`, `21:30 Conclusion`).
3. **Series Playlist Link (`PLAYBOOK.md` §4):**
   - Link the film's home series playlist so viewers binge straight into a second 25–40 minute film:
     - *Engineering That Won the War*
     - *The Supply War*
     - *Deception & Intelligence*
4. **`Sources:` Block (`studio/RULES.md` rule 5):**
   - Cite 4–6 primary official histories, war diaries, technical surveys, and declassified archive files backing the film's spoken numbers and claims (Author/Agency, Year, Title / Record Group, and what it backs).
   - Never mention AI fact-checkers.
5. **`Archive photography & maps:` Block (`studio/RULES.md` rule 5):**
   - Credit the verified public-domain US federal (`NARA`, `NHHC`, `Library of Congress`, `US Coast Guard`, `USAAF`) and UK Crown-copyright-expired (`Imperial War Museums` official collections, `The National Archives`) series logged per image in `03_Picture/ARCHIVE_PROVENANCE.md`, and note that operational maps are drawn in code from campaign records.
   - Never use AP, Getty, Pathé, wire-agency, or private-donor images.
6. **Conditional `AI disclosure:` Line (Include ONLY when a rare photoreal AI plate is used):**
   - Omit completely when the film uses `0%` photoreal AI (the norm, e.g. Pilots `001` and `003`).
   - When a rare photoreal AI transition plate is used (e.g. an empty ocean-swell plate), add:
     `AI disclosure: MM:SS–MM:SS uses an AI-generated transition plate, labelled "AI illustration" on screen. No real historical people or events are AI-generated.`

### Worked Example — Pilot 1 (`WW2:001`)

```text
To supply two Allied armies across open Normandy beaches with a 24-foot Channel tide, British and American engineers built two Dover-sized harbours in secret across Britain and towed 1.5 million tons of steel and concrete to France for D-Day.

Chapters
00:00 The Lesson Written in Shingle at Dieppe
03:30 "The Piers Must Float Up and Down with the Tide"
08:00 Six-Storey Concrete Giants Hidden in the Thames
13:00 The Four-Knot Armada Across the Channel
17:30 When the Worst June Gale in 40 Years Hit Normandy
21:30 Fuel Under the Sea (PLUTO) and the Tonnage Verdict

Series playlist: Engineering That Won the War — [PLAYLIST_URL_ONCE_LIVE]

Sources:
• Ruppenthal, Roland G. (1953), Logistical Support of the Armies, Vol. I, US Army Center of Military History — daily Normandy beach vs Mulberry tonnage tables
• UK The National Archives CAB 106/999 & WO 219/2522 — SHAEF Chief Engineers' Report on Artificial Harbours (Mulberry A & B), 1944–1945
• Institution of Civil Engineers (1948), The Civil Engineer in War, Vol. 2: Docks and Harbours — Phoenix caisson and Whale flexible roadway engineering papers
• Morison, Samuel Eliot (1957), History of United States Naval Operations in World War II, Vol. XI — Mulberry A tow and 19–22 June storm logs
• Hartcup, Guy (1977), Code Name Mulberry: The Planning, Building & Operation of the Normandy Harbours

Archive photography & maps:
Original wartime photographs and film from UK Imperial War Museums (War Office BU, Admiralty A, and Ministry of Information D series, Crown copyright expired) and the US National Archives (RG 111-SC, RG 80-G, and US Coast Guard, public domain). Operational and tidal engineering diagrams drawn in code from 1944 campaign charts.
```

---

## 3. Tags Style (`10–15` Tags, `≤ 400` Characters Total)

YouTube uses tags mainly for spelling variants (`mulberry harbour` / `mulberry harbor`, `d-day` / `d day`) and initial topic classification on a brand-new channel:

1. **4–6 Specific Hardware / Operation Tags (first):**
   - `mulberry harbours`, `mulberry harbor d-day`, `arromanches artificial port`, `phoenix caissons`, `operation pluto`, `normandy logistics`
2. **3–4 Theatre / Problem Tags (second):**
   - `d-day engineering`, `operation overlord`, `allied supply lines`, `amphibious warfare`
3. **3–4 Core Channel Niche Tags (last, consistent across uploads):**
   - `ww2 documentary`, `world war 2 history`, `military history`, `war documentary`

**Never include:** other YouTube channel names, `#hashtags`, misleading battle names not covered in the film, or 500-character keyword stuffing.

---

## 4. When to Tick the "Altered Content" Box in YouTube Studio

YouTube Studio asks on every upload: *"Altered content — Do any of the following describe your content? Makes a real person appear to say or do something they didn't · Alters footage of a real event or place · Generates a realistic-looking scene that didn't actually occur."*

Follow this exact two-case rule (`studio/RULES.md` rule 5):

| What is in the finished cut | Tick **"Yes"** or **"No"**? | Required on-screen & description action |
|---|---|---|
| **Case A — Pure Archive + Code Maps (Default, e.g. Pilots `001` & `003`):** Authentic wartime archive stills and public-domain newsreels (cropped, pan-and-zoomed, dust-cleaned, tonally graded or colour-restored without altering events), non-photoreal code-drawn maps/charts, and Ben's authorised ElevenLabs voice clone narrating our own script. | **Tick `No`** | Standard `Sources:` and `Archive photography & maps:` blocks only. *(YouTube explicitly exempts colour grading, dust clean-up, clearly stylized motion graphics/maps, and a creator's own authorised synthetic narration when no real historical person is made to say something they didn't and no realistic event is fabricated.)* |
| **Case B — Contains Any Photoreal AI Plate (Rare exception, e.g. an empty ocean-swell transition clip):** Even **one** photorealistic AI-generated video clip or synthetic photoreal still appears anywhere in the film. | **Tick `Yes`** | 1. Burn subtle corner label **`AI illustration`** on that shot (`studio/RULES.md` rule 5).<br>2. Include the timestamped `AI disclosure:` line at the bottom of the description. |
| **Forbidden on This Channel (`studio/RULES.md` rule 5)** | **NEVER MAKE** | Never generate AI video or photoreal AI images depicting real historical people, combat, casualties, or real wartime events as if filmed on camera. |

> **Engineering note for automated API uploads (`07_Content-Ops`):** `07_Content-Ops/src/lib/youtube/upload.ts` currently hardcodes `containsSyntheticMedia: true` because Orbit With Ben and History of Science are AI-scene channels. When WW2 connects to the API uploader, read `containsSyntheticMedia` from the film's upload manifest (`false` for Case A, `true` for Case B) rather than forcing `true` on pure archive documentaries.

---

## 5. End Screen, Pinned Comment & Post-Upload Checklist

1. **Thumbnail Test & Compare (`PLAYBOOK.md` §3):** Upload Thumbnail A (bright-graded real archive photo + `1–3` white/signal-yellow words) and arm Test & Compare with Variant B once YouTube Advanced Features are active.
2. **Playlist:** Add immediately to one of the three core series playlists (*Engineering That Won the War*, *The Supply War*, *Deception & Intelligence*).
3. **End screen (final `20 s`):** `1 × Next video in series` (or *Best for viewer* on Film 1) + `1 × Subscribe`.
4. **Pinned comment (immediately upon publish):** Paste the film's `4–5` headline primary sources + **one concrete operational question** inviting viewer discussion (for Pilot 1: *"Could the Allies have supplied Normandy across open beaches with LSTs and DUKWs alone if Mulberry B had also broken up in the June gale — or did Arromanches make the breakout possible?"*).
