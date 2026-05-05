# Testfall-Vorlage

So legen wir Testfälle bei EXCO im Team IT Solutions an. Die Vorlage ist
befüllt mit dem realen Testfall **TC-1042 — Patient anlegen mit gültigen Daten**,
damit man sieht, wie eine fertige Beschreibung aussieht.

---

## Kopfdaten

| Feld            | Wert                                              |
|-----------------|---------------------------------------------------|
| Test-ID         | TC-1042                                           |
| Titel           | Patient anlegen mit gültigen Daten                |
| Modul           | Surgeon UI                                        |
| Verlinkte Anforderung | REQ-SUI-12                                  |
| Risikoklasse    | B (nach IEC 62304)                                |
| Status          | Implementiert                                     |
| Autor           | Anas Haj Naeif                                    |
| Reviewer        | Sarah (Senior Dev)                                |
| Squish-Skript   | `tst_1042_patient_create.py`                      |

## Verlinkte Anforderung

**REQ-SUI-12** — "Das System muss einen neuen Patientendatensatz mit
Pflichtfeldern (Name, Geburtsdatum, Patient-ID, Augenseite) speichern und in
der Patientenliste anzeigen."

## Voraussetzungen

- AUT (LaserSystemUI.exe) ist gestartet und befindet sich auf dem Hauptbildschirm.
- Squish ist im Attachable-Modus konfiguriert (`squishserver` läuft auf Port 4322).
- Datenbank enthält keinen Patient mit der ID `P-2026-1042`.

## Testschritte

1. AUT starten und auf Hauptscreen warten.
2. Button "Neuer Patient" klicken.
3. Pflichtfelder ausfüllen:
   - Name: *Mustermann, Max*
   - Geburtsdatum: *01.01.1980*
   - Patient-ID: *P-2026-1042*
   - Augenseite: *OD (rechts)*
4. Schaltfläche "Speichern" klicken.
5. Verifizieren: Patient erscheint in der Patientenliste.

## Erwartetes Ergebnis

- Dialog "Neuer Patient" schließt sich nach dem Speichern.
- Patient ist in der Patientenliste sichtbar (Eintrag "Mustermann, Max").
- Keine Fehlermeldung im Log.

## Object-Map-Einträge

```
:MainWindow
:btnNewPatient
:nameField
:dobField
:patientIdField
:btnSave
:patientList_Mustermann
```

## Squish-Skript-Ausschnitt

```python
def main():
    startApplication("LaserSystemUI")
    waitForObject(":MainWindow")
    clickButton(waitForObject(":btnNewPatient"))
    type(waitForObject(":nameField"), "Mustermann, Max")
    type(waitForObject(":dobField"), "01.01.1980")
    type(waitForObject(":patientIdField"), "P-2026-1042")
    clickButton(waitForObject(":btnSave"))
    test.verify(object.exists(":patientList_Mustermann"))
```

## Reviewer-Checkliste

- [ ] Schritte sind eindeutig und vollständig.
- [ ] Erwartetes Ergebnis ist messbar.
- [ ] Object-Map-Namen sind sprechend (kein `Object_42`).
- [ ] Skript läuft im CI in unter 10 Sekunden.
- [ ] Verlinkte Anforderung existiert und ist aktiv.
