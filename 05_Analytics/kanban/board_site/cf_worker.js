import { adapt } from "./cf_adapter.js";
import checks from "./api/checks.js";
import data from "./api/data.js";
import pair from "./api/pair.js";
import ref from "./api/ref.js";
import watch from "./api/watch.js";
import migration from "./api/migration.js";
const routes = { checks, data, pair, ref, watch, migration };
export default {
  async fetch(request, env) {
    const name = new URL(request.url).pathname.match(/^\/api\/([a-z]+)\/?$/)?.[1];
    // The temporary probe must not inherit bindings from an earlier request.
    const handler = name === "migration" ? (req, res) => migration(req, res, env) : routes[name];
    const response = handler ? await adapt(handler, request, env) : new Response("Not found", { status: 404 });
    response.headers.set("X-Robots-Tag", "noindex, nofollow");
    return response;
  },
};
