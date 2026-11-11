# Splitting the rule book: studio rules and channel rules

J2527. Written 11 Nov 2026 against `AGENTS.md` as it stood that morning (704 lines). The line numbers below are that
file's. **The move is done** (step 2): the channel rows are in `studio/RULES.md`, word for word. "What changed between
the table and the move" near the end lists the four places where the move differs from the first version of this
table, and why.

## Why

Ben, 10 Nov 2026: *"this system will read the individual channel's rules and guidance"*. `docs/MULTI_CHANNEL_PLAN.md`,
decision 4: `AGENTS.md` mixes two kinds of rule.

- **Studio rules** hold for every channel the studio runs: the Ben gate, the Never list's safety lines, sign-offs,
  who does what, the queue, the relay, the machines, the NAS.
- **Channel rules** are one channel's own style: how its films teach, look, sound, are titled and are packaged, and
  when they air.

A channel can add a rule. It can never remove a studio rule.

After the move, `AGENTS.md` keeps the studio rules and says where a channel's rules are read from. Orbit With Ben's
own rules live in `studio/RULES.md` at this repo's root, the file `scripts/channel_check.py` already asks for.

## How each rule was sorted

Three questions, in order. The first "yes" decides.

1. Would breaking it cost money, publish or delete something, leak something, or stop the machines working together?
   Then it is a **studio** rule.
2. Does History of Science already carry its own, different version in its own `AGENTS.md`? Then it is a **channel**
   rule, and each channel keeps its own.
3. Is it about what a film says, shows, sounds like or is called? Then it is a **channel** rule.

Anything left is a studio rule.

## Section by section

"Split" means the section holds both kinds. Those have a line-by-line table further down.

| Section in `AGENTS.md` | Lines | Goes to | Note |
|---|---|---|---|
| Opening: "Read this first", the hand-over pointer | 1–5 | Studio | |
| Opening: "The channel", "The job" | 7–9 | Channel | Who Orbit With Ben is and what its films are for. |
| Docs in force | 11–23 | Channel | All eight docs listed are Orbit With Ben's own, so the section went whole. `AGENTS.md` has a new short section saying which file wins. |
| Where things live | 24–44 | Split | See below. |
| Commands | 45–78 | Studio | Tools every channel uses. Three rules written as comments inside it stay with it (social copy on every package, the Sources line, a Short's swap also updates its Buffer posts): each says it holds for every channel. |
| Standing lessons | 79–115 | Split | See below. |
| Teach on screen | 116–154 | Channel | History of Science has its own section of the same name. |
| Polish pass | 155–221 | Channel | History of Science has its own. One budget line inside is out of date, see "Lines in the wrong place". |
| Reference lessons | 222–294 | Channel | History of Science has its own. Item 4, "Graphics go to Codex", is routing: it points at *Who does what* and stays readable from there. |
| Packaging | 295–328 | Channel | Titles, thumbnails, the one Short length test. |
| Topic pick, neighbour pass | 329–332 | Channel | |
| Packaging panel and the thumbnail ledger | 333–340 | Studio | The panel and the ledger are a process every channel goes through. |
| Who does what | 341–385 | Studio | Routing, Chief succession, "Quotes must be real". |
| Job queue | 386–406 | Studio | |
| Always on | 407–414 | Studio | |
| Chief relay | 415–451 | Studio | |
| Studio board and claims | 452–462 | Studio | |
| Film folders on the NAS | 463–525 | Studio | |
| How films get worked on | 526–555 | Studio | The weekly targets are each channel's own numbers, but one table holds both, so it stays for now. |
| Stop and ask Ben | 556–650 | Studio | The publish days and times are each channel's own, but each list names both channels, so they stay for now. See below. |
| Never | 651–686 | Split | See below. |
| Missing footage fallback | 687–697 | Studio | History of Science carries the same text. |
| Studio core | 698–701 | Studio | |
| Changing the rules | 702–704 | Studio | Gains one clause: a channel changes its own rules file the same way. |

By line count: 231 lines with text went to `studio/RULES.md` and 326 stayed in `AGENTS.md`.

## Where things live (lines 24–44)

| Row | Goes to |
|---|---|
| `00_Brand/Channel-Setup/` and its `tools/`, `could-orbit-survive/`, `audits/`, `social/` | Channel |
| `01_Orbit-Character/` | Channel |
| `02_Video-Projects/NNN_Slug/` | Channel (the folder layout is the same for every channel; the films are this channel's) |
| The two NAS rows (`studio-live`, `mac-mini-archive`) | Studio |
| `04_Audio/tools/` | Channel today. `orbit_voice.py` holds this channel's voice settings. |
| `05_Analytics/`, `07_Content-Ops/`, `scripts/`, `scripts/cdp_tabs.py` | Studio |
| `docs/ORBIT_PLAYBOOK_LESSONS.md` | Channel |
| `_archive/` | Studio |

## Standing lessons (lines 79–115)

| Lesson | Goes to | Note |
|---|---|---|
| 1. Neighbour | Channel | Topic method. History of Science states its own in its "Definition of done". |
| 2. Edit (v03b) | Channel | |
| 3. Production | Studio | One line holds both kinds ("Orbit = Omni only" is channel; "no media in git" and "Chief gives the final OK" are studio). It stays whole in `AGENTS.md`. |
| 4. Thread | Studio | |
| 5. Shorts feed, all nine points | Channel | The gate that enforces "every shot fills the 9:16 frame" is shared, so History of Science needs that line in its own rules too. |
| 6. YouTube state changes leave a record | Studio | |
| 7. Picture and music QA | Channel | What fails a picture or a bed is this channel's taste. Three lines inside it are not about QA at all, see next table. |

## Lines in the wrong place today

These sit inside a style section but are studio rules about money or routing. They move to the studio side with
their words and dates unchanged.

| Line | Where it sits now | Where it belongs |
|---|---|---|
| "All subscription credit floors are zero (Ben, 12 Oct 2026 14:46)" | Standing lessons 7, under Music | Stop and ask Ben, Budget |
| "ElevenLabs has no floor (Ben, 9 Oct)" | Standing lessons 7, under Music | Stop and ask Ben, Budget |
| "Standalone Shorts test + compilation film (Ben, 12 Oct 2026 14:50)" | Standing lessons 7, under Music | Channel, with the Shorts rules (it is an Orbit With Ben test) |
| "Credit hold: until the 30 Oct reset, no new bed starts without Chief's OK" | Polish pass 2 | Stop and ask Ben, Budget. The date has passed; it moves as written and is marked for the Chief to retire. |
| "Graphics go to Codex (`--kind chart`)" | Reference lessons 4 | Stays where it is, as a pointer. The rule itself is already in *Who does what*. |

## Stop and ask Ben (lines 556–650)

| Part | Goes to |
|---|---|
| "Chief owns the studio", "Ben only watches finished videos", "Ben's final watch is the watch-and-listen check" | Studio |
| Continuous flow E, F, G, H | Studio |
| Weekly publish cadence (Orbit: two longs a week, Sunday and Wednesday 18:00; History of Science: one, Thursday 18:00) | Studio for now. One line names both channels. |
| "Standing order: ask Chief first, not Ben" and the four things only Ben decides | Studio |
| "Chief owns `AGENTS.md` and the Never list" | Studio. Gains: the Chief owns each channel's rules file too. |
| Budget, the credit holds, the AI spend month | Studio |
| "Four a month on each channel" | Studio |
| "One film at a time, then Ben watches it" | Studio |
| Videos tab, how work moves, dashboard behaviours | Studio |
| Locked publish slots (the four lines of days and times) | Studio for now. One list names both channels. |
| "The real upload is the only run that passes `PUBLISHING_DRY_RUN=false`" | Studio |

## Never (lines 651–686)

| Line | Goes to | Note |
|---|---|---|
| Uploads: swap a file on an id, re-upload a public idea, delete a video, re-render over an uploaded file | Studio | History of Science has the same four. |
| Publishing: premiere a long | Channel | History of Science's version differs ("until subscribers are in the hundreds"). |
| Publishing: more than one Short a day | Studio | Same in both. |
| Publishing: a Short of 40 s or more | Studio | Same number in both. The line carries Orbit With Ben's one length-test exception and stays whole. |
| Publishing: a silent or near-silent file | Studio | Same in both. |
| Publishing: Orbit at frame 0 of a Short or on any thumbnail | Channel | |
| Subscribe asks | Channel | History of Science words its own. |
| Titles | Channel | |
| Studio: a pinned comment on a Short, a `/go/` link, and pressing Continue on "Run a new test? Your current test will be deleted" | Studio | One line. The Test & Compare part is the same in both channels and destroys a running test; the line stays whole. |
| Generation: Kling, Seedance, ElevenLabs Image & Video; Omni for the whole film | Channel | Which picture tools a channel uses. |
| Generation: anything on the ElevenLabs website | Studio | It bills the credit pool both channels share. |
| Generation: a video model's speech as voice-over | Studio | Same in both. |
| Generation: any voice other than Ben Orbit Narrator | Channel | Each channel names its voice, even while both name the same one. |
| Security, all six lines | Studio | |
| Repo: merge, close or push to a studio thread | Studio | |
| Social: Buffer mirror only, Buffer time equals go-public time, TikTok paused | Channel | History of Science words its own. |
| Secrets | Studio | |

## How films get worked on (lines 526–555)

| Part | Goes to |
|---|---|
| "Two layers decide what gets worked on" (the cap of nine, the job picker) | Studio. The split of the nine between channels stays here: it is one number shared between them. |
| "Locked weekly targets" | Studio for now. One table names both channels. |
| "Never two Shorts on the same day" | Studio (already in Never). |
| Machine split, Ben vs agents | Studio |

## What History of Science's own rules file should hold

For the job that writes it there. History of Science's `AGENTS.md` already separates most of this.

- Its sections *Definition of done*, *Teach on screen*, *Polish pass*, *Reference lessons*, *Packaging* and
  *Ben's check-in*.
- From its Never list: Channels, the publishing lines that are its own (premiere until subscribers are in the
  hundreds, the Explorer at frame 0, burned-in subscribe graphics, Made for Kids), Titles, Studio, Picture, Voice,
  TikTok and Social.
- Its publish days and times.
- "Every shot fills the 9:16 frame", which it does not state yet although the shared gate enforces it.

Its studio rules (the desk, who does what, the status board, uploads, secrets, network details, git) stay in its
`AGENTS.md` until the studio repo exists, then are read from there.

## What changed between the table and the move

One rule decided all four: **a line is never cut in two.** Each line went whole to one file, so no word could change.
A line that holds both kinds stayed in the studio file, where a studio rule can never be lost.

| Where | First version of this table | What the move did | Why |
|---|---|---|---|
| Standing lessons, 3 (Production) | cut at its semicolons | stays whole in `AGENTS.md` | It is the only place that says "no media in git". |
| Never, "Studio:" (pinned comment, `/go/` link, the Test & Compare line) | channel and studio parts apart | stays whole in `AGENTS.md` | One line; the Test & Compare part is the heavy one. |
| Never, "a Short of 40 s or more" with its one exception | exception to the channel | stays whole in `AGENTS.md` | One line. |
| Publish days and times, weekly targets | channel | stay in `AGENTS.md` | Each is one table or list that names both channels. A channel's own rows move to its own file when the studio has its own repo. |

Also: "Docs in force" went to the channel file whole (all eight docs are the channel's), and `AGENTS.md` got a new
short section saying which file wins. The out-of-date "Credit hold" line stays inside Polish pass, for the Chief to
retire. The two budget lines filed under "Music" are now under Budget in *Stop and ask Ben*.

## How the move was checked

`jobs/reviews/J2527/move.py` made both files from `AGENTS.md` on main and compared them with it, line by line:

- 557 lines with text before. 231 moved to `studio/RULES.md`. **None lost, none changed.**
- 18 lines are new: the pointers between the two files, the headings the channel file needs, and four table or
  list headers that both files need. Each is listed in the script.

## What is left of J2527

1. Done: this table.
2. Done: the move.
3. Done: `scripts/sync_rules.py` reads both files, with tests. The copies under `.cursor/rules/` and
   `STUDIO_PLAYBOOK.md` are filled from the file each marker names.
4. Start-up texts. `AGENTS.md` now says in its first screen to read `studio/RULES.md` next, so every agent that is
   told "read AGENTS.md" is led to it. `CLAUDE.md` and the Cursor rule name both files. Two live prompts still name
   only `AGENTS.md` and are changed in their own job: the relay's (`scripts/chief_relay.py`) and the MacBook
   worker's (`scripts/macbook_worker.py`).
5. History of Science's own `studio/RULES.md`: the section above says what it should hold.
