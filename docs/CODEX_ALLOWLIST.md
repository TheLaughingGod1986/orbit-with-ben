# J2040: unattended command permissions — inspection only

Inspected by Codex on 6 November 2026. No approval configuration was changed and no allow-list was installed.

The Mini reports `codex-cli 0.160.0`. Its `codex execpolicy --help` exposes `check`, described as checking execpolicy files against a command. Official background: [OpenAI Rules documentation](https://learn.chatgpt.com/docs/agent-configuration/rules).

J2040 requests exemptions for non-force pushes to the two studio repositories, social uploads to the existing R2 bucket, Buffer post operations and YouTube API calls through studio scripts. These requests affect the agent's own approval controls. This agent cannot change those controls or install exemptions from security review. Configuration must be handled outside this agent run by the authorized operator or administrator.

No executable rules are supplied here. A command prefix alone must not be treated as proof of repository, bucket, profile, channel or operation scope: script arguments, mutable script contents, remote configuration and credentials can change the actual destination or action. No claim is made that the requested restrictions have been enforced.

The requested positive/negative approval tests were not run because no rules were installed. No scratch remote branch was created or deleted. Existing approval review remains active; initial git metadata writes required escalation, and approved pull/queue operations succeeded after escalation. These are not evidence of unattended allow-list operation.

J2007 is currently cancelled (4 November 2026, WIP limit), so its historical rejected push was not retried. Its old local decision must not be landed automatically over newer production state.

J2040 remains unfinished: approval configuration and its acceptance tests are outstanding. This inspection does not authorize another worker to bypass review or mark the job complete.
