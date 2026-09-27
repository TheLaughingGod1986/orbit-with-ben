import { isDryRun } from "@/lib/env";

export function DryRunBanner() {
  if (!isDryRun()) return null;
  return (
    <div className="border-b border-[#FFC85A]/35 bg-[#FFC85A]/15 px-4 py-2 text-center text-sm text-[#FFC85A]">
      Dry-run mode is active. No content will be published.
    </div>
  );
}
