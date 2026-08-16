/**
 * Honest labels from existing LongFormVideo fields only.
 *
 * Video Auditor:
 * - /videos is a film list forever — never /go/, Amazon, or a shop module here.
 * - Named-in-film (if marked): only `Named: {book title}` — no slug, no link.
 * - Shorts never get a book line.
 * - Private cuts must not win next/this Thursday:
 *   last-star v09 (`dbBojuwg4r8`), v10 (`z-fUtdjWn5o`); Europa private (`3_W_jl2GR8w`).
 * - Live named cuts: last-star v11 (`REXYxuLOBoI` — letter O, not zero), Europa v02 (`NbW5G1BpPY0`).
 */

/** Auditor-confirmed named-in-film longs. Book title text only — no /go/. */
const NAMED_IN_FILM_BY_YOUTUBE_ID: Record<string, string> = {
  REXYxuLOBoI: "The End of Everything",
  NbW5G1BpPY0: "Alien Oceans",
};

/** Private cuts — must not win “next Thursday” / “this film”. */
const PRIVATE_NOT_NEXT_YOUTUBE_IDS = new Set([
  "dbBojuwg4r8", // last-star v09
  "z-fUtdjWn5o", // last-star v10
  "3_W_jl2GR8w", // Europa private (not v02)
]);

export function resolveYoutubeId(video: {
  youtubeVideoId: string | null;
  youtubeUrl: string | null;
}): string | null {
  const stored = video.youtubeVideoId?.trim();
  if (stored) return stored;
  const url = video.youtubeUrl?.trim();
  if (!url) return null;
  try {
    const u = new URL(url);
    if (u.hostname.includes("youtu.be")) {
      const id = u.pathname.replace(/^\//, "").split("/")[0];
      return id || null;
    }
    const v = u.searchParams.get("v");
    if (v) return v;
  } catch {
    return null;
  }
  return null;
}

/**
 * One-line Auditor status. No privacy field on LongFormVideo —
 * never claim "private" or "live" without status=published.
 * Visible commerce on /videos: none (Film-only), aside from optional Named title text.
 */
export function auditorFilmStatusLine(video: {
  status: string;
  youtubeVideoId: string | null;
  youtubeUrl: string | null;
}): string {
  if (video.status === "published") return "Long · Film-only · Published";
  if (video.status === "scheduled") return "Long · Film-only · Scheduled";
  return "Long · Film-only · Not published";
}

/**
 * Auditor named-in-film mark (title text only).
 * Returns `Named: …` or null. Never a slug or link.
 */
export function namedInFilmBookLine(video: {
  youtubeVideoId: string | null;
  youtubeUrl: string | null;
}): string | null {
  const ytId = resolveYoutubeId(video);
  if (ytId && NAMED_IN_FILM_BY_YOUTUBE_ID[ytId]) {
    return `Named: ${NAMED_IN_FILM_BY_YOUTUBE_ID[ytId]}`;
  }
  return null;
}

/** True when this cut must not be the next/this Thursday hero (private cuts). */
export function excludeFromNextThursdayHero(video: {
  youtubeVideoId: string | null;
  youtubeUrl: string | null;
}): boolean {
  const ytId = resolveYoutubeId(video);
  return Boolean(ytId && PRIVATE_NOT_NEXT_YOUTUBE_IDS.has(ytId));
}
