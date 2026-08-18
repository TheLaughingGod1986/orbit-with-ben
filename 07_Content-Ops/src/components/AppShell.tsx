import Link from "next/link";
import { MobileNav, type NavItem } from "@/components/MobileNav";
import { logoutOperator } from "@/app/login/actions";
import { isOperatorAuthenticated } from "@/lib/security/operator-auth";

const NAV: NavItem[] = [
  { href: "/", label: "Overview" },
  { href: "/pipeline", label: "Pipeline" },
  { href: "/videos", label: "Films" },
  { href: "/calendar", label: "Calendar" },
  { href: "/analytics", label: "Analytics" },
  { href: "/affiliate", label: "Affiliate" },
  { href: "/settings/connections", label: "Connections" },
  { href: "/settings", label: "Settings" },
];

export async function AppShell({ children }: { children: React.ReactNode }) {
  const signedIn = await isOperatorAuthenticated();

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-40 border-b border-white/5 bg-[#0a0c12]/80 backdrop-blur-xl">
        <div className="relative mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3 sm:px-6 sm:py-4">
          <Link href="/" className="group flex min-w-0 items-baseline gap-2 sm:gap-3">
            <span className="font-[family-name:var(--font-orbit-display)] text-2xl tracking-tight text-[#F5E8D2]">
              ORBIT
            </span>
            <span className="truncate text-[0.65rem] uppercase tracking-[0.22em] text-[#FF7A24] sm:text-xs">
              Content Ops
            </span>
          </Link>
          <nav className="hidden flex-wrap items-center gap-1 text-sm text-[#F5E8D2]/75 md:flex">
            {NAV.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="rounded-full px-3 py-1.5 transition hover:bg-white/5 hover:text-[#F5E8D2]"
              >
                {item.label}
              </Link>
            ))}
            {signedIn ? (
              <form action={logoutOperator}>
                <button
                  type="submit"
                  className="rounded-full px-3 py-1.5 text-[#F5E8D2]/55 transition hover:bg-white/5 hover:text-[#F5E8D2]"
                >
                  Sign out
                </button>
              </form>
            ) : (
              <Link
                href="/login"
                className="rounded-full px-3 py-1.5 text-[#FF7A24] transition hover:bg-white/5"
              >
                Sign in
              </Link>
            )}
          </nav>
          <div className="flex items-center gap-2 md:hidden">
            {signedIn ? (
              <form action={logoutOperator}>
                <button
                  type="submit"
                  className="rounded-full border border-white/10 px-3 py-2 text-xs text-[#F5E8D2]/70"
                >
                  Sign out
                </button>
              </form>
            ) : (
              <Link
                href="/login"
                className="rounded-full border border-[#FF7A24]/40 px-3 py-2 text-xs text-[#FF7A24]"
              >
                Sign in
              </Link>
            )}
            <MobileNav items={NAV} />
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8">{children}</main>
    </div>
  );
}
