# J2716 — First-Day Check at 6 h: *How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?* (`uhZSRcvngvE`)

- **Channel:** Orbit With Ben (`UC_esArsDKd3GJvOkeO0DUog`, verified on CDP `9223` before reading)
- **Video:** `uhZSRcvngvE` (*How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?*), Short (`55 s` / `0:55` badge; scheduled one-off 50–60 s length test per `studio/RULES.md` → *Packaging* §5)
- **Went live:** `2026-11-12T11:30:00Z` (Thu 12 Nov 11:30 London)
- **Read window:** `2026-11-12T18:00Z`–`18:03Z` UTC (~6 h 30 m after going live)
- **Mode:** Read-only (`£0` spend, zero YouTube or Studio settings changed; reused existing `studio.youtube.com` tab on CDP `9223`)

---

## 1. Is Anything Broken? (`0` faults)

| Check | Studio Readback (`2026-11-12T18:00Z`–`18:03Z`) | Status |
|---|---|---|
| **Visibility** | **Public** (`Public` on Content > Shorts row and Video details; `VIDEO_PRIVACY_PUBLIC`, `draftStatus: DRAFT_STATUS_NONE`) | **OK** |
| **Listed under Content > Shorts tab** | **Yes** (Row 0 under `Content > Shorts` filtered to Public; `contentType: CREATOR_CONTENT_TYPE_SHORTS`, watch URL `https://youtube.com/shorts/uhZSRcvngvE`) | **OK** |
| **Restrictions column** | **Empty (`—`)** — `Notices: —`, not Made for Kids (`This video is set to not 'Made for Kids'`), no copyright claim, no age restriction | **OK** |
| **HD processing** | **Finished** (UI badges `Standard Definition complete` + `High Definition complete`) | **OK** |
| **Related video vs upload package** | **`Could a Robot Survive on Mars? (One Lasted 14 Years)`** (`Js6EQJ8qDi8`) — matches `PACKAGE_MANIFEST.json` (`"relatedVideoId": "Js6EQJ8qDi8"`) and `UPLOADS.json` | **OK** |
| **Description vs upload package** | Exact match to `PACKAGE_MANIFEST.json`:<br>`Could a Robot Survive on Mars?`<br>`https://www.youtube.com/watch?v=Js6EQJ8qDi8` | **OK** |
| **Language & tags** | `Video language: English (United Kingdom)`, `Title and description language: English (United Kingdom)`, and all 6 manifest tags (`opportunity rover`, `mars rover`, `opportunity 14 years`, `mars dust storm 2018`, `could a robot survive on mars`, `nasa mars`) confirmed live | **Confirmed** |

No faults found in Step 1.

---

## 2. Studio Analytics Numbers (`Since published`, at ~6 h 30 m)

| Metric | Studio Value | Flag Recorded |
|---|---|---|
| **Overview > Views** | **`19`** | `--views 19` |
| **Overview > N more/less than usual** | **`221 less than the usual 240 – 810`** (`19 + 221 = 240`) | `--typical 240` |
| **Dashboard > Ranking by views (Latest Short card)** | **`9 of 10`** (*First 6 hours 30 minutes*) | `--rank 9 --of 10` |
| **Reach > Traffic sources (Shorts feed)** | **Shorts feed `52.6%` = `10` views** (`YouTube search 47.4%` = `9` views; `Other YouTube features 0.0%` = `0` views) | `--feed-views 10` |
| **Reach > Shown in feed** | No separate "Shown in feed" number card in Studio (`launch_check.py` derives `~19` from `10 / 53.3%`; Engagement tab notes `Engaged views: 8`) | *(omitted)* |
| **Engagement > Viewed vs swiped away** | **`53.3%` Stayed to watch** / `46.7%` Swiped away | `--stayed 53.3` |
| **Dashboard / Engagement > Average percentage viewed** | **`58.9%`** on Dashboard Latest Short card (`Average view duration: 0:32` on `0:55`) | `--avg-pct 58.9` |
| **Likes** | **`1`** | `--likes 1` |

Recorded in `05_Analytics/owb/launch/uhZSRcvngvE.json` via:
```bash
python3 scripts/launch_check.py record uhZSRcvngvE --hours 6 --views 19 --rank 9 --of 10 --typical 240 --feed-views 10 --stayed 53.3 --avg-pct 58.9 --likes 1 --by macbook-2
```

---

## 3. Output of `python3 scripts/launch_check.py judge uhZSRcvngvE`

```text
"How Did Martian Wind Keep a 90-Day Rover Alive for 14 Years?" (uhZSRcvngvE) · Orbit With Ben · Short · went live Thu 12 Nov 11:30 London
At 6 h: views 19 · Studio rank 9 of 10 · shown in feed about 19 (from 10 feed views) · stayed to watch 53.3% · average viewed 58.9%
Usual for this channel: stayed to watch 32.0%, average viewed 65.4%

Verdict: BEHIND, not shown
  - 19 views at 6 h; Studio says the usual for us at this age is 240.
  - Studio ranks it 9 of 10 against our latest videos at the same age.

What is different about this one
  - It is 55 s long; the last 10 Shorts were 18 to 27 s.
  - The title starts with "How", like 3 earlier Shorts: they had 386 views by the next morning (median), against 78 for all Shorts.
  - It is a second upload of the same video (it replaced N42gKBbD7tE).

Do now
  - Nothing in the cut explains this yet: YouTube has shown it to too few people to judge it.
  - Check the faults list is empty, then read tomorrow morning's snapshot. Under a tenth of the usual first day means the feed tried it and stopped: treat the subject and the title as the cause, not the edit.

Carry forward
  - If "What is different about this one" says earlier videos on its subject were weak too, take that subject off the next four weeks of the schedule and tell the topic go/no-go.
```

---

## 4. Context Notes for Chief

1. **Viewer response vs feed reach:** As on Wednesday's Mars Short `B1z2dv7m7Vk` (`45` views at 6 h, `68.4%` stayed, `59.0%` average viewed), the small group shown `uhZSRcvngvE` stayed well above the channel's usual (`53.3%` stayed vs `32.0%` usual; `58.9%` average viewed / `0:32` average view duration across a `55 s` cut), and YouTube search supplied nearly half its early views (`9` of `19`), while the Shorts feed has only given it ~19 impressions (`10` feed views) so far.
2. **Back-to-back Mars rover Shorts (`B1z2dv7m7Vk` note, 11 Nov):** Yesterday's Chief note on `B1z2dv7m7Vk` flagged that if Thursday's Mars Short also started slowly, back-to-back Mars rover Shorts are the shared factor and upcoming weeks' Shorts should be spread across subjects.
3. **One-off 50–60 s length test (`studio/RULES.md` → *Packaging* §5):** `uhZSRcvngvE` is the single Chief-OK'd 55 s length-test Short (`lengthTest: true`), to be logged in `00_Brand/Channel-Setup/audits/SHORT_LENGTH_TEST_2026-11/TEST_LOG.md` once its window matures.

Per Step 5 (`Verdict: BEHIND, not shown`), parking `J2716` for the Chief.
