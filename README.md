# Robin's Marketing Engine — SEO + Meta Ads + Google Ads

> One terminal-driven pipeline that does organic SEO **and** paid campaigns
> for your clients. Keyword research, content writing, backlink building,
> local citations, Meta Ads, Google Ads — all from Claude Code, with a
> per-client isolation pattern so every account has its own scoped tokens.

---

## What this does

**Organic SEO**
- **Finds keywords your competitors rank for, but you don't** — runs gap analysis via Brave Search and outputs a prioritized list of content opportunities
- **Writes SEO-optimized articles** based on your brand voice (`brand.md`), competitor analysis, and target keywords — with title, meta description, H1/H2 structure, and FAQ section included
- **Discovers backlink and citation opportunities** — finds guest post targets, directories, and local citation sources for your niche and city
- **Tracks your Google rankings weekly** — compares current positions to last week and reports which keywords moved up or down

**Paid Ads**
- **Manages Meta Ads campaigns** (create, pause, resume, update budget, read insights) through a per-client MCP server built on `brijr/meta-mcp`
- **Manages Google Ads campaigns** (create campaigns + ad groups, add keywords, update bids, read performance) through `itallstartedwithaidea/google-ads-mcp`
- **Per-client isolation** — each client gets their own `meta-ads-<client>` and `google-ads-<client>` server with scoped tokens, so you can rotate or revoke one client without touching the others

---

## Results you can expect

These are realistic timelines based on how local SEO and paid ads work — not guarantees.

| Scenario | Timeline |
|---|---|
| Local niche with low competition (e.g. "accountant Tilburg") | Top 3 in 4–8 weeks (organic) |
| Regional service keyword (e.g. "vastgoed financieren Amstelveen") | Top 5 in 6–12 weeks (organic) |
| National competitive keyword (e.g. "zakelijke hypotheek") | 3–6 months organic, depends on domain authority |
| New domain with no content | 2–4 weeks before Google starts indexing |
| Paid Meta/Google traffic | Same day (if developer token and Business Manager are set up) |

What actually moves the needle:
1. Publishing 3–5 well-structured articles per week
2. Getting 5–10 relevant backlinks per month
3. Consistent NAP data across local directories
4. Tracking and responding to ranking changes weekly
5. Running paid ads alongside organic while SEO takes hold (months 1–3)

---

## How it works

```
No rankings, no traffic
    │
    ▼
[1] Keyword gap analysis
    → Find keywords competitors rank for, you don't
    → Output: briefs/keyword-gaps-YYYY-MM-DD.md
    │
    ▼
[2] Competitor content analysis
    → Scrape top-ranking pages, extract structure + semantics
    → Output: briefs/competitor-[name]-YYYY-MM-DD.md
    │
    ▼
[3] Content generation
    → Write SEO articles based on brand.md + competitor analysis
    → Output: content/[slug].md
    │
    ▼
[4] Backlink + citation building
    → Find guest post targets, directories, outreach emails
    → Output: briefs/backlinks-YYYY-MM-DD.json
    │
    ▼
[5] Paid ads (parallel to SEO)
    → Meta Ads + Google Ads campaigns via per-client MCP servers
    → Output: sites/<client>/rankings/ads-report-YYYY-MM-DD.md
    │
    ▼
[6] Weekly ranking + ads tracking
    → Compare positions + campaign performance week-over-week
    → Output: rankings/report-YYYY-MM-DD.md
    │
    ▼
Rank #1 + profitable ads
```

---

## Prerequisites

**For SEO (baseline)**
- **Python 3.10+** — [download here](https://www.python.org/downloads/)
- **Claude Code** — `npm install -g @anthropic-ai/claude-code` (requires Node.js 18+)
- **Brave Search API key** — free tier available at [brave.com/search/api](https://brave.com/search/api/)
- **Git** — [download here](https://git-scm.com/downloads)
- Optional: `ANTHROPIC_API_KEY` for AI-powered outreach email generation

**For Meta Ads** (optional, see [docs/ADS-MCP-SETUP.md](docs/ADS-MCP-SETUP.md))
- Your own Meta developer app (App ID + App Secret)
- A system-user token per client Business Manager

**For Google Ads** (optional, see [docs/ADS-MCP-SETUP.md](docs/ADS-MCP-SETUP.md))
- Google Cloud OAuth 2.0 Client ID + Secret
- Google Ads developer token (Test or Basic access)
- A refresh token generated with your MCC-access account
- `uv` / `uvx` — `curl -LsSf https://astral.sh/uv/install.sh | sh`

---

## Quick Start (5 minutes, SEO only)

**Step 1 — Clone the repo**
```bash
git clone https://github.com/robinbril/seo-agent-public.git
cd seo-agent-public
```

**Step 2 — Install Python dependencies**
```bash
pip install -r scripts/requirements.txt
```

**Step 3 — Copy env template and fill in secrets**
```bash
cp .env.example .env
# Edit .env: fill in BRAVE_API_KEY (minimum). Add Meta + Google Ads keys later.
```

**Step 4 — Fill in `config.json`**
Open the file and replace the placeholder values. See "Config reference" section below for what each field means.

**Step 5 — Fill in `brand.md`**
Describe your business, tone of voice, services, and competitors. The AI uses this file to write content that sounds like you.

**Step 6 — Open Claude Code and run your first command**
```bash
claude
```
Then type:
```
Run keyword gap analysis
```

That's it. Claude reads your config, runs the Python script, and writes a brief to `briefs/`.

**For ads, continue with [docs/ADS-MCP-SETUP.md](docs/ADS-MCP-SETUP.md).**

---

## Commands

All commands are typed directly into Claude Code.

### Organic SEO

| Command | What it does | Output |
|---|---|---|
| `Run keyword gap analysis` | Finds keywords competitors rank for that you don't | `briefs/keyword-gaps-YYYY-MM-DD.md` |
| `Analyze competitor content for [URL]` | Extracts word count, headings, semantic keywords | `briefs/competitor-[name]-YYYY-MM-DD.md` |
| `Write an article about [topic]` | Runs competitor analysis then writes SEO article | `content/[slug].md` |
| `Track rankings for all keywords` | Runs weekly rank tracker, compares to last week | `rankings/report-YYYY-MM-DD.md` |
| `Find backlink opportunities` | Finds guest post + backlink targets | `briefs/backlinks-YYYY-MM-DD.json` |
| `Generate outreach for [target-url]` | Writes guest post article + outreach email | `briefs/outreach-[domain]-YYYY-MM-DD.md` |
| `Find citation opportunities for [city]` | Finds local directories for your niche + city | `briefs/citations-[city]-YYYY-MM-DD.md` |
| `Run full SEO audit` | Keyword gaps + competitor analysis + ranking report | multiple files |
| `Run full SEO pipeline` | Keyword gaps → articles → backlinks → citations | multiple files |

### Paid Ads (after setup)

| Command | What it does |
|---|---|
| `Check ads performance for [client] last [N] days` | Pulls insights from Meta + Google Ads |
| `Launch new [platform] campaign for [client] targeting [topic] with budget €X/day` | Drafts + launches after your confirmation |
| `Pause [campaign name] for [client]` | Pauses a specific campaign (confirmation required) |
| `Set budget of [campaign name] to €X/day for [client]` | Updates daily budget (confirmation required) |

All mutations require explicit confirmation before execution — see safety rules in `CLAUDE.md`.

---

## Works with

| Tool | How |
|---|---|
| **Claude Code** | Primary use case. Project-scoped `.mcp.json` wires up ads servers automatically. |
| **Cursor** | Open repo in Cursor, use the chat panel. Ads MCP servers need manual wiring. |
| **Windsurf** | Same as Cursor. |
| **ChatGPT (manual)** | Copy `CLAUDE.md` content into a ChatGPT conversation, then run scripts manually in your terminal. No ads support. |
| **Gemini CLI** | `gemini` in terminal, same SEO commands work. No ads support. |

---

## Config reference (`config.json`)

```json
{
  "site_name": "Your Site Name",         // Display name for reports
  "domain": "yoursite.com",              // Your domain without https://
  "niche": "zakelijk vastgoed",          // Your niche/industry (used in search queries)
  "target_keywords": ["keyword 1"],      // Primary keywords to track
  "target_location": "Amsterdam",        // Your city or region
  "competitors": ["competitor.nl"],      // Competitor domains (no https://)
  "language": "nl",                      // nl or en
  "serp_location": "nl",                 // Country for Google results (nl, de, us, etc.)
  "weekly_tracking_day": "monday"        // Day to run rank tracker
}
```

---

## Folder structure

```
seo-agent-public/
├── scripts/
│   ├── keyword_gaps.py                   # Keyword gap analysis via Brave Search
│   ├── scraper.py                        # Competitor page scraper
│   ├── rank_tracker.py                   # Weekly ranking tracker
│   ├── backlink_finder.py                # Finds guest post + backlink targets
│   ├── outreach_generator.py             # Writes outreach emails + guest posts
│   ├── citation_builder.py               # Finds local directory listing opportunities
│   ├── google_ads_get_refresh_token.py   # OAuth bootstrap for Google Ads MCP
│   └── requirements.txt                  # Python dependencies
├── docs/
│   └── ADS-MCP-SETUP.md                  # Full walkthrough for Meta + Google Ads
├── sites/                                # Multi-site setup (one subfolder per site)
├── content/                              # Generated articles saved here
├── briefs/                               # Keyword analyses, competitor reports, backlink lists
├── rankings/                             # Weekly ranking + ads snapshots
├── .env.example                          # Template for secrets (never commit .env)
├── .mcp.json                             # Project-scoped MCP server definitions
├── config.json                           # Your domain, keywords, competitors
├── brand.md                              # Your brand voice and services
├── CLAUDE.md                             # Instructions for the AI agent
└── SETUP.md                              # Detailed SEO setup guide
```

---

## FAQ

**1. Do I need to pay for the Brave Search API?**
The free tier gives you 2,000 queries/month. That's enough for weekly keyword tracking + a few analyses. Paid plans start at $3/1,000 queries if you need more.

**2. Does the ads stack work without Claude Code?**
The ads stack relies on Claude Code's MCP loader. Cursor and Windsurf can manually wire MCP servers but it's less polished. ChatGPT cannot call MCP tools.

**3. What Python version do I need?**
Python 3.10 or higher. Check with `python --version` or `python3 --version`.

**4. How do I manage multiple clients?**
Put each client's site in its own subfolder under `sites/`, and add a `meta-ads-<client>` + `google-ads-<client>` entry per client in `.mcp.json`. See [docs/ADS-MCP-SETUP.md](docs/ADS-MCP-SETUP.md) §5.

**5. Will this get my site penalized by Google?**
No. The scripts use the official Brave Search API (not scraping Google). Content is written by AI using your brand voice — Google's issue is low-quality content, not AI-generated content per se. Write for humans, not for bots.

**6. How many articles should I publish per week?**
For local niche: 2–3 per week is enough. For national keywords: 5+ per week, plus active backlink building.

**7. Why `brijr/meta-mcp` and `itallstartedwithaidea/google-ads-mcp` specifically?**
They're the only widely-used MIT-licensed MCP servers that actually support write operations (`create_campaign`, `update_campaign_budget`, etc.). Most popular alternatives (`cohnen/mcp-google-ads`, `gomarble-ai/*`, even Google's official `googleads/google-ads-mcp`) are read-only. See [docs/ADS-MCP-SETUP.md](docs/ADS-MCP-SETUP.md) §7 for the rejection list.

**8. Can I use this for e-commerce sites?**
The SEO scripts are optimized for local service businesses and content sites. The ads stack works for any vertical.

**9. How do I see which keywords I'm ranking for right now?**
Run `Track rankings for all keywords` in Claude Code. First run creates a baseline; second run (next week) shows movement.

**10. The outreach email generator is not working well. Why?**
Set `ANTHROPIC_API_KEY` in your environment for AI-powered generation. Without it, the script falls back to a basic template.

**11. Can the ads MCP accidentally spend my client's budget?**
Only if you tell it to. `CLAUDE.md` hard-requires explicit user confirmation before any `create_*`, `update_*_budget`, or `update_*_status` call. Treat Claude as a junior media buyer — always check the plan before approving.

---

## Detailed setup

- SEO: [SETUP.md](SETUP.md)
- Meta + Google Ads: [docs/ADS-MCP-SETUP.md](docs/ADS-MCP-SETUP.md)
