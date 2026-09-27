import { prisma } from "@/lib/storage/prisma";
import type { AffiliateProgramInput } from "./schemas";
import { affiliateProgramInputSchema } from "./schemas";
import { earningsPerClick, conversionRate, roundMoney } from "./revenue";

export async function listPrograms() {
  return prisma.affiliateProgram.findMany({
    orderBy: { name: "asc" },
    include: {
      _count: { select: { products: true, conversions: true } },
    },
  });
}

export async function getProgramBySlug(slug: string) {
  return prisma.affiliateProgram.findUnique({
    where: { slug },
    include: {
      products: { include: { tags: { include: { tag: true } } } },
      _count: { select: { products: true, conversions: true } },
    },
  });
}

export async function createProgram(raw: AffiliateProgramInput) {
  const input = affiliateProgramInputSchema.parse(raw);
  const { categories, website, ...rest } = input;
  return prisma.affiliateProgram.create({
    data: {
      ...rest,
      website: website || null,
      categoriesJson: categories?.length ? JSON.stringify(categories) : null,
    },
  });
}

export async function updateProgram(id: string, raw: Partial<AffiliateProgramInput>) {
  const existing = await prisma.affiliateProgram.findUnique({ where: { id } });
  if (!existing) throw new Error("Programme not found");
  const input = affiliateProgramInputSchema.partial().parse(raw);
  const { categories, website, ...rest } = input;
  return prisma.affiliateProgram.update({
    where: { id },
    data: {
      ...rest,
      ...(website !== undefined ? { website: website || null } : {}),
      ...(categories !== undefined
        ? { categoriesJson: categories.length ? JSON.stringify(categories) : null }
        : {}),
    },
  });
}

export async function getProgramPerformance(programId: string) {
  const [clicks, conversions, placements] = await Promise.all([
    prisma.affiliateClick.count({
      where: { affiliateProduct: { affiliateProgramId: programId } },
    }),
    prisma.affiliateConversion.aggregate({
      where: { affiliateProgramId: programId },
      _sum: { commissionAmount: true },
      _count: true,
    }),
    prisma.affiliatePlacement.count({
      where: {
        affiliateProduct: { affiliateProgramId: programId },
        status: { in: ["APPROVED", "ACTIVE"] },
      },
    }),
  ]);

  const revenue = conversions._sum.commissionAmount ?? 0;
  const conversionCount = conversions._count;
  return {
    clicks,
    placements,
    conversions: conversionCount,
    revenue: roundMoney(revenue),
    epc: earningsPerClick(revenue, clicks),
    conversionRate: conversionRate(conversionCount, clicks),
  };
}
