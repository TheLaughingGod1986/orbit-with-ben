# J0277 — Orbit rebuild of the three B candidates

Cursor covering, 15 October 2026. Codex was out of usage, so this job ran on Cursor.

**15 Oct reopen:** Chief kept Fermi and Europa v02 and asked for them to be armed. Both are thumbnail-only tests, titles unchanged, both videos still Public.

| Test | Video | State |
|---|---|---|
| T005 | `Mo93x0fxB1Q` | Running. A is the live SILENCE thumb. B is `fermi_B_v02.jpg` (ALIENS HIDING?). |
| T006 | `NbW5G1BpPY0` | Running. A is the live A HIDDEN OCEAN thumb. B is `europa_B_v02.jpg`. |
| T007 | `ziKBPJ6FY0U` | Running. A is the live TOO EARLY? thumb. B is `jwst_B_v03.jpg` (GALAXIES TOO SOON?). |

Studio confirmed all three reports as "Test running…" with about 14 days left. No title, privacy, or schedule change.

## What changed from J0271 v01

Same hooks Chief already kept: **ALIENS HIDING?**, **A HIDDEN OCEAN**, **GALAXIES TOO SOON?**. Orbit is in each frame, with a readable face (worried on Fermi, surprised at the ocean, wide-eyed at the field). The no-Orbit rule stays waived for these OWB thumbs under the 15 Oct ruling.

| Video | Fix | B file | 168 px sheet |
|---|---|---|---|
| `Mo93x0fxB1Q` | Whole Earth globe, lower limb in frame | `fermi_B_v02.jpg` | `fermi_AB_v02.jpg` |
| `NbW5G1BpPY0` | Cutaway kept; Orbit added | `europa_B_v02.jpg` | `europa_AB_v02.jpg` |
| `ziKBPJ6FY0U` | Webb deep field, gold craft, surprised Orbit | `jwst_B_v03.jpg` | `jwst_AB_v03.jpg` |

Files live in `/Users/benjaminoats/_desk/J0277-thumbnails/`. Images are not in git. The type and shadow lift are `j0277_build.py`.

## Checks

`thumb_preview.py long <B> --out score_sheet.jpg --score` exit 0:

```
PASS  fermi_B_v02.jpg  saturation=163.2  near_black=4%
PASS  europa_B_v02.jpg  saturation=137.3  near_black=3%
PASS  jwst_B_v02.jpg  saturation=132.5  near_black=7%
```

Each file is RGB 1280×720 and under 2 MB. Hook text is top-left, white plus one yellow word, clear of the bottom-right duration badge. At 168×94 the words and Orbit's face both read.

## JWST v03 (Chief fix, 15 Oct)

v02's field still read as a generic star streak. v03 keeps the gold JWST craft, Orbit, and **GALAXIES TOO SOON?**, and replaces the background with a Webb deep-field look: a dense field of small galaxies, curved lensing arcs, and foreground stars with six-point spikes. Orbit's face is surprised (wide eyes, small open mouth).

`thumb_preview.py long jwst_B_v03.jpg --score`:

```
PASS  jwst_B_v03.jpg  saturation=170.1  near_black=5%
```

168 px sheet: `/Users/benjaminoats/_desk/J0277-thumbnails/jwst_AB_v03.jpg`. Hook text is house type over the plate, top-left, clear of the duration badge. Orbit's face still reads at 168×94.

Chief KEEP on v03 (15 Oct). T007 armed the same day: thumbnail only, title unchanged, video still Public. Studio report after reload: "Test running…", about 14 days left. A is the live TOO EARLY? plate. B is GALAXIES TOO SOON? with the Webb deep field, the gold craft, and surprised Orbit.
