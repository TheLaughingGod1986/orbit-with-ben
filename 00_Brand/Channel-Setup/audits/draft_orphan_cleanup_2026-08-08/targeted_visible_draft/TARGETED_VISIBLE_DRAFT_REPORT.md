# Targeted Visible Draft Investigation

Generated: `2026-08-08T21:48:00Z`  
Mode: **READ-ONLY** · No deletions · No metadata/schedule mutations

## Final verdict

```text
VISIBLE ITEM PROTECTED — KEEP
```

## 1. Exact Studio item

The Content list (Orbit with Ben) shows **no rows under Visibility: Draft** (“No matching videos”).

The item that visually appears as the top private leftover (after scheduled longs) is:

| Field | Value |
|---|---|
| Title | What Happens If You Fall Into a Black Hole? Orbit's Cosmic Journey |
| Duration | 21:13 (`PT21M13S`) |
| Studio status | Processed / uploaded video |
| Visibility label | **Private** (not Draft) |
| Studio Draft label | **No** |
| URL | `https://studio.youtube.com/video/RCs6MMxF3ko/edit` |
| Video ID | `RCs6MMxF3ko` |
| publishAt | `null` (not scheduled) |
| Upload/processing | `uploadStatus=processed` |
| Opens edit screen | Yes |
| Analytics/history | Edit page has Analytics nav; API views=`0`, comments=`0` |
| Approximate upload date | `2026-08-06T22:35:03Z` (publishedAt / upload timestamp) |

Content-table order observed:

1. `tfTkMdE7qqw` — Scheduled (JWST long)  
2. `b8-X_FyJnHM` — Scheduled (Exo long)  
3. **`RCs6MMxF3ko` — Private** ← investigated leftover  
4. `3xrxdmaOwJI` — Public canonical BH long (same title + duration)  
5. `1wxUhF3XnwI` — Private (dead JWST parent)  
6. `n7CbJrOCnU0` — Private (older BH long variant)  
7. `Mo93x0fxB1Q` — Public Fermi long  

## 2. Video ID / draft identifier

- YouTube ID: **`RCs6MMxF3ko`**
- Not a Studio Draft (no draft-only ID). Drafts filter returned zero matching videos.

## 3. Current state

- Privacy: **private**
- Scheduled: **no**
- Public: **no**
- Canonical: **no** (canonical is `3xrxdmaOwJI`)

## 4. Local / registry matches

| Source | Match |
|---|---|
| `YOUTUBE_CANONICAL_REGISTRY.json` | Listed under `historicalDuplicateIds` of `3xrxdmaOwJI` (`v002-bh-long`, BLACK_HOLE) |
| `STUDIO_DUPLICATE_CLASSIFICATION.json` | `EXACT_DUPLICATE` of `3xrxdmaOwJI` · action `KEEP_PRIVATE` |
| Stage A `DRAFT_CLEANUP_BEFORE.json` | `HISTORICAL_DUPLICATE_PROTECTED` |
| Canonical public twin | `3xrxdmaOwJI` — same title, same duration `PT21M13S`, public |
| Content Ops / manifests | Referenced across recovery/forensic audits (94 repo paths mention the ID) |

## 5. References found

- Registry historical duplicate of public BH long: **yes**
- Active schedule: **no**
- Future release plan as canonical: **no**
- Playlist membership (Stage A): **none**
- Related-video target: **no**
- End-screen target: **no** (end screens use `3xrxdmaOwJI` / `Mo93x0fxB1Q`, not this ID)
- Historical duplicate registry: **yes**

## 6. Classification

```text
HISTORICAL_DUPLICATE_PROTECTED
```

Not `GENUINE_ABANDONED_DRAFT` because:

1. Studio does **not** label it Draft — label is **Private**.
2. It is a fully processed upload with a stable video ID.
3. It is explicitly registered as a historical duplicate of the healthy public canonical.
4. Prior forensic classification already required `KEEP_PRIVATE`.

## 7. Evidence

- API: private · publishAt null · processed · duration match to canonical  
- Studio edit: Visibility = Private  
- Drafts filter: empty  
- Registry + duplicate classification + Stage A inventory  

## 8. Safe to delete

**NO**

## 9. Screenshot paths

Under `00_Brand/Channel-Setup/audits/draft_orphan_cleanup_2026-08-08/targeted_visible_draft/`:

- `visible_draft_overview.png` — Content page overview  
- `visible_draft_details.png` — Edit details for `RCs6MMxF3ko`  
- `drafts_filter_check.png` — Visibility: Draft → no matching videos  
- `private_filter_overview.png` — Private filter context  
- `shorts_tab_overview.png` — Shorts tab check  

Machine-readable:

- `PHASE1_STUDIO_CAPTURE.json`
- `PHASE2_CROSSCHECK.json`
- `content_rows_raw.json`

## 10. Final recommendation

**Keep `RCs6MMxF3ko` private.** It is the smooth-CFR competing BH long duplicate of public `3xrxdmaOwJI`, held for forensic / anti-reupload purposes.

Do not delete. Do not change visibility, schedule, titles, or thumbnails.

If a different Studio row was meant (e.g. `1wxUhF3XnwI` or `n7CbJrOCnU0`), say which title/ID — both are also private protected leftovers, not Drafts.

## Protected state (before & after investigation)

| Check | Result |
|---|---|
| Public canonicals | 6/6 |
| Scheduled | 13/13 |
| Unexpected public | 0 |
| Missing scheduled | 0 |
| Schedule diff | [] |
| New video IDs | 0 |
| Mutations | 0 |

## Verdict (exact)

```text
VISIBLE ITEM PROTECTED — KEEP
```
