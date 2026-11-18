# J3071 MacBook HOS Studio Fallback Evidence for J3070

- **Verified by:** `macbook-2` (`J3071`) on the MacBook
- **Analytics observed at:** `2026-11-18T20:37:02.820251+00:00` (active chips `Insights` + `Since published` re-confirmed at `2026-11-18T20:38:54.212534+00:00`)
- **Endpoint & helper:** `http://127.0.0.1:9222` via `scripts/cdp_tabs.py` `reuse_page(ctx, "studio.youtube.com")` (single tab `EA394E247B8CE3D31BDC9C7D3C8291D6` preserved; `:9222` remains up on the MacBook so `macbook_worker.py` advertises `9222` in `MACBOOK_CDP`)
- **Responsiveness:** `connect_over_cdp` `0.0298 s`, `reuse_page` `0.0023 s`, `Runtime.evaluate` (`document.title` + `document.body.innerText`) `0.0097 s` (`readyState: "complete"`)
- **Signed-in channel:** `HistoryOfScienceYT` (`History of Science`, `UCXp7HkBIl1LgaznXuZHJyRg`), verified on both Studio dashboard (`20:35:59Z`) and `/channel/UCXp7HkBIl1LgaznXuZHJyRg/editing/profile` (`20:36:57Z`)
- **Target Analytics page:** `https://studio.youtube.com/video/ChbsigHD5_o/analytics/tab-overview/period-since_publish` → resolved cleanly to `https://studio.youtube.com/video/ChbsigHD5_o/analytics/hub_overview` (`Video analytics - YouTube Studio`, `How Do Plants Clean the Air?`, `Since published` selected, range `18 Nov 2026, 11:30` – `18 Nov 2026, 20:36`, `Views: 0`, `Likes: 0`, retention/engagement `Not enough data`; dashboard card `First 9 hours 5 minutes` shows `Ranking by views: 9 of 10`).
- **Full sanitized evidence:** `jobs/reviews/J3071/REPORT.md` and `jobs/reviews/J3071/evidence.json`.
- **Scope preserved:** `J3063` and `J3064` untouched; no `launch_check.py` write or performance verdict recorded here; zero YouTube/login/profile edits.
