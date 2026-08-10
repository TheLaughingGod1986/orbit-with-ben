# Draft Delete + Private “Should Be Live” Decision

Generated: `2026-08-10T12:14:23.985477+00:00`

## What we did

Deleted **15** Studio Draft–linked historical duplicate uploads (API `videos.delete`).

Protected catalogue after deletes:
- Public canonicals: **OK** (7 including today’s `tUAdhOnMW2g`)
- Remaining scheduled: **12/12** exact
- Schedule untouched: **yes**
- Republished private→public: **0**

## Why things looked “Private” (and why we did NOT make them public)

### 1. Scheduled Shorts show as Private — this is correct

YouTube holds future releases as `privacyStatus=private` + `publishAt`.

Studio Content often labels these **Private** (or Scheduled). They go live automatically at the scheduled Paris time.

Examples still correctly private until air:
- `svYOx07OrIM` — Tue 11 Aug 12:30 Paris
- `ho9VJxp7f3A` — Thu 13 Aug 21:00 Paris
- …through `AeFm7gWyWik` — Sun 23 Aug

**Making these public now would break the approved calendar.**

### 2. Historical duplicates were switched to Private on purpose (Aug 7 cleanup)

During catalogue repair we had multiple uploads of the same Short.

Action taken then: keep **one canonical** public/scheduled, set competing copies to **private** (`KEEP_PRIVATE`).

That is why you see many private Shorts with the same titles as live/scheduled ones. They are leftovers from replace/upload cycles — not forgotten publishes.

### 3. Accidental early publishes were privatized on purpose

`dPMJQp2gMNc` and `rFJoOdQAc9c` went public too early, then were repaired to private. **Do not re-public.**

### 4. Studio “Draft” rows

Those Drafts were not empty unfinished uploads. Each mapped via `udvid=` to a **private historical duplicate** ID. Deleting them removes the duplicate upload; the real canonical (public or scheduled) stays.

## What was NOT wrongly private

Live check before/after:
- All expected public IDs are **public**
- All remaining approved schedule IDs are **private + correct publishAt**
- **Zero** “should already be live” canonicals were stuck private

So there was nothing to “fix” by flipping Private→Public.

## Deleted draft duplicate IDs

- `z-kgwJaz5pY`
- `Cw-tfP1QnBE`
- `trrKgW7m_98`
- `ItuOwgTvS1Y`
- `slCssHVBOz0`
- `4dGXJt9dElk`
- `lUvMhe1BWJM`
- `B95wuAH68QY`
- `IvSMHnngXdE`
- `6dSntxIQgXI`
- `dFO50RT5s14`
- `J_uLnRIwqu0`
- `zc79sRBCDnU`
- `z8-haBeF6mI`
- `RF6wivuPYqI`

## Recommendation

- Let the schedule publish on its own (next: `svYOx07OrIM` tomorrow)
- Leave remaining private historical copies private unless you explicitly approve another delete batch
- Do not publicize excluded/private accidentals

## Verdict

```text
DRAFTS DELETED — SCHEDULED PRIVATES LEFT CORRECTLY PRIVATE
```
