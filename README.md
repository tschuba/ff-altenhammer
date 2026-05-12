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

Wenn das Formular-Skript selbst geändert wird (Felder, Texte): `python3 scripts/generate_forms.py` lokal ausführen — das erzeugt neue DOCX-Dateien, die dann committed werden.

---

## Offene Aufgaben

### Inhalte ergänzen

| Datei | Was fehlt |
|---|---|
| `content/spenden.md` | IBAN + BIC des Vereinskontos |
| `content/kontakt.md` | Genaue Adresse des Feuerwehrhauses (falls abweichend von Flossenbürger Str. 9) |
| `content/kuchentheke.md` | Ausstattung, Mietpreis, Kaution, Bedingungen |
| `content/fahrzeuge.md` | Fahrzeuge, Baujahre, Fotos |
| `content/ueber-uns/mannschaft.md` | Kommandant, Stellvertreter, Mannschaftsfoto |
| `content/ueber-uns/geschichte.md` | Chronik, historische Fotos |
| `content/jubilaeum/_index.md` | Chronik, Archivfotos |
| `content/kinderfeuerwehr/_index.md` | Fotos |
| `hugo.toml` | Echte Facebook-/Instagram-/WhatsApp-URLs eintragen |

### Logos einbinden

| Logo | Status | Aktion |
|---|---|---|
| FF Altenhammer Hauptlogo | Platzhalter | SVG bereitstellen → `static/images/logo-mark.svg` + `logo-mark-white.svg` ersetzen |
| Kinderfeuerwehr-Logo | Platzhalter | SVG bereitstellen → in `content/kinderfeuerwehr/_index.md` einbinden |
| Jubiläums-Logo (100 Jahre) | Platzhalter | SVG bereitstellen → als `assets/images/jubilaeum-logo.svg` ablegen |

### GiroCode-QR für Spendenseite

Sobald IBAN bekannt: GiroCode-SVG generieren (EPC-Standard) und in `content/spenden.md` einbinden.

### Coolify Services einrichten

#### HeyForm (Kontaktformular + Spendenquittung)

1. Coolify → Projekt **„FF Altenhammer"** anlegen (getrennt von privaten Diensten)
2. Neuer Service → Docker Compose → Inhalt aus `coolify/heyform.compose.yml`
3. Outlook-Passwort im Coolify-UI unter Environment Variables eintragen (Schlüssel: `SMTP_PASSWORD`)
4. Domain: `forms.feuerwehr.altenhammer.bayern`, Port `3000`
5. Deployen → Admin-Account anlegen
6. hCaptcha aktivieren: kostenlosen Account auf [hcaptcha.com](https://www.hcaptcha.com) anlegen, Keys in HeyForm-Einstellungen eintragen
7. **Kontaktformular** anlegen: Felder Name, E-Mail, Nachricht — Betreff-Präfix `[FF-Kontakt]`
8. **Spendenquittung-Formular** anlegen (alle Felder) — Betreff-Präfix `[FF-Spendenquittung]`
9. Embed-Link beider Formulare in `content/kontakt.md` bzw. `content/spenden.md` eintragen

#### Easy!Appointments (Kuchentheke-Buchung)

1. Coolify → Projekt „FF Altenhammer" → Neuer Service → Docker Compose → `coolify/easyappointments.compose.yml`
2. Domain: `buchung.feuerwehr.altenhammer.bayern`, Port `80`
3. Setup-Wizard: SMTP konfigurieren (`smtp-mail.outlook.com:587`, `ff-altenhammer@outlook.com`)
4. Service **„Kuchentheke"** anlegen, manuelle Bestätigung aktivieren
5. Betreff-Präfix: `[FF-Kuchentheke]`
6. Buchungs-Widget-Code in `content/kuchentheke.md` eintragen

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
| CNAME | `buchung.feuerwehr` | `schubs.net.` | Easy!Appointments (Coolify/Raspi) |

`schubs.net` zeigt via DynDNS auf den Raspberry Pi — CNAMEs folgen automatisch bei IP-Wechsel.

---

## Build & Deploy

Automatisch bei jedem Push auf `main` via GitHub Actions (`.github/workflows/deploy.yml`).

| Trigger | Was passiert |
| --- | --- |
| Push auf `main` | Build + Deploy |
| Täglich 04:00 UTC | Rebuild — abgelaufene Termine verschwinden automatisch |
| Manuell | GitHub → Actions → „Run workflow" |

PDFs werden nur neu generiert wenn sich DOCX-Dateien geändert haben (gecacht per DOCX-Hash).
LibreOffice-Pakete sind ebenfalls gecacht — Version bumpen: `v1` → `v2` in `deploy.yml`, Zeile `apt-libreoffice-`.
