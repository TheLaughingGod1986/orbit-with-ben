"use server";

import { redirect } from "next/navigation";
import {
  clearOperatorSessionCookie,
  isOperatorPasswordConfigured,
  safeOperatorNextPath,
  setOperatorSessionCookie,
  verifyOperatorPassword,
} from "@/lib/security/operator-auth";

export async function loginOperator(formData: FormData): Promise<void> {
  const next = safeOperatorNextPath(String(formData.get("next") || "/"));

  if (!isOperatorPasswordConfigured()) {
    redirect(
      `/login?next=${encodeURIComponent(next)}&error=${encodeURIComponent(
        "CONTENT_OPS_OPERATOR_PASSWORD is not configured on this deploy",
      )}`,
    );
  }
  const password = String(formData.get("password") || "");
  if (!(await verifyOperatorPassword(password))) {
    redirect(
      `/login?next=${encodeURIComponent(next)}&error=${encodeURIComponent(
        "Invalid operator password",
      )}`,
    );
  }
  await setOperatorSessionCookie();
  redirect(next);
}

export async function logoutOperator(): Promise<void> {
  await clearOperatorSessionCookie();
  redirect("/login");
}
