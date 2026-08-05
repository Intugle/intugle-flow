# Intugle Flow Rebranding Plan

Based on the DESIGN.md spec and the provided branding assets.

---

## Phase 1: Theme & Colors (index.css — the primary change)

**File: `src/frontend/src/style/index.css`**

Replace the light/dark HSL tokens to match the Intugle Design System (§2). Key changes:

| Change | Current | New (Intugle) |
|--------|---------|---------------|
| Page bg (dark) | `--background: 240 6% 10%` | `--background: 224 71.4% 4.1%` (= `#0f172a`) |
| Page bg (light) | `--background: 0 0% 100%` | `--background: 0 0% 100%` (same) |
| Muted/card (dark) | `--muted: 240 4% 16%` | `--muted: 215 27.9% 16.9%` (= `#1e293b`) |
| Muted/card (light) | `--muted: 240 5% 96%` | `--muted: 210 15% 93%` |
| Primary (dark) | `white` / black fg | `210 20% 98%` / `220.9 39.3% 11%` fg |
| Primary (light) | `black` / white fg | `217 91% 60%` / white fg |
| Accent base (both) | `240 5% 96%` | `215 27.9% 16.9%` (dark), `210 15% 90%` (light) |
| Border (dark) | `240 5% 26%` | `215 27.9% 16.9%` (= `#334155`) |
| Border (light) | `240 6% 90%` | `220 13% 87%` |
| Ring (dark) | white | `216 12.2% 83.9%` |
| Ring (light) | black | `217 91% 60%` |
| Destructive (dark) | `0 84% 60%` | `0 62.8% 30.6%` |
| Destructive (light) | `0 72% 45%` | `0 72% 51%` |
| Foreground/text | `0 0% 100%` (dark) / `0 0% 0%` (light) | `210 20% 98%` (dark) / `222 47% 11%` (light) |
| Input (dark) | `240 5% 34%` | `215 27.9% 16.9%` |
| Input (light) | `240 6% 90%` | `220 13% 87%` |
| Muted-fg (dark) | `240 5% 65%` | `217.9 10.6% 64.9%` |
| Muted-fg (light) | `240 4% 43%` | `220 10% 45%` |

**Semantic accent tokens** to adjust:
- `--accent-blue`: already close to `#3b82f6` spec — verify consistency
- Keep `--accent-emerald`, `--accent-indigo`, `--accent-pink`, `--accent-amber` as they're functional
- Status colors (`--success: 142 70% 45%`, `--warning: 48 96% 53%`, `--info: 217 91% 60%`) — update to match spec §2.3

**Add new glass/panel tokens** (§2.5):
- `--app-panel-bg`, `--app-glass-bg`, `--app-glass-border`, `--app-glass-shadow`

**Add sidebar tokens** (§7):
- `--sb-*` namespace tokens for dark/light

**Add motion tokens** (§4.4):
- `--transition-fast/base/slow`

---

## Phase 2: Fonts (index.css + index.html)

**File: `src/frontend/src/style/index.css`**

Replace font families per §3.1:
- `--font-sans`: `"Inter", sans-serif` (keep)
- `--font-mono`: `"JetBrains Mono", ...` (keep)
- `--font-chivo`: Change to `"Raleway", sans-serif` (Chivo → Raleway for display headings per spec)
- Add `--font-secondary`: `"Open Sans", sans-serif` (new — secondary text)

**File: `src/frontend/tailwind.config.mjs`** — update `fontFamily.chivo` → `fontFamily.raleway` (rename)
- Add `fontFamily.secondary` for Open Sans

**File: `src/frontend/index.html`** — replace Google Fonts link:
- Remove Chivo, add Raleway + Open Sans

**File: `src/frontend/src/style/applies.css`** (§1-500) & **`src/frontend/src/style/classes.css`** — search for `.chivo` class references and update to `.raleway`

---

## Phase 3: Logo & Icons (assets + imports)

**A. Create new SVG assets from branding files:**

| New File | Based on | Use |
|----------|----------|-----|
| `src/frontend/src/assets/IntugleIcon.svg` | `branding/intugle-icon.svg` | Monochrome app icon (equivalent to LangflowLogo.svg) |
| `src/frontend/src/assets/IntugleLogo.svg` | `branding/intugle-logo.svg` | Full wordmark for login/splash pages |

Need to adapt the branding SVGs:
1. **IntugleIcon.svg** — Extract just the icon mark from `intugle-logo.svg` (first 7 `<path>` elements, viewBox adjusted), set `fill="currentColor"` for theme-aware coloring, 24x24 like the existing LangflowLogo
2. **IntugleLogo.svg** — Adapt `intugle-logo.svg` for use as a full wordmark component (231x110, inline gradients preserved)

**B. Update all imports** (~12 component files):
Replace `import LangflowLogo from "@/assets/LangflowLogo.svg?react"` with `import IntugleIcon from "@/assets/IntugleIcon.svg?react"`

Files to update:
- `appHeaderComponent/index.tsx`
- `LoginPage/index.tsx`
- `SignUpPage/index.tsx`
- `AdminPage/LoginPage/index.tsx`
- `DeleteAccountPage/index.tsx`
- `emptyPage/index.tsx`
- `loadingComponent/index.tsx`
- `chat-logo-icon.tsx`
- `chat-view.tsx`
- `bot-message.tsx`
- `bot-message-logo.tsx`
- `playground-modal.tsx` (LangflowLogoColor → IntugleLogo)

**C. Favicon:**
- Convert `branding/intugle-icon.svg` → `src/frontend/public/favicon.ico` (use a tool like ImageMagick or an online converter)
- Create `public/icons/` with 32x32, 128x128, 256x256 PNGs from the icon

**D. Clean up old assets:**
- Remove or keep `LangflowLogo*.svg`, `langflow_logo_*.svg`, `logo_*.png` — keep for potential reference, but they won't be imported anymore

---

## Phase 4: Text Rebranding (Langflow → Intugle Flow)

**A. HTML metadata:**
- `index.html`: `<title>Langflow</title>` → `<title>Intugle Flow</title>`
- `public/manifest.json`: name/short_name/description → Intugle Flow

**B. Locale files** (7 files, global search-and-replace "Langflow" → "Intugle Flow"):
- `en.json`, `pt.json`, `fr.json`, `es.json`, `zh-Hans.json`, `de.json`, `ja.json`
- ~20+ keys each — careful: some are URLs, some are brand names. Only replace brand references, not URLs.

**C. Constants/strings** (~5 files):
- `constants.ts`: taglines, LANGFLOW_CHAT_TITLE, STORE_TITLE, INSERT_API_KEY, docs URLs
- `urls.ts`: `"https://langflow.org"` → Intugle URL
- `assistant-panel.constants.ts`: ASSISTANT_TITLE
- `pages/Playground/index.tsx`: document.title fallback
- `custom-poll-build-events.ts`, `buildUtils.ts`, `dbProviderConstants.ts`, `knowledgePage/utils/backendMetadata.ts`

**D. CSS class names** (optional, for consistency):
- `.langflow-page-icon` → `.intugle-page-icon`
- `.langflow-chat-*` → `.intugle-chat-*`

**E. MCP/wiring references:**
- `langflow:` config key → `intugle:` (or keep as is if it's a protocol key)
- `<langflow-chat>` custom element tag → keep (may break embedded chat if changed)

**F. Test files:** Update mock references to LangflowLogo.svg → IntugleIcon.svg (lower priority but needed for passing tests)

---

## Phase 5: Gradient Background (applies.css)

**File: `src/frontend/src/style/applies.css`** (lines 1342-1360)

Replace the pink/magenta/purple animated gradient with navy/blue tones matching the Intugle palette:
```
--color1: 59, 130, 246       (#3b82f6 blue)
--color2: 96, 165, 250       (#60a5fa lighter blue)
--color3: 37, 99, 235        (#2563eb deep blue)
--color-interactive: 96, 165, 250
--color-bg1: #0f172a (dark), #ffffff (light)
```

---

## Summary Table

| # | Phase | Files Affected | Effort |
|---|-------|---------------|--------|
| 1 | Theme colors | `style/index.css` (+500 tokens) | **High** |
| 2 | Fonts | `index.css`, `index.html`, `tailwind.config.mjs` | Medium |
| 3 | Logo/Icons | 2 new SVG files + ~12 imports + favicon | Medium |
| 4 | Text strings | `index.html`, `manifest.json`, ~7 locales, ~8 source files | Medium |
| 5 | Gradients | `style/applies.css` (~20 lines) | Low |

**What NOT to change:**
- Component structure, layouts, spacing
- ChatApp theme system (isolated `--th-*` namespace)
- Ace editor theming
- AG Grid theming (uses HSL tokens — will auto-update)
- Datatype colors, note colors, JSE tokens (functional)
- Sidebar component code (just the CSS token values change)
- Zustand store / theme toggle logic