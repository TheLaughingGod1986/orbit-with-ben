# J2452 — sequential picture PASS; master safety copy partial

Worker macbook-2. PR #789 remains open. Progress 14/15; no UAT, final delivery, upload, Studio, login, generation or spend.

The full sequential picture decode PASSes: exactly 195,070 frames, 108:22.333, exit 0, empty error log, zero duplicates/drops. Old seek-block coverage is not a full-file PASS; its final block missed one frame due to the source timestamp offset. Absolute timestamp seek recovered that frame, then the worker independently decoded the whole file with no seek. See FINAL_SEQUENTIAL_DECODE_V04.json. Candidate picture/audio hashes match the prior checkpoint. Ending fade measurement and thumbnail NAS hash also pass.

Local stream-copy mux candidate: `$SCRATCH/final_join_v01/sleep_video_01_master_v01.mp4`. 26505479537 bytes. SHA-256 `05b439cbc3a0ab77d006f571f79fb8d0d9b3054a0023250c569941c70887d698`. ffprobe confirms 195,070 video frames, 1920x1080, video duration 6502.332333 seconds, AAC duration 6502.333 seconds. No picture or sound encode was repeated. Encoded video and audio packet payload SHA-256 checks both PASS against the verified source candidates (LOCAL_MUX_PAYLOAD_READBACK_V01.json). Join, bed, sound, CTA and complete sequential decode checks are complete; reel/copies/watch card remain.

NAS safety copy is **partial**, not delivered: `/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/sleep_video_01_master_v01.mp4`. Preserved 10703863808 of 26505479537 bytes. Original writer exited 130 after explicit SIGINT, with file handles closed. No destination full hash exists. Nothing on NAS was replaced or deleted. Do not rerun mux_verified_master.py: local mux already exists.

## Next run

1. Verify no old writer remains. Resume from the same job branch with:

   ```sh
   python3 jobs/reviews/J2452/resume_master_safety_copy.py --scratch "$HOME/_desk/J2452-sleep-scratch" --destination /Volumes/data/studio-live/orbit-with-ben/02_Video-Projects/_sleep_video_01/sleep_video_01_master_v01.mp4 --seconds-budget 900
   ```

   It freshly hashes the local candidate, compares the entire existing NAS prefix byte for byte, appends only missing bytes, verifies the full destination hash and checks mux packet payloads. No delivery claim until MASTER_DELIVERY_V01.json is written. Partial files stay intact on timeout.
2. Then render the 12:26 reel via build_watch_reel.py with the same --scratch and --destination ending sleep_video_01_spotcheck_v01.mp4. The 12-minute first/join/last selection includes repaired Saturn → Earth; the 26-second appendix shows each chapter's brightest two-second window. Review proxy is 720p. Script fully decodes the reel and verifies its NAS hash. Reel is not yet rendered.
3. Record final mux packet identity and delivery reports; advance progress honestly, create the watch card with running order and files/hashes, then awaits/UAT (or park for Chief if refused). Version-one charts/labels remain; dissolves only on compilation edits; earliest air date 12 December. Previous audio/CTA/12 join checks remain in the preceding checkpoint. No playback/listening claim.

All earlier source masters, saved chapters, rejected candidates and evidence remain. No new source search or generation.

Validation: 13 privacy tests, Python compilation and git diff --check PASS. All launched processes exited, including sequential decode, mux/copy writer, source hashing and packet-payload verification.
