# Digitalfunk-Übungen — FF Altenhammer

> [!WARNING]
> **NUR ÜBUNG — DMO-MODUS (Direktbetrieb)**
> Diese Übung findet ausschließlich im Digitalfunk-Direktbetrieb (DMO) statt.
> **Kein echter Einsatz! Keine automatische Alarmierung anderer Einheiten.**

Übungsskripte für den Digitalfunk BOS im DMO-Modus (Direktbetrieb).

## Rufzeichen

| Einheit | Rufzeichen |
|---------|------------|
| Eigenes TSF | Florian Altenhammer 44/1 |
| Leitstelle | Leitstelle Neustadt |
| TSF Flossenbürg | Florian Flossenbürg 41/1 |
| DMO-Gruppe | [DMO-Gruppe eintragen] |

## Szenarien

| Nr. | Szenario | Sprecher min–max | Besonderheit | Optionen |
|-----|----------|-----------------|--------------|---------|
| 1 | Sturmschaden — Baum auf Fahrbahn | 2 – 5 | Parallele Truppbefehle, Fortschrittsmeldungen | OPT-Beleuchtung |
| 2 | Ölspur auf Fahrbahn St2395 | 2 – 5 | M2: 3 Varianten (Spur gefunden / nicht gefunden / läuft noch) | — |
| 3 | Stallbrand — Unterstützung Wasserversorgung | 3 – 6 | Unterstellungsverhältnis (EL Flossenbürg), Zweikanal-Betrieb | OPT-Wasser (3×), OPT-Tierrettung |
| 4 | Hubschrauberlandeplatz (nachts) | 2 – 4 | RTH-Koordination, Koordinaten + Windrichtung, ETA-Management | — |
| 5a | Tierrettung — Katze auf Baum | 2 – 3 | Einstiegsszenario, einfache Tierrettung | — |
| 5b | Tierrettung — Hund in Kanalisation | 2 – 3 | THL beengter Raum, ggf. Tierarzt anfordern | — |

*(geplant: Unfall mit Verletzten + RD-Übergabe)*

### Optionen im Detail

| Szenario | Option | Zusatz-Sprecher | Was die Option trainiert |
|----------|--------|-----------------|--------------------------|
| S1 | [OPT-Beleuchtung](Szenario-1-Sturmschaden/S1-OPT-Beleuchtung.md) | +1 (WTF) | Nachteinsatz, RD bereits vor Ort, Blendschutz-Kommunikation |
| S3 | [OPT-Wasser-Bach](Szenario-3-Stallbrand/S3-OPT-Wasser-Bach.md) | +1–2 | Ansaugbetrieb TS, Zweikanal, 400 m Schlauchleitung |
| S3 | [OPT-Wasser-Hydrant](Szenario-3-Stallbrand/S3-OPT-Wasser-Hydrant.md) | +1–2 | Zweikanal, Druckschwankungen überwachen |
| S3 | [OPT-Wasser-Löschteich](Szenario-3-Stallbrand/S3-OPT-Wasser-Loeschteich.md) | +1–2 | Zweikanal, Pegelüberwachung, Abbruchpegel kommunizieren |
| S3 | [OPT-Tierrettung](Szenario-3-Stallbrand/S3-OPT-Tierrettung.md) | +1–2 | Tierevakuierung parallel zu Wasserversorgung, Reihenfolge beachten |

### Empfehlung nach Gruppengröße

| Personen | Passende Szenarien |
|----------|--------------------|
| **2** | S1 Basis · S2 (Variante A, B oder C) · S4 Basis · S5a · S5b |
| **3** | S1 Vollbesetzung · S2 Vollbesetzung · S3 Basis · S4 Vollbesetzung |
| **4** | S1 + OPT-Beleuchtung · S3 + OPT-Wasser · S4 Vollbesetzung |
| **5** | S1 Vollbesetzung + OPT-Beleuchtung · S3 + OPT-Wasser + ATF · S2 Vollbesetzung |
| **6** | S3 Vollübung (Basis + OPT-Wasser + OPT-Tierrettung) |

## Module je Szenario

| Modul | Inhalt | Kommunikationsebene | Min. Funk-Sprecher |
|-------|--------|---------------------|-------------------|
| M1 | Alarmierung | Leitstelle → GF | 2 |
| M2 | Anfahrt & Lagemeldung | GF → Leitstelle | 2 |
| M3 | Befehlsgebung | GF → Trupp(s) | 2 (GF + 1 TF) |
| M4 | Einsatzabwicklung | GF ↔ Trupp(s) + ggf. Leitstelle | 2–5 |
| M5 | Abmeldung | GF → Leitstelle | 2 |

Module können einzeln oder am Stück gespielt werden.

> **Hinweis S3:** Szenario 3 weicht vom Schema ab — M2 heißt „Meldung bei EL" und M3 „Befehlsempfang", da Florian Flossenbürg 41/1 die Einsatzleitung ist. Die Leitstelle Neustadt wird erst wieder in M5 (Abmeldung nach Entlassung) kontaktiert.

## Übungsformate

| Format | Für | Beschreibung |
|--------|-----|--------------|
| **A — Dialogskript** | Einsteiger | Vollständiger Wortlaut Zeile für Zeile |
| **B — Rollenkarten** | Mittelstufe | Jeder sieht nur seine eigenen Sprechanteile |
| **C — Kombination** | Fortgeschritten | Übungsleiter hat Vollskript, Teilnehmer Rollenkarten |
| **D — Freies Szenario** | Erfahren | Nur Ausgangslage, kein vorgegebener Wortlaut |

## BOS-Sprechfunkregeln Kurzreferenz

### Anrufformat
```
[Gerufener] von [Rufender], kommen
```
Beispiel: „Leitstelle Neustadt von Florian Altenhammer 44/1, kommen"

### Antwortformat
```
[Gerufener] von [Rufender], kommen
```

### Gesprächsende
- Mit erwarteter Antwort: **„kommen"**
- Ohne Antwort / Gesprächsende: **„Ende"**

### Quittierung
- **„Verstanden"** — Nachricht empfangen und verstanden
- Niemals: „Roger", „OK", „Ja"

### Dringlichkeit
- Normal: Kein Präfix
- Dringend: „DRINGEND" dreimal voranstellen

### Rollenkennzeichnung in Skripten
- **[PFLICHT]** — muss besetzt sein
- **[OPTIONAL]** — bei genug Teilnehmern besetzen
- **[KEIN FUNK]** — TM ist physisch dabei, funkt nie
