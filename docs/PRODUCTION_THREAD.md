# Production thread (do not merge)

This file exists only so the draft pull request "Production thread: Chief of Staff <-> Claude" has a diff and stays open.
The pull request is the message channel between the Chief of Staff (via the Mini) and Claude. **Never merge or close it.**

- The Mini posts and reads with `python3 scripts/owb_thread.py` (see the script's help).
- Chief messages start with `[Chief]`. Claude's replies end with the Claude Code footer.
- Decisions that need Ben are flagged `NEEDS BEN` in the reply; Ben still decides.
