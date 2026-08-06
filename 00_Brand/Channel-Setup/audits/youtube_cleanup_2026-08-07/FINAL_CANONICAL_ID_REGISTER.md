# FINAL CANONICAL ID REGISTER

Audited (UTC): 2026-08-06T23:31:49.529Z

Rule: **ONE CONTENT ITEM = ONE CANONICAL YOUTUBE VIDEO ID**

Integrity OK: `False`

Missing baseline files (not invented): CANONICAL_ASSET_MAP.json, LOCAL_YOUTUBE_CONTENT_MAP.json, FULL_CATALOGUE_REPAIR_REPORT.md

Closest substitute used: `00_Brand/Channel-Setup/YOUTUBE_CANONICAL_REGISTRY.json`

| Content ID | Family | Type | Canonical YouTube ID | Current state | Intended state | Historical duplicates | Schedule | Verification |
|---|---|---|---|---|---|---|---|---|
| v001-fermi-long | FERMI | longform | `Mo93x0fxB1Q` | public | public | (none) | — | PASS |
| v001-fermi-short-01 | FERMI | shorts | `1HuV8o3gOss` | public | public | (none) | — | PASS |
| v001-fermi-short-02 | FERMI | shorts | `KcKBixwmcV4` | public | public | zc79sRBCDnU, --CxhjNqtSY | — | PASS |
| v002-bh-long | BLACK_HOLE | longform | `3xrxdmaOwJI` | private | public | RCs6MMxF3ko, n7CbJrOCnU0 | — | FAIL |
| v002-bh-short-01 | BLACK_HOLE | shorts | `JRfhE6yWom4` | private | public | IwpO33AJaPQ, kv1Yz74_S10, 2777WlMGM8M, eZGAhF8dN7w, RF6wivuPYqI, P95alanW8GU | — | FAIL |
| v002-bh-short-02 | BLACK_HOLE | shorts | `L2OFjL4neOo` | private | public | IqII5mVGdrs, z-kgwJaz5pY, jyzrl9ueKq4, C4GuFEFGySI, xhBR-ixXi8s | — | FAIL |
| v002-bh-nf01 | BLACK_HOLE | shorts | `tUAdhOnMW2g` | private+2026-08-07T10:30:00Z | private+publishAt | 2C-eiSMsBLc, EO-44QH4glI | 2026-08-07T10:30:00Z | PASS |
| v002-bh-nf02-look-back | BLACK_HOLE | shorts | `svYOx07OrIM` | private+2026-08-08T10:30:00Z | private+publishAt | lIHb_tyxQSM, t1hTGIH8O44, 80S5E-AWFhA | 2026-08-08T10:30:00Z | PASS |
| v002-bh-nf03-what-you-see | BLACK_HOLE | shorts | `B2STcIAF1lY` | private+2026-08-09T10:30:00Z | private+publishAt | wOlnj7nZWJM, nX84ileqPKw | 2026-08-09T10:30:00Z | PASS |
| v002-bh-nf04-point-of-no-return | BLACK_HOLE | shorts | `w1ej9u0rPTA` | private+2026-08-10T10:30:00Z | private+publishAt | 2uT3wXJLybw, 5jjJ5CHrbCs, 5nMieBeymKU | 2026-08-10T10:30:00Z | PASS |

## Approved vs live public

- Approved public: `Mo93x0fxB1Q`, `1HuV8o3gOss`, `KcKBixwmcV4`, `3xrxdmaOwJI`, `JRfhE6yWom4`, `L2OFjL4neOo`
- Live public: `1HuV8o3gOss`, `IwpO33AJaPQ`, `KcKBixwmcV4`, `Mo93x0fxB1Q`, `RCs6MMxF3ko`, `UWwNKYf_aU8`, `dPMJQp2gMNc`, `rFJoOdQAc9c`, `z-DLqoSoEBo`
- Unexpected public: `IwpO33AJaPQ`, `RCs6MMxF3ko`, `UWwNKYf_aU8`, `dPMJQp2gMNc`, `rFJoOdQAc9c`, `z-DLqoSoEBo`
- Missing approved public: `3xrxdmaOwJI`, `JRfhE6yWom4`, `L2OFjL4neOo`

## Privatized duplicates (expected private)

- `IwpO33AJaPQ` → **public** (intended private)
- `RCs6MMxF3ko` → **public** (intended private)

## Held assets

- `2C-eiSMsBLc` → privacy=private publishAt=2026-12-31T11:30:00Z
- `IqII5mVGdrs` → privacy=private publishAt=2026-12-31T11:30:00Z
- `lIHb_tyxQSM` → privacy=private publishAt=2026-12-31T11:30:00Z
- `wOlnj7nZWJM` → privacy=private publishAt=2026-12-31T11:30:00Z
- `2uT3wXJLybw` → privacy=private publishAt=2026-12-31T11:30:00Z