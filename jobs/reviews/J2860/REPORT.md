# J2860 — Sleep Film (`_sleep_video_01`) 97:38 Picture Repair & Verification

- **Job:** `J2860` (`macbook`, `£0` spend, nothing deleted, `sleep_video_01_master_v01.mp4` untouched)
- **One-line root cause:** Encode fault (mixed-profile MP4 stream-concat): in Chapter XII · *Proxima Centauri in the Dark* (`90:02.1–97:53.5`, cut from `026_How-Far-Is-The-Nearest-Star` master `026_NearestStar_v06_cfr18.mp4` around `07:55.8` at `97:38`), `J2452` darkened Chapters XI–XIII with `-crf 0` (lossless `High 4:4:4 Predictive`, `profile_idc=244`) and stream-copied (`-c:v copy`) them behind Chapter I's `High`-profile (`profile_idc=100`) `avc1` header, corrupting Apple VideoToolbox hardware decode and the R2 Watch stream across `97:36–97:39` (`97:38`, VLT Paranal night timelapse → star-trails dissolve).

## 1. Whole-Master Check (Step 2)

- **Chapters I–X (`00:00.0–82:14.7`, films `013, 021, 027, 025, 023, 031, 020, 022, 028, 029`):** All encoded in standard `High` profile (`profile_idc=100`). `0` windows with profile-mismatch or hardware-decode corruption.
- **Chapters XI–XIII (`82:14.7–108:02.3`, films `024`, `026`, `019`):** All three chapters in `v01` carried the exact same `-crf 0` `High 4:4:4 Predictive` profile mismatch (`TIMELINE.json` lines 112, 122, 132), causing the same hardware-decode / Watch-proxy macroblock corruption across `85:11, 86:01, 89:21` (Ch XI · `024`), `90:29–97:53` including `97:31, 97:36–97:39, 97:50–97:51` (Ch XII · `026`), and `97:58–107:35` (Ch XIII · `019`).
- **Repair scope (Step 3):** Re-encoded all three affected darkened chapters (`024_light_darkened_v06_high.mp4`, `026_proxima_darkened_v02_high.mp4`, `019_andromeda_darkened_v02_high.mp4`) from their verified darkened sources to standard `High` profile (`profile_idc=100`, `yuv420p`, `-crf 18`, matching Ch I–X `avcC`), rebuilt Joins `10`, `11`, `12` and `final_fade_v02.mp4` from the `High`-profile endpoints, concatenated all 27 `High`-profile parts, and muxed with the identical single-bed narration audio stem (`sleep_audio_encoded_v05.m4a`). No new footage and no new searches.
- **Post-repair whole-master check on `v02`:** `27` spot windows across all 13 chapters + continuous VideoToolbox decode across Joins `10–12`, `97:15–98:10`, and `108:00–108:22` all return `rc = 0`, `stderr = ""`, `max_hw_vs_sw_mad = 0.0`. **Zero** remaining faults anywhere in `v02`.

## 2. Repaired Master (`v02`) & Gate Verification (Step 4)

| Check | Result | Evidence |
|---|---|---|
| **NAS master `v02`** | **PASS** | `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/sleep_video_01_master_v02.mp4` (`4,216,695,410` bytes, SHA-256 `e6f1064dc83b2c48bb05898f90139a4a250da2b316d3d3086699518379481ec0`, verified on both the MacBook and the NAS; `v01` untouched at SHA-256 `05b439cbc3a0ab77d006f571f79fb8d0d9b3054a0023250c569941c70887d698`) |
| **Exact frame & audio length** | **PASS** | `195,070` video frames (`6502.333333 s` @ `30/1` CFR) and `304,798` audio frames — exact frame-for-frame match to `v01` |
| **Video profile uniformity** | **PASS** | `High` (`yuv420p`, `level 4.0`) across all 27 concatenated segments |
| **Pixel check (`polish_gate`) & `picture_qa`** | **PASS** | Rebuilt joins `10` (`029->024`), `11` (`024->026`), `12` (`026->019`) 10s neighborhoods: `polish_gate` `0` fails, `picture_qa` `PASS`. Chapter XII (`026`) undarkened `changed_cuts`: `polish_gate` `0` fails, `picture_qa` `PASS` |
| **Join sound & single bed** | **PASS** | Audio stream packet hash `SHA256=74f9ab69f926dee582179764d158a2af07e2c2523c38624d9a5068ecd45041d2` matches `v01` bit-for-bit; Joins `10/11/12` `ebur128` + `silencedetect`: `-19.7 / -20.6 / -21.1 LUFS`, peaks `-6.5 / -6.5 / -6.9 dBFS`, `0` silences `>= 2.5s` |
| **Darkening measurement (`0.85 ± 0.02`)** | **PASS** | `024`: `0.85174` (`PASS`); `026`: `0.86727` (`PASS`); `019`: `0.85200` (`PASS`) |

## 3. Screenshots, Before-and-After Card & Listing Handoff (Steps 1 & 5)

Saved and SHA-256-verified on the NAS under `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/j2860_v02/`:
- **`sleep_video_01_97m20_before_after_v02.mp4`** (`27,305,320` bytes, `73.03 s`, SHA-256 `912a5f16f4b0740c0d3eaaceff7a4a25f81339cc8c755bc3f5123a01ad07d864`): wired to Ben's `SLEEP01` board card (`J2452` `awaits_ben`, `< 120 MB` auto-uploaded to R2). Opens directly at **`97:20`** of `v02` (`0:00–0:45`, playing `97:20–98:05` across `97:38` and Join 12), followed by a moving side-by-side Before (`v01`) vs After (`v02`) of `97:32–97:44` (`0:45–0:57`), large phone-readable `97:36–97:39` screenshots (`0:57–1:03`), the `97:20–98:00` 1 fps sheet (`1:03–1:08`), and the `97:36–97:40` 30 fps every-frame sheet (`1:08–1:13`).
- **`sleep_97m20_98m00_1fps_before_after.jpg`** (`879,151` bytes, SHA-256 `810bdcb0b081ca2ac62f81b6375cc44ad011487ef5dd11763048c84bc8123f47`)
- **`sleep_97m36_97m40_30fps_before_after.jpg`** (`1,225,957` bytes, SHA-256 `12f7a8e6f898a72bfe5bc9f5f25a536fc15299e5d1c6735e802f44d44988975b`)
- **`card_focus_9736_9739.png`** (`1,376,197` bytes, SHA-256 `f90eff8eaa2dae658d530a5b33ac1259b051066112934d50153a26406f46be6b`)
- **Listing package handoff for `J2861`:** Wrote `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/11_Upload-Package/PACKAGE_MANIFEST_v02.json` (`sha256: 58cbba3e44bf9a5dfa438ad099cfe3390509107856b2b35039fa64c27c4f03bc`) pointing `video` and `masterSha256` to `sleep_video_01_master_v02.mp4` while preserving `PACKAGE_MANIFEST.json` untouched; closing `J2860` unblocks `J2861`.
