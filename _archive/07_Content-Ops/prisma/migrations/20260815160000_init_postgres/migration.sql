-- CreateTable
CREATE TABLE "LongFormVideo" (
    "id" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "workingTitle" TEXT,
    "slug" TEXT NOT NULL,
    "topic" TEXT NOT NULL,
    "category" TEXT,
    "status" TEXT NOT NULL DEFAULT 'idea',
    "script" TEXT,
    "summary" TEXT,
    "youtubeUrl" TEXT,
    "youtubeVideoId" TEXT,
    "thumbnailPath" TEXT,
    "finalVideoPath" TEXT,
    "durationSeconds" INTEGER,
    "publicationDate" TIMESTAMP(3),
    "primaryKeyword" TEXT,
    "secondaryKeywords" TEXT,
    "targetAudience" TEXT,
    "projectFolder" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "LongFormVideo_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ShortClip" (
    "id" TEXT NOT NULL,
    "longFormVideoId" TEXT NOT NULL,
    "clipNumber" INTEGER NOT NULL,
    "workingTitle" TEXT NOT NULL,
    "hook" TEXT,
    "hookCategory" TEXT,
    "transcript" TEXT,
    "sourceStartTime" TEXT,
    "sourceEndTime" TEXT,
    "targetDurationSeconds" INTEGER,
    "visualDirection" TEXT,
    "onScreenText" TEXT,
    "endingLine" TEXT,
    "callToAction" TEXT,
    "whyItWorks" TEXT,
    "exportPath" TEXT,
    "thumbnailPath" TEXT,
    "fileChecksum" TEXT,
    "status" TEXT NOT NULL DEFAULT 'proposed',
    "qualityScore" INTEGER,
    "qualityBreakdown" TEXT,
    "sortOrder" INTEGER NOT NULL DEFAULT 0,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "ShortClip_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "PlatformPost" (
    "id" TEXT NOT NULL,
    "shortClipId" TEXT NOT NULL,
    "platform" TEXT NOT NULL,
    "title" TEXT,
    "caption" TEXT,
    "hashtags" TEXT,
    "callToAction" TEXT,
    "scheduledAt" TIMESTAMP(3),
    "publishedAt" TIMESTAMP(3),
    "platformPostId" TEXT,
    "platformUrl" TEXT,
    "uploadStatus" TEXT NOT NULL DEFAULT 'draft',
    "publishingMethod" TEXT NOT NULL DEFAULT 'manual',
    "notes" TEXT,
    "pinnedComment" TEXT,
    "coverText" TEXT,
    "storyCaption" TEXT,
    "commentPrompt" TEXT,
    "repostReason" TEXT,
    "approvedForPublish" BOOLEAN NOT NULL DEFAULT false,
    "privacyStatus" TEXT,
    "madeForKids" BOOLEAN,
    "containsSyntheticMedia" BOOLEAN,
    "mediaChecksum" TEXT,
    "mediaFilePath" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "PlatformPost_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "PerformanceMetric" (
    "id" TEXT NOT NULL,
    "platformPostId" TEXT NOT NULL,
    "recordedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "views" INTEGER,
    "impressions" INTEGER,
    "likes" INTEGER,
    "comments" INTEGER,
    "shares" INTEGER,
    "saves" INTEGER,
    "averageWatchTime" DOUBLE PRECISION,
    "averagePercentageViewed" DOUBLE PRECISION,
    "completionRate" DOUBLE PRECISION,
    "profileVisits" INTEGER,
    "linkClicks" INTEGER,
    "subscribersGained" INTEGER,
    "followersGained" INTEGER,
    "engagementRate" DOUBLE PRECISION,
    "clickThroughRate" DOUBLE PRECISION,
    "retention30s" DOUBLE PRECISION,
    "retentionDropAtSeconds" DOUBLE PRECISION,
    "retentionDropDepth" DOUBLE PRECISION,
    "returningViewers" INTEGER,
    "newViewers" INTEGER,
    "browsePercent" DOUBLE PRECISION,
    "suggestedPercent" DOUBLE PRECISION,
    "searchPercent" DOUBLE PRECISION,
    "endScreenCtr" DOUBLE PRECISION,
    "cardsCtr" DOUBLE PRECISION,
    "averageSessionSeconds" DOUBLE PRECISION,
    "importSource" TEXT,
    "importBatchId" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "PerformanceMetric_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ContentInsight" (
    "id" TEXT NOT NULL,
    "type" TEXT NOT NULL,
    "topic" TEXT,
    "platform" TEXT,
    "finding" TEXT NOT NULL,
    "evidence" TEXT,
    "confidence" DOUBLE PRECISION,
    "recommendedAction" TEXT,
    "sampleSize" INTEGER,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "ContentInsight_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "PlatformSettings" (
    "id" TEXT NOT NULL,
    "platform" TEXT NOT NULL,
    "enabled" BOOLEAN NOT NULL DEFAULT true,
    "accountDisplayName" TEXT,
    "profileUrl" TEXT,
    "defaultHashtags" TEXT,
    "defaultCallToAction" TEXT,
    "publishingMethod" TEXT NOT NULL DEFAULT 'manual',
    "postingTimesJson" TEXT,
    "connectionStatus" TEXT NOT NULL DEFAULT 'manual_only',
    "tokenStatus" TEXT NOT NULL DEFAULT 'not_configured',
    "lastSuccessfulPublish" TIMESTAMP(3),
    "defaultVisibility" TEXT NOT NULL DEFAULT 'public',
    "analyticsImportNotes" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "PlatformSettings_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ContentTemplate" (
    "id" TEXT NOT NULL,
    "key" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "platform" TEXT,
    "body" TEXT NOT NULL,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "ContentTemplate_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AnalyticsImport" (
    "id" TEXT NOT NULL,
    "platform" TEXT NOT NULL,
    "filename" TEXT NOT NULL,
    "importedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "rowCount" INTEGER NOT NULL,
    "successCount" INTEGER NOT NULL,
    "errorCount" INTEGER NOT NULL,
    "errorsJson" TEXT,
    "notes" TEXT,

    CONSTRAINT "AnalyticsImport_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AppSetting" (
    "id" TEXT NOT NULL,
    "key" TEXT NOT NULL,
    "value" TEXT NOT NULL,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "AppSetting_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "PlatformConnection" (
    "id" TEXT NOT NULL,
    "platform" TEXT NOT NULL,
    "accountId" TEXT,
    "accountName" TEXT,
    "accountUsername" TEXT,
    "accountType" TEXT,
    "profileUrl" TEXT,
    "avatarUrl" TEXT,
    "channelId" TEXT,
    "pageId" TEXT,
    "instagramBusinessAccountId" TEXT,
    "externalUserId" TEXT,
    "connectionStatus" TEXT NOT NULL DEFAULT 'pending',
    "grantedScopes" TEXT,
    "capabilitiesJson" TEXT,
    "accessTokenEncrypted" TEXT,
    "refreshTokenEncrypted" TEXT,
    "accessTokenExpiresAt" TIMESTAMP(3),
    "refreshTokenExpiresAt" TIMESTAMP(3),
    "lastValidatedAt" TIMESTAMP(3),
    "lastRefreshAt" TIMESTAMP(3),
    "lastSuccessfulPublishAt" TIMESTAMP(3),
    "lastConnectionError" TEXT,
    "metadataJson" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "disconnectedAt" TIMESTAMP(3),

    CONSTRAINT "PlatformConnection_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "PublishingJob" (
    "id" TEXT NOT NULL,
    "platformPostId" TEXT NOT NULL,
    "platformConnectionId" TEXT,
    "status" TEXT NOT NULL DEFAULT 'pending',
    "scheduledAt" TIMESTAMP(3),
    "startedAt" TIMESTAMP(3),
    "completedAt" TIMESTAMP(3),
    "nextAttemptAt" TIMESTAMP(3),
    "attemptCount" INTEGER NOT NULL DEFAULT 0,
    "maxAttempts" INTEGER NOT NULL DEFAULT 5,
    "lockedAt" TIMESTAMP(3),
    "lockedBy" TEXT,
    "idempotencyKey" TEXT NOT NULL,
    "lastErrorCode" TEXT,
    "lastErrorMessage" TEXT,
    "lastErrorRetryable" BOOLEAN,
    "externalUploadId" TEXT,
    "externalPostId" TEXT,
    "externalPostUrl" TEXT,
    "requestSummary" TEXT,
    "responseSummary" TEXT,
    "dryRun" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "PublishingJob_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "PublishingAttempt" (
    "id" TEXT NOT NULL,
    "publishingJobId" TEXT NOT NULL,
    "attemptNumber" INTEGER NOT NULL,
    "startedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "completedAt" TIMESTAMP(3),
    "status" TEXT NOT NULL,
    "requestId" TEXT,
    "httpStatus" INTEGER,
    "externalErrorCode" TEXT,
    "errorCategory" TEXT,
    "errorMessage" TEXT,
    "retryable" BOOLEAN NOT NULL DEFAULT false,
    "responseSummary" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "PublishingAttempt_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "OAuthState" (
    "id" TEXT NOT NULL,
    "platform" TEXT NOT NULL,
    "stateHash" TEXT NOT NULL,
    "codeVerifierEncrypted" TEXT,
    "redirectPath" TEXT,
    "expiresAt" TIMESTAMP(3) NOT NULL,
    "usedAt" TIMESTAMP(3),
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "OAuthState_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "WorkerHeartbeat" (
    "id" TEXT NOT NULL,
    "workerId" TEXT NOT NULL,
    "lastHeartbeatAt" TIMESTAMP(3) NOT NULL,
    "lastJobId" TEXT,
    "status" TEXT NOT NULL DEFAULT 'online',
    "metadataJson" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "WorkerHeartbeat_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AffiliateProgram" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "slug" TEXT NOT NULL,
    "description" TEXT,
    "website" TEXT,
    "network" TEXT,
    "defaultCommissionType" TEXT NOT NULL DEFAULT 'PERCENTAGE',
    "defaultCommissionValue" DOUBLE PRECISION,
    "cookieDurationDays" INTEGER,
    "status" TEXT NOT NULL DEFAULT 'ACTIVE',
    "affiliateIdEnvKey" TEXT,
    "categoriesJson" TEXT,
    "disclosureText" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "AffiliateProgram_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AffiliateProduct" (
    "id" TEXT NOT NULL,
    "affiliateProgramId" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "slug" TEXT NOT NULL,
    "description" TEXT,
    "destinationUrl" TEXT NOT NULL,
    "affiliateUrl" TEXT NOT NULL,
    "imageUrl" TEXT,
    "category" TEXT NOT NULL,
    "subcategory" TEXT,
    "price" DOUBLE PRECISION,
    "currency" TEXT NOT NULL DEFAULT 'GBP',
    "estimatedCommission" DOUBLE PRECISION,
    "commissionType" TEXT,
    "commissionValue" DOUBLE PRECISION,
    "active" BOOLEAN NOT NULL DEFAULT true,
    "featured" BOOLEAN NOT NULL DEFAULT false,
    "priority" INTEGER NOT NULL DEFAULT 0,
    "evergreen" BOOLEAN NOT NULL DEFAULT false,
    "unsuitableForJson" TEXT,
    "notes" TEXT,
    "urlHealthStatus" TEXT NOT NULL DEFAULT 'UNKNOWN',
    "urlLastCheckedAt" TIMESTAMP(3),
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "AffiliateProduct_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AffiliateTag" (
    "id" TEXT NOT NULL,
    "slug" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "AffiliateTag_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AffiliateProductTag" (
    "productId" TEXT NOT NULL,
    "tagId" TEXT NOT NULL,

    CONSTRAINT "AffiliateProductTag_pkey" PRIMARY KEY ("productId","tagId")
);

-- CreateTable
CREATE TABLE "AffiliatePlacement" (
    "id" TEXT NOT NULL,
    "videoId" TEXT NOT NULL,
    "affiliateProductId" TEXT NOT NULL,
    "placementType" TEXT NOT NULL,
    "position" INTEGER NOT NULL DEFAULT 0,
    "relevanceScore" DOUBLE PRECISION,
    "manuallyApproved" BOOLEAN NOT NULL DEFAULT false,
    "generatedAutomatically" BOOLEAN NOT NULL DEFAULT false,
    "status" TEXT NOT NULL DEFAULT 'PENDING',
    "clicks" INTEGER NOT NULL DEFAULT 0,
    "conversions" INTEGER NOT NULL DEFAULT 0,
    "estimatedRevenue" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "AffiliatePlacement_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AffiliateClick" (
    "id" TEXT NOT NULL,
    "affiliateProductId" TEXT NOT NULL,
    "videoId" TEXT,
    "placementId" TEXT,
    "source" TEXT,
    "campaign" TEXT,
    "medium" TEXT,
    "content" TEXT,
    "destinationUrl" TEXT NOT NULL,
    "userAgent" TEXT,
    "referrer" TEXT,
    "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "AffiliateClick_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AffiliateConversion" (
    "id" TEXT NOT NULL,
    "affiliateProgramId" TEXT NOT NULL,
    "affiliateProductId" TEXT,
    "videoId" TEXT,
    "orderReference" TEXT,
    "saleAmount" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "commissionAmount" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "currency" TEXT NOT NULL DEFAULT 'GBP',
    "conversionDate" TIMESTAMP(3) NOT NULL,
    "imported" BOOLEAN NOT NULL DEFAULT false,
    "importBatchId" TEXT,
    "source" TEXT,
    "notes" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "AffiliateConversion_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AffiliateUrlHealthCheck" (
    "id" TEXT NOT NULL,
    "affiliateProductId" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    "httpStatus" INTEGER,
    "finalUrl" TEXT,
    "checkedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "notes" TEXT,

    CONSTRAINT "AffiliateUrlHealthCheck_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AffiliateDescriptionTemplate" (
    "id" TEXT NOT NULL,
    "key" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "category" TEXT,
    "body" TEXT NOT NULL,
    "active" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "AffiliateDescriptionTemplate_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AffiliateImportBatch" (
    "id" TEXT NOT NULL,
    "programmeSlug" TEXT,
    "filename" TEXT,
    "source" TEXT NOT NULL,
    "rowCount" INTEGER NOT NULL,
    "successCount" INTEGER NOT NULL,
    "errorCount" INTEGER NOT NULL,
    "skippedCount" INTEGER NOT NULL DEFAULT 0,
    "errorsJson" TEXT,
    "contentHash" TEXT,
    "importedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "notes" TEXT,

    CONSTRAINT "AffiliateImportBatch_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "LongFormVideo_slug_key" ON "LongFormVideo"("slug");

-- CreateIndex
CREATE UNIQUE INDEX "ShortClip_longFormVideoId_clipNumber_key" ON "ShortClip"("longFormVideoId", "clipNumber");

-- CreateIndex
CREATE INDEX "PlatformPost_platform_uploadStatus_idx" ON "PlatformPost"("platform", "uploadStatus");

-- CreateIndex
CREATE INDEX "PlatformPost_scheduledAt_idx" ON "PlatformPost"("scheduledAt");

-- CreateIndex
CREATE INDEX "PerformanceMetric_platformPostId_recordedAt_idx" ON "PerformanceMetric"("platformPostId", "recordedAt");

-- CreateIndex
CREATE INDEX "PerformanceMetric_importBatchId_idx" ON "PerformanceMetric"("importBatchId");

-- CreateIndex
CREATE UNIQUE INDEX "PlatformSettings_platform_key" ON "PlatformSettings"("platform");

-- CreateIndex
CREATE UNIQUE INDEX "ContentTemplate_key_key" ON "ContentTemplate"("key");

-- CreateIndex
CREATE UNIQUE INDEX "AppSetting_key_key" ON "AppSetting"("key");

-- CreateIndex
CREATE INDEX "PlatformConnection_platform_connectionStatus_idx" ON "PlatformConnection"("platform", "connectionStatus");

-- CreateIndex
CREATE UNIQUE INDEX "PlatformConnection_platform_externalUserId_key" ON "PlatformConnection"("platform", "externalUserId");

-- CreateIndex
CREATE UNIQUE INDEX "PublishingJob_idempotencyKey_key" ON "PublishingJob"("idempotencyKey");

-- CreateIndex
CREATE INDEX "PublishingJob_status_nextAttemptAt_idx" ON "PublishingJob"("status", "nextAttemptAt");

-- CreateIndex
CREATE INDEX "PublishingJob_scheduledAt_idx" ON "PublishingJob"("scheduledAt");

-- CreateIndex
CREATE INDEX "PublishingJob_lockedAt_idx" ON "PublishingJob"("lockedAt");

-- CreateIndex
CREATE INDEX "PublishingAttempt_publishingJobId_attemptNumber_idx" ON "PublishingAttempt"("publishingJobId", "attemptNumber");

-- CreateIndex
CREATE UNIQUE INDEX "OAuthState_stateHash_key" ON "OAuthState"("stateHash");

-- CreateIndex
CREATE INDEX "OAuthState_expiresAt_idx" ON "OAuthState"("expiresAt");

-- CreateIndex
CREATE UNIQUE INDEX "WorkerHeartbeat_workerId_key" ON "WorkerHeartbeat"("workerId");

-- CreateIndex
CREATE UNIQUE INDEX "AffiliateProgram_slug_key" ON "AffiliateProgram"("slug");

-- CreateIndex
CREATE UNIQUE INDEX "AffiliateProduct_slug_key" ON "AffiliateProduct"("slug");

-- CreateIndex
CREATE INDEX "AffiliateProduct_affiliateProgramId_active_idx" ON "AffiliateProduct"("affiliateProgramId", "active");

-- CreateIndex
CREATE INDEX "AffiliateProduct_category_idx" ON "AffiliateProduct"("category");

-- CreateIndex
CREATE INDEX "AffiliateProduct_featured_priority_idx" ON "AffiliateProduct"("featured", "priority");

-- CreateIndex
CREATE UNIQUE INDEX "AffiliateTag_slug_key" ON "AffiliateTag"("slug");

-- CreateIndex
CREATE INDEX "AffiliateProductTag_tagId_idx" ON "AffiliateProductTag"("tagId");

-- CreateIndex
CREATE INDEX "AffiliatePlacement_videoId_status_idx" ON "AffiliatePlacement"("videoId", "status");

-- CreateIndex
CREATE INDEX "AffiliatePlacement_affiliateProductId_idx" ON "AffiliatePlacement"("affiliateProductId");

-- CreateIndex
CREATE UNIQUE INDEX "AffiliatePlacement_videoId_affiliateProductId_placementType_key" ON "AffiliatePlacement"("videoId", "affiliateProductId", "placementType");

-- CreateIndex
CREATE INDEX "AffiliateClick_affiliateProductId_timestamp_idx" ON "AffiliateClick"("affiliateProductId", "timestamp");

-- CreateIndex
CREATE INDEX "AffiliateClick_videoId_timestamp_idx" ON "AffiliateClick"("videoId", "timestamp");

-- CreateIndex
CREATE INDEX "AffiliateClick_placementId_idx" ON "AffiliateClick"("placementId");

-- CreateIndex
CREATE INDEX "AffiliateConversion_affiliateProgramId_conversionDate_idx" ON "AffiliateConversion"("affiliateProgramId", "conversionDate");

-- CreateIndex
CREATE INDEX "AffiliateConversion_affiliateProductId_idx" ON "AffiliateConversion"("affiliateProductId");

-- CreateIndex
CREATE INDEX "AffiliateConversion_videoId_idx" ON "AffiliateConversion"("videoId");

-- CreateIndex
CREATE INDEX "AffiliateConversion_importBatchId_idx" ON "AffiliateConversion"("importBatchId");

-- CreateIndex
CREATE UNIQUE INDEX "AffiliateConversion_importBatchId_orderReference_key" ON "AffiliateConversion"("importBatchId", "orderReference");

-- CreateIndex
CREATE INDEX "AffiliateUrlHealthCheck_affiliateProductId_checkedAt_idx" ON "AffiliateUrlHealthCheck"("affiliateProductId", "checkedAt");

-- CreateIndex
CREATE UNIQUE INDEX "AffiliateDescriptionTemplate_key_key" ON "AffiliateDescriptionTemplate"("key");

-- CreateIndex
CREATE UNIQUE INDEX "AffiliateImportBatch_contentHash_key" ON "AffiliateImportBatch"("contentHash");

-- AddForeignKey
ALTER TABLE "ShortClip" ADD CONSTRAINT "ShortClip_longFormVideoId_fkey" FOREIGN KEY ("longFormVideoId") REFERENCES "LongFormVideo"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "PlatformPost" ADD CONSTRAINT "PlatformPost_shortClipId_fkey" FOREIGN KEY ("shortClipId") REFERENCES "ShortClip"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "PerformanceMetric" ADD CONSTRAINT "PerformanceMetric_platformPostId_fkey" FOREIGN KEY ("platformPostId") REFERENCES "PlatformPost"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "PublishingJob" ADD CONSTRAINT "PublishingJob_platformPostId_fkey" FOREIGN KEY ("platformPostId") REFERENCES "PlatformPost"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "PublishingJob" ADD CONSTRAINT "PublishingJob_platformConnectionId_fkey" FOREIGN KEY ("platformConnectionId") REFERENCES "PlatformConnection"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "PublishingAttempt" ADD CONSTRAINT "PublishingAttempt_publishingJobId_fkey" FOREIGN KEY ("publishingJobId") REFERENCES "PublishingJob"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AffiliateProduct" ADD CONSTRAINT "AffiliateProduct_affiliateProgramId_fkey" FOREIGN KEY ("affiliateProgramId") REFERENCES "AffiliateProgram"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AffiliateProductTag" ADD CONSTRAINT "AffiliateProductTag_productId_fkey" FOREIGN KEY ("productId") REFERENCES "AffiliateProduct"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AffiliateProductTag" ADD CONSTRAINT "AffiliateProductTag_tagId_fkey" FOREIGN KEY ("tagId") REFERENCES "AffiliateTag"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AffiliatePlacement" ADD CONSTRAINT "AffiliatePlacement_videoId_fkey" FOREIGN KEY ("videoId") REFERENCES "LongFormVideo"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AffiliatePlacement" ADD CONSTRAINT "AffiliatePlacement_affiliateProductId_fkey" FOREIGN KEY ("affiliateProductId") REFERENCES "AffiliateProduct"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AffiliateClick" ADD CONSTRAINT "AffiliateClick_affiliateProductId_fkey" FOREIGN KEY ("affiliateProductId") REFERENCES "AffiliateProduct"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AffiliateClick" ADD CONSTRAINT "AffiliateClick_videoId_fkey" FOREIGN KEY ("videoId") REFERENCES "LongFormVideo"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AffiliateClick" ADD CONSTRAINT "AffiliateClick_placementId_fkey" FOREIGN KEY ("placementId") REFERENCES "AffiliatePlacement"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AffiliateConversion" ADD CONSTRAINT "AffiliateConversion_affiliateProgramId_fkey" FOREIGN KEY ("affiliateProgramId") REFERENCES "AffiliateProgram"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AffiliateConversion" ADD CONSTRAINT "AffiliateConversion_affiliateProductId_fkey" FOREIGN KEY ("affiliateProductId") REFERENCES "AffiliateProduct"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AffiliateConversion" ADD CONSTRAINT "AffiliateConversion_videoId_fkey" FOREIGN KEY ("videoId") REFERENCES "LongFormVideo"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AffiliateUrlHealthCheck" ADD CONSTRAINT "AffiliateUrlHealthCheck_affiliateProductId_fkey" FOREIGN KEY ("affiliateProductId") REFERENCES "AffiliateProduct"("id") ON DELETE CASCADE ON UPDATE CASCADE;

