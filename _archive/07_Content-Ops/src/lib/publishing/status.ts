const CLIP_TRANSITIONS: Record<string, string[]> = {
  proposed: ["approved", "rejected", "proposed"],
  approved: ["editing", "rejected", "proposed"],
  editing: ["exported", "approved"],
  exported: ["scheduled", "editing"],
  scheduled: ["published", "exported"],
  published: ["published"],
  rejected: ["proposed"],
};

const POST_TRANSITIONS: Record<string, string[]> = {
  draft: ["ready", "skipped"],
  ready: ["scheduled", "draft", "skipped"],
  scheduled: ["published", "failed", "ready"],
  published: ["published"],
  failed: ["ready", "draft"],
  skipped: ["draft"],
};

export function canTransitionClip(from: string, to: string): boolean {
  return (CLIP_TRANSITIONS[from] || []).includes(to);
}

export function canTransitionPost(from: string, to: string): boolean {
  return (POST_TRANSITIONS[from] || []).includes(to);
}

export function assertClipTransition(from: string, to: string): void {
  if (!canTransitionClip(from, to)) {
    throw new Error(`Invalid clip status transition: ${from} → ${to}`);
  }
}

export function assertPostTransition(from: string, to: string): void {
  if (!canTransitionPost(from, to)) {
    throw new Error(`Invalid post status transition: ${from} → ${to}`);
  }
}
