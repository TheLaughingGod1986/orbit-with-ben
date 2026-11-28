// Compatibility endpoint for older board pages. Use the same repository, authentication,
// cache policy and response shape as /api/data?f=ref when the engine moves.
import dataHandler from "./data.js";

export default async function handler(req, res) {
  return dataHandler({ ...req, query: { f: "ref" } }, res);
}
