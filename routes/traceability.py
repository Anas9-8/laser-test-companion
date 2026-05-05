from fastapi import APIRouter

from routes.storage import load

router = APIRouter(prefix="/api", tags=["traceability"])


# Return the raw requirements list — the frontend uses it for dropdowns
# in the bug-report form and for the IEC overview.
@router.get("/requirements")
def list_requirements():
    return load("requirements.json")


# Build the full RTM by joining requirements and test cases on the
# requirement_id. Each row contains everything a regulator wants to see.
@router.get("/traceability")
def traceability():
    reqs = load("requirements.json")
    cases = load("test_cases.json")

    rows = []
    for req in reqs:
        # Find the test case linked to this requirement (one-to-one for our
        # demo data — in real life there can be many).
        tc = next((c for c in cases if c["requirement_id"] == req["id"]), None)
        rows.append({
            "user_need": req["user_need"],
            "system_req": req["system_req"],
            "software_req": req["id"],
            "architecture": req["architecture"],
            "test_case": tc["id"] if tc else None,
            "status": tc["last_run_result"] if tc else "MISSING",
            "risk_class": req["risk_class"],
            "title": req["title"],
        })
    return rows


# Quick-and-dirty stats endpoint for the dashboard cards on Seite 1.
@router.get("/stats")
def stats():
    cases = load("test_cases.json")
    bugs = load("bugs.json")
    sprint = load("sprint.json")

    # Hard-coded totals to match the headline numbers from the project brief —
    # real numbers would come from a CI report aggregator. The kanban below
    # only shows a subset (5 demo bugs) to keep the UI readable.
    total_cases = 142
    passed = 118
    open_bugs = 7
    open_bugs_demo = sum(1 for b in bugs if b["status"] != "CLOSED")
    sprint_progress = round(100 * sprint["story_points_done"] / sprint["story_points_total"])

    return {
        "active_test_cases": total_cases,
        "passed": passed,
        "passed_label": f"{passed}/{total_cases}",
        "open_bugs": open_bugs,
        "open_bugs_demo": open_bugs_demo,
        "sprint_progress": sprint_progress,
        "sprint_number": sprint["number"],
        "sprint_day": sprint["current_day"],
        "sprint_total_days": sprint["total_days"],
        "live_demo_test_cases": len(cases),
    }
