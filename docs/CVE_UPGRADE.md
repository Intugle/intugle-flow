# CVE Vulnerability Remediation & Package Upgrade Report

This document records the vulnerability assessment against `package_findings_export.xlsx` using **Trivy**, detail of the packages upgraded, vulnerabilities resolved, and packages intentionally held due to high-risk breaking changes.

---

## Executive Summary

- **Total CVEs Analyzed from Findings Export:** 149
- **Vulnerabilities Resolved:** 128 unique vulnerability IDs across Python backend and React frontend
- **Vulnerability Count Reduction (Trivy scan):**
  - **`uv.lock` (Backend):** 106 $\rightarrow$ 33 vulnerabilities (72 resolved)
  - **`src/frontend/package-lock.json` (Frontend):** 79 $\rightarrow$ 22 vulnerabilities (56 resolved)
- **High-Risk Breaking Packages Held:** `react-router` / `react-router-dom` v7 upgrade deferred to avoid breaking changes.

---

## 1. Upgrades Applied

### A. Python Backend Dependencies (`uv.lock`, `pyproject.toml`, `src/backend/base/pyproject.toml`)

| Package | Previous Version | Upgraded Version | Target Constraints / Semver | Resolved CVEs & Security Advisories |
| :--- | :--- | :--- | :--- | :--- |
| **`pypdf`** | `6.14.2` | `6.19.0` | `>=6.19.0,<7.0.0` | `CVE-2026-102993`, `CVE-2026-102994`, `CVE-2026-84309`, `CVE-2026-84311`, `CVE-2026-102996`, `CVE-2026-71852`, `CVE-2026-103000` |
| **`GitPython`** | `3.1.57` | `3.2.0` | `GitPython>=3.1.62` | `CVE-2026-87817`, `CVE-2026-87819`, `CVE-2026-78676`, `CVE-2026-78679`, `GHSA-59cr-6r3x-644w` |
| **`nltk`** | `3.10.0` | `3.10.3` | `nltk>=3.10.3` | `CVE-2026-71513`, `CVE-2026-71514`, `CVE-2026-72818`, `CVE-2026-81723`, `CVE-2026-81724`, `CVE-2026-81727` |
| **`urllib3`** | `2.7.0` | `2.8.0` | `>=2.8.0,<3.0.0` | `CVE-2026-97687`, `CVE-2026-97688`, `CVE-2026-97689` |
| **`pyjwt`** | `2.13.0` | `2.15.1` | `pyjwt>=2.14.0` | `CVE-2026-101918`, `CVE-2026-102265`, `CVE-2026-102266`, `CVE-2026-102271`, `CVE-2026-102274`, `CVE-2026-102267`, `CVE-2026-102268`, `CVE-2026-102275` |
| **`cryptography`** | `48.0.1` / `49.0.0` | `50.0.2` | `>=48.0.1` | `CVE-2026-69247`, `CVE-2026-69248`, `CVE-2026-69249` |
| **`litellm`** | `1.93.0` | `1.104.0` | `>=1.93.0,<2.0.0` | `CVE-2026-84377` |
| **`virtualenv`** | `21.7.0` | `21.14.5` | Transitive | `CVE-2026-102925`, `CVE-2026-102930`, `CVE-2026-102937`, `CVE-2026-102938` |

---

### B. Frontend Dependencies (`src/frontend/package-lock.json`)

| Package | Previous Version | Upgraded Version | Target Constraints / Semver | Resolved CVEs & Security Advisories |
| :--- | :--- | :--- | :--- | :--- |
| **`axios`** | `1.19.0` | `1.20.0` | `^1.15.0` | `CVE-2026-101900`, `CVE-2026-101903`, `CVE-2026-101905`, `CVE-2026-101907`, `CVE-2026-101908`, `CVE-2026-101909`, `CVE-2026-101904`, `CVE-2026-101902` |
| **`dompurify`** | `3.4.13` | `3.4.16` | `^3.4.12` | `GHSA-p98j-92pf-mc4p`, `GHSA-6688-9rhm-gjv2` |
| **`brace-expansion`** | `5.0.9` | `5.0.12` | Transitive | `CVE-2026-102276`, `CVE-2026-102277`, `CVE-2026-102278` |
| **`devalue`** | `5.9.0` | `5.9.3` | Transitive | `CVE-2026-92708`, `CVE-2026-81176`, `GHSA-mcm9-63f2-9j32`, `GHSA-4q55-j62x-fr9h`, `GHSA-wf3x-273g-mvxv` |
| **`fast-uri`** | `4.1.2` | `4.1.5` | Transitive | `CVE-2026-75931`, `CVE-2026-84292`, `CVE-2026-86472` |
| **`hono`** | `4.13.0` | `4.13.7` | Transitive | `CVE-2026-93981`, `CVE-2026-84363`, `CVE-2026-84364`, `CVE-2026-84365` |
| **`ip-address`** | `10.4.0` | `10.7.1` | Transitive | `CVE-2026-101910`, `CVE-2026-101912`, `CVE-2026-101913` |
| **`js-yaml`** | `4.3.1` | `4.3.2` | Transitive | `CVE-2026-84375` |
| **`moment`** | `2.30.1` | `2.31.0` | `^2.30.1` | `CVE-2026-17495` |
| **`nanoid`** | `3.3.17` | `3.3.18` | `^5.1.6` | `CVE-2026-67213` |
| **`piscina`** | `4.9.3` | `4.9.4` | Transitive | `CVE-2026-102992` (Resolved on v4 line without v5/v6 breaking changes) |
| **`qs`** | `6.15.3` | `6.16.0` | Transitive | `CVE-2026-82417` |
| **`source-map-js`** | `1.2.1` | `1.2.2` | Transitive | `CVE-2026-93749` |

---

## 2. Held Packages (High Risk / Breaking Changes)

The following dependencies were intentionally held from major version upgrades to protect existing application routing and architecture:

1. **`react-router` / `react-router-dom` (Held on `6.30.4`):**
   - **Advisories:** `CVE-2026-53666`, `CVE-2026-53669`
   - **Reason:** Upgrading to `react-router@7.x` requires breaking architectural changes across layout providers, route definitions, hooks, and loaders. `react-router-dom` remains pinned on `6.30.4` until a planned migration to v7 is scheduled.
2. **`basic-ftp` / `accessibility-checker` / `puppeteer`:**
   - **Reason:** Upgrading requires force-updating breaking build toolchains (`@swc/cli@0.8.1`, `remark-math@3.0.1`, `accessibility-checker@3.1.82`).

---

## 3. Vulnerabilities Without Upstream Fixes

The following CVEs currently have no fixed release from upstream package maintainers:

- `CVE-2025-14505` (`npm-elliptic <= 6.6.1`)
- `CVE-2025-69872` (`pip-diskcache <= 5.6.3`)
- `CVE-2026-103001` (`pip-pyjwt >= 2.11.0, <= 2.13.0`)
- `CVE-2026-69112` (`pip-accelerate <= 1.14.0`)
- `CVE-2026-76845` (`npm-adm-zip <= 0.6.0`)
- `CVE-2026-80047` (`pip-transformers <= 5.8.1`)
- `CVE-2026-81726` (`pip-nltk <= 3.10.3`)
- `CVE-2026-85393` (`npm-node-forge <= 1.4.0`)
- `CVE-2026-93687` (`npm-braces <= 3.0.3`)
- `CVE-2026-93748` (`npm-http-cache-semantics <= 4.2.0`)

---

## 4. Verification & Testing

- **Backend Unit Tests:** Verified and passing (`uv run pytest`).
- **Dependency Tree & Lockfiles:** `uv.lock`, `pyproject.toml`, `src/backend/base/pyproject.toml`, and `src/frontend/package-lock.json` are synchronized and verified.
