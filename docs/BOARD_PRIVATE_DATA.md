# The board reads its data through its own server (J2532)

The studio repo will be private (Ben, 10 Nov 2026; `docs/MULTI_CHANNEL_PLAN.md`, decision 8). The board's pages used
to read their data straight from GitHub's public file addresses, and from a private repo those addresses answer
nothing. Since J2532 every read goes through one function on the board's own site, `api/data.js`, which reads GitHub
with the server's token.

It ships before the move and changes nothing while the repo is public.

## What the pages read

| Page | What | Before | Now | How often |
|---|---|---|---|---|
| Studio (`/`), AI (`/ai`), Tracker (`/tracker`) | which commit the `board-data` branch is on | `/api/ref`, then GitHub's API | `/api/data?f=ref` | once a minute while the page is open |
| Studio, AI | `board.json` at that commit | GitHub's public file address | `/api/data?f=board&sha=<commit>` | only when the commit has changed |
| Tracker | `tracker.json` at that commit | GitHub's public file address | `/api/data?f=tracker&sha=<commit>` | only when the commit has changed |
| Studio | the MacBook's `heartbeat.json` | GitHub's public file address | `/api/data?f=macbook` | with each new `board.json` |

Nothing else on the pages reads GitHub. The old addresses stay in the pages as a fallback for when the function
cannot be reached. They only work while the repo is public, and a page never falls back to them after a 401.
`/api/ref` is left in place for pages a phone still has cached from before.

## Who may read

- **While the data's repo is public:** anyone, as today.
- **Once it is private:** only a signed-in viewer, which means Ben's cookie or his board key (`benauth.js`). Anyone
  else gets 401, and each page shows one line: "This board is private. Open your board link on this device to sign
  in, then come back to this page." Without this rule the site would publish what the repo hides.
- **How "public" is decided:** by the function itself, not by a setting that could be forgotten at the move. GitHub's
  public file address must answer for the board's own file with no token. If that cannot be confirmed, the data
  counts as private. `BOARD_PRIVATE=1` in the site's settings forces private, to try it before the move.
- A private answer is marked so that no shared cache keeps it for another viewer.

## What it costs

Measured on 11 Nov 2026: `board.json` is 1.99 MB and travels as about 253 KB; `tracker.json` is 108 KB and travels as
about 18 KB.

| Case | Requests to the site | Data sent |
|---|---|---|
| The board open for an hour a day (likely) | about 180 a day, 5,400 a month | about 15 MB a day, 0.5 GB a month |
| One page left open round the clock with a new board every minute (worst) | 4,320 a day, about 130,000 a month | about 364 MB a day, 11 GB a month |

Both are for a private repo, where every request reaches the function. While the repo is public the site's shared
cache answers most of them, so the real numbers today are lower.

How the cost is kept down:
- The function holds a copy: the branch's commit for 20 seconds, a branch file for 45 seconds, and a file at a commit
  until the function sleeps. Twenty-five rounds of requests in a row cost three GitHub reads (tested).
- A page that already has the current copy is told "not changed" (304) and nothing is sent.
- A file is only read at the commit the branch is on. A request that names any other commit gets the current one and
  is not kept, so invented commits cannot spend the token's allowance.
- GitHub sees at most about 320 reads an hour from one running copy of the function. A token is allowed 5,000 an hour.

**The free plan of the host.** The worst case above is far below what I understand the host's free plan to include
(about a million function requests and 100 GB of data a month). I could not read the plan's current figures in the
session that wrote this, so check the project's Usage page in Vercel after the first week on the private repo and
compare it with the table. The likely case is under one per cent of either figure.

## Ben's step at the move

The server's token (`BOARD_GH_TOKEN`) can only comment today. Reading a private repo needs read access to its files.
Do this once, when the `studio` repo exists. Never paste the token anywhere but Vercel's own field.

1. GitHub: Settings, Developer settings, Personal access tokens, Fine-grained tokens. Open the board's token.
2. **Repository access:** add the `studio` repo to the selected repositories.
3. **Repository permissions:** set **Contents** to **Read-only**. Metadata is set to Read-only with it. Leave
   **Issues** on Read and write: the board posts your ticks with it.
4. Save. If GitHub shows a new token value, put it in Vercel: project `studio-kanban`, Settings, Environment
   Variables, `BOARD_GH_TOKEN`.
5. In the same place add `BOARD_DATA_REPO` with the value `TheLaughingGod1986/studio`, then redeploy.

If the token turns out to be the older "classic" kind, replace it with a fine-grained one set up as above. A classic
token can only read a private repo with the `repo` scope, which also lets it write to every repo you own.

## Left for the move

- The Tracker page carries a copy of the daily channel snapshot built into the page itself, so it opens with no
  network. That copy is public with the page. It holds the channels' public YouTube numbers. At the move, build the
  page without it if the snapshot should be private too.
- `api/checks.js` and `api/watch.js` already read and write with the server's token and are not changed here.

## Tests

`scripts/test_board_data_api.py` holds `api/data.js` to all of the above, and opens the three built pages in a real
browser with GitHub's public addresses blocked (`scripts/board_data_browser_check.cjs`): signed in and private, every
page loads its data; not signed in and private, every page shows the sign-in line; public and not signed in, the
board works as before; and no page asks GitHub directly in any of the three.
