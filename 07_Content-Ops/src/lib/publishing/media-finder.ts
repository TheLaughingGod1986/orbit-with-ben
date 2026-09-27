/**
 * Finds the local file behind a YouTube upload, so the daily Buffer check can mirror
 * uploads that didn't go through `youtube:package` (STUDIO_PLAYBOOK.md §12).
 *
 * Where it looks, in order:
 * 1. 00_Brand/Channel-Setup/social/UPLOADS.json: the registry. `youtube:package` writes
 *    every upload here, and `buffer-mirror.ts register` adds one uploaded by hand.
 * 2. Older records in 02_Video-Projects: SHORTS_UPLOAD_INDEX.json, *upload_result*.json and
 *    PACKAGE_UPLOAD_RESULT_*.json.
 * A match only counts if the file exists on this machine. It never guesses from titles.
 */
import fs from "fs";
import path from "path";

export type UploadRecord = {
  kind?: "short" | "long";
  /** Short: the mp4 that went to YouTube. Repo-relative in the registry. */
  file?: string;
  /** Long: the selected thumbnail (Instagram posts it). */
  thumb?: string;
  /** Short: the long it promotes. */
  long?: string;
  /** Short with no long. */
  standalone?: boolean;
  registeredAt?: string;
};

export type Registry = { version: 1; videos: Record<string, UploadRecord> };

export type MediaHint = {
  videoId: string;
  mediaPath: string | null;
  thumbPath: string | null;
  longId: string | null;
  standalone: boolean;
  source: string;
};

const PROJECTS = "02_Video-Projects";

export function loadRegistry(file: string): Registry {
  return fs.existsSync(file) ? (JSON.parse(fs.readFileSync(file, "utf8")) as Registry) : { version: 1, videos: {} };
}

export function registerUpload(file: string, repoRoot: string, videoId: string, rec: UploadRecord, now = new Date()): Registry {
  const reg = loadRegistry(file);
  const rel = (p?: string) => (p ? path.relative(repoRoot, path.resolve(p)) : undefined);
  const prev = reg.videos[videoId] ?? {};
  const next: UploadRecord = { ...prev, ...rec, file: rel(rec.file) ?? prev.file, thumb: rel(rec.thumb) ?? prev.thumb, registeredAt: now.toISOString() };
  for (const k of Object.keys(next) as (keyof UploadRecord)[]) if (next[k] === undefined) delete next[k];
  reg.videos[videoId] = next;
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(reg, null, 2) + "\n");
  return reg;
}

/** The project folder (02_Video-Projects/NNN_Slug) a record file sits in. */
function projectDir(recordFile: string, repoRoot: string): string | null {
  const rel = path.relative(path.join(repoRoot, PROJECTS), recordFile);
  if (rel.startsWith("..")) return null;
  return path.join(repoRoot, PROJECTS, rel.split(path.sep)[0]);
}

/**
 * A path as written in an old record, resolved on this machine. Absolute paths from another
 * checkout are remapped from their `02_Video-Projects/` part. Returns null if no file exists.
 */
export function resolveRecordedPath(p: string | undefined | null, recordFile: string, repoRoot: string): string | null {
  if (!p || typeof p !== "string") return null;
  const candidates: string[] = [];
  if (path.isAbsolute(p)) {
    candidates.push(p);
    const i = p.indexOf(`/${PROJECTS}/`);
    if (i >= 0) candidates.push(path.join(repoRoot, p.slice(i + 1)));
  } else {
    const dir = path.dirname(recordFile);
    candidates.push(path.join(dir, p), path.join(path.dirname(dir), p));
    const proj = projectDir(recordFile, repoRoot);
    if (proj) candidates.push(path.join(proj, p));
    candidates.push(path.join(repoRoot, p));
  }
  return candidates.find((c) => fs.existsSync(c) && fs.statSync(c).isFile()) ?? null;
}

type Found = { file: string | null; thumb: string | null; long: string | null; kind?: "short" | "long"; source: string };

function walkRecords(dir: string, out: string[], depth = 0) {
  if (depth > 6 || !fs.existsSync(dir)) return;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith(".") || e.name === "node_modules" || e.name.startsWith("_template")) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walkRecords(p, out, depth + 1);
    else if (/^(SHORTS_UPLOAD_INDEX|PACKAGE_UPLOAD_RESULT_.*|.*upload_result.*)\.json$/i.test(e.name)) out.push(p);
  }
}

/** Every video id the old records know about, with its files resolved on this machine. */
export function scanProjectRecords(repoRoot: string): Map<string, Found> {
  const files: string[] = [];
  walkRecords(path.join(repoRoot, PROJECTS), files);
  const found = new Map<string, Found>();
  const add = (id: unknown, f: Found) => {
    if (typeof id !== "string" || !/^[\w-]{11}$/.test(id)) return;
    const prev = found.get(id);
    // Prefer a record that actually resolves a file.
    if (!prev || (!prev.file && !prev.thumb && (f.file || f.thumb))) found.set(id, { ...f, long: f.long ?? prev?.long ?? null });
  };
  for (const file of files.sort()) {
    let d: Record<string, unknown>;
    try {
      d = JSON.parse(fs.readFileSync(file, "utf8"));
    } catch {
      continue;
    }
    const src = path.relative(repoRoot, file);
    if (Array.isArray(d.shorts)) {
      for (const s of d.shorts as Record<string, unknown>[]) {
        add(s.youtube_video_id ?? s.video_id, {
          file: resolveRecordedPath(s.file as string, file, repoRoot),
          thumb: resolveRecordedPath(s.thumb as string, file, repoRoot),
          long: (s.related as string) ?? (d.long_id as string) ?? null,
          kind: "short",
          source: src,
        });
      }
    }
    const upload = d.upload as Record<string, unknown> | undefined;
    const pkg = d.package as Record<string, unknown> | undefined;
    if (upload?.platformPostId && pkg) {
      const sources = (pkg.sources ?? {}) as Record<string, string>;
      const isShort = pkg.format === "shorts";
      add(upload.platformPostId, {
        file: resolveRecordedPath(sources.video, file, repoRoot),
        thumb: resolveRecordedPath((pkg.thumbnailPath as string) ?? sources.thumbnail, file, repoRoot),
        long: null,
        kind: isShort ? "short" : "long",
        source: src,
      });
    }
    if (typeof d.video_id === "string") {
      add(d.video_id, {
        file: resolveRecordedPath((d.file as string) ?? (d.source as string), file, repoRoot),
        thumb: resolveRecordedPath(d.thumb as string, file, repoRoot),
        long: (d.related as string) ?? null,
        source: src,
      });
    }
  }
  return found;
}

/** Everything the mirror needs for one upload, or null when nothing on this machine matches. */
export function findMedia(videoId: string, opts: { registry: Registry; scanned: Map<string, Found>; repoRoot: string; registryFile: string }): MediaHint | null {
  const reg = opts.registry.videos[videoId];
  if (reg) {
    const abs = (p?: string) => (p ? resolveRecordedPath(path.resolve(opts.repoRoot, p), opts.registryFile, opts.repoRoot) : null);
    return {
      videoId,
      mediaPath: abs(reg.file),
      thumbPath: abs(reg.thumb),
      longId: reg.long ?? null,
      standalone: Boolean(reg.standalone),
      source: path.relative(opts.repoRoot, opts.registryFile),
    };
  }
  const f = opts.scanned.get(videoId);
  if (!f || (!f.file && !f.thumb)) return null;
  return { videoId, mediaPath: f.file, thumbPath: f.thumb, longId: f.long, standalone: false, source: f.source };
}
