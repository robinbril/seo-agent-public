#!/usr/bin/env python3
"""
Keyword Gap Finder - gebruikt Brave Search API om te vinden
welke topics competitors ranken maar ons domein niet.
"""
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime

import urllib.request
import urllib.parse

BASE_DIR = Path(__file__).parent.parent
CONFIG_FILE = BASE_DIR / "config.json"

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def brave_search(query: str, api_key: str, count: int = 10) -> list[dict]:
    """Search via Brave API, return list of results."""
    params = urllib.parse.urlencode({
        "q": query,
        "count": count,
        "country": "NL",
        "search_lang": "nl",
    })
    url = f"https://api.search.brave.com/res/v1/web/search?{params}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key,
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("web", {}).get("results", [])
    except Exception as e:
        print(f"  Search error: {e}")
        return []

def check_domain_ranks(domain: str, keyword: str, results: list[dict]) -> int | None:
    """Return position (1-based) if domain ranks, else None."""
    for i, r in enumerate(results, 1):
        if domain.lower() in r.get("url", "").lower():
            return i
    return None

def main():
    api_key = os.environ.get("BRAVE_API_KEY")
    if not api_key:
        print("ERROR: BRAVE_API_KEY not set in environment")
        sys.exit(1)

    config = load_config()
    domain = config["domain"]
    competitors = config["competitors"]
    keywords = config.get("target_keywords", [])

    print(f"\n🔍 Keyword Gap Analysis")
    print(f"Domain: {domain}")
    print(f"Competitors: {', '.join(competitors)}")
    print(f"Keywords to check: {len(keywords)}")
    print("=" * 60)

    gaps = []
    our_rankings = []
    
    for kw in keywords:
        print(f"\n  Checking: '{kw}'")
        results = brave_search(kw, api_key, count=10)
        time.sleep(0.5)  # rate limit
        
        our_pos = check_domain_ranks(domain, kw, results)
        
        competitor_hits = []
        for comp in competitors:
            pos = check_domain_ranks(comp, kw, results)
            if pos:
                competitor_hits.append((comp, pos))
        
        if our_pos:
            print(f"    ✅ We rank #{our_pos}")
            our_rankings.append({"keyword": kw, "position": our_pos})
        else:
            print(f"    ❌ We don't rank")
            if competitor_hits:
                comps_str = ", ".join(f"{c} (#{p})" for c, p in competitor_hits)
                print(f"    Competitors ranking: {comps_str}")
                gaps.append({
                    "keyword": kw,
                    "competitor_rankings": competitor_hits,
                    "top_results": [r.get("title", "") + " - " + r.get("url", "") for r in results[:3]]
                })

    # Write report
    output_dir = BASE_DIR / config.get("briefs_output_dir", "briefs")
    output_dir.mkdir(exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file = output_dir / f"keyword-gaps-{date_str}.md"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# Keyword Gap Report - {date_str}\n\n")
        f.write(f"**Domain:** {domain}\n")
        f.write(f"**Keywords analyzed:** {len(keywords)}\n")
        f.write(f"**Gaps found:** {len(gaps)}\n")
        f.write(f"**Already ranking:** {len(our_rankings)}\n\n")
        
        f.write("## 🎯 Keyword Gaps (Opportunity)\n\n")
        if gaps:
            for g in sorted(gaps, key=lambda x: len(x["competitor_rankings"]), reverse=True):
                f.write(f"### {g['keyword']}\n")
                for comp, pos in g["competitor_rankings"]:
                    f.write(f"- {comp} ranks **#{pos}**\n")
                f.write(f"\nTop results:\n")
                for r in g["top_results"]:
                    f.write(f"- {r}\n")
                f.write("\n")
        else:
            f.write("No gaps found for target keywords.\n\n")
        
        f.write("## ✅ Current Rankings\n\n")
        for r in sorted(our_rankings, key=lambda x: x["position"]):
            f.write(f"- **#{r['position']}** — {r['keyword']}\n")
    
    print(f"\n{'='*60}")
    print(f"📊 Results: {len(gaps)} gaps found, {len(our_rankings)} current rankings")
    print(f"📄 Report saved to: {output_file}")
    return gaps

if __name__ == "__main__":
    main()
