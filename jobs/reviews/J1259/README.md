# J1259 HOS release gate: block a long with no Chapters or Sources (Claude, 30 Oct 2026)

## What the gates do today (HOS main @ cb1b92e)

- `npm run lint:package` does not check for chapters or sources in a long's description. It only fails an empty one (`description.missing`). On main, 008, 009 and 010 all print `PASS` with no Chapters and no Sources.
- `npm run gate:episode` is a pre-VO/Veo script gate (`src/lib/analytics/episode-gate`). It never reads the upload description.
- Released longs differ: 006 and 007 carry both blocks, 001, 002 and 004 have chapters but no Sources, and 005 has both. 001 to 005 are already public, so lint skips them.

## The change (`hos_release_gate_chapters_sources.patch`, applies to HOS main @ cb1b92e)

- `rules.ts` gains `checkChaptersAndSources(description)`, and `lintLongPackage` calls it only when the description isn't empty. Shorts never go through `lintLongPackage`, so they're exempt.
- **Chapters:** stamp lines like `0:00 Title`. The first must be 0:00, there must be at least 3, and each must be at least 10 s after the last. These are YouTube's own conditions for showing chapters.
- **Sources:** a line starting `Sources` with at least one non-empty, non-timestamp line under it, or `Sources: …` on one line.
- Nothing is invented for 008, 009 or 010.
- `tests/hos-contract.test.ts`: the good-package fixture now carries both blocks, plus 4 new tests.

## Evidence (run here)

- `npx vitest run`: 97/97 pass (hos-contract 24/24).
- `npx tsx scripts/package-lint.ts`, with the patch: FAIL on exactly 008, 009 and 010, each with `description.chapters` and `description.sources`. Every other package is unchanged (006 and 007 PASS, public longs SKIP).
- On main the same command fails nothing.

**CI:** `.github/workflows/hos-contract.yml` runs `npx tsx scripts/package-lint.ts`, so the PR's `hos-contract` check will be red on 008, 009 and 010 by design until their descriptions get real Chapters and Sources. The vitest step is green.

Claude can't push to the HOS repo, so the Mini opens the PR and parks it for the Chief. Not to be merged by the worker.
