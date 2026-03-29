#!/usr/bin/env python3
"""
backlink_finder.py - Vindt backlink-kansen voor een gegeven domein/niche via Brave Search.

Usage:
    python scripts/backlink_finder.py --site boomgaard-site.vercel.app --niche "zakelijk vastgoed" --limit 20
    python scripts/backlink_finder.py --site boomgaard-site.vercel.app --niche "zakelijk vastgoed" --competitors mogelijk.nl,fortus.nl --limit 30
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


BRAVE_API_KEY = os.environ.get("BRAVE_API_KEY", "")
BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"

GUEST_POST_QUERIES = [
    '"write for us" {niche}',
    '"guest post" {niche}',
    '"submit article" {niche}',
    '"guest author" {niche}',
    '"bijdrage leveren" {niche}',
    '"gastblog" {niche}',
]

DIRECTORY_QUERIES = [
    'bedrijvenregister {niche} site:.nl',
    'branchevereniging {niche}',
    'directory {niche} Nederland',
    'gids {niche} bedrijven',
]

COMPETITOR_LINK_QUERIES = [
    'link:"{competitor}" -{site}',
    'site die linkt naar {competitor}',
]


def brave_search(query: str, count: int = 10) -> list[dict]:
    """Zoek via Brave Search API, geeft lijst van resultaten terug."""
    if not BRAVE_API_KEY:
        print("[WARN] BRAVE_API_KEY niet gezet - sla API calls over", file=sys.stderr)
        return []

    params = f"?q={query.replace(' ', '+')}&count={count}&country=nl&search_lang=nl"
    req = Request(
        BRAVE_SEARCH_URL + params,
        headers={
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": BRAVE_API_KEY,
        },
    )
    try:
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("web", {}).get("results", [])
    except (URLError, HTTPError) as e:
        print(f"[ERROR] Brave Search fout voor '{query}': {e}", file=sys.stderr)
        return []


def extract_contact(url: str) -> str:
    """Probeer contactinfo te vinden op de pagina (simpele regex)."""
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=8) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", html)
        # Filter spam-achtige matches
        emails = [e for e in emails if len(e) < 60 and "." in e.split("@")[1]]
        return emails[0] if emails else ""
    except Exception:
        return ""


def estimate_dr(url: str, description: str) -> str:
    """Simpele DR-schatting op basis van domein-heuristieken."""
    domain = urlparse(url).netloc.lower()
    high_dr_signals = [
        "kvk.nl", "thuiswinkel.org", "goudengids.nl", "linkedin.com",
        "facebook.com", "rabobank.nl", "ing.nl", "rijksoverheid.nl",
        "nos.nl", "rtl.nl", "telegraaf.nl", "nu.nl",
    ]
    med_dr_signals = ["branche", "vereniging", "platform", "gids", "register"]

    if any(s in domain for s in high_dr_signals):
        return "hoog (70+)"
    if any(s in domain for s in med_dr_signals):
        return "middel (40-70)"
    if description and len(description) > 200:
        return "middel (40-70)"
    return "laag (<40)"


def find_opportunities(site: str, niche: str, competitors: list[str], limit: int) -> list[dict]:
    opportunities = []
    seen_urls = set()

    def add_opp(url: str, opp_type: str, title: str, description: str, fetch_contact: bool = False):
        domain = urlparse(url).netloc
        if domain in seen_urls or urlparse(site).netloc == domain or site in domain:
            return
        seen_urls.add(domain)
        contact = extract_contact(url) if fetch_contact else ""
        opportunities.append({
            "type": opp_type,
            "url": url,
            "domain": domain,
            "title": title,
            "description": description[:200] if description else "",
            "dr_estimate": estimate_dr(url, description),
            "contact": contact,
            "found_at": datetime.now().isoformat(),
        })

    print(f"[1/4] Zoek guest post kansen voor niche: {niche}", file=sys.stderr)
    for tmpl in GUEST_POST_QUERIES[:3]:
        query = tmpl.format(niche=niche)
        results = brave_search(query, count=5)
        for r in results:
            add_opp(r.get("url", ""), "guest_post", r.get("title", ""), r.get("description", ""), fetch_contact=True)
        time.sleep(0.5)
        if len(opportunities) >= limit:
            break

    print(f"[2/4] Zoek directories en brancheverenigingen", file=sys.stderr)
    for tmpl in DIRECTORY_QUERIES[:2]:
        query = tmpl.format(niche=niche)
        results = brave_search(query, count=5)
        for r in results:
            add_opp(r.get("url", ""), "directory", r.get("title", ""), r.get("description", ""))
        time.sleep(0.5)
        if len(opportunities) >= limit:
            break

    print(f"[3/4] Zoek competitor backlinks", file=sys.stderr)
    for comp in competitors[:3]:
        query = f'links naar "{comp}" zakelijk nederland -{site}'
        results = brave_search(query, count=5)
        for r in results:
            add_opp(r.get("url", ""), "competitor_link", r.get("title", ""), r.get("description", ""))
        time.sleep(0.5)
        if len(opportunities) >= limit:
            break

    print(f"[4/4] Zoek mention-kansen (niche + stad)", file=sys.stderr)
    mention_query = f"{niche} experts blog nederland advies"
    results = brave_search(mention_query, count=8)
    for r in results:
        add_opp(r.get("url", ""), "mention", r.get("title", ""), r.get("description", ""))
    time.sleep(0.3)

    return opportunities[:limit]


def main():
    parser = argparse.ArgumentParser(description="Vind backlink-kansen via Brave Search")
    parser.add_argument("--site", required=True, help="Jouw domein (bv. boomgaard-site.vercel.app)")
    parser.add_argument("--niche", required=True, help="Niche/branche (bv. 'zakelijk vastgoed')")
    parser.add_argument("--competitors", default="", help="Komma-gescheiden lijst van competitor-domeinen")
    parser.add_argument("--limit", type=int, default=20, help="Max aantal resultaten")
    parser.add_argument("--output", default="", help="Output JSON bestand (optioneel)")
    parser.add_argument("--config", default="config.json", help="Pad naar config.json")
    args = parser.parse_args()

    # Competitors ophalen: CLI arg of config.json
    competitors = []
    if args.competitors:
        competitors = [c.strip() for c in args.competitors.split(",") if c.strip()]
    elif os.path.exists(args.config):
        with open(args.config) as f:
            cfg = json.load(f)
        competitors = [c["domain"] for c in cfg.get("competitors", [])[:5]]

    print(f"\n🔍 Backlink Finder — {args.site}", file=sys.stderr)
    print(f"   Niche: {args.niche}", file=sys.stderr)
    print(f"   Competitors: {competitors or 'geen'}", file=sys.stderr)
    print(f"   Limit: {args.limit}\n", file=sys.stderr)

    opps = find_opportunities(args.site, args.niche, competitors, args.limit)

    result = {
        "site": args.site,
        "niche": args.niche,
        "generated_at": datetime.now().isoformat(),
        "total": len(opps),
        "opportunities": opps,
    }

    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"\n✅ Resultaten opgeslagen: {args.output}", file=sys.stderr)
    else:
        print(output_json)

    print(f"\n📊 Gevonden: {len(opps)} backlink-kansen", file=sys.stderr)
    by_type = {}
    for o in opps:
        by_type[o["type"]] = by_type.get(o["type"], 0) + 1
    for t, n in by_type.items():
        print(f"   {t}: {n}", file=sys.stderr)


if __name__ == "__main__":
    main()
