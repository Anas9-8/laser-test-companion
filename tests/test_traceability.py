import csv
import io

from fastapi.testclient import TestClient

from main import app
from routes.storage import load

client = TestClient(app)


# Jeder Testfall braucht einen Verweis auf eine Anforderung
def test_jeder_testfall_hat_anforderung():
    cases = load("test_cases.json")
    reqs = {r["id"] for r in load("requirements.json")}
    for c in cases:
        assert c["requirement_id"] in reqs, f"{c['id']} verweist auf unbekannte Anforderung"


# IEC 62304 Klasse C Anforderungen müssen mindestens einen Test haben
def test_jede_klasse_c_anforderung_hat_test():
    reqs = load("requirements.json")
    cases = load("test_cases.json")
    class_c = [r for r in reqs if r["risk_class"] == "C"]
    for r in class_c:
        linked = [c for c in cases if c["requirement_id"] == r["id"]]
        assert linked, f"Klasse-C-Anforderung {r['id']} hat keinen Test"


# Es darf keine Anforderung geben die nirgendwo getestet wird
def test_keine_orphan_anforderungen():
    reqs = load("requirements.json")
    cases = load("test_cases.json")
    used = {c["requirement_id"] for c in cases}
    orphan = [r["id"] for r in reqs if r["id"] not in used]
    assert not orphan, f"Orphan-Anforderungen gefunden: {orphan}"


# Die Traceability-Antwort lässt sich als CSV exportieren
def test_matrix_export_csv():
    res = client.get("/api/traceability")
    rows = res.json()
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    csv_text = buf.getvalue()
    assert "user_need" in csv_text.splitlines()[0]
    assert len(csv_text.splitlines()) == len(rows) + 1
