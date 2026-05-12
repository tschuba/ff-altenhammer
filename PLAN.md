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
| Hosting | **GitHub Pages** | Kostenlos, HTTPS, Custom Domain `feuerwehr.altenhammer.bayern` |
| CI/CD | **GitHub Actions** (native actions) | Automatisches Build + Deploy auf Push zu `main` |
| Schriften | **Selbst-gehostet** (kein Google Fonts CDN) | DSGVO-Pflicht seit BGH-Urteil 2022 |
| Kontaktformular | **HeyForm** (selbst-gehostet, Coolify) | Kein Drittanbieter, kein Code, DSGVO-sauber |
| Kuchentheke-Buchung | **Easy!Appointments** (selbst-gehostet, Coolify) | Kalender + Buchungsanfrage ohne GitHub-Pflege |
| Nicht-technische Pflege | **GitHub Web Editor** | Markdown-Dateien direkt im Browser editieren |

---

## Formulare — HeyForm auf Coolify

Statt eines custom Microservices wird **HeyForm** (Open Source, selbst-gehostet) auf Coolify betrieben. HeyForm übernimmt das allgemeine Kontaktformular. Die Kuchentheke-Buchungsanfrage läuft separat über Easy!Appointments (eigener Abschnitt). Kein eigener Code nötig.

### Formulare im Überblick

| Formular | Felder | Benachrichtigung an |
| --- | --- | --- |
| Kontaktformular | Name, E-Mail, Nachricht | `ff-altenhammer@outlook.com` (im HeyForm-UI änderbar) |
| Spendenquittung-Anfrage | Vor-/Nachname, Straße, PLZ, Ort, E-Mail, Telefon (optional), Spendenbetrag, Datum der Überweisung, Verwendungszweck (optional) | `ff-altenhammer@outlook.com` (im HeyForm-UI änderbar) |

### Coolify-Deployment (HeyForm)

HeyForm benötigt: Node.js-App + MongoDB. Coolify stellt beides als Docker-Compose bereit.

1. Coolify → Neues Projekt → "Docker Compose" → HeyForm-Compose einfügen
2. MongoDB als Service im selben Compose-Stack
3. Subdomain `forms.feuerwehr.altenhammer.bayern` → HeyForm-UI
4. SMTP konfigurieren: `smtp-mail.outlook.com:587` + `ff-altenhammer@outlook.com`
5. Formulare in der HeyForm-UI anlegen, Embed-Link/iFrame für die Hugo-Seiten kopieren

### DNS-Eintrag

```text
forms.feuerwehr.altenhammer.bayern.  CNAME  schubs.net.
```

> Vollständige DNS-Tabelle s. Abschnitt "Custom Domain".

### Ablauf Kontaktformular (HeyForm)

```text
1. Besucher füllt Formular auf Hugo-Seite aus (iFrame von forms.feuerwehr.altenhammer.bayern)
2. HeyForm validiert Eingabe + prüft hCaptcha
3. HeyForm speichert Einsendung in MongoDB
4. HeyForm sendet E-Mail-Benachrichtigung an ff-altenhammer@outlook.com
5. HeyForm sendet Bestätigungsmail an Besucher
6. Wehr antwortet direkt per E-Mail (Reply-To = Absender-Adresse des Besuchers)
   — Alle Einsendungen auch im HeyForm-Admin-UI einsehbar
```

### Zugangsdaten & Absicherung (HeyForm)

| Maßnahme | Details |
| --- | --- |
| Admin-Login | E-Mail + sicheres Passwort — wird bei Ersteinrichtung gesetzt |
| HTTPS | Automatisch via Coolify + Let's Encrypt |
| Spam-Schutz | **hCaptcha** (DSGVO-freundlich, kein Google reCAPTCHA) — in HeyForm-UI aktivierbar |
| Brute-Force | Traefik Rate-Limiting-Middleware auf `/admin`-Pfad (s. Abschnitt "Server-Schutz & Isolation") |
| Admin-UI | Nur unter `forms.feuerwehr.altenhammer.bayern` erreichbar — optional mit HTTP Basic Auth als zweite Schicht absicherbar |

### DSGVO-Hinweis

HeyForm speichert Einsendungen in der MongoDB-Datenbank auf dem Coolify-Server (schubs.net). Da selbst-gehostet, verlassen die Daten nicht die eigene Infrastruktur — aber die Datenschutzerklärung muss erwähnen, dass Formulardaten serverseitig gespeichert werden (Rechtsgrundlage: Art. 6 Abs. 1 lit. b DSGVO — Vertragsanbahnung/berechtigtes Interesse).

### Sichtbarkeit der Empfängeradresse

Die Empfängeradresse (`ff-altenhammer@outlook.com`) ist ausschließlich im Backend der Tools konfiguriert — sie wird **nicht** im iFrame oder Buchungs-Widget an Besucher angezeigt.

> **⚠ Beim Setup beachten:** In HeyForm und Easy!Appointments gibt es Freitextfelder für Formularbeschreibungen. Die Empfängeradresse darf dort **nicht** eingetragen werden.

**Einzige unvermeidbare Sichtbarkeit:** Die Bestätigungsmail an den Besucher kommt FROM `ff-altenhammer@outlook.com` — Outlook erzwingt das. Der Besucher sieht die Adresse als Absender, wenn er die Eingangsbestätigung öffnet. Das ist technisch nicht lösbar ohne eigene Domain-Mail (s. Abschnitt "Absenderadresse").

**Auf der Website:** `ff-altenhammer@outlook.com` erscheint **nirgendwo** für Besucher — alle Formulare (Kontakt, Spendenquittung, Kuchentheke) laufen über iFrames, die Empfängeradresse liegt ausschließlich im Backend.

### Absenderadresse bei ausgehenden E-Mails

Der **Display-Name** ist in beiden Tools frei einstellbar — empfohlen:
`Freiwillige Feuerwehr Altenhammer <ff-altenhammer@outlook.com>`

Die technische Absenderadresse muss identisch mit dem SMTP-Konto sein — Outlook erzwingt das. `ff-altenhammer@outlook.com` erscheint also immer als echte Absenderadresse.

> **Langfristig:** Für eine eigene Adresse wie `info@feuerwehr.altenhammer.bayern` wäre ein Mailprovider mit Custom-Domain-Support nötig (z.B. Microsoft 365 ~5 €/Monat oder ein Hoster wie Strato/IONOS mit der Domain). Aktuell kein Handlungsbedarf — Display-Name-Lösung ist für Besucher vollkommen ausreichend.

### Branding — HeyForm & Easy!Appointments

Beide Tools werden als iFrame in die Hugo-Seite eingebettet. Die CSS-Stile der Hugo-Seite greifen nicht ins iFrame — Branding muss in den jeweiligen Admin-UIs konfiguriert werden.

| Einstellung | HeyForm | Easy!Appointments |
| --- | --- | --- |
| Primärfarbe | `#CC0000` — im Admin-UI einstellbar | `#CC0000` — Farbschema-Einstellung |
| Logo | Hinterlegbar | Hinterlegbar |
| Schriften (Oswald/Inter) | Nicht ohne Eingriff in Quelldateien | Nicht ohne Eingriff in Quelldateien |
| Hintergrundfarbe | Konfigurierbar | Begrenzt |

> Für ein ehrenamtliches Vereinsprojekt ist farbliche Anpassung ausreichend. Pixel-perfekte Typografie-Anpassung (Oswald/Inter) wäre nur mit Eingriff in die Tool-Quelldateien auf dem Server möglich — unverhältnismäßiger Aufwand.

### CC / BCC bei Benachrichtigungen

Recherchiert am 2026-05-12 anhand der Quellcodes beider Tools:

| | HeyForm | Easy!Appointments |
| --- | --- | --- |
| Natives CC/BCC | ❌ Nicht vorhanden | ❌ Nicht vorhanden |
| Mehrere Empfänger | ❌ Nur eine Adresse konfigurierbar | ⚠️ Ja — aber als separate E-Mails (Admin + Sekretärin-Rolle) |

Alle verfügbaren Optionen nach aufsteigendem Aufwand:

**Option A — Easy!Appointments: Sekretärin-Rolle (kein Code, nur Kuchentheke)**
Die eingebaute Sekretärin-Rolle kann als zweiter Admin-Empfänger angelegt werden. Beide bekommen separate E-Mails mit identischem Inhalt. Einrichtung im Easy!Appointments Admin-UI, ~2 Minuten.

**Option B — Outlook-Regel nach Betreff (kein Code, beide Tools)**
Da alle E-Mails von `ff-altenhammer@outlook.com` kommen, muss nach Betreff gefiltert werden. Beim Setup eindeutige Präfixe konfigurieren:

```text
Wenn Betreff enthält "[FF-Kontakt]"        → Kopie an [weitere Adresse]
Wenn Betreff enthält "[FF-Kuchentheke]"    → Kopie an [weitere Adresse]
Wenn Betreff enthält "[FF-Spendenquittung]" → Kopie an [weitere Adresse]
```

**Option C — Outlook: alle E-Mails automatisch weiterleiten (kein Code, beide Tools)**
In Outlook.com → Einstellungen → Weiterleitung: alle eingehenden E-Mails pauschal an eine zweite Adresse weiterleiten. Einfachste Einrichtung, aber unspezifisch — alle Mails werden weitergeleitet, nicht nur Formular-Benachrichtigungen.

**Option D — Easy!Appointments: 1-Zeile Code-Änderung (minimaler Eingriff, nur Kuchentheke)**
PHPMailer ist bereits integriert und unterstützt CC/BCC nativ. In `/application/libraries/Email_messages.php` eine Zeile ergänzen:

```php
$mail->addCC('weitere@adresse.de');
```

Einmalige Serveränderung, kein Redeploy nötig — aber bei Tool-Updates ggf. neu anwenden.

---

## Benachrichtigungen — Push & Messaging

E-Mail allein ist für zeitkritische Benachrichtigungen unzuverlässig (Junk-Filter, zu spätes Lesen). Die Lösung ist eine zweistufige Infrastruktur auf Coolify — alle Dienste kostenlos und selbst-gehostet.

### Übersicht der Dienste

```text
HeyForm (Webhook)       ──┐
                           ├──▶  n8n (Coolify)  ──▶  ntfy (Coolify)       ──▶  Push-App
Easy!Appointments (Hook)──┘          │
                                     └──▶  Matrix/Conduit (Coolify)  ──▶  Element-App
                                                      │
                                            mautrix-whatsapp  ──▶  WhatsApp-Nummern
```

### Stufe 1 — ntfy (sofort einsetzbar, minimal)

ntfy ist ein ultrakleiner Push-Notification-Server (~10 MB, kein Login nötig).

| | Details |
| --- | --- |
| Deployment | Docker-Container auf Coolify |
| Subdomain | `push.feuerwehr.altenhammer.bayern` |
| Empfänger-Setup | ntfy-App (iOS/Android) installieren, privaten Kanal abonnieren — fertig |
| Mehrere Empfänger | Beliebig viele — alle Abonnenten des Kanals erhalten die Nachricht |
| Datenschutz | Vollständig selbst-gehostet, kein Drittanbieter |

**n8n als Verbindungsschicht** (ebenfalls auf Coolify):

```text
HeyForm Webhook → n8n → ntfy: "Neue Kontaktanfrage von [Name]"
HeyForm Webhook → n8n → ntfy: "Spendenquittung angefragt von [Name]"
Easy!Appointments (neue Buchung)   → n8n → ntfy: "Kuchentheke-Anfrage: [Datum]"
Easy!Appointments (Stornierung)    → n8n → ntfy: "Stornierungsanfrage: [Datum]"
```

Zusätzliche DNS-Einträge (s. auch zentrale Tabelle im Abschnitt "Custom Domain"):

```text
push.feuerwehr.altenhammer.bayern.  CNAME  schubs.net.
n8n.feuerwehr.altenhammer.bayern.   CNAME  schubs.net.
```

### Stufe 2 — Matrix/Conduit + WhatsApp-Bridge (optional)

Für Mitglieder, die lieber WhatsApp nutzen als eine neue App zu installieren.

**Conduit** ist ein schlanker Matrix-Server in Rust — deutlich leichter als Synapse.

| Komponente | Details |
| --- | --- |
| Conduit | Matrix-Server auf Coolify, Subdomain `matrix.feuerwehr.altenhammer.bayern` |
| Element-App | Client für iOS/Android/Web — wer Element bevorzugt |
| mautrix-whatsapp | Ein Telefon wird als Sender gekoppelt (wie WhatsApp Web) |
| Empfang | Nachrichten kommen auf bestehenden WhatsApp-Nummern an — keine neue App nötig |

> **Hinweis:** mautrix-whatsapp nutzt das WhatsApp-Web-Protokoll. Bei wenigen Nachrichten pro Woche ist das Sperrrisiko sehr gering. Eine eigene Nummer/ein eigenes Gerät als Sender empfohlen.

Zusätzlicher DNS-Eintrag (s. auch zentrale Tabelle im Abschnitt "Custom Domain"):

```text
matrix.feuerwehr.altenhammer.bayern.  CNAME  schubs.net.
```

### Empfohlene Reihenfolge

1. **Zuerst ntfy + n8n** einrichten — läuft in ~30 Minuten, sofortiger Mehrwert
2. **Matrix + WhatsApp-Bridge** als optionaler zweiter Schritt, wenn WhatsApp-Integration gewünscht

---

## Server-Schutz & Isolation (Coolify)

### Multi-Domain auf einer Maschine

Coolify/Traefik routet anhand des HTTP-`Host`-Headers. Mehrere Domains auf derselben IP funktionieren nativ — kein zweites Coolify, kein zweiter Server nötig.

```text
DNS: forms.feuerwehr.altenhammer.bayern.  CNAME  schubs.net.
     (→ löst auf dieselbe IP wie schubs.net)

Eingehende Requests:
  Host: schubs.net                    → Traefik → private Dienste
  Host: forms.feuerwehr.altenhammer.bayern   → Traefik → HeyForm
  Host: buchung.feuerwehr.altenhammer.bayern → Traefik → Easy!Appointments
  Host: push.feuerwehr.altenhammer.bayern    → Traefik → ntfy
```

Let's Encrypt stellt pro Hostname automatisch ein eigenes TLS-Zertifikat aus — kein manueller Eingriff nötig. Bestehende `schubs.net`-Dienste sind davon nicht betroffen.

**Coolify-Konfiguration:** Beim Anlegen eines neuen Dienstes im FF-Projekt einfach die gewünschte Subdomain (z.B. `forms.feuerwehr.altenhammer.bayern`) als "Domain" eintragen — Traefik und Let's Encrypt erledigen den Rest automatisch.

### Projekt-Isolation: FF Altenhammer vs. private Dienste

Alle FF-Dienste laufen in einem **eigenen Coolify-Projekt** — getrennt von privaten Services.

| Was | Warum wichtig |
| --- | --- |
| Separate Secrets & Env-Variablen | SMTP-Passwort, Datenbank-Credentials der FF nicht neben privaten Keys sichtbar |
| Eigene Docker-Netzwerke | FF-Container sprechen nicht mit privaten Containern |
| Separate Ressourcen-Überwachung | CPU/RAM-Verbrauch der FF-Dienste klar ablesbar |
| Unabhängige Backups | FF-Datenbanken lassen sich separat sichern/löschen |

**Empfohlene Coolify-Struktur:**

```text
Coolify
├── Projekt: "FF Altenhammer"
│   ├── HeyForm + MongoDB
│   ├── Easy!Appointments + MySQL
│   ├── n8n
│   ├── ntfy
│   └── Matrix/Conduit + mautrix-whatsapp (optional)
└── Projekt: "Private" (bestehend)
    └── ... bestehende private Dienste
```

> Coolify-Projekte teilen sich denselben Docker-Host, sind aber auf Netzwerk- und Verwaltungsebene getrennt. Für maximale Isolation wäre eine eigene VM nötig — für diesen Use-Case unnötig.

### Rate Limiting via Traefik

Traefik hat eine native Rate-Limiting-Middleware — per Service als Label konfiguriert, kein Extra-Dienst.

| Endpunkt | Limit | Begründung |
| --- | --- | --- |
| HeyForm (Formular-Submit) | 10 Req/min pro IP | Normale Nutzung: 1–2 Einsendungen pro Besuch |
| Easy!Appointments (Buchungs-Submit) | 10 Req/min pro IP | Selten mehr als 1–2 Anfragen pro Besucher |
| Admin-Login-Endpunkte | 5 Req/min pro IP | Brute-Force-Schutz |

**Coolify v4 — Zweistufiger Ansatz:**

**Schritt 1 — Middleware definieren** via *Server → Proxy → Dynamic Configurations → "+ Add"*:

Dateiname z.B. `ff-ratelimit.yaml`, Inhalt:

```yaml
http:
  middlewares:
    heyform-rl:
      rateLimit:
        average: 10
        burst: 20
        period: 1m
    easyapp-rl:
      rateLimit:
        average: 10
        burst: 20
        period: 1m
```

Diese Datei liegt serverseitig in `/data/coolify/proxy/dynamic/` und wird von Traefik automatisch geladen — kein Neustart nötig.

**Schritt 2 — Middleware einem Service zuweisen** über Custom Labels im Service (Application → Labels):

```yaml
traefik.http.routers.<coolify-router-name>.middlewares=heyform-rl@file
```

> **⚠ Router-Name beim Setup ermitteln:** Coolify generiert Traefik-Router-Namen automatisch (UUID-basiert). Den korrekten Namen im Traefik-Dashboard → "HTTP" → "Routers" nachschlagen — dort nach der konfigurierten Domain filtern.
>
> Der Suffix `@file` (nicht `@docker`) verweist auf die Dynamic-Config-Datei aus Schritt 1.

### Docker-Ressourcenlimits

Jeden Container in Coolify mit Obergrenzen belegen, damit ein angegriffener Dienst nicht den gesamten Server destabilisiert (Coolify → Service → Resources → Limits).

| Dienst | CPU-Limit | RAM-Limit |
| --- | --- | --- |
| HeyForm | 0.5 Core | 512 MB |
| MongoDB (HeyForm) | 0.5 Core | 256 MB |
| Easy!Appointments | 0.5 Core | 256 MB |
| MySQL (Easy!Appointments) | 0.5 Core | 256 MB |
| n8n | 0.5 Core | 256 MB |
| ntfy | 0.1 Core | 64 MB |

### Mehrstufiges Schutzkonzept im Überblick

```text
Schicht 1 — Traefik Rate Limit         HTTP-Flut abgewiesen, bevor der Container antwortet
Schicht 2 — hCaptcha (HeyForm)         Bot-Formular-Spam blockiert
Schicht 3 — Manuelle Bestätigung       Easy!Appointments-Spam landet nur als "ausstehend"
Schicht 4 — Docker-Ressourcenlimits    Kein Container kann den ganzen Server überlasten
Schicht 5 — Coolify-Projekttrennung    Private Dienste bleiben vom FF-Traffic unberührt
```

---

## Branding & Design (Brand Guardian + UI Designer)

### Kernbotschaft & Identität

Die Homepage ist kein Nachrichtenkanal — das übernimmt Social Media. Die Homepage ist die **Anlaufstelle für Menschen, die mehr wissen wollen**: Wer seid ihr? Was macht ihr? Wie kann ich mitmachen, unterstützen, spenden?

**Die wichtigste emotionale Botschaft** — muss auf der Startseite sichtbar sein:

> Wir sind ganz normale Menschen aus Altenhammer, die ihre Freizeit freiwillig dafür einsetzen, unsere Gemeinde sicherer zu machen. Keine Profis — engagierte Nachbarn.

Diese Botschaft macht Mitmachen und Spenden greifbar: Man unterstützt keine anonyme Institution, sondern konkrete Nachbarn.

### Brand Foundation

- **Name:** Freiwillige Feuerwehr Altenhammer / FF Altenhammer
- **Jubiläumslinie:** "100 Jahre im Dienst der Gemeinschaft — 1926–2026"
- **Werte:** Gemeinschaft · Sicherheit · Einsatzbereitschaft · Tradition
- **Ton:** Professionell, warm, bodenständig — kein Behördendeutsch, keine Distanz

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
| Jubiläums-Logo 100 Jahre | **Vorhanden** (SVG, bereitstellen) | Hero-Badge, Jubiläumsseite, Jubiläumsteaser |

**Hauptlogo-Konzept:** Stilisiertes Feuerwehrkreuz (Malteser-Stil) in Rot + "FF Altenhammer" in Oswald Bold. Varianten: Farbe (für hellen Hintergrund) + Weiß (für roten Header).

### Jubiläums-Branding

Gold-Akzent `#F0A500` für alle Jubiläumselemente. Das **bestehende Jubiläums-SVG-Logo** wird direkt in Hero-Badge, Jubiläumsteaser (Startseite) und der dedizierten `/jubilaeum/`-Seite eingebunden — kein CSS-only-Badge nötig. Separater Bereich auf der Startseite.

### Social Media Icons — Header (prominent, dauerhaft sichtbar)

Facebook · Instagram · WhatsApp — als **SVG-Icon-Buttons oben rechts im Header**, auf jeder Seite sichtbar.

```text
┌─────────────────────────────────────────────────────────┐
│  [Logo] FF Altenhammer    Termine  Über uns  …   f  📷  w │
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
├── Termine (/termine/)                   ← Einfache statische Liste, manuell gepflegt
├── 100 Jahre (/jubilaeum/)               ← Jubiläumsseite 2026
├── Über uns (/ueber-uns/)
│   ├── Mannschaft (/ueber-uns/mannschaft/)   ← Mit Foto pro Person (optional)
│   ├── Verein (/ueber-uns/verein/)           ← Förderverein
│   └── Geschichte (/ueber-uns/geschichte/)
├── Kinderfeuerwehr (/kinderfeuerwehr/)   ← Mit unterstützenden Fotos
│   └── Mitmachen (/kinderfeuerwehr/mitmachen/)
├── Fahrzeuge & Ausrüstung (/fahrzeuge/) ← Mit unterstützenden Fotos
├── Kuchentheke Verleih (/kuchentheke/)  ← Beschreibung, Verfügbarkeitskalender, Anfrage
├── Mitmachen (/mitmachen/)              ← Aktiv + Passiv erklärt, Mitgliederzahlen, QR-Code
├── Spenden (/spenden/)                  ← IBAN, Verwendungszweck, GiroCode-QR
├── Kontakt (/kontakt/)                  ← Adresse + Feuerwehrhaus-Standort
├── Impressum (/impressum/)              ⚠ GESETZESPFLICHT
└── Datenschutz (/datenschutz/)          ⚠ GESETZESPFLICHT
```

**Keine Aktuelles-/Artikel-Sektion, keine Galerie** — Aktuelles läuft über Social Media. Fotos werden seitenspezifisch als Unterstützung eingebunden (Mannschaft, Kinderfeuerwehr, Fahrzeuge), nicht als fortlaufendes Album.

### Startseiten-Aufbau (Hero → Sections)

1. **Hero** — Logo, Slogan, Jubiläums-Badge, zwei CTAs: "Mitmachen" + "Über uns"
2. **Jubiläums-Teaser** — Goldener Akzentbereich, Einladung zur Jubiläumsseite
3. **Wer wir sind** — Kurzer, menschlicher Text: normale Dorfbürger, die ihre Freizeit der Feuerwehr widmen. Warum wir das tun. Ehrenamt als Stärke, nicht als Bürde. 2–3 Sätze + Bild.
4. **Was wir tun** — Einsatz, Ausbildung, Gemeinschaft — knapp, mit 2–3 unterstützenden Fotos
5. **Nächste Termine** — Einfache Liste der 3 nächsten Einträge aus `termine/` (statisch gepflegt)
6. **Kinderfeuerwehr-Teaser** — Eigenes Logo + Einladung
7. **Kuchentheke-Teaser** — Kurzer Hinweis "Kuchentheke vermieten? Jetzt Verfügbarkeit prüfen", Link zur Kuchentheke-Seite
8. **Mitmachen-Teaser** — Aktiv/Passiv in zwei Kacheln, Mitgliederzahlen
9. **Social Media** — Auffälliger Banner: "Alles Aktuelle findet ihr auf Facebook und Instagram" + große Icons
10. **Footer** — Logo, Navigation, Kontakt, Impressum/Datenschutz

---

## Kontaktseite — Feuerwehrhaus-Standort

Die Kontaktseite enthält Adresse, Kontaktdaten, den **Standort des Feuerwehrhauses** und das eingebettete HeyForm-Kontaktformular.

**Karte:** Statisches OpenStreetMap-Screenshot-Bild + "Auf der Karte anzeigen"-Button → öffnet OpenStreetMap im neuen Tab. Kein Tracking, keine Cookies, kein Wartungsaufwand.

**Kontaktformular:** HeyForm-iFrame eingebettet (`forms.feuerwehr.altenhammer.bayern`). Felder: Name, E-Mail, Nachricht.

---

## Fotos — seitenspezifisch, kein Galerie-System

Es gibt keine dedizierte Galerie oder ein Album-System. Fotos dienen ausschließlich als unterstützende Illustration auf den jeweiligen Seiten. Aktuelles Bildmaterial läuft über Social Media.

**Wo Fotos verwendet werden:**

| Seite | Foto-Verwendung |
| --- | --- |
| Startseite Hero | 1 Hintergrundbild oder Feuerwehrmotiv |
| Startseite "Was wir tun" | 2–3 Actionfotos nebeneinander |
| Mannschaft | Optional 1 Foto pro Person (Porträt) |
| Kinderfeuerwehr | 1–2 Gruppenfotos |
| Fahrzeuge & Ausrüstung | 1 Foto pro Fahrzeug/Gerät |
| Jubiläumsseite | Historische Fotos (Archiv) |
| Kuchentheke | 1–2 Produktfotos |

**Technisch:** Bilder liegen als Page Resources direkt beim jeweiligen Content (`content/ueber-uns/mannschaft/bild.jpg`). Hugo skaliert sie beim Build automatisch — kein externes Bild-Service, kein Album-Ordner-System.

**Pflege:** Selten nötig. Fotos auf diesen Seiten ändern sich kaum — Mannschaftsfoto vielleicht alle 2–3 Jahre, Fahrzeugfotos bei Neuanschaffungen.

---

## Termine (`/termine/`)

Termine werden als einzelne Markdown-Dateien in `content/termine/` gepflegt — jede Datei ein Termin. Das Hugo-Template filtert automatisch alle Termine heraus, die mehr als 14 Tage zurückliegen. Ein **täglicher Rebuild** via GitHub Actions sorgt dafür, dass abgelaufene Termine jeden Tag neu verschwinden — kein manuelles Löschen nötig.

### Frontmatter eines Termins

```yaml
---
title: "Jahreshauptversammlung"
date: 2026-06-15T19:00:00
ort: "Feuerwehrhaus Altenhammer"
---
Kurze optionale Beschreibung.
```

### Hugo-Template-Filterlogik

```go
{{/* Nur Termine anzeigen, die weniger als 14 Tage zurückliegen */}}
{{ $cutoff := now.AddDate 0 0 -14 }}
{{ range where .Pages "Date" "gt" $cutoff }}
  ...
{{ end }}
```

### Automatischer täglicher Rebuild (GitHub Actions)

```yaml
on:
  push:
    branches: [main]
  schedule:
    - cron: "0 4 * * *"   # täglich 04:00 Uhr UTC → abgelaufene Termine verschwinden
  workflow_dispatch:
```

### Hinweis auf der Terminseite

Unterhalb der Terminliste steht sichtbar:

> Für kurzfristige Änderungen und aktuelle Infos folgt uns auf [Facebook] und [Instagram] — dort sind wir am schnellsten.

### Pflege

Neuen Termin anlegen: GitHub Web Editor → `content/termine/` → neue Datei `2026-06-15-jahreshauptversammlung.md` → Frontmatter ausfüllen → speichern. Aufwand: ~2 Minuten. Löschen: nie nötig — Termine verschwinden automatisch.

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

Die **Über uns**-Sektion trennt zwar strukturell zwischen Wehr und Verein, betont aber ausdrücklich die enge Verzahnung:

- **Aktive Wehr** — Einsatzabteilung, Mannschaft, Führung
- **Feuerwehrverein** — Zweck (Förderung der Wehr), Vorstand, Mitgliedschaft, Satzung (PDF-Link)
- **Kinderfeuerwehr** — eigene Sektion (s. Sitemap)

**Kernbotschaft auf der Vereinsseite:** Verein und aktive Wehr arbeiten Hand in Hand — aktive Feuerwehrmitglieder sitzen im Vereinsvorstand. Kein "Wir vs. Die", sondern eine Gemeinschaft mit zwei organisatorischen Säulen. Diese Botschaft soll im Einleitungstext der Vereinsseite und im "Über uns"-Überblick sichtbar sein.

---

## Kuchentheke Verleih (`/kuchentheke/`)

Die Feuerwehr verleiht eine Kuchentheke. Die Seite zeigt Beschreibung, Fotos, Konditionen, einen Verfügbarkeitskalender und ein Anfrage-Formular.

### Verfügbarkeit & Buchungsanfragen — Easy!Appointments auf Coolify

Die Verfügbarkeit und Buchungsanfragen werden über **Easy!Appointments** verwaltet — ein selbst-gehostetes Open-Source-Buchungssystem. Die Person, die heute die Papierliste führt, pflegt stattdessen im Browser-UI von Easy!Appointments.

**Kein GitHub, kein Markdown, kein technisches Wissen nötig.**

#### Coolify-Deployment (Easy!Appointments)

Easy!Appointments läuft als Docker-Container mit MySQL auf Coolify.

```text
buchung.feuerwehr.altenhammer.bayern  →  Easy!Appointments (Coolify)
                                            ├── Admin-UI (Wehr)
                                            └── Buchungs-Widget (eingebettet in Hugo)
```

DNS-Eintrag:

```text
buchung.feuerwehr.altenhammer.bayern.  CNAME  schubs.net.
```

> Vollständige DNS-Tabelle s. Abschnitt "Custom Domain".

#### Konfiguration in Easy!Appointments

| Einstellung | Wert |
| --- | --- |
| Service | "Kuchentheke Verleih" |
| Dauer | Ganztägig (oder 1–3 Tage je Buchung) |
| Bestätigung | **Manuell** — Admin muss Anfrage bestätigen (kein Sofort-Buchen) |
| E-Mail-Benachrichtigung | Bei neuer Anfrage → `ff-altenhammer@outlook.com` (jederzeit im Admin-UI änderbar, kein Redeploy) |
| Bestätigungs-Mail | Automatisch an Anfragenden: "Ihre Anfrage ist eingegangen. Dies ist **keine** Buchungsbestätigung." |
| Stornierung | Automatischer Stornierungslink **deaktiviert** — Stornierungen laufen über das HeyForm-Kontaktformular (s.u.) |

#### Hugo-Integration

Das Easy!Appointments Buchungs-Widget wird als iFrame in `content/kuchentheke.md` eingebettet. Besucher sehen direkt auf der Seite, welche Tage verfügbar sind, und können eine Anfrage stellen — ohne die Seite zu verlassen.

#### Ablauf Kuchentheke-Anfrage (Easy!Appointments)

```text
1. Besucher wählt Wunschtermin im Widget auf der Hugo-Seite
2. Besucher gibt Name, E-Mail, Telefon ein → sendet Anfrage
3. Easy!Appointments speichert Anfrage als "Ausstehend"
4. Easy!Appointments sendet Benachrichtigung an ff-altenhammer@outlook.com
5. Easy!Appointments sendet Eingangsbestätigung an Besucher:
   "Ihre Anfrage ist eingegangen. Dies ist keine Buchungsbestätigung."
6. Admin öffnet Easy!Appointments im Browser → sieht ausstehende Anfrage
7. Admin bestätigt oder lehnt ab
8. Easy!Appointments sendet automatisch Bestätigung/Absage an Besucher
9. Bestätigte Buchung erscheint im Kalender als belegt — für alle sichtbar
```

#### Zugangsdaten & Absicherung (Easy!Appointments)

| Maßnahme | Details |
| --- | --- |
| Admin-Login | E-Mail + sicheres Passwort — wird bei Ersteinrichtung gesetzt |
| HTTPS | Automatisch via Coolify + Let's Encrypt |
| Spam-Schutz | Manuelle Bestätigung nötig — unerwünschte Anfragen werden einfach abgelehnt, erscheinen nie als "belegt" |
| CSRF-Schutz | In Easy!Appointments eingebaut |
| Admin-UI | Nur unter `buchung.feuerwehr.altenhammer.bayern` — optional mit HTTP Basic Auth als zweite Schicht |
| SMTP | Gleiche Outlook-Konfiguration wie HeyForm — in Easy!Appointments Admin-UI hinterlegt, nicht im Code |

#### Admin-Workflow (Papierliste → Browser)

1. Neue Anfrage kommt per E-Mail + Easy!Appointments-Benachrichtigung
2. Admin öffnet Easy!Appointments im Browser, prüft den Kalender
3. Bestätigt oder lehnt ab → Interessent bekommt automatisch eine E-Mail
4. Bestätigte Buchung erscheint im Kalender als belegt — für alle sichtbar

### Stornierungsprozess

Alle Stornierungen laufen über das **HeyForm-Kontaktformular** — keine privaten Kontaktdaten nötig, kein separater Formular-Aufwand.

**Außerhalb der Stornofrist:**
Anfrage über Kontaktformular → Wehr storniert im Easy!Appointments-Backend → manuelle Bestätigungsmail an Anfrager.

**Innerhalb der Stornofrist:**
Anfrage über Kontaktformular → Wehr prüft Einzelfall manuell → Entscheidung per E-Mail. Kein automatisches Recht auf Stornierung, aber kulanzbasierte Prüfung.

> **⚠ Stornofrist noch offen** — muss von der Wehr intern definiert werden (z.B. 7 oder 14 Tage). Platzhalter `[X Tage]` in den Buchungsbedingungen bis zur Entscheidung.

### Buchungsbedingungen (auf der Kuchentheke-Seite)

Unterhalb des Easy!Appointments-Widgets werden die Konditionen klar sichtbar angezeigt:

```text
Buchungsbedingungen

– Die Kuchentheke wird nach Eingang Ihrer Anfrage manuell geprüft.
  Sie erhalten eine Bestätigung per E-Mail.
– Diese Bestätigung ist bindend — erst dann ist die Buchung gültig.
– Stornierung: Kostenlos bis [X] Tage vor Verleihbeginn über
  unser Kontaktformular.
– Bei kurzfristiger Stornierung (weniger als [X] Tage) entscheidet
  die Wehr im Einzelfall.
```

### Startseiten-Teaser

Ein kleiner Teaser-Block auf der Startseite verweist auf die Kuchentheke-Seite.

---

## Spenden (`/spenden/`)

Der Verein finanziert sich u.a. über Spenden. Die Seite erklärt den Zweck der Spende und macht es so einfach wie möglich.

### Seiteninhalt

- Kurztext: Wofür die Spende verwendet wird (Ausrüstung, Jugendarbeit, Vereinsleben)
- **SEPA-Überweisung:** IBAN + BIC + Vereinsname + empfohlener Verwendungszweck — als Copytext zum Kopieren
- **GiroCode-QR:** Statisch generiertes QR-Bild (EPC-Standard), das jede deutsche Banking-App direkt mit den Bankdaten vorausfüllt
- **Spendenquittung:** Expliziter Abschnitt auf der Seite (s.u.)

### GiroCode-QR — Technische Umsetzung

Der GiroCode (EPC QR Code) ist ein offener Standard — kein Drittanbieter, keine externe API, vollständig DSGVO-sauber.

**Generierung:** Einmalig mit einem freien Node.js-Skript (`epc-qr` + `qrcode` NPM-Pakete) oder einem Offline-Generator → Ausgabe als statisches SVG/PNG → liegt in `assets/images/spenden-qrcode.svg`.

```text
GiroCode enthält:
  BCD       (Service Tag)
  002       (Version)
  1         (Encoding: UTF-8)
  SCT       (SEPA Credit Transfer)
  BIC       (Vereinsbank-BIC)          ← Platzhalter, wird eingetragen
  Vereinsname
  IBAN                                  ← Platzhalter, wird eingetragen
  EUR                                   (Betrag leer — Spender wählt selbst)
  Verwendungszweck: "Spende FF Altenhammer"
```

### Spendenquittung

Auf der Spendenseite wird ein eigener Abschnitt "Spendenquittung" angezeigt:

```text
Spendenquittung

Bis 300 €: Ihr Kontoauszug gilt als vereinfachter Zuwendungsnachweis
           gegenüber dem Finanzamt — keine gesonderte Quittung nötig.

Ab 300 €:  Wir stellen Ihnen gerne eine offizielle Zuwendungsbestätigung aus.
           Bitte füllen Sie nach Ihrer Überweisung das folgende Formular aus:

           [Spendenquittung anfordern →]   ← HeyForm-Formular (iFrame)
```

Das HeyForm-Formular für die Spendenquittungs-Anfrage ist direkt auf der Spendenseite eingebettet — die E-Mail-Adresse der Wehr ist für Besucher nicht sichtbar.

> **⚠ Voraussetzung:** Dieser Abschnitt setzt voraus, dass der Feuerwehrverein als **gemeinnützig anerkannt** ist (Freistellungsbescheid vom Finanzamt). Falls nicht, muss der Text angepasst werden. Bitte vor Livegang prüfen.
>
> **⚠ IBAN noch unbekannt** — wird nachgetragen sobald die Vereins-IBAN vorliegt. Dann QR neu generieren und `assets/images/spenden-qrcode.svg` ersetzen.

### QR-Codes — Übersicht aller drei Einsatzfälle

| Seite | QR-Ziel | Verwendung |
| --- | --- | --- |
| `/spenden/` | GiroCode (IBAN/SEPA) | Direkt auf der Seite + Download für Druckmaterial |
| `/kuchentheke/` | `https://feuerwehr.altenhammer.bayern/kuchentheke/` | Download-Button "QR-Code für Flyer" |
| `/mitmachen/` | `https://feuerwehr.altenhammer.bayern/mitmachen/` | Download-Button "QR-Code für Aushang" |

Die URL-QR-Codes (Kuchentheke, Mitmachen) werden **clientseitig im Browser gerendert** — das Hugo-Template bindet einen selbst-gehosteten QR-Generator (vanilla JS, ~5 KB) ein, der den QR-Code inline darstellt und als PNG-Download anbietet. Kein Build-Schritt, kein externe Abhängigkeit.

---

## Repository-Struktur

```text
ff-altenhammer/                        ← Hugo-Seite
├── .github/
│   └── workflows/
│       └── deploy.yml
├── archetypes/
│   ├── default.md
│   └── termine.md                     ← Vorausgefülltes Frontmatter für neue Termine
├── assets/
│   ├── css/
│   │   └── main.css
│   ├── images/
│   │   ├── logo.svg                   ← Hauptlogo (Farbe, neu erstellt)
│   │   ├── logo-white.svg             ← Hauptlogo Weiß
│   │   ├── kf-logo.svg                ← Kinderfeuerwehr-Logo (bereitgestellt)
│   │   ├── jubilaeum-logo.svg         ← 100-Jahre-Jubiläumslogo (vorhanden, bereitgestellt)
│   │   ├── feuerwehrhaus-karte.png    ← Statischer OSM-Screenshot
│   │   └── spenden-qrcode.svg         ← GiroCode QR (einmalig generiert, bei IBAN-Änderung ersetzen)
│   └── js/
│       └── main.js
├── content/
│   ├── _index.md
│   ├── termine/                       ← Je eine .md-Datei pro Termin
│   │   └── YYYY-MM-DD-titel.md
│   ├── jubilaeum/
│   │   └── _index.md
│   ├── ueber-uns/
│   │   ├── _index.md
│   │   ├── mannschaft/                ← Page Bundle: _index.md + Personenfotos
│   │   │   ├── _index.md
│   │   │   └── *.jpg
│   │   ├── verein.md
│   │   └── geschichte.md
│   ├── kinderfeuerwehr/
│   │   ├── _index.md                  ← Mit unterstützenden Fotos als Page Resources
│   │   ├── mitmachen.md               ← Mitmachen bei der Kinderfeuerwehr
│   │   └── *.jpg
│   ├── fahrzeuge/
│   │   ├── _index.md                  ← Mit Fahrzeugfotos als Page Resources
│   │   └── *.jpg
│   ├── kuchentheke.md
│   ├── mitmachen.md
│   ├── spenden.md
│   ├── kontakt.md
│   ├── impressum.md
│   └── datenschutz.md
├── layouts/
│   ├── _default/
│   │   ├── baseof.html
│   │   ├── list.html
│   │   └── single.html
│   ├── index.html
│   └── partials/
│       ├── head.html
│       ├── header.html
│       ├── footer.html
│       ├── hero.html
│       ├── jubilaeum-banner.html
│       ├── termine-liste.html
│       └── social-banner.html
├── static/
│   ├── fonts/
│   ├── dokumente/                     ← Einwilligungsformulare (PDF/DOCX)
│   └── CNAME
├── package.json
├── tailwind.config.js
├── postcss.config.js
├── hugo.toml
└── README.md

```

---

## Content-Typen & Frontmatter

### Termin (termine/)

Frontmatter-Schema s. Abschnitt [Termine](#termine-termine). Entspricht dem Archetype `archetypes/termine.md` — Hugo füllt Datum automatisch vor.

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
  schedule:
    - cron: "0 4 * * *"   # täglich 04:00 UTC — abgelaufene Termine verschwinden automatisch
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
      - id: pages
        uses: actions/configure-pages@v5
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

Nicht-technischer Redakteur (neuer Termin):
  github.com → Repository → content/termine/ → ✏ Neue Datei anlegen
  → Frontmatter ausfüllen (Titel, Datum, Ort) → "Commit changes" → Live (~90s)

Mitgliederzahlen aktualisieren:
  hugo.toml → aktiveMitglieder / foerdermitglieder ändern → commit → Live
```

---

## ⚠ Wichtige Probleme & Einschränkungen

### Gesetzlich verpflichtend (Deutschland)

1. **Impressum (TMG §5):** Vollständige Adresse, Name des Verantwortlichen, Kontakt. Abmahnrisiko + bis zu 50.000 € Bußgeld bei Fehlen.
2. **Datenschutzerklärung (DSGVO):** Folgendes muss erwähnt werden: GitHub Pages Server-Logs; HeyForm speichert Kontaktformular-Einsendungen in MongoDB auf schubs.net; Easy!Appointments speichert Buchungsanfragen in MySQL auf schubs.net; n8n leitet Formulardaten intern weiter (kein Drittanbieter, schubs.net). Rechtsgrundlage jeweils Art. 6 Abs. 1 lit. b DSGVO.
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

### Custom Domain — `feuerwehr.altenhammer.bayern`

**DNS-Einträge (beim Domain-Registrar eintragen):**

```text
feuerwehr.altenhammer.bayern.          A      185.199.108.153
feuerwehr.altenhammer.bayern.          A      185.199.109.153
feuerwehr.altenhammer.bayern.          A      185.199.110.153
feuerwehr.altenhammer.bayern.          A      185.199.111.153
www.feuerwehr.altenhammer.bayern.      CNAME  <github-username>.github.io.
forms.feuerwehr.altenhammer.bayern.    CNAME  schubs.net.
buchung.feuerwehr.altenhammer.bayern.  CNAME  schubs.net.
push.feuerwehr.altenhammer.bayern.     CNAME  schubs.net.
n8n.feuerwehr.altenhammer.bayern.      CNAME  schubs.net.
matrix.feuerwehr.altenhammer.bayern.   CNAME  schubs.net.   # optional, nur wenn Stufe 2 eingerichtet wird
```

> Die vier A-Records sind die aktuellen GitHub Pages IPs. `www` als CNAME auf `<github-username>.github.io` — GitHub Pages leitet automatisch auf die Apex-Domain um.

**Hugo & GitHub Pages konfigurieren:**

- `hugo.toml`: `baseURL = "https://feuerwehr.altenhammer.bayern/"`
- `static/CNAME`: Datei mit Inhalt `feuerwehr.altenhammer.bayern` (eine Zeile, kein `https://`)
- GitHub Repository → Settings → Pages → Custom domain eintragen → "Enforce HTTPS" aktivieren

GitHub Pages stellt HTTPS via Let's Encrypt automatisch bereit (~15 Min nach DNS-Propagation).

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
- [ ] Kinderfeuerwehr-Logo integrieren (bereitgestellt)
- [ ] **Jubiläums-Logo SVG integrieren** (bereits vorhanden — `assets/images/jubilaeum-logo.svg`)
- [ ] Schriften (Oswald, Inter) herunterladen + `@font-face` CSS
- [ ] Design-Tokens in `tailwind.config.js`
- [ ] Startseite: Hero mit Jubiläums-Logo eingebunden, alle Sektionen
- [ ] Responsives Menü (Mobile Hamburger + Desktop)
- [ ] **Theming-Review** — Farben, Schriften, Logo, Header, Footer, Hero auf `hugo server` abnehmen, bevor Contentseiten gebaut werden

### Phase 3 — Compliance & Pflichtseiten

- [ ] `impressum.md` Vorlage mit Platzhaltern (Name, Adresse, Kontakt)
- [ ] `datenschutz.md` DSGVO-konform (GitHub Pages, HeyForm, Easy!Appointments, n8n)
- [ ] Einwilligungsformular Erwachsene (DOCX + PDF in `static/dokumente/`)
- [ ] Einwilligungsformular Minderjährige (DOCX + PDF in `static/dokumente/`)
- [ ] Kein externer Tracking-Code

### Phase 4 — Inhalt & Templates
- [ ] Alle Seitentypen implementieren
- [ ] Startseite: "Wer wir sind" + "Was wir tun" + Ehrenamt-Botschaft
- [ ] Termine-Seite mit Hugo-Filterlogik (14-Tage-Cutoff)
- [ ] Kontaktseite: Adresse + statisches OSM-Kartenbild + externer Map-Link + HeyForm-iFrame
- [ ] Placeholder-Inhalte für alle Seiten (inkl. Foto-Platzhalter)
- [ ] Spenden-Seite (GiroCode-QR einbinden, Spendenquittung-Abschnitt)
- [ ] Kuchentheke-Seite (Easy!Appointments-iFrame + Beschreibung + Buchungsbedingungen)
- [ ] Kuchentheke- und Mitmachen-Seite: URL-QR-Code via clientseitigem JS-Generator (Download-Button)

### Phase 5 — Coolify Services

- [ ] Coolify: Neues Projekt "FF Altenhammer" anlegen (getrennt von privaten Diensten)
- [ ] DNS-Einträge für alle FF-Subdomains beim Registrar eintragen (s. zentrale DNS-Tabelle)
- [ ] HeyForm auf Coolify deployen (Docker Compose + MongoDB)
- [ ] HeyForm: SMTP konfigurieren, hCaptcha aktivieren
- [ ] HeyForm: Kontaktformular anlegen, Betreff-Präfix `[FF-Kontakt]` → iFrame in Kontaktseite
- [ ] HeyForm: Spendenquittung-Formular anlegen, Betreff-Präfix `[FF-Spendenquittung]` → iFrame in Spendenseite
- [ ] Easy!Appointments auf Coolify deployen (Docker + MySQL)
- [ ] Easy!Appointments: SMTP, Service "Kuchentheke", manuelle Bestätigung, Betreff-Präfix `[FF-Kuchentheke]`
- [ ] Easy!Appointments: Widget-Embed-Code in Hugo-Kuchentheke-Seite eintragen
- [ ] Traefik Rate-Limiting-Labels für HeyForm und Easy!Appointments setzen
- [ ] Docker-Ressourcenlimits (CPU/RAM) für alle FF-Container in Coolify konfigurieren
- [ ] Integrationstest: Kontaktformular → E-Mail empfangen
- [ ] Integrationstest: Kuchentheke-Anfrage → ausstehend in Easy!Appointments → bestätigen → Bestätigungsmail

### Phase 6 — Benachrichtigungen (ntfy + n8n)

- [ ] n8n auf Coolify deployen (Docker, Subdomain `n8n.feuerwehr.altenhammer.bayern`)
- [ ] ntfy auf Coolify deployen (Docker, Subdomain `push.feuerwehr.altenhammer.bayern`)
- [ ] ntfy: Privaten Kanal anlegen + Zugangsdaten sichern
- [ ] n8n: Workflow "HeyForm → ntfy" anlegen (Webhook-URL in HeyForm eintragen)
- [ ] n8n: Workflow "Easy!Appointments → ntfy" anlegen (Webhook-URL in Easy!Appointments eintragen)
- [ ] ntfy-App auf Empfänger-Smartphones einrichten, Kanal abonnieren
- [ ] Integrationstest: Kontaktformular absenden → Push-Benachrichtigung erscheint
- [ ] Integrationstest: Kuchentheke-Anfrage → Push-Benachrichtigung erscheint
- [ ] Optional: Matrix/Conduit + mautrix-whatsapp auf Coolify deployen (Subdomain `matrix.feuerwehr.altenhammer.bayern`)

### Phase 7 — Dokumentation
- [ ] `README.md` — Pflege-Anleitung für alle Redakteure
- [ ] Beispiel-Termin + Beispielinhalte für Platzhalterseiten anlegen

---

## Verifikation

1. `hugo server` lokal — alle Seiten erreichbar, kein 404
2. Push auf `main` → GitHub Actions grün → Live-URL korrekt
3. Täglicher Cron-Build → abgelaufene Termine verschwinden nach 14 Tagen
4. Mobile-Test bei 375px — Navigation, Hero, Termine-Liste, Formulare
5. WCAG: Kontrast Rot/Weiß = 5.25:1 (erfüllt AA 4.5:1)
6. Impressum + Datenschutz in max. 2 Klicks von jeder Seite erreichbar
7. Fonts laden von `/fonts/` — nicht von `fonts.googleapis.com`
8. HeyForm: Kontaktformular → Testmail empfangen, Bestätigungsmail an Absender
9. Easy!Appointments: Kuchentheke-Anfrage → ausstehend → bestätigen → Bestätigungsmail
10. ntfy: Kontaktformular absenden → Push-Benachrichtigung auf Empfänger-Smartphone erscheint
11. ntfy: Kuchentheke-Anfrage → Push-Benachrichtigung erscheint
12. Jubiläums-Badge sichtbar; `jubilaeum = false` → Badge verschwindet
13. Kontaktseite: Kartenbild lädt, OSM-Link öffnet korrekte Position
14. Spendenseite: GiroCode-QR scannbar mit Banking-App (sobald IBAN vorliegt)
15. Gemeinnützigkeit prüfen → Spendenquittungs-Text ggf. anpassen
16. Rate Limiting testen: >20 Requests/min auf Formular → HTTP 429 Too Many Requests
17. Projektisolation prüfen: FF-Container im Coolify-Projekt "FF Altenhammer", private Dienste nicht sichtbar
