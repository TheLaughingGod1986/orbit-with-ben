# J2564: what the usage pages show (copied from the Mini's credit-reading log)

Job J2566. Source: `~/Library/Logs/owb-ai-spend.log` on the Mini, the daily run of 11 Nov 2026 08:30Z
(the first run after #797; log lines 663-736 of 736). Lines inside the code blocks are copied exactly.

## cursor

```
UNREAD cursor: RuntimeError: no 'Cursor Models' or 'Other Models · N% used' line on the Cursor spending page (signed out, or the page changed) · likely cause: signed in, but the page's wording is not what the reader expects; the reader needs a fix (the page's text is below) · last recorded 09 Nov 08:30Z by mini-daily (48 h ago)
  page address: grok.com/dashboard/billing
  page shows: Overview
  page shows: My settings
  page shows: Cloud Agents
  page shows: API
  page shows: API keys
  page shows: Customizations
  page shows: Plugins
  page shows: Integrations
  page shows: Shared resources
  page shows: Subscription
  page shows: Members
  page shows: Usage
  page shows: Billing
  page shows: Benjamin Oats
  page shows: Ultra
  page shows: Overview
  page shows: Ultra
  page shows: 30%
  page shows: used
  page shows: x
  page shows: Grok Bot 29%
  page shows: Cursor 1%
  page shows: Weekly included usage
  page shows: Resets 12 Nov
  page shows: Included usage with your subscription. Used before your credits.
```

## codex

```
READ codex: left=92.0 total=100.0 · weekly 8% used, resets Tue 17 Nov 23:22Z; read from the Codex log at 11 Nov 08:18Z
```

## claude

```
UNREAD claude: RuntimeError: no 'Current session' or weekly 'N% used' line on the Claude usage page (signed out, or the page changed) · likely cause: signed in, but the page's wording is not what the reader expects; the reader needs a fix (the page's text is below) · last recorded 08 Nov 08:30Z by mini-daily (3 days ago)
  page address: claude.ai/new
  page shows: Claude
  page shows: 
  page shows: Claude
  page shows: 
  page shows: 
  page shows: Navigation
  page shows: 
  page shows: New
  page shows: ⇧
  page shows: Shift
  page shows: ⌘
  page shows: Command
  page shows: O
  page shows: 
  page shows: Search
  page shows: ⌘
  page shows: Command
  page shows: K
  page shows: 
  page shows: Projects
  page shows: 
  page shows: Artifacts
  page shows: 
  page shows: 
  page shows: Scheduled
```

## Summary line

```
SUMMARY 5 read; usage pages not read (no spending figure is missing): cursor, claude; every spending figure read was recorded
```
## Exit code

`launchctl list | grep ai-spend-daily`, read 11 Nov 2026 09:05Z:

```
-	0	com.owb.ai-spend-daily
```

Last exit code 0, not running.

## Notes from the copy (J2566, Claude Code on the Mini)

These are observations only. The readers were not changed.

- **Neither page is a sign-in screen.** Both show a signed-in account's own navigation.
- **cursor:** the lines are a usage overview with an "Ultra" plan, "30% used", a per-product split
  ("Grok Bot 29%", "Cursor 1%"), "Weekly included usage" and "Resets 12 Nov". There is no
  "Cursor Models" or "Other Models · N% used" line, which is what the reader looks for. The page
  address the log printed is the one shown above, copied as written.
- **claude:** the address is the new-chat page, not a usage page, and the 25 lines are the left-hand
  navigation only. No usage figure appears in the lines the log kept, so this file cannot show what
  the usage page itself says. Either the browser was sent on from the usage address to the new-chat
  page, or the tab the reader picked was not the usage tab.
- **codex:** read normally in this run (from the Codex session log, no page), so it has no
  `page address:` or `page shows:` lines.
- **Privacy check:** no email address and no card or payment line in this file; nothing had to be
  replaced. One `page shows:` line in the cursor block is the account holder's name as the page
  prints it. It is left as copied, since the brief asks for exact lines and only email addresses
  and card details are to be removed; the Chief can swap it for `<removed>` if preferred.
- The same run's log also carries a `git push` rejection (remote had newer work) between the codex
  `READ` line and its ledger row. It is outside this job; the row did reach main later.
