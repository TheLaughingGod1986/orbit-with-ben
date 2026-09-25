# Analytics import

## Growth System v2

Canonical: `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md`

Content Ops **Analytics** dashboard surfaces:

Impressions · CTR · AVD · APV · returning/new viewers · Browse % · Suggested % · Search % · end screen / cards CTR · session time · top hooks / topics / Shorts · actionable recommendations (weak openings, retention drops, poor titles/thumbnails, runtime, funnel gaps).

```bash
cd 07_Content-Ops
npm run diagnose:youtube -- --file path/to/metrics.json
```

## Sample templates

```
07_Content-Ops/content/samples/csv/
  youtube_analytics_sample.csv
  tiktok_analytics_sample.csv
  instagram_insights_sample.csv
  facebook_insights_sample.csv
```

## Flow

1. Export analytics from the platform UI
2. Paste into Content Ops → Analytics
3. Preview column mapping
4. Import valid rows
5. Duplicate metric keys are skipped
6. Import batch metadata is stored on `AnalyticsImport`

## YouTube CSV columns (v2 mapping)

Defaults in `src/lib/analytics/csv-import.ts` include:

| Field | Typical Studio column |
|-------|------------------------|
| Impressions | Impressions |
| CTR | Impressions click-through rate (%) |
| AVD | Average view duration |
| APV | Average percentage viewed |
| Retention 30s | Audience retention at 30 seconds (%) |
| Returning / new | Returning viewers · New viewers |
| Browse / Suggested / Search | Browse features (%) · Suggested videos (%) · YouTube search (%) |
| End screen / cards | End screen element click rate (%) · Card clicks (%) |
| Session | Average session duration |

Missing fields are listed in the preview. Blank numeric cells are allowed — metrics stay `null`.

## Matching posts

Rows match existing `PlatformPost` records by `platformUrl` or `platformPostId`.  
If neither matches, the row errors clearly so you can paste the published URL onto the post first.

## Retention (manual + helper)

Studio retention curves are not auto-ingested yet. For Shorts:

1. Note stayed-to-watch, AVD, % viewed, completion from Studio.
2. Run:

```bash
python3 docs/tools/retention_diagnose_short.py \
  --title "Your Short Title" \
  --duration 26 --avd 19 --stayed 20.4 --pct-viewed 44 --completion 21 \
  --append-learnings
```

3. Update `docs/RETENTION_LEARNINGS.md` and the relevant row in `docs/SHORTS_EXPERIMENTS.md`.

Priority fields: stayed-to-watch · avg % viewed · AVD · completion · impressions · CTR · 30s retention · traffic sources · subs gained · end screen CTR.
