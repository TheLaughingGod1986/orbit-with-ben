/**
 * Affiliate go-live readiness — reporting only.
 * Does not invent affiliate IDs or auto-approve placements.
 */

import { isPlaceholderAffiliateUrl } from "./live-product-urls";

export type GoLiveCheckStatus = "pass" | "fail" | "warn" | "manual";

export type GoLiveCheck = {
  id: string;
  label: string;
  status: GoLiveCheckStatus;
  detail: string;
  blocking: boolean;
};

export type GoLiveReport = {
  readyForTrackedRedirects: boolean;
  readyForPaidTraffic: boolean;
  checks: GoLiveCheck[];
  summary: string;
  generatedAt: string;
};

export type GoLiveInput = {
  amazonTag: string | null;
  brilliantId: string | null;
  appBaseUrl: string | null;
  affiliateRedirectBaseUrl: string | null;
  activeProductCount: number;
  placeholderUrlCount: number;
  brokenUrlCount: number;
  activeProgramCount: number;
  approvedPlacementCount: number;
  clickCount: number;
  /** Optional: whether /go route is reachable (CLI can probe). */
  goRouteReachable?: boolean | null;
};

function redirectBaseLooksProduction(url: string | null): boolean {
  if (!url) return false;
  try {
    const u = new URL(url);
    return (
      u.protocol === "https:" &&
      (u.hostname === "orbitwithben.com" ||
        u.hostname === "www.orbitwithben.com" ||
        u.hostname.endsWith(".orbitwithben.com"))
    );
  } catch {
    return false;
  }
}

/**
 * Pure readiness evaluation from env + catalogue stats.
 */
export function evaluateAffiliateGoLive(input: GoLiveInput): GoLiveReport {
  const checks: GoLiveCheck[] = [];

  checks.push({
    id: "amazon_tag",
    label: "Amazon Associates UK tag",
    status: input.amazonTag ? "pass" : "fail",
    detail: input.amazonTag
      ? "AMAZON_ASSOCIATE_TAG is set (value not shown)."
      : "Set AMAZON_ASSOCIATE_TAG after Amazon Associates UK approval.",
    blocking: true,
  });

  checks.push({
    id: "brilliant_id",
    label: "Brilliant affiliate ID",
    status: input.brilliantId ? "pass" : "fail",
    detail: input.brilliantId
      ? "BRILLIANT_AFFILIATE_ID is set (value not shown)."
      : "Set BRILLIANT_AFFILIATE_ID after Brilliant affiliate approval.",
    blocking: true,
  });

  const redirect =
    input.affiliateRedirectBaseUrl ||
    (input.appBaseUrl ? `${input.appBaseUrl.replace(/\/$/, "")}/go` : null);

  checks.push({
    id: "redirect_base",
    label: "Tracked redirect base (/go)",
    status: redirect
      ? redirectBaseLooksProduction(redirect)
        ? "pass"
        : "warn"
      : "fail",
    detail: redirect
      ? redirectBaseLooksProduction(redirect)
        ? `Using ${redirect}`
        : `Using ${redirect} — for public YouTube links prefer https://orbitwithben.com/go`
      : "Set APP_BASE_URL or AFFILIATE_REDIRECT_BASE_URL.",
    blocking: !redirect,
  });

  checks.push({
    id: "products",
    label: "Active affiliate products",
    status: input.activeProductCount > 0 ? "pass" : "fail",
    detail:
      input.activeProductCount > 0
        ? `${input.activeProductCount} active product(s).`
        : "Seed or create products under /affiliate/products.",
    blocking: true,
  });

  checks.push({
    id: "placeholder_urls",
    label: "No example.invalid product URLs",
    status: input.placeholderUrlCount === 0 ? "pass" : "fail",
    detail:
      input.placeholderUrlCount === 0
        ? "No placeholder merchant URLs in active products."
        : `${input.placeholderUrlCount} active product(s) still use example.invalid / PLACEHOLDER — run npm run affiliate:apply-urls or edit in admin.`,
    blocking: true,
  });

  checks.push({
    id: "broken_urls",
    label: "Broken URL health",
    status: input.brokenUrlCount === 0 ? "pass" : "warn",
    detail:
      input.brokenUrlCount === 0
        ? "No products marked BROKEN."
        : `${input.brokenUrlCount} product(s) marked BROKEN — run a throttled health check.`,
    blocking: false,
  });

  checks.push({
    id: "programs",
    label: "Active programmes",
    status: input.activeProgramCount > 0 ? "pass" : "fail",
    detail: `${input.activeProgramCount} active programme(s).`,
    blocking: true,
  });

  checks.push({
    id: "first_placement",
    label: "First approved placement (starts goals clock)",
    status: input.approvedPlacementCount > 0 ? "pass" : "manual",
    detail:
      input.approvedPlacementCount > 0
        ? `${input.approvedPlacementCount} approved/active placement(s).`
        : "Approve a trust-gated placement on a long-form video when ready — Shorts stay zero links.",
    blocking: false,
  });

  checks.push({
    id: "clicks",
    label: "Click tracking smoke",
    status: input.clickCount > 0 ? "pass" : "manual",
    detail:
      input.clickCount > 0
        ? `${input.clickCount} click(s) recorded.`
        : "After deploy, open /go/{slug} once and confirm a click row + merchant 302.",
    blocking: false,
  });

  if (input.goRouteReachable != null) {
    checks.push({
      id: "go_reachable",
      label: "/go route probe",
      status: input.goRouteReachable ? "pass" : "fail",
      detail: input.goRouteReachable
        ? "Redirect base responded (2xx/3xx)."
        : "Could not reach redirect base — check deploy + DNS/proxy for /go.",
      blocking: true,
    });
  }

  checks.push({
    id: "amazon_account",
    label: "Amazon Associates UK account",
    status: input.amazonTag ? "pass" : "manual",
    detail: "Manual: affiliate-program.amazon.co.uk approval (cannot be automated).",
    blocking: !input.amazonTag,
  });

  checks.push({
    id: "brilliant_account",
    label: "Brilliant affiliate account",
    status: input.brilliantId ? "pass" : "manual",
    detail: "Manual: Brilliant creator/affiliate approval (cannot be automated).",
    blocking: !input.brilliantId,
  });

  checks.push({
    id: "dns_go",
    label: "orbitwithben.com/go DNS or proxy",
    status: redirectBaseLooksProduction(redirect) ? "pass" : "manual",
    detail:
      "Manual: point https://orbitwithben.com/go to Content Ops (or set AFFILIATE_REDIRECT_BASE_URL to the live app /go).",
    blocking: false,
  });

  const blockingFails = checks.filter((c) => c.blocking && c.status === "fail");
  const readyForTrackedRedirects =
    Boolean(redirect) &&
    input.activeProductCount > 0 &&
    input.placeholderUrlCount === 0 &&
    input.activeProgramCount > 0 &&
    (input.goRouteReachable == null || input.goRouteReachable);

  const readyForPaidTraffic =
    readyForTrackedRedirects && Boolean(input.amazonTag || input.brilliantId);

  const summary = readyForPaidTraffic
    ? "Ready for tracked affiliate traffic on programmes with IDs set."
    : readyForTrackedRedirects
      ? "Catalogue + /go ready — still need Amazon and/or Brilliant IDs for commission attribution."
      : `Not ready: ${blockingFails.map((c) => c.id).join(", ") || "see checks"}.`;

  return {
    readyForTrackedRedirects,
    readyForPaidTraffic,
    checks,
    summary,
    generatedAt: new Date().toISOString(),
  };
}

export { isPlaceholderAffiliateUrl };
