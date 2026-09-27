import { createCipheriv, createDecipheriv, randomBytes, createHash, timingSafeEqual } from "crypto";

const ALGO = "aes-256-gcm";
const IV_LEN = 12;

export function validateEncryptionKey(raw?: string | null): Buffer {
  if (!raw || !raw.trim()) {
    throw new Error(
      "ORBIT_TOKEN_ENCRYPTION_KEY is missing. Generate with: openssl rand -base64 32",
    );
  }
  const buf = Buffer.from(raw.trim(), "base64");
  if (buf.length !== 32) {
    throw new Error(
      "ORBIT_TOKEN_ENCRYPTION_KEY must be 32 bytes base64-encoded (openssl rand -base64 32).",
    );
  }
  return buf;
}

export function encryptSecret(plaintext: string, key = process.env.ORBIT_TOKEN_ENCRYPTION_KEY): string {
  const keyBuf = validateEncryptionKey(key);
  const iv = randomBytes(IV_LEN);
  const cipher = createCipheriv(ALGO, keyBuf, iv);
  const encrypted = Buffer.concat([cipher.update(plaintext, "utf8"), cipher.final()]);
  const tag = cipher.getAuthTag();
  return `v1:${iv.toString("base64")}:${tag.toString("base64")}:${encrypted.toString("base64")}`;
}

export function decryptSecret(payload: string, key = process.env.ORBIT_TOKEN_ENCRYPTION_KEY): string {
  const keyBuf = validateEncryptionKey(key);
  const [version, ivB64, tagB64, dataB64] = payload.split(":");
  if (version !== "v1" || !ivB64 || !tagB64 || !dataB64) {
    throw new Error("Invalid encrypted token payload format");
  }
  const decipher = createDecipheriv(ALGO, keyBuf, Buffer.from(ivB64, "base64"));
  decipher.setAuthTag(Buffer.from(tagB64, "base64"));
  const decrypted = Buffer.concat([
    decipher.update(Buffer.from(dataB64, "base64")),
    decipher.final(),
  ]);
  return decrypted.toString("utf8");
}

export function hashState(state: string): string {
  return createHash("sha256").update(state).digest("hex");
}

export function randomUrlSafe(bytes = 32): string {
  return randomBytes(bytes).toString("base64url");
}

export function safeEqual(a: string, b: string): boolean {
  const ab = Buffer.from(a);
  const bb = Buffer.from(b);
  if (ab.length !== bb.length) return false;
  return timingSafeEqual(ab, bb);
}

export function pkceChallenge(verifier: string): string {
  return createHash("sha256").update(verifier).digest("base64url");
}
