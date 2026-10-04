import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
import { loadRegistry, resolveRecordedPath } from "./media-finder";

async function sha256(file: string): Promise<string> {
  const hash = createHash("sha256");
  for await (const chunk of fs.createReadStream(file)) hash.update(chunk);
  return hash.digest("hex");
}

/** Called after desk-lock acquisition, before authentication or uploading. */
export async function checkPackageDuplicate(input: {
  packageDir: string; videoPath: string; uploadsFile: string; repoRoot: string; forceNew?: boolean;
}): Promise<{ packageDir: string; sha256: string }> {
  const packageDir = path.relative(input.repoRoot, path.resolve(input.packageDir));
  const digest = await sha256(input.videoPath);
  const identity = { packageDir, sha256: digest };
  if (input.forceNew) return identity;
  const samePackage = (dir: string) => path.resolve(input.repoRoot, dir) === path.resolve(input.packageDir);
  const matches = async (record: { packageDir?: string; sha256?: string; file?: string }, recordFile: string, inPackage = false) => {
    if (record.packageDir ? !samePackage(record.packageDir) : !inPackage) {
      // Legacy registry entries have no package identity: only the exact source file is safe evidence.
      const source = resolveRecordedPath(record.file, recordFile, input.repoRoot);
      if (record.packageDir || !source || path.resolve(source) !== path.resolve(input.videoPath)) return false;
    }
    if (record.sha256) return record.sha256 === digest;
    const source = resolveRecordedPath(record.file, recordFile, input.repoRoot);
    return source ? await sha256(source) === digest : false;
  };
  for (const [id, record] of Object.entries(loadRegistry(input.uploadsFile).videos)) {
    if (id && await matches(record, input.uploadsFile)) {
      throw new Error(`Refusing duplicate package upload: UPLOADS.json already records ${id}. Use --force-new only for an explicitly approved new upload.`);
    }
  }
  for (const dir of [input.packageDir, path.join(input.packageDir, "Schedule")]) {
    if (!fs.existsSync(dir)) continue;
    for (const name of fs.readdirSync(dir)) {
      if (!/^(?:.*_PACKAGE_UPLOAD_RESULT|PACKAGE_UPLOAD_RESULT.*)\.json$/i.test(name)) continue;
      const file = path.join(dir, name);
      const result = JSON.parse(fs.readFileSync(file, "utf8"));
      const id = result.upload?.platformPostId;
      if (result.dryRun || !id) continue;
      const record = { ...result.package, file: result.package?.sources?.video };
      if (await matches(record, file, true)) {
        throw new Error(`Refusing duplicate package upload: ${name} already records ${id}. Use --force-new only for an explicitly approved new upload.`);
      }
    }
  }
  return identity;
}
