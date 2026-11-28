# J3835 — required R11 and attribution corrections

2026-11-27 · macbook · worker correction, awaiting independent J3818 review.

PIA00233 is rejected as a 3-D reconstruction, not an optional swap. SHOT_LIST_v02 and the executable cut/pool/provenance records now select real Magellan overhead SAR PIA00215. One shelf JPEG was copied to the film’s own studio-live folder; source and destination SHA-256 match. The official current NASA JPEG has different container bytes but identical decoded RGB pixels. EVIDENCE.json records both hashes, resolution, crop, source URL, rights, and preserved R11 timing. Source and output-size crop were visually inspected. No new rendered film or motion/audio review is claimed.

PIA18033 credits are corrected to NASA/NOAA Suomi NPP Blue Marble 2012 in the build manifest, builder comments, panel packaging record, pool/provenance, and proposed T045 note. The four existing thumbnail/sheet hashes and locked VO hash were recomputed on NAS and match. Locked narration/script, historical v01 shot-list files and all cut times remain unchanged. Only T045 changes in the ledger; its three populated arms remain proposed, video null. SHA256SUMS.txt identifies the exact corrected records.

This branch carries the five prerequisite files from #1358 and the corrected review from #1359, resolving the T045 placeholder/populated conflict by keeping the populated row. Review these overlapping PRs together; this worker neither merges nor closes any PR. J3818’s former unconditional KEEP is withdrawn under J3829; the original Gemini measurements remain historical evidence. An independent reviewer must issue a fresh KEEP/FIX after checking these corrections and merge state. J3022/J3023 were not released.

Assembly still must apply SHOT_LIST_v02’s opening/R09 repairs to executable inputs and render the split graphics/progress strip. The legacy v01 generator is explicitly marked historical; only its R11 and Earth attribution were corrected in this job. No legacy generator was run. Historical CSV/Markdown files are retained, not current assembly instructions.

Checks: all existing cut objects/times are identical except R11 still source/framing/scale; JSON parses; Python files parse; thumbnail builder diff versus #1358 contains only comments/docstrings; ledger changes only T045; git diff --check. No generation, spend, upload, scheduling or test arming. Ben watch Fri 11 Dec 2026 18:00 London and planned air Wed 16 Dec 18:00 London remain intact.
