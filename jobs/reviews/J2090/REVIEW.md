# J2090: 032 source identity ruling (PR491 / J2089)

4 Nov 2026 · Claude (review lane; Mini heartbeat had Claude as Chief at 18:51Z) · £0

Codex's audit is right: nine pinned NASA IDs in SHOT_LIST_v02 show the wrong subject. Each replacement below was checked against the live NASA Images API record (title and description) at 20:05Z. The rule stays the same: a plate shows what its caption and VO say, and it's credited as NASA/JPL-Caltech/SSI (or /ASI for radar).

| Row(s) | Was | Use instead | Live record | Note |
|---|---|---|---|---|
| R3 | PIA14909 | **PIA14602** | "Hazy Orange Orb", natural colour | orange haze, slow push |
| R4 | PIA08399 (labelled map) | **PIA08167** | "Shifting Northern Hazes" | upper-haze limb |
| R11 | PIA08399 | **PIA21902** | "Twilight Haze", individual haze layers | detached layers at the limb |
| R6 | PIA20016 (infrared) | **PIA14922** | "Colorful Colossuses…", natural colour Titan + Saturn | Titan beside ringed Saturn |
| R9 | PIA20021 (Ligeia feature) | **PIA08733** | "Titan Crescent View" | use 1 of 2 |
| R23 | PIA20021 | **PIA08733** | same | use 2 of 2, reframed |
| R13 | PIA01536 (Triton!) | **PIA02238** | "Titan Thick Haze Layer" (Voyager) | **inset only** (framed card "VOYAGER 1 · 1980" over a graded Cassini plate), never full-frame: its 2.41× upscale was rejected for the Short |
| R14 | PIA17172 (Saturn panorama) | **PIA21450** | "Cloud Bands Streak Across Titan" | |
| R28 | PIA17172 | **PIA21610** | "Titan Northern Summer Clouds" | tight reframe |
| R33 | PIA17655 (labelled polar map) | **PIA17031** | "Vast Ligeia Mare in False Color" | on-screen tag "FALSE COLOUR" |
| R34 | PIA17655 | **PIA21434** | "Titan: Kraken and Ligeia In Sharper Focus" | strait framing |
| R35 | PIA20016 | keep **PIA20016** | "Peering Through Titan Haze", infrared | on-screen tag "INFRARED VIEW" (disclosure) |
| R38 | PIA21445 (Earth through the rings) | **PIA19051** | "Perspective on Kraken Mare Shores" (SAR) | tag "RADAR" |
| R40 | PIA21445 | **PIA14584** | "Titan Kraken Mare" | reframed |
| R44 | PIA14909 | **PIA17163** | "Titan Crescents" | |
| R50 | PIA11831 (Hotei) | **PIA16638** | "Titan Craters, the Old and the New" (Sinlap radar) | **no "Selk" label on this plate.** Name Selk only on the CODE map pin "SELK CRATER · DRAGONFLY TARGET", with the APL Dragonfly animation as the second beat. The VO never says the plate is Selk. |

Excluded (already used in the uploaded S6 Short): PIA14925, PIA06230, PIA09739, PIA21625. None of these replacements overlaps them.

Each still still appears at most twice. PIA08733 and PIA20016 are the only two-use plates above.

**Low-res plates** (PIA07231/07232/07233/07236, PIA09182, PIA10008): no blanket OK. Use one of three: an inset card no larger than its native size × 2, a Ken Burns move on a crop at ≥ 50% of the native pixels, or a swap to a listed lead. Record the exact crop in the manifest.

**13 overlay stills:** approved to render as specified, and text-checked against the manifest/SOURCES rows. Codex re-checks them on the Mini against AGENTS packaging rules: safe area, ≥ 4.5:1 contrast on the graded plate, and no text over a subject's face or key feature. The frame check then moves to the picture review and Ben's final watch (Ben, 4 Nov: his final watch is the watch-and-listen check). They are not held for a separate Chief frame pass.

**Licences:** NASA/JPL imagery is generally not copyrighted. Keep the per-asset check in the pool (credit line and any third-party/ESA/ASI note) and finish it during the harvest.

Next: J2089 resumes at 2/4 with these mappings. Codex updates SHOT_LIST to v03 with the table above, then does the moving-footage harvest, the DATA/mechanism graphics, the R26/R46 £0 fallbacks and the overlay renders.
