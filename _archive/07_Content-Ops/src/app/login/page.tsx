import Link from "next/link";
import { loginOperator } from "@/app/login/actions";
import { isOperatorAuthenticated, isOperatorPasswordConfigured, safeOperatorNextPath } from "@/lib/security/operator-auth";
import { redirect } from "next/navigation";

export const dynamic = "force-dynamic";

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ next?: string; error?: string }>;
}) {
  const sp = await searchParams;
  const next = safeOperatorNextPath(sp.next);
  if (await isOperatorAuthenticated()) {
    redirect(next);
  }

  const configured = isOperatorPasswordConfigured();

  return (
    <div className="mx-auto flex min-h-[70vh] max-w-md flex-col justify-center px-4 py-10">
      <p className="text-xs uppercase tracking-[0.22em] text-[#FF7A24]">Orbit Content Ops</p>
      <h1 className="mt-3 font-[family-name:var(--font-orbit-display)] text-3xl text-[#F5E8D2]">
        Operator sign-in
      </h1>
      <p className="mt-3 text-sm text-[#F5E8D2]/65">
        Reads stay open. Writes (films, imports, settings, OAuth) need the operator password from
        Vercel env.
      </p>

      {!configured ? (
        <div className="mt-6 rounded-xl border border-[#FFC85A]/35 bg-[#FFC85A]/10 px-4 py-3 text-sm text-[#FFC85A]">
          <code className="text-[#F5E8D2]">CONTENT_OPS_OPERATOR_PASSWORD</code> is not set on this
          deploy. Add it in Vercel (Production + Preview), then sign in here. Mutating actions stay
          blocked until then.
        </div>
      ) : (
        <form action={loginOperator} className="card-panel mt-6 space-y-4 p-5">
          <input type="hidden" name="next" value={next} />
          <label className="block space-y-1.5">
            <span className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Password</span>
            <input
              name="password"
              type="password"
              required
              autoComplete="current-password"
              className="w-full rounded-lg border border-white/10 bg-[#0A0C12] px-3 py-2.5 text-sm text-[#F5E8D2]"
            />
          </label>
          {sp.error ? <p className="text-sm text-[#FFC85A]">{sp.error}</p> : null}
          <button
            type="submit"
            className="inline-flex min-h-11 w-full items-center justify-center rounded-full bg-[#FF7A24] px-5 py-2.5 text-sm font-medium text-[#0A0C12]"
          >
            Sign in
          </button>
        </form>
      )}

      <p className="mt-6 text-center text-sm text-[#5A6E82]">
        <Link href="/" className="text-[#FF7A24] hover:underline">
          Back to overview
        </Link>
      </p>
    </div>
  );
}
