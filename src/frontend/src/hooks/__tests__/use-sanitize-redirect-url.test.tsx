import { renderHook } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import {
  consumeRedirectUrl,
  isSafeRedirectUrl,
  useSanitizeRedirectUrl,
} from "../use-sanitize-redirect-url";

const mockNavigate = jest.fn();

jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => mockNavigate,
}));

describe("isSafeRedirectUrl", () => {
  it("should allow valid internal relative paths", () => {
    expect(isSafeRedirectUrl("/dashboard")).toBe(true);
    expect(isSafeRedirectUrl("/flow/123-abc")).toBe(true);
    expect(isSafeRedirectUrl("/all?search=test&page=1")).toBe(true);
    expect(isSafeRedirectUrl("/settings#general")).toBe(true);
  });

  it("should reject malicious protocol-relative and backslash URLs (CVE-2026-53669)", () => {
    expect(isSafeRedirectUrl("\\evil.com")).toBe(false);
    expect(isSafeRedirectUrl("\\\\evil.com")).toBe(false);
    expect(isSafeRedirectUrl("//evil.com")).toBe(false);
    expect(isSafeRedirectUrl("/\\evil.com")).toBe(false);
    expect(isSafeRedirectUrl("/dashboard\\evil.com")).toBe(false);
    expect(isSafeRedirectUrl("/path/to/\\evil")).toBe(false);
  });

  it("should reject external absolute URLs and malicious schemes", () => {
    expect(isSafeRedirectUrl("https://evil.com")).toBe(false);
    expect(isSafeRedirectUrl("http://evil.com")).toBe(false);
    expect(isSafeRedirectUrl("javascript:alert(1)")).toBe(false);
    expect(isSafeRedirectUrl("data:text/html,evil")).toBe(false);
  });

  it("should reject non-string, empty, or whitespace values", () => {
    expect(isSafeRedirectUrl("")).toBe(false);
    expect(isSafeRedirectUrl("   ")).toBe(false);
    expect(isSafeRedirectUrl(null)).toBe(false);
    expect(isSafeRedirectUrl(undefined)).toBe(false);
  });
});

describe("useSanitizeRedirectUrl", () => {
  beforeEach(() => {
    mockNavigate.mockClear();
    sessionStorage.clear();
  });

  it("should call navigate and save to sessionStorage when valid redirect param exists", () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <MemoryRouter initialEntries={["/login?redirect=/dashboard"]}>
        <Routes>
          <Route path="/login" element={<div>{children}</div>} />
        </Routes>
      </MemoryRouter>
    );

    renderHook(() => useSanitizeRedirectUrl(), { wrapper });

    expect(mockNavigate).toHaveBeenCalledWith(expect.any(String), {
      replace: true,
    });
    expect(consumeRedirectUrl()).toBe("/dashboard");
  });

  it("should not store unsafe redirect param in sessionStorage", () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <MemoryRouter initialEntries={["/login?redirect=\\evil.com"]}>
        <Routes>
          <Route path="/login" element={<div>{children}</div>} />
        </Routes>
      </MemoryRouter>
    );

    renderHook(() => useSanitizeRedirectUrl(), { wrapper });

    expect(mockNavigate).toHaveBeenCalledWith(expect.any(String), {
      replace: true,
    });
    expect(consumeRedirectUrl()).toBeNull();
  });

  it("should not navigate when redirect param does not exist", () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <MemoryRouter initialEntries={["/login"]}>
        <Routes>
          <Route path="/login" element={<div>{children}</div>} />
        </Routes>
      </MemoryRouter>
    );

    renderHook(() => useSanitizeRedirectUrl(), { wrapper });

    expect(mockNavigate).not.toHaveBeenCalled();
  });

  it("should handle multiple query params", () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <MemoryRouter
        initialEntries={["/login?redirect=/dashboard&token=abc123"]}
      >
        <Routes>
          <Route path="/login" element={<div>{children}</div>} />
        </Routes>
      </MemoryRouter>
    );

    renderHook(() => useSanitizeRedirectUrl(), { wrapper });

    expect(mockNavigate).toHaveBeenCalledWith(expect.any(String), {
      replace: true,
    });
    expect(consumeRedirectUrl()).toBe("/dashboard");
  });

  it("should handle paths with no query params", () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <MemoryRouter initialEntries={["/dashboard"]}>
        <Routes>
          <Route path="/dashboard" element={<div>{children}</div>} />
        </Routes>
      </MemoryRouter>
    );

    renderHook(() => useSanitizeRedirectUrl(), { wrapper });

    expect(mockNavigate).not.toHaveBeenCalled();
  });

  it("should only run effect once on mount", () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <MemoryRouter initialEntries={["/login?redirect=/dashboard"]}>
        <Routes>
          <Route path="/login" element={<div>{children}</div>} />
        </Routes>
      </MemoryRouter>
    );

    const { rerender } = renderHook(() => useSanitizeRedirectUrl(), {
      wrapper,
    });

    const initialCallCount = mockNavigate.mock.calls.length;

    rerender();
    rerender();

    expect(mockNavigate).toHaveBeenCalledTimes(initialCallCount);
  });
});
