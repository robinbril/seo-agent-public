#!/usr/bin/env python3
"""
Competitor Content Scraper - haalt content op en analyseert structure.
Usage: python scripts/scraper.py --url https://competitor.com/article
"""
import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from datetime import datetime
from html.parser import HTMLParser

BASE_DIR = Path(__file__).parent.parent

class ContentExtractor(HTMLParser):
    """Simple HTML parser to extract text content and structure."""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.headings = []
        self.current_tag = ""
        self.in_body = False
        self.skip_tags = {"script", "style", "nav", "footer", "header"}
        self.heading_tags = {"h1", "h2", "h3", "h4"}
        self.current_heading = []
        self.in_heading = False
        self.current_text = []
        self.in_skip = False
        self.skip_depth = 0
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag in self.skip_tags:
            self.in_skip = True
            self.skip_depth += 1
        if tag in self.heading_tags:
            self.in_heading = True
            self.current_heading = [tag]
            
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip_depth -= 1
            if self.skip_depth == 0:
                self.in_skip = False
        if tag in self.heading_tags and self.in_heading:
            text = " ".join(self.current_heading[1:]).strip()
            if text:
                self.headings.append({"tag": self.current_heading[0], "text": text})
            self.in_heading = False
            self.current_heading = []
            
    def handle_data(self, data):
        if self.in_skip:
            return
        data = data.strip()
        if not data:
            return
        if self.in_heading:
            self.current_heading.append(data)
        else:
            self.text_parts.append(data)
    
    def get_text(self):
        return " ".join(self.text_parts)
    
    def get_word_count(self):
        return len(self.get_text().split())


def fetch_url(url: str) -> str:
    """Fetch URL content."""
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read()
        encoding = resp.headers.get_content_charset() or "utf-8"
        return content.decode(encoding, errors="replace")


def extract_meta(html: str) -> dict:
    """Extract title and meta description."""
    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', html, re.IGNORECASE)
    return {
        "title": title_match.group(1).strip() if title_match else "",
        "meta_description": desc_match.group(1).strip() if desc_match else "",
    }


def analyze(url: str) -> dict:
    print(f"Fetching: {url}")
    html = fetch_url(url)
    
    meta = extract_meta(html)
    parser = ContentExtractor()
    parser.feed(html)
    
    word_count = parser.get_word_count()
    headings = parser.headings
    
    # Count heading types
    h2s = [h["text"] for h in headings if h["tag"] == "h2"]
    h3s = [h["text"] for h in headings if h["tag"] == "h3"]
    
    # Extract keywords from headings (simple frequency)
    all_heading_text = " ".join(h["text"].lower() for h in headings)
    words = re.findall(r'\b[a-z]{4,}\b', all_heading_text)
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    top_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:15]
    
    return {
        "url": url,
        "title": meta["title"],
        "meta_description": meta["meta_description"],
        "word_count": word_count,
        "heading_count": len(headings),
        "h1": next((h["text"] for h in headings if h["tag"] == "h1"), ""),
        "h2s": h2s,
        "h3s": h3s[:10],
        "top_keywords": top_keywords,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    
    data = analyze(args.url)
    
    # Output dir
    briefs_dir = BASE_DIR / "briefs"
    briefs_dir.mkdir(exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    domain = re.sub(r'https?://(www\.)?', '', args.url).split('/')[0]
    output_file = briefs_dir / f"competitor-{domain}-{date_str}.md"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# Competitor Analysis: {data['title']}\n\n")
        f.write(f"**URL:** {data['url']}\n")
        f.write(f"**Word count:** {data['word_count']}\n")
        f.write(f"**Meta:** {data['meta_description']}\n\n")
        
        f.write(f"## Content Structure\n\n")
        if data['h1']:
            f.write(f"**H1:** {data['h1']}\n\n")
        
        if data['h2s']:
            f.write(f"**H2 sections ({len(data['h2s'])}):**\n")
            for h in data['h2s']:
                f.write(f"- {h}\n")
            f.write("\n")
        
        if data['h3s']:
            f.write(f"**H3 subsections (sample):**\n")
            for h in data['h3s']:
                f.write(f"- {h}\n")
            f.write("\n")
        
        f.write(f"## Top Keywords in Headings\n\n")
        for kw, count in data['top_keywords']:
            f.write(f"- **{kw}** ({count}x)\n")
    
    print(f"\n✅ Analysis complete")
    print(f"   Word count: {data['word_count']}")
    print(f"   H2 sections: {len(data['h2s'])}")
    print(f"   Report: {output_file}")
    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
