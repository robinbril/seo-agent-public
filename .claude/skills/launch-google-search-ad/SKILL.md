---
name: launch-google-search-ad
description: Create a new Google Search (keyword) ad campaign for a client via the google-ads-<client> MCP server. Use when the user asks to launch, start, run, or set up a Google Ads / Google Search / keyword / SEA campaign. Always requires explicit confirmation before mutations.
---

# Launch Google Search Ad Campaign

Creates a keyword-based Search campaign in Google Ads via the
`google-ads-<client>` MCP server. **Never** mutates without explicit
confirmation.

## When to use
User says things like:
- "Launch Google Ads campaign for tpzuyderhoven"
- "Set up keyword ads for [client] targeting [keyword]"
- "Run search ads for [client] with €X/day"

## Inputs to gather (ask if missing)
1. **Client** — short ID (e.g. `tpzuyderhoven`). Must match a server in
   `.mcp.json` (`google-ads-<client>`).
2. **Daily budget** (EUR). Default: `sites/<client>/ads-config.json` →
   `default_daily_budget_eur`, else ask.
3. **Keywords** — list of target keywords. Derive from
   `sites/<client>/config.json` → `target_keywords` if user said "default".
4. **Match types** — BROAD, PHRASE, EXACT. Default: PHRASE + EXACT combo.
5. **Landing URL** — destination page. Default from
   `sites/<client>/ads-config.json` → `default_landing_urls.search`, else ask.
6. **Location targeting** — default from `sites/<client>/config.json` →
   `target_location` + surrounding geo (e.g. radius). Confirm with user.
7. **Campaign name** — propose `<client>-search-<YYYY-MM-DD>-<keyword-slug>`.

## Workflow

### Step 1 — Load client context
- Read `sites/<client>/config.json`, `sites/<client>/brand.md`, and
  `sites/<client>/ads-config.json` (if exists).
- Confirm Customer ID via `google-ads-<client>` → `list_accounts`.

### Step 2 — Draft plan
Output a compact plan to the user:
```
CAMPAIGN DRAFT — Google Search for <client>
Name          : <proposed name>
Customer ID   : <10-digit>
Daily budget  : €X
Bidding       : MAXIMIZE_CLICKS (start) / TARGET_CPA (if conversions set up)
Locations     : <cities + radius>
Languages     : Dutch, English
Ad group      : <name>
Keywords      :
  • "<kw1>" [PHRASE]
  • "<kw2>" [EXACT]
  • ...
Negatives     : (add common: free, jobs, vacature, reviews for dentists)
Landing URL   : <url>
Ad assets     : RSA — 15 headlines + 4 descriptions (Claude will draft)
```

### Step 3 — Explicit confirmation
Ask verbatim: **"Shall I create this campaign now? Reply 'ja' to proceed,
or tell me what to change."**

Only continue if the user says yes / ja / go / approve. ANY other answer
= revise the plan.

### Step 4 — Draft ad copy
Using `sites/<client>/brand.md` for voice:
- Generate 15 RSA headlines (≤30 chars each), mix of benefit-driven,
  keyword-loaded, and call-to-action.
- Generate 4 descriptions (≤90 chars each) covering USP, trust signals,
  CTA, location.
- Generate 2 sitelinks + 1 callout extension suggestion.

Show the copy to the user before committing. Second confirmation for copy.

### Step 5 — Execute mutations (in order)
1. `google-ads-<client>` → `create_campaign` with:
   ```
   advertising_channel_type: SEARCH
   status: PAUSED   // always start paused for safety
   budget_amount_micros: <daily_budget * 1_000_000>
   bidding_strategy_type: MAXIMIZE_CLICKS
   geo_target_constants: <from location config>
   language_constants: [nl, en]
   ```
2. `create_ad_group` → inside the new campaign.
3. `add_keywords` → with match types as planned.
4. `add_negative_keywords` → common negatives + any user-specified.
5. `generic_mutate` (if needed for RSA creation) — create responsive
   search ad with the drafted headlines + descriptions.

### Step 6 — Final review + enable
- Show user: campaign ID, ad group ID, keyword count, ad preview.
- Ask: **"Alles ziet er goed uit — zal ik de campaign nu ENABLED
  zetten?"**
- On yes: `update_campaign_status` → ENABLED.

### Step 7 — Log
Append to `sites/<client>/rankings/ads-changelog.md`:
```
## YYYY-MM-DD HH:MM — Google Search campaign launched
- Name: <name>
- Campaign ID: <id>
- Daily budget: €X
- Keywords: N (<match mix>)
- Status at launch: ENABLED / PAUSED
- Launched by: Claude via google-ads-<client>
```

## Safety rules
- Always start campaign in PAUSED state; only set ENABLED after user
  confirms ad copy.
- If `developer_token` is Test access, warn user that live accounts
  won't accept mutations and abort.
- Respect budget sanity: if daily_budget > €50 and the client has no
  prior ads history, double-confirm.
- Never use `generic_mutate` for anything a typed tool can do.
