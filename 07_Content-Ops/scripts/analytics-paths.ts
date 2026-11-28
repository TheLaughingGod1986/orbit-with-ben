/** Resolve channel records through the studio registry, without network or writes. */
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import type { ChannelKey } from "../src/lib/analytics/channel-tracker";

export const ENGINE_ROOT = path.resolve(__dirname, "../..");
export const ANALYTICS_ROOT = path.join(ENGINE_ROOT, "05_Analytics");

export function channelRoot(key: ChannelKey, engine = ENGINE_ROOT): string {
  const registry = JSON.parse(fs.readFileSync(path.join(engine, "channels/channels.json"), "utf8"));
  if (!registry.channels.some((entry: { slug: string }) => entry.slug === key)) {
    throw new Error(`Analytics channel is not registered: ${key}`);
  }
  // Preserve the running resident timer until its separate cutover.
  if (registry.channels.some((entry: { home?: boolean }) => entry.home)) {
    return key === "ww2" ? path.join(engine, "channels/ww2/05_Analytics") : path.join(engine, "05_Analytics", key);
  }
  // Use the same loader as the board. Never guess a missing detached data checkout.
  const probe = `import json, pathlib, sys
sys.path.insert(0, sys.argv[1])
import channels
key = sys.argv[2]
co = channels.checkout(key)
if co is None:
    raise SystemExit("Analytics requires the channel record checkout")
if json.loads((co / "studio/channel.json").read_text()).get("slug") != key:
    raise SystemExit("Analytics checkout identity mismatch")
folder = channels.analytics_dir(key).resolve()
if not folder.is_dir() or not (folder / "snapshots").is_dir():
    raise SystemExit("Analytics history must be staged before cutover")
if co.resolve() == channels.ROOT.resolve() or channels.ROOT.resolve() in folder.parents:
    raise SystemExit("Detached analytics cannot write into the engine")
print(json.dumps(str(folder)))
`;
  try {
    return JSON.parse(execFileSync("python3", ["-c", probe, path.join(engine, "scripts"), key],
      { encoding: "utf8", timeout: 10000, stdio: ["ignore", "pipe", "pipe"] }));
  } catch {
    throw new Error(`Analytics record root unavailable for ${key}; stage its checkout and history before cutover`);
  }
}

export function assertAnalyticsEngine(): void {
  try {
    execFileSync("python3", [path.join(ENGINE_ROOT, "scripts/engine_guard.py")],
      { timeout: 10000, stdio: ["ignore", "ignore", "pipe"] });
  } catch {
    throw new Error("Analytics refused: engine identity guard failed");
  }
}
