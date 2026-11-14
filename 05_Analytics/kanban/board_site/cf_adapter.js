// Bridge the existing Node-style handlers to Pages without changing their contracts.
export async function adapt(handler, request, env = {}) {
  // Compatibility dates after 2025-04-01 populate process.env. Also support local tests.
  for (const [key, value] of Object.entries(env)) {
    if (typeof value === "string") process.env[key] = value;
  }
  const url = new URL(request.url);
  const headers = Object.fromEntries(request.headers);
  headers.host = url.host;
  // Do not accept a client-supplied forwarded host for origin checks.
  headers["x-forwarded-host"] = url.host;
  if (headers["cf-connecting-ip"]) headers["x-real-ip"] = headers["cf-connecting-ip"];
  const req = { method: request.method, headers, query: Object.fromEntries(url.searchParams) };
  if (!["GET", "HEAD"].includes(request.method)) req.body = await request.text();
  let status = 200, body = null;
  const responseHeaders = new Headers();
  const res = {
    setHeader(key, value) {
      responseHeaders.delete(key);
      for (const item of (Array.isArray(value) ? value : [value])) responseHeaders.append(key, String(item));
      return this;
    },
    status(code) { status = code; return this; },
    json(value) { this.setHeader("Content-Type", "application/json; charset=utf-8"); body = JSON.stringify(value); return this; },
    send(value) { body = value; return this; },
    end(value = null) { body = value; return this; },
  };
  await handler(req, res);
  const response = new Response(request.method === "HEAD" || [204, 205, 304].includes(status) ? null : body,
    { status, headers: responseHeaders });
  if (!responseHeaders.has("Content-Type")) response.headers.delete("Content-Type");
  return response;
}
