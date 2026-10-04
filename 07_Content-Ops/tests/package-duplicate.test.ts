import { it, expect } from "vitest";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { checkPackageDuplicate } from "../src/lib/publishing/package-duplicate";

it("refuses matching registry and result IDs, ignores dry runs and different hashes, allows force-new", async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "owb-duplicate-"));
  try {
    const pkg = path.join(root, "package");
    fs.mkdirSync(pkg);
    const video = path.join(root, "video.mp4");
    fs.writeFileSync(video, "test media");
    const uploadsFile = path.join(root, "UPLOADS.json");
    const input = { packageDir: pkg, videoPath: video, uploadsFile, repoRoot: root };
    const identity = await checkPackageDuplicate(input);
    fs.writeFileSync(uploadsFile, JSON.stringify({ version: 1, videos: { live: identity } }));
    await expect(checkPackageDuplicate(input)).rejects.toThrow("UPLOADS.json");
    await expect(checkPackageDuplicate({ ...input, forceNew: true })).resolves.toEqual(identity);
    fs.writeFileSync(uploadsFile, JSON.stringify({ version: 1, videos: { live: { ...identity, sha256: "different" } } }));
    await expect(checkPackageDuplicate(input)).resolves.toEqual(identity);
    for (const name of ["film_PACKAGE_UPLOAD_RESULT.json", "PACKAGE_UPLOAD_RESULT_stamp.json"]) {
      const resultFile = path.join(pkg, name);
      const result = { dryRun: true, upload: { platformPostId: "live" }, package: identity };
      fs.writeFileSync(resultFile, JSON.stringify(result));
      await expect(checkPackageDuplicate(input)).resolves.toEqual(identity);
      fs.writeFileSync(resultFile, JSON.stringify({ ...result, dryRun: false }));
      await expect(checkPackageDuplicate(input)).rejects.toThrow(name);
      // Retain as a dry result for the next iteration.
      fs.writeFileSync(resultFile, JSON.stringify(result));
    }
    fs.writeFileSync(path.join(pkg, "PACKAGE_UPLOAD_RESULT_legacy.json"), JSON.stringify({
      upload: { platformPostId: "legacy" }, package: { sources: { video } },
    }));
    await expect(checkPackageDuplicate(input)).rejects.toThrow("legacy");
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});
