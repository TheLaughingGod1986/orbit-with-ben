import { prisma } from "@/lib/storage/prisma";
import type { AffiliateProductInput } from "./schemas";
import { affiliateProductInputSchema } from "./schemas";
import type { ProductMatchInput } from "./types";

export function toProductMatchInput(product: {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  category: string;
  subcategory: string | null;
  active: boolean;
  featured: boolean;
  priority: number;
  evergreen: boolean;
  estimatedCommission: number | null;
  commissionType: string | null;
  commissionValue: number | null;
  price: number | null;
  currency: string;
  unsuitableForJson: string | null;
  tags?: Array<{ tag: { slug: string } }>;
  affiliateProgram?: { slug: string; status: string };
}): ProductMatchInput {
  let unsuitableFor: string[] = [];
  if (product.unsuitableForJson) {
    try {
      unsuitableFor = JSON.parse(product.unsuitableForJson) as string[];
    } catch {
      unsuitableFor = [];
    }
  }
  return {
    id: product.id,
    name: product.name,
    slug: product.slug,
    description: product.description,
    category: product.category,
    subcategory: product.subcategory,
    active: product.active,
    featured: product.featured,
    priority: product.priority,
    evergreen: product.evergreen,
    estimatedCommission: product.estimatedCommission,
    commissionType: product.commissionType,
    commissionValue: product.commissionValue,
    price: product.price,
    currency: product.currency,
    unsuitableFor,
    tagSlugs: (product.tags || []).map((t) => t.tag.slug),
    programSlug: product.affiliateProgram?.slug,
    programStatus: product.affiliateProgram?.status,
  };
}

export async function listProducts(filters?: {
  programmeId?: string;
  category?: string;
  active?: boolean;
  featured?: boolean;
  evergreen?: boolean;
  tag?: string;
  search?: string;
}) {
  const products = await prisma.affiliateProduct.findMany({
    where: {
      affiliateProgramId: filters?.programmeId || undefined,
      category: filters?.category || undefined,
      active: filters?.active,
      featured: filters?.featured,
      evergreen: filters?.evergreen,
      tags: filters?.tag
        ? { some: { tag: { slug: filters.tag } } }
        : undefined,
      OR: filters?.search
        ? [
            { name: { contains: filters.search } },
            { slug: { contains: filters.search } },
            { category: { contains: filters.search } },
            { description: { contains: filters.search } },
          ]
        : undefined,
    },
    include: {
      affiliateProgram: true,
      tags: { include: { tag: true } },
    },
    orderBy: [{ featured: "desc" }, { priority: "desc" }, { name: "asc" }],
  });
  return products;
}

export async function getProductBySlug(slug: string) {
  return prisma.affiliateProduct.findUnique({
    where: { slug },
    include: {
      affiliateProgram: true,
      tags: { include: { tag: true } },
    },
  });
}

export async function upsertProductTags(productId: string, tagSlugs: string[]) {
  const tags = [];
  for (const slug of tagSlugs) {
    const normalized = slug.trim().toLowerCase().replace(/\s+/g, "-");
    if (!normalized) continue;
    const tag = await prisma.affiliateTag.upsert({
      where: { slug: normalized },
      create: {
        slug: normalized,
        name: normalized
          .split("-")
          .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
          .join(" "),
      },
      update: {},
    });
    tags.push(tag);
  }
  await prisma.affiliateProductTag.deleteMany({ where: { productId } });
  if (tags.length) {
    await prisma.affiliateProductTag.createMany({
      data: tags.map((t) => ({ productId, tagId: t.id })),
    });
  }
  return tags;
}

export async function createProduct(raw: AffiliateProductInput) {
  const input = affiliateProductInputSchema.parse(raw);
  const { tagSlugs, unsuitableFor, imageUrl, ...rest } = input;
  const product = await prisma.affiliateProduct.create({
    data: {
      ...rest,
      imageUrl: imageUrl || null,
      unsuitableForJson: unsuitableFor?.length ? JSON.stringify(unsuitableFor) : null,
    },
  });
  await upsertProductTags(product.id, tagSlugs || []);
  return getProductBySlug(product.slug);
}

export async function updateProduct(id: string, raw: Partial<AffiliateProductInput>) {
  const existing = await prisma.affiliateProduct.findUnique({ where: { id } });
  if (!existing) throw new Error("Product not found");

  const merged = affiliateProductInputSchema.parse({
    affiliateProgramId: raw.affiliateProgramId ?? existing.affiliateProgramId,
    name: raw.name ?? existing.name,
    slug: raw.slug ?? existing.slug,
    description: raw.description ?? existing.description,
    destinationUrl: raw.destinationUrl ?? existing.destinationUrl,
    affiliateUrl: raw.affiliateUrl ?? existing.affiliateUrl,
    imageUrl: raw.imageUrl ?? existing.imageUrl,
    category: raw.category ?? existing.category,
    subcategory: raw.subcategory ?? existing.subcategory,
    price: raw.price ?? existing.price,
    currency: raw.currency ?? existing.currency,
    estimatedCommission: raw.estimatedCommission ?? existing.estimatedCommission,
    commissionType: raw.commissionType ?? existing.commissionType,
    commissionValue: raw.commissionValue ?? existing.commissionValue,
    active: raw.active ?? existing.active,
    featured: raw.featured ?? existing.featured,
    priority: raw.priority ?? existing.priority,
    evergreen: raw.evergreen ?? existing.evergreen,
    unsuitableFor: raw.unsuitableFor,
    notes: raw.notes ?? existing.notes,
    tagSlugs: raw.tagSlugs ?? [],
  });

  const { tagSlugs, unsuitableFor, imageUrl, ...rest } = merged;
  await prisma.affiliateProduct.update({
    where: { id },
    data: {
      ...rest,
      imageUrl: imageUrl || null,
      unsuitableForJson:
        unsuitableFor !== undefined
          ? unsuitableFor?.length
            ? JSON.stringify(unsuitableFor)
            : null
          : undefined,
    },
  });
  if (raw.tagSlugs) {
    await upsertProductTags(id, tagSlugs);
  }
  return prisma.affiliateProduct.findUnique({
    where: { id },
    include: { affiliateProgram: true, tags: { include: { tag: true } } },
  });
}

export async function loadActiveProductsForMatching(): Promise<ProductMatchInput[]> {
  const products = await prisma.affiliateProduct.findMany({
    where: { active: true, affiliateProgram: { status: "ACTIVE" } },
    include: {
      tags: { include: { tag: true } },
      affiliateProgram: true,
    },
  });
  return products.map(toProductMatchInput);
}
