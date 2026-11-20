# J3012 MacBook installed/loaded inventory

20 November 2026. Job J3242. Read-only. £0. No LaunchAgent, service, credential, or active-studio marker was installed, restarted, paused, or modified.

The inventory ran on `main` at `f24a43b71e1b330412a1dd28a0f087e6cdd64578`, using the loaded-state reader merged in PR #1011. Exit 0. Standard error was empty. Three installed definitions matched the requested prefixes. All three parsed, all three loaded-state reads resolved, and none reference the old engine. `needs_review` stays true on every row: a guard or pause mention is a lexical flag, not a safety proof.

## Sanitized inventory

```json
{
  "inventory_only": true,
  "services": [
    {
      "source_sha256": "83f58098fbbe7989b61a5c4090c3077e0bfcc0b6c7781b430e980a54c56c420b",
      "status": "read",
      "needs_review": true,
      "source_name": "com.cursor.agents-window.plist",
      "label": "com.cursor.agents-window",
      "old_engine_reference": false,
      "scripts": [
        {
          "sha256": "e10a9ffa79f56d55160ac49d1d05c73267fd39bf6af6a3be5de46d264da19be7",
          "old_engine_reference": false,
          "guard_mentioned": false,
          "pause_mentioned": false
        }
      ],
      "command_resolved": true,
      "loaded": {
        "status": "loaded",
        "state": "not running"
      }
    },
    {
      "source_sha256": "c1f814efda0f1bd0d17050e14c82ba4aa1bee672e0dcae3a9e644f71195026a9",
      "status": "read",
      "needs_review": true,
      "source_name": "com.owb.macbook-cdp.plist",
      "label": "com.owb.macbook-cdp",
      "old_engine_reference": false,
      "scripts": [
        {
          "sha256": "eb5ea044b0387ab9e6fda32667d3901a58142670f77ae40d4f22f7eee83ad507",
          "old_engine_reference": false,
          "guard_mentioned": false,
          "pause_mentioned": false
        }
      ],
      "command_resolved": true,
      "loaded": {
        "status": "loaded",
        "state": "not running"
      }
    },
    {
      "source_sha256": "804d9c80529c3502ececc36d1f01d27c19fff141edc6a722b80157bd581ff071",
      "status": "read",
      "needs_review": true,
      "source_name": "com.owb.macbook-worker.plist",
      "label": "com.owb.macbook-worker",
      "old_engine_reference": false,
      "scripts": [
        {
          "sha256": "33802b851b3e5c19d9384ec365749090f6e24c176f0442c6497b2af8af12045e",
          "old_engine_reference": false,
          "guard_mentioned": true,
          "pause_mentioned": true
        }
      ],
      "command_resolved": true,
      "loaded": {
        "status": "loaded",
        "state": "running"
      }
    }
  ]
}
```

`com.owb.macbook-worker` is loaded and running. `com.owb.macbook-cdp` and `com.cursor.agents-window` are loaded and not running. The worker row mentions a guard and a pause; the other two rows mention neither.

## Studio repository access

Read-only `gh` access to the private `TheLaughingGod1986/studio` repo succeeded. No token was printed or recorded.

```json
{
  "name": "studio",
  "isPrivate": true,
  "defaultBranchRef": {
    "name": "rehearsal/j3012"
  }
}
```

```json
{
  "ref": "refs/heads/rehearsal/j3012",
  "sha": "534cf0f70852e06414cbe39f6a01efe9024c8a91"
}
```

The repository default branch is `rehearsal/j3012`, the same commit the rehearsal ref names. No clone and no fetch of file contents was made.

## Worker slots

`macbook` and `macbook-2` share one LaunchAgent: `com.owb.macbook-worker`. No second worker LaunchAgent is installed. The installed worker definition does not name slot 2. Each slot has its own studio checkout, its own History of Science checkout, and its own lock file, and the two studio checkouts are distinct directories.

Two other installed labels contain "macbook" and are not a second job slot: `com.owb.macbook-cdp` (in the inventory above) and `com.ben.macbook-no-phone-workers` (outside the requested prefixes; its contents were not read).

`scripts/macbook/render_worker_plist.py` staged a proposal into a mode `0600` file outside the git checkout. `plutil -lint` passed, no placeholder tokens remained, the label was `com.owb.macbook-worker`, and the renderer was silent with exit 0. SHA-256 of that proposal: `7aaa76c3198fe5f7c47aa1b410a2b8f0c9a9be0cd46389d1e0d87e9e5c2c3059`. The file was removed after the lint. The installed agent was unchanged and was not replaced.

## Left unchanged

No service, board deployment, film, credential, active-engine marker, or spend changed. J3012 is not complete; this is the MacBook inventory slice only.
