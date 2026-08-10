# Root Cause Analysis — Shorts Visibility / Drafts

Generated: `2026-08-10T12:25:00Z`  
Mode: forensic (read-only for this repair pass)

## Question 1 — Why did prior tooling say “True Studio drafts: 0”?

### Verdict

```text
RECONCILIATION_BUG
```

More precisely:

```text
WRONG_STUDIO_TAB_FILTER
```

### Evidence

| Check | Result |
|---|---|
| Content → **Videos** `/videos/upload` · Visibility: Draft | Empty (“No matching videos”) |
| Content → **Shorts** `/videos/short` · Visibility: Draft | Had rows (before 2026-08-10 draft cleanup) |
| YouTube Data API `privacyStatus` | Only `public` / `private` / `unlisted` — **no `draft` enum** |
| Draft edit URLs | Often use `?udvid=VIDEO_ID` pointing at existing private uploads |

Commits / artifacts:

- `00_Brand/Channel-Setup/audits/shorts_forensic_reconciliation_2026-08-10/AUDIT_FAILURE_ROOT_CAUSE.md`
- Fix module: `07_Content-Ops/src/lib/publishing/youtube-studio-visibility.ts`
- Tests: `07_Content-Ops/tests/youtube-studio-visibility.test.ts`

Previous draft/orphan Playwright work filtered **Videos**, not **Shorts**, so it falsely concluded Drafts = 0.

### What those Draft rows actually were

After opening Edit draft, each row resolved to an existing **private historical duplicate** via `udvid=`. They were not empty unfinished uploads lacking catalogue IDs.

User-approved cleanup on 2026-08-10 deleted **22** such Draft-linked duplicate IDs. Studio Draft filter is now empty (verified this repair: `DRAFT: 0` of 62 Shorts).

---

## Question 2 — Why are so many Shorts Private? Did overdue canonicals fail to publish?

### Verdict for overdue canonical publication

```text
NO_OVERDUE_CANONICAL_FAILURE
```

Authoritative approved calendar (post 16→13) expects **exactly 5 Shorts public by now**:

| ID | Intended | Actual |
|---|---|---|
| `1HuV8o3gOss` | PUBLIC | public |
| `KcKBixwmcV4` | PUBLIC | public |
| `JRfhE6yWom4` | PUBLIC | public |
| `L2OFjL4neOo` | PUBLIC | public |
| `tUAdhOnMW2g` | PUBLIC (slot 2026-08-10T10:30:00Z) | public (natural publish) |

**expected_public_by_now = 5 · correctly_public = 5 · overdue = 0 · missing = 0**

Future Shorts correctly remain `private + publishAt` (Studio may label Private or Scheduled).

### Why other Shorts are Private (intentional)

| Class | Cause |
|---|---|
| Historical duplicates | Aug 7 catalogue repair privatized competing uploads (`KEEP_PRIVATE`) so one canonical wins |
| 16→13 exclusions | `w1ej9u0rPTA`, `gPCpMsB0w2E`, `YsyPMhNmHMk` removed from approved schedule — stay private |
| Accidental early | `dPMJQp2gMNc`, `rFJoOdQAc9c` intentionally privatized — must not re-public |
| Studio Private filter | Includes scheduled holds (`privacyStatus=private`) — looks like “private leftovers” |

### Was canonical visibility incorrectly flipped to private by recent scripts?

Searched schedule repair / reconcile / cleanup paths: mutations targeted **duplicate / excluded** IDs and schedule `publishAt` on the approved 13 — not demoting the five public Shorts.

Live API confirms the five approved public Shorts remain `public` with `publishAt=null`.

No evidence of a script that set **canonical public Shorts** to private after they were live.

---

## Combined root-cause summary

| Issue | Root cause code | Status |
|---|---|---|
| False “Drafts = 0” | `WRONG_STUDIO_TAB_FILTER` | Fixed in tooling + tests; Drafts cleaned 2026-08-10 |
| Many Private Shorts | `SUPERSEDED_UPLOAD` / intentional `KEEP_PRIVATE` / schedule holds | Expected |
| Overdue canonical stuck private | N/A — **none found** | Healthy |

```text
UPLOAD_DEFAULT_PRIVATE — N/A for overdue case
SCHEDULE_NOT_APPLIED — N/A (future slots have publishAt)
RECONCILIATION_BUG — YES for Draft enumeration only
CANONICAL_ID_MISMATCH — not found for public set
MANUAL_STUDIO_CHANGE — not required to explain current public set
SUPERSEDED_UPLOAD — YES explains private clutter
UNKNOWN — remaining unregistered privates kept as INVESTIGATE/KEEP
```
