---
name: adjust-ad-budget
description: Change the daily or lifetime budget of a Meta or Google Ads campaign/ad set for a client. Use when the user asks to increase, decrease, raise, lower, or set the budget of a campaign. Requires confirmation and a sanity check against spending limits.
---

# Adjust Ad Budget

Updates daily/lifetime budget on a Meta or Google Ads entity. Never
mutates without confirmation.

## When to use
- "Increase budget of [campaign] to €X/day for [client]"
- "Set budget of [campaign] to €X/day"
- "Lower the budget on IG story ad to €X"

## Workflow

### Step 1 — Identify target + new budget
- Client, platform, entity (campaign / ad set).
- New daily budget value in EUR.

### Step 2 — Pull current budget + recent spend
- **Meta**: `get_campaign_info` or `get_insights` → current
  `daily_budget`, last 7d spend.
- **Google**: GAQL for `campaign_budget.amount_micros` and recent
  performance.

### Step 3 — Sanity check
- Is new budget >3x current? Flag as "major change".
- Does new budget exceed `sites/<client>/ads-config.json` →
  `max_daily_budget_eur`? Refuse and flag.
- Does total across all campaigns + new budget exceed
  `account_spending_limit`? Warn.

### Step 4 — Confirm
**"Current budget €X/day, new budget €Y/day (+Z%). Last 7d spend €W.
Shall I apply this change? Reply 'ja' to proceed."**

### Step 5 — Execute
- **Meta**:
  ```
  update_ad_set(ad_set_id, daily_budget: <cents>)
  // campaign-level budget: update_campaign(budget_rebalance_flag=true, ...)
  ```
- **Google**:
  ```
  update_campaign_budget(budget_id, amount_micros: <EUR * 1_000_000>)
  ```

### Step 6 — Verify + log
- Re-fetch budget → confirm new value.
- Append to `sites/<client>/rankings/ads-changelog.md`.

## Safety rules
- Refuse silently-destructive changes (set to 0 = pause → ask if they
  meant to pause, not zero-budget).
- Meta allows a minimum of €1/day; Google allows €0.01/day but ads rarely
  deliver below €3/day. Warn if new budget < €3.
- For a NEW campaign (<48h old), don't allow sudden 5x budget jump —
  Meta's learning phase re-resets and torches performance.
