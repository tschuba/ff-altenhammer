# Homepage Freiwillige Feuerwehr Altenhammer

Statische Hugo-Website auf GitHub Pages. Inhaltspflege über den GitHub Web Editor, keine technischen Vorkenntnisse nötig.

- **Live:** [feuerwehr.altenhammer.bayern](https://feuerwehr.altenhammer.bayern)
- **Fallback:** [tschuba.github.io/ff-altenhammer](https://tschuba.github.io/ff-altenhammer) (wenn Custom Domain deaktiviert ist)
- **Repo:** [github.com/tschuba/ff-altenhammer](https://github.com/tschuba/ff-altenhammer) (privat)

---

## Lokale Entwicklung

```bash
git clone https://github.com/tschuba/ff-altenhammer.git
cd ff-altenhammer
npm install
hugo server
# → http://localhost:1313/
```

Voraussetzungen: [Hugo Extended ≥ 0.161.1](https://gohugo.io/installation/), Node.js ≥ 22

---

## Inhaltspflege (nicht-technisch)

Alle Inhalte sind Markdown-Dateien im Ordner `content/`. Änderungen direkt im GitHub Web Editor vornehmen — der Build läuft automatisch.

### Termin anlegen

1. GitHub → `content/termine/` → **Add file → Create new file**
2. Dateiname: `JJJJ-MM-TT-kurztitel.md` (z. B. `2026-08-01-sommerfest.md`)
3. Inhalt:
   ```yaml
   ---
   title: "Sommerfest"
   date: 2026-08-01T18:00:00
   ort: "Feuerwehrhaus Altenhammer"
   draft: false
   ---
   Kurze optionale Beschreibung.
   ```
4. **Commit changes** → fertig. Termine verschwinden 14 Tage nach dem Datum automatisch.

### Termin löschen

Datei in `content/termine/` über GitHub löschen — oder einfach abwarten (automatisch nach 14 Tagen).

### Mitgliederzahlen aktualisieren

`hugo.toml` → `aktiveMitglieder` und `foerdermitglieder` ändern → committen.

### Aufnahmeantrag-Formulare aktualisieren

Die DOCX-Dateien in `static/dokumente/` sind Binärdateien und können nicht im Browser bearbeitet werden.

**Ablauf:** Datei herunterladen → lokal in Word/LibreOffice bearbeiten → über GitHub hochladen (Upload files).

Die PDFs werden bei jedem Build **automatisch aus den DOCX-Dateien generiert** — kein manueller Schritt nötig.

### Links in Markdown-Dateien

Interne Seitenlinks müssen `{{< relref >}}` verwenden, damit sie auf GitHub Pages korrekt auflösen:

```markdown
[Termine]({{< relref "termine" >}})
[Mitmachen]({{< relref "mitmachen" >}}#aktiv)
```

Externe Links mit `target="_blank"` via `extlink`-Shortcode:

```markdown
{{< extlink "https://example.com" "Link-Text" >}}
```

---

## Offene Aufgaben

### Inhalte ergänzen

| Datei | Was fehlt |
|---|---|
| `content/spenden.md` | IBAN + BIC des Vereinskontos |
| `content/kuchentheke.md` | Ausstattung, Mietpreis, Kaution, Bedingungen |
| `content/fahrzeuge.md` | Fahrzeuge, Baujahre, Fotos |
| `content/ueber-uns/geschichte.md` | Chronik, historische Fotos |
| `content/jubilaeum/_index.md` | Chronik, Archivfotos |
| `content/kinderfeuerwehr/_index.md` | Fotos der Kinder |

### GiroCode-QR für Spendenseite

Sobald IBAN bekannt: GiroCode-SVG generieren (EPC-Standard) und in `content/spenden.md` einbinden.

### Coolify Services einrichten

#### HeyForm (Kontaktformular + Spendenquittung)

1. Coolify → Projekt **„FF Altenhammer"** anlegen (getrennt von privaten Diensten)
2. Neuer Service → Docker Compose → Inhalt aus `coolify/heyform.compose.yml`
3. Outlook-Passwort im Coolify-UI unter Environment Variables eintragen (Schlüssel: `SMTP_PASSWORD`)
4. Domain: `forms.feuerwehr.altenhammer.bayern`, Port `3000`
5. Deployen → Admin-Account anlegen
6. Google reCAPTCHA aktivieren (optional): Projekt auf [google.com/recaptcha/admin](https://www.google.com/recaptcha/admin) anlegen (reCAPTCHA v3, Domain `ff-forms.schubs.net`), dann `GOOGLE_RECAPTCHA_KEY` und `GOOGLE_RECAPTCHA_SECRET` in Coolify unter Environment Variables eintragen → neu deployen → pro Formular unter Settings → Protection aktivieren
7. **Kontaktformular** anlegen: Felder Name, E-Mail, Nachricht — Betreff-Präfix `[FF-Kontakt]`
8. **Spendenquittung-Formular** anlegen (alle Felder) — Betreff-Präfix `[FF-Spendenquittung]`
9. ~~Embed-Link beider Formulare in `content/kontakt.md` bzw. `content/spenden.md` eintragen~~ ✓ erledigt (Shortcode `{{</* heyform "FORM-ID" */>}}`)

#### Kuchentheke Buchungs-App

1. Coolify → Projekt „FF Altenhammer" → Neuer Service → Docker Compose → `coolify/kuchentheke.compose.yml`
2. Domain: `buchung.feuerwehr.altenhammer.bayern`
3. Image `ghcr.io/tschuba/kuchentheke-app:latest` wird automatisch per GitHub Actions gebaut
4. Umgebungsvariablen im Coolify-UI setzen:

   | Variable | Wert |
   | --- | --- |
   | `MICROSOFT_CLIENT_ID` | Azure App Registration → siehe [docs/kuchentheke-konfiguration.md](docs/kuchentheke-konfiguration.md) |
   | `MICROSOFT_CLIENT_SECRET` | Azure App Registration → siehe [docs/kuchentheke-konfiguration.md](docs/kuchentheke-konfiguration.md) |
   | `SECRET_KEY` | Zufälliger 32-Zeichen-String (`openssl rand -hex 16`) |
   | `CALENDAR_NAME` | `Kuchentheke` |
   | `BASE_URL` | `https://buchung.feuerwehr.altenhammer.bayern` |

5. Service starten → einmalig `https://buchung.feuerwehr.altenhammer.bayern/setup` aufrufen und mit `ff-altenhammer@outlook.com` autorisieren
6. Vollständige Anleitung (Azure App Registration, Outlook-Kalender, Troubleshooting): `docs/kuchentheke-konfiguration.md`

#### Traefik Rate Limiting (nach Deployment)

Middleware-Datei `ff-ratelimit.yaml` in Coolify unter **Server → Proxy → Dynamic Configurations** anlegen.
Details und YAML-Inhalt: `PLAN.md`, Abschnitt „Rate Limiting via Traefik".

#### Push-Benachrichtigungen (Phase 6)

ntfy + n8n auf Coolify einrichten — Details folgen in Phase 6.

### Redakteure einladen

GitHub → Repository → **Settings → Collaborators → Add people**

---

## Custom Domain aktivieren / deaktivieren

Die Site ist immer unter `tschuba.github.io/ff-altenhammer` erreichbar. Die Custom Domain `feuerwehr.altenhammer.bayern` kann jederzeit ein- und ausgeschaltet werden. **Jede Änderung löst automatisch einen Rebuild aus (~3 Min).**

**Aktivieren:**

1. GitHub → Repository → **Settings → Pages → Custom domain**
2. `feuerwehr.altenhammer.bayern` eintragen → **Save**
3. Warten bis DNS-Prüfung grün (~5 Min), dann **Enforce HTTPS** aktivieren
4. Ab sofort leitet `tschuba.github.io/ff-altenhammer` auf die Custom Domain weiter

**Deaktivieren** (z. B. während der Entwicklung):

1. GitHub → Repository → **Settings → Pages → Custom domain**
2. Feld leeren → **Save**
3. Die Site ist danach nur noch unter `tschuba.github.io/ff-altenhammer` erreichbar
4. `feuerwehr.altenhammer.bayern` gibt einen DNS-Fehler — DNS-Einträge bei IONOS **nicht** anfassen

---

## DNS-Einträge (IONOS) — Referenz

| Typ | Subdomain | Wert | Zweck |
| --- | --- | --- | --- |
| CNAME | `feuerwehr` | `tschuba.github.io.` | GitHub Pages Hauptdomain |
| CNAME | `www.feuerwehr` | `tschuba.github.io.` | www-Weiterleitung |
| CNAME | `forms.feuerwehr` | `schubs.net.` | HeyForm (Coolify/Raspi) |
| CNAME | `buchung.feuerwehr` | `schubs.net.` | Kuchentheke App (Coolify/Raspi) |

`schubs.net` zeigt via DynDNS auf den Raspberry Pi — CNAMEs folgen automatisch bei IP-Wechsel.

---

## Build & Deploy

Automatisch bei jedem Push auf `main` via GitHub Actions (`.github/workflows/deploy.yml`).

| Trigger | Was passiert |
| --- | --- |
| Push auf `main` | Hugo Build + Deploy auf GitHub Pages |
| Push auf `main` (Änderungen in `kuchentheke-app/`) | Docker Image Build + Push nach `ghcr.io` |
| Täglich 04:00 UTC | Rebuild — abgelaufene Termine verschwinden automatisch |
| Manuell | GitHub → Actions → „Run workflow" |

PDFs werden nur neu generiert wenn sich DOCX-Dateien geändert haben (gecacht per DOCX-Hash).
LibreOffice-Pakete sind ebenfalls gecacht — Version bumpen: `v1` → `v2` in `deploy.yml`, Zeile `apt-libreoffice-`.

---

## Erledigte Einrichtung (Referenz)

| Was | Details |
| --- | --- |
| FF-Logo | `static/images/logo-mark.png` — ChatGPT-generiert (zwei Feuerwehrmänner, Seilring, Burg Flossenbürg) |
| Kinderfeuerwehr-Logo | `static/images/logo-loeschzwerge.png` — Hammerer Löschzwerge |
| Jubiläums-Logo | `static/images/logo-jubilaeum.png` — 100 Jahre 1926–2026 |
| Mannschaftsfoto | `static/images/mannschaft.jpg` |
| Führung | 1. Kommandant: Rüdiger Hettler · 2. Kommandant: Florian Moser |
| Social Media | Facebook & Instagram verlinkt, WhatsApp entfernt |
| Sticky Navigation | Header fixiert beim Scrollen, Logo blendet sich ein wenn Hero-Logo aus dem Bild scrollt |
| GitHub Pages Pfade | Alle internen Links mit `relURL` / `relref` — funktionieren unter Subdirectory und Custom Domain |
| HeyForm | Kontakt- + Spendenquittungsformular auf `ff-forms.schubs.net` |
| Kuchentheke App | Docker-Container auf Coolify, einmalig `/setup` autorisiert — Details: `docs/kuchentheke-konfiguration.md` |
