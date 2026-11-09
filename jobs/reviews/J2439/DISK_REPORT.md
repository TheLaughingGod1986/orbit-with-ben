# J2439 — Mac mini Read-Only Disk Usage & `studio-live` Film Folder Report

- **Date:** 2026-11-09T12:48Z
- **Job:** `J2439` (`qa`, read-only)
- **Worker:** `gemini` (`gemini-4-argon-high`)
- **Mode:** Strictly read-only (nothing changed, moved, or deleted on the Mac mini or NAS).

---

## Summary Table (`path` | `size` | `on studio-live`)

### A. Film Folders Over 1 GB (plus `032` at `976M` / `1.02 GB` decimal and `hos-008-lightning` worktree)

| path | size | on studio-live (yes/partial/no) | local count / total bytes | studio-live count / total bytes | notes |
|---|---:|---|---|---|...|
| `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/028_A-Star-Is-Coming-Toward-Us` | `2.4G` | **yes** (all non-`.pyc` files; `status.json` differs) | `926` files / `2,583,139,162` B (`926` non-AppleDouble) | `1,930` raw files / `2,586,746,057` B (`918` non-AppleDouble / `2,582,600,905` B + `1,012` `._*`/`.DS_Store`) | Only 8 local `__pycache__/*.pyc` files are absent on NAS; `status.json` differs in size; all media and source files match. |
| `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin` | `2.0G` | **yes** | `752` raw files / `2,115,955,441` B (`749` non-AppleDouble / `2,115,943,153` B) | `1,608` raw files / `2,137,077,481` B (`753` non-AppleDouble / `2,133,575,401` B + `855` `._*`/`.DS_Store`) | `0` local files missing on NAS (`0` size diffs); NAS has all 749 local content files with identical byte sizes plus 4 extra files (`+17.6 MB`). |
| `/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin` *(separate worktree checkout)* | `1.5G` | **partial** | `528` raw files / `1,630,094,024` B (`525` non-AppleDouble / `1,630,081,736` B) | `1,608` raw files / `2,137,077,481` B (`753` non-AppleDouble / `2,133,575,401` B) | `506` local files in this worktree (`04_Generated-Clips/part01..05` raw/refs/uat and `07_Edit-Project/_precheck/rough_v08` & `rough_v12`) are not in `/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin`. |
| `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode` | `1.1G` | **yes** (all non-`.pyc` files; `status.json` differs) | `1,066` files / `1,192,036,264` B (`1,066` non-AppleDouble) | `2,190` raw files / `1,195,833,257` B (`1,057` non-AppleDouble / `1,191,192,489` B + `1,133` `._*`/`.DS_Store`) | Only 9 local `__pycache__/*.pyc` files are absent on NAS; `status.json` differs in size; all media and source files match. |
| `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan` | `976M` (`1.02 GB` decimal) | **yes** (NAS is a `2.9G` superset; 5 doc/sheet files differ) | `364` files / `1,023,004,223` B (`364` non-AppleDouble) | `1,717` raw files / `3,077,099,644` B (`838` non-AppleDouble / `3,073,499,260` B + `879` `._*`/`.DS_Store`) | `0` local files missing on NAS; NAS has 474 additional working files (`+2.05 GB`) and 5 files with different sizes (`production-status.md`, `status.json`, `03_Reference-Material/harvest_J2089_v01/contact_sheet.jpg`, `10_Shorts/README.md`, `10_Shorts/SHORTS_PLAN_v01.md`). |

### B. Sub-1 GB Film Folders (`100M` – `800M`) in OWB & HOS `02_Video-Projects`

| path | size | on studio-live (yes/partial/no) | local count / total bytes | studio-live count / total bytes | notes |
|---|---:|---|---|---|...|
| `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/027_What-If-Earth-Stopped-Spinning` | `797M` | **partial** | `1,314` files / `832,230,830` B | `2,693` raw (`1,305` non-AppleDouble / `832,029,796` B) | 3 local `cuts_v02_first_second_plan.json` files + 6 `.pyc` files missing on NAS; `10_Shorts/EARTH_SPIN_SHORTS_SCRIPTS_v01.md` differs in size. |
| `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/031_What-Happens-When-Earths-Magnetic-Field-Flips` | `717M` | **partial** (NAS has `6.8G` media, local has newer upload receipts/scripts) | `373` files / `750,961,546` B | `1,843` raw (`893` non-AppleDouble / `7,288,795,925` B) | 12 local upload-result JSONs and Short assembly scripts (`11_Upload-Package/PACKAGE_UPLOAD_RESULT*`, `10_Shorts/_assemble_031_short*`) + 5 `.pyc` files not yet on NAS; 5 tracked files differ in size; NAS has 537 extra media files (`6.8G`). |
| `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air` | `611M` | **yes** (all non-`.pyc` files) | `460` files / `639,313,134` B | `983` raw (`459` non-AppleDouble / `639,272,269` B) | Only 1 `.pyc` file (`_mint_flow_cdp_v01.cpython-314.pyc`) missing on NAS; `0` size diffs. |
| `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/034_Why-Plutos-Frozen-Heart-Has-Zero-Craters` | `545M` | **yes** (NAS is a `3.3G` superset; `status.json` differs) | `133` files / `571,486,681` B | `4,034` raw (`1,991` non-AppleDouble / `3,533,525,168` B) | Only 1 `.pyc` file missing on NAS; `status.json` differs; NAS has 1,859 extra working media files (`3.3G`). |
| `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/013_Darwin-Wallace-Evolution` | `503M` | **yes** | `92` files / `527,576,663` B | `201` raw (`92` non-AppleDouble / `527,576,663` B) | Exact match on all 92 content files and bytes (`527,576,663` B) plus 109 AppleDouble sidecars on NAS. |
| `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/030_Apophis-Closer-Than-Our-Satellites` | `497M` | **yes** (`status.json` differs by 21 B) | `317` files / `520,255,322` B | `681` raw (`317` non-AppleDouble / `520,255,343` B) | All 317 files present on NAS; only `status.json` differs by 21 B. |
| `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/_Buffer-Backlog` | `488M` | **no** | `735` files / `510,105,141` B | `0` files / `0` B | Folder does not exist on `studio-live`. |
| `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/004_Whats-Really-Inside-An-Atom` | `481M` | **no** | `1,052` files / `501,895,600` B | `0` files / `0` B | Shipped film (archived under `mac-mini-archive` with `MOVED_TO_NAS_2026-10-24.txt`; not on `studio-live`). |
| `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity` | `293M` | **yes** | `214` files / `307,045,727` B | `472` raw (`214` non-AppleDouble / `307,045,727` B) | Exact match on all 214 content files and bytes. |
| `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/024_What-Happens-If-You-Travel-Near-Light-Speed` | `282M` | **no** | `1,128` files / `292,715,663` B | `0` files / `0` B | Shipped film (archived under `mac-mini-archive` with `MOVED_TO_NAS_2026-11-05.txt`; not on `studio-live`). |
| `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/033_Why-This-Planet-Has-21-Year-Winters` | `244M` | **partial** | `97` files / `255,639,032` B | `670` raw (`349` non-AppleDouble / `1,632,960,114` B) | 15 local files (`harvest_J2290*`, `SOURCE_AUDIT_J2299_v01.json`, etc.) missing on NAS; 5 files differ in size; NAS has `1.6G` working media. |
| `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs` | `236M` | **yes** | `161` files / `247,198,664` B | `354` raw (`161` non-AppleDouble / `247,198,664` B) | Exact match on all 161 content files and bytes. |
| `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/003_Invisible-Bones-X-Rays` | `181M` | **no** | `572` files / `187,980,641` B | `0` files / `0` B | Shipped film (archived under `mac-mini-archive` with `MOVED_TO_NAS_2026-10-10.txt`; not on `studio-live`). |
| `/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/023_What-Happened-To-Venus` | `128M` | **no** | `1,420` files / `131,194,368` B | `0` files / `0` B | Shipped film (archived under `mac-mini-archive` with `MOVED_TO_NAS_2026-11-05.txt`; not on `studio-live`). |

---

## 1. Free Space (`df -h ~`)

```text
Filesystem      Size    Used   Avail Capacity iused ifree %iused  Mounted on
/dev/disk3s5   228Gi   196Gi   5.9Gi    98%    4.1M   62M    6%   /System/Volumes/Data
```

---

## 2. Top 40 Directories by Size

Command run:
```bash
du -sh ~/YouTube/* /private/tmp/* ~/_desk/* ~/Library/Caches ~/Library/Developer ~/.cache ~/.npm ~/Downloads 2>/dev/null | sort -h | tail -40
```
*(Note: `~/Library/Caches` is `132M`, just below the top-40 cutoff of `135M`, and `~/Library/Developer` does not exist.)*

### Top 10 Largest (Descending)

| Rank | Path | Size | On `studio-live` |
|---:|---|---:|---|
| 1 | `/Users/benjaminoats/YouTube/orbit-with-ben` | `16G` | **partial** (working films `028`, `029`, `030`, `032`, `034` on `studio-live`; `027`, `031`, `033` partial; shipped `023`, `024` on `mac-mini-archive`; repo also holds git `.git`, `07_Content-Ops/node_modules`, `04_Audio`, etc.) |
| 2 | `/Users/benjaminoats/_desk/worktrees` | `13G` | **no** (local git worktrees; e.g. 12 `J2141-*` worktrees at `~530M` each = `~6.4G`, plus `J2381`, `J2387`, `J2419`, `analytics`, `J2206`, `J2245`, `J2246`) |
| 3 | `/Users/benjaminoats/YouTube/History Of Science` | `8.9G` | **partial** (`006`, `008`, `009`, `010`, `013` on `studio-live`; `_Buffer-Backlog` `488M` and shipped `003`/`004` not on `studio-live`; repo also holds `.git`, `07_Content-Ops/node_modules`, `04_Audio`, etc.) |
| 4 | `/Users/benjaminoats/_desk/renders` | `4.6G` | **no** (local render outputs, incl. `J1100-v07` `2.0G`, `J2169` `346M`) |
| 5 | `/Users/benjaminoats/_desk/scratch` | `4.0G` | **no** (local worker scratch, incl. `chief` `2.8G`, `gemini-J2427` `543M`, `j2427-wt` `542M`) |
| 6 | `/Users/benjaminoats/_desk/cache` | `2.3G` | **no** (local desk/gate media cache) |
| 7 | `/Users/benjaminoats/YouTube/hos-008-lightning` | `1.5G` | **partial** (standalone HOS 008 git worktree; `506` files in `02_Video-Projects/008_Lightning-Franklin` are not in `studio-live`) |
| 8 | `/Users/benjaminoats/Downloads` | `1.2G` | **no** |
| 9 | `/Users/benjaminoats/_desk/state` | `891M` | **no** |
| 10 | `/private/tmp/gemini-J1100-wt` | `569M` | **no** (temp git worktree; 13 temp worktrees in `/private/tmp/*` total `~7.0G`) |

### Exact `sort -h | tail -40` Output

```text
135M	/Users/benjaminoats/_desk/J2141-hubble-v01
148M	/Users/benjaminoats/_desk/handoff
163M	/Users/benjaminoats/_desk/logs
169M	/private/tmp/j2229-frames
210M	/Users/benjaminoats/_desk/006
210M	/Users/benjaminoats/_desk/031
225M	/Users/benjaminoats/_desk/media
249M	/Users/benjaminoats/_desk/tmp-item9
256M	/Users/benjaminoats/_desk/_share_test
292M	/Users/benjaminoats/_desk/venv-graphics
300M	/Users/benjaminoats/YouTube/hos-009-gravity
319M	/Users/benjaminoats/_desk/jobs
322M	/Users/benjaminoats/_desk/venvs
353M	/Users/benjaminoats/_desk/008
368M	/private/tmp/j0912-short-a-v04
464M	/Users/benjaminoats/.cache
522M	/Users/benjaminoats/_desk/J1924-records
530M	/private/tmp/J2089-rights
530M	/private/tmp/codex-J2089
530M	/private/tmp/codex-j2200-record
531M	/private/tmp/codex-J2248-chief-review
531M	/private/tmp/codex-J2248-v03
532M	/private/tmp/J2309-resume
538M	/private/tmp/codex-j2199-queue
540M	/private/tmp/J2404-wt
542M	/private/tmp/j2427-wt
545M	/private/tmp/codex-j2159-queue
545M	/private/tmp/codex-j2278-queue
550M	/private/tmp/codex-j2292-queue
559M	/Users/benjaminoats/.npm
569M	/private/tmp/gemini-J1100-wt
891M	/Users/benjaminoats/_desk/state
1.2G	/Users/benjaminoats/Downloads
1.5G	/Users/benjaminoats/YouTube/hos-008-lightning
2.3G	/Users/benjaminoats/_desk/cache
4.0G	/Users/benjaminoats/_desk/scratch
4.6G	/Users/benjaminoats/_desk/renders
8.9G	/Users/benjaminoats/YouTube/History Of Science
 13G	/Users/benjaminoats/_desk/worktrees
 16G	/Users/benjaminoats/YouTube/orbit-with-ben
```

---

## 3. Detailed Comparison of Film Folders Over 1 GB vs `/Volumes/data/studio-live`

> **Note on NFS AppleDouble files (`._*`):** On `/Volumes/data/studio-live` (Synology NFS mount), macOS creates `._<filename>` AppleDouble extended-attribute sidecar files (`4,096` bytes each) alongside copied files. Below, both **raw** counts/bytes (including `._*` and `.DS_Store`) and **content** counts/bytes (excluding `._*` and `.DS_Store`) are reported so the comparison is exact.

1. **`/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/028_A-Star-Is-Coming-Toward-Us`**
   - **Local size:** `2.4G` (`du -sh`), `926` files, `2,583,139,162` bytes (`0` AppleDouble/DS_Store files).
   - **NAS path:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/028_A-Star-Is-Coming-Toward-Us`
   - **NAS size:** `2.4G` (`du -sh`), `1,930` raw files / `2,586,746,057` bytes (`918` content files / `2,582,600,905` bytes + `1,012` `._*`/`.DS_Store` files).
   - **On `studio-live`:** **yes** — all `918` non-`.pyc` content files exist on `studio-live`. Only 8 local `__pycache__/*.pyc` files are absent on NAS, and `status.json` has a slight byte-length difference.

2. **`/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode`**
   - **Local size:** `1.1G` (`du -sh`), `1,066` files, `1,192,036,264` bytes (`0` AppleDouble/DS_Store files).
   - **NAS path:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/029_Is-Betelgeuse-About-To-Explode`
   - **NAS size:** `1.1G` (`du -sh`), `2,190` raw files / `1,195,833,257` bytes (`1,057` content files / `1,191,192,489` bytes + `1,133` `._*`/`.DS_Store` files).
   - **On `studio-live`:** **yes** — all `1,057` non-`.pyc` content files exist on `studio-live`. Only 9 local `__pycache__/*.pyc` files are absent on NAS, and `status.json` has a slight byte-length difference.

3. **`/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin`**
   - **Local size:** `2.0G` (`du -sh`), `752` raw files / `2,115,955,441` bytes (`749` content files / `2,115,943,153` bytes + `3` `.DS_Store` files).
   - **NAS path:** `/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin`
   - **NAS size:** `2.0G` (`du -sh`), `1,608` raw files / `2,137,077,481` bytes (`753` content files / `2,133,575,401` bytes + `855` `._*`/`.DS_Store` files).
   - **On `studio-live`:** **yes** — `0` local files missing on NAS and `0` size differences across all 749 content files (`100%` byte-for-byte size match), plus 4 additional files (`+17.6 MB`) on NAS.

4. **`/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan`** *(borderline: `976M` binary `du -sh`, `1,023,004,223` decimal bytes > 1 GB)*
   - **Local size:** `976M` (`du -sh`), `364` files, `1,023,004,223` bytes.
   - **NAS path:** `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/032_What-Would-Happen-If-You-Landed-On-Titan`
   - **NAS size:** `2.9G` (`du -sh`), `1,717` raw files / `3,077,099,644` bytes (`838` content files / `3,073,499,260` bytes + `879` `._*`/`.DS_Store` files).
   - **On `studio-live`:** **yes** (superset on NAS) — `0` local files are missing on `studio-live`; `studio-live` holds 474 additional working files (`+2.05 GB`) and 5 files (`production-status.md`, `status.json`, `03_Reference-Material/harvest_J2089_v01/contact_sheet.jpg`, `10_Shorts/README.md`, `10_Shorts/SHORTS_PLAN_v01.md`) differ in byte size.
