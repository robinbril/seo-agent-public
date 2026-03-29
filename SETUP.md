# SEO Agent Setup Guide

AI-powered SEO automation met Claude Code. Werkt voor elke website, niche, en taal.

---

## Wat doet dit?

- **Keyword research** - vindt gaps ten opzichte van concurrenten
- **Content genereren** - SEO-geoptimaliseerde artikelen op basis van jouw brand voice
- **Ranking tracking** - houdt bij hoe jouw keywords scoren in Google
- **Backlink finder** - vindt relevante sites om links van te krijgen
- **Outreach generator** - schrijft gastblog-artikelen en outreach emails
- **Citation builder** - vindt Nederlandse directories voor lokale SEO

---

## Stap 1 — Vereisten

### Python 3.9+
```bash
python --version
# Als niet geïnstalleerd: https://python.org/downloads
```

### Brave Search API key (verplicht)
1. Ga naar https://api.search.brave.com/
2. Maak een gratis account aan
3. Kopieer je API key

### Anthropic API key (optioneel, voor AI-outreach)
1. Ga naar https://console.anthropic.com/
2. Maak een account aan en genereer een API key
3. Nodig voor `outreach_generator.py` met AI-gegenereerde content

### Claude Code (optioneel, voor /seo commands)
```bash
npm install -g @anthropic-ai/claude-code
```

---

## Stap 2 — Installatie

```bash
# Clone de repo
git clone https://github.com/robinbril/seo-agent-public.git
cd seo-agent-public

# Installeer dependencies (optioneel, stdlib werkt ook)
pip install -r scripts/requirements.txt
```

---

## Stap 3 — API Keys configureren

### Windows
```powershell
$env:BRAVE_API_KEY = "jouw_brave_api_key_hier"
$env:ANTHROPIC_API_KEY = "jouw_claude_key_hier"  # optioneel
```

### macOS/Linux
```bash
export BRAVE_API_KEY="jouw_brave_api_key_hier"
export ANTHROPIC_API_KEY="jouw_claude_key_hier"  # optioneel
```

### Permanent (aanbevolen)
Voeg bovenstaande toe aan je `~/.bashrc`, `~/.zshrc`, of Windows Environment Variables.

---

## Stap 4 — Configureer je site

### 4a. Bewerk `config.json`
```json
{
  "site_name": "Jouw Bedrijfsnaam",
  "domain": "jouwebsite.nl",
  "niche": "jouw branche",
  "target_keywords": ["keyword 1", "keyword 2 stad"],
  "target_location": "Jouw Stad",
  "competitors": [
    {"domain": "concurrent1.nl", "type": "nationaal", "strength": "hoog"}
  ]
}
```

### 4b. Vul `brand.md` in
Open `brand.md` en beantwoord alle vragen. Dit is het fundament van alle gegenereerde content.

---

## Stap 5 — Test de scripts

### Keyword gaps
```bash
python scripts/keyword_gaps.py
```

### Backlink kansen vinden
```bash
python scripts/backlink_finder.py --site jouwebsite.nl --niche "jouw niche" --limit 10
```

### Lokale citations
```bash
python scripts/citation_builder.py --site jouwebsite --city "Jouw Stad"
```

### Outreach genereren
```bash
python scripts/outreach_generator.py --site jouwebsite --target-url https://branche-blog.nl --type guest-post
```

---

## Stap 6 — Claude Code gebruiken (aanbevolen)

Met Claude Code kun je commando's in gewone taal geven:

```bash
claude
```

Dan in de chat:
```
Run keyword gap analysis
Write an article about [onderwerp]
Find backlink opportunities
Generate outreach for https://target-site.nl
Find citation opportunities for [stad]
```

Claude leest automatisch `config.json` en `brand.md` en voert de juiste scripts uit.

---

## Meerdere sites

Maak per site een submap aan:
```
sites/
  site-a/
    config.json
    brand.md
    content/
    briefs/
  site-b/
    config.json
    brand.md
```

Geef de sitenaam mee bij commando's:
```bash
python scripts/backlink_finder.py --site site-a --niche "niche A" --config sites/site-a/config.json
```

Of via Claude Code: `Find backlinks for site-a`

---

## Output bestanden

| Script | Output locatie |
|--------|---------------|
| `keyword_gaps.py` | `briefs/keyword-gaps-DATUM.md` |
| `rank_tracker.py` | `rankings/report-DATUM.md` |
| `backlink_finder.py` | stdout JSON of `--output` bestand |
| `citation_builder.py` | `briefs/citations-STAD-DATUM.md` |
| `outreach_generator.py` | `briefs/outreach-DOMEIN-DATUM.md` |
| Content genereren | `content/[slug].md` |

---

## Veelgestelde vragen

**Q: Werkt dit ook voor Engelstalige sites?**
A: Ja. Pas `config.json` aan (`"language": "en", "serp_location": "us"`) en vertel Claude Code dat je in het Engels wilt schrijven.

**Q: Heb ik alle API keys nodig?**
A: Alleen `BRAVE_API_KEY` is verplicht. `ANTHROPIC_API_KEY` is optioneel - outreach_generator werkt dan met templates.

**Q: Hoe vaak moet ik rankings tracken?**
A: Wekelijks is aanbevolen. Stel een cron job in of run elke maandag `python scripts/rank_tracker.py`.

**Q: Mijn site is niet in het Nederlands. Wat dan?**
A: De scripts werken taalAgnostisch. Claude Code genereert content in de taal die je opgeeft in `brand.md` en je prompts.

---

## Support

Issues en feature requests: https://github.com/robinbril/seo-agent-public/issues
