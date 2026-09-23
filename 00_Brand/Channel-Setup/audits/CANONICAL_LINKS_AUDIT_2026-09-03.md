# Canonical links / IDs audit — 3 Sep 2026

Not content canons. This is **YouTube IDs**, Related pills, and `watch?v=` URLs.

Probed via oEmbed at 2026-09-03 (Europe/London). **200** = public/listed title confirmed. **403** = ID exists but is private/scheduled (expected for tonight’s Shorts). **404** = bad ID.

## Parent longs (these are the only Related targets)

| Channel | Title | ID | Canonical URL | oEmbed |
|---------|-------|----|---------------|--------|
| `@OrbitWithBen` | Could Life Exist Under The Ice Of Europa? | `NbW5G1BpPY0` | `https://www.youtube.com/watch?v=NbW5G1BpPY0` | 200 · title match |
| `@OrbitWithBen` | What Happens to Your Body Near a Neutron Star? | `Yk1tLh23rko` | `https://www.youtube.com/watch?v=Yk1tLh23rko` | 200 · title match |
| `@OrbitWithBen` | What Happens When the Last Star Dies? | `REXYxuLOBoI` (**letter O**, not zero) | `https://www.youtube.com/watch?v=REXYxuLOBoI` | 200 · title still has `\| Orbit's Cosmic Journey` |
| `@HistoryOfScienceYT` | How Did We Discover Germs? | `_C92tIJCk8A` | `https://www.youtube.com/watch?v=_C92tIJCk8A` | 200 · History of Science |

Typo trap: `REXYxuL0BoI` (zero) → **404**. Do not use.

Do **not** mix channels. HOS Shorts never Related → Orbit IDs. Orbit Shorts never Related → `_C92tIJCk8A`.

## Europa Shorts — IDs correct in git

Every live Europa Short in `SHORTS_UPLOAD_INDEX.json` / `EUROPA_SHORTS_CLUSTER_v01.json` has:

- `related`: `NbW5G1BpPY0`
- description `watch?v=`: `https://www.youtube.com/watch?v=NbW5G1BpPY0`
- `affiliate`: false (zero `/go/`)

| Slot UK | Title | Short ID | Related | oEmbed |
|---------|-------|----------|---------|--------|
| Thu 3 11:30 | There's an Ocean Under That Ice | `QNTeou-w-gY` | `NbW5G1BpPY0` | 403 scheduled |
| Thu 3 **20:00** | Those Ice Scars Are How You Find It | `keXe1GNxWSU` | `NbW5G1BpPY0` | 403 scheduled |
| Fri 4 11:30 | Europa's Hidden Ocean Is Bigger Than Earth's | `g0ZqPP3nR5U` | `NbW5G1BpPY0` | 403 scheduled |
| Sat 5 11:30 | The Dive Under Europa's Ice | `uYL9DMGoDjk` | `NbW5G1BpPY0` | 403 scheduled |
| Sun 6 11:30 | How We'd Know Europa Is Alive | `38acs_fCCvc` | `NbW5G1BpPY0` | 403 scheduled |
| Mon 7 11:30 | Salt and Plumes Are Fingerprints | `34v3leUHzi0` | `NbW5G1BpPY0` | 403 scheduled |
| Tue 8 11:30 | Clipper Goes to Look | `L_nUSC5ObNk` | `NbW5G1BpPY0` | 403 scheduled |
| Wed 9 11:30 | Closer Is Not Certain | **no ID** | `NbW5G1BpPY0` (template) | not uploaded |

No Europa Short points at Last Star (`REXYxuLOBoI`) or Neutron (`Yk1tLh23rko`). That part of git is correct.

**Studio gap:** Related pills are Studio-only. Git templates ≠ the live pill until each video is checked. The **20:00** slot for `keXe1GNxWSU` is written in git; it was **not** confirmed Saved in Studio from this agent (CDP `:9222` down).

## HOS 001 Shorts — IDs correct in git + Studio result

Parent: `_C92tIJCk8A`. Studio cover/Related pass (`PACKAGE_COVER_RELATED_RESULT_2026-09-02.json`) marked `relatedApplied: true` on all five.

| Slot UK | Title | Short ID | Related | oEmbed |
|---------|-------|----------|---------|--------|
| Fri 4 11:30 | Germs don't cast a shadow | `8uBR-9oxeWs` | `_C92tIJCk8A` | 403 scheduled |
| Sat 5 11:30 | Microbes in a drop of pond water | `YX2UR1u-JCQ` | `_C92tIJCk8A` | 403 scheduled |
| Sun 6 11:30 | Germs hitch a ride on you | `Fnb3p81u-wY` | `_C92tIJCk8A` | 403 scheduled |
| Mon 7 11:30 | A flask that proved germs come from outside | `vpuRgKXtFlY` | `_C92tIJCk8A` | 403 scheduled |
| Tue 8 11:30 | Invisible life is still everywhere | `Lcmh5y2KMQM` | `_C92tIJCk8A` | 403 scheduled |

Zero `/go/`. Not Orbit. No Thursday 20:00 Short (HOS cadence: long first).

## Last Star Shorts — Related IDs correct; two FAIL IDs still public

All Related + `watch?v=` → `REXYxuLOBoI`.

Public keepers (oEmbed 200, `@OrbitWithBen`): `PV50PX-bE4g` · `DN4L1DkerMM` · `wIh3armF7_k` · `9lLZMy8rBJo` · `n2WbOfJhOwc`.

Still public, marked `public_pending_unpublish`: `CkSECfUfH2Y` · `KX-XU_AODoI`. Related ID is still the right long, but they should not stay in the funnel.

## Neutron Star — long ID correct; Shorts IDs missing

Long `Yk1tLh23rko` is the right parent (oEmbed 200).

There is **no** `10_Shorts/SHORTS_UPLOAD_INDEX.json`. Cluster seeds have titles only. Studio already shows Neutron Shorts (from the Scheduled screenshot) but **live Short IDs are not in git**, so Related/`watch?v=` cannot be audited from the repo.

For 10 Sep success, every Neutron Short must Related + description URL → `Yk1tLh23rko` (not Europa). Launch Short = teaspoon gold beat at **Thu 10 Sep 20:00**.

## Affiliate doors (canonical `/go/` URLs)

Shorts: **zero** `/go/` — Europa + HOS listings match.

Long `/go/europa-icy-moons-book` only if **this** Europa cut names *Alien Oceans* (Kevin Hand) in VO or on screen. No “Alien Oceans” string in the Europa project files in this clone — **do not bolt it on**. Base if ever used: `https://orbit-content-ops.vercel.app/go/{slug}` only. Neutron: no `/go/` unless that cut names a product.

## Verdict

**The IDs we have are the right IDs.** Parent longs match oEmbed titles and channels. Last Star is letter **O**. Europa and HOS Shorts in git all point at the correct parent. Scheduled Short IDs exist (403, not 404).

**Not yet set up for success:**

1. Studio Save for Europa **20:00** `keXe1GNxWSU` (unconfirmed).
2. Studio Related pill check on each Europa Short (git cannot see pills).
3. Neutron Shorts: write live IDs + Related `Yk1tLh23rko`; move launch Short to 10 Sep 20:00.
4. Europa punch-08 has no YouTube ID (Wed 9 Sep 11:30 empty unless built).
5. Unpublish Last Star FAIL shorts `CkSECfUfH2Y` and `KX-XU_AODoI`.
6. Long end screen on Europa → next film `Yk1tLh23rko` (Studio, not git).
