"""
One-shot helper to generate a Google Ads refresh token for use with
itallstartedwithaidea/google-ads-mcp.

Usage:
    python3 -m venv .venv && source .venv/bin/activate
    pip install google-auth-oauthlib
    export GOOGLE_ADS_CLIENT_ID=...     # from Google Cloud Console OAuth client
    export GOOGLE_ADS_CLIENT_SECRET=...
    python3 scripts/google_ads_get_refresh_token.py

Opens a browser, you sign in with the Google account that has MCC access
and the script prints the refresh token to paste into .env as
GOOGLE_ADS_REFRESH_TOKEN.
"""

import os
import sys

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/adwords"]


def main() -> int:
    client_id = os.environ.get("GOOGLE_ADS_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_ADS_CLIENT_SECRET")
    if not client_id or not client_secret:
        print(
            "ERROR: set GOOGLE_ADS_CLIENT_ID and GOOGLE_ADS_CLIENT_SECRET first.",
            file=sys.stderr,
        )
        return 1

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }

    flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
    credentials = flow.run_local_server(
        port=0,
        prompt="consent",
        access_type="offline",
        authorization_prompt_message=(
            "Log in with the Google account that has MCC access."
        ),
    )

    print()
    print("=" * 72)
    print("GOOGLE_ADS_REFRESH_TOKEN=" + credentials.refresh_token)
    print("=" * 72)
    print()
    print("Paste the line above into your .env file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
