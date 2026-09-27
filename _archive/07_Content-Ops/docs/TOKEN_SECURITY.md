# Token Security

## Encryption

OAuth access and refresh tokens are encrypted at rest with **AES-256-GCM**.

- Key env: `ORBIT_TOKEN_ENCRYPTION_KEY` (32 bytes, **base64**-encoded)
- Format stored: `v1:<iv_b64>:<tag_b64>:<ciphertext_b64>`
- Fresh IV per encryption
- Decrypt only on the server immediately before API calls
- Never returned to the browser

## Generate a key

```bash
openssl rand -base64 32
```

Add to `.env` (never commit):

```env
ORBIT_TOKEN_ENCRYPTION_KEY=<output>
```

## Production behaviour

If `NODE_ENV=production` and the key is missing, server env validation fails closed via `requireEncryptionKeyInProduction()`.

## OAuth state

- Cryptographically random state
- SHA-256 hashed before storage
- Single-use (`usedAt`)
- Short TTL (default 10 minutes)
- PKCE supported for TikTok and X

## Logging

Never log access tokens, refresh tokens, client secrets, authorisation codes, or the encryption key. Use `redactSummary()` before persisting API responses.
