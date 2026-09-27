# Publishing adapters

Shared interface (`src/lib/publishing/adapters.ts`):

```ts
interface PublishingAdapter {
  validate(post): Promise<ValidationResult>;
  publish(post): Promise<PublishResult>;
  getStatus(postId): Promise<PublishStatus>;
}
```

## v1 adapters

| Adapter | Behaviour |
|---------|-----------|
| ManualPublishingAdapter | Always requires manual upload |
| YouTubeAdapter | Detects env credentials; does not fake publish |
| TikTokAdapter | Manual; marks API unavailable even if keys present |
| MetaAdapter | Manual for IG/FB Reels |
| XAdapter | Detects keys; publish not enabled |

`publish()` never returns a fake success. Successful distribution in v1 means:

1. Export package created
2. Human uploads
3. URL recorded on the PlatformPost

## Adding a real API later

1. Implement `PublishingAdapter` for the platform
2. Read tokens only from `process.env`
3. Wire `getAdapterForPlatform`
4. Keep manual fallback when auth expires
5. Add tests for expired credentials / validation failures
