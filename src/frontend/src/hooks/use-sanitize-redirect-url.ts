import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

const REDIRECT_SESSION_KEY = "langflow_login_redirect";

/**
 * Validates whether a redirect URL is a safe internal relative path.
 * Protects against open redirect vulnerabilities (CVE-2026-53669 / CVE-2025-68470)
 * caused by backslashes (\evil.com), protocol-relative URLs (//evil.com),
 * or absolute external URLs (https://evil.com).
 */
export function isSafeRedirectUrl(url: string | null | undefined): boolean {
  if (!url || typeof url !== "string") return false;

  const trimmed = url.trim();
  if (!trimmed) return false;

  // Must start with a single '/' and not with '//', '/\', '\\', or '\'
  if (
    !trimmed.startsWith("/") ||
    trimmed.startsWith("//") ||
    trimmed.startsWith("/\\") ||
    trimmed.startsWith("\\")
  ) {
    return false;
  }

  // Reject URLs that contain schemes (e.g., javascript:, data:) or protocol specifiers (://)
  if (
    trimmed.includes("://") ||
    trimmed.includes("javascript:") ||
    trimmed.includes("data:")
  ) {
    return false;
  }

  // Reject backslashes in the path part (browsers may normalize \ to / creating open redirects)
  const pathPart = trimmed.split("?")[0].split("#")[0];
  if (pathPart.includes("\\")) {
    return false;
  }

  return true;
}

export function useSanitizeRedirectUrl() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    if (searchParams.has("redirect")) {
      const redirectPath = searchParams.get("redirect");
      if (redirectPath && isSafeRedirectUrl(redirectPath)) {
        sessionStorage.setItem(REDIRECT_SESSION_KEY, redirectPath);
      } else {
        sessionStorage.removeItem(REDIRECT_SESSION_KEY);
      }
      navigate(window.location.pathname, { replace: true });
    }
  }, []);
}

export function consumeRedirectUrl(): string | null {
  const redirectPath = sessionStorage.getItem(REDIRECT_SESSION_KEY);
  if (redirectPath) {
    sessionStorage.removeItem(REDIRECT_SESSION_KEY);
    if (isSafeRedirectUrl(redirectPath)) {
      return redirectPath;
    }
  }
  return null;
}
