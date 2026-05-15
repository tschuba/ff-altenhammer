import json
import os
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from auth import get_auth_url, handle_callback
from graph import get_buchungen
from token_store import has_token

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def _fmt_dt(iso: str, all_day: bool) -> str:
    try:
        dt = datetime.fromisoformat(iso)
        if all_day:
            return dt.strftime("%-d. %b %Y")
        return dt.strftime("%-d. %b %Y, %H:%M Uhr")
    except Exception:
        return iso


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    if not has_token():
        return RedirectResponse("/setup")

    try:
        buchungen_raw = await get_buchungen()
    except Exception:
        buchungen_raw = []

    buchungen = [
        {
            **b,
            "start_fmt": _fmt_dt(b["start"], b["allDay"]),
            "end_fmt": _fmt_dt(b["end"], b["allDay"]),
        }
        for b in buchungen_raw
    ]

    return templates.TemplateResponse("kalender.html", {
        "request": request,
        "buchungen": buchungen,
        "buchungen_json": json.dumps([
            {"title": b["title"], "start": b["start"], "end": b["end"], "allDay": b["allDay"]}
            for b in buchungen
        ]),
    })


@app.get("/api/buchungen")
async def api_buchungen():
    if not has_token():
        return []
    try:
        return await get_buchungen()
    except Exception:
        return []


@app.get("/setup", response_class=HTMLResponse)
async def setup(request: Request):
    calendar_error = None
    if has_token():
        try:
            await get_buchungen()
        except ValueError as e:
            calendar_error = str(e)
        except Exception:
            pass

    return templates.TemplateResponse("setup.html", {
        "request": request,
        "auth_url": get_auth_url(),
        "success": False,
        "error": None,
        "calendar_error": calendar_error,
    })


@app.get("/auth/callback", response_class=HTMLResponse)
async def auth_callback(request: Request, code: str = "", state: str = "", error: str = ""):
    if error:
        return templates.TemplateResponse("setup.html", {
            "request": request,
            "auth_url": get_auth_url(),
            "success": False,
            "error": f"Microsoft hat die Anfrage abgelehnt: {error}",
            "calendar_error": None,
        })

    try:
        await handle_callback(code, state)
    except Exception as e:
        return templates.TemplateResponse("setup.html", {
            "request": request,
            "auth_url": get_auth_url(),
            "success": False,
            "error": str(e),
            "calendar_error": None,
        })

    calendar_error = None
    try:
        await get_buchungen()
    except ValueError as e:
        calendar_error = str(e)
    except Exception:
        pass

    return templates.TemplateResponse("setup.html", {
        "request": request,
        "auth_url": get_auth_url(),
        "success": True,
        "error": None,
        "calendar_error": calendar_error,
    })
