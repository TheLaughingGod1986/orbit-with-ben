// Bounded publisher edits keep minute polls small. Keep the untouched transport copy separate from UI normalisation.
(function () {
  let raw = null, revision = "", busy = null;
  function apply(value, ops) {
    const result = structuredClone(value);
    for (const [kind, path, ...args] of ops) {
      if (path.some(k => ["__proto__", "prototype", "constructor"].includes(String(k)))) throw new Error("Unsafe update path");
      let parent = result;
      for (const key of path.slice(0, -1)) parent = parent[key];
      const key = path[path.length - 1];
      if (kind === "setMany") {
        const [indices, suffix, value] = args;
        if (suffix.some(k => ["__proto__", "prototype", "constructor"].includes(String(k)))) throw new Error("Unsafe update path");
        const list = path.length ? parent[key] : result;
        for (const index of indices) {
          if (!Number.isInteger(index) || index < 0 || index >= list.length) throw new Error("Invalid update index");
          let item = list;
          const target = [index, ...suffix];
          for (const part of target.slice(0, -1)) item = item[part];
          item[target[target.length - 1]] = structuredClone(value);
        }
      } else if (kind === "splice") {
        const list = path.length ? parent[key] : result;
        list.splice(args[0], args[1], ...args[2]);
      } else if (kind === "delete") delete parent[key];
      else if (kind === "set" && path.length) parent[key] = args[0];
      else throw new Error("Invalid update");
    }
    return result;
  }
  window.__boardUpdates = async function (sha, own, full) {
    if (busy) return busy;
    busy = (async () => {
      let update = null, commit = sha;
      try {
        const response = await own("f=updates", "no-cache");
        if (response.ok) {
          update = await response.json();
          if (update.schema === 2 && update.encoding === "gzip-base64") {
            const bytes = Uint8Array.from(atob(update.payload), c => c.charCodeAt(0));
            const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream("gzip"));
            update = await new Response(stream).json();
          }
          commit = ""; // Branch reads avoid the rate-limited GitHub commit lookup.
          if (update.schema !== 1 || !Array.isArray(update.edits)) update = null;
        }
      } catch (e) { if (e && e.signIn) throw e; }
      if (update && raw) {
        // The CDN may serve an older branch copy while revalidating it. Keep the
        // newer snapshot rather than treating a backward update as missed history.
        if (Date.parse(update.publishedAt) < Date.parse(raw.publishedAt)) {
          return new Response(JSON.stringify(raw));
        }
        let next = raw, at = revision;
        try {
          for (const edit of update.edits) if (edit.from === at) { next = apply(next, edit.ops); at = edit.to; }
          if (at === update.revision) { raw = next; revision = at; return new Response(JSON.stringify(raw)); }
        } catch (e) { /* a missed or incompatible update gets the full file */ }
      }
      const response = await full(commit);
      if (!response.ok) return response;
      raw = await response.json();
      const served = response.headers.get("X-Board-Sha");
      const etag = (response.headers.get("ETag") || "").replace(/^W\//, "").replaceAll('"', "");
      revision = update && ((update.snapshotEtag && etag === update.snapshotEtag) || (served && served === commit)) ? update.revision : "";
      // Independent branch caches can return a slightly older snapshot. Identify it exactly
      // from the retained history, then let the next poll replay forward instead of downloading again.
      if (!revision && update && Array.isArray(update.edits)) {
        const match = update.edits.find(edit => edit.fromEtag && edit.fromEtag === etag);
        if (match) revision = match.from;
      }
      return new Response(JSON.stringify(raw));
    })();
    try { return (await busy).clone(); } finally { busy = null; }
  };
  window.__applyBoardEdits = apply;
})();
