# Schedule + /go/ scrub — 2026-10-01

## 1. CtllH6VOhEI publishAt

| Field | Value |
|---|---|
| id | `CtllH6VOhEI` |
| title | What Happens When Galaxies Actually Collide? |
| privacy | `private` |
| publishAt (API) | `2026-10-01T10:30:00Z` (= **11:30 London BST**) |
| before fix | `private`, `publishAt: null` |
| k9pXeeJvLpc | left `private`, `publishAt: null` (untouched) |

Proof: `CTLL_PUBLISHAT.json`.

## 2. After 11:30 — public + register

Pending until air time. Will download mp4 (no local file on disk) then:

```bash
npx tsx --env-file=.env scripts/buffer-mirror.ts register \
  --video CtllH6VOhEI \
  --media <mp4> \
  --long ojk-dfOpAmw
```

## 3. /go/ links on live descriptions

Scanned all 122 channel uploads. Only two public descriptions contain `/go/` URLs:

| video | title | url | HTTP | removed |
|---|---|---|---:|---|
| `NbW5G1BpPY0` | Could Life Exist Under The Ice Of Europa? | `https://orbit-content-ops.vercel.app/go/europa-icy-moons-book` | 200 | no (live) |
| `REXYxuLOBoI` | What Happens When the Last Star Dies? | `https://orbit-content-ops.vercel.app/go/cosmology-end-book` | 200 | no (live) |

Digest 404s checked separately (not present in any video description):

| slug | HTTP | in any description? |
|---|---:|---|
| `/go/andromeda-book` | 404 | **no** |
| `/go/saturn-rings-book` | 404 | **no** |

No description edits required. Affiliate `/go/` stays paused for new books; no new book links set up.
