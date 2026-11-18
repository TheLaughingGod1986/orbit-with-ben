# J2982 board cleanup

Codex covering, elected acting Chief. KEEP: the changes are bounded to display wording, published string privacy, and the Pages build configuration.

The Agents team rows now turn usage resets into London day/date/time (including British Summer Time) and remove probe/job jargon from the visible reason. Raw model records remain available in the existing AI Details view. Working job descriptions retain their plain-language text.

The publisher recursively sanitizes every string and dictionary key in board and tracker data before digesting and publishing, including retained update history. Home-folder prefixes become `~`. The source documents are untouched.

The Pages build read the old routing file, so its contents are retained as `host_config.json`, with build/tests/docs migrated. Removed the unused local Vercel project link. The adapter and Wrangler configuration read neither Vercel file. The separate board-data `NO_DEPLOY` Vercel guard is unchanged. Open taps remain off.

Legacy project audit: no active current script, operational document, LaunchAgent, or inspected Vercel configuration points at the retired hostname. Seven OWB historical review/patch records and one HOS historical checks read retain it. A non-executable local pairing-test file also retains it; no current script or launchd reference to that test was found. Old scratch checkouts and a proxy log retain historical copies; these are not proof of a live dependency. Those local files were left untouched. The old project itself is retained; deletion stays Ben’s decision.

Validation: 40 publisher tests, 4 site tests, 10 update tests, 13 authentication tests, and the Studio JavaScript suite pass. The site tests build Pages output and verify redirects, headers and worker placement. Production verification follows merge.
