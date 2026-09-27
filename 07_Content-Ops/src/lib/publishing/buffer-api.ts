/**
 * Buffer GraphQL API client (https://api.buffer.com), used by the automatic mirror.
 * The key is BUFFER_API_KEY (Buffer → Settings → API); it is never logged.
 * Inputs are the same shapes the Buffer MCP takes, so a plan runs through either.
 */

export type BufferPostResult = { id: string; dueAt: string | null; status: string | null };

export interface BufferClient {
  createPost(input: Record<string, unknown>): Promise<BufferPostResult>;
  editPost(input: { postId: string; mode: string; dueAt: string }): Promise<BufferPostResult>;
  deletePost(postId: string): Promise<void>;
}

const ENDPOINT = "https://api.buffer.com";

const POST_FIELDS = `
  __typename
  ... on PostActionSuccess { post { id dueAt status } }
  ... on MutationError { message }
`;

const CREATE = `mutation OrbitCreatePost($input: CreatePostInput!) { createPost(input: $input) { ${POST_FIELDS} } }`;
const EDIT = `mutation OrbitEditPost($input: EditPostInput!) { editPost(input: $input) { ${POST_FIELDS} } }`;
const DELETE = `mutation OrbitDeletePost($input: DeletePostInput!) {
  deletePost(input: $input) { __typename ... on DeletePostSuccess { id } ... on MutationError { message } }
}`;

type Fetch = typeof fetch;

/** MCP-shaped create_post input → GraphQL CreatePostInput. */
export function toCreatePostInput(input: Record<string, unknown>): Record<string, unknown> {
  return { needsApproval: false, source: "orbit-with-ben", ...input, assets: input.assets ?? [] };
}

export function createBufferApiClient(apiKey: string, fetchImpl: Fetch = fetch): BufferClient {
  if (!apiKey) throw new Error("BUFFER_API_KEY is not set");

  async function call(query: string, input: Record<string, unknown>) {
    const res = await fetchImpl(ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${apiKey}` },
      body: JSON.stringify({ query, variables: { input } }),
    });
    const text = await res.text();
    let body: { data?: Record<string, Record<string, unknown>>; errors?: { message?: string }[] };
    try {
      body = JSON.parse(text);
    } catch {
      throw new Error(`Buffer API ${res.status}: ${text.slice(0, 200)}`);
    }
    if (!res.ok || body.errors?.length) {
      const msg = body.errors?.map((e) => e.message).join("; ") || text.slice(0, 200);
      throw new Error(`Buffer API ${res.status}: ${msg}`);
    }
    const payload = body.data ? Object.values(body.data)[0] : undefined;
    if (!payload) throw new Error("Buffer API: empty response");
    if (typeof payload.message === "string") throw new Error(`Buffer ${payload.__typename}: ${payload.message}`);
    return payload;
  }

  function post(payload: Record<string, unknown>): BufferPostResult {
    const p = payload.post as { id?: string; dueAt?: string | null; status?: string | null } | undefined;
    if (!p?.id) throw new Error(`Buffer ${String(payload.__typename)}: no post returned`);
    return { id: p.id, dueAt: p.dueAt ?? null, status: p.status ?? null };
  }

  return {
    async createPost(input) {
      return post(await call(CREATE, toCreatePostInput(input)));
    },
    async editPost({ postId, mode, dueAt }) {
      return post(await call(EDIT, { id: postId, mode, dueAt }));
    },
    async deletePost(postId) {
      await call(DELETE, { id: postId });
    },
  };
}
