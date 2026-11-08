# J1809 Chief review — FIX

Codex, elected acting Chief, 7 November 2026. Reviewed HOS PR450 head
`5f3feb775398ea06d87807ae825dfce2a6118e94`, its body, worker result/history,
changed source and tests. The original J1809 stays held. Do not merge PR450
or refresh the watcher at this revision.

The 12 existing tests pass (`python3 -m unittest scripts/test_hos_desk_handoffs.py`).
Three isolated probes against the exact head demonstrate gaps those tests miss.
All process launches and GitHub comments were mocked; no live restart or replay occurred.

1. **Unsafe refresh (high):** `cmd_refresh` takes `children` from the caller,
   defaulting to zero. It never discovers the launchd PID or checks children,
   descendants or the dispatch lock. With an installed file containing CODE and
   `apply=True, children=0`, its only subprocess call is
   `launchctl kickstart -k gui/501/com.hos.desk`. The advertised idle boundary is
   not enforced. Require real process/lease/dispatch-lock inspection, fail closed
   on unknown state, and protect the boundary against a concurrent dispatch.
   Record loaded PID/version after a permitted restart, not only a source marker.
2. **Historical replay (high):** start with `last=2`, empty pending, and an already
   existing literal Grok task id 4. The first upgraded `check_inbox(run=True)`
   calls `run_agent` once. `run_fence` covers only old pending entries, not unseen
   historical literal mail above the saved watermark. Fence the whole initial
   snapshot for every affected recipient; keep watermarks monotonic and admit
   only specific, reviewed unresolved IDs. Do not bulk replay or reset state.
3. **Lost handback delivery (high):** deliver role message 4 to Codex, hand it
   back to Grok, then call `deliver_role` for elected Grok. It returns zero because
   only fresh incoming IDs are shown. On Grok's first literal poll the pending
   role message is added to `run_fence` and also hidden there. Durable state alone
   is not delivery. Keep pending role mail visible until trusted acknowledgement,
   including after restart and handback, without dispatching it through Cursor.

Required repair verification: command-level tests for real idle inspection
(mock the OS boundary, not a caller-provided count), pre-upgrade unseen literal
mail, pending role redelivery, restart, handback to a first-time recipient,
trusted ack, duplicate recipients and Chief succession. Existing tests must
remain green. Ordinary Cursor must never gain Chief authority.

Follow-up: queue a specialist code repair linked to J1809, update PR450 and
return the corrected head to the elected Chief. J1809 is held on that repair;
no external date/credit/Ben hold is involved. After the corrected code passes
review and merges, the Chief authorises an idle-boundary refresh and controlled
live delivery/ack with PID/version evidence. Historical recovery separately
requires classification against later desk outcomes, queue and stage history.
Missing J1754 inventory is not permission to replay anything.

No production, publishing, spend or media approval. Ben's finished-film UAT and
all unrelated holds are unchanged. No audio/motion perception was claimed.
