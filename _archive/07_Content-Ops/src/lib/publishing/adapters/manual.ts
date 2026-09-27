import {
  ConnectionValidationResult,
  ExternalPublishStatus,
  LegacyAdapterPost,
  LegacyPublishResult,
  LegacyPublishStatus,
  PlatformCapabilities,
  PlatformConnectionRecord,
  PlatformPostRecord,
  PublishingAdapter,
  PublishingContext,
  PublishResult,
} from "@/lib/publishing/types";

export class ManualPublishingAdapter implements PublishingAdapter {
  platform = "manual" as const;
  id: string;
  label: string;

  constructor(id = "manual", label = "Manual") {
    this.id = id;
    this.label = label;
  }

  getCapabilities(): PlatformCapabilities {
    return {
      canConnect: false,
      canUploadVideo: false,
      canPublishDirectly: false,
      canUploadDraft: false,
      canScheduleNatively: false,
      canSetThumbnail: false,
      canSetPrivacy: false,
      canReadPublishStatus: false,
      canRetrievePostUrl: false,
      canDeletePost: false,
      requiresAppReview: false,
      requiresManualCompletion: true,
      limitations: ["Manual upload required — use export package"],
    };
  }

  async validateConnection(): Promise<ConnectionValidationResult> {
    return {
      ok: false,
      status: "unsupported",
      capabilities: this.getCapabilities(),
      errors: ["Manual adapter has no OAuth connection"],
      warnings: [],
    };
  }

  async validatePost(post: PlatformPostRecord) {
    const errors: string[] = [];
    if (!post.caption && !post.title) errors.push("Title or caption required");
    return {
      ok: errors.length === 0,
      errors,
      warnings: post.exportPath ? [] : ["No export path set — upload the clean source file manually"],
    };
  }

  async publish(
    post: PlatformPostRecord,
    _connection: PlatformConnectionRecord,
    context: PublishingContext,
  ): Promise<PublishResult> {
    if (context.dryRun) {
      return {
        success: true,
        published: false,
        message: "Dry-run: manual package would be prepared",
        method: "dry_run",
      };
    }
    return {
      success: false,
      published: false,
      message:
        "Manual upload required. Export the package, upload in the platform UI, then record the published URL in Content Ops.",
      method: "manual",
      requiresManualCompletion: true,
    };
  }

  async getExternalStatus(): Promise<ExternalPublishStatus> {
    return { status: "manual_action_required", detail: "Track URL manually after upload" };
  }

  /** Legacy helpers for existing UI/tests */
  async validate(post: LegacyAdapterPost) {
    const errors: string[] = [];
    const warnings: string[] = [];
    if (!post.caption && !post.title) errors.push("Title or caption required");
    if (!post.exportPath) warnings.push("No export path set — upload the clean source file manually");
    warnings.push("Manual upload required — API publishing is not enabled for this adapter");
    return { ok: errors.length === 0, errors, warnings };
  }

  async legacyPublish(post: LegacyAdapterPost): Promise<LegacyPublishResult> {
    const validation = await this.validate(post);
    if (!validation.ok) {
      return { success: false, message: validation.errors.join("; "), method: "manual" };
    }
    return {
      success: false,
      message:
        "Manual upload required. Export the package, upload in the platform UI, then record the published URL in Content Ops.",
      method: "manual",
    };
  }

  async legacyGetStatus(): Promise<LegacyPublishStatus> {
    return {
      status: "unknown",
      detail: "No live API status — track URLs manually after upload.",
      connection: "manual_upload_required",
    };
  }
}
