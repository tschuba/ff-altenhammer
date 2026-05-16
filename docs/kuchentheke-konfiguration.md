# Kuchentheke Buchungssystem – Konfigurationsanleitung

## Übersicht

Die Kuchentheke-App zeigt auf der Website einen Verfügbarkeitskalender an, der direkt aus dem Outlook-Kalender gelesen wird. Buchungen werden direkt in Outlook eingetragen — die App hat keine eigene Admin-Oberfläche.

---

## Schritt 1: Outlook-Unterkalender anlegen

1. Outlook.com im Browser öffnen (outlook.com)
2. Linke Seitenleiste → Kalender-Symbol
3. Unter "Meine Kalender" auf **"Kalender hinzufügen"** klicken
4. **"Neuen Kalender erstellen"** wählen
5. Name: **`Kuchentheke`** (Groß-/Kleinschreibung beachten)
6. Farbe nach Wunsch wählen → Speichern

> Der Kalender-Name muss exakt mit der Umgebungsvariable `CALENDAR_NAME` übereinstimmen (Standard: `Kuchentheke`).

---

## Schritt 2: Azure App Registration anlegen

1. Browser öffnen: [portal.azure.com](https://portal.azure.com)
2. Mit `ff-altenhammer@outlook.com` anmelden
3. Oben auf das **Lupen-Symbol** klicken → `App-Registrierungen` eintippen → ersten Treffer öffnen
   *(alternativ: linkes Menü → **Microsoft Entra ID** → linkes Untermenü → **App-Registrierungen**)*
4. **"+ Neue Registrierung"** klicken
5. Formular ausfüllen:
   - Name: `FF Altenhammer Kuchentheke`
   - Unterstützte Kontotypen: **"Persönliche Microsoft-Konten"**
   - Umleitungs-URI: `https://ff-buchung.schubs.net/auth/callback`
6. **Registrieren** klicken

### CLIENT_ID notieren

Nach der Registrierung auf der Übersichtsseite:
- **Anwendungs-ID (Client)** → das ist die `MICROSOFT_CLIENT_ID`

### CLIENT_SECRET erstellen

1. Linkes Menü → **"Zertifikate & Geheimnisse"**
2. **"+ Neuer geheimer Clientschlüssel"**
3. Beschreibung: `Kuchentheke`, Ablauf: **24 Monate**
4. **Hinzufügen** → den angezeigten **Wert** sofort kopieren (wird nur einmal angezeigt!)
5. Das ist die `MICROSOFT_CLIENT_SECRET`

---

## Schritt 3: Coolify-Service einrichten

1. Coolify öffnen → **"New Service"** → **"Docker Compose"**
2. Compose-Datei: Inhalt von `coolify/kuchentheke.compose.yml` einfügen
3. Domain: `ff-buchung.schubs.net`
4. Umgebungsvariablen setzen:

| Variable | Wert |
|---|---|
| `MICROSOFT_CLIENT_ID` | Wert aus Schritt 2 |
| `MICROSOFT_CLIENT_SECRET` | Wert aus Schritt 2 |
| `SECRET_KEY` | Zufälliger 32-Zeichen-String (z.B. mit `openssl rand -hex 16` generieren) |
| `CALENDAR_NAME` | `Kuchentheke` |
| `BASE_URL` | `https://ff-buchung.schubs.net` |

5. Service starten

---

## Schritt 4: Erster Setup (einmalig)

1. Browser öffnen: `https://ff-buchung.schubs.net/setup`
2. **"Mit Microsoft autorisieren"** klicken
3. Mit `ff-altenhammer@outlook.com` anmelden
4. Berechtigungsanfrage bestätigen (Kalenderzugriff lesen)
5. Weiterleitung zurück zur Setup-Seite → **"Autorisierung erfolgreich"**

Die App kann jetzt automatisch den Outlook-Kalender lesen. Diese Seite muss nicht erneut aufgerufen werden.

---

## Buchungen verwalten

Buchungen werden **direkt in Outlook** eingetragen — keine App nötig.

**Neue Buchung anlegen:**
1. Outlook öffnen (Web, PC oder Handy)
2. Im Unterkalender **"Kuchentheke"** ein neues Ereignis erstellen
3. Titel: Name der Veranstaltung (z.B. "Schützenfest Mayer")
4. Start- und Endzeitpunkt setzen (mehrtägig möglich)
5. Speichern → erscheint sofort auf der Website

**Buchung löschen:**
1. Ereignis im Kalender "Kuchentheke" öffnen
2. Löschen → verschwindet auf der Website

---

## Weitere erlaubte E-Mail-Adressen hinzufügen

Die Umgebungsvariable `ALLOWED_EMAILS` ist für zukünftige Admin-Erweiterungen reserviert. Aktuell wird sie nicht für den Lesezugriff benötigt.

---

## Troubleshooting

### Der Kalender lädt nicht / zeigt keine Buchungen

Mögliche Ursachen:
1. **Unterkalender falsch benannt** → Outlook öffnen, Kalender-Name prüfen (muss exakt `Kuchentheke` sein)
2. **Token abgelaufen** → `/setup` erneut aufrufen und neu autorisieren
3. **Container nicht gestartet** → Coolify-Log prüfen

### "Autorisierung erfolgreich" aber Kalender nicht gefunden

Der Unterkalender "Kuchentheke" existiert nicht. Schritt 1 dieser Anleitung durchführen.

### Token muss erneuert werden

Falls die App aufhört Buchungen zu laden (passiert nach sehr langer Inaktivität):

1. `https://ff-buchung.schubs.net/setup` aufrufen
2. Erneut autorisieren

---

## Technische Details

| Komponente | Wert |
|---|---|
| Docker Image | `ghcr.io/tschuba/kuchentheke-app:latest` |
| Token-Speicherort | Docker Volume `token_data:/data/token.json` |
| Graph API Scope | `Calendars.Read offline_access` |
| Kalender-Zeitraum | 30 Tage zurück bis 365 Tage voraus |
