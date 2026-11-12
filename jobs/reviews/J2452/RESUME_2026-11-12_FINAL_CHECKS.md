# J2452 — repaired joins and encoded sound, 12 November

Worker macbook. Progress remains **13/15**. PR #789 is open and unmerged. No UAT, upload, Studio action, generation, spend or NAS writes this run.

## Completed

- Repaired Saturn's dark exit using its own previously measured clean frame at chapter second 505. Original saved chapter remains intact. Stream-copied prefix is exactly 15,016 frames; new tail is 551 frames, preserving all 15,567 chapter frames and every narration sample in the separate PCM mix. Dissolve to the neighbor begins at 504.033 seconds for two seconds, followed by the neighbor hold. No source search or generation.
- Normal picture QA over the complete repaired tail, four-second breath and three incoming Earth seconds passes. All twelve compilation join neighborhoods pass, with three source-side seconds on either side for the other eleven. No threshold change or waiver. Warning sheets and six repair stills inspected as still images; no playback/listening claim.
- New picture candidate: `$SCRATCH/final_join_v01/sleep_picture_candidate_v04.mp4`, 195,070 frames, container duration 6502.332333 seconds. SHA-256 `4b7ac31c0a3b85052d2a9ed2eae09035eb91cd7b6b9ae3bc46ade2e74ad5f4e6`. Only Saturn's small tail and breath changed; all other saved chapter interiors are stream-copied. Timeline remains 108:22.333 at 30 fps.
- Saved AAC: `$SCRATCH/final_join_v01/sleep_audio_encoded_v05.m4a`, SHA-256 `2ed0fc501d49a91f2987632b3931124e0c15f017883959396c8fe5e2dbd6bb01`, duration 6502.333 seconds. Independent whole-file decode: **−20.1 LUFS, −6.4 dBTP, no silence over 3 seconds at −60 dB**. Native AAC fast coder, 192 kbps. Earlier slow native attempt stopped cleanly; AudioToolbox initialization failed. Those files remain as rejected/incomplete evidence.
- Whole-film kept-transcript audit: all thirteen build reports contain narration text; no subscribe, next-week, agenda or promotional phrase flags. This is an audit of the corrected source-word transcripts, not independent ASR of the final mix.
- Final picture decode: **41,400/195,070 frames**, contiguous first 23 minutes, passed in 60-second blocks with `-xerror`, exact frame counts and empty error logs. **Partial, not a full-decode PASS.** Covers both repaired Saturn boundaries. The earlier whole-file decode was stopped; its partial log is not a pass. Hardware decoding was unavailable; a software fallback probe is not counted in block coverage.

## Resume without repeating work

`$SCRATCH` is the MacBook's `_desk/J2452-sleep-scratch` folder. Reports under `final_join_v04/` are sanitized copies; actual resume ledger remains in local scratch.

1. Continue bounded software decode:

   ```sh
   python3 jobs/reviews/J2452/decode_final_in_chunks.py --scratch "$HOME/_desk/J2452-sleep-scratch" --seconds-budget 900
   ```

   It skips successful blocks and records each completed minute. Partial blocks are never credited. It stops its own child on timeout. No new picture encode or audio encode is needed.
2. Once all 195,070 frames pass, verify the picture and AAC hashes, stream-copy mux them to a new versioned master, verify mux duration/frame count/audio and the repair/joins against the saved candidates. Check intentional twenty-second ending fade by measurement; do not waive an accidental black join.
3. Build the roughly twelve-minute reel, including first five minutes, two joins (include repaired Saturn → Earth), last five minutes, and the required brightest-window material. Follow the Chief's reel/watch instructions if those require a separate extra brightest-window reel.
4. Add master/reel to the NAS film folder without replacing existing files; read back complete destination hashes. Thumbnail Option A is already saved per the input record. Record all paths/hashes and Ben's watch card, retaining version-one scope: source charts/labels stay; dissolves only on compilation edits; earliest air date 12 December.
5. Only then set awaits/UAT, or park for Chief with complete file evidence if worker awaits is refused. No upload.

Thirteen privacy tests, Python compilation and diff check passed. All processes launched by this run exited, including bounded decode, AAC encode and measurements, and join checks. OWB restored to main after pushing; HOS untouched. Thread read through #6810393552; the CLI displayed messages but could not persist its home-directory read marker under the sandbox.

## Superseding verification, macbook-2, 12 November

The default seek-based final block returned 669 frames versus 670 expected, despite an empty error log. Absolute timestamp seek decoded all 670; the first source frame has a 0.021-second offset. The worker therefore replaced block coverage with a full sequential no-seek decode, using fps_mode passthrough: exactly 195,070 frames, exit 0, no errors, duplicates or drops. See final_join_v04/FINAL_SEQUENTIAL_DECODE_V04.json and DECODE_SEEK_FINDING_V01.json. Do not rerun or promote the old partial block ledger. Both candidate hashes were freshly verified; final fade and thumbnail measurements are recorded beside these reports. Delivery outcome is recorded in the newer resume checkpoint.
