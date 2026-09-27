import { z } from "zod";
import {
  AFFILIATE_PROGRAM_STATUSES,
  COMMISSION_TYPES,
  PLACEMENT_STATUSES,
  PLACEMENT_TYPES,
  URL_HEALTH_STATUSES,
} from "./types";

export const affiliateProgramInputSchema = z.object({
  name: z.string().min(1),
  slug: z.string().min(1).regex(/^[a-z0-9-]+$/),
  description: z.string().optional().nullable(),
  website: z.string().url().optional().nullable().or(z.literal("")),
  network: z.string().optional().nullable(),
  defaultCommissionType: z.enum(COMMISSION_TYPES).default("PERCENTAGE"),
  defaultCommissionValue: z.number().nonnegative().optional().nullable(),
  cookieDurationDays: z.number().int().positive().optional().nullable(),
  status: z.enum(AFFILIATE_PROGRAM_STATUSES).default("ACTIVE"),
  affiliateIdEnvKey: z.string().optional().nullable(),
  categories: z.array(z.string()).optional(),
  disclosureText: z.string().optional().nullable(),
});

export const affiliateProductInputSchema = z.object({
  affiliateProgramId: z.string().min(1),
  name: z.string().min(1),
  slug: z.string().min(1).regex(/^[a-z0-9-]+$/),
  description: z.string().optional().nullable(),
  destinationUrl: z.string().url(),
  /** Empty allowed — /go builds from destinationUrl + AMAZON_ASSOCIATE_TAG. */
  affiliateUrl: z.union([z.string().url(), z.literal("")]).default(""),
  imageUrl: z.string().url().optional().nullable().or(z.literal("")),
  category: z.string().min(1),
  subcategory: z.string().optional().nullable(),
  price: z.number().nonnegative().optional().nullable(),
  currency: z.string().default("GBP"),
  estimatedCommission: z.number().nonnegative().optional().nullable(),
  commissionType: z.enum(COMMISSION_TYPES).optional().nullable(),
  commissionValue: z.number().nonnegative().optional().nullable(),
  active: z.boolean().default(true),
  featured: z.boolean().default(false),
  priority: z.number().int().default(0),
  evergreen: z.boolean().default(false),
  unsuitableFor: z.array(z.string()).optional(),
  notes: z.string().optional().nullable(),
  tagSlugs: z.array(z.string()).default([]),
});

export const placementActionSchema = z.object({
  videoId: z.string().min(1),
  affiliateProductId: z.string().min(1),
  placementType: z.enum(PLACEMENT_TYPES),
  position: z.number().int().nonnegative().optional(),
  relevanceScore: z.number().optional().nullable(),
  status: z.enum(PLACEMENT_STATUSES).optional(),
  manuallyApproved: z.boolean().optional(),
  generatedAutomatically: z.boolean().optional(),
});

export const urlHealthStatusSchema = z.enum(URL_HEALTH_STATUSES);

export type AffiliateProgramInput = z.infer<typeof affiliateProgramInputSchema>;
export type AffiliateProductInput = z.infer<typeof affiliateProductInputSchema>;
