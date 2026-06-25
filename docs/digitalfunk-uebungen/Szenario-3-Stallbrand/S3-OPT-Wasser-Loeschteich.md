# OPT: Wasserversorgung — Löschteich

**Ergänzt:** M1, M3, M4, M5
**Zusätzliche Rollen:** [PFLICHT] Maschinist, [OPTIONAL] ATF (Schlauchlegen)
**Kombinierbar mit:** OPT-Tierrettung

**Besonderheit:** Begrenzter Vorrat — Pegelüberwachung ist Pflicht.
Abbruchpegel (50 cm) festlegen und klar kommunizieren — sonst Trockenlauf der Pumpe!
Zweikanal-Betrieb wie OPT-Wasser-Bach.

---

## M1

In Leitstellen-Alarmtext einfügen: „… Wasserversorgung über Löschteich auf dem Hofgelände. …"

### Format A

| Wer | Spricht |
|-----|---------|
| **Leitstelle** | „Stallbrand in Flossenbürg, Hofstraße 12. Unterstützung Wasserversorgung angefordert. Wasserversorgung über Löschteich auf dem Hofgelände. Melden Sie sich bei EL Florian Flossenbürg 41/1. Ausrücken! Kommen" |
| **GF** | „Verstanden. Stallbrand Hofstraße 12 Flossenbürg, Wasserversorgung Löschteich Hofgelände, Meldung bei Florian Flossenbürg 41/1. Wir rücken aus. Ende" |

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
| **EL** | „Florian Altenhammer 44/1, ihr übernehmt die Wasserversorgung. Löschteich 80 Meter östlich des Hofs. TS aufbauen, Pegel überwachen, Abbruch bei unter 50 Zentimeter. Kommen" |
| **GF** | „Verstanden. Wasserversorgung Löschteich 80 Meter östlich, TS aufbauen, Pegel überwachen, Abbruch unter 50cm. Kommen" |
| **EL** | „Richtig. Meldung wenn bereit für Wasser marsch. Ende" |
| **GF** | „Verstanden. Ende" |

### Phase 1: Befehle auf Betriebskanal (GF → Trupp)

| Wer | Kanal | Spricht |
|-----|-------|---------|
| **GF** | [BETRIEBSKANAL] | „Angriffstrupp von Florian Altenhammer 44/1, kommen" |
| **ATF** | [BETRIEBSKANAL] | „Florian Altenhammer 44/1 von Angriffstrupp, kommen" |
| **GF** | [BETRIEBSKANAL] | „Angriffstrupp, Schlauchleitung vom Löschteich zur Einsatzstelle legen. Kommen" |
| **ATF** | [BETRIEBSKANAL] | „Verstanden. Schlauchleitung Löschteich zur Einsatzstelle. Kommen" |
| **GF** | [BETRIEBSKANAL] | „Richtig. Ende" |
| **GF** | [BETRIEBSKANAL] | „Maschinist von Florian Altenhammer 44/1, kommen" |
| **Ma** | [BETRIEBSKANAL] | „Florian Altenhammer 44/1 von Maschinist, kommen" |
| **GF** | [BETRIEBSKANAL] | „Maschinist, TS in Stellung, Saugschlauch legen. Pegel alle zwei Minuten auf Wasserkanal melden. Abbruch bei unter 50 Zentimeter. Danach auf Wasserkanal wechseln. Kommen" |
| **Ma** | [BETRIEBSKANAL] | „Verstanden. TS, Saugschlauch, Pegel alle zwei Minuten Wasserkanal, Abbruch unter 50cm, dann Wasserkanal. Kommen" |
| **GF** | [BETRIEBSKANAL] | „Richtig. Ende" |

### Phase 2: Wasserkanal aktivieren

| Wer | Kanal | Spricht |
|-----|-------|---------|
| **GF** | [WASSERKANAL] | „Maschinist von Wasserführer, kommen" |
| **Ma** | [WASSERKANAL] | „Wasserführer von Maschinist, kommen" |
| **GF** | [WASSERKANAL] | „Wasserkanal aktiv. Abbruchpegel 50 Zentimeter. Bereit auf Kommando. Kommen" |
| **Ma** | [WASSERKANAL] | „Verstanden. Abbruch unter 50cm, bereit. Kommen" |
| **GF** | [WASSERKANAL] | „Ende" |

### Format B — Rollenkarten

#### Rollenkarte: GF [PFLICHT]
**Betriebskanal:** ATF: Schlauchleitung legen. Maschinist: TS+Saugschlauch, Pegel alle 2min, Abbruch bei <50cm.
**Wasserkanal:** Abbruchpegel bestätigen lassen.

#### Rollenkarte: Maschinist [PFLICHT]
TS in Stellung, Saugschlauch. Dann Wasserkanal. **Pegel alle 2 Minuten melden. Abbruch bei <50cm.**

#### Rollenkarte: ATF [OPTIONAL]
Schlauchleitung vom Löschteich zur Einsatzstelle legen.

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

### Phase 2: Pegelmeldungen (alle 2 Minuten)

| Wer | Kanal | Spricht |
|-----|-------|---------|
| **Ma** | [WASSERKANAL] | „Wasserführer von Maschinist, kommen" |
| **GF** | [WASSERKANAL] | „Maschinist von Wasserführer, kommen" |
| **Ma** | [WASSERKANAL] | „Pegel jetzt 1,0 Meter. Förderung stabil. Kommen" |
| **GF** | [WASSERKANAL] | „Verstanden. Weiter beobachten. Ende" |

### Phase 3: Kritischer Pegel — Vorabwarnung

| Wer | Kanal | Spricht |
|-----|-------|---------|
| **Ma** | [WASSERKANAL] | „Wasserführer von Maschinist, kommen" |
| **GF** | [WASSERKANAL] | „Maschinist von Wasserführer, kommen" |
| **Ma** | [WASSERKANAL] | „Pegel 60 Zentimeter. Nähere mich Abbruchpegel. Kommen" |
| **GF** | [WASSERKANAL] | „Verstanden. Weiter beobachten, bei 50cm sofort melden. Ende" |
| **GF** | [BETRIEBSKANAL] | „Florian Flossenbürg 41/1 von Florian Altenhammer 44/1, kommen" |
| **EL** | [BETRIEBSKANAL] | „Florian Altenhammer 44/1 von Florian Flossenbürg 41/1, kommen" |
| **GF** | [BETRIEBSKANAL] | „Löschteich-Pegel kritisch. Noch ca. fünf Minuten Förderung möglich. Alternative Versorgung erforderlich. Kommen" |
| **EL** | [BETRIEBSKANAL] | „Verstanden. Tanklöschfahrzeug ist unterwegs. Noch drei Minuten. Ende" |
| **GF** | [BETRIEBSKANAL] | „Verstanden. Ende" |

### Format B — Rollenkarten

#### Rollenkarte: GF [PFLICHT]
**Wasserkanal:** Wasser marsch. Pegelmeldungen empfangen. Bei 50cm: Wasser halt vorbereiten.
**Betriebskanal:** Bei kritischem Pegel EL vorwarnen.

#### Rollenkarte: Maschinist [PFLICHT]
**Wasserkanal dauerhaft.** Wasser marsch. Pegel alle 2min. Bei 60cm: Vorabwarnung. Bei 50cm: sofort melden.

#### Rollenkarte: EL [bereits in Basis]
**Betriebskanal.** Pegelwarnung empfangen. TLF als Alternative anbieten.

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

---

> **Format D Besonderheit:** Abbruchpegel muss klar und quittiert werden — Trockenlauf vermeiden!
