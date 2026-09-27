-- CreateTable
CREATE TABLE "BufferMirrorPost" (
    "id" TEXT NOT NULL,
    "youtubeVideoId" TEXT NOT NULL,
    "channel" TEXT NOT NULL,
    "bufferPostId" TEXT NOT NULL,
    "kind" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "dueAt" TIMESTAMP(3),
    "mode" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "BufferMirrorPost_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "BufferMirrorPost_dueAt_idx" ON "BufferMirrorPost"("dueAt");

-- CreateIndex
CREATE UNIQUE INDEX "BufferMirrorPost_youtubeVideoId_channel_key" ON "BufferMirrorPost"("youtubeVideoId", "channel");

