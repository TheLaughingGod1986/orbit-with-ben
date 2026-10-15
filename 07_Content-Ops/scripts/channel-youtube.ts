/**
 * Orbit With Ben's half of the shared YouTube scripts (studio core, Ben 15 Oct 2026: "unify HOS and OWB but keeping
 * their own rules"). Core scripts (retitle-videos.ts, update-pinned-comment.ts) import these three hooks; each repo
 * keeps its own copy of this file, so how a channel signs in and guards its desk stays the channel's own.
 */
export { ensureDeskLock as beforeRun } from "./with-desk-lock";
export { getYouTubeAccessToken as youtubeAccessToken } from "../src/lib/youtube/data-api";

export async function afterRun(): Promise<void> {}
