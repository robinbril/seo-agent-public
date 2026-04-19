---
name: ads-daily-check
description: Pull yesterday's ads performance across Meta and Google for a client and summarize spend, CPC, CTR, conversions, and top/bottom performers. Use when the user asks for a daily/weekly ads status, performance check, or stand-up.
---

# Daily Ads Check

Quick performance snapshot combining Meta + Google for one client. Safe
— read-only.

## When to use
- "How are ads performing for [client]?"
- "Daily ads check for [client]"
- "Wat doen mijn ads voor [client] vandaag?"

## Inputs
1. **Client** — short ID.
2. **Date range** — default: yesterday. User may say "last 7 days",
   "this week", "since launch".

## Workflow

### Step 1 — Pull Meta insights
`meta-ads-<client>` → `get_insights`:
```
account_id: act_<id from ads-config.json>
level: campaign
date_preset: yesterday  // or last_7d, last_30d
fields: campaign_name, spend, impressions, clicks, ctr, cpc,
        actions, action_values, cost_per_action_type
```

### Step 2 — Pull Google insights
`google-ads-<client>` → `get_campaign_performance`:
```
customer_id: <from ads-config.json>
date_range: YESTERDAY  // or LAST_7_DAYS, LAST_30_DAYS
metrics: cost_micros, impressions, clicks, ctr, average_cpc,
         conversions, cost_per_conversion
```

### Step 3 — Present combined report

```
ADS CHECK — <client> — <date range>

💰 Total spend        : €XX.XX  (Meta €XX + Google €XX)
📊 Total clicks       : NNN
🎯 Avg CTR            : X.XX%
💵 Avg CPC            : €X.XX
✅ Conversions        : N (€XX.XX each)

TOP PERFORMERS
  [Meta]   <campaign>  — €X spend, N clicks, X% CTR, N conversions
  [Google] <campaign>  — €X spend, N clicks, X% CTR, N conversions

UNDERPERFORMERS
  [Meta]   <campaign>  — €X spend, 0 conversions → consider pausing
  [Google] <keyword>   — €X spend, high CPC → consider bid reduction

OBSERVATIONS
  • <pattern in data: e.g. "mobile CTR 2x desktop">
  • <pattern: e.g. "Aalsmeer keywords outperforming Amstelveen 3:1">
```

### Step 4 — Save report
Write to `sites/<client>/rankings/ads-report-YYYY-MM-DD.md`.

### Step 5 — Action items (optional)
If the user wants, offer to:
- Pause underperformers (delegate to `pause-ad` skill)
- Increase budget on top performers (delegate to `adjust-ad-budget`
  skill)
- Draft negative keywords for wasteful Google spend

## Safety rules
- Read-only. No mutations in this skill.
- If a platform's MCP server is not configured, skip that platform and
  flag it in the report.
