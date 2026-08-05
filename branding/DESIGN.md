# Intugle Design System

This document is the authoritative specification for the Intugle product visual language. An application built from this specification should be immediately recognizable as an Intugle product: a dark-first, navy-and-blue, AI-product aesthetic with calm information density, soft glass surfaces, a quiet blue accent, and a collapsible rail navigation.

The spec is prescriptive. Where a reference implementation exists in this repo, the source files are listed in [Source of truth](#source-of-truth). Implement the tokens and patterns described here; do not reinvent them.

---

## 1. Brand identity

| Attribute | Value |
|---|---|
| Personality | Calm, technical, AI-native, data-dense but uncluttered |
| Default mode | **Dark** (light is a first-class peer, not an afterthought) |
| Signature palette | Deep navy slate backgrounds, cool slate text, a single quiet blue accent |
| Signature surfaces | Soft glass / frosted panels over a navy field |
| Signature motion | Subtle, 150–300ms, cubic-bezier easing, never bouncy |
| Signature layout | Full-height app shell, collapsible icon rail, centered content columns |
| Type voice | Inter for UI, JetBrains Mono for data/code, Raleway for display headings |

The single most recognizable trait is the **deep navy `#0f172a` field with a `#3b82f6` blue accent and `#1e293b` card surfaces**. Preserve this ratio of accent-to-neutral: blue is sparse and purposeful (primary actions, active states, links, focus rings), never decorative.

---

## 2. Color

### 2.1 Dark palette (default)

| Role | Token | Value |
|---|---|---|
| Page background | `--theme-bg` | `#0f172a` |
| Primary text | `--theme-text` | `#cbd5e1` |
| Card surface | `--theme-bg-card` | `#1e293b` |
| Border | `--theme-border` | `#334155` |
| Muted border | `--theme-border-muted` | `#3341554d` |
| Muted surface | `--theme-bg-muted` | `#1e293b` |
| Muted surface 2 | `--theme-bg-muted-2` | `#151e31` |
| Accent / primary | `--theme-primary` | `#3b82f6` |
| Secondary | `--theme-secondary` | `#64748b` |

### 2.2 Light palette

| Role | Token | Value |
|---|---|---|
| Page background | `--theme-bg` | `#ffffff` |
| Primary text | `--theme-text` | `#0f172a` |
| Card surface | `--theme-bg-card` | `#ffffff` |
| Border | `--theme-border` | `#e2e8f0` |
| Muted border | `--theme-border-muted` | `#e2e8f0` |
| Muted surface | `--theme-bg-muted` | `#f9f9fa` |
| Accent / primary | `--theme-primary` | `#3b82f6` |
| Secondary | `--theme-secondary` | `#64748b` |

The blue accent `#3b82f6` is constant across both modes. Active/hover accent steps to `#2563eb`.

### 2.3 Semantic status colors

These are HSL channel tokens (consumed as `hsl(var(--success) / <alpha>)`).

| Status | Token | Dark | Light |
|---|---|---|---|
| Success | `--success` | `142 70% 45%` | `142 70% 45%` |
| Warning | `--warning` | `48 96% 53%` | `48 96% 53%` |
| Info | `--info` | `217 91% 60%` | `217 91% 60%` |
| Destructive | `--destructive` | `0 62.8% 30.6%` | `0 72% 51%` |

Status colors are reserved for state communication (success toasts, validation, destructive actions). Do not use them for brand decoration.

### 2.4 Shadcn/Radix HSL tokens

The component library reads HSL tokens. These are the canonical values; implement them in `:root` (dark defaults) and override under an `html:not(.dark)` (or `.light`) selector for light.

| Token | Dark | Light |
|---|---|---|
| `--background` | `224 71.4% 4.1%` | `0 0% 100%` |
| `--foreground` | `210 20% 98%` | `222 47% 11%` |
| `--card` | `224 71.4% 4.1%` | `0 0% 100%` |
| `--card-foreground` | `210 20% 98%` | `222 47% 11%` |
| `--popover` | `224 71.4% 4.1%` | `0 0% 100%` |
| `--primary` | `210 20% 98%` | `217 91% 60%` |
| `--primary-foreground` | `220.9 39.3% 11%` | `0 0% 100%` |
| `--secondary` | `215 27.9% 16.9%` | `210 15% 93%` |
| `--muted` | `215 27.9% 16.9%` | `210 15% 93%` |
| `--muted-foreground` | `217.9 10.6% 64.9%` | `220 10% 45%` |
| `--accent` | `215 27.9% 16.9%` | `210 15% 90%` |
| `--border` | `215 27.9% 16.9%` | `220 13% 87%` |
| `--input` | `215 27.9% 16.9%` | `220 13% 87%` |
| `--ring` | `216 12.2% 83.9%` | `217 91% 60%` |
| `--destructive` | `0 62.8% 30.6%` | `0 72% 51%` |

### 2.5 Glass / panel surfaces

Frosted translucent panels are a signature surface, used for dialogs, command palettes, and premium cards.

| Token | Dark | Light |
|---|---|---|
| `--app-panel-bg` | `rgba(12, 18, 34, 0.85)` | `#ffffff` |
| `--app-glass-bg` | `rgba(10, 15, 28, 0.65)` | `rgba(255, 255, 255, 0.98)` |
| `--app-glass-border` | `rgba(255, 255, 255, 0.1)` | `rgba(203, 213, 225, 0.8)` |
| `--app-glass-shadow` | `0 8px 40px rgba(0,0,0,0.5), 0 0 1px rgba(255,255,255,0.1), inset 0 1px 0 rgba(255,255,255,0.05)` | `0 8px 40px rgba(0,0,0,0.08), 0 0 1px rgba(0,0,0,0.05), inset 0 1px 0 rgba(255,255,255,0.9)` |

### 2.6 Accent usage rules

- **Primary actions** (main CTA, send button): blue fill, white text.
- **Active state** (sidebar item, selected tab): blue-tinted translucent background (`rgba(37,99,235,0.2)` dark / `rgba(59,130,246,0.12)` light) with `#60a5fa`/`#2563eb` text.
- **Focus ring**: `--theme-primary` / `--ring`, 2px, offset 2px.
- **Links**: blue. **Hover**: step one shade deeper.
- Never use blue for large neutral fills. The accent ratio is roughly 5% accent, 95% neutral.

---

## 3. Typography

### 3.1 Font families

| Role | Family | Loaded from |
|---|---|---|
| UI body (default) | `Inter, sans-serif` | Self-hosted variable font |
| Display headings | `Raleway, sans-serif` | Self-hosted variable font |
| Secondary text | `Open Sans, sans-serif` | Self-hosted variable font |
| Data / code | `"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace` | Self-hosted variable font |

Fonts are self-hosted as variable TTFs and declared via `@font-face`. Do not load display/mono fonts from a CDN in the shell app. Body font is set at runtime on `--theme-font-primary`.

### 3.2 Type scale

The Intugle type scale is intentionally compact and information-dense. These are the configured Tailwind sizes — they are **smaller than stock Tailwind**; use them, do not assume defaults.

| Token | rem | px (approx) | Use |
|---|---|---|---|
| `text-sm` | 0.65rem | 10.4px | Labels, captions, table cells |
| `text-base` | 0.8rem | 12.8px | Default body |
| `text-lg` | 1.00rem | 16px | Emphasized body, small headings |
| `text-xl` | 1.05rem | 16.8px | Card titles |
| `text-2xl` | 1.363rem | 21.8px | Section headings |
| `text-3xl` | 1.753rem | 28px | Page headings |
| `text-4xl` | 2.241rem | 35.9px | Hero numerals |
| `text-5xl` | 2.852rem | 45.6px | Marketing hero |

Weights: regular 400 for body, medium 500 for labels/nav, semibold 600 for titles/values, bold 700 for hero numerals. Tracking-tight (`-0.025em`) on the product wordmark and large headings.

---

## 4. Spatial system

### 4.1 Radii

| Token / class | Radius | Use |
|---|---|---|
| `--radius` | `0.5rem` (8px) | Base token |
| `rounded-sm` | 2px | Compact controls (buttons in size variants) |
| `rounded-md` | 6px | Standard controls (inputs, buttons base, selects) |
| `rounded-lg` | 8px | Standard cards |
| `rounded-xl` | 12px | Feature cards, home/dashboard panels |
| `rounded-2xl` | 16px | Dialogs, premium cards, chat composer |
| `rounded-full` | 9999px | Tags, pills, status dots, icon-only CTAs |

### 4.2 Spacing conventions

| Context | Value |
|---|---|
| Outer page padding | 16–24px |
| Card padding (default) | 16px (`p-4`) |
| Large card / dialog padding | 24px (`p-6`) |
| Compact control padding | 4–12px |
| Nav item padding | 12px |
| Section gap | 16–24px |

### 4.3 Elevation

| Token | Value (dark) |
|---|---|
| `--shadow-sm` | `0 1px 2px 0 hsl(222 47% 11% / 0.05)` |
| `--shadow-md` | `0 4px 6px -1px hsl(222 47% 11% / 0.1), 0 2px 4px -2px hsl(222 47% 11% / 0.1)` |
| `--shadow-lg` | `0 10px 15px -3px hsl(222 47% 11% / 0.1), 0 4px 6px -4px hsl(222 47% 11% / 0.1)` |
| `--shadow-xl` | `0 20px 25px -5px hsl(222 47% 11% / 0.1), 0 8px 10px -6px hsl(222 47% 11% / 0.1)` |
| Glass shadow | `--app-glass-shadow` (see §2.5) |

Shadows are intentionally soft and low-opacity. Premium/dashboard cards may add a subtle colored glow (blue, low alpha) — use sparingly.

### 4.4 Motion

| Token | Duration | Easing |
|---|---|---|
| `--transition-fast` | 150ms | `cubic-bezier(0.4, 0, 0.2, 1)` |
| `--transition-base` | 200ms | `cubic-bezier(0.4, 0, 0.2, 1)` |
| `--transition-slow` | 300ms | `cubic-bezier(0.4, 0, 0.2, 1)` |

Keyframes: `accordion-down/up` (200ms), `pulse-glow` (2s ease-in-out infinite), `slide-down` (200ms). Motion is always subtle; never use spring/bounce easing. Honor `prefers-reduced-motion`.

---

## 5. Theme system

### 5.1 Modes

Three modes: `dark`, `light`, `system`. `system` resolves `prefers-color-scheme` and live-updates when the OS theme changes.

- Persistence key: `localStorage["app-theme"]` (`"dark" | "light" | "system"`); default `system`.
- The resolved boolean is exposed as `isDark` via `useTheme()`.
- The `.dark` / `.light` class is toggled on `<html>`.
- **No-flash bootstrap**: theme class and base CSS variables are set by a synchronous inline script in `index.html` before first paint. Any new app must replicate this to avoid a white flash on load.

### 5.2 Token architecture (canonical contract)

A new app should implement exactly these token namespaces:

1. **`--theme-*`** — runtime app tokens (bg, text, bg-card, border, border-muted, bg-muted, primary, secondary, font-primary, font-secondary). Set by the theme provider on `:root`.
2. **Shadcn HSL tokens** — `--background`, `--foreground`, `--card`, `--primary`, `--muted`, `--accent`, `--border`, `--input`, `--ring`, `--destructive`, plus `--radius`. Component primitives read these.
3. **`--sb-*`** — sidebar-scoped tokens (see §7).
4. **`--app-*` glass tokens** — panel/glass surfaces (see §2.5).
5. **Status tokens** — `--success`, `--warning`, `--info`, `--destructive`.

> Note on the reference implementation: this repo additionally carries legacy "skin" RGB-channel tokens (`--bg-skin-*`, `--text-skin-*`, `--color-*`) and a broad `!important` light-mode override layer for backwards compatibility. A new app **should not** adopt the legacy skin namespace; implement the canonical contract above.

### 5.3 Dark-first authoring rule

Author surfaces against semantic tokens (`bg-card`, `text-foreground`, `border`, `bg-muted`, `text-theme-primary`), not raw slate values. The reference app contains some dark-first hardcoded surfaces; treat those as legacy and prefer token-driven styling so both modes work without override hacks.

---

## 6. Components

The shared primitive library lives in `src/components/ui/` and is Radix/Shadcn-style with `class-variance-authority`. Use these primitives; do not create parallel ones.

### 6.1 Button

`rounded-md` base, `text-sm font-medium`, `focus-visible:ring-2 ring-theme-primary ring-offset-2`, disabled opacity 50%.

| Variant | Style |
|---|---|
| `default` | `bg-theme-primary text-white`, hover opacity 90 |
| `destructive` | `bg-destructive text-destructive-foreground` |
| `outline` | transparent, `border --theme-border`, `text --theme-text`, hover `bg-muted` |
| `secondary` | `bg-muted text-theme-text` |
| `ghost` | transparent, hover `bg-muted` |
| `link` | `text-theme-primary` underline on hover |

| Size | Height |
|---|---|
| `sm` | 32px |
| `default` / `md` | 36px |
| `lg` | 44px |
| `icon` | 40×40px |

Loading state: prepend a spinning loader, opacity 75%, cursor not-allowed.

### 6.2 Input

`h-10`, `rounded-md`, `px-3 py-2`, `border-input bg-background`, placeholder `text-muted-foreground`, focus `ring-2 ring-ring ring-offset-2`. The Tailwind base text size is `text-base` dropping to `text-sm` at `md`.

### 6.3 Card

`rounded-lg border shadow-sm`, dark `bg-card` / light `bg-white`, `text-card-foreground`. Header/Content/Footer use `p-6` (24px) with `space-y-1.5` between title and description. CardTitle is `text-2xl font-semibold tracking-tight`; CardDescription is `text-sm text-muted-foreground`.

### 6.4 Dialog

Centered, `max-w-lg`, `sm:rounded-2xl`, **liquid-glass** surface (`bg-white/70 backdrop-blur-xl` light / `dark:bg-slate-900/70` dark), `shadow-2xl` plus inset glass shadow. Overlay: `bg-black/40 backdrop-blur-sm`, `z-[9999]`. Entry/exit: fade + zoom 95% + slide from center. Close affordance: red `X` top-right, `rounded-full`, red focus ring. Outside interaction is prevented (explicit product convention).

### 6.5 Table

Responsive `overflow-auto` wrapper. Body text 14px, header row 40px, cell padding 8px, muted header text, hover and selected row states. Use for data-dense views.

### 6.6 Tabs

Segmented `bg-muted` tab list, 40px tall; active tab gets elevated background, contrasting text, and a subtle shadow. Feature tabs may override into an underline style (thin blue underline, slate labels).

### 6.7 Select / DropdownMenu / Tooltip / Badge / Checkbox

All Radix-based, token-driven. Select/Menu overlays are high z-index (`z-[10000]`). Checkbox is 16px Radix. Tooltip is a token popover. Badge is token-colored by variant.

### 6.8 Sidebar (generic)

Desktop: fixed 20rem. Mobile: 18rem Sheet. `Ctrl/Cmd+B` toggles. State persisted via cookie. Screen-reader labels provided.

---

## 7. Navigation rail (product sidebar)

The signature Intugle navigation is a slim collapsible icon rail, not a wide fixed sidebar.

| Attribute | Value |
|---|---|
| Collapsed width | 68px |
| Expanded width | 240px |
| Logo area height | 64px |
| Logo mark | 40×40px |
| Nav icon size | 20×20px |
| Nav label | 14px, weight 500 |
| Item padding | 12px |
| Item radius | 8px (`rounded-lg`) |
| Section gap | 8px |
| Transition | 200–300ms ease |

Sidebar tokens (`--sb-*`):

| Token | Dark | Light |
|---|---|---|
| `--sb-bg` | `#020617` | `#f8fafc` |
| `--sb-border` | `rgba(30,41,59,0.5)` | `rgba(226,232,240,0.8)` |
| `--sb-text` | `#d1d5db` | `#334155` |
| `--sb-text-muted` | `#9ca3af` | `#64748b` |
| `--sb-text-active` | `#60a5fa` | `#2563eb` |
| `--sb-item-bg` | `rgba(30,41,59,0.3)` | `rgba(226,232,240,0.5)` |
| `--sb-item-bg-hover` | `rgba(30,41,59,0.6)` | `rgba(203,213,225,0.7)` |
| `--sb-item-bg-active` | `rgba(37,99,235,0.2)` | `rgba(59,130,246,0.12)` |
| `--sb-accent` | `#3b82f6` | `#3b82f6` |

Behavior: collapsed state centers icons and hides labels; labels and chevrons fade in on expand with `max-width`/opacity transitions. Active item uses a blue-tinted translucent background and blue active text. Collapsed items reveal CSS tooltips on hover. The active session indicator is a 2px blue bar at the item's left edge.

---

## 8. Application shell

- Full-height flex shell: `h-screen`/`h-dvh`, `overflow-hidden` on the root, with independently scrollable inner regions (`.themed-scrollbar`).
- Background/text use `--theme-bg` / `--theme-text`.
- Main content area is `overflow-hidden`; nested scroll containers handle vertical scroll.
- Hide the product sidebar on embedded/plugin/app-user routes.
- Command palette / search modal: monospace shortcut badge, keyboard-navigable results, dark hardcoded overlay surface.

---

## 9. ChatApp — isolated branded experience

ChatApp is a separately deployable/embedded AI chat experience with its **own** theme system, intentionally isolated from the shell. It must remain visually self-contained: it can be light while the shell is dark.

### 9.1 Isolation guarantee

All ChatApp theme variables are applied as **inline styles on the ChatApp root `<div>`**, never on `document.documentElement`. Inline custom properties cascade downward only, so they cannot leak to or from the shell.

### 9.2 The `--th-*` token contract

ChatApp uses a `--th-*` namespace covering: backgrounds (`--th-bg`, `--th-bg-sidebar`, `--th-bg-surface`, `--th-bg-input`, `--th-bg-header`), text (`--th-text`, `--th-text-secondary`, `--th-text-muted`), borders (`--th-border`, `--th-border-subtle`), accent (`--th-accent`, `-hover`, `-subtle`, `-glow`, `-soft`, `-faint`), bubbles, send button, background animation, input glow, response rendering (steps, code, prose, tables, charts). See `docs/features/chatapp-theming-guide.md` for the full token table.

### 9.3 Theme registry

Seven registered themes, each defining `id`, `label`, `isDark`, `fonts`, `colors`, `shadcnVars`, `cssClass`, `preview`:

| ID | Label | Variant | Heading font | Body font |
|---|---|---|---|---|
| `dark` | Classic | Dark | Outfit | Fira Sans |
| `light` | Light | Light | Outfit | Fira Sans |
| `linear` | Dev Dark | Dark | Inter | Inter |
| `notion` | Notion | Light | Inter | Inter |
| `cursor` | Newspaper | Light | Space Grotesk | Lora |
| `spacex` | Space | Dark | Rajdhani | Inter |
| `liquidglass` | Liquid Glass | Dark | Inter | Inter |

The **Classic** theme (`#0A192F` deep navy, `#007BFF` accent, `#E2E8F0` text) is the canonical ChatApp look and the closest spiritual relative of the shell's dark palette. ChatApp loads its own Google Fonts at runtime; this is an exception to the shell's self-hosted-font rule and is scoped to the ChatApp root only.

---

## 10. Responsive design

Tailwind breakpoints: `sm` 640, `md` 768, `lg` 1024, `xl` 1280.

- `sm`: modest gutter/grid expansion.
- `md`: desktop sidebar appears; 2-column card grids.
- `lg`: 3–4-column card grids; full desktop layout.

Conventions: full-screen pages use `h-screen`/`h-dvh` + `overflow-hidden` with nested scroll; tables/code panes scroll horizontally; use `min-w-0`, `max-w-*`, `truncate`, and `line-clamp-*` to prevent overflow. Page padding 16–24px; card padding 16px; large card/dialog 24px. Design mobile-first where the surface is mobile-aware (ChatApp, dashboards, dialogs); data-heavy admin surfaces may be desktop-first.

---

## 11. Accessibility

- Use Radix primitives for focus management, modal semantics, and keyboard interaction.
- Always provide a **visible focus indicator**: `focus-visible:ring-2 ring-ring ring-offset-2`. Never remove outline without replacing it.
- Use semantic HTML (native `<button>`/`<a>`); use `role="button"` containers only when a native control is impossible, and then add full keyboard handling.
- Provide `sr-only` labels and `aria-*` where semantic HTML is insufficient (icon buttons, close affordances, sidebar triggers).
- Maintain accessible color contrast in both themes (the navy/slate text-on-navy and `#0f172a`-on-white pairings meet AA for body text).
- Honor `prefers-reduced-motion` for non-essential animation.
- Give decorative images empty `alt`; give meaningful images explicit alt text.

---

## 12. Implementation rules

**Do**
- Use the tokens in §2–§5 and the primitives in `src/components/ui/`.
- Support dark, light, and system modes from the start; bootstrap theme before paint.
- Author against semantic tokens so both modes work without `!important` hacks.
- Keep blue accent sparse and purposeful.
- Reuse shared primitives before creating new components.
- Validate every change in both themes, across `sm`/`md`/`lg`, and with keyboard navigation.

**Don't**
- Don't hardcode colors, spacing, radii, shadows, or fonts outside the tokens above.
- Don't create parallel component generations when a primitive exists.
- Don't leak ChatApp `--th-*` variables to `document.documentElement`.
- Don't adopt the legacy `--bg-skin-*`/`--text-skin-*`/`--color-*` namespace in new work.
- Don't use status colors for brand decoration.
- Don't use spring/bounce easing.

---

## 13. Source of truth

| Concern | File |
|---|---|
| Global tokens (Shadcn HSL, status, glass, sidebar, transitions, shadows) | `src/index.css` |
| Runtime theme provider (modes, persistence, `--theme-*` application) | `src/context/ThemeContext.tsx` |
| No-flash bootstrap + preloader | `index.html` |
| Tailwind config (fonts, type scale, radii, animations) | `tailwind.config.cjs` |
| Self-hosted fonts | `public/css/fonts.css` |
| Shared primitives (Button, Input, Card, Dialog, Table, Tabs, Select…) | `src/components/ui/` |
| Product sidebar styles | `src/features/newSidebar/style.css` |
| ChatApp theme registry + `--th-*` contract | `src/features/chatApp/chatapp-themes.ts` |
| ChatApp theme CSS overrides | `src/features/chatApp/chatapp-theme.css` |
| ChatApp theming guide | `docs/features/chatapp-theming-guide.md` |
