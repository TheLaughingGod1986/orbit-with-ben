/** Re-export legacy type names expected by older imports. */
export type PublishResult = {
  success: boolean;
  platformPostId?: string;
  platformUrl?: string;
  message: string;
  method: "manual" | "api" | "scheduled_export" | "third_party";
};

export type PublishStatus = {
  status: "draft" | "ready" | "scheduled" | "published" | "failed" | "skipped" | "unknown";
  detail: string;
  connection:
    | "manual_upload_required"
    | "api_available"
    | "api_unavailable"
    | "authentication_expired"
    | "publish_successful"
    | "publishing_failed";
};

export type AdapterPost = {
  id: string;
  platform: string;
  title?: string | null;
  caption?: string | null;
  exportPath?: string | null;
  uploadStatus: string;
};

export interface PublishingAdapter {
  id: string;
  label: string;
  validate(post: AdapterPost): Promise<{ ok: boolean; errors: string[]; warnings: string[] }>;
  publish(post: AdapterPost): Promise<PublishResult>;
  getStatus(postId: string): Promise<PublishStatus>;
}
