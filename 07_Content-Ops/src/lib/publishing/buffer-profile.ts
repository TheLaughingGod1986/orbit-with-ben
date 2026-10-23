/**
 * The two YouTube channels the Buffer mirror serves (J0817, Ben 21 Oct 2026: "can we look at why buffer for hos and
 * owb is not working"). Each profile has its own Buffer organisation, key, networks, YouTube login and records, so
 * an Orbit post can never reach History of Science or the reverse.
 *
 * - owb: Orbit With Ben. Instagram, Facebook, Threads; Shorts and longs. Records in social/.
 * - hos: History of Science (HOS AGENTS.md "Social posting", 5 Oct 2026). Shorts only; Instagram, Facebook and
 *   TikTok (no Threads); its own Buffer org and BUFFER_HOS_API_KEY; the read-only HOS YouTube login the channel
 *   tracker already uses. Records in social/hos/, media under social/hos/ on R2.
 *
 * Ids are not secret. Keys stay in 07_Content-Ops/.env.
 */
import path from "path";
import type { BufferChannel } from "@/lib/publishing/buffer-mirror";

export type ProfileId = "owb" | "hos";

export type BufferProfile = {
  id: ProfileId;
  name: string;
  /** The Buffer organisation every channel must belong to. */
  organizationId: string;
  /** The Buffer channel ids this profile may post to, by network. The guard refuses any other id. */
  channelIds: Partial<Record<BufferChannel, string>>;
  networks: readonly BufferChannel[];
  shortsOnly: boolean;
  /** .env name of the Buffer key. */
  keyEnv: string;
  /** .env name of the YouTube refresh token, and the channel it must belong to (null: not checked). */
  youtubeTokenEnv: string;
  youtubeChannelId: string | null;
  /** Repo-relative folder holding BUFFER_CHANNELS.json, BUFFER_POSTS.json, UPLOADS.json and buffer-plans/. */
  socialDir: string;
  /** Hosted media path prefix. Each profile only lists, adopts and sweeps its own. */
  mediaPrefix: string;
  /** Look for uploads in 02_Video-Projects records too (Orbit's own films only). */
  scanProjects: boolean;
};

const SOCIAL = "00_Brand/Channel-Setup/social";

export const PROFILES: Record<ProfileId, BufferProfile> = {
  owb: {
    id: "owb",
    name: "Orbit With Ben",
    organizationId: "6ab9206ad1f589b389040174",
    channelIds: { instagram: "6ab920b2ea19ca0bde03abff", facebook: "6ab92149ea19ca0bde03af77", threads: "6ab92127ea19ca0bde03aead" },
    networks: ["instagram", "facebook", "threads"],
    shortsOnly: false,
    keyEnv: "BUFFER_API_KEY",
    youtubeTokenEnv: "YOUTUBE_REFRESH_TOKEN",
    youtubeChannelId: null,
    socialDir: SOCIAL,
    mediaPrefix: "social/",
    scanProjects: true,
  },
  hos: {
    id: "hos",
    name: "History of Science",
    organizationId: "6431f03385378b838b780157",
    channelIds: { instagram: "6ac36d3c6a5c39ccb61d3b5f", facebook: "6ac369f16a5c39ccb61d223b", tiktok: "6ac381bc6a5c39ccb61dd8aa" },
    networks: ["instagram", "facebook", "tiktok"],
    shortsOnly: true,
    keyEnv: "BUFFER_HOS_API_KEY",
    youtubeTokenEnv: "YT_ANALYTICS_REFRESH_TOKEN_HOS",
    youtubeChannelId: "UCXp7HkBIl1LgaznXuZHJyRg",
    socialDir: `${SOCIAL}/hos`,
    mediaPrefix: "social/hos/",
    scanProjects: false,
  },
};

export function getProfile(id: string | undefined): BufferProfile {
  const key = (id ?? "owb").toLowerCase();
  if (!(key in PROFILES)) throw new Error(`unknown channel ${id}: use owb or hos`);
  return PROFILES[key as ProfileId];
}

export function profileFiles(profile: BufferProfile, repoRoot: string) {
  const dir = path.join(repoRoot, profile.socialDir);
  return {
    dir,
    channels: path.join(dir, "BUFFER_CHANNELS.json"),
    ledger: path.join(dir, "BUFFER_POSTS.json"),
    uploads: path.join(dir, "UPLOADS.json"),
    plans: path.join(dir, "buffer-plans"),
  };
}

/**
 * Why a post to this Buffer channel id is refused, or null when it is one of the profile's own.
 * An id that belongs to another profile is named, so a crossed wire is obvious in the log.
 */
export function refuseChannel(profile: BufferProfile, channelId: unknown): string | null {
  const id = typeof channelId === "string" ? channelId : "";
  if (Object.values(profile.channelIds).includes(id)) return null;
  const other = Object.values(PROFILES).find((p) => p.id !== profile.id && Object.values(p.channelIds).includes(id));
  return other
    ? `Refusing a ${profile.name} post to ${other.name}'s Buffer channel ${id}`
    : `Refusing a post to Buffer channel ${id || "(none)"}: not one of ${profile.name}'s channels in org ${profile.organizationId}`;
}

/** The channel ids from a profile's BUFFER_CHANNELS.json, checked against the profile: wrong org or id throws. */
export function checkChannelsFile(
  profile: BufferProfile,
  cfg: { organizationId?: string; channels?: Record<string, { id?: string }> },
): Partial<Record<BufferChannel, string>> {
  if (cfg.organizationId && cfg.organizationId !== profile.organizationId) {
    throw new Error(`${profile.socialDir}/BUFFER_CHANNELS.json names org ${cfg.organizationId}, not ${profile.name}'s ${profile.organizationId}`);
  }
  const ids: Partial<Record<BufferChannel, string>> = {};
  for (const c of profile.networks) {
    const id = cfg.channels?.[c]?.id;
    if (!id) continue;
    const refused = refuseChannel(profile, id);
    if (refused) throw new Error(`${profile.socialDir}/BUFFER_CHANNELS.json ${c}: ${refused}`);
    ids[c] = id;
  }
  return ids;
}

/** Hosted path to the YouTube id it was uploaded for: <prefix><11-character id><suffix>. Null outside the prefix. */
export function videoIdFromMediaPath(pathname: string, prefix: string): string | null {
  if (!pathname.startsWith(prefix)) return null;
  const m = /^([\w-]{11})/.exec(pathname.slice(prefix.length));
  return m ? m[1] : null;
}

/** A hosted file another profile owns (its prefix is nested inside this one's), which this profile must leave alone. */
export function ownedByOtherProfile(pathname: string, profile: BufferProfile): boolean {
  return Object.values(PROFILES).some(
    (p) => p.id !== profile.id && p.mediaPrefix.length > profile.mediaPrefix.length && pathname.startsWith(p.mediaPrefix),
  );
}
