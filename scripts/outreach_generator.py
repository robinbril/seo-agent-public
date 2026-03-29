#!/usr/bin/env python3
"""
outreach_generator.py - Genereert outreach content voor link building via Claude API.

Usage:
    python scripts/outreach_generator.py --site boomgaard --target-url https://vastgoedpro.nl --type guest-post
    python scripts/outreach_generator.py --site boomgaard --target-url https://blog.nl --type link-request
    python scripts/outreach_generator.py --site revive --target-url https://skincare.nl --type guest-post
"""

import argparse
import json
import os
import sys
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


CLAUDE_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
BRAVE_API_KEY = os.environ.get("BRAVE_API_KEY", "")
BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"


def find_site_root(site: str) -> Path:
    """Zoek de root directory van een site (sites/<naam>/ of huidige dir)."""
    base = Path(__file__).parent.parent
    candidates = [
        base / "sites" / site,
        base / "sites" / site.lower().replace(" ", "-"),
        base,
    ]
    for p in candidates:
        if (p / "brand.md").exists() or (p / "config.json").exists():
            return p
    return base


def load_brand(site: str) -> str:
    root = find_site_root(site)
    brand_path = root / "brand.md"
    if brand_path.exists():
        return brand_path.read_text(encoding="utf-8")
    return "Brand informatie niet beschikbaar."


def load_config(site: str) -> dict:
    root = find_site_root(site)
    config_path = root / "config.json"
    if config_path.exists():
        return json.loads(config_path.read_text(encoding="utf-8"))
    return {}


def fetch_target_info(url: str) -> str:
    """Haal basale info op van de target site."""
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=8) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        # Haal title + eerste 500 chars tekst op
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else ""
        # Strip HTML tags
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text).strip()[:800]
        return f"Titel: {title}\nContent preview: {text}"
    except Exception as e:
        return f"Kon target site niet ophalen: {e}"


def call_claude(prompt: str, max_tokens: int = 2000) -> str:
    """Stuur een prompt naar Claude API."""
    if not CLAUDE_API_KEY:
        # Fallback: genereer template zonder AI
        return "[CLAUDE_API_KEY niet gezet - gebruik template hieronder]\n\n" + generate_fallback(prompt)

    body = json.dumps({
        "model": "claude-3-5-haiku-20241022",
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = Request(
        CLAUDE_API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["content"][0]["text"]
    except (URLError, HTTPError) as e:
        return f"[API fout: {e}]"


def generate_fallback(prompt: str) -> str:
    """Simpele template als geen API key beschikbaar."""
    return """
## Template (vul zelf in)

**Onderwerp:** [Gastblog voorstel] - [Jouw naam/bedrijf] x [Target site]

Hallo [naam],

Ik ben [naam] van [bedrijf]. Ik volg [target site] al een tijdje en waardeer jullie content over [onderwerp].

Ik wil een gastbijdrage schrijven over [topic], specifiek gericht op [doelgroep van target site].

Voorgestelde titel: [Titel hier]

Het artikel behandelt:
- [Punt 1]
- [Punt 2]
- [Punt 3]

Ik heb eerder geschreven voor [referentie]. Zou dit interessant zijn?

Met vriendelijke groet,
[Naam]
[Bedrijf]
[Website]
"""


def generate_guest_post_article(brand: str, config: dict, target_url: str, target_info: str) -> str:
    target_domain = urlparse(target_url).netloc
    niche = config.get("niche", "de branche")
    brand_name = config.get("brand_name", config.get("site_name", "ons bedrijf"))
    domain = config.get("domain", "")

    prompt = f"""Je bent een SEO content schrijver die een gastblog-artikel schrijft namens {brand_name}.

## Brand informatie:
{brand[:1500]}

## Target website:
URL: {target_url}
Domein: {target_domain}
{target_info[:500]}

## Instructies:
Schrijf een professioneel gastblog-artikel van ~800 woorden in het Nederlands voor publicatie op {target_domain}.

Het artikel moet:
- Aansluiten bij de niche: {niche}
- Waardevolle informatie bieden voor lezers van {target_domain}
- Subtiel {brand_name} positioneren als expert (niet te commercieel)
- Een natuurlijke backlink bevatten naar {domain}
- SEO-geoptimaliseerd zijn met relevante keywords
- Een sterke intro, 3-4 secties met H2-headings, en CTA aan het einde

Format output als Markdown met frontmatter:
---
title: [artikel titel]
meta_description: [150 chars]
target_site: {target_domain}
backlink_anchor: [anchor tekst voor backlink]
---

[artikel hier]
"""
    return call_claude(prompt, max_tokens=2500)


def generate_outreach_email(brand: str, config: dict, target_url: str, target_info: str, content_type: str) -> str:
    target_domain = urlparse(target_url).netloc
    brand_name = config.get("brand_name", config.get("site_name", "ons bedrijf"))
    domain = config.get("domain", "")

    type_descriptions = {
        "guest-post": "gastblog artikel",
        "link-request": "vermelding/link naar onze site",
        "resource-page": "toevoeging aan jullie resource/links pagina",
        "broken-link": "vervanging van een gebroken link",
    }
    type_desc = type_descriptions.get(content_type, content_type)

    prompt = f"""Schrijf een persoonlijke, professionele outreach email in het Nederlands voor link building.

## Van:
Bedrijf: {brand_name}
Website: {domain}
Brand context: {brand[:800]}

## Naar:
Website: {target_url}
Domein: {target_domain}
Context: {target_info[:300]}

## Doel: {type_desc}

Schrijf een outreach email die:
- Persoonlijk aanvoelt (noem iets specifieks over hun site)
- Kort en to-the-point is (max 150 woorden body)
- Duidelijk communiceert wat we aanbieden
- Een concrete call-to-action heeft
- Professioneel maar niet formeel is

Format:
**Onderwerp:** [onderwerp hier]

[email body]

**Naam:** [contactpersoon naam van {brand_name}]
**Bedrijf:** {brand_name}
**Email:** [email@{domain}]
"""
    return call_claude(prompt, max_tokens=600)


def main():
    parser = argparse.ArgumentParser(description="Genereer outreach content voor link building")
    parser.add_argument("--site", required=True, help="Site naam of 'boomgaard', 'revive', etc.")
    parser.add_argument("--target-url", required=True, help="URL van de target site")
    parser.add_argument(
        "--type",
        choices=["guest-post", "link-request", "resource-page", "broken-link"],
        default="guest-post",
        help="Type outreach",
    )
    parser.add_argument("--output-dir", default="", help="Output directory (optioneel)")
    args = parser.parse_args()

    print(f"\n✍️  Outreach Generator — {args.site} → {args.target_url}", file=sys.stderr)
    print(f"   Type: {args.type}\n", file=sys.stderr)

    brand = load_brand(args.site)
    config = load_config(args.site)

    if not config:
        print(f"[WARN] Geen config.json gevonden voor site '{args.site}'", file=sys.stderr)

    print("📡 Target site info ophalen...", file=sys.stderr)
    target_info = fetch_target_info(args.target_url)

    output_parts = []
    output_parts.append(f"# Outreach Package: {args.site} → {urlparse(args.target_url).netloc}")
    output_parts.append(f"Gegenereerd: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    output_parts.append(f"Type: {args.type}\n")

    if args.type == "guest-post":
        print("📝 Gastblog artikel genereren...", file=sys.stderr)
        article = generate_guest_post_article(brand, config, args.target_url, target_info)
        output_parts.append("---\n## Gastblog Artikel\n")
        output_parts.append(article)

    print("📧 Outreach email genereren...", file=sys.stderr)
    email = generate_outreach_email(brand, config, args.target_url, target_info, args.type)
    output_parts.append("\n---\n## Outreach Email\n")
    output_parts.append(email)

    result = "\n".join(output_parts)

    # Output bepalen
    if args.output_dir:
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        site_root = find_site_root(args.site)
        out_dir = site_root / "briefs"
        out_dir.mkdir(parents=True, exist_ok=True)

    target_slug = urlparse(args.target_url).netloc.replace(".", "-")
    filename = f"outreach-{target_slug}-{datetime.now().strftime('%Y-%m-%d')}.md"
    out_path = out_dir / filename
    out_path.write_text(result, encoding="utf-8")

    print(f"\n✅ Outreach content opgeslagen: {out_path}", file=sys.stderr)
    print(result)


if __name__ == "__main__":
    main()
