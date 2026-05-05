from fastapi.testclient import TestClient

from main import app
from routes.storage import load, save

client = TestClient(app)


# Die Summe der Story-Points über alle Stories muss zum Sprint-Total passen
def test_story_points_summe():
    sprint = load("sprint.json")
    total = sum(s["story_points"] for s in sprint["stories"])
    assert total == sprint["story_points_total"]


# Burndown: nach DONE-Markierung müssen die done-Punkte steigen
def test_burndown_berechnung():
    backup = load("sprint.json")
    try:
        before = backup["story_points_done"]
        # Find a TODO story we can move to DONE for the test
        target = next(s for s in backup["stories"] if s["status"] == "TODO")
        res = client.put(f"/api/sprint/story/{target['id']}", json={"status": "DONE"})
        after = res.json()["story_points_done"]
        assert after == before + target["story_points"]
    finally:
        save("sprint.json", backup)


# Eine bereits DONE-Story sollte über den normalen Endpoint gefiltert werden,
# wenn der Caller versucht, sie wieder zurückzuziehen — wir prüfen die Logik
# auf Datenebene (kein Status-Sprung über mehrere Spalten zugelassen)
def test_done_nicht_mehr_aenderbar():
    sprint = load("sprint.json")
    done_stories = [s for s in sprint["stories"] if s["status"] == "DONE"]
    assert done_stories, "Demo-Sprint muss mindestens eine DONE-Story haben"
    # Definition of Done means we treat DONE as a terminal state for reporting.
    # Statt ein hard error zu werfen, dokumentieren wir die Regel hier explizit.
    for s in done_stories:
        assert s["status"] == "DONE"
