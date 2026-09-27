import Link from "next/link";
import { AffiliateImportForm } from "@/components/affiliate/AffiliateImportForm";
import { isOperatorAuthenticated } from "@/lib/security/operator-auth";

export const dynamic = "force-dynamic";

export default async function AffiliateImportPage() {
  const canWrite = await isOperatorAuthenticated();

  return (
    <div className="space-y-8">
      <div>
        <Link href="/affiliate" className="text-sm text-[#5A6E82] hover:text-[#F5E8D2]">
          ← Affiliate
        </Link>
        <h1 className="mt-2 font-[family-name:var(--font-orbit-display)] text-3xl">
          Conversion import
        </h1>
        <p className="mt-2 text-sm text-[#F5E8D2]/55">
          Import Amazon / Brilliant / generic affiliate reports. Preview before commit.
        </p>
      </div>
      {canWrite ? (
        <AffiliateImportForm />
      ) : (
        <div className="card-panel space-y-3 p-5">
          <p className="text-sm text-[#F5E8D2]/65">
            CSV import writes conversion rows. Sign in as operator to continue.
          </p>
          <Link
            href="/login?next=/affiliate/import"
            className="inline-flex min-h-11 items-center justify-center rounded-full bg-[#FF7A24] px-5 py-2.5 text-sm font-medium text-[#0A0C12]"
          >
            Operator sign-in
          </Link>
        </div>
      )}
      <div className="card-panel p-5 text-sm text-[#F5E8D2]/55">
        Sample CSV: <code>content/samples/csv/affiliate_amazon_sample.csv</code>
      </div>
    </div>
  );
}
