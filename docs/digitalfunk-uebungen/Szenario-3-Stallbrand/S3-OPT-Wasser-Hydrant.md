# OPT: Wasserversorgung — Hydrant

**Ergänzt:** M1, M3, M4, M5
**Zusätzliche Rollen:** [PFLICHT] Maschinist, [OPTIONAL] ATF (Schlauchlegen)
**Kombinierbar mit:** OPT-Tierrettung

**Besonderheit:** Druckspeisung — kein Ansaugvorgang, schnellere Bereitschaft.
Hydrantendruck kann schwanken — Abbruchkriterium (<3 Bar) kommunizieren.
Zweikanal-Betrieb wie OPT-Wasser-Bach.

---

## M1

In Leitstellen-Alarmtext einfügen: „… Wasserversorgung über Hydranten, nächster Hydrant Kreuzung Dorfstraße. …"

### Format A

| Wer | Spricht |
|-----|---------|
| **Leitstelle** | „Stallbrand in Flossenbürg. Unterstützung Wasserversorgung angefordert. Wasserversorgung über Hydranten, nächster Hydrant Kreuzung Dorfstraße. Melden Sie sich bei EL Florian Flossenbürg 41/1. Ausrücken! Kommen" |
| **GF** | „Verstanden. Stallbrand Flossenbürg, Wasserversorgung Hydrant Kreuzung Dorfstraße, Meldung bei Florian Flossenbürg 41/1. Wir rücken aus. Ende" |

---

## M2

> Kein Ergänzung nötig — M2 ist Stärkemeldung bei EL Flossenbürg.
> Die Wasserquelle wird von der EL in M3 mitgeteilt.

---

## M3

Ersetzt den EL-Auftrag aus M3-Basis (Phase 1).

### Phase 0: EL nennt spezifische Wasserquelle (ersetzt M3-Basis Phase 1)

| Wer | Spricht |
|-----|---------|
| **EL** | „Florian Altenhammer 44/1 von Florian Flossenbürg 41/1, kommen" |
| **GF** | „Florian Flossenbürg 41/1 von Florian Altenhammer 44/1, kommen" |
| **EL** | „Florian Altenhammer 44/1, ihr übernehmt die Wasserversorgung. Hydrant Kreuzung Dorfstraße, 200 Meter. B-Schlauch legen, Hydrant anschließen. Kommen" |
| **GF** | „Verstanden. Wasserversorgung Hydrant Kreuzung Dorfstraße, 200 Meter, B-Schlauch. Kommen" |
| **EL** | „Richtig. Meldung wenn bereit für Wasser marsch. Ende" |
| **GF** | „Verstanden. Ende" |

### Phase 1: Befehle auf Betriebskanal (GF → Trupp)

| Wer | Kanal | Spricht |
|-----|-------|---------|
| **GF** | [BETRIEBSKANAL] | „Angriffstrupp von Florian Altenhammer 44/1, kommen" |
| **ATF** | [BETRIEBSKANAL] | „Florian Altenhammer 44/1 von Angriffstrupp, kommen" |
| **GF** | [BETRIEBSKANAL] | „Angriffstrupp, B-Schlauch vom Hydranten Dorfstraße zur Einsatzstelle legen, 200 Meter. Kommen" |
| **ATF** | [BETRIEBSKANAL] | „Verstanden. B-Schlauch Hydrant Dorfstraße, 200 Meter. Kommen" |
| **GF** | [BETRIEBSKANAL] | „Richtig. Ende" |
| **GF** | [BETRIEBSKANAL] | „Maschinist von Florian Altenhammer 44/1, kommen" |
| **Ma** | [BETRIEBSKANAL] | „Florian Altenhammer 44/1 von Maschinist, kommen" |
| **GF** | [BETRIEBSKANAL] | „Maschinist, Hydrant anschließen. Nach Fertigstellung auf Wasserkanal wechseln. Kommen" |
| **Ma** | [BETRIEBSKANAL] | „Verstanden. Hydrant anschließen, dann Wasserkanal. Kommen" |
| **GF** | [BETRIEBSKANAL] | „Richtig. Ende" |

### Phase 2: Wasserkanal aktivieren

| Wer | Kanal | Spricht |
|-----|-------|---------|
| **GF** | [WASSERKANAL] | „Maschinist von Wasserführer, kommen" |
| **Ma** | [WASSERKANAL] | „Wasserführer von Maschinist, kommen" |
| **GF** | [WASSERKANAL] | „Wasserkanal aktiv. Bereit für Wasser marsch auf Kommando. Kommen" |
| **Ma** | [WASSERKANAL] | „Verstanden. Bereit. Kommen" |
| **GF** | [WASSERKANAL] | „Ende" |

### Format B — Rollenkarten

#### Rollenkarte: GF [PFLICHT]
**Betriebskanal:** ATF: B-Schlauch 200m legen. Maschinist: Hydrant anschließen, dann Wasserkanal.
**Wasserkanal:** Maschinist bestätigen lassen.

#### Rollenkarte: Maschinist [PFLICHT]
Betriebskanal: Hydrant anschließen. Dann Wasserkanal wechseln. Bereitschaft melden.

#### Rollenkarte: ATF [OPTIONAL]
B-Schlauch 200m vom Hydranten Dorfstraße zur Einsatzstelle legen.

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
| **Ma** | [WASSERKANAL] | „Ausgangsdruck fünf Bar. Hydrantendruck schwankt leicht. Kommen" |
| **GF** | [WASSERKANAL] | „Verstanden. Druckschwankung beobachten. Bei Abfall unter drei Bar sofort melden. Ende" |

### Format B — Rollenkarten

#### Rollenkarte: GF [PFLICHT]
**Wasserkanal:** Nach EL-Freigabe Wasser marsch. Druckmeldungen empfangen. Bei <3 Bar: EL informieren.

#### Rollenkarte: Maschinist [PFLICHT]
**Wasserkanal dauerhaft.** Wasser marsch ausführen. Druck melden. Schwankungen sofort melden.

---

## M5

Vor der Abmeldung: Wasser halt auf Wasserkanal.

### Format A

| Wer | Kanal | Spricht |
|-----|-------|---------|
| **GF** | [WASSERKANAL] | „Maschinist von Wasserführer, kommen" |
| **Ma** | [WASSERKANAL] | „Wasserführer von Maschinist, kommen" |
| **GF** | [WASSERKANAL] | „Wasser halt! Hydrant schließen. Kommen" |
| **Ma** | [WASSERKANAL] | „Verstanden. Wasser halt! Ende" |

In GF-Abmeldung ergänzen: „… Wasser halt, Schlauchleitung eingezogen. Wir rücken ein. …"

---

> **Format D Besonderheit:** Hydrantendruck kann schwanken — Abbruchkriterium (<3 Bar) klar kommunizieren.
