import os
import secrets

import httpx

from token_store import save_token

CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
REDIRECT_URI = f"{BASE_URL}/auth/callback"

AUTHORIZE_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
SCOPE = "Calendars.Read offline_access"

# In-Memory State-Store (reicht für single-instance Setup-Flow)
_pending_states: set[str] = set()


def get_auth_url() -> str:
    state = secrets.token_urlsafe(16)
    _pending_states.add(state)
    params = (
        f"client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPE.replace(' ', '%20')}"
        f"&state={state}"
        f"&prompt=consent"
    )
    return f"{AUTHORIZE_URL}?{params}"


async def handle_callback(code: str, state: str) -> None:
    if state not in _pending_states:
        raise ValueError("Ungültiger OAuth-State.")
    _pending_states.discard(state)

    async with httpx.AsyncClient() as client:
        resp = await client.post(TOKEN_URL, data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        })
        resp.raise_for_status()
        token = resp.json()

    if "refresh_token" not in token:
        raise ValueError(
            "Kein Refresh-Token erhalten. "
            "Bitte sicherstellen dass 'offline_access' im Scope enthalten ist."
        )

    save_token({"refresh_token": token["refresh_token"]})
