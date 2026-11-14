import { adapt } from "./cf_adapter.js";
import checks from "./api/checks.js";
import data from "./api/data.js";
import pair from "./api/pair.js";
import ref from "./api/ref.js";
import watch from "./api/watch.js";
const routes = { checks, data, pair, ref, watch };
export default {
  async fetch(request, env) {
    const name = new URL(request.url).pathname.match(/^\/api\/([a-z]+)\/?$/)?.[1];
    const response = routes[name] ? await adapt(routes[name], request, env) : new Response("Not found", { status: 404 });
    response.headers.set("X-Robots-Tag", "noindex, nofollow");
    return response;
  },
};
