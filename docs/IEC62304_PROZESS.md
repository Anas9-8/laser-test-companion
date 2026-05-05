# IEC 62304 — Software-Lebenszyklus für Medizinprodukte

Kurzer Überblick darüber, was IEC 62304 von uns verlangt und wie das im
Alltag bei EXCO aussieht. Geschrieben aus der Perspektive der
Testautomatisierung.

## Worum es geht

IEC 62304 ist die internationale Norm für den Software-Lebenszyklus von
Medizinprodukten. Sie schreibt vor, wie Software für medizinische Geräte
geplant, entwickelt, getestet, freigegeben und gewartet werden muss. Wer
ein Medizinprodukt mit Software in Europa oder den USA in Verkehr bringen
will, kommt nicht daran vorbei.

Die Norm steht nicht alleine. Sie wird ergänzt durch:

- **ISO 13485** — Qualitätsmanagementsystem für Medizinprodukte.
- **ISO 14971** — Risikomanagement für Medizinprodukte.
- **EU MDR (2017/745)** — Medical Device Regulation in Europa.
- **FDA 21 CFR 820.30** — Design Controls für den US-Markt.

## Software-Sicherheitsklassen

IEC 62304 teilt Software in drei Klassen ein. Die Klasse hängt davon ab,
was passiert, wenn die Software versagt.

| Klasse | Mögliche Auswirkung           | Beispiel im Lasersystem        |
|--------|-------------------------------|--------------------------------|
| A      | Keine Verletzung möglich      | Help-System, Sprach-Auswahl    |
| B      | Verletzung, nicht lebensbedrohlich | Patientendaten-Eingabe   |
| C      | Tod oder schwere Verletzung   | Notabschaltung, Laser-Energie  |

Je höher die Klasse, desto strenger sind die Anforderungen an Doku,
Verifikation und Risikoanalyse. Klasse C heißt: jede Anforderung braucht
mindestens einen Test, jede Architekturentscheidung muss begründet sein
und jede Änderung wird vollständig nachvollzogen.

## Lebenszyklus-Phasen

1. **Software Development Planning** — Wer macht was, mit welchen Tools?
2. **Software Requirements Analysis** — User Needs → System Reqs → Software Reqs.
3. **Software Architectural Design** — Module, Schnittstellen, Datenflüsse.
4. **Software Detailed Design** — Klassen, Funktionen, Algorithmen.
5. **Software Unit Implementation & Verification** — Code + Unit-Tests.
6. **Software Integration & Integration Testing** — Module zusammen testen.
7. **Software System Testing** — Unsere Hauptarbeit: GUI-Tests mit Squish.
8. **Software Release** — Freigabe durch QA und Compliance.

Parallel dazu laufen drei Begleitprozesse:

- **Software Configuration Management** (bei uns SVN).
- **Software Problem Resolution** (bei uns Jira).
- **Software Risk Management** (nach ISO 14971).

## Verfolgbarkeit (Traceability)

Das Herzstück der Compliance ist die **Requirements Traceability Matrix
(RTM)**. Sie verbindet jede User-Anforderung lückenlos bis zum
ausgeführten Test:

```
User Need → System Req → Software Req → Architecture → Code → Test → Risk Control
```

Eine einzige Lücke in dieser Kette bedeutet: nicht zulassungsfähig.
Deshalb pflegen wir die Matrix kontinuierlich und automatisieren ihre
Erzeugung aus Jira und SVN.

## Was das für die Testautomatisierung heißt

- Jeder GUI-Test referenziert eine REQ-ID.
- Klasse-C-Anforderungen werden zuerst getestet und am häufigsten in CI
  ausgeführt.
- Ein Failure auf einer Klasse-C-Anforderung blockiert das Release.
- Bug-Tickets müssen die Klasse der betroffenen Anforderung mitführen.
- Reports werden archiviert (mindestens für die Lebensdauer des Produkts).

## Typische Artefakte

- Testplan (Word/PDF, signiert)
- Testprotokolle (JUnit-XML aus Squish)
- Testbericht (zusammenfassend, pro Release)
- Risk Management File (ISO 14971)
- Verifikations- und Validierungsbericht
- RTM (CSV oder Excel)
- Audit-Trail (SVN-History + Jira-History)
