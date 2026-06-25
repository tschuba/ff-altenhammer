# OPT: Einsatzstellenbeleuchtung (Nachteinsatz)

**Ergänzt:** M1 (Alarm), M2 (Lagemeldung), M3 (Befehlsgebung), M4 (Einsatzabwicklung), M5 (Abmeldung)
**Zusätzliche Rollen:** [PFLICHT] WTF (Beleuchtungsaufbau)
**Kombinierbar mit:** Basis-Szenario S1

**Kontext:** Sturmschaden bei Nacht. Rettungsdienst ist ebenfalls alarmiert und vor Ort —
er benötigt Ausleuchtung des Arbeitsbereichs, während FF den Baum räumt.

---

## M1

Alarm ergänzen: Nacht + RD benötigt Beleuchtung.

### Format A

| Wer | Spricht |
|-----|---------|
| **Leitstelle** | „Sturmschaden, Baum auf Fahrbahn, Staatsstraße 2395, Höhe Waldrand bei Altenhammer. Fahrbahn blockiert. Rettungsdienst ist vor Ort, benötigt Einsatzstellenbeleuchtung. Ausrücken! Kommen" |
| **GF** | „Verstanden. Sturmschaden, Baum St2395, Waldrand Altenhammer. RD vor Ort, Beleuchtung erforderlich. Wir rücken aus. Ende" |

### Rollenkarte: Leitstelle — Ergänzung
„Rettungsdienst ist vor Ort, benötigt Einsatzstellenbeleuchtung" zum Alarm ergänzen.

### Rollenkarte: GF — Ergänzung
Merke: Zwei Aufgaben gleichzeitig — Baum räumen UND Beleuchtung aufbauen.

---

## M2

Lagemeldung ergänzen: Nacht, schlechte Sicht, RD-Bedarf.

### Format A

| Wer | Spricht |
|-----|---------|
| **GF** | „… Schlechte Sichtverhältnisse, Nachteinsatz. Rettungsdienst ist vor Ort und benötigt Ausleuchtung des Arbeitsbereichs. Räumung und Beleuchtungsaufbau laufen parallel. Kommen" |
| **Leitstelle** | „Verstanden. Straßenmeisterei ist informiert. Ende" |

### Rollenkarte: GF — Ergänzung
Melde zusätzlich: Nacht, schlechte Sicht, RD braucht Beleuchtung, beides läuft parallel.

---

## M3

WTF-Befehl für Beleuchtungsaufbau hinzufügen. Läuft parallel zur Räumung durch ATF.

### Format A

| Wer | Spricht |
|-----|---------|
| **GF** | „Wassertrupp von Florian Altenhammer 44/1, kommen" |
| **WTF** | „Florian Altenhammer 44/1 von Wassertrupp, kommen" |
| **GF** | „Wassertrupp, Lichtmast und Flutlichtstrahler aufbauen, RD-Arbeitsbereich ausleuchten. Notstromaggregat starten. Kein Licht in Fahrtrichtung. Kommen" |
| **WTF** | „Verstanden. Lichtmast, Flutlicht, RD-Bereich, Nosta starten, kein Licht in Fahrtrichtung. Kommen" |
| **GF** | „Richtig. Ausführen. Ende" |

### Rollenkarte: GF — Ergänzung
**WTF:** Lichtmast + Flutlicht aufbauen, RD-Bereich ausleuchten, Notstromaggregat starten.
Sicherheitshinweis im Befehl: kein Licht in Fahrtrichtung.

### Rollenkarte: WTF [PFLICHT]
Lichtmast und Flutlichtstrahler aufbauen. Notstromaggregat starten. RD-Bereich ausleuchten.
**Wichtig: Licht nicht in Fahrtrichtung richten — Blendgefahr für Verkehr!**
Melde Fertigstellung an GF.

---

## M4

Beleuchtungs-Fertigmeldung + Blendschutz-Check einbauen. Läuft parallel zur Räumungs-Abwicklung.

### Format A

#### WTF meldet Beleuchtung fertig

| Wer | Spricht |
|-----|---------|
| **WTF** | „Florian Altenhammer 44/1 von Wassertrupp, kommen" |
| **GF** | „Wassertrupp von Florian Altenhammer 44/1, kommen" |
| **WTF** | „Lichtmast steht, Notstromaggregat läuft, Licht ein. RD-Bereich ausgeleuchtet. Kommen" |
| **GF** | „Verstanden. Ausrichtung prüfen — kein Blendlicht in Fahrtrichtung. Ende" |

#### WTF bestätigt Ausrichtung (nach kurzer Pause)

| Wer | Spricht |
|-----|---------|
| **WTF** | „Florian Altenhammer 44/1 von Wassertrupp, kommen" |
| **GF** | „Wassertrupp von Florian Altenhammer 44/1, kommen" |
| **WTF** | „Ausrichtung geprüft. Kein Blendlicht in Fahrtrichtung. RD bestätigt ausreichende Ausleuchtung. Kommen" |
| **GF** | „Verstanden. Stellung halten. Ende" |

### Rollenkarte: WTF [PFLICHT]
1. Melde wenn Lichtmast steht, Nosta läuft, Licht ein.
2. Prüfe auf GF-Anweisung: kein Blendlicht in Fahrtrichtung.
3. Melde Ergebnis und Feedback des RD.

### Rollenkarte: GF — Ergänzung
Empfange WTF-Fertigmeldung. Anweisung zur Blendschutz-Prüfung geben. Ergebnis abwarten.

---

## M5

Abmeldung ergänzen: Beleuchtung abgebaut.

In GF-Abmeldung aufnehmen:
> „… Fahrbahn geräumt, Beleuchtung abgebaut, Übergabe an Straßenmeisterei. Wir rücken ein. …"

### Format A

| Wer | Spricht |
|-----|---------|
| **GF** | „Florian Altenhammer 44/1, Einsatz beendet. Fahrbahn geräumt, Beleuchtung abgebaut. Übergabe an Straßenmeisterei. Wir rücken ein. Kommen" |
| **Leitstelle** | „Verstanden. Florian Altenhammer 44/1 einrücken. Ende" |
| **GF** | „Ende" |

---

> **Format D:** Bewertet: Blendschutz-Hinweis im Befehl, RD-Feedback eingeholt, Beleuchtung in Abmeldung erwähnt.
