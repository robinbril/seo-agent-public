---
name: pause-ad
description: Pause a Meta or Google Ads campaign, ad set, ad group, or ad for a client. Use when the user asks to pause, stop, disable, or turn off a specific campaign/ad. Requires confirmation.
---

# Pause Ad

Pauses an active ad entity on Meta or Google. Never runs without
confirmation.

## When to use
- "Pause [campaign name] for [client]"
- "Stop de IG story ad voor [client]"
- "Turn off the [keyword] Google campaign for [client]"

## Workflow

### Step 1 — Identify target
Ask if ambiguous:
- Which client?
- Which platform (Meta / Google)?
- Which level (campaign / ad set / ad group / specific ad)?
- Which name or ID?

### Step 2 — Look up current state
- **Meta**: `meta-ads-<client>` → `get_insights` or `list_campaigns`
  filtered by name. Show current status, spend-to-date, last 7d metrics.
- **Google**: `google-ads-<client>` → GAQL query for the campaign/ad group,
  show status + recent performance.

### Step 3 — Confirm
Ask verbatim:
**"Current status: [ACTIVE]. Last 7d: €X spend, N clicks, X conversions.
Shall I pause this? Reply 'ja' to proceed."**

### Step 4 — Execute
- **Meta**: `pause_campaign(campaign_id)` OR
  `update_ad_set(status: PAUSED)` OR `update_ad(status: PAUSED)`.
- **Google**: `update_campaign_status(status: PAUSED)` OR
  `update_ad_group_status(status: PAUSED)`.

### Step 5 — Verify + log
- Re-fetch status → confirm it's PAUSED.
- Append to `sites/<client>/rankings/ads-changelog.md`:
  ```
  ## YYYY-MM-DD HH:MM — Paused <entity> on <platform>
  - Name/ID: <...>
  - Reason: <if user gave one>
  - Status before: ACTIVE → after: PAUSED
  ```

## Safety rules
- NEVER pause without confirmation, even if user seems certain — state
  the current spend/performance first.
- If the entity is already PAUSED, say so and skip the mutation.
- Pausing a CAMPAIGN cascades to all child ad sets/ad groups — warn user
  before a campaign-level pause.
