# J3403: Field Order History audience read — 23 November 2026

Codex covering. Read-only, £0. Existing Studio tab on the configured channel browser reused. Live ytcfg CHANNEL_ID matched UCu94mInMFosxu3W0H6jlI6Q; Studio also named Field Order History.

- Earn: https://studio.youtube.com/channel/UCu94mInMFosxu3W0H6jlI6Q/monetization — “0 qualified watch hours”, “last 365 days”. The card says “Showing data as of: 17 Nov 2026”. This is the displayed qualified balance, not a current API watch-time estimate. Read date is separate from the card's reporting lag.
- Audience: https://studio.youtube.com/channel/UCu94mInMFosxu3W0H6jlI6Q/analytics/hub_audience — “When your viewers are on YouTube”, “Your local time (GMT+00:00)”, “Last 28 days”, “Not enough data”. No weekday/hour/activity values exist to transcribe. Top geographies, Age and Gender also say “Not enough data”. The key-metrics range shown is 25 Oct–21 Nov 2026.
- Content: one Public film, ek9F61FVYqY, published 22 Nov; one Scheduled film for 25 Nov. The old missing reason saying no public films is superseded.
- Public-film test read: https://studio.youtube.com/video/ek9F61FVYqY/edit — A/B Testing opens the setup dialog with Title only / Thumbnail only / Title and thumbnail and “Set test”; no running or finished results. Closed via Close without setting a test. No watch-time shares or winner invented.

Playwright's browser attach timed out. Direct CDP Runtime.evaluate against the same existing Studio target successfully read the DOM and navigated existing links. No new tab, account switch, sign-in, settings save, test creation or public change occurred.

The strict dated importer merges this partial channel read, preserving all prior video windows. No per-film reporting window is added because this weekly channel read has no matching API window yet.

Session disk check found about 12 GB free. The prescribed detached nas_offload.py --apply completed with no eligible old scratch; nothing moved or deleted. Log: ~/_desk/logs/J3403-disk.log.
