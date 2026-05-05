# Laser Test Companion

> Demo-Projekt zur Testautomatisierung eines medizintechnischen Lasersystems.

---

## Live-Demo

![Laser Test Companion — Walkthrough durch alle 5 Ansichten](assets/demo.gif)

Das GIF zeigt einen kompletten Durchlauf durch die Anwendung — von der Anforderung bis zur Compliance-Freigabe.

> **Aufnahme erstellen:**
> ```bash
> make gif-deps    # einmalig: Playwright installieren
> make run         # Terminal 1: Server starten
> make demo        # Terminal 2: Auto-Walkthrough (währenddessen Bildschirm aufnehmen)
> ```
> Die Aufnahme als `assets/demo.gif` speichern. `make gif-help` zeigt die volle Anleitung.

### Was im GIF zu sehen ist (Workflow von oben nach unten)

| Sek.  | Ansicht                     | Was passiert                                                                 |
|-------|------------------------------|------------------------------------------------------------------------------|
| 0–6   | **1 — Übersicht & Pipeline**  | 4 Statistikkarten (142 / 118 / 7 / 50 %) und das große End-to-End-Diagramm: Auslöser → Anforderung → Squish → **Test-Ausführung (Pass/Fail-Raute)** → Report → Compliance. |
| 6–16  | **2 — Test Case Manager**     | 4 reale Testfälle (TC-1042, TC-1118, TC-1203, TC-1255) als Karten. Detail-Modal öffnet sich mit Schritten, Object-Map und Squish-Skript. |
| 16–30 | **3 — Squish Simulator**      | TC-1042 wird ausgeführt → **PASS** (animierte Konsole). Dann TC-1203 → **FAIL** mit automatisch erzeugtem Bug **BUG-887** und Screenshot-Pfad. |
| 30–40 | **4 — Bug Tracking (Jira)**   | Kanban-Board mit 5 Spalten (OPEN / IN PROGRESS / IN REVIEW / IN TEST / CLOSED). Bug-Workflow-Diagramm und Bug-Report-Formular (Beschreibung auf Englisch). |
| 40–55 | **5 — Traceability & Sprint** | RTM-Tabelle (Risikoklasse C rot markiert), IEC-62304-Lebenszyklus als Kreis (Schritt 7 pulsiert), Sprint-14-Backlog mit Story-Points und 14-Tage-Scrum-Zeitlinie. |
| 55+   | **Zurück zur Übersicht**      | Schließt den Kreis — das ist der ganze Workflow eines Junior-Testers bei EXCO. |

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
| `make gif-deps`   | Playwright installieren (einmalig für Demo-Aufnahme).     |
| `make demo`       | Auto-Walkthrough durch alle 5 Seiten (für Bildschirmaufnahme). |
| `make gif-help`   | Zeigt die komplette Anleitung zum Aufnehmen des Demo-GIFs.|
| `make github-init`| Erstellt GitHub-Repo mit `gh` CLI und pusht.              |
| `make push`       | Pusht aktuellen Stand nach `origin main`.                 |
| `make status`     | Zeigt `git status`.                                       |

---

## Projektstruktur

```
laser-test-companion/
│
├── Makefile                    ← Make-Befehle (make run, make test, make demo, ...)
├── README.md                   ← diese Datei
├── .gitignore                  ← schließt Cache, .claude*, persönliche Notizen aus
├── main.py                     ← FastAPI-App-Start, öffnet Browser automatisch
│
├── assets/                     ← Demo-GIF und sonstige Medien
│   └── demo.gif                    • Walkthrough durch alle 5 Ansichten
│
├── data/                       ← JSON-Dateien als „Datenbank"
│   ├── test_cases.json             • 4 Testfälle (TC-1042, TC-1118, TC-1203, TC-1255)
│   ├── bugs.json                   • 5 Bugs (BUG-820, BUG-844, BUG-851, BUG-862, BUG-887)
│   ├── requirements.json           • 4 Anforderungen (REQ-SUI-12, REQ-CAL-07, REQ-SAFETY-03, REQ-IMG-15)
│   ├── test_runs.json              • 10 letzte CI-Läufe (für Trend-Chart)
│   └── sprint.json                 • Sprint 14 mit 8 Stories
│
├── models/                     ← Pydantic-Modelle (Daten-Validierung)
│   ├── test_case.py                • TestCase, TestCaseCreate
│   ├── bug.py                      • Bug, BugCreate, BugStatusUpdate
│   └── requirement.py              • Requirement
│
├── routes/                     ← FastAPI-Routen (das Backend)
│   ├── storage.py                  • load() / save() für JSON-Dateien
│   ├── test_cases.py               • GET/POST/PUT /api/test-cases
│   ├── bugs.py                     • GET/POST/PUT /api/bugs
│   ├── runs.py                     • POST /api/run + GET /api/runs/trend
│   ├── traceability.py             • GET /api/requirements, /api/traceability, /api/stats
│   └── simulator.py                • GET/PUT /api/sprint
│
├── scripts/                    ← Helfer-Skripte
│   └── demo_walkthrough.py         • Playwright-Auto-Demo durch alle 5 Seiten
│
├── static/
│   └── app.js                  ← Alpine.js-Komponenten + Fetch-Calls + Animation
│
├── templates/
│   └── index.html              ← Single-Page-App mit Sidebar + 5 Ansichten
│
├── tests/                      ← 16 pytest-Tests in 4 Dateien
│   ├── conftest.py                 • macht das Projekt importierbar
│   ├── test_squish_runner.py       • 5 Tests (PASS-/FAIL-Szenarien)
│   ├── test_traceability.py        • 4 Tests (RTM, CSV-Export)
│   ├── test_bug_workflow.py        • 4 Tests (Status, Release-Blocker)
│   └── test_sprint_logic.py        • 3 Tests (Story-Points, Burndown)
│
└── docs/                       ← Dokumentation auf Deutsch
    ├── TEST_CASE_VORLAGE.md        • Vorlage für einen Testfall (befüllt mit TC-1042)
    ├── IEC62304_PROZESS.md         • Erklärung der Norm IEC 62304
    └── SPRINT_GUIDE.md             • Wie ein 2-Wochen-Sprint abläuft
```

---

## Die fünf Ansichten der Anwendung

### 1. Übersicht & Pipeline
Vier Statistik-Karten oben: aktive Testfälle, Pass-Rate, offene Bugs, Sprint-Fortschritt. Darunter das **große End-to-End-Pipeline-Diagramm** mit 5 Schichten (Auslöser → Anforderung → Squish → Test-Ausführung mit Pass/Fail-Raute → Report → IEC-62304-Freigabe), Sprint-Fortschrittsleiste und Teamstruktur-Baum.

### 2. Test Case Manager
Filter nach Modul und Status, vier Testfall-Karten (TC-1042 Pass, TC-1118 Pass, TC-1203 Fail+Bug, TC-1255 WIP), Detail-Modal mit Schritten, Object-Map und Squish-Skript-Vorschau. Das Formular „+ Neuen Testfall anlegen" speichert wirklich in `data/test_cases.json`.

### 3. Squish Simulator
Testfall wählen, AUT-Modus (Attachable / Auto-Start), „▶ Test ausführen". Live-Konsole animiert die Schritte alle 350 ms — TC-1042 → PASS, TC-1203 → FAIL mit automatischem Bug **BUG-887**. Daneben: Squish-Skript-Vorschau, Vergleich manuell ↔ automatisch (~96 % Zeitersparnis), Trend-Chart der letzten 10 CI-Läufe.

### 4. Bug Tracking (Jira)
Kanban-Board mit fünf Spalten (OPEN, IN PROGRESS, IN REVIEW, IN TEST, CLOSED), 5 Demo-Bugs vorgeladen. Bug-Workflow-Diagramm in 6 Stufen, drei Statistik-Karten (Donut nach Schweregrad, Behebungs-Rate, Avg. Fix-Zeit), Bug-Report-Formular mit englischer Beschreibung — wie bei EXCO Standard.

### 5. Traceability & Sprint
**Requirements Traceability Matrix (RTM)** nach IEC 62304 §5.7.1 (User Need → System Req → Software Req → Architecture → Test Case → Status → Risk Class), IEC-62304-Lebenszyklus als Kreisdiagramm (Schritt 7 — System Testing — pulsiert), Sprint-14-Backlog mit Story-Points-Badges, Scrum-Ceremonies-Zeitlinie über 14 Tage.

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
- **Demo-Aufnahme:** **Playwright** (für Auto-Walkthrough)
- **Build-Tools:** keine (drei Befehle und es läuft)

---

## Doku im `docs/`-Ordner

- **`TEST_CASE_VORLAGE.md`** — Vorlage für einen Testfall, ausgefüllt mit TC-1042.
- **`IEC62304_PROZESS.md`** — Erklärung der Norm IEC 62304 (Klassen A/B/C, RTM, ISO 13485, ISO 14971).
- **`SPRINT_GUIDE.md`** — wie ein 2-Wochen-Sprint im Team IT Solutions abläuft.

---

## Lizenz

MIT — Anas Haj Naeif, 2026.
