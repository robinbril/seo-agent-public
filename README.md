# SEO Agent - AI-powered SEO automation for Claude Code

> Rank #1 on Google with a fully automated SEO pipeline. Keyword research, content writing, backlink building, local citations — all from your terminal with Claude Code.

---

## What this does

- **Finds keywords your competitors rank for, but you don't** — runs gap analysis via Brave Search and outputs a prioritized list of content opportunities
- **Writes SEO-optimized articles** based on your brand voice (`brand.md`), competitor analysis, and target keywords — with title, meta description, H1/H2 structure, and FAQ section included
- **Discovers backlink and citation opportunities** — finds guest post targets, directories, and local citation sources for your niche and city
- **Tracks your Google rankings weekly** — compares current positions to last week and reports which keywords moved up or down

---

## Results you can expect

These are realistic timelines based on how local SEO works — not guarantees.

| Scenario | Timeline |
|---|---|
| Local niche with low competition (e.g. "accountant Tilburg") | Top 3 in 4–8 weeks |
| Regional service keyword (e.g. "vastgoed financieren Amstelveen") | Top 5 in 6–12 weeks |
| National competitive keyword (e.g. "zakelijke hypotheek") | 3–6 months, depends on domain authority |
| New domain with no content | 2–4 weeks before Google starts indexing |

What actually moves the needle:
1. Publishing 3–5 well-structured articles per week
2. Getting 5–10 relevant backlinks per month
3. Consistent NAP data across local directories
4. Tracking and responding to ranking changes weekly

---

## How it works

```
No rankings
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
[5] Weekly ranking tracking
    → Compare positions week-over-week
    → Output: rankings/report-YYYY-MM-DD.md
    │
    ▼
Rank #1
```

---

## Prerequisites

- **Python 3.10+** — [download here](https://www.python.org/downloads/)
- **Claude Code** — `npm install -g @anthropic-ai/claude-code` (requires Node.js 18+)
- **Brave Search API key** — free tier available at [brave.com/search/api](https://brave.com/search/api/)
- **Git** — [download here](https://git-scm.com/downloads)
- Optional: `ANTHROPIC_API_KEY` for AI-powered outreach email generation

---

## Quick Start (5 minutes)

**Step 1 — Clone the repo**
```bash
git clone https://github.com/robinbril/seo-agent-public.git
cd seo-agent-public
```

**Step 2 — Install Python dependencies**
```bash
pip install -r scripts/requirements.txt
```

**Step 3 — Set your Brave API key**

On Mac/Linux:
```bash
export BRAVE_API_KEY=your_key_here
```

On Windows (PowerShell):
```powershell
$env:BRAVE_API_KEY = "your_key_here"
```

**Step 4 — Fill in `config.json`**
```bash
# Open the file and replace the placeholder values
# See "Config reference" section below for what each field means
```

**Step 5 — Fill in `brand.md`**
```bash
# Describe your business, tone of voice, services, and competitors
# The AI uses this file to write content that sounds like you
```

**Step 6 — Open Claude Code and run your first command**
```bash
claude
```

Then type:
```
Run keyword gap analysis
```

That's it. Claude reads your config, runs the Python script, and writes a brief to `briefs/`.

---

## Commands

All commands are typed directly into Claude Code (or your AI tool of choice).

### Keyword research
```
Run keyword gap analysis
```
Finds keywords your competitors rank for that you don't. Output: `briefs/keyword-gaps-YYYY-MM-DD.md`

### Competitor analysis
```
Analyze competitor content for https://competitor.nl/page
```
Scrapes a competitor page and extracts word count, heading structure, semantic keywords. Output: `briefs/competitor-[name]-YYYY-MM-DD.md`

### Write an article
```
Write an article about zakelijk vastgoed financieren Uithoorn
```
Runs competitor analysis first, then writes a full SEO article based on `brand.md`. Output: `content/[slug].md`

### Track rankings
```
Track rankings for all keywords
```
Runs `scripts/rank_tracker.py` and compares to last week. Output: `rankings/report-YYYY-MM-DD.md`

### Find backlink opportunities
```
Find backlink opportunities
```
Runs `scripts/backlink_finder.py --site yoursite.com --niche "your niche" --limit 20`. Output: `briefs/backlinks-YYYY-MM-DD.json`

### Generate outreach email
```
Generate outreach for https://target-blog.nl/page
```
Writes a guest post article + outreach email. Output: `briefs/outreach-[domain]-YYYY-MM-DD.md`

### Local citations
```
Find citation opportunities for Amsterdam
```
Finds local directories relevant to your niche and city. Output: `briefs/citations-[city]-YYYY-MM-DD.md`

### Full audit
```
Run full SEO audit
```
Runs keyword gaps + competitor analysis + ranking report in one go.

### Full pipeline
```
Run full SEO pipeline
```
Runs everything in order: keyword gaps → 3 articles → backlinks → citations → summary report.

---

## Works with

| Tool | How |
|---|---|
| **Claude Code** | Primary use case. Type commands directly. |
| **Cursor** | Open repo in Cursor, use the chat panel. |
| **Windsurf** | Same as Cursor — open repo, use AI chat. |
| **ChatGPT (manual)** | Copy `CLAUDE.md` content into a ChatGPT conversation, then run scripts manually in your terminal. |
| **Gemini CLI** | `gemini` in terminal, same commands work. |
| **Any AI assistant** | Paste the contents of `CLAUDE.md` as a system prompt, run scripts manually. |

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
│   ├── keyword_gaps.py        # Keyword gap analysis via Brave Search
│   ├── scraper.py             # Competitor page scraper
│   ├── rank_tracker.py        # Weekly ranking tracker
│   ├── backlink_finder.py     # Finds guest post + backlink targets
│   ├── outreach_generator.py  # Writes outreach emails + guest posts
│   ├── citation_builder.py    # Finds local directory listing opportunities
│   └── requirements.txt       # Python dependencies (requests, beautifulsoup4)
├── sites/                     # Multi-site setup (one subfolder per site)
├── content/                   # Generated articles saved here
├── briefs/                    # Keyword analyses, competitor reports, backlink lists
├── rankings/                  # Weekly ranking snapshots
├── config.json                # Your domain, keywords, competitors
├── brand.md                   # Your brand voice and services
├── CLAUDE.md                  # Instructions for the AI agent
└── SETUP.md                   # Detailed setup guide
```

---

## FAQ

**1. Do I need to pay for the Brave Search API?**
The free tier gives you 2,000 queries/month. That's enough for weekly keyword tracking + a few analyses. Paid plans start at $3/1,000 queries if you need more.

**2. Does this work without Claude Code?**
Yes. You can run the Python scripts directly from the terminal and use any AI (ChatGPT, Gemini, etc.) to interpret results and write content. See "Works with" section.

**3. What Python version do I need?**
Python 3.10 or higher. Check with `python --version` or `python3 --version`.

**4. How do I track rankings for multiple sites?**
Put each site in its own subfolder under `sites/`. See SETUP.md step 8 for the full multi-site setup.

**5. Will this get my site penalized by Google?**
No. The scripts use the official Brave Search API (not scraping Google). Content is written by AI using your brand voice — Google's issue is low-quality content, not AI-generated content per se. Write for humans, not for bots.

**6. How many articles should I publish per week?**
For local niche: 2–3 per week is enough. For national keywords: 5+ per week, plus active backlink building.

**7. The script says `BRAVE_API_KEY not set`. What do I do?**
You need to set it as an environment variable before running. See Quick Start step 3. Note: this resets when you close your terminal — add it to your `.bashrc` or `.zshrc` to make it permanent.

**8. Can I use this for e-commerce sites?**
Yes, but the scripts are optimized for local service businesses and content sites. E-commerce SEO (product pages, schema, etc.) needs additional tooling.

**9. How do I see which keywords I'm ranking for right now?**
Run `Track rankings for all keywords` in Claude Code. First run creates a baseline; second run (next week) shows movement.

**10. The outreach email generator is not working well. Why?**
Set `ANTHROPIC_API_KEY` in your environment for AI-powered generation. Without it, the script falls back to a basic template.

---

## Detailed setup

See [SETUP.md](SETUP.md) for step-by-step installation, config explanation, and multi-site setup.
