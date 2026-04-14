#!/usr/bin/env python3
"""
Serper-based Rank Tracker — werkt als alternatief voor rank_tracker.py
Gebruikt SERPER_API_KEY ipv BRAVE_API_KEY.
Ondersteunt multi-site via --site argument.
"""
import json
import os
import sys
import time
import urllib.request
import argparse
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent

def load_config(site=None):
    if site:
        cfg = BASE_DIR / "sites" / site / "config.json"
    else:
        cfg = BASE_DIR / "config.json"
    with open(cfg) as f:
        return json.load(f)

def site_dir(site=None):
    if site:
        return BASE_DIR / "sites" / site
    return BASE_DIR

def serper_search(query: str, api_key: str, count: int = 20) -> dict:
    body = json.dumps({"q": query, "gl": "nl", "hl": "nl", "num": count}).encode()
    req = urllib.request.Request(
        "https://google.serper.dev/search",
        data=body,
        headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  Error: {e}")
        return {}

def get_position(domain: str, data: dict):
    """Returns (position, snippet_url) — checks organic + localResults."""
    for i, r in enumerate(data.get("organic", []), 1):
        if domain.lower() in r.get("link", "").lower():
            return i, r.get("link", "")
    for i, r in enumerate(data.get("localResults", []), 1):
        if domain.lower() in r.get("website", "").lower():
            return f"local#{i}", r.get("website", "")
    return None, None

def get_competitors_in_results(competitors: list, data: dict) -> list:
    hits = []
    for comp in competitors:
        for i, r in enumerate(data.get("organic", []), 1):
            if comp.lower() in r.get("link", "").lower():
                hits.append((comp, i, r.get("link", "")))
                break
    return hits

def load_previous(rankings_dir: Path) -> dict:
    files = sorted(rankings_dir.glob("rankings-*.json"), reverse=True)
    if len(files) < 2:
        return {}
    with open(files[1]) as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", help="Site subfolder (e.g. tpzuyderhoven)")
    args = parser.parse_args()

    api_key = os.environ.get("SERPER_API_KEY")
    if not api_key:
        print("ERROR: SERPER_API_KEY not set")
        sys.exit(1)

    config = load_config(args.site)
    domain = config["domain"]
    keywords = config.get("target_keywords", [])
    competitors = config.get("competitors", [])
    base = site_dir(args.site)
    rankings_dir = base / config.get("rankings_dir", "rankings")
    rankings_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"\n📈 Rank Tracker (Serper) — {date_str}")
    print(f"Domain: {domain} | Keywords: {len(keywords)}")
    print("=" * 65)

    current = {}
    gap_details = []

    for kw in keywords:
        print(f"\n  🔍 '{kw}'")
        data = serper_search(kw, api_key, count=20)
        pos, url = get_position(domain, data)
        current[kw] = pos
        comp_hits = get_competitors_in_results(competitors, data)

        if pos:
            print(f"    ✅ #{pos} — {url}")
        else:
            print(f"    ❌ Niet gevonden in top 20")
            if comp_hits:
                for c, p, u in comp_hits:
                    print(f"    ⚔️  {c} staat op #{p}")
            gap_details.append({
                "keyword": kw,
                "competitor_rankings": [(c, p) for c, p, _ in comp_hits],
                "top_organic": [
                    {"pos": i+1, "title": r.get("title",""), "link": r.get("link","")}
                    for i, r in enumerate(data.get("organic", [])[:5])
                ],
                "local_pack": [r.get("title","") for r in data.get("localResults", [])[:3]],
                "paa": [q.get("question","") for q in data.get("peopleAlsoAsk", [])[:4]],
            })
        time.sleep(0.6)

    # Save JSON snapshot
    json_file = rankings_dir / f"rankings-{date_str}.json"
    with open(json_file, "w") as f:
        json.dump({"date": date_str, "domain": domain, "rankings": current}, f, indent=2, ensure_ascii=False)

    # Load previous for diff
    previous = load_previous(rankings_dir)
    prev_rankings = previous.get("rankings", {})

    improved, declined, new_entries, unchanged = [], [], [], []
    for kw, pos in current.items():
        prev = prev_rankings.get(kw)
        pos_num = int(str(pos).replace("local#","")) if pos else None
        prev_num = int(str(prev).replace("local#","")) if prev else None

        if pos is None and prev is None:
            continue
        elif prev is None and pos is not None:
            new_entries.append((kw, pos))
        elif pos is None and prev is not None:
            declined.append((kw, prev, None))
        elif pos_num and prev_num and pos_num < prev_num:
            improved.append((kw, prev, pos))
        elif pos_num and prev_num and pos_num > prev_num:
            declined.append((kw, prev, pos))
        else:
            unchanged.append((kw, pos))

    # Write markdown report
    report_file = rankings_dir / f"report-{date_str}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"# Ranking Report — {date_str}\n\n")
        f.write(f"**Domain:** {domain} | **Keywords:** {len(keywords)} | **Gaps:** {len(gap_details)}\n\n")

        ranked = [(kw, pos) for kw, pos in current.items() if pos]
        not_ranked = [(kw,) for kw, pos in current.items() if not pos]

        f.write("## 🏆 Huidige Rankings\n\n")
        if ranked:
            for kw, pos in sorted(ranked, key=lambda x: str(x[1])):
                f.write(f"- **#{pos}** — {kw}\n")
        else:
            f.write("- Nog geen rankings gevonden.\n")
        f.write("\n")

        f.write("## 🎯 Gaps — Niet in top 20\n\n")
        for gap in gap_details:
            f.write(f"### {gap['keyword']}\n")
            if gap["competitor_rankings"]:
                for c, p in gap["competitor_rankings"]:
                    f.write(f"- Concurrent: **{c}** staat op #{p}\n")
            if gap["local_pack"]:
                f.write(f"- Local pack: {', '.join(gap['local_pack'])}\n")
            if gap["paa"]:
                f.write(f"- PAA vragen: {' | '.join(gap['paa'])}\n")
            if gap["top_organic"]:
                f.write(f"- Top resultaat: [{gap['top_organic'][0]['title']}]({gap['top_organic'][0]['link']})\n")
            f.write("\n")

        if improved:
            f.write("## 📈 Verbeterd (vs vorige week)\n\n")
            for kw, prev, curr in improved:
                f.write(f"- **{kw}**: #{prev} → **#{curr}**\n")
            f.write("\n")

        if declined:
            f.write("## 📉 Gedaald (vs vorige week)\n\n")
            for kw, prev, curr in declined:
                curr_str = f"#{curr}" if curr else "niet meer in top 20"
                f.write(f"- **{kw}**: #{prev} → {curr_str}\n")
            f.write("\n")

    print(f"\n{'='*65}")
    print(f"✅ Rankings: {len(ranked)} | Gaps: {len(gap_details)} | Verbeterd: {len(improved)}")
    print(f"📄 Report: {report_file}")
    print(f"💾 JSON:   {json_file}")

if __name__ == "__main__":
    main()
