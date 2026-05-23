# SEO Agent - Claude/Codex Setup

This is a public SEO automation template. Do not put client-specific strategy, customer data, private analytics, API keys, credentials, Search Console exports, Wix account data, or proprietary SEO plans in this repository.

## Required setup

- `BRAVE_API_KEY` in environment for search/ranking scripts.
- Python 3.10+.
- `config.json` and `brand.md` filled in inside a private/local copy.

## Workflow

1. Read `config.json`.
2. Read `brand.md`.
3. Run keyword/ranking scripts.
4. Write reports to `briefs/` and `rankings/`.
5. Keep private client output out of public repos.

## Commands

### Keyword gap analysis

```bash
python scripts/keyword_gaps.py
```

### Rank tracking

```bash
python scripts/rank_tracker.py
```

### Backlink opportunities

```bash
python scripts/backlink_finder.py --site example.com --niche "local service" --limit 20
```

### Citation opportunities

```bash
python scripts/citation_builder.py --site example.com --city Amsterdam
```

## Rules

- One search intent = one primary URL.
- No hidden text or hidden links.
- No fake reviews.
- No keyword stuffing.
- Public repo stays generic. Real client strategy belongs in a private repo or local automation prompt.
