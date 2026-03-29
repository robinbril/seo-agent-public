# Setup Guide

Everything you need to go from zero to running your first SEO analysis.

---

## Step 1 — Install Python

You need Python 3.10 or higher.

**Check if you already have it:**
```bash
python --version
# or
python3 --version
```

If you see `Python 3.10.x` or higher, skip to Step 2.

**Install Python:**
- Download from [python.org/downloads](https://www.python.org/downloads/)
- On Mac with Homebrew: `brew install python@3.12`
- On Ubuntu/Debian: `sudo apt install python3.12`

On Windows: during installation, check the box **"Add Python to PATH"** — otherwise commands won't work in the terminal.

---

## Step 2 — Get a Brave Search API key (free)

The scripts use Brave Search to find keywords, competitors, and backlink opportunities. The free tier gives 2,000 queries/month.

1. Go to [brave.com/search/api](https://brave.com/search/api/)
2. Click **"Get started for free"**
3. Create an account (email + password, no credit card needed for free tier)
4. After login, go to **API Keys** in the dashboard
5. Click **"New API key"**
6. Copy the key — it looks like `BSA...` (long string)

Keep this key somewhere safe. You'll set it as an environment variable in Step 5.

---

## Step 3 — Install Claude Code (optional but recommended)

Claude Code lets you control the agent by typing natural language commands in your terminal.

**Requirements:** Node.js 18 or higher. Check with `node --version`.

If you don't have Node.js: download from [nodejs.org](https://nodejs.org/) (LTS version).

**Install Claude Code:**
```bash
npm install -g @anthropic-ai/claude-code
```

**Verify installation:**
```bash
claude --version
```

You'll need an Anthropic API key to use Claude Code. Get one at [console.anthropic.com](https://console.anthropic.com/).

> **Don't want to use Claude Code?** That's fine. You can run the Python scripts manually in your terminal and use ChatGPT, Cursor, or any AI to interpret the results.

---

## Step 4 — Clone the repo and install dependencies

```bash
git clone https://github.com/robinbril/seo-agent-public.git
cd seo-agent-public
pip install -r scripts/requirements.txt
```

The `requirements.txt` installs `requests` and `beautifulsoup4`. Everything else uses Python's standard library.

**Check that scripts are accessible:**
```bash
python scripts/rank_tracker.py --help
```

If you see a usage message, you're good.

---

## Step 5 — Set your Brave API key as environment variable

The scripts read the key from `BRAVE_API_KEY` in your environment.

**Mac/Linux (current session):**
```bash
export BRAVE_API_KEY=your_key_here
```

**Mac/Linux (permanent — add to ~/.zshrc or ~/.bashrc):**
```bash
echo 'export BRAVE_API_KEY=your_key_here' >> ~/.zshrc
source ~/.zshrc
```

**Windows (PowerShell, current session):**
```powershell
$env:BRAVE_API_KEY = "your_key_here"
```

**Windows (permanent — via System Properties):**
1. Search "environment variables" in Start menu
2. Click "Edit the system environment variables"
3. Click "Environment Variables..."
4. Under "User variables", click "New"
5. Variable name: `BRAVE_API_KEY`, value: your key
6. Click OK

**Test that it's set:**
```bash
# Mac/Linux:
echo $BRAVE_API_KEY

# Windows PowerShell:
echo $env:BRAVE_API_KEY
```

Should print your key, not an empty line.

---

## Step 6 — Fill in `config.json`

Open `config.json` in any text editor. Replace every placeholder with your actual values.

```json
{
  "site_name": "Bakkerij De Hoek",
  "domain": "bakkerijdehoek.nl",
  "niche": "ambachtelijke bakkerij",
  "target_keywords": [
    "bakkerij Utrecht",
    "vers brood Utrecht",
    "biologisch brood Utrecht"
  ],
  "target_location": "Utrecht",
  "competitors": [
    "bakkerijkoolwijk.nl",
    "oudhollandschebakkerij.nl"
  ],
  "language": "nl",
  "serp_location": "nl",
  "weekly_tracking_day": "monday",
  "content_output_dir": "content/",
  "briefs_output_dir": "briefs/",
  "rankings_dir": "rankings/"
}
```

**Field explanation:**

| Field | What to put here |
|---|---|
| `site_name` | Your business name (for reports) |
| `domain` | Your domain without `https://` — e.g. `bakkerijdehoek.nl` |
| `niche` | Your industry in 2–3 words — used in Brave Search queries |
| `target_keywords` | 5–20 keywords you want to rank for |
| `target_location` | Your city or region |
| `competitors` | 3–5 competitor domains (no `https://`) |
| `language` | `nl` for Dutch, `en` for English |
| `serp_location` | Country code for Google results: `nl`, `de`, `be`, `us`, etc. |
| `weekly_tracking_day` | Day the rank tracker runs: `monday`, `tuesday`, etc. |

---

## Step 7 — Fill in `brand.md`

This is the most important file. The AI reads this every time it writes content — it determines tone, style, and what to emphasize.

Open `brand.md` and fill in all sections:

**Bedrijfsnaam / Website / Tagline**
Simple. Your name, URL, and a one-sentence description.

**Wat doe je?**
2–3 sentences. What do you offer? Who is it for? What problem does it solve?

**Doelgroep**
Describe your ideal customer. What do they search for? What frustrates them?

**USPs**
3 things that make you different from competitors. Be specific.
- Bad: "We have great service"
- Good: "We answer within 2 hours on weekdays and Saturdays"

**Tone of voice**
How do you want to sound? Pick from: professional/informal, direct/explanatory, formal/conversational.
Add a sample sentence that captures your voice.

**Diensten**
Fill in the table with your services, descriptions, and optional prices.

**Geografisch werkgebied**
Where do you operate? City only, region, or national?

**Concurrenten**
Same domains as in `config.json`. Helps the AI understand what you're competing with.

---

## Step 8 — Run your first analysis

**With Claude Code:**
```bash
claude
```

Then type:
```
Run keyword gap analysis
```

Claude will:
1. Read `config.json` for your domain and competitors
2. Run `python scripts/keyword_gaps.py`
3. Analyze the results
4. Save a brief to `briefs/keyword-gaps-YYYY-MM-DD.md`

Open that file to see which keywords you should target first.

**Without Claude Code (manual):**
```bash
python scripts/keyword_gaps.py
```

Then paste the output into ChatGPT with the question: "Which of these keywords should I target first for a local business in [your city]?"

---

## Step 9 — Multi-site setup

Running the agent for multiple websites? Put each site in its own subfolder under `sites/`.

**Folder structure:**
```
sites/
  my-bakery/
    config.json     ← site-specific config
    brand.md        ← site-specific brand voice
    content/
    briefs/
    rankings/
  my-restaurant/
    config.json
    brand.md
    content/
    briefs/
    rankings/
```

**Setup:**
```bash
mkdir -p sites/my-bakery/content sites/my-bakery/briefs sites/my-bakery/rankings
cp config.json sites/my-bakery/config.json
cp brand.md sites/my-bakery/brand.md
# Edit the copied files with that site's data
```

**Usage with Claude Code:**
```
Run keyword gap analysis for my-bakery
Write article for my-restaurant about pasta Utrecht
Track rankings for my-bakery
```

**Usage with scripts directly:**
```bash
python scripts/rank_tracker.py --config sites/my-bakery/config.json
python scripts/backlink_finder.py --site mybakery.nl --niche "bakkerij" --limit 20
```

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'requests'`**
```bash
pip install -r scripts/requirements.txt
```

**`BRAVE_API_KEY not set or empty`**
Set the environment variable as described in Step 5. Note it resets when you close your terminal unless you added it permanently.

**`python: command not found`**
Try `python3` instead of `python`. On some systems the command is `python3`.

**Scripts run but return no results**
Check that your `config.json` has real competitor domains (not placeholders). The keyword gap script needs at least one competitor to compare against.

**Claude Code says it can't run scripts**
Make sure you're running `claude` from inside the repo directory (`cd seo-agent-public` first).
