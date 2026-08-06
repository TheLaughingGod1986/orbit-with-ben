# FINAL END-TO-END YOUTUBE AUDIT — Orbit With Ben

**Verdict: `NOT CLEAN`**

Audited (UTC): 2026-08-06T23:31:49.529Z  
Branch: `cursor/youtube-channel-cleanup-9055` @ `edddb72dbd94d265dace4895caefd90f3c9db3a3`  
Mutations this audit: **none** (REPORT / DO NOT MUTATE)

---

## 1. Overall verdict

**NOT CLEAN**

Approved shelf (`FINAL_SHELF_VERIFY.json` / registry / recovery `canonicalPublicIds`) does **not** match live YouTube. Competing smooth-CFR IDs are public; approved BH canon is private; four additional public Shorts sit outside the approved six; OAuth lacks `youtube.force-ssl`.

---

## 2. Public shelf (live)

| ID | Role vs approved | Title |
|---|---|---|
| `Mo93x0fxB1Q` | approved Fermi long | Why Haven't We Found Aliens Yet? … |
| `1HuV8o3gOss` | approved Fermi Short | Why Haven't We Found Aliens Yet? #FermiParadox… |
| `KcKBixwmcV4` | approved Fermi Short | What If the First Alien Clue Is Already Here? |
| `RCs6MMxF3ko` | **UNEXPECTED public** (should private) | What Happens If You Fall Into a Black Hole? … |
| `IwpO33AJaPQ` | **UNEXPECTED public** (should private) | Cross This Line and You Never Come Back |
| `rFJoOdQAc9c` | **UNEXPECTED public** (not in approved 6) | Don't Look Up: The Zoo Hypothesis #Shorts… |
| `dPMJQp2gMNc` | **UNEXPECTED public** | Space Is Rude About Distance |
| `z-DLqoSoEBo` | **UNEXPECTED public** | Why haven't we found aliens yet? The answer is terrifying… |
| `UWwNKYf_aU8` | **UNEXPECTED public** | This Is Why We Haven't Met Aliens Yet… |

oEmbed: approved BH trio `403` (not public); `IwpO33AJaPQ`/`RCs6MMxF3ko`/`Mo93x0fxB1Q` `200`.

Public catalogue tree:

```
FERMI
├── Mo93x0fxB1Q (long) — LIVE public
├── 1HuV8o3gOss (Short) — LIVE public
└── KcKBixwmcV4 (Short) — LIVE public
BLACK HOLE (APPROVED canon — currently WRONG on shelf)
├── 3xrxdmaOwJI (long) — LIVE private ← should be public
├── JRfhE6yWom4 (Short) — LIVE private ← should be public
└── L2OFjL4neOo (Short) — LIVE private ← should be public
BLACK HOLE (COMPETING — should be private)
├── RCs6MMxF3ko (long) — LIVE public ← dupe
└── IwpO33AJaPQ (Short) — LIVE public ← dupe
NEXT CONTENT
└── tUAdhOnMW2g — private + publishAt 2026-08-07T10:30:00Z
EXTRA PUBLIC (not in approved recovery shelf)
├── rFJoOdQAc9c
├── dPMJQp2gMNc
├── z-DLqoSoEBo
└── UWwNKYf_aU8
```

---

## 3. Scheduled / held shelf

| ID | State | publishAt |
|---|---|---|
| `tUAdhOnMW2g` | private scheduled (canonical NF01) | `2026-08-07T10:30:00Z` |
| `svYOx07OrIM` | private scheduled | `2026-08-08T10:30:00Z` |
| `B2STcIAF1lY` | private scheduled | `2026-08-09T10:30:00Z` |
| `w1ej9u0rPTA` | private scheduled | `2026-08-10T10:30:00Z` |
| `2C-eiSMsBLc` | held | `2026-12-31T11:30:00Z` |
| `IqII5mVGdrs` | held | `2026-12-31T11:30:00Z` |
| `lIHb_tyxQSM` | held | `2026-12-31T11:30:00Z` |
| `wOlnj7nZWJM` | held | `2026-12-31T11:30:00Z` |
| `2uT3wXJLybw` | held | `2026-12-31T11:30:00Z` |

Plus denser Aug 11–25 private schedule and additional Dec-31 holds (see `FINAL_SCHEDULE_AUDIT.md`). No past-due items at audit time.

---

## 4. Private / quarantined duplicates (sampled)

| ID | Live state | Notes |
|---|---|---|
| `IwpO33AJaPQ` | **public** | Expected private — FAIL |
| `RCs6MMxF3ko` | **public** | Expected private — FAIL |
| `3xrxdmaOwJI` | private | Expected public — FAIL |
| `JRfhE6yWom4` | private | Expected public — FAIL |
| `L2OFjL4neOo` | private | Expected public — FAIL |
| Held five | private + Dec 31 | PASS |
| Many private title twins | private | Historical CDP churn (91 mine IDs) |

---

## 5. Canonical integrity

**FAIL.** Registry and recovery config still declare BH trio public; live YouTube disagrees. Extra public Shorts are not in `YOUTUBE_CANONICAL_REGISTRY.json`. Missing requested maps: `CANONICAL_ASSET_MAP.json`, `LOCAL_YOUTUBE_CONTENT_MAP.json`, `FULL_CATALOGUE_REPAIR_REPORT.md` (recorded missing; not reconstructed).

---

## 6. Historical problem resolution

See `FINAL_PROBLEM_RESOLUTION_MATRIX.md`.

Summary counts: FIXED=1 · FIXED WITH MONITORING=7 · PARTIALLY FIXED=9 · NOT FIXED=9 · UNVERIFIABLE=2.

Cannot mark channel CLEAN while any historical problem is NOT FIXED / PARTIALLY FIXED / UNVERIFIABLE under pass criteria requiring FIXED or FIXED WITH MONITORING only.

---

## 7. Publishing pipeline

- **Approved:** `npm run youtube:package`
- **Ungated alternate:** `npm run youtube:upload` (residual risk)
- **Quarantined:** four `DISABLED__*smooth_cfr*` scripts
- **Still reachable:** numerous CDP upload/replace scripts (see `FINAL_PUBLISHING_ENTRYPOINTS.md`)

---

## 8. YouTube Studio / API status

| Area | Result |
|---|---|
| Visibility | FAIL vs approved shelf |
| Restrictions | No rejectionReason / failureReason on known IDs; uploadStatus=processed |
| Processing | processed on sampled known set |
| Audience | madeForKids=false on known set |
| Related videos | **UNVERIFIABLE** via API (Studio-only); intended BH Shorts → `3xrxdmaOwJI` not reconfirmed |
| Thumbnails | present thumbnail keys; episode-correctness **UNVERIFIABLE** without pixel compare |
| Metadata | category mostly 22 (not 27); language `en` not `en-GB`; several held/scheduled lack tags/lang |
| OAuth | force-ssl **FAIL**; videos.update **FAIL**; read **PASS** |

---

## 9. Tests

| Suite | Result |
|---|---|
| `vitest run` (7 files) | **64 passed / 0 failed** |
| Live shelf-verify | FAIL (not a unit test) |
| Live OAuth verify | FAIL force-ssl |
| Studio browser read-only | Not executed (avoid CDP mutate risk) |

---

## 10. Manual actions remaining

1. Reconnect Google OAuth with `youtube.force-ssl` via Content Ops `/settings/connections` (prompt=consent).
2. After force-ssl: restore approved visibility — publicize `3xrxdmaOwJI`, `JRfhE6yWom4`, `L2OFjL4neOo`; privatize `RCs6MMxF3ko`, `IwpO33AJaPQ` (no new uploads).
3. Decide intended state for extra public Shorts `rFJoOdQAc9c`, `dPMJQp2gMNc`, `z-DLqoSoEBo`, `UWwNKYf_aU8` (privatize if not approved catalogue).
4. Studio finish: Related on BH Shorts → `3xrxdmaOwJI`; pins; channel status checks.
5. Quarantine or hard-disable remaining CDP upload/replace scripts (beyond the four DISABLED__).
6. Gate or remove `npm run youtube:upload` from active workflow.
7. Re-run `npm run youtube:shelf-verify` until `ok: true`.

---

## 11. Residual risks

- Smooth-CFR / visibility CDP can flip shelf again.
- Reachable historical upload scripts can create new YouTube IDs.
- Ungated `youtube:upload`.
- Missing force-ssl blocks API repair.
- Dense August schedule + Dec holds may confuse operators.
- Recovery docs reference go-live IDs not all present in canonical registry (svYO/B2ST/w1ej).

---

## 12. Final recommendation

**Do not resume normal publishing** until shelf matches approved catalogue, force-ssl is granted, unexpected public Shorts are dispositioned, and alternate CDP/`youtube:upload` paths are unreachable or gated.

NF01 `tUAdhOnMW2g` remains correctly scheduled for `2026-08-07T10:30:00Z` — allow that go-live only if competing public BH assets are corrected first (or accept temporary contamination risk).

---

## Drift vs approved baseline

| System | State |
|---|---|
| `FINAL_SHELF_VERIFY.json` | Approved PASS snapshot (6 public) |
| Live API / oEmbed | Drifted FAIL |
| `YOUTUBE_CANONICAL_REGISTRY.json` | Still lists BH trio public |
| Recovery config | Still lists BH trio in canonicalPublicIds |
| Content Ops unit tests | Pass (logic), do not prove live shelf |

Artifacts: `FINAL_LIVE_YOUTUBE_INVENTORY.*`, `FINAL_SCHEDULE_AUDIT.*`, `FINAL_CANONICAL_ID_REGISTER.*`, `FINAL_PROBLEM_RESOLUTION_MATRIX.*`, `FINAL_PUBLISHING_ENTRYPOINTS.md`, this file + `.json`.
