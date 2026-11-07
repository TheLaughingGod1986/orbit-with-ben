# Chief pickup — 7 Nov 2026 ~13:00 London

**This note will go stale.** It is a dated desk snapshot so a new Chief can continue without chat history. Live state always wins:

- `python3 scripts/studio.py board`
- `jobs/queue.json`, `jobs/WIP.json`
- each film's `status.json`
- thread PRs **OWB #99** / **HOS #180**
- working media under `/Volumes/data/studio-live/…/02_Video-Projects/`

Standing rules (not dated): `AGENTS.md` → **Film folders on the NAS**, **How films get worked on**, **Videos tab**, Never list. Master index: `HANDOVER.md`.

---

## WIP (dated; from `jobs/WIP.json` updated `2026-11-05T18:32Z`)

**Active (9):** HOS 008, 009, 010, 013 and OWB 030, 031, 032, 033, 034.

**Waiting lines:**
- `next` (OWB): J01, then 035–061
- `next_hos`: 011, 012, 014, 015, 018

**Current three-film focus moving (operational, inside the nine):** Titan (**032**), Magnetic Field (**031**), Uranus (**033**). After Titan long + its Shorts, next HOS focus is remaining Willow Shorts as **HOS:006** (not a bare `006`).

**Do not** start new Pluto (**034**) production beyond what is already queued. Money / OMNI / merging OWB **#626** waits for Ben.

---

## studio-live media (dated ~13:00 London 7 Nov 2026)

**First studio-live copy COMPLETE for only these nine:** OWB **030–034** and HOS **008, 009, 010, 013**. Do **not** invent any other folder as already complete on studio-live.

**Leftover working/upcoming copy → studio-live: INCOMPLETE** as of ~**12:53 London** and was resumed. Do **not** claim it finished.

**Technique (standing):** `nice -n 15 rsync -a --partial --update` (never `--delete`); exclude `.git` / `node_modules` / `__pycache__`; never kill studio processes; never delete Mini originals; never overwrite newer NAS files with older Mini copies; do not recopy shipped archive films. Full rules: `AGENTS.md` → **Film folders on the NAS**.

| Status (dated) | Films / notes |
|---|---|
| **Partial** | **OWB025** Mars (airs Sun **8 Nov 18:00 London**) — last rsync exit **1**; Mini ~**79272** KiB vs studio-live ~**47206** KiB |
| **Started / unverified** | **OWB026** — Mini ~**98284** vs studio-live ~**98933** (size alone is **not** completeness) |
| **Still pending** (when last reported) | OWB027; OWB028 (largest, ~**2.5 GiB**); OWB029; **HOS005** Harvey (remaining November Shorts); **HOS006** Trees (recent launch); **HOS007** Vaccine (upcoming launch); small future editorial **OWB035–061** (copying them does **not** authorise production); OWB **J01** Journey; **HOS000** Explorer Test and **HOS099** Compilation (tiny/uncertain); **HOS002** Periodic Table (ambiguous records — copy conservatively). Skip empty stub **HOS004 How-Did-We-Discover-The-Atom** if still **0 KiB** |
| **Skipped shipped** (do not recopy) | OWB001–024 except the leftover **025+** working set; **HOS001** Germs; **HOS003** X-Rays; **HOS004** Whats-Really-Inside-An-Atom |

**Existing-nine** were not overwritten during the leftover attempt. A few Mini-newer `status.json` files exist (**031**, **032**, **034**); HOS008 has some NAS-newer AppleDouble metadata. MacBook may have written newer harvest files (e.g. Magnetic Field **J2141**).

---

## Videos / calendar flags (dated)

- Dashboard Videos chips are the live **3×3 nine lanes** (Backlog → … → Post-live), including **QA**, **Live**, and **Post-live**. Computed chips — Chief does not drag by date (`AGENTS.md` → **Videos tab**).
- A Titan Short titled **"What Would Standing on Saturn's Moon Titan Feel Like?"** (**v11**) sits on **Tuesday 10 Nov 18:00** and was **not** uploaded; it is **not** a locked Orbit Short slot (those are Mon/Wed/Fri/Sat **11:30**). Flagged to Ben once; **do not move the date without him**.

---

## Outstanding elected-Chief reviews (as of ~12:57 London sweep)

Verify live before acting:

- **J2364** — 034 Pluto Shorts plan / Short 2 lift
- **J2350** — HOS desk PR **450** merge + watcher refresh

Do **not** silently merge money / OMNI work or conflicting **HOS #411**.
