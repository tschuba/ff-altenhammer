import os
from datetime import datetime, timedelta, timezone

import httpx

from token_store import load_token, save_token

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
CALENDAR_NAME = os.getenv("CALENDAR_NAME", "Kuchentheke")
CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")


async def _refresh_access_token() -> str:
    token = load_token()
    if not token:
        raise RuntimeError("Kein Token vorhanden — bitte /setup aufrufen.")

    async with httpx.AsyncClient() as client:
        resp = await client.post(TOKEN_URL, data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": token["refresh_token"],
            "grant_type": "refresh_token",
            "scope": "Calendars.Read offline_access",
        })
        resp.raise_for_status()
        new_token = resp.json()

    # Refresh-Token aktualisieren falls Microsoft einen neuen schickt
    if "refresh_token" in new_token:
        token["refresh_token"] = new_token["refresh_token"]
        save_token(token)

    return new_token["access_token"]


async def _get(path: str) -> dict:
    access_token = await _refresh_access_token()
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{GRAPH_BASE}{path}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Prefer": 'outlook.timezone="Europe/Berlin"',
            },
        )
        resp.raise_for_status()
        return resp.json()


async def get_calendar_id() -> str:
    data = await _get("/me/calendars")
    for cal in data.get("value", []):
        if cal["name"] == CALENDAR_NAME:
            return cal["id"]
    raise ValueError(
        f"Outlook-Unterkalender '{CALENDAR_NAME}' nicht gefunden. "
        "Bitte den Kalender in Outlook anlegen."
    )


async def get_buchungen() -> list[dict]:
    cal_id = await get_calendar_id()
    now = datetime.now(timezone.utc)
    start = (now - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = (now + timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")

    data = await _get(
        f"/me/calendars/{cal_id}/calendarView"
        f"?startDateTime={start}&endDateTime={end}"
        f"&$select=subject,start,end,isAllDay"
        f"&$orderby=start/dateTime"
        f"&$top=100"
    )

    buchungen = []
    for event in data.get("value", []):
        buchungen.append({
            "title": event.get("subject", "Belegt"),
            "start": event["start"]["dateTime"],
            "end": event["end"]["dateTime"],
            "allDay": event.get("isAllDay", False),
        })
    return buchungen
