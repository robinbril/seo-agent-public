#!/usr/bin/env python3
"""
citation_builder.py - Vindt Nederlandse bedrijfsdirectories voor lokale SEO citations.

Usage:
    python scripts/citation_builder.py --site boomgaard --city Uithoorn
    python scripts/citation_builder.py --site revive --city Amstelveen --niche skincare
    python scripts/citation_builder.py --site boomgaard --city Uithoorn --output citations-report.md
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
from urllib.error import URLError


BRAVE_API_KEY = os.environ.get("BRAVE_API_KEY", "")
BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"

# Nederlandse directories - vaste lijst (altijd relevant)
NL_DIRECTORIES = [
    {
        "name": "KVK Bedrijvengids",
        "url": "https://www.kvk.nl/zoeken/",
        "type": "overheid",
        "dr": "hoog (90+)",
        "free": True,
        "submit_url": "https://www.kvk.nl/inschrijven/",
        "notes": "Verplicht voor NL bedrijven. Zorg dat NAP overeenkomt met handelsregister.",
    },
    {
        "name": "Gouden Gids",
        "url": "https://www.goudengids.nl",
        "type": "algemeen",
        "dr": "hoog (75+)",
        "free": True,
        "submit_url": "https://www.goudengids.nl/nl/gratis-bedrijf-toevoegen/",
        "notes": "Grootste Nederlandse bedrijvengids. Gratis basislisting.",
    },
    {
        "name": "Telefoongids.nl",
        "url": "https://www.telefoongids.nl",
        "type": "algemeen",
        "dr": "hoog (72+)",
        "free": True,
        "submit_url": "https://www.telefoongids.nl/bedrijf-aanmelden/",
        "notes": "Klassieke telefoongids, goed voor local SEO.",
    },
    {
        "name": "Cylex Nederland",
        "url": "https://www.cylex.nl",
        "type": "algemeen",
        "dr": "middel (55+)",
        "free": True,
        "submit_url": "https://www.cylex.nl/bedrijf-aanmelden.html",
        "notes": "Europese bedrijvengids met NL sectie.",
    },
    {
        "name": "Detelefoongids.nl",
        "url": "https://www.detelefoongids.nl",
        "type": "algemeen",
        "dr": "middel (60+)",
        "free": True,
        "submit_url": "https://www.detelefoongids.nl/bedrijf-aanmelden/",
        "notes": "Gratis listing mogelijk.",
    },
    {
        "name": "Bedrijfspagina.nl",
        "url": "https://www.bedrijfspagina.nl",
        "type": "algemeen",
        "dr": "middel (50+)",
        "free": True,
        "submit_url": "https://www.bedrijfspagina.nl/bedrijf-aanmelden",
        "notes": "Gratis bedrijfspagina aanmaken.",
    },
    {
        "name": "Startpagina.nl (branche)",
        "url": "https://www.startpagina.nl",
        "type": "branche",
        "dr": "hoog (78+)",
        "free": False,
        "submit_url": "https://www.startpagina.nl/contact/",
        "notes": "Links via redactie aanvragen. Zoek relevante branche-pagina.",
    },
    {
        "name": "Google Business Profile",
        "url": "https://business.google.com",
        "type": "essentieel",
        "dr": "hoog (100)",
        "free": True,
        "submit_url": "https://business.google.com/create",
        "notes": "PRIORITEIT 1. Vereist voor lokale zoekresultaten. NAP exact matchen.",
    },
    {
        "name": "Bing Places",
        "url": "https://www.bingplaces.com",
        "type": "essentieel",
        "dr": "hoog (90+)",
        "free": True,
        "submit_url": "https://www.bingplaces.com/",
        "notes": "Bing equivalent van Google Business. Eenvoudig in te stellen.",
    },
    {
        "name": "Yelp Nederland",
        "url": "https://www.yelp.nl",
        "type": "reviews",
        "dr": "hoog (94+)",
        "free": True,
        "submit_url": "https://biz.yelp.nl/",
        "notes": "Reviews platform, ook goed voor citations.",
    },
    {
        "name": "Foursquare",
        "url": "https://foursquare.com",
        "type": "locatie",
        "dr": "hoog (90+)",
        "free": True,
        "submit_url": "https://foursquare.com/add-place",
        "notes": "Data wordt gebruikt door Apple Maps en andere services.",
    },
    {
        "name": "Nextdoor",
        "url": "https://nextdoor.nl",
        "type": "lokaal",
        "dr": "hoog (80+)",
        "free": True,
        "submit_url": "https://nextdoor.nl/voor-bedrijven/",
        "notes": "Lokaal sociaal netwerk. Goed voor buurtgerichte bedrijven.",
    },
    {
        "name": "LinkedIn Company Page",
        "url": "https://linkedin.com",
        "type": "professioneel",
        "dr": "hoog (99+)",
        "free": True,
        "submit_url": "https://www.linkedin.com/company/setup/new/",
        "notes": "Bedrijfspagina aanmaken met website URL en adres.",
    },
    {
        "name": "Facebook Business",
        "url": "https://business.facebook.com",
        "type": "sociaal",
        "dr": "hoog (99+)",
        "free": True,
        "submit_url": "https://www.facebook.com/pages/create",
        "notes": "Bedrijfspagina met NAP informatie.",
    },
    {
        "name": "Trustpilot Nederland",
        "url": "https://nl.trustpilot.com",
        "type": "reviews",
        "dr": "hoog (92+)",
        "free": True,
        "submit_url": "https://nl.trustpilot.com/evaluate/",
        "notes": "Review platform, vraag klanten om reviews na registratie.",
    },
]

NICHE_DIRECTORIES = {
    "vastgoed": [
        {
            "name": "Vastgoedpro.nl",
            "url": "https://vastgoedpro.nl",
            "type": "branche",
            "dr": "middel (55+)",
            "free": False,
            "submit_url": "https://vastgoedpro.nl/contact",
            "notes": "Vakblad vastgoed, link aanvragen via redactie.",
        },
        {
            "name": "VastgoedMarkt",
            "url": "https://vastgoedmarkt.nl",
            "type": "branche",
            "dr": "hoog (65+)",
            "free": False,
            "submit_url": "https://vastgoedmarkt.nl/adverteren",
            "notes": "Vakblad vastgoed professionals.",
        },
        {
            "name": "NVB Hypotheken",
            "url": "https://www.nvb.nl",
            "type": "branchevereniging",
            "dr": "hoog (70+)",
            "free": False,
            "submit_url": "https://www.nvb.nl/leden/",
            "notes": "Nederlandse Vereniging van Banken - lidmaatschap vereist.",
        },
    ],
    "skincare": [
        {
            "name": "Beautyplatform.nl",
            "url": "https://beautyplatform.nl",
            "type": "branche",
            "dr": "middel (45+)",
            "free": True,
            "submit_url": "https://beautyplatform.nl/contact",
            "notes": "Beauty en skincare platform NL.",
        },
    ],
    "auto": [
        {
            "name": "AutoTrack",
            "url": "https://www.autotrack.nl",
            "type": "branche",
            "dr": "hoog (75+)",
            "free": False,
            "submit_url": "https://www.autotrack.nl/dealers/",
            "notes": "Dealer listing, betaald.",
        },
        {
            "name": "Marktplaats Auto",
            "url": "https://www.marktplaats.nl/auto",
            "type": "marktplaats",
            "dr": "hoog (90+)",
            "free": False,
            "submit_url": "https://www.marktplaats.nl/zakelijk/",
            "notes": "Zakelijk profiel aanmaken.",
        },
    ],
}


def brave_search_directories(niche: str, city: str) -> list[dict]:
    """Zoek niche-specifieke directories via Brave."""
    if not BRAVE_API_KEY:
        return []

    results = []
    queries = [
        f"bedrijvengids {niche} {city} site:.nl",
        f"branchevereniging {niche} Nederland aanmelden",
        f"directory {niche} bedrijven Nederland gratis",
    ]

    for query in queries[:2]:
        try:
            params = f"?q={query.replace(' ', '+')}&count=5&country=nl"
            req = Request(
                BRAVE_SEARCH_URL + params,
                headers={
                    "Accept": "application/json",
                    "X-Subscription-Token": BRAVE_API_KEY,
                },
            )
            with urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for r in data.get("web", {}).get("results", []):
                    url = r.get("url", "")
                    domain = urlparse(url).netloc
                    if domain and not any(d["url"] in url for d in NL_DIRECTORIES):
                        results.append({
                            "name": r.get("title", domain),
                            "url": url,
                            "type": "niche_search",
                            "dr": "onbekend",
                            "free": None,
                            "submit_url": url,
                            "notes": r.get("description", "")[:150],
                        })
        except Exception as e:
            print(f"[WARN] Search fout: {e}", file=sys.stderr)

    return results[:5]


def load_nap_from_config(site: str) -> dict:
    """Laad NAP data uit config.json."""
    base = Path(__file__).parent.parent
    candidates = [base / "sites" / site / "config.json", base / "config.json"]
    for p in candidates:
        if p.exists():
            cfg = json.loads(p.read_text(encoding="utf-8"))
            return {
                "naam": cfg.get("brand_name", cfg.get("site_name", "")),
                "website": cfg.get("domain", ""),
                "niche": cfg.get("niche", ""),
                "stad": "",
            }
    return {}


def generate_nap_data(site: str, city: str, config_nap: dict) -> dict:
    """Genereer consistente NAP data template."""
    return {
        "naam": config_nap.get("naam", f"[Bedrijfsnaam - vul in]"),
        "adres": f"[Straat + Huisnummer], {city}",
        "postcode": "[Postcode]",
        "stad": city,
        "provincie": "[Provincie]",
        "land": "Nederland",
        "telefoon": "[+31 XX XXX XXXX]",
        "email": f"[info@{config_nap.get('website', 'jouwebsite.nl')}]",
        "website": f"https://{config_nap.get('website', 'jouwebsite.nl')}",
        "kvk": "[KVK-nummer]",
        "openingstijden": {
            "maandag-vrijdag": "09:00-17:30",
            "zaterdag": "Gesloten",
            "zondag": "Gesloten",
        },
        "beschrijving": f"[Korte bedrijfsbeschrijving - max 150 woorden. Gebruik '{config_nap.get('niche', 'branche')}' als keyword.]",
        "categorieen": [config_nap.get("niche", "[Branche]"), city, "Nederland"],
    }


def generate_report(site: str, city: str, niche: str, directories: list, nap: dict) -> str:
    lines = []
    lines.append(f"# Citation Building Report: {site}")
    lines.append(f"Gegenereerd: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Stad: {city} | Niche: {niche}\n")

    lines.append("---\n## 📋 NAP Data (gebruik OVERAL exact dezelfde info)\n")
    lines.append("```json")
    lines.append(json.dumps(nap, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("\n⚠️ **Belangrijk:** NAP moet 100% consistent zijn op alle directories.")
    lines.append("Schrijf naam, adres en telefoonnummer altijd exact hetzelfde.\n")

    # Sorteer: essentieel eerst
    priority_order = {"essentieel": 0, "branchevereniging": 1, "overheid": 2, "reviews": 3, "algemeen": 4, "sociaal": 5, "branche": 6, "locatie": 7, "lokaal": 8, "marktplaats": 9, "niche_search": 10, "professioneel": 5}
    dirs_sorted = sorted(directories, key=lambda d: priority_order.get(d.get("type", ""), 99))

    lines.append("---\n## 📍 Directories\n")
    lines.append(f"Totaal gevonden: **{len(dirs_sorted)}** directories\n")

    essential = [d for d in dirs_sorted if d.get("type") == "essentieel"]
    if essential:
        lines.append("### 🔴 Prioriteit 1 - Start hier\n")
        for d in essential:
            free_str = "✅ Gratis" if d.get("free") else "💰 Betaald"
            lines.append(f"#### {d['name']}")
            lines.append(f"- **URL:** {d['url']}")
            lines.append(f"- **Aanmelden:** {d['submit_url']}")
            lines.append(f"- **DR:** {d['dr']} | {free_str}")
            lines.append(f"- **Note:** {d['notes']}\n")

    other = [d for d in dirs_sorted if d.get("type") != "essentieel"]
    if other:
        lines.append("### 🟡 Prioriteit 2 - Directories\n")
        for d in other:
            free_str = "✅ Gratis" if d.get("free") else ("💰 Betaald" if d.get("free") is False else "❓ Onbekend")
            lines.append(f"#### {d['name']}")
            lines.append(f"- **URL:** {d['url']}")
            lines.append(f"- **Aanmelden:** {d['submit_url']}")
            lines.append(f"- **DR:** {d['dr']} | {free_str}")
            if d.get("notes"):
                lines.append(f"- **Note:** {d['notes']}")
            lines.append("")

    lines.append("---\n## ✅ Actieplan\n")
    lines.append("1. **Vul NAP data in** - doe dit eerst, gebruik exact dezelfde info overal")
    lines.append("2. **Google Business Profile** - dit is prioriteit 1, direct impact op local pack")
    lines.append("3. **KVK Bedrijvengids** - zorg dat handelsregister up-to-date is")
    lines.append("4. **Gouden Gids + Telefoongids** - gratis, hoge DR, doe dit in week 1")
    lines.append("5. **Review platforms** (Yelp, Trustpilot) - vraag bestaande klanten om reviews")
    lines.append("6. **Branche-specifieke directories** - na basis gedaan")
    lines.append("7. **Track** in spreadsheet: directory, datum aangemeld, status, live URL")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Vind Nederlandse citation-kansen voor lokale SEO")
    parser.add_argument("--site", required=True, help="Site naam of directory")
    parser.add_argument("--city", required=True, help="Stad (bv. Uithoorn)")
    parser.add_argument("--niche", default="", help="Niche override (anders uit config)")
    parser.add_argument("--output", default="", help="Output bestand pad (anders stdout)")
    args = parser.parse_args()

    print(f"\n📍 Citation Builder — {args.site} | {args.city}", file=sys.stderr)

    config_nap = load_nap_from_config(args.site)
    niche = args.niche or config_nap.get("niche", "algemeen")

    print(f"   Niche: {niche}", file=sys.stderr)

    # Basis directories
    directories = list(NL_DIRECTORIES)

    # Niche-specifieke directories
    for key, dirs in NICHE_DIRECTORIES.items():
        if key.lower() in niche.lower():
            directories.extend(dirs)
            print(f"   + {len(dirs)} {key}-specifieke directories", file=sys.stderr)

    # Dynamisch zoeken via Brave
    if BRAVE_API_KEY:
        print("   🔍 Zoek extra directories via Brave...", file=sys.stderr)
        extra = brave_search_directories(niche, args.city)
        directories.extend(extra)
        print(f"   + {len(extra)} extra via zoekresultaten", file=sys.stderr)

    nap = generate_nap_data(args.site, args.city, config_nap)
    report = generate_report(args.site, args.city, niche, directories, nap)

    print(f"\n✅ {len(directories)} directories gevonden", file=sys.stderr)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"   Opgeslagen: {args.output}", file=sys.stderr)
    else:
        # Sla ook op in site briefs
        base = Path(__file__).parent.parent
        candidates = [base / "sites" / args.site / "briefs", base / "briefs"]
        for briefs_dir in candidates:
            if briefs_dir.parent.exists():
                briefs_dir.mkdir(parents=True, exist_ok=True)
                filename = f"citations-{args.city.lower()}-{datetime.now().strftime('%Y-%m-%d')}.md"
                out_path = briefs_dir / filename
                out_path.write_text(report, encoding="utf-8")
                print(f"   Opgeslagen: {out_path}", file=sys.stderr)
                break
        print(report)


if __name__ == "__main__":
    main()
