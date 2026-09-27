import crypto from "crypto";
import Papa from "papaparse";
import { estimateCommission, roundMoney } from "./revenue";

export type AffiliateCsvRow = {
  date?: string;
  product?: string;
  productSlug?: string;
  clicks?: number;
  orders?: number;
  sales?: number;
  commission?: number;
  orderReference?: string;
  currency?: string;
};

export type AffiliateColumnMapping = Record<keyof AffiliateCsvRow, string | undefined>;

export const AFFILIATE_CSV_DEFAULT_MAPPINGS: Record<string, Partial<AffiliateColumnMapping>> = {
  amazon: {
    date: "Date",
    product: "Product Name",
    clicks: "Clicks",
    orders: "Items Shipped",
    sales: "Revenue",
    commission: "Earnings",
    orderReference: "Order ID",
    currency: "Currency",
  },
  brilliant: {
    date: "Date",
    product: "Offer",
    clicks: "Clicks",
    orders: "Conversions",
    sales: "Sale Amount",
    commission: "Commission",
    orderReference: "Transaction ID",
  },
  generic: {
    date: "date",
    product: "product",
    productSlug: "product_slug",
    clicks: "clicks",
    orders: "orders",
    sales: "sales",
    commission: "commission",
    orderReference: "order_reference",
    currency: "currency",
  },
};

export type AffiliateImportPreview = {
  headers: string[];
  matched: Partial<AffiliateColumnMapping>;
  missing: string[];
  sampleRows: AffiliateCsvRow[];
  contentHash: string;
  rowCount: number;
};

function num(v: unknown): number | undefined {
  if (v == null || v === "") return undefined;
  const n = Number(String(v).replace(/[^0-9.-]/g, ""));
  return Number.isFinite(n) ? n : undefined;
}

function hashContent(text: string): string {
  return crypto.createHash("sha256").update(text.trim()).digest("hex");
}

export function previewAffiliateCsv(
  csvText: string,
  mapping: Partial<AffiliateColumnMapping>,
): AffiliateImportPreview {
  const parsed = Papa.parse<Record<string, string>>(csvText, {
    header: true,
    skipEmptyLines: true,
  });
  const headers = parsed.meta.fields || [];
  const missing: string[] = [];
  for (const [field, col] of Object.entries(mapping)) {
    if (col && !headers.includes(col)) missing.push(`${field} ← ${col}`);
  }

  const sampleRows = (parsed.data || []).slice(0, 5).map((row) => mapRow(row, mapping));

  return {
    headers,
    matched: mapping,
    missing,
    sampleRows,
    contentHash: hashContent(csvText),
    rowCount: (parsed.data || []).length,
  };
}

function mapRow(
  row: Record<string, string>,
  mapping: Partial<AffiliateColumnMapping>,
): AffiliateCsvRow {
  const get = (key: keyof AffiliateCsvRow) => {
    const col = mapping[key];
    return col ? row[col] : undefined;
  };
  return {
    date: get("date"),
    product: get("product"),
    productSlug: get("productSlug"),
    clicks: num(get("clicks")),
    orders: num(get("orders")),
    sales: num(get("sales")),
    commission: num(get("commission")),
    orderReference: get("orderReference"),
    currency: get("currency") || "GBP",
  };
}

export function parseAffiliateCsv(
  csvText: string,
  mapping: Partial<AffiliateColumnMapping>,
): { rows: AffiliateCsvRow[]; contentHash: string } {
  const parsed = Papa.parse<Record<string, string>>(csvText, {
    header: true,
    skipEmptyLines: true,
  });
  const rows = (parsed.data || []).map((row) => mapRow(row, mapping));
  return { rows, contentHash: hashContent(csvText) };
}

export type ParsedConversion = {
  conversionDate: Date;
  saleAmount: number;
  commissionAmount: number;
  currency: string;
  orderReference: string | null;
  productName: string | null;
  productSlug: string | null;
  clicks: number;
  orders: number;
};

export function rowsToConversions(rows: AffiliateCsvRow[]): {
  conversions: ParsedConversion[];
  errors: string[];
} {
  const conversions: ParsedConversion[] = [];
  const errors: string[] = [];

  rows.forEach((row, i) => {
    if (!row.date && row.commission == null && row.sales == null) {
      errors.push(`Row ${i + 1}: empty`);
      return;
    }
    const date = row.date ? new Date(row.date) : new Date();
    if (Number.isNaN(date.getTime())) {
      errors.push(`Row ${i + 1}: invalid date "${row.date}"`);
      return;
    }
    const saleAmount = roundMoney(row.sales ?? 0);
    const commissionAmount = roundMoney(
      row.commission ??
        estimateCommission({
          saleAmount,
          commissionType: "PERCENTAGE",
          commissionValue: 0,
        }),
    );
    conversions.push({
      conversionDate: date,
      saleAmount,
      commissionAmount,
      currency: row.currency || "GBP",
      orderReference: row.orderReference || null,
      productName: row.product || null,
      productSlug: row.productSlug || null,
      clicks: row.clicks ?? 0,
      orders: row.orders ?? 0,
    });
  });

  return { conversions, errors };
}
