import fs from "fs";
import os from "os";
import path from "path";
import { describe, expect, it } from "vitest";
import { findMedia, loadRegistry, registerUpload, resolveRecordedPath, scanProjectRecords } from "../src/lib/publishing/media-finder";

function repo() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "orbit-repo-"));
  const put = (rel: string, body = "x") => {
    const p = path.join(root, rel);
    fs.mkdirSync(path.dirname(p), { recursive: true });
    fs.writeFileSync(p, body);
    return p;
  };
  return { root, put };
}

describe("media finder", () => {
  it("registers repo-relative paths and finds them again", () => {
    const { root, put } = repo();
    const mp4 = put("02_Video-Projects/020_Jupiter/10_Shorts/survive.mp4");
    const regFile = path.join(root, "00_Brand/Channel-Setup/social/UPLOADS.json");
    registerUpload(regFile, root, "buaOI3QGm7U", { kind: "short", file: mp4, long: "-jmMROGoZCM" });
    expect(loadRegistry(regFile).videos.buaOI3QGm7U.file).toBe("02_Video-Projects/020_Jupiter/10_Shorts/survive.mp4");
    const hint = findMedia("buaOI3QGm7U", { registry: loadRegistry(regFile), scanned: new Map(), repoRoot: root, registryFile: regFile });
    expect(hint).toMatchObject({ mediaPath: mp4, longId: "-jmMROGoZCM", standalone: false });
  });

  it("keeps a long's trailer and social copy, and merges later copy into it", () => {
    const { root, put } = repo();
    const thumb = put("02_Video-Projects/020_Jupiter/08_Thumbnail/no-floor.jpg");
    const trailer = put("02_Video-Projects/020_Jupiter/11_Upload-Package/Trailer/trailer.mp4");
    const regFile = path.join(root, "00_Brand/Channel-Setup/social/UPLOADS.json");
    registerUpload(regFile, root, "-jmMROGoZCM", { kind: "long", thumb, trailer, social: { hook: "There's no ground on Jupiter." } });
    registerUpload(regFile, root, "-jmMROGoZCM", { social: { question: "Would you go in?" } });
    const rec = loadRegistry(regFile).videos["-jmMROGoZCM"];
    expect(rec).toMatchObject({ kind: "long", trailer: "02_Video-Projects/020_Jupiter/11_Upload-Package/Trailer/trailer.mp4" });
    expect(rec.social).toEqual({ hook: "There's no ground on Jupiter.", question: "Would you go in?" });
    const hint = findMedia("-jmMROGoZCM", { registry: loadRegistry(regFile), scanned: new Map(), repoRoot: root, registryFile: regFile });
    expect(hint).toMatchObject({ thumbPath: thumb, trailerPath: trailer, social: rec.social });
  });

  it("reads SHORTS_UPLOAD_INDEX, old upload results and package results", () => {
    const { root, put } = repo();
    put(
      "02_Video-Projects/007_Neutron/10_Shorts/SHORTS_UPLOAD_INDEX.json",
      JSON.stringify({ long_id: "Yk1tLh23rko", shorts: [{ youtube_video_id: "vCxXTYXSSqY", file: "10_Shorts/06_Final-Exports/a.mp4" }, { video_id: "fhJP6eMoU0Q", file: "10_Shorts/missing.mp4" }] }),
    );
    const a = put("02_Video-Projects/007_Neutron/10_Shorts/06_Final-Exports/a.mp4");
    // An absolute path from the old checkout is remapped onto this repo.
    put(
      "02_Video-Projects/013_Moon/10_Shorts/cover/upload/monday_upload_result.json",
      JSON.stringify({ video_id: "dQlOgsDGmtA", file: "/Users/ben/code/Orbit-YouTube/02_Video-Projects/013_Moon/10_Shorts/cover/moon_v10.mp4", related: "2fsQcea-voM" }),
    );
    const moon = put("02_Video-Projects/013_Moon/10_Shorts/cover/moon_v10.mp4");
    const thumb = put("02_Video-Projects/020_Jupiter/08_Thumbnail/Selected/cloud.jpg");
    put(
      "02_Video-Projects/020_Jupiter/11_Upload-Package/Schedule/PACKAGE_UPLOAD_RESULT_2026.json",
      JSON.stringify({ upload: { platformPostId: "-jmMROGoZCM" }, package: { format: "longform", thumbnailPath: thumb, sources: { video: "/nowhere/master.mp4" } } }),
    );
    const scanned = scanProjectRecords(root);
    expect(scanned.get("vCxXTYXSSqY")).toMatchObject({ file: a, long: "Yk1tLh23rko", kind: "short" });
    expect(scanned.get("dQlOgsDGmtA")).toMatchObject({ file: moon, long: "2fsQcea-voM" });
    expect(scanned.get("-jmMROGoZCM")).toMatchObject({ file: null, thumb, kind: "long" });
    const regFile = path.join(root, "UPLOADS.json");
    const opts = { registry: loadRegistry(regFile), scanned, repoRoot: root, registryFile: regFile };
    expect(findMedia("fhJP6eMoU0Q", opts)).toBeNull();
    expect(findMedia("-jmMROGoZCM", opts)).toMatchObject({ thumbPath: thumb, mediaPath: null });
  });

  it("only resolves files that exist", () => {
    const { root, put } = repo();
    const rec = put("02_Video-Projects/005_Star/r.json", "{}");
    expect(resolveRecordedPath("nope.mp4", rec, root)).toBeNull();
    expect(resolveRecordedPath(undefined, rec, root)).toBeNull();
    const f = put("02_Video-Projects/005_Star/10_Shorts/s.mp4");
    expect(resolveRecordedPath("10_Shorts/s.mp4", rec, root)).toBe(f);
  });
});
