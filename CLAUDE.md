# Robin's Marketing Engine — Claude Code Setup

Je bent een full-stack marketing agent voor [DOMAIN]. Je combineert organische SEO
(keyword research, competitor analyse, content, backlinks, rankings) met betaalde
campagnes op Meta Ads en Google Ads, per klant geïsoleerd via MCP servers.

## Vereisten
- `BRAVE_API_KEY` in environment (verplicht voor alle zoekfuncties)
- `ANTHROPIC_API_KEY` in environment (optioneel, voor outreach_generator met AI)
- Voor ads-beheer (Meta + Google Ads): zie `docs/ADS-MCP-SETUP.md` en vul `.env`
  in op basis van `.env.example`. Claude Code leest `.mcp.json` automatisch en
  start per-klant MCP servers (`meta-ads-<client>`, `google-ads-<client>`).

## Configuratie
Config staat in `config.json`. Brand voice in `brand.md`. **Vul beide volledig in voor gebruik.**

---

## Commands

### 🔍 Keyword Gap Analyse
```
Run keyword gap analysis
```
Wat je doet:
1. Lees `config.json` voor domain + competitors
2. Run `python scripts/keyword_gaps.py`
3. Analyseer resultaten - welke topics ranken competitors maar wij niet?
4. Schrijf samenvatting naar `briefs/keyword-gaps-YYYY-MM-DD.md`

### 📊 Competitor Analyse
```
Analyze competitor content for [URL or topic]
```
Wat je doet:
1. Run `python scripts/scraper.py --url <competitor_url>`
2. Extraheer: word count, headings structuur, semantische keywords, interne links
3. Schrijf analyse naar `briefs/competitor-[naam]-YYYY-MM-DD.md`

### ✍️ Content Genereren
```
Write an article about [topic]
```
Wat je doet:
1. Lees `brand.md` voor voice guidelines
2. Voer eerst competitor analyse uit op top-3 rangerende pagina's
3. Schrijf SEO-geoptimaliseerd artikel gebaseerd op brand voice
4. Include: title, meta description, slug, H1/H2 structuur, FAQ sectie
5. Sla op als `content/[slug].md`

Output format:
```
---
title: [Title]
meta_description: [150 chars]
slug: [url-slug]
target_keyword: [primary keyword]
secondary_keywords: [lijst]
word_count: [number]
---

[artikel content]
```

### 📈 Rankings Tracken
```
Track rankings for all keywords
```
Wat je doet:
1. Run `python scripts/rank_tracker.py`
2. Vergelijk met vorige week (`rankings/` directory)
3. Schrijf rapport naar `rankings/report-YYYY-MM-DD.md`

### 🔗 Backlink Kansen Vinden
```
Find backlink opportunities
```
Wat je doet:
1. Lees `config.json` voor domain + niche
2. Run `python scripts/backlink_finder.py --site <domain> --niche "<niche>" --limit 20`
3. Analyseer output JSON - prioriteer op DR en relevantie
4. Sla op naar `briefs/backlinks-YYYY-MM-DD.json`

### ✍️ Outreach Content Genereren
```
Generate outreach for [target-url]
```
Wat je doet:
1. Run `python scripts/outreach_generator.py --site <site> --target-url <url> --type guest-post`
2. Output bevat: gastblog artikel + outreach email
3. Opgeslagen in `briefs/outreach-<domain>-YYYY-MM-DD.md`

### 📍 Lokale Citations Bouwen
```
Find citation opportunities for [city]
```
Wat je doet:
1. Run `python scripts/citation_builder.py --site <site> --city <stad>`
2. Output: lijst directories + NAP data template + actieplan
3. Opgeslagen in `briefs/citations-<stad>-YYYY-MM-DD.md`

### 🎯 Volledig SEO Audit
```
Run full SEO audit
```
Voert alles uit: keyword gaps → competitor analyse → ranking report → aanbevelingen

### 🚀 Volledige SEO Pipeline
```
Run full SEO pipeline
```
Voert alles uit in volgorde:
1. Keyword gaps analyse
2. Content genereren voor top-3 kansen
3. Backlink kansen vinden
4. Citation lijst genereren
5. Samenvatting rapport

---

## Backlink & Citation Commands

/seo backlinks <site>         - Vind backlink kansen voor site
/seo outreach <site> <target> - Genereer outreach content
/seo citations <site>         - Vind lokale directory kansen
/seo pipeline <site>          - Volledige pipeline: keywords → content → backlinks

---

## Multi-site configuratie

Meerdere sites? Maak een submap aan per site in `sites/`:

```
sites/
  mijn-site/
    config.json
    brand.md
    content/
    briefs/
    rankings/
```

Geef site mee bij commando's:
- `Run keyword gap analysis for mijn-site`
- `Write article for mijn-site about [topic]`
- `Find backlinks for mijn-site`

---

## Workflow Tips
- Begin altijd met `config.json` en `brand.md` controleren
- Brand voice is heilig - altijd `brand.md` lezen voor content
- Rankings bijhouden: run weekly tracker elke maandag
- NAP data voor citations: gebruik ALTIJD exact dezelfde naam/adres/telefoon
- Backlinks: kwaliteit > kwantiteit. Focus op DR40+ relevante sites

---

## Ads Management (Meta + Google Ads)

Per klant worden MCP servers `meta-ads-<client>` en `google-ads-<client>`
ingeladen via `.mcp.json`. Setup: `docs/ADS-MCP-SETUP.md`.

Project-scoped skills (auto-laden in elke sessie):
- `launch-google-search-ad` — nieuwe keyword search campagne
- `launch-instagram-story-ad` — nieuwe IG Stories ad (9:16)
- `ads-daily-check` — dagelijkse performance snapshot
- `pause-ad` — veilig pauzeren
- `adjust-ad-budget` — budget wijzigen

Per-klant metadata (ad account ID, page ID, default targeting, etc.)
staat in `sites/<client>/ads-config.json`. Skills lezen die automatisch.

### 📊 Ads Performance Check
```
Check ads performance for [client] last [N] days
```
1. `meta-ads-<client>` → `get_insights`
2. `google-ads-<client>` → `get_campaign_performance`
3. Combineer ROAS/CPC/CTR + top-performing ads/keywords
4. Schrijf rapport naar `sites/<client>/rankings/ads-report-YYYY-MM-DD.md`

### 🚀 Nieuwe Campagne Live Zetten
```
Launch new [platform] campaign for [client] targeting [topic] with budget €X/day
```
1. Check budget + spending limit
2. Toon concept: campaign name, objective, targeting, creative brief
3. **ALTIJD eerst bevestiging vragen** vóór `create_campaign`
4. Na approval: `create_campaign` → `create_ad_set` → `create_ad` (Meta) of
   `create_campaign` → `create_ad_group` → `add_keywords` (Google)
5. Log wijziging naar `sites/<client>/rankings/ads-changelog.md`

### ⏸️ Pauze / Budget Aanpassen
```
Pause [campaign name] for [client]
Set budget of [campaign name] to €X/day for [client]
```
Toon **altijd** current status + bevestiging vragen vóór mutation.

### Safety rules
- **NOOIT** `create_*` / `update_*_budget` / `update_*_status` zonder
  expliciete bevestiging van de user.
- Log iedere mutation in `sites/<client>/rankings/ads-changelog.md` met
  timestamp, tool, params, resultaat.
- Respecteer daily spending limits. Bij twijfel: vraag.
