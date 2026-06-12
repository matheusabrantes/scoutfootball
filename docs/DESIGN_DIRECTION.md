# ScoutFootball Design Direction

## Design Goal

ScoutFootball should feel premium, focused, and fast. The design should combine Apple-like restraint with the efficiency of professional sports analysis software. It should not look like a dense dashboard or a clone of any reference football site.

## Visual Principles

- Light interface by default.
- High contrast where data legibility matters.
- Large spacing on content pages, tighter density in tables.
- Premium typography with restrained sizing.
- Subtle borders, fine separators, and soft shadows only where depth helps.
- Minimal color usage, reserved for semantic status, percentiles, and selected controls.
- Smooth but quiet hover, focus, and transition states.
- Mobile layouts that prioritize search, filters, and readable tables.

## Product Layout

### App Shell

- Top navigation with product name, main routes, and search entry.
- Main content constrained to readable width on editorial pages.
- Full-width table and comparison views with aligned filter bars.
- Sticky filter bar on database, rankings, and compare pages.
- Clear route-specific page titles and compact supporting context.

### Landing Page

- First viewport should make the product immediately identifiable as ScoutFootball.
- Include a prominent search input and "Explore Players" CTA.
- Show supported league coverage early.
- Avoid marketing-heavy sections before the usable product entry.
- Use real product UI previews only after the primary search/CTA area.

### Data Pages

- Use segmented controls for position groups.
- Use menus/selects for league, season, club, nationality, and metric selection.
- Use numeric inputs or sliders for age and minutes ranges.
- Use compact chips for active filters.
- Keep table interactions fast and predictable.

## Components

### Player Table

- TanStack Table for sorting, filtering, and column management.
- Sticky header.
- Compact rows with clear player identity, club, age, minutes, and selected metrics.
- D3-powered percentile mini bars where useful.
- No radar charts or scatter plots in MVP.

### Player Cards

- Use cards for individual repeated player summaries only.
- Show name, age, nationality, club, league, position group, minutes, and top percentile metrics.
- Keep card radius at 8px or less unless the future design system says otherwise.

### Metric Cards

- Label, raw value, percentile, availability status, and short tooltip.
- Percentile visualization should be a subtle horizontal bar.
- Approximation and unavailable states must be visible without overwhelming the page.

### Comparison Table

- Columns are players.
- Rows are metrics.
- Display raw value and percentile together.
- Highlight best value per row subtly.
- Avoid chart-heavy presentation.

## Motion

- Use motion to clarify state changes, not decorate.
- Hover states should respond within 150ms.
- Filter changes should not shift layout unexpectedly.
- Loading states should preserve table and card dimensions.

## Typography

- Prefer a system font stack initially.
- Use clear hierarchy:
  - Page title.
  - Section heading.
  - Control label.
  - Table text.
  - Small metadata.
- Do not scale text with viewport width.
- Do not use negative letter spacing.

## Color Guidance

- Base: white, near-white, charcoal text, neutral borders.
- Accent: one restrained accent for selected states.
- Data: percentile scale should be subtle and readable, not rainbow-heavy.
- Avoid one-note palettes dominated by purple, dark blue, beige, brown, or heavy gradients.

## Accessibility

- Keyboard focus visible on all interactive elements.
- Sufficient contrast for text, borders, and active states.
- Buttons and controls have accessible names.
- Tooltips supplement labels but do not replace essential text.
- Tables remain navigable with screen readers where practical.

## UX Rules

- Do not use visible text to explain generic app behavior or keyboard shortcuts.
- Do not nest cards inside cards.
- Do not use decorative gradient blobs, orbs, or bokeh backgrounds.
- Do not allow text to overflow buttons, cards, filters, or table cells.
- Use icons for familiar actions when icon meaning is obvious.
- Use text buttons for commands that need clarity.

