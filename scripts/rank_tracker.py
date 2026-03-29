#!/usr/bin/env python3
"""
Weekly Rank Tracker - tracks keyword positions via Brave Search.
Compares with previous week and generates change report.
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

def brave_search(query: str, api_key: str, count: int = 20) -> list[dict]:
    params = urllib.parse.urlencode({"q": query, "count": count})
    url = f"https://api.search.brave.com/res/v1/web/search?{params}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "X-Subscription-Token": api_key,
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("web", {}).get("results", [])
    except Exception as e:
        print(f"  Error: {e}")
        return []

def get_position(domain: str, results: list) -> int | None:
    for i, r in enumerate(results, 1):
        if domain.lower() in r.get("url", "").lower():
            return i
    return None

def load_previous(rankings_dir: Path) -> dict:
    """Load most recent previous rankings JSON."""
    files = sorted(rankings_dir.glob("rankings-*.json"), reverse=True)
    if len(files) < 2:
        return {}
    with open(files[1]) as f:
        return json.load(f)

def main():
    api_key = os.environ.get("BRAVE_API_KEY")
    if not api_key:
        print("ERROR: BRAVE_API_KEY not set")
        sys.exit(1)
    
    config = load_config()
    domain = config["domain"]
    keywords = config.get("target_keywords", [])
    rankings_dir = BASE_DIR / config.get("rankings_dir", "rankings")
    rankings_dir.mkdir(exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"\n📈 Rank Tracker - {date_str}")
    print(f"Domain: {domain} | Keywords: {len(keywords)}")
    print("=" * 60)
    
    current = {}
    for kw in keywords:
        print(f"  Checking: '{kw}'")
        results = brave_search(kw, api_key, count=20)
        pos = get_position(domain, results)
        current[kw] = pos
        if pos:
            print(f"    #{pos}")
        else:
            print(f"    Not in top 20")
        time.sleep(0.5)
    
    # Save current rankings
    json_file = rankings_dir / f"rankings-{date_str}.json"
    with open(json_file, "w") as f:
        json.dump({"date": date_str, "domain": domain, "rankings": current}, f, indent=2)
    
    # Load previous
    previous = load_previous(rankings_dir)
    prev_rankings = previous.get("rankings", {})
    
    # Generate report
    improved, declined, new_rankings, unchanged = [], [], [], []
    for kw, pos in current.items():
        prev = prev_rankings.get(kw)
        if pos is None and prev is None:
            continue
        elif prev is None and pos is not None:
            new_rankings.append((kw, pos))
        elif pos is None and prev is not None:
            declined.append((kw, prev, None))
        elif pos < prev:
            improved.append((kw, prev, pos))
        elif pos > prev:
            declined.append((kw, prev, pos))
        else:
            unchanged.append((kw, pos))
    
    report_file = rankings_dir / f"report-{date_str}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"# Ranking Report - {date_str}\n\n")
        f.write(f"**Domain:** {domain} | **Keywords tracked:** {len(keywords)}\n\n")
        
        if improved:
            f.write("## 📈 Improved\n\n")
            for kw, prev, curr in sorted(improved, key=lambda x: x[1]-x[2], reverse=True):
                f.write(f"- **{kw}**: #{prev} → **#{curr}** (+{prev-curr})\n")
            f.write("\n")
        
        if new_rankings:
            f.write("## 🆕 New Rankings\n\n")
            for kw, pos in sorted(new_rankings, key=lambda x: x[1]):
                f.write(f"- **{kw}**: #{pos} (new!)\n")
            f.write("\n")
        
        if declined:
            f.write("## 📉 Declined\n\n")
            for kw, prev, curr in sorted(declined, key=lambda x: (x[2] or 99)-x[1], reverse=True):
                curr_str = f"#{curr}" if curr else "not ranking"
                f.write(f"- **{kw}**: #{prev} → {curr_str}\n")
            f.write("\n")
        
        if unchanged:
            f.write("## ➡️ Unchanged\n\n")
            for kw, pos in sorted(unchanged, key=lambda x: x[1]):
                f.write(f"- {kw}: #{pos}\n")
            f.write("\n")
        
        ranked = [(kw, pos) for kw, pos in current.items() if pos]
        if ranked:
            f.write("## 🏆 All Current Rankings\n\n")
            for kw, pos in sorted(ranked, key=lambda x: x[1]):
                f.write(f"- **#{pos}** — {kw}\n")
    
    print(f"\n{'='*60}")
    print(f"📊 {len(improved)} improved, {len(declined)} declined, {len(new_rankings)} new")
    print(f"📄 Report: {report_file}")

if __name__ == "__main__":
    main()
