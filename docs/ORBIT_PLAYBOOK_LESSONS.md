# Orbit playbook lessons (1 Oct 2026)

Standing rules and findings from Ben (relayed by Chief of Staff) and the Saturn v03b / v03c edit pass. **Cursor and Claude both work from this file** on the PR #99 thread. Orbit With Ben only — not History of Science.

Linked from `AGENTS.md`. When this conflicts with older notes in `_archive/` or a project UAT folder, this file and the docs in force in `AGENTS.md` win. Ben merges the PR that lands or updates these rules.

---

## 1. Neighbour rule (topic lock)

Every film needs **at least three** big education or space videos (**≈1M+ views**) on its topic **before topic lock**.

- Log them in `00_Brand/Channel-Setup/templates/TOPIC_OPPORTUNITY_SCORE.md` and the project's `PRE_BUILD_VIDIQ_AUDIT.md`.
- Reuse their **subject words** in title, description and tags.
- **Never** put their channel names in the public listing.
- A strong neighbour pool is evidence for Ben. It does **not** pick the topic.

**Evidence:** HOS 002 gets **55.6%** of its views Suggested from TED-Ed's Mendeleev video. Orbit should chase the same Suggested / related neighbourhood pattern with education peers (Kurzgesagt, TED-Ed, Veritasium, SciShow Space, PBS Space Time, NASA, Crash Course, BBC Earth Science, and peers).

Full step: `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` §2. Audit example: `00_Brand/Channel-Setup/audits/neighbour_pass_2026-10-01/REPORT.md`.

---

## 2. Edit rules (from Ben's v03b notes)

These are assembly locks for every long from Saturn v03c onward.

### Chapter cards

- Wait for the **VO sentence to finish** before a chapter card.
- Hold **0.5–0.8 s** of breathing room (music / picture only).
- Then cross-fade the card in about **0.4 s**.
- No spoken line is ever clipped by a row or card boundary.

### End of film

- Picture and music run **past the last VO word**.
- Picture holds **15–20 s** after the last VO word (end-screen space).
- Music carries **2–3 s** past the last word, then fades over ~10 s.
- Picture fades over the last **2 s**.
- Music covers the **full runtime** (a silent end hold fails).

### Timing source (root cause)

- Row times come from the **locked VO's word timestamps** (`align_shot_list.py`), never from planned times.
- `clip_check --words` catches clipped lines; aligning from the LOCK VO first prevents them.

### Picture

- Fill **16:9** with no flat bars.
- Use a feathered blurred background if the plate is not natively 16:9.
- Upscale no more than about **2.35×** (see also `NASA_POOL_v01.md` rule 4 — defers to this §2).

### Audio

- Mix around **−14 LUFS** with clear VO.
- Check for **repeated or stumbled VO phrases** before delivery (do not ship a take that doubles a line).

### Gate

```bash
python3 00_Brand/Channel-Setup/tools/clip_check.py <shot_list.csv> [--words vo_words.json] [--vo-end SEC]
```

Run this (or the project `check_shot_list.py` that calls it) before marking a cut ready for Ben. Exit 0 only on pass.

Also see `STUDIO_PLAYBOOK.md` §7.

---

## 3. Production locks (existing · restated)

| Rule | Detail |
|---|---|
| Orbit generation | Orbit is always **Omni**. One approved tumble fallback only: the **0–3 s** window on the named tumble file (e.g. `veo_orbit_tumble_v03_fallback_0-3s.mp4`). No other Orbit fallback without Ben. |
| Thumbnails | **Never** include Orbit on **any** thumbnail (longs and Shorts covers). |
| NASA stills | Verify every NASA ID against the images / Photojournal API (or the project's verified pool JSON) before the shot list goes to Ben. |
| Media in git | **No media in git.** Stills, VO, Veo/Omni clips and broadcast masters live in iCloud / local UAT paths only. |
| Public / KEEP | Claude gives the final OK before anything is scheduled (3 Oct order). **Nothing is KEEP until Claude reviews it.** |
| Shot list | The shot list goes to **Claude on the thread before generation**. Never a whole planet as an Omni/Veo start frame: it drifts to the wrong planet. |
| Compute | **Vertex only** for film generation, on the free credit already on the account; Omni (`gemini-omni-flash-preview`) is served from location `global` only. Never AI Studio prepaid. No Kling, Seedance, or ElevenLabs Image & Video. |

---

## 4. Thread protocol (PR #99)

PR #99 is the Chief of Staff ↔ Claude message thread (`scripts/owb_thread.py`).

| Rule | Detail |
|---|---|
| Read first | Run `python3 scripts/owb_thread.py status` (or `read`) at the start of every session and **before telling Ben anything is waiting on Claude**. Exit 10 means unread Claude messages: read and act on them first. End every report to Ben with "Thread read to #<id>". (2 Oct: Ben was told "waiting on Claude's titles" while the titles had been on the thread for hours.) |
| One actor | Only Ben's primary Chief session acts on the thread (swaps, renames, posts). **Before acting on a Claude message, claim it:** answer with `owb_thread.py post --re <claude id>`; if it is refused ("Already answered") or exits "LOST" (two claims in the same seconds: the lowest comment id wins and the loser withdraws its claim), another session has it: stop, do not touch Studio. Act only when `post --re` exits 0. Claim first, then act, then post results with a plain `post` (no `--re`: your own claim already counts as the reply) starting "Done <id>:". (3 Oct: two wakes both swapped the same covers and both replied.) |
| Act on Claude | Claude's replies on the thread are acted on **like Ben's relays** — implement, report, continue. |
| NEEDS BEN | Since 3 Oct 2026 (Ben: *"always ask Claude first"*) every NEEDS BEN item goes to Claude on this thread first; Claude decides and tells Ben. Only money, the irreversible, what only Ben can do and direction changes still go to Ben (`AGENTS.md`). Since 5 Oct 2026 (Ben to Claude directly), Claude owns `AGENTS.md` and the Never list, and may make a public video private or take it down; real money stays with Ben. Do not invent Ben's OK. |
| Claude's OK | Since 3 Oct Claude's decision on the thread is the final OK before scheduling, recorded as "Claude OK (Ben's 3 Oct order)" and reported to Ben. A PASS on a step is not the final OK; the final OK names the files and the slot. |
| Never touch #99 | Never **merge**, **close**, or **push** to PR #99, even when told to merge all PRs. |
| Orbit only | Keep HOS packaging and HOS media out of this thread unless Ben explicitly asks. |

---

## 5. What agents should do when unsure

1. Read `AGENTS.md`, then this file, then `STUDIO_PLAYBOOK.md`.
2. Prefer a proposal + evidence over a silent Studio or git change.
3. Post status to the Claude thread with `python3 scripts/owb_thread.py post -f report.md` when the order says to.
4. Take sign-offs to Claude on the thread (`AGENTS.md` "Stop and ask Ben"). Only real money, things only Ben can do, and direction changes go to Ben.

---

## 6. Shorts feed lessons (Claude ruling, 5 Oct 2026)

Source: Chief's read of YouTube Analytics for 60 public Orbit Shorts after Moon Short `dQlOgsDGmtA` stalled (#99 5999672592). The report is on the Mini at `~/_desk/handoff/moon-short-vs-winners-2026-10-05.md`. On day 1 a Short is either fed by the Shorts feed or it isn't. Fed Shorts (40) had a median of 85.5 day-1 views, 85% of them from the feed. Not-fed Shorts (20) had a median of 13 views, 15.5% from the feed. Retention did not separate the two groups.

| Rule | Detail |
|---|---|
| **R1 · Score by feed share** | Judge a Short by its **day-1 Shorts-feed share** in Analytics: 50% or more means fed. Under ~50 views, % viewed is noise; don't use it to call a Short. This is a post-publish read, not a ship gate. |
| **R2 · Topic fatigue** | At most 6 Shorts in a row on one topic. Stop a topic after **2 not-fed Shorts in a row**, then give it a 2-week break. (Moon #1–#6 were fed; #7–#10 were not.) |
| **R3 · Own open** | Every Short gets its own open. Frame 0 shows the subject the title names. Never reuse an opening background from the last 10 Shorts. The Auditor ship gate checks frame 0 against the last 10. |
| **R4 · Orbit early, never at frame 0** | Orbit may arrive from about 1 s (`Ih2zhZTbIR0` was fed with an Orbit slide-in). The Never list still bans Orbit at frame 0. |
| **R5 · Retention target** | Aim for a day-1 average viewed of 60% or more. Fed Shorts above it had a median of 142 day-1 views; fed Shorts below it, 61. This is a target, not a gate. |
| **R6 · One at a time** | Already covered by the Never list: one Short a day, and never re-upload an idea that already went public. The 24 Sep Moon batch broke both, so treat it as a warning, not a method. |

`dQlOgsDGmtA`: leave it alone (no delete, re-upload or retitle). Read its Analytics on Wed 7 or Thu 8 Oct. Moon Shorts are paused for at least 2 weeks; the next Short is Jupiter `buaOI3QGm7U` on 14 Oct.
