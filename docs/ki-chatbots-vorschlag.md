# KI-Features für feuerwehr.altenhammer.bayern — Designvorschlag

> **Status: VORSCHLAG / ENTWURF**
> Dieses Dokument beschreibt einen Vorschlag für zwei KI-Features im Kontext des 100-jährigen Jubiläums 2026.
> Es handelt sich noch um keinen Beschluss und um keinen fertigen Implementierungsplan.
> Der Inhalt dieses Dokuments landet **nicht** auf der Website (liegt außerhalb von `content/`).

---

## Überblick

Im Jubiläumsjahr 2026 sollen zwei KI-gestützte Features entwickelt werden:

| Feature | Zielgruppe | Kanal |
|---|---|---|
| Geschichts-Chatbot „100 Jahre in einem Gespräch" | Alle Besucher | QR-Code am Fest + dauerhaft online |
| Brandschutz-Assistent „Löschzwerge" | Kinder 5–12 Jahre | Fest-Station + online |

Beide Features sind voneinander unabhängig und können einzeln umgesetzt werden.

---

## Feature 0: Chronik-Digitalisierung (Voraussetzung für Feature 1)

### Was es tut

Aus vorhandenen Protokollen, Zeitungsberichten und anderen Quellen wird mithilfe von KI eine strukturierte Vereinschronik erstellt. Diese Chronik ist:
- **Wissensbasis** für den Geschichts-Chatbot (Feature 1)
- **Inhalt** für die `/ueber-uns/geschichte/`-Seite der Homepage
- **Archiv** für die Wehr — unabhängig von den KI-Features wertvoll

### Ausgangslage

| Quelltyp | Format | Menge (Schätzung) |
|---|---|---|
| Sitzungsprotokolle | Physisches Papier (getippt/handschriftlich) | Hoch |
| Zeitungsberichte | Physisches Papier (Ausschnitte) | Mittel |
| Digitale Dokumente | Word, PDF, E-Mails | Gering |

### Workflow

```
Physische Dokumente
      ↓
Scannen mit Smartphone-App
(Microsoft Lens oder Adobe Scan — kostenlos)
      ↓
KI-Extraktion (Weg A: Claude Code CLI  |  Weg B: Python-Skript)
      ↓  Markdown-Datei wird automatisch erstellt
Menschliche Kontrolle & Korrektur
(menschlich_geprüft: true setzen)
      ↓
Öffentliche Chronik-Version kompilieren
      ↓
Chatbot-Wissensbasis + Homepage
```

### Scan-Empfehlungen

| Dokumenttyp | Vorgehen |
|---|---|
| Gedruckte / getippte Protokolle | Microsoft Lens oder Adobe Scan — Sekunden pro Seite, sehr gute Erkennung |
| Zeitungsausschnitte | Gleiche Apps, auf weißem Untergrund fotografieren |
| Handschriftliche Protokolle | Gutes Licht, Dokument flach auf Tisch, Foto aus senkrechter Perspektive — Claude versteht viele Handschriften, aber Qualität variiert |
| Bereits digitale Dokumente | Direkt hochladen, kein Scan nötig |

### Datenschutz — zwei Versionen der Chronik

Protokolle enthalten Namen lebender Mitglieder. Daraus entstehen zwei Versionen:

| Version | Inhalt | Verwendung |
|---|---|---|
| **Interne Vollversion** | Alle Details, alle Namen | Vereinsarchiv, interner Filebrowser |
| **Öffentliche Version** | Ereignisse ohne personenbezogene Daten (oder nur mit Einwilligung) | Chatbot-Wissensbasis, Homepage |

Namen verstorbener Mitglieder sind in der Regel unproblematisch. Für lebende Mitglieder gilt: entweder Einwilligung einholen oder Namen weglassen.

### Wie Markdown-Dateien entstehen

Markdown-Dateien werden **halbautomatisch** erstellt: ein Python-Skript (`scripts/digitize.py`) übernimmt Extraktion und Dateierstellung, ein Mensch prüft danach das Ergebnis.

Vollständig manuell wäre bei vielen Dokumenten zu aufwändig und fehleranfällig. Vollständig automatisch ohne menschliche Kontrolle wäre für historische Inhalte zu riskant — Claude macht gelegentlich Fehler bei schwierigen Scans.

Es gibt zwei gleichwertige Wege zur Erstellung der Markdown-Dateien:

---

#### Weg A: Claude Code CLI (empfohlen für den Einstieg)

Kein Skript nötig. Claude Code liest die Scans direkt, erstellt die Markdown-Dateien und fragt bei Unklarheiten nach — alles interaktiv im Terminal.

```
1. Scans in einen Ordner legen:
   docs/chronik/neue-scans/scan-001.jpg, scan-002.jpg, ...

2. Claude Code im Projektordner öffnen und anweisen:
   „Verarbeite alle Bilder in docs/chronik/neue-scans/.
    Erstelle für jedes Bild eine Markdown-Datei im passenden
    Unterordner von docs/chronik/quellen/ nach dem Format
    in docs/chronik/README.md."

3. Claude Code erstellt die Dateien, meldet Unsicherheiten
   (unleserliche Stellen, unklare Daten) und fragt nach.

4. Mensch prüft Ergebnis und setzt menschlich_geprüft: true.
```

**Voraussetzung:** Claude Code läuft über die bestehende claude.ai-Subscription (Pro oder Max). Bei intensiver Nutzung kann Claude Code alternativ mit einem eigenen API-Key konfiguriert werden — dann identische Kosten wie Weg B.

**Gut für:** überschaubare Mengen, gelegentliche Nutzung, wenn kein separater API-Account gewünscht ist.

---

#### Weg B: Python-Skript `scripts/digitize.py` + API-Key

Ein einmalig geschriebenes Skript verarbeitet Dokumente vollautomatisch ohne Aufsicht. Braucht einen separaten Account auf console.anthropic.com mit Kreditkarte (keine Grundgebühr, nur Verbrauch).

```
1. Dokument scannen → scan.jpg

2. Skript aufrufen:
   python scripts/digitize.py scan.jpg
   # oder einen ganzen Ordner:
   python scripts/digitize.py --ordner ./neue-scans/

3. Skript sendet jedes Bild an Claude API mit festem Prompt
   und erwartet JSON zurück:
   {
     "datum": "1952-03-15",
     "typ": "protokoll",
     "titel": "Jahreshauptversammlung 1952",
     "punkte": ["Neuwahl Vorstand", "Beschluss neue Schläuche"],
     "enthaelt_personendaten": true,
     "rohtext": "vollständiger extrahierter Text"
   }

4. Skript erstellt automatisch:
   docs/chronik/quellen/protokolle/1950-1970/
     1952-03-15-jahreshauptversammlung.md
   (Frontmatter befüllt, ki_verarbeitet: true,
    menschlich_geprüft: false)

5. Mensch prüft Ergebnis und setzt menschlich_geprüft: true.
```

PDFs mit mehreren Seiten: Das Skript extrahiert jede Seite als Bild und sendet sie einzeln — die Ergebnisse werden zu einer Markdown-Datei zusammengefasst.

**Gut für:** große Mengen, Batch-Verarbeitung ohne Aufsicht, vollständige Automatisierung.

---

#### Gegenüberstellung

| | Weg A: Claude Code CLI | Weg B: Python-Skript |
|---|---|---|
| Setup | Keiner | API-Account + Skript schreiben |
| Billing | claude.ai-Subscription | console.anthropic.com pay-per-use |
| Interaktivität | Fragt bei Unklarheiten nach | Läuft durch, markiert Unsicherheiten |
| Batch-Verarbeitung | Möglich, aber interaktiv | Vollautomatisch |
| Empfehlung | Einstieg und kleinere Mengen | Große Mengen oder regelmäßige Nutzung |

**Empfohlene Reihenfolge:** Mit Weg A starten — kein Setup, sofort nutzbar. Wenn die Menge der Dokumente es erfordert, auf Weg B umsteigen.

---

#### Manuelle Erstellung als Fallback

Wenn ein Dokument für beide Wege zu schwierig ist (sehr schlechte Qualität, ungewöhnliches Format), kann die Datei manuell erstellt werden. Vorlage liegt in `docs/chronik/README.md`. Frontmatter und Struktur bleiben identisch — `ki_verarbeitet: false` setzen.

#### Was immer manuell bleibt

- Prüfen ob Datum und Typ korrekt erkannt wurden
- Kontrollieren ob wichtige Punkte vollständig sind
- Entscheiden was in die öffentliche Version darf (Personendaten)
- `menschlich_geprüft: true` setzen

### Scan-Workflow: kein OpenCV nötig

Die kostenlose OCR in Microsoft Lens und Google Lens ist für sauberen modernen Drucktext so gut wie Tesseract — ohne Installation, ohne Setup. OpenCV lohnt sich erst bei automatisierten Pipelines mit Tausenden von Dokumenten. Für eine einmalige Digitalisierung ist der Aufwand unverhältnismäßig.

| Dokumenttyp | Vorgehen | Kosten |
|---|---|---|
| Gedruckte moderne Protokolle | Microsoft Lens fotografieren → Text kopieren → in Claude.ai einfügen | €0 |
| Zeitungsartikel (sauber) | Gleicher Weg | €0 |
| Handschrift / alte Schrift / schlechte Qualität | Foto direkt in Claude.ai hochladen | ~€0.003/Seite |

**Realistische Gesamtkosten** für 1.000 Seiten (davon 200 schwierige Dokumente direkt per Vision): unter **€1**.

### Ordnerstruktur — optimiert für Claude und Menschen

Alle Dokumente liegen in `docs/chronik/` im Repository. Scans (JPEGs) werden **nicht** in git versioniert (zu groß) — sie liegen auf dem Filebrowser im Feuerwehrhaus und werden im Markdown referenziert.

```
docs/chronik/
├── README.md                        ← Anleitung + Frontmatter-Vorlage (s. unten)
├── neue-scans/                      ← Temporärer Eingangsordner für neue Scans
│   └── .gitkeep                     ← Ordner in git, Inhalte in .gitignore
├── quellen/                         ← Rohe Extraktion, ein Dokument pro Datei
│   ├── protokolle/
│   │   ├── 1926-1950/
│   │   │   ├── 1926-gruendung.md
│   │   │   └── 1932-jahresversammlung.md
│   │   ├── 1950-1970/
│   │   ├── 1970-1990/
│   │   ├── 1990-2010/
│   │   └── 2010-2026/
│   ├── zeitungsberichte/
│   │   ├── 1926-1950/
│   │   └── ...
│   └── sonstiges/                   ← Urkunden, Fotos mit Beschreibung, etc.
├── chronik/
│   ├── intern/                      ← Vollversion mit Namen (nur interner Zugriff)
│   │   ├── 1926-1950.md
│   │   ├── 1950-1970.md
│   │   └── ...
│   └── oeffentlich/                 ← Namen anonymisiert oder mit Einwilligung
│       ├── 1926-1950.md
│       └── ...
└── chatbot-wissensbasis.md          ← Kompilierte öffentliche Version für den Chatbot
```

`.gitignore`-Ergänzung damit Scan-Bilder nicht in git landen:
```
docs/chronik/neue-scans/*.jpg
docs/chronik/neue-scans/*.pdf
docs/chronik/neue-scans/*.png
```

**`docs/chronik/README.md` enthält:**
- Kurzanleitung: Scan-App einrichten, Weg A (Claude Code) und Weg B (Skript) aufrufen
- Die Frontmatter-Vorlage zum Kopieren für manuelle Erstellung
- Erklärung der Ordnerstruktur
- Hinweise zu Datenschutz (welche Namen dürfen in die öffentliche Version)

Diese README ist die einzige Datei, die ein nicht-technisches Mitglied lesen muss, um Dokumente beizutragen.

### Format jeder Quelldatei

Jedes Dokument bekommt eine eigene Markdown-Datei mit einheitlichem Aufbau. Das macht es Claude leicht, gezielt Informationen zu finden, und Menschen leicht, den Status zu überblicken.

```markdown
---
datum: 1952-03-15          # YYYY-MM-DD, oder 1952-ca wenn Datum unbekannt
typ: protokoll             # protokoll | zeitungsbericht | urkunde | sonstiges
quelle: Jahreshauptversammlung 1952, handschriftliches Protokoll
scan: JHV-1952-03-15.jpg   # Dateiname auf dem Filebrowser
ki_verarbeitet: true
menschlich_geprueft: false  # auf true setzen nach menschlicher Kontrolle
enthaelt_personendaten: true
---

## Extrahierte Information

**Datum:** 15. März 1952
**Veranstaltung:** Jahreshauptversammlung
**Ort:** Feuerwehrhaus Altenhammer

## Wichtige Punkte

- Neuwahl des Vorstands
- Beschluss: Anschaffung neuer Schläuche
- Mitgliederstand: 24 aktive Mitglieder

## Roher Text (OCR / Notizen)

[Hier der rohe extrahierte Text oder handschriftliche Notizen]
```

**Warum dieses Format für Claude optimal ist:**
- Frontmatter ermöglicht gezielte Filterung (z.B. „nur Protokolle vor 1950")
- Klare Trennung zwischen Metadaten, strukturierter Extraktion und Rohtext
- Chronologische Ordnung = natürlicher Kontext beim Lesen

**Warum es für Menschen wartbar ist:**
- Eine Datei pro Dokument — keine riesige Datei die schwer zu bearbeiten ist
- `menschlich_geprüft: false` zeigt sofort was noch kontrolliert werden muss
- Auch nicht-technische Mitglieder können im GitHub Web Editor Korrekturen machen

### Chatbot-Wissensbasis kompilieren und einpflegen

`chatbot-wissensbasis.md` ist die kompilierte öffentliche Version — chronologisch, ohne personenbezogene Daten. Sie wird per Python-Skript (`scripts/compile_chronik.py`) aus allen Dateien in `docs/chronik/chronik/oeffentlich/` zusammengestellt.

**Wie die Wissensbasis in den Chatbot-Service kommt:**
Die Datei liegt im Repository und wird beim Deployment des Docker-Containers in das Image eingebaut (COPY in Dockerfile). Bei Aktualisierungen muss der Container neu gebaut und deployed werden — ein einzeiliger Befehl in Coolify.

Bei neuen Dokumenten:
```
Quelldatei anlegen → öffentliche Chronik-Datei ergänzen
→ python scripts/compile_chronik.py
→ git commit + push
→ Coolify: Container neu bauen (1 Klick)
→ Chatbot hat neues Wissen
```

### Verbindung zu Feature 1

Die öffentliche Chronik-Version wird direkt als Wissensbasis für den Geschichts-Chatbot verwendet. Ohne diese Vorarbeit hat der Chatbot nichts zu erzählen — **Feature 0 ist Voraussetzung für Feature 1**.

### Zeitaufwand (Schätzung)

| Tätigkeit | Wer | Aufwand |
|---|---|---|
| Scannen physischer Dokumente | Beliebiges Mitglied | 2–4 Stunden je nach Menge |
| KI-Extraktion + Kontrolle pro Dokument | Thomas | ~5–10 Min. pro Dokument |
| Lektorat der fertigen Chronik | Vorstand / Chronikverantwortliche | 2–4 Stunden |

---

## Feature 1: Geschichts-Chatbot „100 Jahre in einem Gespräch"

### Was es tut

Besucher stellen per Smartphone oder Tablet Fragen zur Geschichte der FF Altenhammer und bekommen Antworten auf Basis echter Vereinsunterlagen. Beim Jubiläumsfest als Erlebnis-Station per QR-Code, danach dauerhaft über die Homepage erreichbar.

Beispielfragen:
- „Wann wurde die Wehr gegründet?"
- „Was war der größte Einsatz in der Geschichte?"
- „Wie hat sich die Ausrüstung in 100 Jahren verändert?"

### Wie es technisch funktioniert

```
Besucher (Smartphone/Tablet)
        ↓  HTTPS
Cloudflare  (DDoS-Schutz, Rate Limiting)
        ↓  Cloudflare Tunnel (ausgehende Verbindung vom Server)
Mini-PC im Feuerwehrhaus / gewählte Infrastruktur
        ↓
Anthropic Claude Haiku API   ← API-Key nur serverseitig, nie im Browser
```

Der Chatbot antwortet **ausschließlich** auf Basis von Dokumenten, die wir selbst einpflegen (Chronik, Einsatzstatistiken, Vereinsgeschichte). Er erfindet nichts und greift nicht frei ins Internet.

### Technischer Stack

| Komponente | Entscheidung | Begründung |
|---|---|---|
| Backend | Python FastAPI (Docker) | Schlankes Muster, analog zur bestehenden `kuchentheke-app` |
| KI-Modell | Anthropic Claude Haiku | Günstigster Tier, für Frage-Antwort auf eigenem Content ausreichend |
| Hosting | Gewählte Infrastruktur (s. Abschnitt „Infrastruktur-Optionen") | Vollständig getrennt von `schubs.net` |
| Konnektivität | **Cloudflare Tunnel** — kein offener Port, keine statische IP nötig | Sicher, wartungsarm, kostenlos |
| Frontend | Einfaches HTML/CSS/JS im Container | Kein Framework-Overhead für ein Chatfenster |
| Subdomain | `chatbot.feuerwehr.altenhammer.bayern` | Konsistent mit bestehendem Muster |
| Rate Limiting | Cloudflare (erste Linie) + Traefik im Container (zweite Linie) | max. 20 Anfragen/Min. pro IP |

DNS-Eintrag: wird automatisch von Cloudflare Tunnel verwaltet — kein manueller CNAME auf eine Server-IP nötig.

Ressourcen:
| Dienst | CPU | RAM |
|---|---|---|
| ff-ki-service | 0.5 Core | 256 MB |

### Content-Aufwand (nicht-technisch)

Vor der Implementierung müssen folgende Inhalte als Text aufbereitet werden:

- [ ] Vereinschronik (Gründung, Meilensteine, Jubiläen)
- [ ] Bedeutende Einsätze (ohne personenbezogene Daten)
- [ ] Entwicklung der Ausrüstung und Fahrzeuge
- [ ] Mitgliederzahlen im Zeitverlauf
- [ ] Besonderheiten des Ortes / der Gemeinde

Verantwortlich: Vorstand / Chronik-Verantwortliche — **nicht** der Entwickler.
Format: einfaches Markdown-Dokument, das in den Service eingepflegt wird.

### Datenschutz

- Kein User-Login, keine Registrierung
- Keine Speicherung von Gesprächsverläufen
- Anthropic Data Processing Agreement (DPA) unterzeichnen → DSGVO-konform
- Datenschutzerklärung der Homepage ergänzen (Abschnitt: Chatbot-Dienst)
- Anthropic trainiert **nicht** auf API-Anfragen (Vertragsgrundlage)

### Kosten

| Posten | Option A (Mini-PC) | Option B (Hetzner) | Option C (RPi 4) |
|---|---|---|---|
| Infrastruktur (einmalig) | €130–150 | €0 | €155–185 |
| Infrastruktur (laufend/Jahr) | ~€10 Strom | ~€50 | ~€10 Strom |
| Anthropic API (Normalbetrieb/Monat) | €2–10 | €2–10 | €2–10 |
| Anthropic API (Festtag, einmalig) | €10–20 | €10–20 | €10–20 |
| **Jahr 1 gesamt** | **~€200** | **~€140** | **~€230** |
| **Ab Jahr 2 (laufend)** | **~€50–70** | **~€120** | **~€50–70** |

Empfehlung: In der Anthropic Console ein monatliches Ausgabenlimit setzen (z.B. €30), damit keine Überraschungen entstehen.

---

## Feature 2: Brandschutz-Assistent „Löschzwerge"

### Was es tut

Ein kindgerechter interaktiver Assistent, der Kindern Brandschutz auf spielerische Art näherbringt. Kein trockener FAQ — eine Figur mit Persönlichkeit, die Rätsel stellt, lobt und Geschichten erzählt.

Vorschlag Figur: **„Funke"** — ein frecher kleiner Feuerwehrmann mit Helm, der alles über Feuer weiß.

### Zwei Modi für zwei Altersgruppen

#### Modus A: Kleine Löschzwerge (5–7 Jahre)

- Reine statische Web-App — **kein Backend, kein API-Key, keine KI**
- Große bunte Bild-Buttons statt Texteingabe (keine Lesekompetenz nötig)
- Browser-eigene Sprachausgabe (Web Speech API) liest Antworten laut vor
- Vordefinierter Inhalt, vollständig von der Wehr kontrolliert:
  - Was mache ich, wenn's brennt? → Raus, Tür zu, 112 anrufen
  - Was ist die Notrufnummer? → 112
  - Was macht ein Rauchmelder? → Er gibt Alarm, wenn es raucht
  - u.a.
- Deployment: statische Datei auf GitHub Pages (`static/loeschzwerge/index.html`)
- **Kosten: €0**

#### Modus B: Große Löschzwerge (8–12 Jahre)

- Chatbot-Interface (gleicher Coolify-Service wie Feature 1, separater Endpunkt `/kinder`)
- Claude Haiku mit striktem System-Prompt:
  - Nur Brandschutzthemen — keine anderen Themen
  - Kindgerechte, einfache Sprache
  - Charakter „Funke" mit Persönlichkeit
  - Stellt Gegenfragen und gibt kleine Missionen
  - Fragt niemals nach persönlichen Daten
  - Lobt richtige Antworten
- **Kosten: Teil der API-Kosten von Feature 1** (keine Zusatzkosten)

#### Gemeinsamer Startbildschirm

Zwei große Buttons ohne Texteingabe:
```
┌─────────────────────────────────────────────┐
│  Hallo! Ich bin Funke.                       │
│  Wie alt bist du?                           │
│                                             │
│   [ 5–7 Jahre ]        [ 8–12 Jahre ]       │
└─────────────────────────────────────────────┘
```

### Datenschutz (besonders wichtig bei Kindern)

- Keine Abfrage personenbezogener Daten (Name, Alter, Schule, Adresse)
- Kein Login, keine Registrierung
- Keine Speicherung von Gesprächsverläufen
- System-Prompt verhindert aktiv, dass die KI nach persönlichen Infos fragt
- Da keine Verarbeitung personenbezogener Daten: DSGVO Art. 8 (Kinder) unproblematisch

---

## Infrastruktur-Optionen für den KI-Service

Der KI-Service muss vollständig von `schubs.net` (privater Server) getrennt sein.
Drei Optionen stehen zur Wahl — alle erfüllen diese Anforderung:

### Option A: Mini-PC mit Intel N100 im Feuerwehrhaus (~€130–150, einmalig)

Empfehlung wenn physische Hardware im Feuerwehrhaus gewünscht ist.

| Merkmal | Detail |
|---|---|
| Beispiele | Beelink EQ12, GMKtec NucBox G3 |
| Architektur | **x86_64** — 100% Docker-Kompatibilität, null Image-Probleme |
| RAM / SSD | 8–16 GB RAM + 256–500 GB SSD **bereits inklusive** |
| Stromverbrauch | ~10–15 W (Dauerbetrieb: ~€8–12/Jahr) |
| Gesamtkosten | ~€130–150 einmalig, kein laufender Beitrag |
| Vorteil | Robuster als SBC, alles inklusive, einfach zu verwalten |

Konnektivität: **Cloudflare Tunnel** — kein offener Port am Feuerwehrhaus-Router, keine statische IP nötig. Der Mini-PC baut selbst eine ausgehende Verbindung zu Cloudflare auf.

Remote-Verwaltung: **Tailscale** (kostenloses Zero-Config-VPN) für SSH-Zugriff ohne exponierte Ports.

### Option B: Hetzner Cloud CAX11 (~€50/Jahr, kein Hardware-Kauf)

Empfehlung wenn kein Hardware-Aufwand gewünscht ist und „getrennt von schubs.net" ausreicht.

| Merkmal | Detail |
|---|---|
| Specs | 2 vCPU ARM64, 4 GB RAM, 40 GB SSD |
| Standort | Rechenzentrum Nürnberg oder Helsinki |
| Kosten | €4.15/Monat = ~€50/Jahr |
| Uptime | ~99.9% (professionelle Infrastruktur) |
| Vorteil | Kein Hardware-Kauf, keine Wartung, keine Abhängigkeit vom Feuerwehrhaus-Anschluss |
| Nachteil | Laufende Kosten, physisch nicht im Feuerwehrhaus |

Für den Chatbot ist der physische Standort technisch irrelevant — er ruft sowieso die Anthropic API im Internet auf.

### Option C: Raspberry Pi 4 (8 GB) im Feuerwehrhaus (~€155–185, einmalig)

Vertraute Wahl mit der größten Community.

| Merkmal | Detail |
|---|---|
| Architektur | ARM64 — ~95% Docker-Kompatibilität (für diesen Use-Case ausreichend) |
| RAM | 8 GB |
| SSD | USB-SSD extern, extra Kosten (~€40) |
| Stromverbrauch | ~5–8 W |
| Gesamtkosten | ~€155–185 einmalig |
| Vorteil | Größte Community, beste Dokumentation, jahrelang erprobt |
| Nachteil | Teurer als Mini-PC bei geringerem Umfang (SSD extra, weniger RAM) |

Gleiche Konnektivität wie Option A: Cloudflare Tunnel + Tailscale.

> **Warum nicht Raspberry Pi 2?** Der vorhandene RPi 2 eignet sich gut als lokale Entwicklungsumgebung, aber nicht für Produktion: 32-bit ARM schließt viele moderne Docker-Images aus, 1 GB RAM ist für Docker + Coolify sehr eng.

### Empfehlung

| Priorität | Option |
|---|---|
| Hardware im Feuerwehrhaus, minimaler Aufwand | **A — Mini-PC N100** |
| Kein Hardware-Kauf, professionelle Infrastruktur | **B — Hetzner CAX11** |
| Bekannte Plattform, große Community | **C — RPi 4** |

---

## Deployment-Gesamtübersicht

```
Coolify-Projekt „FF Altenhammer"  ← läuft auf gewählter Infrastruktur (Option A/B/C)
└── ff-ki-service              (NEU)
    ├── Endpunkt /             → Geschichts-Chatbot
    ├── Endpunkt /kinder       → Brandschutz-Assistent Modus B (8–12)
    ├── RAM-Limit: 256 MB
    ├── CPU-Limit: 0.5 Core
    └── Secret: ANTHROPIC_API_KEY

GitHub Pages (Hugo, bestehend — unverändert)
└── static/loeschzwerge/       (NEU, statisch)
    └── index.html             → Brandschutz-Assistent Modus A (5–7)
```

Bestehende Dienste auf schubs.net (HeyForm, Easy!Appointments, n8n, ntfy) können dort verbleiben oder zu einem späteren Zeitpunkt migriert werden — das ist eine separate Entscheidung.

---

## Weitere Anwendungsfälle im Feuerwehrhaus

Der Server rechtfertigt sich nicht allein durch den KI-Chatbot. Die folgenden Anwendungsfälle nutzen dieselbe Hardware und verbessern den Vereinsalltag direkt.

### Vorhandene Hardware im Feuerwehrhaus

- Fernseher mit HDMI
- Samsung Soundbar (am Fernseher)
- Beamer
- FritzBox mit Gastzugang

### Jellyfin — Medienserver und lokales Abspielgerät

Open-Source-Medienverwaltung (selbst-gehostet, kostenlos). Trainingsvideos, Schulungsfilme, Aufzeichnungen — alles in einer sauberen Bibliothek.

**Setup:** Mini-PC per HDMI direkt am Fernseher. Jellyfin läuft im Browser auf dem Mini-PC selbst — kein Streaming, kein Transcoding, volle Qualität. Soundbar übernimmt Audio automatisch über den Fernseher.

Zusätzlich: Mitglieder können Schulungsmaterial von zuhause herunterladen (über Cloudflare Tunnel mit Login).

> **Warum das den Mini-PC gegenüber dem RPi 4 stärkt:** Sollte doch zu einem anderen Gerät gestreamt werden (z.B. Beamer über WLAN), nutzt der Intel N100 Intel QuickSync für Hardware-Transcoding — nahezu kostenlos in Rechenleistung. Ein RPi 4 würde dabei deutlich ins Schwitzen kommen.

### Digitale Anzeigetafel

Browser im Kiosk-Modus am Fernseher zeigt automatisch wechselnde Inhalte, solange das Gerät nicht aktiv genutzt wird:

- Nächste Termine (aus der Hugo-Homepage)
- Ankündigungen
- Jubiläums-Countdown

Technisch minimal: eine lokale HTML-Seite, die sich selbst aktualisiert. Kein separates Tool nötig.

### Filebrowser — Dokumenten-Server

Leichtgewichtiger Web-Dateimanager. Zugänglich von jedem Gerät im Feuerwehrhaus-WLAN oder von zuhause.

Inhalt:
- Schulungsunterlagen (PDFs, Präsentationen)
- Formulare (Aufnahmeanträge, Vorlagen)
- Fotos von Übungen und Veranstaltungen
- Vereinschronik-Dokumente (Basis für den KI-Chatbot)

Kein E-Mail-Anhang-Chaos mehr — immer die aktuelle Version, für alle erreichbar.

### Pi-hole — Netzwerk-weiter Werbeblocker

Minimaler Ressourcenverbrauch (~50 MB RAM). Blockiert Werbung für alle Geräte im Feuerwehrhaus-Netzwerk ohne Konfiguration an den einzelnen Geräten.

> **Hinweis Gastnetz:** Die FritzBox trennt das Gastnetz vom Hauptnetz. Der Filebrowser und andere interne Dienste sind vom Gastnetz aus nicht erreichbar — das ist gewollt. Der KI-Chatbot hingegen läuft über das Internet (Cloudflare Tunnel) und ist vom Gastnetz aus erreichbar, weil er über die normale URL aufgerufen wird.

### Gesamtbild: ein Gerät, viele Aufgaben

| Anwendungsfall | Technisch | Ressourcen |
|---|---|---|
| KI-Chatbot (Geschichte + Kinder) | Docker-Container | gering |
| Jellyfin Medienserver | Docker-Container | mittel (Transcoding nur bei Bedarf) |
| Lokale Wiedergabe via HDMI | Browser direkt am TV | keine (kein Transcoding) |
| Digitale Anzeigetafel | Browser Kiosk-Modus | minimal |
| Filebrowser Dokumente | Docker-Container | minimal |
| Pi-hole | Docker-Container | minimal |

---

### Warum das die Hardware-Entscheidung beeinflusst

| | Hetzner CAX11 | RPi 4 | **Mini-PC N100** |
|---|---|---|---|
| KI-Chatbot | ✓ | ✓ | ✓ |
| Jellyfin + lokale HDMI-Wiedergabe | ⚠ kein HDMI (Remote-Streaming möglich) | ⚠ schwach bei Transcoding | **✓ QuickSync + HDMI direkt** |
| Filebrowser | ✓ | ✓ | ✓ |
| Digitale Anzeigetafel | — (kein lokales Netz) | ✓ | ✓ |
| Pi-hole | — | ✓ | ✓ |
| Lokales Netz (TV, Beamer, WLAN) | **nein** | ja | ja |
| Einmalkosten | €0 | ~€155–185 | ~€130–150 |
| Laufende Kosten | ~€50/Jahr | €0 | €0 |

Für den Gesamtbedarf ist der **Mini-PC N100 im Feuerwehrhaus** die sinnvollste Wahl: mehr Leistung als der RPi 4, günstiger als ein vollausgestatteter RPi 4 (SSD inklusive), und als einzige Option mit direktem HDMI-Anschluss an Fernseher und Beamer nutzbar.

---

## Empfohlene Umsetzungsreihenfolge

### Phase 0 — Chronik-Digitalisierung (kann sofort beginnen, unabhängig von allem anderen)

> Scans liegen in Phase 0 noch lokal auf dem Rechner (Filebrowser existiert noch nicht).
> Nach Phase C werden sie auf den Filebrowser im Feuerwehrhaus übertragen.

- [ ] `docs/chronik/`-Ordnerstruktur im Repository anlegen inkl. `README.md` mit Vorlage
- [ ] `.gitignore` um Scan-Dateien ergänzen
- [ ] Scanning-App einrichten (Microsoft Lens oder Adobe Scan)
- [ ] Dokumente sichten und priorisieren (was ist am relevantesten?)
- [ ] Physische Dokumente scannen → lokal ablegen
- [ ] Digitale Dokumente sammeln und konsolidieren
- [ ] KI-Extraktion mit Weg A (Claude Code) oder Weg B (Skript), Markdown-Dateien erstellen
- [ ] Interne Vollversion reviewen (Vorstand), `menschlich_geprueft: true` setzen
- [ ] Öffentliche Version erstellen (Namen prüfen, ggf. entfernen)
- [ ] `scripts/compile_chronik.py` ausführen → `chatbot-wissensbasis.md` generieren
- [ ] Öffentliche Version in `/content/ueber-uns/geschichte.md` einarbeiten

### Phase A — Hardware & Infrastruktur

- [ ] Infrastruktur-Option entscheiden (Mini-PC / Hetzner / RPi 4)
- [ ] Hardware beschaffen und aufstellen (bei Option A/C: Mini-PC oder RPi im Feuerwehrhaus)
- [ ] Betriebssystem + Docker + Coolify installieren (analog zu schubs.net)
- [ ] Cloudflare Tunnel einrichten (`chatbot.feuerwehr.altenhammer.bayern`)
- [ ] Tailscale für Remote-Verwaltung einrichten
- [ ] Anthropic Account anlegen, DPA akzeptieren, Spending-Limit setzen

### Phase B — KI-Features (vor dem Jubiläumsfest)

- [ ] Content-Aufbereitung: Vereinschronik als Markdown-Dokument (Vereinsseite)
- [ ] Brandschutz-Assistent Modus A (5–7): statische Web-App auf GitHub Pages
- [ ] Backend-Service: Docker-Container, API-Key, Rate Limiting
- [ ] Geschichts-Chatbot: Endpunkt + Chat-UI
- [ ] Brandschutz-Assistent Modus B (8–12): Endpunkt + Charakter-Prompt
- [ ] QR-Code-Generierung für Fest-Plakate
- [ ] Datenschutzerklärung auf Homepage ergänzen

### Phase C — Weitere Dienste im Feuerwehrhaus (parallel oder danach)

- [ ] Jellyfin: Docker-Container, Medienbibliothek anlegen, am TV testen
- [ ] Filebrowser: Docker-Container, Ordnerstruktur anlegen, Zugangsdaten vergeben
- [ ] Digitale Anzeigetafel: HTML-Seite, Browser-Kiosk-Modus am TV einrichten
- [ ] Pi-hole: Docker-Container, als DNS-Server in FritzBox eintragen

### Phase D — Nach dem Fest

- [ ] Verlinkung auf `/jubilaeum/`- und `/kinderfeuerwehr/`-Seite
- [ ] Permanenter Betrieb + monatliche Kostenkontrolle (Anthropic Console)

---

## Offene Entscheidungen

Folgende Punkte müssen noch intern geklärt werden:

- [ ] **Subdomain-Name:** `chatbot.*` oder `ki.*` oder anders?
- [ ] **Figur:** Name „Funke" und Konzept bestätigen — gibt es ein vorhandenes Maskottchen der Löschzwerge?
- [ ] **Content-Verantwortung:** Wer bereitet die Vereinschronik als Text auf?
- [ ] **Fest-Setup:** QR-Code-Plakate, Tablet-Kiosk oder beides?
- [ ] **Anthropic API-Account anlegen:** console.anthropic.com — eigener Account, getrennt von der claude.ai-Subscription. Kreditkarte hinterlegen (nur tatsächlicher Verbrauch wird abgerechnet, keine Grundgebühr).
- [ ] **Spending-Limit setzen:** Settings → Billing → Usage limits → €30/Monat (Empfehlung)
- [ ] **API-Key erstellen:** API Keys → Create Key → in `.env`-Datei speichern, nie in git committen
- [ ] **Anthropic DPA:** Einmalig in der Anthropic Console unter „Privacy" akzeptieren

---

## Was dieses Projekt ausdrücklich NICHT ist

- Kein Ersatz für menschliche Ausbilder oder Betreuer
- Kein System für Einsatzkommunikation oder Alarmierung
- Kein Datensammler — keine personenbezogenen Nutzerdaten werden gespeichert
- Kein fester Bestandteil der Homepage-Navigation (vorerst)
- Kein Großprojekt: Gesamtaufwand realistisch 2–4 Wochen Entwicklungszeit

---

## Hinweis: Weiternutzung durch andere Wehren

Der Service ist von Anfang an so zu bauen, dass er mit minimalem Aufwand für andere kleine Freiwillige Wehren adaptiert werden kann (andere Chronik-Dokumente, anderes Branding). Das ermöglicht eine spätere Zusammenarbeit mit dem Kreisfeuerwehrverband oder Landesverband — ohne dass dafür jetzt Mehraufwand entsteht.
