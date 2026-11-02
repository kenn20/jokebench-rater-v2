# JokeBench Rater Design System

## 0. Research Log
- Embedded refs: shortlisted Linear, Vercel, and Sentry → picked taste-skill + Linear because this is an operational reviewer surface requiring calm density and precise status hierarchy.
- Lazyweb: skipped — no lazyweb browsing tool available in this environment.
- Imagen drafts: skipped — no image-generation tool available; the product’s focal object is the live rating card, not decorative imagery.

## 1. Atmosphere & Identity
A focused evaluation desk: dark, quiet, and slightly editorial so the joke is the visual event. Signature: a luminous paper-like quote field nested in dark precision chrome, making one choice feel deliberate rather than gamified.

## 2. Color
| Role | Token | Value | Usage |
|---|---|---|---|
| Canvas | `--canvas` | `#08090a` | Page background |
| Panel | `--panel` | `#0f1011` | Header and side panels |
| Raised | `--raised` | `#191a1b` | Rating card |
| Text | `--text` | `#f7f8f8` | Primary content |
| Muted | `--muted` | `#a7acb4` | Supporting copy |
| Faint | `--faint` | `#6f747d` | Metadata |
| Border | `--border` | `rgba(255,255,255,.09)` | Surface separation |
| Accent | `--accent` | `#7170ff` | Active controls and progress |
| Accent hover | `--accent-hover` | `#828fff` | Interactive hover |
| Success | `--success` | `#27a644` | Completion state |
| Not funny | `--not-funny` | `#d7765d` | Negative rating action |

## 3. Typography
- Primary: `ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`
- Mono: `ui-monospace, SFMono-Regular, Menlo, monospace`
- Display: `clamp(2rem, 5vw, 4rem)` / 510 / 1.0; body: 16px / 1.55; metadata: 12px / 1.4.

## 4. Spacing & Layout
- Base unit: 4px. Scale: 4, 8, 12, 16, 20, 24, 32, 48, 64px.
- Max content: 1120px. Two-column evaluator layout at 761px+, single column at 760px and below.
- Primary content never horizontally scrolls; controls are minimum 44px tall.

## 5. Components
### Rating card
- Structure: context strip, joke text, rating actions, feedback state.
- States: unrated, selected-funny, selected-not-funny, complete; hover, active, keyboard focus.
- Accessibility: `article`, live result message, real buttons, text labels in addition to color.
- Motion: 180ms opacity/transform feedback; reduced motion removes transforms.

### Progress rail
- Structure: numeric count, progress bar, completion chip.
- States: in-progress and complete; status conveyed by text and bar.

### Export controls
- Structure: JSON and CSV buttons.
- States: disabled until one rating exists, enabled, downloaded announcement.
- Accessibility: clear labels and polite live region.

## 6. Motion & Interaction
- Button press: 120ms ease-out scale transform; hover: 180ms ease-out color/opacity.
- Rating selection advances to the next unresolved item after 220ms; reduced motion advances immediately.

## 7. Depth & Surface
- Strategy: tonal shift with whisper borders. Raised cards use `--raised`, one `--border`, and subtle inset highlight; no floating drop-shadow stacks.

## 8. Accessibility Constraints & Accepted Debt
- WCAG 2.2 AA contrast target; keyboard operation for rating and exports; touch targets ≥44px; visible focus rings; reduced-motion support.
- Accepted debt: none.
