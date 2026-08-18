import { NextRequest, NextResponse } from "next/server";
import {
  isMutatingApiPath,
  isOperatorRequestAuthenticated,
  isPublicPath,
} from "@/lib/security/operator-auth";

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const method = request.method.toUpperCase();

  if (isPublicPath(pathname)) {
    return NextResponse.next();
  }

  const authed = await isOperatorRequestAuthenticated(request);

  // Gate mutating APIs + OAuth start/callback (token minting).
  if (isMutatingApiPath(method, pathname)) {
    if (!authed) {
      const isOAuthBrowser =
        method === "GET" &&
        /^\/api\/oauth\/[^/]+\/(start|callback)$/.test(pathname);
      if (isOAuthBrowser) {
        const login = new URL("/login", request.url);
        login.searchParams.set("next", "/settings/connections");
        login.searchParams.set(
          "error",
          "Sign in as operator before connecting accounts",
        );
        return NextResponse.redirect(login);
      }
      return NextResponse.json(
        { error: "Unauthorized: operator sign-in required" },
        { status: 401 },
      );
    }
    return NextResponse.next();
  }

  // Next.js server actions POST with a next-action header.
  if (method === "POST" && request.headers.has("next-action")) {
    if (!authed) {
      return NextResponse.json(
        { error: "Unauthorized: operator sign-in required" },
        { status: 401 },
      );
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
