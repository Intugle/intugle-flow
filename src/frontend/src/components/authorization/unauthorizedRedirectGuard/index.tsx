import { useEffect } from "react";
import { UNAUTHORIZED_REDIRECT_URL } from "@/constants/constants";

// When LANGFLOW_UNAUTHORIZED_REDIRECT_URL is configured (a build-time env var
// exposed as an absolute http(s) URL), the application never renders the local
// /login page — every redirect that targets /login instead performs a full-page
// navigation to that external URL (e.g. an SSO/session-expiry endpoint).
//
// This is the single choke point that guarantees "before /login renders, route
// to the external URL". It intentionally wraps LoginPage only inside
// ProtectedLoginRoute, so an authenticated user is redirected away (to /home)
// before this guard ever runs.
export function UnauthorizedRedirectGuard({
  children,
}: {
  children: React.ReactNode;
}) {
  const target = UNAUTHORIZED_REDIRECT_URL;
  const shouldRedirect = isValidRedirectURL(target);

  useEffect(() => {
    if (shouldRedirect) {
      // Full-page navigation discards the SPA + any ?redirect query param in
      // favor of the configured external authentication URL.
      window.location.assign(target);
    }
  }, [shouldRedirect, target]);

  // Avoid flashing LoginPage while the navigation is queued.
  if (shouldRedirect) {
    return null;
  }

  return <>{children}</>;
}

// Mirrors the validation in controllers/API/api.tsx so the same value is used
// for the interceptor-level redirect and the route-level guard.
function isValidRedirectURL(url: string | undefined): boolean {
  if (!url) return false;
  try {
    const parsed = new URL(url);
    return parsed.protocol === "http:" || parsed.protocol === "https:";
  } catch {
    return false;
  }
}
