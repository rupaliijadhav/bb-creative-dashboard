# CLAUDE.md — BB Google Ads Optimization Agent

## Project Overview

This repository contains the **BB Google Creative Dashboard**, a single-page analytics interface for monitoring and optimizing Google Ads creative performance. The dashboard visualizes key ad metrics (CTR, ROAS, CPA, impressions, spend) across campaigns, ad groups, and individual creatives.

## Account Context

Fill these in before starting a session:

- **Business type:** [e.g. ecommerce, lead gen, SaaS]
- **Monthly budget:** [e.g. $5,000]
- **Target CPA:** [e.g. $25]
- **Target ROAS:** [e.g. 4×]

---

## Agent Purpose

This agent assists with **Google Ads creative optimization**: analyzing performance data surfaced in the dashboard, identifying underperforming creatives, recommending copy/asset changes, and implementing dashboard UI improvements to better support optimization workflows.

---

## Repository Structure

```
bb-creative-dashboard/
├── index.html                  # Primary dashboard (use this as the source of truth)
├── BB_Dashboard_FINAL.html     # Archived snapshot
├── BB_Dashboard_FINAL (1).html # Archived snapshot
└── CLAUDE.md                   # This file
```

> All active development happens in `index.html`. The `BB_Dashboard_FINAL*.html` files are reference snapshots — do not modify them.

---

## MCP Server Setup

This project connects to Google Ads via the `@hapotech/google-ads-mcp` MCP server. Configuration lives in `.mcp.json` at the repo root.

### Required credentials

| Variable | Where to get it |
|----------|----------------|
| `GOOGLE_ADS_CLIENT_ID` | Google Cloud Console → OAuth 2.0 client |
| `GOOGLE_ADS_CLIENT_SECRET` | Google Cloud Console → OAuth 2.0 client |
| `GOOGLE_ADS_REFRESH_TOKEN` | Run OAuth flow with your client credentials |
| `GOOGLE_ADS_DEVELOPER_TOKEN` | Google Ads UI → Tools → API Center |
| `GOOGLE_ADS_LOGIN_CUSTOMER_ID` | Your top-level MCC account ID (digits only, no dashes) |

Fill in the placeholder values in `.mcp.json` — never commit real credentials to version control. To use real credentials locally, copy `.mcp.json` to `.mcp.local.json` (gitignored) and fill in the values there.

---

## Tech Stack

- **Pure HTML/CSS/JS** — no build step, no package manager, no framework
- **Chart.js 4.4.1** (CDN) — all data visualizations
- **Google Fonts** — DM Mono + Clash Display
- **No backend** — data is currently hardcoded; future iterations may connect to the Google Ads API

### Design System (CSS custom properties)

| Variable | Role |
|----------|------|
| `--bg / --s0–s3` | Background layers (darkest → lightest) |
| `--b0–b2` | Border/surface colors |
| `--cy` `#00d9f5` | Cyan — primary accent, CTR / clicks |
| `--pu` `#b06ef3` | Purple — secondary accent, ROAS |
| `--am` `#f5a623` | Amber — warnings, CPC |
| `--gn` `#17d4a0` | Green — positive signals, conversions |
| `--rd` `#f04e6e` | Red — negative signals, high CPA |
| `--in` `#6c7ef8` | Indigo — impressions |
| `--tx / --mu` | Primary / muted text |

Always use these variables — never hardcode hex values in new CSS.

---

## Google Ads Optimization Domain

### Key Metrics to Track

| Metric | Good Signal | Warning Signal |
|--------|-------------|----------------|
| **CTR** | > 5% (search), > 0.35% (display) | < 2% (search), < 0.1% (display) |
| **ROAS** | > 4× | < 2× |
| **CPA** | Below target CPA | > 150% of target |
| **Quality Score** | 7–10 | < 5 |
| **Impression Share** | > 70% | < 40% |

### Creative Optimization Priorities

1. **Headline testing** — rotate 3–5 headlines per RSA; pin only when statistically necessary
2. **Description copy** — lead with value proposition, include CTA and social proof
3. **Asset strength** — target "Excellent" rating in Google Ads UI; flag "Poor" assets for replacement
4. **Ad relevance** — align headline keywords with ad group themes (boosts Quality Score)
5. **Landing page alignment** — ensure creative messaging matches LP headline and offer

### Optimization Workflow

```
Analyze dashboard metrics
    → Identify creatives with CTR < threshold or CPA > target
    → Audit headline/description asset combinations
    → Propose new copy variants
    → Implement changes in dashboard mock data
    → Document rationale in commit message
```

---

## Development Guidelines

### Making Changes

1. **Read before editing** — always read `index.html` before modifying it
2. **Preserve the design system** — use existing CSS variables; do not introduce new color values
3. **Chart.js patterns** — follow existing dataset/options patterns when adding new charts
4. **Mobile-first** — the `.shell` container is responsive; maintain `flex-wrap` on new row components
5. **No build step** — open `index.html` directly in a browser to verify changes

### Adding New Metrics / Panels

- Copy the structure of an existing metric card (look for `.kpi-card` or similar class patterns)
- Use the correct semantic color variable for the metric type (e.g., `--rd` for high CPA alerts)
- Label all new data points with units in the UI (%, ×, $, #)

### Data Updates

Currently all chart data is hardcoded in `<script>` blocks inside `index.html`. When updating mock data:
- Keep date ranges consistent across all charts
- Use realistic Google Ads benchmark ranges (see table above)
- Comment the data block with the date range it represents

---

## Commit Message Convention

```
<type>: <short description>

Types:
  feat     — new dashboard panel or metric
  fix      — bug or display issue
  data     — mock data refresh or scenario update
  opt      — creative optimization recommendation implemented
  refactor — code cleanup with no visual change
  docs     — CLAUDE.md or inline comment updates
```

Example:
```
opt: flag RSA assets with CTR < 2% using --rd accent color

Identified 3 creatives in the Search campaign group with CTR
below threshold. Added red badge indicator and tooltip with
recommended replacement copy.
```

---

## Slash Commands

| Command | Action |
|---------|--------|
| `/audit` | Full account health check across all campaigns |
| `/waste` | Find budget-wasting keywords (high spend, zero conversions) |
| `/report` | Weekly performance summary (CTR, CPA, ROAS, spend vs budget) |
| `/negatives` | Build negative keyword list from search term report |
| `/copy` | Generate new ad copy variants for a given ad group |

---

## Output Format

Every agent response must follow this structure:

1. **Summary** — one-sentence status
2. **Key findings** — bulleted, metric-backed observations
3. **Recommended actions** — specific, prioritized next steps
4. **What needs your approval** — list anything requiring human sign-off before execution

---

## Agent Behavior Rules

1. **Never pause campaigns** without explicit user confirmation
2. **Flag spend deviations > 20%** above or below expected pacing immediately
3. **Suggest before executing** — always present recommendations and wait for approval before making changes
4. **Never modify** `BB_Dashboard_FINAL.html` or `BB_Dashboard_FINAL (1).html`
5. **Do not introduce** external dependencies beyond Chart.js and Google Fonts (already loaded via CDN)
6. **Validate metric logic** — optimization recommendations must cite the metric thresholds defined above or provide a source
7. **Security** — this dashboard is client-side only; do not add form submissions, fetch calls to unauthenticated endpoints, or eval() usage
8. **Commit and push** all changes to the active feature branch (never push directly to `main` or `master` without review)
9. **One concern per commit** — keep commits focused; separate data changes from UI changes

---

## Branch Strategy

- `main` / `master` — stable, deployed snapshots only
- `claude/<task-id>` — all agent-driven development (current: `claude/create-google-ads-claude-md-occDR`)

Always verify the active branch before committing:
```bash
git branch --show-current
```
