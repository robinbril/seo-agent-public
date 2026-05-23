#!/usr/bin/env python3
"""
Weekly Zuyderhoven SEO report orchestrator.

This script does not replace Search Console or Wix MCP. It turns the weekly
rank/gap output into an action-oriented report for the Zuyderhoven strategy.
"""
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CONFIG_FILE = BASE_DIR / "config.json"
GOAL_FILE = BASE_DIR / "GOAL.md"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def latest_file(directory: Path, pattern: str) -> Path | None:
    files = sorted(directory.glob(pattern), reverse=True)
    return files[0] if files else None


def main() -> None:
    config = load_json(CONFIG_FILE)
    rankings_dir = BASE_DIR / config.get("rankings_dir", "rankings")
    briefs_dir = BASE_DIR / config.get("briefs_output_dir", "briefs")
    reports_dir = BASE_DIR / "reports"
    reports_dir.mkdir(exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    latest_rankings = latest_file(rankings_dir, "rankings-*.json")
    latest_rank_report = latest_file(rankings_dir, "report-*.md")
    latest_gap_report = latest_file(briefs_dir, "keyword-gaps-*.md")

    ranked = []
    not_ranked = []
    if latest_rankings:
        data = load_json(latest_rankings)
        for keyword, position in data.get("rankings", {}).items():
            if position:
                ranked.append((keyword, position))
            else:
                not_ranked.append(keyword)

    target_keywords = config.get("target_keywords", [])
    money_pages = config.get("money_pages", {})

    report = []
    report.append(f"# Weekly Zuyderhoven SEO Report — {today}\n")
    report.append("## Goal\n")
    report.append("Indexatie en ranking verbeteren voor Tandartspraktijk Zuyderhoven rond Amstelveen, Aalsmeer en Middenhoven.\n")
    report.append("## Current tracking scope\n")
    report.append(f"- Keywords tracked: {len(target_keywords)}")
    report.append(f"- Location money pages planned: {len(money_pages.get('locations', []))}")
    report.append(f"- Service money pages planned: {len(money_pages.get('services', []))}\n")

    report.append("## Ranking summary\n")
    report.append(f"- Ranked in top 20: {len(ranked)}")
    report.append(f"- Not in top 20: {len(not_ranked)}\n")
    if ranked:
        report.append("### Current visible keywords")
        for keyword, position in sorted(ranked, key=lambda item: item[1]):
            report.append(f"- #{position}: {keyword}")
        report.append("")

    report.append("## Money page build queue\n")
    report.append("### Location pages")
    for page in money_pages.get("locations", []):
        report.append(f"- {page}")
    report.append("\n### Service pages")
    for page in money_pages.get("services", []):
        report.append(f"- {page}")
    report.append("")

    report.append("## This week’s operating checks\n")
    report.append("1. Check if /tandarts-amstelveen, /tandarts-aalsmeer and /tandarts-middenhoven exist as real Wix pages, not only blogposts.")
    report.append("2. Check Search Console/Wix inspection for these pages after publishing.")
    report.append("3. Ensure /behandelingen has exactly one FAQPage schema.")
    report.append("4. Ensure homepage/footer link to the three location pages and core services.")
    report.append("5. Do not publish duplicate blogposts for the same intent.\n")

    report.append("## Source files\n")
    if GOAL_FILE.exists():
        report.append("- GOAL.md")
    if latest_rank_report:
        report.append(f"- {latest_rank_report.relative_to(BASE_DIR)}")
    if latest_gap_report:
        report.append(f"- {latest_gap_report.relative_to(BASE_DIR)}")
    report.append("")

    output = reports_dir / f"weekly-zuyderhoven-seo-{today}.md"
    output.write_text("\n".join(report), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
