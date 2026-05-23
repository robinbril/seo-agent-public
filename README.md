# SEO Agent - AI-powered SEO automation for Claude Code

Public SEO automation template for keyword research, ranking tracking, competitor checks, backlink discovery and citation planning.

## Privacy note

Do not commit client-specific strategy, customer data, private analytics, API keys, credentials, Google Search Console exports, Wix account data, or proprietary SEO plans to this public repository.

For real client work, clone this repository into a private repo or local folder and keep secrets in local environment variables, a local `.env` file excluded by `.gitignore`, or a trusted secret manager.

## What this does

- Finds keyword gaps via Brave Search.
- Tracks rankings weekly.
- Generates reports into `briefs/` and `rankings/`.
- Supports local citation and backlink opportunity research.

## Setup

```bash
git clone https://github.com/robinbril/seo-agent-public.git
cd seo-agent-public
pip install -r scripts/requirements.txt
export BRAVE_API_KEY=your_key_here
python scripts/rank_tracker.py
python scripts/keyword_gaps.py
```

## Config

Copy the template values in `config.json` and `brand.md` into a private project before adding real client information.

## Commands

```bash
python scripts/rank_tracker.py
python scripts/keyword_gaps.py
python scripts/backlink_finder.py --site example.com --niche "local service" --limit 20
python scripts/citation_builder.py --site example.com --city Amsterdam
```
