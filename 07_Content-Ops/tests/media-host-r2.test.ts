import fs from "fs";
import os from "os";
import path from "path";
import { describe, expect, it, vi } from "vitest";
import { isOwnBlobUrl } from "@/lib/publishing/media-host";
import { createR2Host, isOwnR2Url, parseListObjects, r2Config, r2Key } from "@/lib/publishing/media-host-r2";

const PUB = "https://pub-01001dd688b44d358058422d37345434.r2.dev";
const CFG = { accountId: "acct", accessKeyId: "AKID", secretAccessKey: "SECRET", publicUrl: PUB, bucket: "owb-media" };

describe("r2Config", () => {
  it("needs all four keys", () => {
    expect(r2Config({ R2_ACCOUNT_ID: "a", R2_ACCESS_KEY_ID: "b", R2_SECRET_ACCESS_KEY: "c" })).toBeNull();
    expect(r2Config({ R2_ACCOUNT_ID: "a", R2_ACCESS_KEY_ID: "b", R2_SECRET_ACCESS_KEY: "c", R2_PUBLIC_URL: `${PUB}/` })).toEqual({
      accountId: "a",
      accessKeyId: "b",
      secretAccessKey: "c",
      publicUrl: PUB,
      bucket: "owb-media",
    });
  });
});

describe("r2Key", () => {
  it("adds an unguessable tag before the extension", () => {
    expect(r2Key("social/short0000001.mp4", () => "abcd")).toBe("social/short0000001-abcd.mp4");
    expect(r2Key("/social/long-thumb.jpg", () => "ef")).toBe("social/long-thumb-ef.jpg");
  });
});

describe("own media URLs", () => {
  it("only accepts the bucket's own social/ files", () => {
    expect(isOwnR2Url(`${PUB}/social/a.mp4`, PUB)).toBe(true);
    expect(isOwnR2Url(`${PUB}/other/a.mp4`, PUB)).toBe(false);
    expect(isOwnR2Url("https://pub-someone-else.r2.dev/social/a.mp4", PUB)).toBe(false);
    expect(isOwnR2Url(`${PUB}/social/a.mp4`, undefined)).toBe(false);
  });

  it("cleanup accepts both the old Blob store and the R2 bucket", () => {
    expect(isOwnBlobUrl("https://abc.public.blob.vercel-storage.com/social/a.mp4", undefined)).toBe(true);
    expect(isOwnBlobUrl(`${PUB}/social/a.mp4`, PUB)).toBe(true);
    expect(isOwnBlobUrl(`${PUB}/social/a.mp4`, undefined)).toBe(false);
    expect(isOwnBlobUrl("https://example.com/social/a.mp4", PUB)).toBe(false);
  });
});

describe("createR2Host", () => {
  const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "r2-")), "short.mp4");
  fs.writeFileSync(file, "fake mp4");

  it("PUTs the file signed to the S3 endpoint and returns the public URL", async () => {
    const fetchImpl = vi.fn<(req: Request) => Promise<Response>>(async () => new Response("", { status: 200 }));
    const url = await createR2Host(CFG, fetchImpl as unknown as typeof fetch).host(file, "social/short0000001.mp4");
    expect(url).toMatch(new RegExp(`^${PUB}/social/short0000001-[0-9a-f]{16}\\.mp4$`));
    const req = fetchImpl.mock.calls[0][0];
    expect(req.method).toBe("PUT");
    expect(req.url).toMatch(/^https:\/\/acct\.r2\.cloudflarestorage\.com\/owb-media\/social\/short0000001-/);
    expect(req.headers.get("content-type")).toBe("video/mp4");
    expect(req.headers.get("authorization")).toMatch(/^AWS4-HMAC-SHA256 Credential=AKID\//);
  });

  it("fails loudly when R2 refuses the upload", async () => {
    const fetchImpl = vi.fn(async () => new Response("AccessDenied", { status: 403 }));
    await expect(createR2Host(CFG, fetchImpl as unknown as typeof fetch).host(file, "social/x.mp4")).rejects.toThrow(/403/);
  });

  it("refuses to delete anything outside its own social/ files", async () => {
    const fetchImpl = vi.fn<(req: Request) => Promise<Response>>(async () => new Response(null, { status: 204 }));
    const r2 = createR2Host(CFG, fetchImpl as unknown as typeof fetch);
    await expect(r2.deleteMedia("https://example.com/social/a.mp4")).rejects.toThrow(/refusing/);
    await r2.deleteMedia(`${PUB}/social/a-1.mp4`);
    const req = fetchImpl.mock.calls[0][0];
    expect(req.method).toBe("DELETE");
    expect(req.url).toBe("https://acct.r2.cloudflarestorage.com/owb-media/social/a-1.mp4");
  });

  it("lists every page of social/ files", async () => {
    const page1 = `<ListBucketResult><IsTruncated>true</IsTruncated><NextContinuationToken>T2</NextContinuationToken><Contents><Key>social/a.mp4</Key><LastModified>2026-10-21T10:00:00.000Z</LastModified></Contents></ListBucketResult>`;
    const page2 = `<ListBucketResult><IsTruncated>false</IsTruncated><Contents><Key>social/b.jpg</Key><LastModified>2026-10-22T10:00:00.000Z</LastModified></Contents></ListBucketResult>`;
    const fetchImpl = vi.fn().mockResolvedValueOnce(new Response(page1)).mockResolvedValueOnce(new Response(page2));
    const items = await createR2Host(CFG, fetchImpl as unknown as typeof fetch).listMedia();
    expect(items.map((i) => i.url)).toEqual([`${PUB}/social/a.mp4`, `${PUB}/social/b.jpg`]);
    expect((fetchImpl.mock.calls[1][0] as Request).url).toContain("continuation-token=T2");
  });
});

describe("parseListObjects", () => {
  it("reads keys and times", () => {
    const xml = `<Contents><Key>social/x.mp4</Key><LastModified>2026-10-21T00:00:00Z</LastModified></Contents>`;
    expect(parseListObjects(xml, `${PUB}/`)).toEqual([
      { url: `${PUB}/social/x.mp4`, pathname: "social/x.mp4", uploadedAt: new Date("2026-10-21T00:00:00Z") },
    ]);
  });
});
