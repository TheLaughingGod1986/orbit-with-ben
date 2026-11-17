# Field Order History (WW2 Channel): channel rules

These are this channel's own rules (`J2989`, 17 Nov 2026). The studio's rules (`AGENTS.md`) always apply in full (no spending without Ben, nothing deleted, Ben watches every finished film before it airs, the Never list). A rule here adds to them and never removes or loosens one. *(Public name and handle update to Ben's pick from the three verified options in `00_Brand/LAUNCH_PLAN.md` before registration.)*

## Who it is for

- Viewers on YouTube Browse and Suggested who want calm, deeply researched **25–45 minute** World War II and military history documentaries focused on **how campaigns, machines, logistics, and intelligence operations actually worked** — told through authentic US/UK wartime photography, our own code-drawn tactical maps, and Ben's British narration.
- **Growth engine (17 Nov 2026 research):** Big archive channels hold broad search queries (`world war 2` 564,442/mo; `ww2 documentary` 261,896/mo), while fast-growing 2026 entrants (`WW2 Dossier`, 14,300 subscribers on 39–56 min archive films, no Shorts) grow on **Browse and Suggested**. Packaging and retention carry the channel; 30–45 minute runtimes reach the 1 Feb 2027 **8,000 watch-hour** YPP threshold in ~35,000–40,000 views.

## YouTube monetisation & authenticity rules (enforced from Film 001)

Built directly for YouTube's **inauthentic-content / repetitious-content policy** (July 2025 and July 2026 guidance) and advertiser-friendly guidelines:

1. **Original researched script per film:** Every film is written from primary historical records and authoritative histories, with a `Sources:` line in the description (4–6 primary documents, official histories, or technical manuals backing the spoken numbers) and a quote-checked `01_Script/SOURCES.md`.
2. **Continuous narration — never stills over music:** Ben narrates throughout the entire runtime (chapter breaths `0.6–0.8 s`, final hold `2–3 s` only). No un-narrated photo montages or ambient padding.
3. **Sentence-matched picture (`4–7 s` cuts):** Every archive photograph and code-drawn map depicts the exact vessel, aircraft, commander, place, or figure named in that sentence.
4. **Ad-friendly throughout:** Focus on engineering, logistics, navigation, intelligence, strategy, and operational problem-solving. Zero shock framing, zero graphic violence, zero human remains, and zero extremist symbols on thumbnails or prominent cards.
5. **No deceptive AI history:** Never generate realistic AI photos or video of real historical people, soldiers, or combat events presented as real footage. If an atmospheric non-person Flow Veo background plate is ever used (e.g., empty North Atlantic swell or dawn cloud deck), mark it on screen (`AI illustration` bottom-left corner label), declare it in the description, and keep YouTube's altered/synthetic-content flag accurate. Ben's cloned voice (`Ben Orbit Narrator`) requires no synthetic disclosure.
6. **Honest persona & zero cross-channel reuse:** Narrate as Ben in plain British English — never claim a veteran or academic persona. Reuse zero scripts, VO stems, music beds, or renders from Orbit With Ben or History of Science.

## Titles and thumbnails

- **One fixed title style (`<= 70` characters):**
  - Shape: `How [Concrete System, Vessel, or Operation] [Solved / Closed / Rammed / Kept] [Specific Operational Stakes]` or `Why [Concrete System or Operation] [Specific Operational Cost or Failure]`.
  - Plain Title Case sentence, `55–70` characters, naming the specific hardware/operation plus one physical constraint, time span, or cost.
  - **No colons, no em-dashes, no pipes, no series suffixes, and no clickbait templates** (never copy `"What German Generals Admitted..."` or `"[Maker] Built a [N]-Cylinder Beast — ..."`).
- **One fixed thumbnail style:**
  - **Base:** One genuine, high-resolution US federal public-domain or UK Crown-copyright-expired wartime photograph showing the machine, vessel, or engineering structure clearly at `168×94 px`, graded for crisp silver-gelatin contrast (mean saturation or tonal separation checked with `thumb_preview.py`, near-black `<= 30%`) with warm amber/red operational callout tinting only where an arrow or range circle points to the focal mechanism.
  - **Text:** **2–4 uppercase words** in a clean top band or clear sky/sea quadrant (never covering the subject or the bottom-right duration badge), bold condensed sans-serif, **1–2 key words/numbers in `#FFD600` signal yellow**, remainder in `#FFFFFF` white, heavy black stroke + subtle drop shadow. Cover text never repeats the title verbatim.
  - **Never on a thumbnail:** AI-generated soldiers/battles, swastikas or graphic casualties, cluttered collages of more than two elements, or unreadable microfilm text.

## Voice and script

- **Voice:** ElevenLabs `eleven_v3`, `Ben Orbit Narrator`, API only via `04_Audio/tools/vo_take.py` + `scribe_v2` verification (one shared studio account).
- **Pilot voice budget guard (17 Nov 2026):** While Ben's current shared ElevenLabs cycle holds ~79,000 remaining characters (shared with OWB and HOS; ~800 spoken characters per finished minute), pilot films `001`–`003` target **~25 minutes each (~20,000 spoken characters; 21,000 budgeted with pickups)**, and **at most two pilot films (`001` and `002`, ~40,000–42,000 chars total) may be voiced before Ben upgrades or the monthly plan renews**. Never top up, upgrade, or change the plan. Once upgraded/renewed, standard films run **30–45 minutes** (~24,000–36,000 characters).
- **Opening (`0:00–0:30`):** Proof-first cold open on the single most striking verified archive image or tactical map of the crisis by `0:00`; Sentence 1 states the operational stakes before `0:08`; concrete date, place, and number by `0:20`; zero meta-promises (*"In this documentary we will explore..."*), zero logo/channel bumper, and zero chapter card before `0:45`.
- **Teaching markers:** Every script carries `[VISUAL MUST: ...]` markers (`DATA` >= 5 for 25–45 min films with `SCALE` analogies, `WHO` cards with birth–death years and rank/role at first mention, `WHEN` callouts and campaign timelines, `FACT` cards).

## Picture

- **1. Verified US & UK government archive photography (`65–75%` of runtime):** Every single image is checked individually for rights and recorded in `03_Picture/ARCHIVE_PROVENANCE.md` with catalog ID, URL, photographer/agency, creation year, and licence basis before assembly:
  - **US Federal Public Domain (`17 U.S.C. § 105`):** NARA (`RG 111-SC` Signal Corps, `RG 80-G` US Navy, `RG 342-FH` USAAF, `RG 127-GW` USMC, `RG 208` OWI), Library of Congress (`FSA/OWI` federal photographers), Naval History and Heritage Command (`NHHC`). Reject Associated Press / Acme / Life / commercial wire photos filed inside NARA boxes unless independently public domain.
  - **UK Crown Copyright Expired (`CDPA 1988` — 50 years from creation/publication; all pre-1976 Crown war photography expired):** Imperial War Museums official war collections (`BU`, `B`, `E`, `H`, `NA`, `EA`, `SE` War Office; `A` Admiralty; `CH`, `CL`, `CE`, `C`, `TR` Air Ministry; `D` Ministry of Information) and The National Archives (`ADM`, `AIR`, `WO`, `CAB`, `HW` under Open Government Licence). Confirm `"Crown copyright expired"` + official photographer on each IWM catalog page; reject private donations or trustee-held copyrights.
- **2. Code-drawn tactical & logistics maps (`25–35%` of runtime, `--kind chart`, `£0`):** Built in Python/ffmpeg (`gpt-6-astra` / Cursor / Gemini): Natural Earth / USGS public-domain coastlines, animated convoy routes, air-cover range rings, cross-sections, production/tonnage counters, and order-of-battle cards. Never two static charts back to back without archive photography between them.
- **3. Flow Veo (`0–5%` optional atmospheric plates only, `picture_route: "flow_only"`, `£0` billed):** Only for non-deceptive environmental transitions (e.g. empty ocean swell, rain on steel plating, cloud deck) when needed, always carrying `AI illustration` corner credit and disclosure. Zero Vertex billed fallback until Chief/Ben explicitly changes `picture_route`.

## Shorts

- **Zero Shorts (`shorts.planned_per_long: 0`).** 31 of 36 fast-growing long-form channels in the 17 Nov 2026 cohort posted no Shorts, and `WW2 Dossier` grew to 14,300 subscribers on long-form films alone. Audience browsing 30–45 minute military documentaries must not be diluted by a Shorts-only subscriber pool.

## Cadence

- **Target cadence (pending Ben's lock):** **2 long films a week** (proposed **Tuesday 18:00** and **Saturday 18:00 London**, normal publish, no Premiere — clear of Orbit Sun/Wed 18:00 and HOS Thu 18:00).

## Never (this channel's additions)

- Use an unverified "rare WW2 photo" from Pinterest, Reddit, blogs, or an undated Wikimedia upload without tracing its original US federal (`NARA`/`NHHC`/`LoC`) or UK Crown-expired (`IWM`/`TNA`) catalog record.
- Use AP, Reuters, Pathé, Getty, Ullstein, Bundesarchiv CC-BY-SA (unless Chief explicitly scopes attribution compliance), or IWM private-trustee photographs where rights are restricted.
- Generate AI images or video of soldiers, commanders, prisoners, aircraft combat, or historical events pretending to be archival photography.
- Show graphic casualties, human remains, war-crime shock imagery, or extremist insignia on thumbnails.
- Voice a third film on this channel in the current ElevenLabs billing cycle before Ben upgrades or the monthly plan renews.
- Upload Shorts to this channel.
- Copy the title formulas or scripts of `WW2 Dossier`, `WW2 Combat Files`, `Military Studio`, or any other channel.
