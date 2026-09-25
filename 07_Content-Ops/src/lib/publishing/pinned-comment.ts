/**
 * Pinned comment on each long (STUDIO_PLAYBOOK.md §9, added 25 Sep 2026).
 *
 * The subscriber count and the thank-you live here, not in the film: a comment can be
 * edited every week, a film can't. Small counts are not quoted — under the first
 * milestone the thank-you has no number.
 */

export const DEFAULT_MILESTONES = [10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000];

/** Highest milestone the channel has reached, or null below the first one. */
export function lastMilestone(subscribers: number, milestones: number[] = DEFAULT_MILESTONES): number | null {
  const reached = milestones.filter((m) => subscribers >= m);
  return reached.length ? Math.max(...reached) : null;
}

export function buildPinnedCommentText(opts: {
  question: string;
  subscribers: number;
  milestones?: number[];
  cadence?: string;
}): string {
  const milestone = lastMilestone(opts.subscribers, opts.milestones);
  const thanks =
    milestone === null
      ? "Thank you for being here this early. It genuinely helps."
      : `We've just passed ${milestone.toLocaleString("en-GB")} subscribers. Thank you, genuinely.`;
  const cadence = opts.cadence ?? "A new film every Sunday.";
  return `${opts.question.trim()}\n\n${thanks} ${cadence}`;
}
