---
name: launch-instagram-story-ad
description: Create a new Instagram Stories ad (9:16 vertical video/image placement) for a client via the meta-ads-<client> MCP server. Use when the user asks to launch, create, run, or post an Instagram story ad or IG reels ad. Always requires explicit confirmation before mutations.
---

# Launch Instagram Story Ad

Creates a Meta Ads campaign with Instagram Stories placement (9:16 vertical)
via the `meta-ads-<client>` MCP server. **Never** mutates without explicit
confirmation.

> Instagram Stories is a **placement** inside Meta Ads — not a separate
> product. We configure `publisher_platforms = [instagram]` +
> `instagram_positions = [story]` on the ad set.

## When to use
User says things like:
- "Launch Instagram story ad for tpzuyderhoven"
- "Post an IG story campaign for [client]"
- "Run Instagram Stories for [client] with €X/day"

## Inputs to gather (ask if missing)
1. **Client** — short ID matching `meta-ads-<client>` in `.mcp.json`.
2. **Ad account ID** — from `sites/<client>/ads-config.json` →
   `meta_ad_account_id` (format `act_<digits>`).
3. **Page ID** — Instagram account is linked to a Facebook Page; page ID
   from `sites/<client>/ads-config.json` → `meta_page_id`.
4. **Objective** — one of: AWARENESS, TRAFFIC, ENGAGEMENT, LEADS,
   SALES, APP_PROMOTION. Default: TRAFFIC for service businesses.
5. **Daily budget** (EUR).
6. **Audience** — custom from brief, or default from `ads-config.json` →
   `default_audience` (age, gender, interests, location).
7. **Creative** — 9:16 vertical video (<=60s) or image. User provides
   path/URL; if missing, ask.
8. **Primary text + CTA** — Claude drafts from `brand.md`.
9. **Landing URL** — default from `ads-config.json` →
   `default_landing_urls.instagram`, else ask.

## Workflow

### Step 1 — Load client context
- Read `sites/<client>/config.json`, `sites/<client>/brand.md`, and
  `sites/<client>/ads-config.json`.
- Verify account via `meta-ads-<client>` → `check_account_setup` or
  `diagnose_campaign_readiness` with the ad_account_id.

### Step 2 — Draft plan
```
INSTAGRAM STORY AD DRAFT — <client>
Campaign name     : <client>-igstory-<YYYY-MM-DD>-<slug>
Ad account        : act_<id>
Objective         : <e.g. TRAFFIC>
Daily budget      : €X
Placements        : Instagram Stories ONLY (9:16)
Audience          : <age range>, <locations>, <interests>
Creative          : <video/image asset>
Primary text      : <≤125 chars drafted>
Headline          : <≤40 chars drafted>
CTA button        : <e.g. LEARN_MORE, BOOK_TRAVEL, CONTACT_US>
Landing URL       : <url>
```

### Step 3 — Explicit confirmation
Ask verbatim: **"Zal ik deze Instagram Story campaign aanmaken? Reply 'ja'
om door te gaan, of zeg wat ik moet aanpassen."**

### Step 4 — Draft copy
Using `sites/<client>/brand.md`:
- 3 variants of primary text (≤125 chars each)
- 3 headline options (≤40 chars)
- 2 CTA button options

Show variants, let user pick or auto-pick best-fit. Second confirmation.

### Step 5 — Execute mutations (in order)
1. `meta-ads-<client>` → `create_campaign`:
   ```
   account_id: act_<id>
   name: <campaign name>
   objective: <from plan>
   status: PAUSED
   special_ad_categories: []
   ```
2. `create_ad_set`:
   ```
   campaign_id: <from step 1>
   name: <campaign>-adset
   daily_budget: <cents>          // €10/day = 1000
   billing_event: IMPRESSIONS
   optimization_goal: <e.g. LINK_CLICKS for TRAFFIC>
   targeting: {
     geo_locations: { countries: ["NL"], cities: [...] },
     age_min: X, age_max: Y,
     genders: [0],  // 0 = all
     publisher_platforms: ["instagram"],
     instagram_positions: ["story"],
     interests: [...]
   }
   status: PAUSED
   ```
3. `create_ad_creative`:
   ```
   name: <creative name>
   page_id: <from config>
   instagram_actor_id: <IG account id from page>
   object_story_spec: {
     page_id, instagram_actor_id,
     video_data: { video_id: <uploaded>, image_url: <thumbnail>,
                   title: <headline>, message: <primary text>,
                   call_to_action: { type: <CTA>, value: { link: <url> } } }
   }
   ```
   *Note: video upload goes via a separate step. If user passes an image,
   use `image_hash` instead of `video_data`.*
4. `create_ad`:
   ```
   adset_id: <from step 2>
   creative: { creative_id: <from step 3> }
   status: PAUSED
   ```

### Step 6 — Final review + enable
- Show campaign/adset/ad IDs, preview URL (from Meta API response).
- Ask user to verify preview in Ads Manager before enabling.
- On yes: `resume_campaign` (sets status ACTIVE).

### Step 7 — Log
Append to `sites/<client>/rankings/ads-changelog.md`.

## Safety rules
- Always PAUSED until user verifies preview in Ads Manager.
- If creative video/image is missing, ask — never proceed without asset.
- For health/medical clients (e.g. dentists), confirm
  `special_ad_categories` is NOT triggered by audience narrowing; Meta
  auto-flags medical targeting.
- If daily_budget > €50 with no ad history, double-confirm.
- Store creative file paths/IDs in `sites/<client>/rankings/ads-changelog.md`
  so you can rebuild the campaign later.
