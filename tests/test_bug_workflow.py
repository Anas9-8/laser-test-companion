from fastapi.testclient import TestClient

from main import app
from routes.storage import load, save

client = TestClient(app)


# Ein neu angelegter Bug landet automatisch in der Spalte OPEN
def test_bug_anlegen_geht_in_open():
    backup = load("bugs.json")
    try:
        payload = {
            "title": "Demo Bug Workflow Test",
            "module": "Surgeon UI",
            "severity": "Minor",
            "description": "Demo only",
        }
        res = client.post("/api/bugs", json=payload)
        assert res.status_code == 201
        new_bug = res.json()
        assert new_bug["status"] == "OPEN"
        assert new_bug["id"].startswith("BUG-")
    finally:
        # Restore the original list so the test is idempotent
        save("bugs.json", backup)


# Status-Übergang: ein Bug kann von OPEN nach IN_PROGRESS verschoben werden
def test_bug_status_uebergang():
    backup = load("bugs.json")
    try:
        bug_id = backup[0]["id"]
        res = client.put(f"/api/bugs/{bug_id}", json={"status": "IN_REVIEW"})
        assert res.status_code == 200
        assert res.json()["status"] == "IN_REVIEW"
    finally:
        save("bugs.json", backup)


# BUG-887 muss mit dem fehlerhaften Testfall TC-1203 verknüpft sein
def test_bug_mit_testfall_verknuepft():
    bugs = load("bugs.json")
    bug_887 = next(b for b in bugs if b["id"] == "BUG-887")
    assert bug_887["linked_test"] == "TC-1203"
    assert bug_887["linked_requirement"] == "REQ-SAFETY-03"


# Ein offener Critical-Bug blockiert das Release — wir bilden das als Funktion ab
def test_critical_bug_blockiert_release():
    bugs = load("bugs.json")
    blocking = [b for b in bugs if b["severity"] == "Critical" and b["status"] != "CLOSED"]
    can_release = len(blocking) == 0
    # Aktuelles Demo-Setup: BUG-887 ist offen → Release blockiert
    assert can_release is False
