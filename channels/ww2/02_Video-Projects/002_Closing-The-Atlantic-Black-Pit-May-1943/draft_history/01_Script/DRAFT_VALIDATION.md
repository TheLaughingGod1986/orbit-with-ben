# Draft Validation Report (`DRAFT_VALIDATION.md`) — `WW2:002`

- **Film:** `WW2:002` — *How the Allies Closed the U-Boats' Safest Hunting Ground*
- **Directory:** `channels/ww2/02_Video-Projects/002_Closing-The-Atlantic-Black-Pit-May-1943/`
- **Document Status:** **DRAFT ONLY (`v01`) — NOT APPROVED, NOT VO-LOCKED.** No ElevenLabs voice synthesis has been run (`£0.00` spent), no YouTube channel exists, and no shared queue or status files have been modified.

---

## 1. Reproducible Spoken Word & Character Measurement (`01_Script/SCRIPT_v01.md`)

### A. Extraction Rule
In `01_Script/SCRIPT_v01.md`, stable paragraph IDs (`[P01]` through `[P60]`), chapter titles, and approximate timecodes sit on markdown heading/blockquote lines outside the spoken text. Every spoken narration paragraph is a single plain-text line immediately following its `### [PXX]` header.

The exact measurement can be reproduced at any time from the repository root with:

```bash
python3 -c '
import pathlib, re
p = pathlib.Path("channels/ww2/02_Video-Projects/002_Closing-The-Atlantic-Black-Pit-May-1943/01_Script/SCRIPT_v01.md")
paras = [s for line in p.read_text(encoding="utf-8").splitlines() if (s := line.strip()) and not s.startswith(("#", ">", "-"))]
joined_space = " ".join(paras)
print("Paragraphs:", len(paras))
print("Spoken words:", len(joined_space.split()))
print("Spoken chars (space-joined):", len(joined_space))
print("Spoken chars (no inter-para separator):", sum(len(x) for x in paras))
'
```

### B. Measured Totals Against Job Targets

| Metric | Measured Value (`SCRIPT_v01.md`) | Target / Guardrail | Result |
|---|---:|---|---|
| **Spoken paragraph IDs** | **`60`** (`P01`–`P60`) | Stable IDs outside spoken text | **PASS** |
| **Spoken words** | **`3,351` words** | `~3,300` spoken words | **PASS** |
| **Spoken characters (space-joined across paragraphs)** | **`19,934` chars** | Target `19,500–20,000` chars (`<= 21,000` hard cap) | **PASS (`1,066` chars pickup margin below `21,000`)** |
| **Spoken characters (sum of paragraph lengths, no separator)** | **`19,875` chars** | Target `19,500–20,000` chars (`<= 21,000` hard cap) | **PASS (`1,125` chars pickup margin below `21,000`)** |
| **Approximate runtime (estimated at ~134 wpm / ~800 chars/min)** | **`~25:00` (`1,500 s`)** | `~25 minutes` (**approximate runtime only, not an actual recorded narration duration**) | **PASS** |
| **First 30 seconds (`P01`, `00:00–00:25`)** | **`55` words / `328` chars** | Problem and stakes inside first 30 seconds; no channel intro, no `"in this video"`, no expert persona | **PASS** |
| **Unverified `"600-mile"` figure** | **`0` occurrences** | Must not appear in title, thumbnail, or script | **PASS** |

---

## 2. Cross-File Coverage Verification (`SCRIPT_v01.md` ↔ `SOURCES.md` ↔ `SHOT_LIST_v01.csv` ↔ `ARCHIVE_PROVENANCE.md`)

| Check | Coverage | Verification Detail |
|---|---|---|
| **Script IDs covered in `01_Script/SOURCES.md`** | **`60 / 60` (`100%`)** | Every paragraph `P01` through `P60` is mapped to a unique Claim ID (`C01a`/`C01b` through `C60a`, `61` claim rows total), each with a direct URL on `ibiblio.org/hyperwar` or `history.navy.mil`, a precise chapter/table/page locator, and a short exact supporting quotation read at that URL. |
| **Script IDs covered in `03_Picture/SHOT_LIST_v01.csv`** | **`60 / 60` (`100%`)** | `60` CSV rows (`P01`–`P60`), `0` word mismatches (`spoken_words` column matches `SCRIPT_v01.md` paragraphs byte-for-byte), proposed durations summing to `1,500 seconds` (`25:00` approximate runtime). |
| **Visual breakdown in `03_Picture/SHOT_LIST_v01.csv`** | **`20` Archive Photos + `40` Code Maps/Diagrams** | `20` rows use unique, inspected, cleared US federal public-domain photographs (`NARA RG 80-G` & `RG 26-G` on `history.navy.mil`, zero casualties); `40` rows use specifically designed Python/ffmpeg code-drawn maps, charts, and technical diagrams (`MAP_01`–`MAP_15`, `CHART_01`–`CHART_10`, `DIAG_01`–`DIAG_15`) with explicit factual inputs and Claim IDs. |
| **Selected archive photos logged in `03_Picture/ARCHIVE_PROVENANCE.md`** | **`20 / 20` (`100%`) + `4` Held** | All `20` active `NARA 80-G` / `26-G` photographs have full provenance entries (`CLEARED`), and `4` candidate UK/Allied items (`IWM CH 18035`, `IWM FL 2164`, `NARA 80-G-63997`, `IWM A 20147`) are explicitly flagged `UNCERTAIN — NOT CLEARED (HELD)` and excluded from active shot-list use. |

---

## 3. Known Limitations & Open Notes for Review

1. **Approximate Runtime Only (Not VO-Locked):** All timecodes in `SCRIPT_v01.md` and `duration_sec` values in `SHOT_LIST_v01.csv` (`1,500 seconds` / `25:00`) are **approximate pre-narration estimates** based on `~134 words per minute` (`~800 characters per minute`), not actual audio durations from a recorded voice-over stem.
2. **Online Official Histories vs Unread Physical Archival Files:** Because offline physical files at The National Archives (`TNA ADM 199/2020`, `AIR 41/47`, `ADM 234/578`) cannot be inspected first-hand from this workspace, `SOURCES.md` relies exclusively on published UK official histories (`Roskill Vol. I & II`, `Richards & Saunders RAF Vol. II & III`) and declassified US Navy operational evaluations (`OEG Report No. 51`, `NHHC H-Gram 019-4`, `DANFS Bogue`) read directly online.
3. **Postwar Hull-Number Cross-Reassessments on Convoy `ONS 5` (5–6 May 1943):** As documented in `01_Script/RESEARCH_NOTES.md` (§1.E), `SCRIPT_v01.md` (`[P46]`–`[P49]`) follows Captain S. W. Roskill's 1956 official British naval history (`UK-RN-II-14.html`) in pairing the five confirmed surface-escort kills on 5–6 May 1943 with specific U-boat hull numbers (`Pink` → `U-192`, `Loosestrife` → `U-638`, `Vidette` Hedgehog → `U-125`, `Oribi` ramming → `U-531`, `Pelican` → `U-438`). Later postwar wreck cross-assessments swapped several hull numbers among those same five surface-escort attacks; both attributions involve the same five ships and the same total of five U-boats sunk by the surface escorts on 5–6 May (plus `U-630` sunk by RCAF No. 5 Squadron Canso on 4 May and `U-710` sunk early on by an RAF Flying Fortress, for `7` U-boats in total).
4. **UK IWM Web-Portal Licensing vs US Federal Public Domain:** Although UK statutory 50-year Crown copyright on wartime Air Ministry (`CH`) and Admiralty (`A` / `FL`) official photographs expired decades ago, `iwm.org.uk` applies its Non-Commercial Licence to web downloads. Therefore, all active photograph rows in `SHOT_LIST_v01.csv` use verified US federal public-domain (`NARA 80-G` / `26-G`) photographs from `history.navy.mil`, while UK-specific airbase/convoy visuals are assigned to code-drawn maps and diagrams (`chart` lane).
