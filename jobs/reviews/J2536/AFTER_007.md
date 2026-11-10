# History of Science 007 `ETynHpIYLeY`: after (J2536, 10 Nov 2026)

Done in YouTube Studio (CDP 9222; channel id `UCXp7HkBIl1LgaznXuZHJyRg` checked on the page before every click). Authority: the third exception in AGENTS.md, Never, Studio (Ben, 10 Nov 2026, "Ok on both").

## What was done

1. `Edit title` clicked. Dialog: "Editing your video title will delete your A/B test including your other title options. Do you want to continue?" Continue pressed. Studio showed "Experiment deleted". The J0959 test is gone; it had not started.
2. Title set to **How Was the First Vaccine Made? (And Why It's Named After a Cow)** and saved (about 23:35Z). Read back after a reload: that title, visibility Scheduled, description hash unchanged.
3. `A/B testing` opened, `Title and thumbnail` chosen. Slot 1 came filled with the new title and the video's own thumbnail (THE MILKMAID'S SECRET, thumbnail A); it was left as Studio filled it, not uploaded again. Slot 2: Why Vaccines Are Named After a Cow + `hos_007_thumb_B_immune_v01.jpg` uploaded from the Mini (sha256 `c102e7bd426970a68a799e73b784a2b163f93249985c4f9f02d613870558c71a`). Slot 3 left empty. Studio: "Title and thumbnail test ready". `Set test` (Studio: "The test is ready and will start once you save your changes"), then Save. First try, no retry.

The Studio dialog also carries a vidIQ "Generate" panel. It was not pressed.

## Read-back

- Studio after a reload (23:37:09Z), title panel word for word: A/B testing titles / Ineligible / How Was the First Vaccine Made? (And Why It's Named After a Cow) / Why Vaccines Are Named After a Cow
- Studio: thumbnail panel Ineligible; two custom thumbnails on the video (`mqdefault_custom_1`, `mqdefault_custom_2`); visibility Scheduled. Both pictures were seen in the test dialog before `Set test` (THE MILKMAID'S SECRET in slot 1, IMMUNE in slot 2); after the save they were not compared pixel by pixel.
- API at 2026-11-10T23:37:27Z (`API_AFTER.json`): title `How Was the First Vaccine Made? (And Why It's Named After a Cow)`; privacy private; publishAt 2026-11-12T18:00:00Z (the time J2470 read that morning); custom thumbnail present.
- Description: sha256 `4721ecd5976559544575443ecbdb3c612d53ce3a758927ae33d994075ba0886a`, 995 characters, identical to before, in Studio and from the API. Tags: 8, the same eight as before.
- End screen and cards: not opened and not changed by this job. They were not read back element by element; the Studio side panel still lists both.
- Ledger: the J0959 test had no row; new test **T029** in `05_Analytics/tests/THUMB_LEDGER.json`. The makers of the two thumbnails are not recorded, so both are "unknown".

## Limits of this record

- No API read was taken before the change; the before state is from Studio and from J2470's API read at 05:04Z the same day.
- Thumbnail A in slot 1 is the picture already on the video, as set by J0959 from the A file. It was not re-uploaded, so its bytes were not re-checked against the file's sha256.

Not touched: privacy, schedule, description, tags, cards, end screen, playlist, pinned comment, any other video. £0.
