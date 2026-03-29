# SEO Agent — AI SEO Automation with Claude Code

> Generic template for AI-powered SEO automation. Works for any website, niche, or language.

## What's included

| Script | What it does |
|--------|-------------|
| `scripts/keyword_gaps.py` | Finds keyword gaps vs competitors via Brave Search |
| `scripts/scraper.py` | Scrapes competitor pages for content analysis |
| `scripts/rank_tracker.py` | Tracks keyword rankings over time |
| `scripts/backlink_finder.py` | Finds backlink opportunities (guest posts, directories, mentions) |
| `scripts/outreach_generator.py` | Generates guest post articles + outreach emails |
| `scripts/citation_builder.py` | Finds local directory citation opportunities |

## Quick Start

```bash
git clone https://github.com/robinbril/seo-agent-public.git
cd seo-agent-public

# Set API keys
export BRAVE_API_KEY="your_key"
export ANTHROPIC_API_KEY="your_key"  # optional

# Configure your site
# Edit config.json and brand.md

# Run
python scripts/backlink_finder.py --site yoursite.com --niche "your niche" --limit 20
python scripts/citation_builder.py --site yoursite --city "Your City"
```

See [SETUP.md](SETUP.md) for full instructions.

## Requirements

- Python 3.9+
- Brave Search API key (free tier available at https://api.search.brave.com/)
- Anthropic API key (optional, for AI-powered outreach)
- Claude Code (optional, for natural language commands)

## Usage with Claude Code

```bash
claude
```

Then chat naturally:
```
Run keyword gap analysis
Write an article about [topic]
Find backlink opportunities
Generate outreach for https://target-site.nl
Find citation opportunities for [city]
```

## License

MIT
