# Splitting the rule book: studio rules and channel rules

Step 1 of J2527. Written 11 Nov 2026 against `AGENTS.md` as it stood that morning (704 lines). **Nothing has moved
yet.** This table is here to be read and corrected first. The move itself is the next pull request.

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
| Docs in force | 11–23 | Split | The rule "the higher doc wins, `_archive/` is history" is studio. The eight docs listed are all Orbit With Ben's own. |
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
| How films get worked on | 526–555 | Split | The production cap, the job picker, the machine split and "Ben only does UAT" are studio. The weekly targets are each channel's own numbers. |
| Stop and ask Ben | 556–650 | Split | Nearly all studio. The publish days and times are each channel's own. See below. |
| Never | 651–686 | Split | See below. |
| Missing footage fallback | 687–697 | Studio | History of Science carries the same text. |
| Studio core | 698–701 | Studio | |
| Changing the rules | 702–704 | Studio | Gains one clause: a channel changes its own rules file the same way. |

By line count: about 240 lines are Orbit With Ben's own and about 460 are the studio's.

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
| 3. Production | Both | One line holds both kinds. "Orbit = Omni only", "no Orbit on long thumbs", "verify NASA IDs" are channel. "No media in git" and "Chief gives the final OK" are studio. The line is cut at its semicolons; no word changes. |
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
| Weekly publish cadence (Orbit: two longs a week, Sunday and Wednesday 18:00; History of Science: one, Thursday 18:00) | Channel. Each channel states its own days. The studio keeps one line: every channel has a locked cadence in its rules. |
| "Standing order: ask Chief first, not Ben" and the four things only Ben decides | Studio |
| "Chief owns `AGENTS.md` and the Never list" | Studio. Gains: the Chief owns each channel's rules file too. |
| Budget, the credit holds, the AI spend month | Studio |
| "Four a month on each channel" | Studio |
| "One film at a time, then Ben watches it" | Studio |
| Videos tab, how work moves, dashboard behaviours | Studio |
| Locked publish slots (the four lines of days and times) | Channel, with the cadence above |
| "The real upload is the only run that passes `PUBLISHING_DRY_RUN=false`" | Studio |

## Never (lines 651–686)

| Line | Goes to | Note |
|---|---|---|
| Uploads: swap a file on an id, re-upload a public idea, delete a video, re-render over an uploaded file | Studio | History of Science has the same four. |
| Publishing: premiere a long | Channel | History of Science's version differs ("until subscribers are in the hundreds"). |
| Publishing: more than one Short a day | Studio | Same in both. |
| Publishing: a Short of 40 s or more | Studio | Same number in both. The one 50–60 s length-test exception is Orbit With Ben's and goes with its Packaging section. |
| Publishing: a silent or near-silent file | Studio | Same in both. |
| Publishing: Orbit at frame 0 of a Short or on any thumbnail | Channel | |
| Subscribe asks | Channel | History of Science words its own. |
| Titles | Channel | |
| Studio: a pinned comment on a Short, a `/go/` link | Channel | History of Science words its own. |
| Studio: pressing Continue on "Run a new test? Your current test will be deleted" | Studio | Same in both; it destroys a running test. |
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
| "Locked weekly targets" | Channel. Each channel's own count of longs and Shorts. |
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

## What happens next

1. This table is read. A row that is wrong is changed here first.
2. The move: the channel rows go to `studio/RULES.md` word for word, with every quote of Ben and every date.
   `AGENTS.md` keeps the studio rows and names the channel file. A check compares the two files with the old
   `AGENTS.md` and fails if a line was lost or changed.
3. `scripts/sync_rules.py` reads both files, with tests, so the copies under `.cursor/rules/` and
   `STUDIO_PLAYBOOK.md` keep working.
4. Every start-up text that says "read AGENTS.md" also names the channel's rules file for the job's channel.
