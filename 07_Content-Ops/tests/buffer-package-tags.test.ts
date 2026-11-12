import fs from "fs";
import os from "os";
import path from "path";
import { afterEach, expect, it } from "vitest";
import { registeredPackageTags } from "../src/lib/publishing/buffer-deps";
const roots: string[] = [];
afterEach(() => { for (const root of roots.splice(0)) fs.rmSync(root, {recursive:true,force:true}); });
it("uses the exact registered package tags and rejects missing or foreign paths", () => {
 const root = fs.mkdtempSync(path.join(os.tmpdir(),"buffer-tags-")); roots.push(root);
 const dir=path.join(root,"package");fs.mkdirSync(dir);
 fs.writeFileSync(path.join(dir,"PACKAGE_MANIFEST.json"),JSON.stringify({tags:["mars rover","nasa mars"]}));
 expect(registeredPackageTags(root,"package")).toEqual(["mars rover","nasa mars"]);
 expect(registeredPackageTags(root,undefined)).toEqual([]);
 expect(registeredPackageTags(root,"../elsewhere")).toEqual([]);
 fs.writeFileSync(path.join(dir,"tags.txt"),"mars rover,nasa mars");
 fs.writeFileSync(path.join(dir,"PACKAGE_MANIFEST.json"),JSON.stringify({tagsFile:"tags.txt"}));
 expect(registeredPackageTags(root,"package")).toEqual(["mars rover","nasa mars"]);
});
