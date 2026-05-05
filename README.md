# Laser Test Companion

> Demo-Projekt zur Testautomatisierung eines medizintechnischen Lasersystems.
> Gebaut für die Bewerbung als **(Junior) Softwareentwickler (m/w/d) Testautomatisierung** bei **EXCO GmbH**, Standort Jena oder Frankenthal, Team IT Solutions.

Das Projekt simuliert den Arbeitsalltag eines Junior-Testers bei EXCO:
GUI-Tests in Python mit **Squish**, Bug-Tracking in **Jira**, Code-Verwaltung mit **SVN**, agile Sprints, und **IEC 62304** Compliance — alles in einer kleinen, lauffähigen Web-Anwendung.

---

## Schnellstart in 30 Sekunden

```bash
make install     # einmalig: Abhängigkeiten installieren
make run         # Server starten + Browser öffnet sich
```

Browser geht automatisch auf `http://localhost:8000` auf.

Tests laufen mit:

```bash
make test        # alle 16 pytest-Tests
```

---

## Alle Make-Befehle auf einen Blick

| Befehl            | Was er macht                                              |
|-------------------|-----------------------------------------------------------|
| `make help`       | Zeigt alle Befehle (Standard, wenn man nur `make` schreibt). |
| `make install`    | Installiert die Python-Abhängigkeiten.                    |
| `make run`        | Startet den Server und öffnet automatisch den Browser.    |
| `make dev`        | Startet den Server mit Auto-Reload (für Entwicklung).     |
| `make open`       | Öffnet nur den Browser (wenn der Server schon läuft).     |
| `make test`       | Führt alle 16 pytest-Tests aus.                           |
| `make smoke`      | Schneller API-Smoke-Test ohne laufenden Server.           |
| `make clean`      | Räumt Cache-Dateien auf (`__pycache__`, `.pytest_cache`). |
| `make tree`       | Listet die ganze Projektstruktur.                         |

---

## Projektstruktur

```
laser-test-companion/
│
├── Makefile                    ← Make-Befehle (make run, make test, ...)
├── README.md                   ← diese Datei
├── main.py                     ← FastAPI-App-Start, öffnet Browser automatisch
│
├── data/                       ← JSON-Dateien als „Datenbank"
│   ├── test_cases.json             • 4 Testfälle (TC-1042, TC-1118, TC-1203, TC-1255)
│   ├── bugs.json                   • 5 Bugs (BUG-820, BUG-844, BUG-851, BUG-862, BUG-887)
│   ├── requirements.json           • 4 Anforderungen (REQ-SUI-12, REQ-CAL-07, REQ-SAFETY-03, REQ-IMG-15)
│   ├── test_runs.json              • 10 letzte CI-Läufe (für Trend-Chart)
│   └── sprint.json                 • Sprint 14 mit 8 Stories
│
├── models/                     ← Pydantic-Modelle (Daten-Validierung)
│   ├── __init__.py
│   ├── test_case.py                • TestCase, TestCaseCreate
│   ├── bug.py                      • Bug, BugCreate, BugStatusUpdate
│   └── requirement.py              • Requirement
│
├── routes/                     ← FastAPI-Routen (das Backend)
│   ├── __init__.py
│   ├── storage.py                  • load() / save() für JSON-Dateien
│   ├── test_cases.py               • GET/POST/PUT /api/test-cases
│   ├── bugs.py                     • GET/POST/PUT /api/bugs
│   ├── runs.py                     • POST /api/run + GET /api/runs/trend
│   ├── traceability.py             • GET /api/requirements, /api/traceability, /api/stats
│   └── simulator.py                • GET/PUT /api/sprint
│
├── static/
│   └── app.js                  ← Alpine.js-Komponenten + Fetch-Calls + Animation
│
├── templates/
│   └── index.html              ← Single-Page-App mit Sidebar + 5 Ansichten
│
├── tests/                      ← 16 pytest-Tests in 4 Dateien
│   ├── __init__.py
│   ├── conftest.py                 • macht das Projekt importierbar
│   ├── test_squish_runner.py       • 5 Tests (PASS-/FAIL-Szenarien)
│   ├── test_traceability.py        • 4 Tests (RTM, CSV-Export)
│   ├── test_bug_workflow.py        • 4 Tests (Status, Release-Blocker)
│   └── test_sprint_logic.py        • 3 Tests (Story-Points, Burndown)
│
└── docs/                       ← Dokumentation auf Deutsch
    ├── PROJEKT_BERICHT.md          • Komplette A2-Erklärung + Interview-Q&A + 4-Min-Vortrag
    ├── TEST_CASE_VORLAGE.md        • Vorlage für einen Testfall (befüllt mit TC-1042)
    ├── IEC62304_PROZESS.md         • Erklärung der Norm IEC 62304
    └── SPRINT_GUIDE.md             • Wie ein 2-Wochen-Sprint abläuft
```

---

## Die fünf Ansichten der Anwendung

### 1. Übersicht & Pipeline
- Vier Statistik-Karten (Aktive Testfälle 142, Tests bestanden 118/142, Offene Bugs 7, Sprint 50 %).
- **Großes Pipeline-Diagramm** mit 5 Schichten: Auslöser → Anforderung → Squish → Test-Ausführung (Pass/Fail-Raute) → Report → IEC-62304-Freigabe.
- Sprint-Fortschrittsleiste, Teamstruktur-Baum.

### 2. Test Case Manager
- Filter nach Modul und Status.
- Vier Testfall-Karten (TC-1042 Pass, TC-1118 Pass, TC-1203 Fail+Bug, TC-1255 WIP).
- Detail-Modal mit Schritten, Object-Map und Squish-Skript.
- "+ Neuen Testfall anlegen" speichert wirklich in `data/test_cases.json`.

### 3. Squish Simulator
- Testfall wählen, AUT-Modus (Attachable / Auto-Start), "▶ Test ausführen".
- Live-Konsole animiert die Schritte alle 350 ms.
- TC-1042 → PASS · TC-1203 → FAIL + automatischer Bug BUG-887.
- Manuell vs. automatisch Vergleich (~96 % Zeitersparnis).
- Trend-Chart der letzten 10 CI-Läufe.

### 4. Bug Tracking (Jira)
- Kanban-Board mit 5 Spalten (OPEN, IN PROGRESS, IN REVIEW, IN TEST, CLOSED).
- 5 Demo-Bugs vorgeladen.
- Bug-Report-Formular (Beschreibung in Englisch — wie bei EXCO Standard).
- Bug-Workflow-Diagramm + 3 Statistik-Karten.

### 5. Traceability & Sprint
- **Requirements Traceability Matrix (RTM)** nach IEC 62304 §5.7.1.
- IEC-62304-Lebenszyklus als Kreisdiagramm (Schritt 7 pulsiert).
- Sprint-14-Backlog (TO DO / IN PROGRESS / DONE) mit Story-Points-Badges.
- Scrum-Ceremonies-Zeitlinie über 14 Tage.

---

## Backend-Endpoints (FastAPI)

| Endpoint                                | Was er macht                              |
|-----------------------------------------|-------------------------------------------|
| `GET  /`                                | liefert `templates/index.html`            |
| `GET  /api/stats`                       | Dashboard-Zahlen                          |
| `GET  /api/test-cases`                  | alle Testfälle                            |
| `GET  /api/test-cases/{id}`             | ein Testfall                              |
| `POST /api/test-cases`                  | neuen Testfall anlegen                    |
| `PUT  /api/test-cases/{id}`             | Testfall aktualisieren                    |
| `POST /api/run`                         | Squish-Lauf simulieren (PASS / FAIL)      |
| `GET  /api/runs/trend`                  | letzte 10 CI-Läufe                        |
| `GET  /api/bugs`                        | alle Bugs                                 |
| `POST /api/bugs`                        | neuen Bug anlegen (geht in OPEN)          |
| `PUT  /api/bugs/{id}`                   | Bug-Status ändern (Spaltenwechsel)        |
| `GET  /api/requirements`                | alle Anforderungen                        |
| `GET  /api/traceability`                | komplette RTM                             |
| `GET  /api/sprint`                      | aktueller Sprint                          |
| `PUT  /api/sprint/story/{id}`           | Story-Status TODO/IN_PROGRESS/DONE        |

---

## Wie passt das zur Stellenanzeige?

| Stellenanforderung                                     | Im Projekt umgesetzt durch                              |
|--------------------------------------------------------|---------------------------------------------------------|
| Python-GUI-Tests für ein Lasersystem                   | Squish Simulator + Test Case Manager (Seiten 2 + 3)     |
| Test-Frameworks aufbauen und erweitern                 | `routes/` + `models/` + `static/app.js`                 |
| Anforderungen mit automatisierten Tests prüfen         | RTM auf Seite 5, 16 pytest-Tests                        |
| Tests am Gerät im Labor                                | AUT-Modus „Attachable" simuliert echtes Lasersystem     |
| Reporting im Bug-Tracking-System                       | Bug-Tracking-Seite (Seite 4) mit komplettem Jira-Workflow |
| Dokumentation auf Englisch                             | Alle Bug-Beschreibungen sind in Englisch verfasst       |
| Agile Vorgehensmodelle                                 | Sprint-14-Backlog + Scrum-Zeitlinie auf Seite 5         |
| Python-Kenntnisse                                      | Backend zu 100 % in Python (FastAPI)                    |
| Jira-Erfahrung                                         | Kanban mit 5 Spalten + Bug-Report-Formular              |
| SVN                                                    | Im Pipeline-Diagramm und Sprint-Dokumentation referenziert |
| Squish                                                 | Eigene Seite mit Skript-Vorschau und Live-Lauf          |

---

## Technischer Stack

- **Backend:** Python 3.10+, **FastAPI**, **Pydantic**, uvicorn
- **Frontend:** HTML, CSS, **Tailwind CSS** (CDN), **Alpine.js** (CDN)
- **Persistenz:** JSON-Dateien in `data/` (keine externe Datenbank)
- **Tests:** **pytest** + FastAPI `TestClient`
- **Build-Tools:** keine (drei Befehle und es läuft)

---

## Doku im `docs/`-Ordner

- **`PROJEKT_BERICHT.md`** — der Hauptbericht für das Vorstellungsgespräch:
  EXCO-Hintergrund, Stellenanzeige Wort für Wort erklärt, Arbeitstag-Story,
  alle Begriffe (Squish, AUT, IEC 62304 ...), komplette UI-Tour, **30 Interview-Fragen mit Antworten**, **6 Fragen für die Firma**, **4-Minuten-Vortrag**. Alles in A2-Deutsch.
- **`TEST_CASE_VORLAGE.md`** — Vorlage für einen Testfall, ausgefüllt mit TC-1042.
- **`IEC62304_PROZESS.md`** — Erklärung der Norm IEC 62304 (Klassen A/B/C, RTM, ISO 13485, ISO 14971).
- **`SPRINT_GUIDE.md`** — wie ein 2-Wochen-Sprint im Team IT Solutions abläuft.

---

## Über die Stelle

- **Firma:** EXCO GmbH (gegründet 1994, ~150 Mitarbeiter, 8 Standorte).
- **Standort:** Jena (in der Nähe von Carl Zeiss Meditec) oder Frankenthal (Pfalz).
- **Team:** IT Solutions.
- **Branche:** Medizintechnik (ophthalmologische Laserchirurgie).
- **Kontakt:** Sarah Gogel — `sarah.gogel@exco-group.com` — `+49 6233 73778-373`.
- **Zertifizierungen:** DIN EN ISO 9001:2015, DIN EN ISO 13485:2016.

---

## Lizenz

MIT — Anas Haj Naeif, 2026.
