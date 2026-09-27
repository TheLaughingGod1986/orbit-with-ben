import { prisma } from "@/lib/storage/prisma";
import { encryptSecret, hashState, randomUrlSafe, pkceChallenge } from "@/lib/security/token-crypto";

const STATE_TTL_MS = 10 * 60 * 1000;

export async function createOAuthState(input: {
  platform: string;
  redirectPath?: string;
  withPkce?: boolean;
}): Promise<{ state: string; codeVerifier?: string; codeChallenge?: string }> {
  const state = randomUrlSafe(32);
  const codeVerifier = input.withPkce ? randomUrlSafe(48) : undefined;
  await prisma.oAuthState.create({
    data: {
      platform: input.platform,
      stateHash: hashState(state),
      codeVerifierEncrypted: codeVerifier ? encryptSecret(codeVerifier) : null,
      redirectPath: input.redirectPath || "/settings/connections",
      expiresAt: new Date(Date.now() + STATE_TTL_MS),
    },
  });
  return {
    state,
    codeVerifier,
    codeChallenge: codeVerifier ? pkceChallenge(codeVerifier) : undefined,
  };
}

export async function consumeOAuthState(input: {
  platform: string;
  state: string;
}): Promise<{ ok: true; codeVerifier?: string; redirectPath?: string } | { ok: false; error: string }> {
  const stateHash = hashState(input.state);
  const row = await prisma.oAuthState.findUnique({ where: { stateHash } });
  if (!row) return { ok: false, error: "invalid_state" };
  if (row.platform !== input.platform) return { ok: false, error: "state_platform_mismatch" };
  if (row.usedAt) return { ok: false, error: "state_already_used" };
  if (row.expiresAt.getTime() < Date.now()) return { ok: false, error: "state_expired" };

  await prisma.oAuthState.update({
    where: { id: row.id },
    data: { usedAt: new Date() },
  });

  let codeVerifier: string | undefined;
  if (row.codeVerifierEncrypted) {
    const { decryptSecret } = await import("@/lib/security/token-crypto");
    codeVerifier = decryptSecret(row.codeVerifierEncrypted);
  }

  return { ok: true, codeVerifier, redirectPath: row.redirectPath || undefined };
}
