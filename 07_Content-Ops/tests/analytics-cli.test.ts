/** Real collector/report processes in a detached registry; no live API access. */
import { afterEach, describe, expect, it } from "vitest";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";

const ops = path.resolve(__dirname, "..");
const roots: string[] = [];
afterEach(() => { for (const root of roots.splice(0)) fs.rmSync(root, { recursive: true, force: true }); });
function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "analytics-cli-")); roots.push(root);
  const engine = path.join(root, "engine"), content = path.join(engine, "07_Content-Ops");
  const write = (name: string, value: string) => {
    const file = path.join(root, name); fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, value);
  };
  fs.mkdirSync(content, { recursive: true });
  fs.cpSync(path.join(ops, "src"), path.join(content, "src"), { recursive: true });
  for (const file of ["tsconfig.json", "package.json", "scripts/analytics-snapshot.ts", "scripts/analytics-report.ts", "scripts/analytics-paths.ts"]) {
    write(`engine/07_Content-Ops/${file}`, fs.readFileSync(path.join(ops, file), "utf8"));
  }
  fs.symlinkSync(fs.realpathSync(path.join(ops, "node_modules")), path.join(content, "node_modules"), "dir");
  for (const file of ["channels.py", "engine_guard.py"]) write(`engine/scripts/${file}`, fs.readFileSync(path.join(ops, "../scripts", file), "utf8"));
  const slugs = ["owb", "hos", "ww2"];
  write("engine/channels/channels.json", JSON.stringify({ studio: { github: "fixture/studio", default_channel: "owb" },
    channels: slugs.map(slug => ({ slug, env: `FIXTURE_${slug.toUpperCase()}_REPO`, checkouts: [`fixture-${slug}`] })) }));
  const env: NodeJS.ProcessEnv = { PATH: process.env.PATH, TMPDIR: root,
    GOOGLE_CLIENT_ID: "fixture", GOOGLE_CLIENT_SECRET: "fixture", YT_CHANNEL_ID_WW2: "UC0000000000000000000000" };
  for (const slug of slugs) {
    const manifest = { slug, label: slug, name: slug, title_match: slug, wip: {}, repo: { checkouts: [`fixture-${slug}`] } };
    write(`fixture-${slug}/studio/channel.json`, JSON.stringify(manifest));
    write(`engine/channels/${slug}/channel.json`, JSON.stringify(manifest));
    fs.mkdirSync(path.join(root, `fixture-${slug}/05_Analytics/${slug}/snapshots`), { recursive: true });
    env[`FIXTURE_${slug.toUpperCase()}_REPO`] = path.join(root, `fixture-${slug}`);
    env[`YT_ANALYTICS_REFRESH_TOKEN_${slug.toUpperCase()}`] = slug;
  }
  write("fake-api.mjs", fs.readFileSync(path.join(ops, "tests/fixtures/analytics-api.mjs"), "utf8"));
  env.NODE_OPTIONS = `--import=${path.join(root, "fake-api.mjs")}`;
  env.FIXTURE_REQUEST_LOG = path.join(root, "requests.jsonl");
  const run = (script: string, ...args: string[]) => spawnSync(process.execPath,
    [path.join(content, "node_modules/tsx/dist/cli.mjs"), path.join(content, "scripts", script), ...args],
    { cwd: content, env, encoding: "utf8", timeout: 30000 });
  const read = (name: string) => JSON.parse(fs.readFileSync(path.join(root, name), "utf8"));
  const requests = () => fs.existsSync(env.FIXTURE_REQUEST_LOG!) ? fs.readFileSync(env.FIXTURE_REQUEST_LOG!, "utf8").trim().split("\n").map(line => JSON.parse(line)) : [];
  return { root, engine, env, run, read, requests };
}

describe("detached analytics CLI contracts", () => {
  it("collects three channels and builds reports only in their owning repositories", () => {
    const f = fixture();
    const result = f.run("analytics-snapshot.ts", "--date", "2026-11-20");
    expect(result.status, result.stderr).toBe(0);
    for (const slug of ["owb", "hos", "ww2"]) {
      const snap = f.read(`fixture-${slug}/05_Analytics/${slug}/snapshots/2026-11-20.json`);
      expect(snap.channel).toBe(slug);
      expect(snap.videos).toHaveLength(1);
      expect(snap.videos[0].views).toBe(42);
      expect(snap.analytics.through).toBe("2026-11-18");
      expect(f.read(`fixture-${slug}/05_Analytics/${slug}/channel_daily.json`).rows[0].views).toBe(42);
      expect(fs.existsSync(path.join(f.engine, "05_Analytics", slug))).toBe(false);
    }
    expect(f.read("fixture-ww2/05_Analytics/ww2/detail.json").failures).toEqual([]);
    expect(fs.existsSync(path.join(f.root, "fixture-ww2/05_Analytics/ww2/READS.md"))).toBe(true);
    const before = f.requests().length;
    const report = f.run("analytics-report.ts");
    expect(report.status, report.stderr).toBe(0);
    expect(f.requests()).toHaveLength(before); // report must stay offline
    for (const slug of ["owb", "hos"]) expect(fs.existsSync(path.join(f.root, `fixture-${slug}/05_Analytics/${slug}/REPORT.md`))).toBe(true);
    expect(f.read("engine/05_Analytics/dashboard/data.json").channels).toHaveLength(2);
  }, 40000);

  it("refuses a missing history destination before token exchange", () => {
    const f = fixture();
    fs.rmSync(path.join(f.root, "fixture-hos/05_Analytics"), { recursive: true });
    const result = f.run("analytics-snapshot.ts", "--channel", "hos");
    expect(result.status).toBe(1);
    expect(result.stderr).toContain("record root unavailable");
    expect(f.requests()).toEqual([]);
    expect(fs.existsSync(path.join(f.root, "fixture-hos/05_Analytics"))).toBe(false);
  });

  it("keeps successful channels when one API fails and returns nonzero", () => {
    const f = fixture(); f.env.FIXTURE_FAIL_CHANNEL = "hos";
    const result = f.run("analytics-snapshot.ts", "--date", "2026-11-20");
    expect(result.status).toBe(1);
    for (const slug of ["owb", "ww2"]) expect(f.read(`fixture-${slug}/05_Analytics/${slug}/snapshots/2026-11-20.json`).channel).toBe(slug);
    expect(fs.existsSync(path.join(f.root, "fixture-hos/05_Analytics/hos/snapshots/2026-11-20.json"))).toBe(false);
  });

  it("makes no requests for unconfigured Field Order History", () => {
    const f = fixture(); delete f.env.YT_ANALYTICS_REFRESH_TOKEN_WW2;
    const result = f.run("analytics-snapshot.ts", "--channel", "ww2");
    expect(result.status, result.stderr).toBe(0);
    expect(result.stdout).toContain("disabled");
    expect(f.requests()).toEqual([]);
  });
});
