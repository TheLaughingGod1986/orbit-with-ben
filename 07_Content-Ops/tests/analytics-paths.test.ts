import { afterEach, describe, expect, it } from "vitest";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { channelRoot, ENGINE_ROOT } from "../scripts/analytics-paths";
const temporary: string[] = [];
afterEach(() => { for (const dir of temporary.splice(0)) fs.rmSync(dir, { recursive: true, force: true }); });
function fixture(resident = false) {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), "analytics-paths-")); temporary.push(base);
  const engine = path.join(base, "engine");
  fs.mkdirSync(path.join(engine, "scripts"), { recursive: true });
  fs.mkdirSync(path.join(engine, "channels"), { recursive: true });
  fs.copyFileSync(path.join(ENGINE_ROOT, "scripts/channels.py"), path.join(engine, "scripts/channels.py"));
  const entries = ["owb", "hos", "ww2"].map(slug => ({ slug, home: resident && slug === "owb", checkouts: [`fixture-${slug}`] }));
  fs.writeFileSync(path.join(engine, "channels/channels.json"), JSON.stringify({ studio: { default_channel: "owb" }, channels: entries }));
  for (const { slug } of entries) {
    const manifest = { slug, label: slug, name: slug, repo: { checkouts: [`fixture-${slug}`] }, title_match: slug, wip: {} };
    const checkout = path.join(base, `fixture-${slug}`);
    fs.mkdirSync(path.join(checkout, "studio"), { recursive: true });
    fs.mkdirSync(path.join(checkout, "05_Analytics", slug, "snapshots"), { recursive: true });
    fs.writeFileSync(path.join(checkout, "studio/channel.json"), JSON.stringify(manifest));
    fs.mkdirSync(path.join(engine, "channels", slug), { recursive: true });
    fs.writeFileSync(path.join(engine, "channels", slug, "channel.json"), JSON.stringify(manifest));
  }
  return { base, engine };
}
describe("analytics record destinations", () => {
  it("preserves the resident timer paths", () => {
    const { engine } = fixture(true);
    expect(channelRoot("owb", engine)).toBe(path.join(engine, "05_Analytics/owb"));
    expect(channelRoot("hos", engine)).toBe(path.join(engine, "05_Analytics/hos"));
    expect(channelRoot("ww2", engine)).toBe(path.join(engine, "channels/ww2/05_Analytics"));
  });
  it("resolves every detached channel through the actual registry loader", () => {
    const { engine, base } = fixture();
    for (const key of ["owb", "hos", "ww2"] as const) {
      expect(channelRoot(key, engine)).toBe(fs.realpathSync(path.join(base, `fixture-${key}/05_Analytics/${key}`)));
    }
    expect(fs.existsSync(path.join(engine, "05_Analytics"))).toBe(false);
  });
  it("refuses absent history without creating an empty record tree", () => {
    const { engine, base } = fixture();
    fs.rmSync(path.join(base, "fixture-hos/05_Analytics"), { recursive: true });
    expect(() => channelRoot("hos", engine)).toThrow("record root unavailable");
    expect(fs.existsSync(path.join(base, "fixture-hos/05_Analytics"))).toBe(false);
  });
  it("refuses a checkout naming another channel", () => {
    const { engine, base } = fixture();
    const file = path.join(base, "fixture-hos/studio/channel.json");
    const manifest = JSON.parse(fs.readFileSync(file, "utf8")); manifest.slug = "owb";
    fs.writeFileSync(file, JSON.stringify(manifest));
    expect(() => channelRoot("hos", engine)).toThrow("record root unavailable");
  });
});
