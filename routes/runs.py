from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from routes.storage import load

router = APIRouter(prefix="/api", tags=["runs"])


# Body of the POST /api/run request — frontend sends which test case to run
# and which AUT mode is active (attachable vs. auto-start).
class RunRequest(BaseModel):
    test_case_id: str
    aut_mode: str = "attachable"


# Build the live-step list the frontend animates. We don't actually launch
# squishrunner here — this is a faithful simulation for the demo.
def _build_steps(tc: dict, aut_mode: str) -> list:
    aut_label = "Attachable AUT" if aut_mode == "attachable" else "Auto-Start AUT"
    steps = [
        {"text": "squishserver gestartet auf Port 4322", "ok": True},
        {"text": f"Modus: {aut_label}", "ok": True},
        {"text": "Verbindung zu AUT...", "ok": True},
        {"text": "AUT erkannt: LaserSystemUI.exe (PID 4827)", "ok": True},
    ]
    # Add one step per Squish action. We map them to the test-case steps so
    # the user sees realistic-looking calls (waitForObject, clickButton, ...)
    for idx, descr in enumerate(tc["steps"], start=1):
        steps.append({"text": f"Schritt {idx}: {descr}", "ok": True})
    return steps


# Run a saved test case. The result depends on the test case's stored
# last_run_result so the demo always behaves the same way for the same TC.
@router.post("/run")
def run_test(req: RunRequest):
    cases = load("test_cases.json")
    tc = next((c for c in cases if c["id"] == req.test_case_id), None)
    if tc is None:
        raise HTTPException(status_code=404, detail="Testfall nicht gefunden")

    steps = _build_steps(tc, req.aut_mode)

    # The "FAIL" branch flips the last action red and adds the safety event
    if tc["last_run_result"] == "FAIL":
        steps[-1] = {
            "text": f"Schritt {len(tc['steps'])}: warte auf laserStopped Event...",
            "ok": False,
        }
        steps.append({"text": "Timeout nach 250 ms (erwartet ≤ 200 ms)", "ok": False})

    if tc["last_run_result"] == "WIP":
        # "In Arbeit" — we cut the run short to mimic an unfinished script
        steps = steps[:6]
        steps.append({"text": "Skript noch unvollständig — Implementierung läuft", "ok": False})

    pass_or_fail = tc["last_run_result"]
    duration = tc.get("last_run_seconds") or 0.0
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    report_path = f"reports/{tc['squish_script'].replace('.py','')}_{timestamp}.xml"

    # Auto-bug only triggers if the failure is the safety scenario
    auto_bug = "BUG-887" if tc["id"] == "TC-1203" else None

    return {
        "test_case_id": tc["id"],
        "title": tc["title"],
        "result": pass_or_fail,
        "duration_seconds": duration,
        "steps": steps,
        "report_path": report_path,
        "screenshot": f"failures/{tc['id']}_{timestamp}.png" if pass_or_fail == "FAIL" else None,
        "auto_bug": auto_bug,
    }


# Return the last 10 CI runs so the trend chart on the Squish page can
# render its bar graph.
@router.get("/runs/trend")
def runs_trend():
    return load("test_runs.json")
