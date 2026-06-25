# OPT: Wasserversorgung — Offenes Gewässer (Bach)

**Ergänzt:** M1, M3, M4, M5
**Zusätzliche Rollen:** [PFLICHT] Maschinist, [OPTIONAL] ATF (Schlauchlegen)
**Kombinierbar mit:** OPT-Tierrettung

**Besonderheit:** Ansaugbetrieb — TS muss angesaugt werden (max. Ansaughöhe ~7m).
Zweikanal-Betrieb: Betriebskanal (GF ↔ EL) + Wasserkanal (GF ↔ Maschinist).

---

## Zweikanal-Setup (vor M3 festlegen)

**Variante A — 1 Person, 2 Geräte:** GF trägt Gerät 1 auf Betriebskanal + Gerät 2 auf Wasserkanal.
**Variante B — 2 Personen:** GF auf Betriebskanal, TM dauerhaft auf Wasserkanal.

---

## M1

In Leitstellen-Alarmtext einfügen: „… Wasserversorgung über offenes Gewässer, Bach ca. 300 Meter östlich. …"

### Format A

| Wer | Spricht |
|-----|---------|
| **Leitstelle** | „Stallbrand in Flossenbürg. Unterstützung Wasserversorgung angefordert. Wasserversorgung über offenes Gewässer, Bach ca. 300 Meter östlich. Melden Sie sich bei EL Florian Flossenbürg 41/1. Ausrücken! Kommen" |
| **GF** | „Verstanden. Stallbrand Flossenbürg, Wasserversorgung Bach 300 Meter östlich, Meldung bei Florian Flossenbürg 41/1. Wir rücken aus. Ende" |

---

## M2

> Kein Ergänzung nötig — M2 ist Stärkemeldung bei EL Flossenbürg.
> Die Wasserquelle wird von der EL in M3 mitgeteilt.

---

## M3

Ersetzt den EL-Auftrag aus M3-Basis (Phase 1). Die GF→Trupp-Befehle (Phase 2) bleiben wie im OPT angegeben.

### Phase 0: EL nennt spezifische Wasserquelle (ersetzt M3-Basis Phase 1)

| Wer | Spricht |
|-----|---------|
| **EL** | „Florian Altenhammer 44/1 von Florian Flossenbürg 41/1, kommen" |
| **GF** | „Florian Flossenbürg 41/1 von Florian Altenhammer 44/1, kommen" |
| **EL** | „Florian Altenhammer 44/1, ihr übernehmt die Wasserversorgung. Bach 300 Meter östlich des Hofs. Schlauchleitung aufbauen, TS in Stellung. Kommen" |
| **GF** | „Verstanden. Wasserversorgung Bach 300 Meter östlich, TS in Stellung, Schlauchleitung aufbauen. Kommen" |
| **EL** | „Richtig. Meldung wenn bereit für Wasser marsch. Ende" |
| **GF** | „Verstanden. Ende" |

### Phase 1: Befehle auf Betriebskanal (GF → Trupp)

| Wer | Kanal | Spricht |
|-----|-------|---------|
| **GF** | [BETRIEBSKANAL] | „Angriffstrupp von Florian Altenhammer 44/1, kommen" |
| **ATF** | [BETRIEBSKANAL] | „Florian Altenhammer 44/1 von Angriffstrupp, kommen" |
| **GF** | [BETRIEBSKANAL] | „Angriffstrupp, Schlauchleitung vom Bach zur Einsatzstelle legen, 400 Meter. Kommen" |
| **ATF** | [BETRIEBSKANAL] | „Verstanden. Schlauchleitung Bach zur Einsatzstelle, 400 Meter. Kommen" |
| **GF** | [BETRIEBSKANAL] | „Richtig. Ende" |
| **GF** | [BETRIEBSKANAL] | „Maschinist von Florian Altenhammer 44/1, kommen" |
| **Ma** | [BETRIEBSKANAL] | „Florian Altenhammer 44/1 von Maschinist, kommen" |
| **GF** | [BETRIEBSKANAL] | „Maschinist, TS in Stellung bringen, Saugschlauch legen. Danach auf Wasserkanal wechseln. Kommen" |
| **Ma** | [BETRIEBSKANAL] | „Verstanden. TS in Stellung, Saugschlauch, dann Wasserkanal. Kommen" |
| **GF** | [BETRIEBSKANAL] | „Richtig. Ende" |

### Phase 2: Wasserkanal aktivieren

| Wer | Kanal | Spricht |
|-----|-------|---------|
| **GF** | [WASSERKANAL] | „Maschinist von Wasserführer, kommen" |
| **Ma** | [WASSERKANAL] | „Wasserführer von Maschinist, kommen" |
| **GF** | [WASSERKANAL] | „Wasserkanal aktiv. Bereit zum Ansaugen auf Kommando. Kommen" |
| **Ma** | [WASSERKANAL] | „Verstanden. Bereit. Kommen" |
| **GF** | [WASSERKANAL] | „Ende" |

### Format B — Rollenkarten

#### Rollenkarte: GF [PFLICHT]
**Betriebskanal:** ATF: Schlauchleitung 400m legen. Maschinist: TS in Stellung, Saugschlauch, dann Wasserkanal.
**Wasserkanal:** Maschinist bestätigen lassen.

#### Rollenkarte: Maschinist [PFLICHT]
1. Betriebskanal: TS in Stellung, Saugschlauch legen.
2. Auf Wasserkanal wechseln. Bereitschaft melden.

#### Rollenkarte: ATF [OPTIONAL]
Schlauchleitung 400m vom Bach zur Einsatzstelle legen.

---

## M4

Nach EL-Freigabe „Wasser marsch" (base M4 Phase 2): Wasserkanal koordinieren.

### Phase 1: Wasser marsch (Wasserkanal)

| Wer | Kanal | Spricht |
|-----|-------|---------|
| **GF** | [WASSERKANAL] | „Maschinist von Wasserführer, kommen" |
| **Ma** | [WASSERKANAL] | „Wasserführer von Maschinist, kommen" |
| **GF** | [WASSERKANAL] | „Schlauchleitung liegt. Wasser marsch! Kommen" |
| **Ma** | [WASSERKANAL] | „Verstanden. Wasser marsch! Ende" |

### Phase 2: Druckmeldung (Wasserkanal)

| Wer | Kanal | Spricht |
|-----|-------|---------|
| **Ma** | [WASSERKANAL] | „Wasserführer von Maschinist, kommen" |
| **GF** | [WASSERKANAL] | „Maschinist von Wasserführer, kommen" |
| **Ma** | [WASSERKANAL] | „Ausgangsdruck sieben Bar. Förderung läuft stabil. Kommen" |
| **GF** | [WASSERKANAL] | „Verstanden. Weiter so. Ende" |

### Format B — Rollenkarten

#### Rollenkarte: GF [PFLICHT]
**Wasserkanal:** Nach EL-Freigabe Wasser marsch an Maschinist. Druckmeldungen empfangen.

#### Rollenkarte: Maschinist [PFLICHT]
**Wasserkanal dauerhaft.** Wasser marsch ausführen. Druck nach ca. 2 Minuten melden.

---

## M5

Vor der Abmeldung: Wasser halt auf Wasserkanal.

### Format A

| Wer | Kanal | Spricht |
|-----|-------|---------|
| **GF** | [WASSERKANAL] | „Maschinist von Wasserführer, kommen" |
| **Ma** | [WASSERKANAL] | „Wasserführer von Maschinist, kommen" |
| **GF** | [WASSERKANAL] | „Wasser halt! Pumpe sichern. Kommen" |
| **Ma** | [WASSERKANAL] | „Verstanden. Wasser halt! Ende" |

In GF-Abmeldung ergänzen: „… Wasser halt, Schlauchleitung wird eingezogen, TS verladen. …"

**Rollenkarte: GF:** Erst Wasser halt (Wasserkanal), dann Abmeldung bei Leitstelle Neustadt.
**Rollenkarte: Maschinist [OPTIONAL]:** Wasser halt bestätigen, Pumpe sichern.

---

> **Format D:** Bewertet: richtiger Kanal für jeden Funkspruch, Kanalwechsel korrekt angekündigt, Wasser halt vor Abmeldung.
