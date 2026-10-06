import { spawnSync } from "child_process";
import path from "path";

/**
 * The Shorts ship gate (`00_Brand/Channel-Setup/tools/gate_shorts_open.py check`) as a hard stop in the upload path.
 * Two Orbit-at-frame-0 Shorts (dQlOgsDGmtA, Ih2zhZTbIR0) went out in Sept because no upload path ran it (#99 6012375100).
 * There is no override: Orbit at frame 0 is on the Never list.
 */
export type GateRunner = (cmd: string, args: string[]) => { status: number | null; stdout: string; stderr: string };

const defaultRunner: GateRunner = (cmd, args) => {
  const r = spawnSync(cmd, args, { encoding: "utf8" });
  return { status: r.status, stdout: r.stdout ?? "", stderr: r.stderr ?? (r.error ? String(r.error) : "") };
};

export type GateResult = { ok: boolean; exitCode: number | null; airDate: string; output: string };

export function airDateFor(scheduledAt: Date | null | undefined, now = new Date()): string {
  return (scheduledAt ?? now).toISOString().slice(0, 10);
}

export function runShortsGate(
  opts: { videoPath: string; repoRoot: string; scheduledAt?: Date | null; videoId?: string },
  run: GateRunner = defaultRunner,
): GateResult {
  const airDate = airDateFor(opts.scheduledAt);
  const gate = path.join(opts.repoRoot, "00_Brand/Channel-Setup/tools/gate_shorts_open.py");
  const args = [gate, "check", opts.videoPath, "--air-date", airDate, ...(opts.videoId ? ["--id", opts.videoId] : [])];
  const r = run("python3", args);
  return { ok: r.status === 0, exitCode: r.status, airDate, output: `${r.stdout}${r.stderr}`.trim() };
}
