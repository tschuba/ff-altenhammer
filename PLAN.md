# Plan: Homepage Freiwillige Feuerwehr Altenhammer

## Kontext

Erstellung einer professionellen, wartungsarmen Homepage für die Freiwillige Feuerwehr Altenhammer.
Hosting via GitHub Pages, Inhaltspflege durch mehrere Personen (teils nicht-technisch), kein bestehendes Hauptlogo/Branding.

**Besonderheiten:**

- **Jubiläum 2026:** 100-jähriges Bestehen (gegründet 1926) — soll prominent auf der Homepage sichtbar sein
- Die **Kinderfeuerwehr** hat ein eigenes Logo (wird bereitgestellt)
- Es gibt einen **Feuerwehrverein** (Förderverein) neben der aktiven Wehr — muss im "Über uns"-Bereich berücksichtigt werden
- **Zwei Mitgliedschaftsarten:** Aktiv (Einsatzkräfte) und Passiv/Fördernd (zahlendes Mitglied, kein Einsatz)

---

## Tech-Stack

| Komponente | Entscheidung | Begründung |
| --- | --- | --- |
| Static Site Generator | **Hugo** (latest extended) | Schnell, Markdown-basiert, keine Datenbankabhängigkeit |
| CSS Framework | **Tailwind CSS v3** via Hugo Pipes + PostCSS | Design-Token-System, responsive, WCAG AA |
| Hosting | **GitHub Pages** | Kostenlos, HTTPS, spätere Custom Domain möglich |
| CI/CD | **GitHub Actions** (native actions) | Automatisches Build + Deploy auf Push zu `main` |
| Schriften | **Selbst-gehostet** (kein Google Fonts CDN) | DSGVO-Pflicht seit BGH-Urteil 2022 |
| Kontaktformular | **Selbst-gehosteter Microservice** auf Coolify | Kein Drittanbieter, DSGVO-sauber (s.u.) |
| Nicht-technische Pflege | **GitHub Web Editor** | Markdown-Dateien direkt im Browser editieren |

---

## Kontaktformular — Selbst-gehosteter Microservice (Coolify)

Da ein Coolify-Server vorhanden ist, wird **kein Drittanbieter** wie Formspree benötigt.

**Architektur:** Minimaler Node.js-Dienst (Fastify + Nodemailer, ~60 Zeilen Code), der auf Coolify läuft.

```text
Hugo-Formular → POST https://mail.ff-altenhammer.de/contact
                  → Coolify: Fastify + Nodemailer → SMTP → E-Mail an Wehr
```

**Vorteile:**

- Keine Drittpartei sieht Formulardaten → DSGVO-Vorteil, kein Eintrag in Datenschutzerklärung nötig
- Kostenlos, dauerhaft zuverlässig
- SMTP-Zugangsdaten als Coolify Environment Variables — nie im Code

**Benötigt:**

- SMTP-Zugangsdaten der Feuerwehr (z.B. bestehende E-Mail-Adresse via STARTTLS)
- Subdomain `mail.ff-altenhammer.de` oder ähnliches (oder IP:Port für Anfang)
- CORS-Header im Microservice auf die GitHub Pages Domain beschränken

**Datei:** `form-service/` als eigenes Repository oder Unterordner

---

## Branding & Design (Brand Guardian + UI Designer)

### Brand Foundation

- **Name:** Freiwillige Feuerwehr Altenhammer / FF Altenhammer
- **Jubiläumslinie:** "100 Jahre im Dienst der Gemeinschaft — 1926–2026"
- **Werte:** Gemeinschaft · Sicherheit · Einsatzbereitschaft · Tradition
- **Ton:** Professionell, warm, bodenständig, vertrauenswürdig

### Farbpalette (Design Tokens)

```css
--color-primary:        #CC0000;   /* Feuerwehr-Rot */
--color-primary-dark:   #990000;   /* Dunkelrot für Hover/Akzente */
--color-gold:           #F0A500;   /* Goldgelb — Jubiläums-Akzent */
--color-dark:           #1C1C1C;   /* Fast Schwarz — Text, Header-BG */
--color-surface:        #F8F8F8;   /* Hintergrund */
--color-white:          #FFFFFF;
```

### Typografie (selbst-gehostet)

- **Headlines:** Oswald Bold — impactvoll, Feuerwehr-gerecht
- **Body:** Inter Regular/Medium — modern, sehr lesbar
- Skala (4px-Basis): 12 → 14 → 16 → 20 → 24 → 30 → 36 → 48px

### Logos

| Logo | Quelle | Verwendung |
| --- | --- | --- |
| FF Altenhammer Hauptlogo | **Neu erstellen** (SVG) | Header, Footer, SEO |
| Kinderfeuerwehr-Logo | **Vorhanden** (bereitstellen) | Kinderfeuerwehr-Sektion |

**Hauptlogo-Konzept:** Stilisiertes Feuerwehrkreuz (Malteser-Stil) in Rot + "FF Altenhammer" in Oswald Bold. Varianten: Farbe (für hellen Hintergrund) + Weiß (für roten Header).

### Jubiläums-Branding

Gold-Akzent `#F0A500` für alle Jubiläumselemente. Badge/Ribbon "100 Jahre — 1926–2026" im Header oder Hero. Separater Bereich auf der Startseite.

### Social Media Icons — Header (prominent, dauerhaft sichtbar)

Facebook · Instagram · WhatsApp — als **SVG-Icon-Buttons oben rechts im Header**, auf jeder Seite sichtbar.

```text
┌─────────────────────────────────────────────────────────┐
│  [Logo] FF Altenhammer    Aktuelles Termine …   f  📷  w │
└─────────────────────────────────────────────────────────┘
         ↑ Navigation                          ↑ Social Icons
```

- Desktop: Icons rechts in der Headerleiste neben der Navigation
- Mobile: Icons neben dem Hamburger-Menü-Button (immer sichtbar, auch wenn Menü zu ist)
- Größe: 20–24px, monochrom weiß auf rotem Header-Hintergrund, Hover: leicht aufgehellt
- SVG-Icons selbst-gehostet (keine CDN wie FontAwesome → DSGVO)
- `hugo.toml` params: `facebookUrl`, `instagramUrl`, `whatsappUrl` — einmal eintragen, überall verwendet

### Responsive Breakpoints (Mobile-First)

`sm: 640px` · `md: 768px` · `lg: 1024px` · `xl: 1280px`

---

## Seitenstruktur (Sitemap)

```text
/ (Startseite)
├── Aktuelles (/aktuelles/)
│   └── [Artikel] (/aktuelles/[slug]/)
├── Termine (/termine/)
├── 100 Jahre (/jubilaeum/)               ← Jubiläumsseite 2026
├── Galerie (/galerie/)                   ← Fotoalben nach Kategorien
│   └── [Album] (/galerie/[slug]/)
├── Über uns (/ueber-uns/)
│   ├── Mannschaft (/ueber-uns/mannschaft/)
│   ├── Verein (/ueber-uns/verein/)        ← Förderverein
│   └── Geschichte (/ueber-uns/geschichte/)
├── Kinderfeuerwehr (/kinderfeuerwehr/)
│   └── Mitmachen (/kinderfeuerwehr/mitmachen/)
├── Fahrzeuge & Ausrüstung (/fahrzeuge/)
├── Mitmachen (/mitmachen/)               ← Aktiv + Passiv erklärt, Mitgliederzahlen
├── Kontakt (/kontakt/)                   ← Adresse + Feuerwehrhaus-Standort
├── Impressum (/impressum/)               ⚠ GESETZESPFLICHT
└── Datenschutz (/datenschutz/)           ⚠ GESETZESPFLICHT
```

### Startseiten-Aufbau (Hero → Sections)

1. **Hero** mit Jubiläums-Badge "100 Jahre — 1926–2026", Logo, Slogan, CTA
2. **Jubiläums-Teaser** — Goldener Akzentbereich mit Einladung zur Jubiläumsseite
3. **Neueste Meldungen** — 3 aktuelle Artikel-Cards (mit Foto-Vorschau)
4. **Nächste Termine** — 3 kommende Veranstaltungen
5. **Galerie-Teaser** — 4–6 aktuelle Fotos als Grid, Link zur Galerie
6. **Kinderfeuerwehr-Teaser** — eigenes Logo + Einladung
7. **Mitmachen-Teaser** — Aktiv/Passiv kurz erklärt, Mitgliederzahlen
8. **Social Media Banner** — Facebook, Instagram, WhatsApp (zusätzlich zu den Header-Icons, als auffällige Sektion)
9. **Footer** — Logo, Navigation, Kontakt, Impressum/Datenschutz

---

## Kontaktseite — Feuerwehrhaus-Standort

Die Kontaktseite enthält Adresse, Kontaktdaten und den **Standort des Feuerwehrhauses**.

**Karte — DSGVO-konforme Lösung (kein Google Maps Embed):**

- **Option A (empfohlen):** Statisches OpenStreetMap-Screenshot-Bild + verlinkter "Auf der Karte anzeigen"-Button → öffnet OpenStreetMap im neuen Tab. Kein Tracking, keine Cookies.
- **Option B:** OpenStreetMap-Iframe-Embed — technisch möglich, aber auch OSM sendet beim Laden die IP-Adresse der Besucher an OSM-Server → muss in Datenschutzerklärung erwähnt werden. Weniger problematisch als Google Maps, aber nicht ganz sauber.
- **Google Maps Embed:** Nur mit Cookie-Consent-Banner erlaubt → zu komplex für diese Site.

**Empfehlung:** Option A — statisches Kartenbild + externer Link. Einfach, DSGVO-sauber, kein Wartungsaufwand.

---

## Galerie

Eine dedizierte Galerie-Sektion für Fotos von Einsätzen, Übungen, Veranstaltungen und dem Feuerwehrhaus.

**Struktur:** Alben als Hugo Page Bundles — jedes Album ist ein Ordner mit Markdown-Datei und Bildern.

```yaml
# content/galerie/jahresuebung-2026/_index.md
---
title: "Jahresübung 2026"
date: 2026-04-20
cover: "bild-01.jpg"
---
```

**Bilder** liegen direkt im Album-Ordner (`content/galerie/jahresuebung-2026/bild-01.jpg` usw.) — Hugo verarbeitet sie automatisch als Page Resources und kann Thumbnails generieren.

**Technisch:** Hugo's eingebaute `images.Resize`-Funktion erstellt komprimierte Thumbnails beim Build — keine externen Bild-Dienste nötig.

---

## Mitmachen-Seite — Mitgliedschaft im Detail

```text
Aktive Mitgliedschaft
  → Alter ab 16 Jahren (nach Kinderfeuerwehr)
  → Einsätze, Übungen, Ausbildung
  → Aktuell X aktive Mitglieder  ← konfigurierbar in hugo.toml params

Fördermitgliedschaft (Passiv)
  → Jedes Alter
  → Finanzielles Bekenntnis zur Wehr
  → Kein Einsatz erforderlich
  → Aktuell X Fördermitglieder   ← konfigurierbar in hugo.toml params
```

Mitgliederzahlen werden als **Hugo-Parameter** in `hugo.toml` gepflegt — kein Code-Edit nötig.

---

## Über uns — Verein

Die **Über uns**-Sektion trennt klar:

- **Aktive Wehr** — Einsatzabteilung, Mannschaft, Führung
- **Feuerwehrverein** — Zweck (Förderung der Wehr), Vorstand, Mitgliedschaft, Satzung (PDF-Link)
- **Kinderfeuerwehr** — eigene Sektion (s. Sitemap)

---

## Repository-Struktur

```text
ff-altenhammer/                        ← Hugo-Seite
├── .github/
│   └── workflows/
│       └── deploy.yml
├── archetypes/
│   ├── aktuelles.md
│   └── termine.md
├── assets/
│   ├── css/
│   │   └── main.css
│   ├── images/
│   │   ├── logo.svg                   ← Hauptlogo (Farbe, neu erstellt)
│   │   ├── logo-white.svg             ← Hauptlogo Weiß
│   │   ├── kf-logo.svg                ← Kinderfeuerwehr-Logo (bereitgestellt)
│   │   └── feuerwehrhaus-karte.png    ← Statischer OSM-Screenshot
│   └── js/
│       └── main.js
├── content/
│   ├── _index.md
│   ├── aktuelles/
│   ├── termine/
│   ├── jubilaeum/
│   │   └── _index.md
│   ├── ueber-uns/
│   │   ├── _index.md
│   │   ├── mannschaft.md
│   │   ├── verein.md
│   │   └── geschichte.md
│   ├── kinderfeuerwehr/
│   │   └── _index.md
│   ├── galerie/
│   │   ├── _index.md
│   │   └── [album]/                   ← Page Bundle: _index.md + Bilder
│   ├── fahrzeuge/
│   │   └── _index.md
│   ├── mitmachen.md
│   ├── kontakt.md
│   ├── impressum.md
│   └── datenschutz.md
├── layouts/
│   ├── _default/
│   │   ├── baseof.html
│   │   ├── list.html
│   │   └── single.html
│   ├── index.html
│   ├── aktuelles/
│   │   ├── list.html
│   │   └── single.html
│   ├── termine/
│   │   └── list.html
│   ├── galerie/
│   │   ├── list.html
│   │   └── single.html
│   └── partials/
│       ├── head.html
│       ├── header.html
│       ├── footer.html
│       ├── hero.html
│       ├── jubilaeum-banner.html
│       ├── news-card.html
│       ├── event-card.html
│       └── galerie-thumb.html
├── static/
│   ├── fonts/
│   ├── dokumente/                     ← Einwilligungsformulare (PDF/DOCX)
│   └── CNAME
├── package.json
├── tailwind.config.js
├── postcss.config.js
├── hugo.toml
└── README.md

form-service/                          ← Separates Repo für Coolify
├── index.js
├── package.json
├── Dockerfile
└── README.md
```

---

## Content-Typen & Frontmatter

### Artikel (aktuelles/)

```yaml
---
title: "Übungsabend Technische Hilfeleistung"
date: 2026-05-10
description: "Kurze Zusammenfassung für Vorschau"
image: "images/uebung-2026-05.jpg"
kategorie: "Übung"   # Einsatz | Übung | Veranstaltung | Allgemein
---
```

### Termin (termine/)

```yaml
---
title: "Jahreshauptversammlung"
date: 2026-06-15T19:00:00
endDate: 2026-06-15T21:00:00
ort: "Feuerwehrhaus Altenhammer"
beschreibung: "Kurze Beschreibung"
oeffentlich: true
---
```

### Hugo Params (hugo.toml)

```toml
[params]
  aktiveMitglieder    = 32
  foerdermitglieder   = 45
  gegruendet          = 1926
  jubilaeum           = true
  facebookUrl         = "https://facebook.com/..."
  instagramUrl        = "https://instagram.com/..."
  whatsappUrl         = "https://wa.me/..."
```

---

## GitHub Actions Workflow (deploy.yml)

```yaml
name: Deploy Hugo to GitHub Pages
on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
      - run: npm ci
      - uses: actions/configure-pages@v5
      - name: Setup Hugo
        run: |
          curl -L -o hugo.deb \
            https://github.com/gohugoio/hugo/releases/latest/download/hugo_extended_linux_amd64.deb
          sudo dpkg -i hugo.deb
      - name: Build
        run: hugo --minify
      - uses: actions/upload-pages-artifact@v3
        with:
          path: public

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

---

## Workflow: Inhaltspflege → Veröffentlichung

```text
Technischer Redakteur:
  Lokaler Clone → hugo server → commit + push → GitHub Actions → Live

Nicht-technischer Redakteur:
  github.com → Repository → content/aktuelles/ → ✏ Edit / Neue Datei
  → Markdown schreiben → "Commit changes" → GitHub Actions → Live (~90s)

Mitgliederzahlen aktualisieren:
  hugo.toml → aktiveMitglieder / foerdermitglieder ändern → commit → Live
```

---

## ⚠ Wichtige Probleme & Einschränkungen

### Gesetzlich verpflichtend (Deutschland)

1. **Impressum (TMG §5):** Vollständige Adresse, Name des Verantwortlichen, Kontakt. Abmahnrisiko + bis zu 50.000 € Bußgeld bei Fehlen.
2. **Datenschutzerklärung (DSGVO):** GitHub Pages Server-Logs erwähnen. Kein Eintrag für Coolify-Formular nötig, da selbst gehostet.
3. **Google Fonts CDN:** Verboten (BGH I ZR 223/19). Fonts selbst hosten — bereits eingeplant.
4. **Facebook:** Direkte Links sind OK. Kein Widget/Embed ohne Cookie-Banner.

### Fotos von Personen (DSGVO Art. 6 + Art. 8)

Zwei Einwilligungsformular-Vorlagen werden als Teil des Projekts erstellt und unter `static/dokumente/` abgelegt:

- **Erwachsene:** Einwilligung zur Veröffentlichung auf Homepage + Social Media (widerrufbar)
- **Minderjährige:** Separate Vorlage, Unterschrift beider Erziehungsberechtigter erforderlich

Bis unterzeichnete Formulare vorliegen: keine erkennbaren Personen online stellen. Die Datenschutzerklärung nennt die Rechtsgrundlage (Art. 6 Abs. 1 lit. a DSGVO).

### Jubiläum — Zeitlicher Hinweis

Das `jubilaeum = true`-Flag in `hugo.toml` steuert das Jubiläums-Banner site-weit. Nach 2026 einfach auf `false` setzen.

### Statische Site — Grenzen

- Eventkalender: Manuelle Markdown-Pflege (kein Live-Sync mit Google Calendar)
- Kommentarfunktion: Nicht vorgesehen — Facebook-Link für Interaktion

### Custom Domain (Zukunft)

`baseURL` in `hugo.toml` + `CNAME`-Datei in `static/` aktualisieren. GitHub Pages bietet HTTPS via Let's Encrypt kostenlos.

### Nicht-technische Mitarbeiter

Benötigen GitHub-Account + Collaborator-Zugang. Kurze Einführung für Bilder-Upload empfohlen.

---

## Implementierungsphasen

### Phase 1 — Foundation
- [ ] GitHub Repository `ff-altenhammer` anlegen
- [ ] Hugo-Projekt initialisieren (`hugo new site`)
- [ ] `hugo.toml` mit Params konfigurieren
- [ ] Tailwind CSS v3 + PostCSS einrichten
- [ ] GitHub Actions Workflow (`deploy.yml`)
- [ ] GitHub Pages Source auf "GitHub Actions" stellen
- [ ] Base-Layout: `baseof.html`, Header, Footer

### Phase 2 — Branding & Design
- [ ] Hauptlogo SVG erstellen (Farbe + Weiß-Variante)
- [ ] Kinderfeuerwehr-Logo integrieren
- [ ] Schriften (Oswald, Inter) herunterladen + `@font-face` CSS
- [ ] Design-Tokens in `tailwind.config.js`
- [ ] Startseite: Hero mit Jubiläums-Badge, alle Sektionen
- [ ] Responsives Menü (Mobile Hamburger + Desktop)

### Phase 3 — Inhalt & Templates
- [ ] Alle Seitentypen implementieren
- [ ] Archetypes für Artikel, Termine und Galerie-Alben
- [ ] Galerie-Templates mit Thumbnail-Grid (Hugo `images.Resize`)
- [ ] Kontaktseite: Adresse + statisches OSM-Kartenbild + externer Map-Link
- [ ] Placeholder-Inhalte für alle Seiten
- [ ] Kontaktformular (fetch → Coolify Microservice)

### Phase 4 — Coolify Form-Service
- [ ] `form-service/`: Fastify + Nodemailer + Dockerfile
- [ ] Auf Coolify deployen + SMTP-Env-Vars setzen
- [ ] CORS auf GitHub Pages Domain beschränken
- [ ] Integrationstest: Formular → E-Mail

### Phase 5 — Compliance & Pflichtseiten
- [ ] `impressum.md` Vorlage mit Platzhaltern
- [ ] `datenschutz.md` DSGVO-konform
- [ ] Einwilligungsformular Erwachsene (DOCX + PDF in `static/dokumente/`)
- [ ] Einwilligungsformular Minderjährige (DOCX + PDF in `static/dokumente/`)
- [ ] Kein externer Tracking-Code

### Phase 6 — Dokumentation
- [ ] `README.md` — Pflege-Anleitung für alle Redakteure
- [ ] Beispiel-Artikel + Beispiel-Termin anlegen

---

## Verifikation

1. `hugo server` lokal — alle Seiten erreichbar, kein 404
2. Push auf `main` → GitHub Actions grün → Live-URL korrekt
3. Mobile-Test bei 375px — Navigation, Hero, Cards, Galerie-Grid
4. WCAG: Kontrast Rot/Weiß = 5.25:1 (erfüllt AA 4.5:1)
5. Impressum + Datenschutz in max. 2 Klicks von jeder Seite erreichbar
6. Fonts laden von `/fonts/` — nicht von `fonts.googleapis.com`
7. Kontaktformular: Testmail über Coolify-Service empfangen
8. Jubiläums-Badge sichtbar; `jubilaeum = false` → Badge verschwindet
9. Kontaktseite: Kartenbild lädt, OSM-Link öffnet korrekte Position
10. Galerie: Thumbnails werden von Hugo generiert (keine externen Bild-Dienste)
