from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# Pass-szenario: TC-1042 muss im Simulator sauber durchlaufen
def test_tc_1042_pass_szenario():
    res = client.post("/api/run", json={"test_case_id": "TC-1042", "aut_mode": "attachable"})
    assert res.status_code == 200
    body = res.json()
    assert body["result"] == "PASS"
    assert body["test_case_id"] == "TC-1042"
    assert body["screenshot"] is None
    assert body["auto_bug"] is None


# Fail-szenario: Notabschaltung TC-1203 muss FAIL liefern und einen Bug auslösen
def test_tc_1203_fail_zeitueberschreitung():
    res = client.post("/api/run", json={"test_case_id": "TC-1203", "aut_mode": "attachable"})
    body = res.json()
    assert body["result"] == "FAIL"
    assert body["auto_bug"] == "BUG-887"
    assert body["screenshot"] is not None


# Attachable AUT muss explizit im Step-Log auftauchen
def test_aut_attachable_modus():
    res = client.post("/api/run", json={"test_case_id": "TC-1042", "aut_mode": "attachable"})
    texts = [s["text"] for s in res.json()["steps"]]
    assert any("Attachable AUT" in t for t in texts)


# JUnit-XML-Reportpfad muss im Antwort-Body unter "report_path" stehen
def test_report_xml_format():
    res = client.post("/api/run", json={"test_case_id": "TC-1118", "aut_mode": "attachable"})
    body = res.json()
    assert body["report_path"].startswith("reports/")
    assert body["report_path"].endswith(".xml")


# Bei einem Failure muss ein Screenshot-Pfad zurückgeliefert werden
def test_screenshot_bei_failure():
    res = client.post("/api/run", json={"test_case_id": "TC-1203"})
    body = res.json()
    assert body["screenshot"] is not None
    assert body["screenshot"].startswith("failures/")
    assert body["screenshot"].endswith(".png")
