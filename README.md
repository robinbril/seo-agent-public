# SEO Agent — Tandartspraktijk Zuyderhoven

Automatisering en strategie voor lokale SEO, Google Maps/local pack en AI-zichtbaarheid van `tpzuyderhoven.nl`.

## Doel

Zuyderhoven moet structureel geïndexeerd en vindbaar worden voor:

- tandarts Amstelveen
- tandarts Aalsmeer
- tandarts Middenhoven
- tandarts nieuwe patiënten Amstelveen/Aalsmeer/Middenhoven
- gebitsreiniging Amstelveen
- Airflow gebitsreiniging Amstelveen
- implantologie Amstelveen
- wortelkanaalbehandeling Amstelveen
- tandvleesbehandeling Amstelveen
- tanden bleken Amstelveen
- spoedtandarts Amstelveen

De strategie staat in [`GOAL.md`](GOAL.md). De brand/context staat in [`brand.md`](brand.md). De dedicated locatiepagina-briefs staan in [`docs/zuyderhoven-location-pages.md`](docs/zuyderhoven-location-pages.md). De servicepagina-briefs staan in [`docs/zuyderhoven-service-pages.md`](docs/zuyderhoven-service-pages.md).

## Belangrijkste strategische keuze

Geen nieuwe bulk-blogposts meer voor dezelfde zoekintentie. De site heeft al veel blogposts die Google grotendeels niet indexeert. De volgende stap is:

1. echte locatiepagina’s bouwen;
2. echte service-money-pages bouwen;
3. duplicate/cannibaliserende blogclusters consolideren;
4. interne links en sitemap opschonen;
5. GBP, citations en reviews versterken.

## Money pages

### Locaties

- `/tandarts-amstelveen`
- `/tandarts-aalsmeer`
- `/tandarts-middenhoven`
- later: `/tandarts-uithoorn`, `/tandarts-kudelstaart`, `/tandarts-de-kwakel`

### Services

- `/behandelingen/gebitsreiniging-amstelveen`
- `/behandelingen/airflow-gebitsreiniging`
- `/behandelingen/implantologie`
- `/behandelingen/wortelkanaalbehandeling`
- `/behandelingen/kindertandheelkunde`
- `/behandelingen/spoedhulp`
- `/behandelingen/tanden-bleken`
- `/behandelingen/tandvleesbehandeling`

## Wekelijkse automatisering

GitHub Actions workflow:

```text
.github/workflows/weekly-zuyderhoven-seo.yml
```

Elke dinsdag draait de workflow:

1. `python scripts/rank_tracker.py`
2. `python scripts/keyword_gaps.py`
3. `python scripts/weekly_zuyderhoven_report.py`
4. commit nieuwe rapporten naar `rankings/`, `briefs/` en `reports/`

Nodig als GitHub secret:

```text
BRAVE_API_KEY
```

Handmatig draaien kan via GitHub → Actions → Weekly Zuyderhoven SEO → Run workflow.

## Skills

Er zijn vijf operationele SEO-skills toegevoegd onder `skills/`:

- `skills/seo-local-pack.md`
- `skills/seo-indexation.md`
- `skills/seo-money-pages.md`
- `skills/seo-geo-ai-visibility.md`
- `skills/seo-cannibalization.md`

Deze skills sturen de agent op de juiste manier: niet contentvolume, maar indexatie, money pages, lokale autoriteit en GEO/AI-citeerbaarheid.

## Scripts

- `scripts/rank_tracker.py` — wekelijkse ranking baseline en bewegingen via Brave Search.
- `scripts/keyword_gaps.py` — keywords waar concurrenten ranken en Zuyderhoven niet.
- `scripts/weekly_zuyderhoven_report.py` — vat rankings, gaps en money-page queue samen in een actiegericht rapport.

## Config

Belangrijkste configuratie staat in [`config.json`](config.json):

- prioriteitslocaties: Amstelveen, Aalsmeer, Middenhoven
- secundaire locaties: Uithoorn, Kudelstaart, De Kwakel, Legmeer, Westwijk, Bovenkerk, Aalsmeerderbrug
- competitors: Carmenlaan, Middenhoven, Aalsmeer-praktijken, Aemstelgroep, Stadshart, enz.
- target keywords: lokale tandarts-, service- en branded termen

## Regels

- Eén zoekintentie = één primaire URL.
- Geen verborgen tekst of verborgen links.
- Geen fake reviews of niet-verifieerbare review schema’s.
- Eén FAQPage-schema per URL.
- Blogposts ondersteunen money pages; ze vervangen money pages niet.
- NAP altijd exact:

```text
Tandartspraktijk Zuyderhoven
Legmeerdijk 210
1187 NK Amstelveen
020-7871336
```

## Setup

```bash
git clone https://github.com/robinbril/seo-agent-public.git
cd seo-agent-public
pip install -r scripts/requirements.txt
export BRAVE_API_KEY=your_key_here
python scripts/rank_tracker.py
python scripts/keyword_gaps.py
python scripts/weekly_zuyderhoven_report.py
```
