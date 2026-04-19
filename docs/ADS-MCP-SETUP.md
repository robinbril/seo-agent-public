# Ads MCP Setup — Meta Ads + Google Ads

Deze guide zet Claude Code op zodat het zelf campagnes kan aanmaken, pauzeren,
bijsturen en rapporteren op Meta Ads en Google Ads — per klant geïsoleerd.

**Stack:**
- **Meta Ads** → [`brijr/meta-mcp`](https://github.com/brijr/meta-mcp) (MIT, 25 tools met
  volledige write-surface). Gepubliceerd op npm als `meta-ads-mcp`.
- **Google Ads** → [`itallstartedwithaidea/google-ads-mcp`](https://github.com/itallstartedwithaidea/google-ads-mcp)
  (MIT, 29 tools inclusief `create_campaign`, `update_campaign_budget`,
  `add_keywords`, `generic_mutate`).

> **Waarom deze en niet de populairste?** `cohnen/mcp-google-ads` en
> `gomarble-ai/*` zijn read-only GAQL wrappers — ze laten Claude wel data
> lezen maar geen campagnes bewerken. Zie `docs/ADS-MCP-SETUP.md` §"Afgewezen
> repos" onderaan voor de volledige lijst.

---

## 0 · Prerequisites

Op jouw lokale machine (waar je Claude Code CLI draait):

| Tool | Installatie |
|---|---|
| Node.js 18+ (voor `npx`) | [nodejs.org](https://nodejs.org) of `brew install node` |
| `uv` / `uvx` (voor de Google Ads server) | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Claude Code CLI | `npm install -g @anthropic-ai/claude-code` |

Verify: `claude --version`, `node --version`, `uvx --version`.

---

## 1 · Haal je credentials op

### 1a · Meta developer app (éénmalig, gedeeld voor alle klanten)

1. Ga naar https://developers.facebook.com/apps/ → **Create App** → type
   **Business** → app naam bv. `robin-ads-agent`.
2. In de app: **Add Product** → **Marketing API**.
3. **App Settings → Basic** → kopieer `App ID` en `App Secret`. Vul in
   `.env` onder `META_APP_ID` / `META_APP_SECRET`.

> App Review is niet nodig zolang je eigen system-user tokens gebruikt
> binnen je eigen Business Manager.

### 1b · Meta system-user token per klant (TP Zuyderhoven)

Dit is een token dat **niet verloopt** en gebonden is aan een specifieke
Business Manager.

1. Login met jouw Meta Business account dat toegang heeft tot de klant-BM.
2. https://business.facebook.com/settings/ → selecteer de Business Manager
   die eigenaar is van de klant-ad-account.
3. **Business Settings → Users → System Users** → **Add** →
   naam `claude-code-agent` → Role **Admin**.
4. **Assign Assets** → voeg toe: de **Ad Account** + de **Facebook Page** van
   de praktijk → permission **Manage**.
5. **Generate New Token** → selecteer jouw Meta app (`robin-ads-agent`) →
   permissions aanvinken: `ads_management`, `ads_read`, `business_management`,
   `pages_read_engagement`, `pages_manage_ads` → **Generate**.
6. Kopieer het token → `.env` onder `TPZ_META_ACCESS_TOKEN=…`.

### 1c · Google Cloud / Google Ads credentials

Jij hebt een Google account met MCC (My Client Center) toegang tot de
klant-ad-accounts. We maken daar een OAuth app bij zodat Claude namens die
account kan inloggen.

1. **Google Cloud Console** → https://console.cloud.google.com → nieuw
   project `robin-ads-agent` → **APIs & Services** → **Enable APIs** →
   zoek "Google Ads API" → **Enable**.
2. **Credentials → Create Credentials → OAuth client ID** →
   Application type **Desktop app** → naam `claude-ads` → Create.
3. Download de JSON → kopieer `client_id` en `client_secret` naar `.env`
   onder `GOOGLE_ADS_CLIENT_ID` / `GOOGLE_ADS_CLIENT_SECRET`.
4. **OAuth consent screen** → User type **External** → fill in app name +
   support email → **Save**. Tijdens Testing mode moet je je eigen mail
   toevoegen onder **Test users**.

### 1d · Google Ads developer token

1. Login op https://ads.google.com met je MCC-account.
2. Switch naar de **MCC** (top-right account switcher).
3. **Tools & Settings → Setup → API Center** → vraag een developer token aan
   (start = **Test access**; je kunt Basic/Standard later aanvragen — dat
   duurt 1–3 weken).
4. Kopieer het token → `.env` onder `GOOGLE_ADS_DEVELOPER_TOKEN`.

> Met **Test access** werkt het tegen test-accounts. Voor live campagnes op
> TP Zuyderhoven heb je Basic of Standard nodig. Vraag Basic aan zodra je
> wilt gaan live testen.

### 1e · Google Ads refresh token

Dit is de stap waar mensen vastlopen. We draaien een kort Python-scriptje dat
een OAuth flow start, het token ophaalt en uitprint.

```bash
# in de root van dit repo
python3 -m venv .venv && source .venv/bin/activate
pip install google-ads google-auth-oauthlib
python3 scripts/google_ads_get_refresh_token.py
```

Het script (zie `scripts/google_ads_get_refresh_token.py`) opent je browser,
laat je inloggen met je MCC-account, en print het refresh token.
Kopieer → `.env` onder `GOOGLE_ADS_REFRESH_TOKEN`.

### 1f · Per-klant customer ID

1. Login op https://ads.google.com.
2. Switch naar het klant-account (TP Zuyderhoven) onder de MCC.
3. Top-right → lees het account nummer, bv. `123-456-7890`.
4. Verwijder de dashes → `1234567890` → `.env` onder
   `TPZ_GOOGLE_ADS_CUSTOMER_ID`.

---

## 2 · Vul `.env` in

```bash
cp .env.example .env
# open .env en vul alle velden in
```

Check dat `.env` écht in `.gitignore` staat (`git status` mag `.env` niet
tonen).

---

## 3 · Claude Code laten lezen van `.mcp.json`

Het repo bevat al `.mcp.json` met 2 server-entries (meta-ads-tpzuyderhoven +
google-ads-tpzuyderhoven). Claude Code pakt die automatisch op wanneer je de
CLI in deze directory opent. De eerste keer vraagt 'ie om goedkeuring
(project-scoped servers zijn default disabled):

```bash
cd /pad/naar/seo-agent-public
claude
# binnen de session:
/mcp
```

Je ziet beide servers met status. Klik `y` of gebruik `/mcp enable`. Je
env-vars moeten ofwel in `.env` staan (Claude Code leest die automatisch in
project scope) ofwel geëxporteerd zijn in je shell.

### Alternatief: user-scoped via CLI

Wil je de servers niet per-project maar user-wide:

```bash
# Meta Ads
claude mcp add --scope user \
  --env META_ACCESS_TOKEN=$TPZ_META_ACCESS_TOKEN \
  --env META_APP_ID=$META_APP_ID \
  --env META_APP_SECRET=$META_APP_SECRET \
  meta-ads-tpzuyderhoven -- npx -y meta-ads-mcp

# Google Ads
claude mcp add --scope user \
  --env GOOGLE_ADS_DEVELOPER_TOKEN=$GOOGLE_ADS_DEVELOPER_TOKEN \
  --env GOOGLE_ADS_CLIENT_ID=$GOOGLE_ADS_CLIENT_ID \
  --env GOOGLE_ADS_CLIENT_SECRET=$GOOGLE_ADS_CLIENT_SECRET \
  --env GOOGLE_ADS_REFRESH_TOKEN=$GOOGLE_ADS_REFRESH_TOKEN \
  --env GOOGLE_ADS_LOGIN_CUSTOMER_ID=$TPZ_GOOGLE_ADS_CUSTOMER_ID \
  google-ads-tpzuyderhoven -- uvx --from git+https://github.com/itallstartedwithaidea/google-ads-mcp gads-mcp
```

---

## 4 · Smoke tests

In een Claude Code sessie:

- **Meta:** "Gebruik `meta-ads-tpzuyderhoven` — lijst alle actieve campagnes
  in ad account `act_<jouw_ad_account_id>` met insights over de laatste 7
  dagen."
- **Google:** "Gebruik `google-ads-tpzuyderhoven` — run `list_accounts` en
  daarna `get_campaign_performance` over de laatste 30 dagen."

Werkt dat? Dan zit je goed.

---

## 5 · Een extra klant toevoegen

Patroon per nieuwe klant — vervang `<client>` door een korte ID (bv. `acme`):

1. Voeg in `.env` toe:
   ```
   <CLIENT>_META_ACCESS_TOKEN=…       # system-user token in de BM van de klant
   <CLIENT>_GOOGLE_ADS_CUSTOMER_ID=…  # klant-account onder jouw MCC
   ```
2. Voeg in `.mcp.json` toe:
   ```json
   "meta-ads-<client>": {
     "command": "npx",
     "args": ["-y", "meta-ads-mcp"],
     "env": {
       "META_ACCESS_TOKEN": "${<CLIENT>_META_ACCESS_TOKEN}",
       "META_APP_ID": "${META_APP_ID}",
       "META_APP_SECRET": "${META_APP_SECRET}"
     }
   },
   "google-ads-<client>": {
     "command": "uvx",
     "args": ["--from", "git+https://github.com/itallstartedwithaidea/google-ads-mcp", "gads-mcp"],
     "env": {
       "GOOGLE_ADS_DEVELOPER_TOKEN": "${GOOGLE_ADS_DEVELOPER_TOKEN}",
       "GOOGLE_ADS_CLIENT_ID": "${GOOGLE_ADS_CLIENT_ID}",
       "GOOGLE_ADS_CLIENT_SECRET": "${GOOGLE_ADS_CLIENT_SECRET}",
       "GOOGLE_ADS_REFRESH_TOKEN": "${GOOGLE_ADS_REFRESH_TOKEN}",
       "GOOGLE_ADS_LOGIN_CUSTOMER_ID": "${<CLIENT>_GOOGLE_ADS_CUSTOMER_ID}"
     }
   }
   ```

App / OAuth credentials zijn gedeeld; alleen de per-klant token +
customer_id verschillen.

---

## 6 · Veiligheid

- `.env` is in `.gitignore`. Commit nooit tokens.
- Rouleer Meta system-user tokens per klant wanneer je de samenwerking met
  een klant beëindigt → BM → System Users → [user] → **Revoke token**.
- Rouleer het Google refresh token door de OAuth client in Google Cloud te
  regenereren — raakt alle klanten tegelijk, dus alleen doen bij
  verdenking lek.
- De `brijr/meta-mcp` server respecteert `appsecret_proof` wanneer je
  `META_APP_SECRET` meegeeft — houd die altijd ingevuld voor productie.

---

## 7 · Afgewezen repos (voor referentie)

| Repo | Reden |
|---|---|
| `cohnen/mcp-google-ads` | Read-only (5 GAQL tools, geen mutations) |
| `gomarble-ai/google-ads-mcp-server` | Read-only (3 tools), funnel naar hosted product |
| `googleads/google-ads-mcp` | Officieel Google, "strictly read-only" |
| `gomarble-ai/facebook-ads-mcp-server` | Read-only, geen write tools |
| `HagaiHen/facebook-mcp-server` | Beheert Pages, geen Ads |
| `attainmentlabs/meta-ads-mcp` | Te beperkt (5 tools) |
| `pipeboard-co/meta-ads-mcp` | BUSL license (niet OSI-open-source), duwt naar hosted tier — bruikbaar als 2e keus als je self-hosted custom Meta app gebruikt |

---

## 8 · Troubleshooting

- `Connection closed` op Windows-native shell: wrap `npx` als `cmd /c npx -y meta-ads-mcp`.
- `uvx: command not found`: `curl -LsSf https://astral.sh/uv/install.sh | sh && source $HOME/.local/bin/env`.
- Meta token invalid: check dat `ads_management` permission is aangevinkt bij
  token generatie én dat het system user role Admin is (niet Employee).
- Google Ads "CUSTOMER_NOT_ENABLED": vraag Basic/Standard access aan voor je
  developer token, Test access werkt niet op echte klant-accounts.
- `/mcp` toont server als "failed": draai `claude mcp get meta-ads-tpzuyderhoven`
  voor stderr.
