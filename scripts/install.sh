#!/usr/bin/env bash
# Robin's Marketing Engine — local bootstrap
# Run once after cloning the repo on a new machine.
# Idempotent: safe to re-run.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

say()  { printf "\033[1;34m▸\033[0m %s\n" "$*"; }
ok()   { printf "\033[1;32m✓\033[0m %s\n" "$*"; }
warn() { printf "\033[1;33m!\033[0m %s\n" "$*"; }
fail() { printf "\033[1;31m✗\033[0m %s\n" "$*"; exit 1; }

# ───────────────────────────────────────────────────────────────
# 1 · Check tooling
# ───────────────────────────────────────────────────────────────
say "Checking required tools"

command -v node >/dev/null 2>&1 || fail "node not found — install from https://nodejs.org (>=18)"
NODE_MAJOR=$(node -p "process.versions.node.split('.')[0]")
[[ "$NODE_MAJOR" -ge 18 ]] || fail "node $NODE_MAJOR found; need >=18"
ok "node $(node --version)"

command -v npx >/dev/null 2>&1 || fail "npx not found (should ship with node)"
ok "npx $(npx --version)"

command -v python3 >/dev/null 2>&1 || fail "python3 not found — install 3.10+"
ok "python3 $(python3 --version | awk '{print $2}')"

if ! command -v uv >/dev/null 2>&1; then
  say "Installing uv (needed for Google Ads MCP)"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi
ok "uv $(uv --version | awk '{print $2}')"

command -v claude >/dev/null 2>&1 || {
  warn "claude CLI not found — install with: npm install -g @anthropic-ai/claude-code"
  warn "The MCP servers + skills will only work through Claude Code."
}

# ───────────────────────────────────────────────────────────────
# 2 · Python deps for SEO scripts
# ───────────────────────────────────────────────────────────────
say "Installing Python deps for SEO scripts"
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
# shellcheck source=/dev/null
source .venv/bin/activate
pip install -q --upgrade pip
pip install -q -r scripts/requirements.txt
pip install -q google-auth-oauthlib  # for google_ads_get_refresh_token.py
ok "Python deps installed in .venv"

# ───────────────────────────────────────────────────────────────
# 3 · .env bootstrap
# ───────────────────────────────────────────────────────────────
if [[ ! -f .env ]]; then
  say "Creating .env from template"
  cp .env.example .env
  warn ".env created — edit it and fill in your keys before running any ads commands"
  warn "See docs/ADS-MCP-SETUP.md for how to obtain each credential"
else
  ok ".env exists"
fi

# Validate .env has at least BRAVE_API_KEY
if ! grep -qE '^BRAVE_API_KEY=.+' .env; then
  warn "BRAVE_API_KEY is not set in .env — SEO scripts won't work"
fi

# ───────────────────────────────────────────────────────────────
# 4 · Prime MCP package caches
# ───────────────────────────────────────────────────────────────
say "Pre-downloading Meta Ads MCP (meta-ads-mcp on npm)"
npx -y meta-ads-mcp --help >/dev/null 2>&1 || warn "meta-ads-mcp pre-download skipped (needs network)"
ok "meta-ads-mcp cached"

say "Pre-downloading Google Ads MCP (gads-mcp via uv)"
# shellcheck disable=SC2015
uvx --from git+https://github.com/itallstartedwithaidea/google-ads-mcp gads-mcp --help >/dev/null 2>&1 \
  || warn "gads-mcp pre-download skipped (needs network or credentials to boot)"
ok "gads-mcp cached"

# ───────────────────────────────────────────────────────────────
# 5 · Verify .mcp.json parses
# ───────────────────────────────────────────────────────────────
say "Validating .mcp.json"
python3 -c 'import json; json.load(open(".mcp.json"))' && ok ".mcp.json is valid JSON"

# ───────────────────────────────────────────────────────────────
# 6 · Summary
# ───────────────────────────────────────────────────────────────
cat <<'EOF'

──────────────────────────────────────────────────────────────────
  Setup complete.

  Next steps:
    1. Edit .env and fill in every TPZ_* and shared credential.
       See docs/ADS-MCP-SETUP.md for step-by-step instructions.
    2. Fill in sites/tpzuyderhoven/ads-config.json with your
       Meta ad account ID, page ID, and Google customer ID.
    3. Run `claude` in this directory. When asked, approve the
       project-scoped MCP servers.
    4. Test: "Check ads performance for tpzuyderhoven last 7 days"

  Skills available in Claude Code:
    • launch-google-search-ad
    • launch-instagram-story-ad
    • ads-daily-check
    • pause-ad
    • adjust-ad-budget
──────────────────────────────────────────────────────────────────
EOF
