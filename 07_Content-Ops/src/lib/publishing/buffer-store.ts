/**
 * Where the Buffer mirror remembers what it posted: 00_Brand/Channel-Setup/social/BUFFER_POSTS.json.
 * Each video is posted once per channel; the file lets `check` move or remove posts later.
 */
import fs from "fs";
import path from "path";
import { recordPost, setEntryMedia, type BufferChannel, type Ledger, type Plan } from "@/lib/publishing/buffer-mirror";

export interface BufferStore {
  load(): Promise<Ledger>;
  /** postId null removes the channel's entry. */
  record(plan: Pick<Plan, "videoId" | "kind" | "title" | "timing">, channel: BufferChannel, postId: string | null): Promise<void>;
  /** Remember the Blob copies behind a video; an empty list forgets them. */
  setMedia(videoId: string, urls: string[]): Promise<void>;
}

export function createFileBufferStore(file: string, now: () => Date = () => new Date()): BufferStore {
  const read = (): Ledger => (fs.existsSync(file) ? (JSON.parse(fs.readFileSync(file, "utf8")) as Ledger) : { version: 1, videos: {} });
  const write = (ledger: Ledger) => {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, JSON.stringify(ledger, null, 2) + "\n");
  };
  return {
    async load() {
      return read();
    },
    async record(plan, channel, postId) {
      write(recordPost(read(), plan, channel, postId, now()));
    },
    async setMedia(videoId, urls) {
      write(setEntryMedia(read(), videoId, urls));
    },
  };
}
