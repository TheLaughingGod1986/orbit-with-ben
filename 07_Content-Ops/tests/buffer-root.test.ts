import fs from "fs";
import os from "os";
import path from "path";
import { afterEach, expect, it } from "vitest";
import { bufferRecordRoot, registeredPackageTags } from "../src/lib/publishing/buffer-deps";
import { getProfile, profileFiles } from "../src/lib/publishing/buffer-profile";
import { findMedia, registerUpload, scanProjectRecords } from "../src/lib/publishing/media-finder";

const roots: string[] = [];
afterEach(() => { for (const root of roots.splice(0)) fs.rmSync(root, { recursive: true, force: true }); });
function fixture(home = false) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "buffer-root-")); roots.push(dir);
  const engine = path.join(dir, "engine");
  const channel = path.join(dir, "channel");
  const put = (file: string, value: unknown) => {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, JSON.stringify(value));
  };
  put(path.join(engine, "channels/channels.json"), { channels: [{ slug: "owb", home, env: "SAMPLE_RECORD_REPO" }] });
  put(path.join(engine, "channels/owb/channel.json"), { repo: { env: "SAMPLE_RECORD_REPO" } });
  put(path.join(channel, "studio/channel.json"), { slug: "owb" });
  return { engine, channel, put };
}
it("keeps the resident layout and fails closed for a detached engine without its channel", () => {
  const resident = fixture(true);
  expect(bufferRecordRoot(resident.engine, {})).toBe(resident.engine);
  const { engine, channel, put } = fixture();
  expect(() => bufferRecordRoot(engine, {})).toThrow(/absolute SAMPLE_RECORD_REPO/);
  expect(() => bufferRecordRoot(engine, { SAMPLE_RECORD_REPO: "relative" })).toThrow(/absolute/);
  put(path.join(channel, "studio/channel.json"), { slug: "hos" });
  expect(() => bufferRecordRoot(engine, { SAMPLE_RECORD_REPO: channel })).toThrow(/independent Orbit/);
});
it("keeps both registers, plans, package tags and relative media in the independent record checkout", () => {
  const { engine, channel, put } = fixture();
  const root = bufferRecordRoot(engine, { SAMPLE_RECORD_REPO: channel });
  const media = path.join(channel, "02_Video-Projects/001_Test/short.mp4");
  fs.mkdirSync(path.dirname(media), { recursive: true }); fs.writeFileSync(media, "test-only");
  const packageDir = "02_Video-Projects/001_Test/package";
  put(path.join(channel, packageDir, "PACKAGE_MANIFEST.json"), { tags: ["test topic"] });
  for (const id of ["owb", "hos"]) {
    const files = profileFiles(getProfile(id), root);
    expect(files.plans.startsWith(channel + path.sep)).toBe(true);
    expect(files.ledger.startsWith(channel + path.sep)).toBe(true);
    expect(files.channels.startsWith(channel + path.sep)).toBe(true);
    const registry = registerUpload(files.uploads, root, "testvideo01", { file: media, packageDir, kind: "short" });
    expect(registry.videos.testvideo01.file).toBe("02_Video-Projects/001_Test/short.mp4");
    expect(findMedia("testvideo01", { registry, scanned: new Map(), repoRoot: root, registryFile: files.uploads })?.mediaPath).toBe(media);
    expect(registeredPackageTags(root, registry.videos.testvideo01.packageDir)).toEqual(["test topic"]);
  }
  put(path.join(channel, "02_Video-Projects/001_Test/upload_result.json"), { video_id: "testvideo02", file: "short.mp4" });
  expect(scanProjectRecords(root).get("testvideo02")?.file).toBe(media);
  expect(scanProjectRecords(engine).size).toBe(0);
  expect(fs.existsSync(path.join(engine, "00_Brand"))).toBe(false);
});
