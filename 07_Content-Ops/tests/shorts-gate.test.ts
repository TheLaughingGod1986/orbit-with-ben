import { describe, expect, it } from "vitest";
import { airDateFor, runShortsGate, type GateRunner } from "../src/lib/publishing/shorts-gate";

function runner(status: number, stdout = ""): GateRunner & { calls: string[][] } {
  const calls: string[][] = [];
  const fn = ((cmd: string, args: string[]) => {
    calls.push([cmd, ...args]);
    return { status, stdout, stderr: "" };
  }) as GateRunner & { calls: string[][] };
  fn.calls = calls;
  return fn;
}

describe("Shorts ship gate in the upload path", () => {
  it("passes only on exit 0", () => {
    const r = runner(0, "PASS");
    const g = runShortsGate({ videoPath: "/x/short.mp4", repoRoot: "/repo", scheduledAt: new Date("2026-10-14T10:30:00Z") }, r);
    expect(g.ok).toBe(true);
    expect(r.calls[0]).toEqual(["python3", "/repo/00_Brand/Channel-Setup/tools/gate_shorts_open.py", "check", "/x/short.mp4", "--air-date", "2026-10-14"]);
  });

  it("blocks on a FAIL, e.g. Orbit at frame 0 (dQlOgsDGmtA)", () => {
    const g = runShortsGate({ videoPath: "/x/moon.mp4", repoRoot: "/repo" }, runner(1, "FAIL Orbit in frame at 0 s"));
    expect(g.ok).toBe(false);
    expect(g.exitCode).toBe(1);
    expect(g.output).toMatch(/Orbit in frame at 0 s/);
  });

  it("blocks on a tool error too (exit 2 or no python)", () => {
    expect(runShortsGate({ videoPath: "/x/a.mp4", repoRoot: "/repo" }, runner(2)).ok).toBe(false);
    expect(runShortsGate({ videoPath: "/x/a.mp4", repoRoot: "/repo" }, ((() => ({ status: null, stdout: "", stderr: "ENOENT" })) as GateRunner)).ok).toBe(false);
  });

  it("uses the scheduled date as the air date, else today", () => {
    expect(airDateFor(new Date("2026-11-23T11:30:00Z"))).toBe("2026-11-23");
    expect(airDateFor(null, new Date("2026-10-06T08:00:00Z"))).toBe("2026-10-06");
  });
});
