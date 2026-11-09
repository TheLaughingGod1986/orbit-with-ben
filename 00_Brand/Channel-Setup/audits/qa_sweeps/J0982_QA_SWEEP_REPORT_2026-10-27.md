# J0982 Bounded Per-Export QA Sweep Inventory & Report (27 Oct 2026)

- **Job:** `J0982` (`both-qa-sweep`)
- **Agent:** `gemini` (Gemini Argon, addressing Acting-Chief Codex ruling of 26 Oct 22:18Z)
- **Total exports inventoried:** `62` (`42` OWB, `20` HOS)
  - **Window A — Original sweep window (`2026-10-24T18:48Z .. 2026-10-26T15:09Z`):** `37` exports (including `hos_sa_s4_curie_notebooks_v07`, `owb_sa_s2_neptune_v07`, `owb_sa_s3_iss_sunrises_v04`, and `hos_007_master_v04`)
  - **Window B — Post-`2026-10-26T15:09Z` revisions:** `19` exports (`owb_sa_s2_neptune_v07a`, `030_apophis_short_v13a`, `029_short_lift_die_young_10my_v01`, `029` `wed09`/`fri11`/`mon14` `v04`, `025` `mon09_night_cold_v04`, the 6 `J1032` Batch C `v04` Shorts, and HOS `004`/`005`/`007` Batch HC revisions)
  - **Window C — Standalone baseline packs (`S1`, `S4..S8` `v01`):** `6` exports (with newly generated `music_gate` sidecars)
- **Spend:** `£0` / `0 credits`
- **New repair jobs needed:** `0` (all exports pass automated gates or have documented source-bound exceptions already covered by active/completed review jobs)

## 1. Specific Items Raised in Acting-Chief Ruling (26 Oct 22:18Z)

1. **HOS Standalone `hos_sa_s4_curie_notebooks_v07` (committed `d0c0ee0a` at `2026-10-25T13:40Z`):**
   - Added to Window A inventory with full MP4 SHA-256 (`be30ff71...`), mtime, and all 3 gate reports under `docs/STANDALONE_SHORTS_TEST_2026-10/qa_shorts_v01/hos_sa_s4_curie_notebooks_v07/` (`picture_qa` `0/11` FAIL, `1` WARN; `polish_gate` `0/11` FAIL, `1` WARN; `music_gate` `PASS`).
2. **OWB Standalone `owb_sa_s2_neptune_v07` (and post-window `v07a`) + `owb_sa_s3_iss_sunrises_v04`:**
   - `447a06234` was indeed `owb_sa_s2_neptune_v06`, while `v07` was built in `J0943` with `polish_gate.json` and `music_gate.json` in `/Volumes/data/mac-mini-archive/scratch/J0943/neptune_v07/`. Ran `picture_qa.py` on both `owb_sa_s2_neptune_v07.mp4` (`rc=0`, `0/7` FAIL, `1` WARN) and `owb_sa_s2_neptune_v07a.mp4` (`rc=0`, `0/7` FAIL, `1` WARN) and committed all three gate reports (`picture_qa`, `polish_gate`, `music_gate`) under `00_Brand/Channel-Setup/audits/STANDALONE_SHORTS_TEST_2026-10/qa_shorts_v01/owb_sa_s2_neptune_v07{,a}/`.
   - For `owb_sa_s3_iss_sunrises_v04.mp4`, ran `picture_qa.py` (`0/6` FAIL on raw cut list, `1` WARN low-detail on `03_cupola_01`; with mapped `max_upscale=2.96` from `owb_sa_s3_iss_sunrises_v04_meta.json`, rows `01_iss_16_1062s` and `06_loop_tail` flag `upscale: 2.96× is over the 2.35× limit` — the known source-bound NASA JSC `640×480` 4:3→9:16 crop documented in `_meta.json` and already uploaded/reviewed in `J0916`). Committed `picture_qa`, `polish_gate`, and `music_gate` under `qa_shorts_v01/owb_sa_s3_iss_sunrises_v04/`.
   - Also ran `music_gate.py` on the remaining 6 OWB standalone baseline Shorts (`S1`, `S4..S8` `v01`, all `rc=0` `PASS`) and committed their `music_gate_*.{json,txt}` sidecars.
3. **HOS `007_The-First-Vaccine` `master_v04_pack`:**
   - `master_v04_pack/` had been committed on branch `codex/J0830-master-v01` (`8eafbbde`) and never merged to `main`. Checked out `02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/master_v04_pack/` (plus `master_v03_pack/`, `vaccine_score_bed_v01_plan.json`, `sfx_cues_v01.json`, and `picture_qa_review.jpg`) onto HOS `main` and verified `hos_007_master_v04.mp4` on NAS (`sha256: c7f62adbb241bf3fbfaa3a17929f05768eedcf89044cb2cc5ebd2971c163e810`, `0/102` FAIL, `6` WARN, `music_gate` `PASS`).
4. **Stale Gate Timestamps (`hos_005_s01_the_sum_v04` and `hos_007_s05_vacca_jesty_v03`):**
   - Re-ran `polish_gate.py`, `picture_qa.py`, and `music_gate.py` on both `hos_005_s01_the_sum_v04.mp4` and `hos_007_s05_vacca_jesty_v03.mp4` (`rc=0` on all 6 runs, `0/10` FAIL, `1` WARN each) so that all three gate report timestamps strictly postdate the `.mp4` files.

## 2. Per-Export Inventory Table

| Ch | Window | Film | Export ID | Media SHA-256 (prefix) | Media Mtime (UTC) | `picture_qa` | `polish_gate` | `music_gate` | Fresh? | Linked Jobs |
|---|---|---|---|---|---|---|---|---|---|---|
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:021` | `saturn_ten_metres_thin_v04` | `6de9961ac45d` | `2026-10-25T14:10:46Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | — |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:023` | `venus_95pct_wide_v05` | `09e5e66332fe` | `2026-10-25T14:09:22Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 13W) | YES | — |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:023` | `venus_two_hours_v04` | `20efc0c80d1c` | `2026-10-25T14:14:56Z` | PASS (0/6F, 1W) | PASS (0/6F, 1W) | PASS (0F, 13W) | YES | — |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:025` | `mon09_night_cold_v03` | `cfff04cdddcd` | `2026-10-26T07:21:16Z` | PASS (0/7F, 2W) | PASS (0/7F, 1W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:025` | `wed11_opening_testA_v04` | `788ae0e891d6` | `2026-10-26T11:46:00Z` | PASS (0/8F, 3W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:025` | `thu12_length_test_dust_v03` | `f9c4fba6550a` | `2026-10-26T10:39:53Z` | PASS (0/16F, 5W) | PASS (0/16F, 2W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:025` | `fri13_ingenuity_72_v04` | `d589d39d02d8` | `2026-10-26T11:06:07Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:026` | `mon16_cant_see_nearest_star_v03` | `cddcfb965567` | `2026-10-26T11:32:08Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:026` | `wed18_robot_reach_nearest_star_v03` | `8a264ecba447` | `2026-10-26T11:34:56Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:026` | `fri20_grapefruit_cherry_v03` | `a4024c86904c` | `2026-10-26T07:46:07Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:027` | `earth_sudden_air_v05` | `666ab5b1b16d` | `2026-10-25T08:04:55Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | — |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:027` | `earth_equator_weight_v03` | `e7220c124e4d` | `2026-10-26T12:03:39Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:028` | `028_short_mon30_comets_v03` | `01bbd942ee93` | `2026-10-26T12:20:40Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:028` | `028_short_wed02_opening_testA_v03` | `8abcd2cadd22` | `2026-10-26T12:38:43Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:028` | `028_short_fri04_scale_v03` | `bb935379881a` | `2026-10-26T12:46:32Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:028` | `028_short_lift_night_sky_35yr_v03` | `55c08d2ebfe9` | `2026-10-26T12:36:11Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:028` | `028_short_lift_oort_marbles_v03` | `344bd0d0ab04` | `2026-10-26T01:32:12Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | — |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:029` | `029_short_wed09_great_dimming_v03` | `fc3c1b30be44` | `2026-10-25T22:23:45Z` | PASS (0/8F, 4W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0961 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:029` | `029_short_fri11_opening_testA_v03` | `c12dc1774e68` | `2026-10-25T22:26:06Z` | PASS (0/12F, 3W) | PASS (0/12F, 2W) | PASS (0F, 13W) | YES | J0961 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:029` | `029_short_mon14_half_moon_daylight_v03` | `1e3d9ba6830b` | `2026-10-25T22:27:39Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0961 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:030` | `030_apophis_short_v13` | `2b276eb295df` | `2026-10-26T07:01:55Z` | PASS (0/7F, 6W) | PASS (0/7F, 1W) | PASS (0F, 14W) | YES | J0974 |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:SA` | `owb_sa_s2_neptune_v07` | `0919db03d432` | `2026-10-25T19:30:17Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 1W) | YES | — |
| OWB | `original_sweep_to_2026-10-26T15:09Z` | `OWB:SA` | `owb_sa_s3_iss_sunrises_v04` | `433ce60e09d4` | `2026-10-25T05:02:45Z` | PASS (0/6F, 6W) | PASS (0/6F, 1W) | PASS (0F, 14W) | YES | — |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:SA` | `owb_sa_s2_neptune_v07a` | `de62264cbd89` | `2026-10-27T00:13:08Z` | PASS (0/7F, 1W) | PASS (0/7F, 1W) | PASS (0F, 1W) | YES | — |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:030` | `030_apophis_short_v13a` | `898d26f526da` | `2026-10-27T00:42:50Z` | PASS (0/7F, 6W) | PASS (0/7F, 1W) | PASS (0F, 14W) | YES | J0974 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:029` | `029_short_lift_die_young_10my_v01` | `dc6bd3ccf387` | `2026-10-26T16:22:05Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0979, J1042 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:029` | `029_short_wed09_great_dimming_v04` | `e0459b017dda` | `2026-10-27T15:42:14Z` | PASS (0/8F, 3W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0961 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:029` | `029_short_fri11_opening_testA_v04` | `ff4194857a02` | `2026-10-27T15:43:27Z` | PASS (0/12F, 3W) | PASS (0/12F, 2W) | PASS (0F, 13W) | YES | J0961 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:029` | `029_short_mon14_half_moon_daylight_v04` | `31f362f4437b` | `2026-10-27T15:44:56Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0961 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:025` | `mon09_night_cold_v04` | `ad52d7b9d65c` | `2026-10-27T22:27:37Z` | PASS (0/8F, 4W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0935 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:026` | `fri20_grapefruit_cherry_v04` | `228cb06dfd37` | `2026-10-27T11:53:47Z` | PASS (0/9F, 3W) | PASS (0/9F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:027` | `earth_equator_weight_v04` | `d35efd737ed0` | `2026-10-27T10:49:19Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:028` | `028_short_mon30_comets_v04` | `65e58aea2a20` | `2026-10-27T11:20:08Z` | PASS (0/8F, 2W) | PASS (0/8F, 2W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:028` | `028_short_wed02_opening_testA_v04` | `0eb18596d2d6` | `2026-10-27T11:20:36Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:028` | `028_short_fri04_scale_v04` | `37fbe8b9ed33` | `2026-10-27T11:21:02Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `post_2026-10-26T15:09Z_revision` | `OWB:028` | `028_short_lift_night_sky_35yr_v04` | `91b297a262c1` | `2026-10-27T11:54:12Z` | PASS (0/8F, 1W) | PASS (0/8F, 1W) | PASS (0F, 13W) | YES | J0936, J1032 |
| OWB | `standalone_baseline_pack` | `OWB:SA` | `owb_sa_s1_mercury_v01` | `590f4e693d5c` | `2026-10-17T04:40:33Z` | PASS (0/5F, 4W) | PASS (0/5F, 1W) | PASS (0F, 1W) | YES | — |
| OWB | `standalone_baseline_pack` | `OWB:SA` | `owb_sa_s4_uranus_v01` | `0aec6e86525d` | `2026-10-17T04:48:23Z` | PASS (0/6F, 4W) | PASS (0/6F, 1W) | PASS (0F, 1W) | YES | J1007, J1008 |
| OWB | `standalone_baseline_pack` | `OWB:SA` | `owb_sa_s5_shooting_stars_v01` | `f21070efa726` | `2026-10-12T22:54:37Z` | PASS (0/5F, 1W) | PASS (0/5F, 1W) | PASS (0F, 1W) | YES | J1007, J1008 |
| OWB | `standalone_baseline_pack` | `OWB:SA` | `owb_sa_s6_titan_v01` | `3f2f51d4f8ff` | `2026-10-17T04:43:45Z` | PASS (0/5F, 4W) | PASS (0/5F, 1W) | PASS (0F, 1W) | YES | J1007, J1008 |
| OWB | `standalone_baseline_pack` | `OWB:SA` | `owb_sa_s7_pluto_heart_v01` | `a3572604f0da` | `2026-10-12T23:01:19Z` | PASS (0/5F, 1W) | PASS (0/5F, 1W) | PASS (0F, 1W) | YES | J1007, J1008 |
| OWB | `standalone_baseline_pack` | `OWB:SA` | `owb_sa_s8_voyager1_v01` | `b8bb56f7ef66` | `2026-10-17T04:44:42Z` | PASS (0/6F, 4W) | PASS (0/6F, 1W) | PASS (0F, 1W) | YES | J1007, J1008 |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:006` | `hos_006_master_v06` | `36c54e684b8a` | `2026-10-24T23:29:39Z` | PASS (0/96F, 5W) | PASS (0/96F, 5W) | PASS (0F, 0W) | YES | J0958 |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:007` | `hos_007_master_v04` | `c7f62adbb241` | `2026-10-24T23:45:35Z` | PASS (0/102F, 6W) | PASS (0/102F, 6W) | PASS (0F, 0W) | YES | J0960 |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:SA` | `hos_sa_s4_curie_notebooks_v07` | `38d643470b2d` | `2026-10-25T13:39:07Z` | PASS (0/11F, 1W) | PASS (0/11F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:001` | `hos_001_s11_curved_flask_v07` | `5de76a824e88` | `2026-10-25T15:16:21Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:002` | `hos_002_backcat_four_elements_v03` | `9340cae9cd5b` | `2026-10-26T00:47:56Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:004` | `hos_004_backcat_gold_foil_v03` | `f1cb7ec072c7` | `2026-10-26T00:45:03Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:004` | `hos_004_s05_dalton_v03` | `f93745e95558` | `2026-10-26T13:14:18Z` | PASS (0/9F, 1W) | PASS (0/9F, 1W) | PASS (0F, 13W) | YES | J0966 |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:005` | `hos_005_s01_the_sum_v04` | `e98ce5602b63` | `2026-10-25T11:58:02Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:005` | `hos_005_s02_the_tied_arm_v05` | `c31fbb5c88f6` | `2026-10-26T00:50:45Z` | PASS (0/12F, 1W) | PASS (0/12F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:005` | `hos_005_s03_never_saw_v03` | `3646009fc651` | `2026-10-26T13:13:27Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | J0966 |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:005` | `hos_005_s04_galen_stove_v04` | `f15fb5ba050b` | `2026-10-25T14:42:10Z` | PASS (0/9F, 1W) | PASS (0/9F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:005` | `hos_005_s05_valves_v03` | `e3aa2c6cfc56` | `2026-10-26T00:51:47Z` | PASS (0/9F, 1W) | PASS (0/9F, 1W) | PASS (0F, 13W) | YES | — |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:007` | `hos_007_s04_smallpox_test_v02` | `745de3f56a11` | `2026-10-26T07:57:45Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 14W) | YES | J0966 |
| HOS | `original_sweep_to_2026-10-26T15:09Z` | `HOS:007` | `hos_007_s05_vacca_jesty_v03` | `c94af4f919a4` | `2026-10-26T07:59:04Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 14W) | YES | J0966 |
| HOS | `post_2026-10-26T15:09Z_revision` | `HOS:005` | `hos_005_s03_never_saw_v04` | `e1f862ba737a` | `2026-10-26T21:33:48Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | J0966, J1005 |
| HOS | `post_2026-10-26T15:09Z_revision` | `HOS:007` | `hos_007_s04_smallpox_test_v03` | `858495ea7dcb` | `2026-10-26T19:08:19Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | J0966, J1005 |
| HOS | `post_2026-10-26T15:09Z_revision` | `HOS:007` | `hos_007_s04_smallpox_test_v04` | `3ef3fa773750` | `2026-10-27T22:42:13Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | J0966, J1005 |
| HOS | `post_2026-10-26T15:09Z_revision` | `HOS:007` | `hos_007_s05_vacca_jesty_v04` | `7a3a736069e2` | `2026-10-26T19:11:04Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | J0966, J1005 |
| HOS | `post_2026-10-26T15:09Z_revision` | `HOS:007` | `hos_007_s05_vacca_jesty_v05` | `e5ea76f012fb` | `2026-10-26T20:38:29Z` | PASS (0/10F, 1W) | PASS (0/10F, 1W) | PASS (0F, 13W) | YES | J0966, J1005 |
| HOS | `post_2026-10-26T15:09Z_revision` | `HOS:004` | `hos_004_s05_dalton_v04` | `8ce07a605697` | `2026-10-27T22:42:47Z` | PASS (0/9F, 1W) | PASS (0/9F, 1W) | PASS (0F, 13W) | YES | J0966, J1005 |
