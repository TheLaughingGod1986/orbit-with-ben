import { PrismaClient } from "@prisma/client";

/**
 * Prisma client singleton — safe for Vercel serverless.
 * Cache on globalThis so warm lambdas reuse one client (avoids connection storms).
 */
const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient };

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === "development" ? ["error", "warn"] : ["error"],
  });

globalForPrisma.prisma = prisma;
