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
      if (kind === "splice") {
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
        const response = await own("f=updates" + (sha ? "&sha=" + sha : ""), "no-cache");
        if (response.ok) {
          update = await response.json();
          commit = response.headers.get("X-Board-Sha") || sha;
          if (update.schema !== 1 || !Array.isArray(update.edits)) update = null;
        }
      } catch (e) { if (e && e.signIn) throw e; }
      if (update && raw) {
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
      revision = update && served === commit ? update.revision : "";
      return new Response(JSON.stringify(raw));
    })();
    try { return (await busy).clone(); } finally { busy = null; }
  };
  window.__applyBoardEdits = apply;
})();
