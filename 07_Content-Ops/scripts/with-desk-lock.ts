import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";

/** Re-exec the CLI under the shared lock, including direct tsx invocations. */
export function ensureDeskLock(): void {
  const root = process.env.DESK_LOCK_ROOT || path.join(os.homedir(), "_desk/locks");
  const dir = path.resolve(root, "youtube-buffer.lock");
  // Only accept inheritance from the actual desk-lock parent, not an env flag alone.
  if (process.env.DESK_LOCK_HELD_DIR === dir) {
    try {
      const owner = fs.readFileSync(path.join(dir, "owner.txt"), "utf8");
      if (owner.split("\n").includes(`pid=${process.ppid}`)) return;
    } catch { /* acquire normally if metadata is absent */ }
  }
  const result = spawnSync("bash", [
    path.join(__dirname, "desk-lock.sh"), "youtube-buffer", "--",
    process.execPath, ...process.execArgv, ...process.argv.slice(1),
  ], { stdio: "inherit", env: process.env });
  if (result.error) console.error(`desk-lock: ${result.error.message}`);
  process.exit(result.status ?? 1);
}
