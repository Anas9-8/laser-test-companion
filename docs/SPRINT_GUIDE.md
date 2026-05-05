# Sprint-Guide — 2-Wochen-Sprints im Team IT Solutions

So läuft ein typischer Sprint bei uns. Der Guide ist absichtlich kurz
gehalten, damit ihn auch Neueinsteiger schnell durchlesen können.

## Rahmen

- Sprint-Länge: **2 Wochen** (10 Arbeitstage, 14 Kalendertage).
- Team-Setup: Junior + Senior Test-Automatisierung, Frontend, Backend, QA.
- Tools: Jira (Boards + Tickets), SVN (Code), Test Center (Reports).

## Sprint-Zyklus auf einen Blick

| Tag    | Was passiert                                  |
|--------|-----------------------------------------------|
| Tag 1  | Sprint Planning (vormittags, ~2 h)            |
| Täglich| Daily Stand-Up um 9:30 Uhr (15 Min)           |
| Tag 7  | Mid-Sprint Refinement (Backlog-Pflege)        |
| Tag 14 vormittags | Sprint Review (Demo)                |
| Tag 14 nachmittags | Sprint Retrospective              |

## Daily Stand-Up

Drei Fragen pro Person, ehrlich und kurz:

1. Was habe ich seit gestern erledigt?
2. Was nehme ich mir heute vor?
3. Wo bin ich blockiert?

Das Daily ist kein Status-Report fürs Management, sondern ein
Synchronisations-Termin fürs Team.

## Story-Point-Schätzung (Planning Poker)

Wir schätzen mit der Fibonacci-Skala: 1, 2, 3, 5, 8, 13, 21.

- **1 SP** — wenige Stunden, klar abgegrenzt (z.B. ein einfacher Klick-Test).
- **3 SP** — halber Tag, etwas Recherche nötig.
- **5 SP** — ein voller Tag, mehrere Schritte.
- **8 SP** — zwei Tage, mehrere Module beteiligt.
- **13 SP** — fast eine Woche, sollte besser geteilt werden.
- **21 SP** — zu groß, muss vor dem Sprint zerschnitten werden.

Faustregel: alles über 8 SP ist Warnsignal. Lieber in zwei Stories teilen.

## Definition of Done (DoD)

Ein Testfall gilt erst dann als **DONE**, wenn:

- Squish-Skript ins SVN eingecheckt ist.
- CI-Pipeline (Jenkins) den Test erfolgreich ausgeführt hat.
- JUnit-XML-Report im Test Center sichtbar ist.
- Pair-Review durchgeführt und im Jira-Ticket bestätigt wurde.
- RTM aktualisiert ist (REQ-ID ↔ TC-ID).
- Optional: Lauf am echten Gerät im Labor (bei Klasse-C-Anforderungen).

## Sprint Review

- Demo der fertigen Stories.
- Stakeholder (Produktmanagement, QA) sehen den realen Stand.
- Was nicht demonstriert werden kann, gilt als nicht fertig.

## Sprint Retrospective

Was lief gut, was lief schlecht, was wollen wir ändern?
Aus jeder Retro nehmen wir maximal **eine** konkrete Verbesserung mit in
den nächsten Sprint. Sonst überfrachten wir uns.

## Tipps für Junior-Test-Automatisierer

- Frag früh, nicht spät. Eine 5-Minuten-Frage spart oft 5 Stunden Suche.
- Pair-Programming mit dem Senior macht in den ersten Wochen mehr Sinn
  als alleine zu kämpfen.
- Halt deine Object Map sauber. Sprechende Namen sparen Wochen.
- Schau dir das Ergebnis im Labor an, wenn du kannst — die Realität ist
  manchmal anders als die Simulation.
