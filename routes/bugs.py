from datetime import date

from fastapi import APIRouter, HTTPException

from models.bug import BugCreate, BugStatusUpdate
from routes.storage import load, save

router = APIRouter(prefix="/api/bugs", tags=["bugs"])


# Allowed Jira-style status values — kept here in a constant so the kanban
# columns and the API stay in sync.
ALLOWED_STATUS = {"OPEN", "IN_PROGRESS", "IN_REVIEW", "IN_TEST", "CLOSED"}


# Return every bug so the kanban board can split them across the 5 columns.
@router.get("")
def list_bugs():
    return load("bugs.json")


# Create a new bug from the bug-report form. New bugs always start in OPEN.
@router.post("", status_code=201)
def create_bug(payload: BugCreate):
    bugs = load("bugs.json")

    # Generate the next BUG-id (one above the largest current number)
    next_num = max((int(b["id"].split("-")[1]) for b in bugs), default=800) + 1
    new_id = f"BUG-{next_num}"

    new_bug = {
        "id": new_id,
        "title": payload.title,
        "module": payload.module,
        "severity": payload.severity,
        "status": "OPEN",
        "reporter": "Anas Haj Naeif",
        "assignee": None,
        "linked_test": payload.linked_test,
        "linked_requirement": payload.linked_requirement,
        "description": payload.description,
        "steps_to_reproduce": payload.steps_to_reproduce,
        "expected": payload.expected,
        "actual": payload.actual,
        "component": None,
        "created_at": date.today().isoformat(),
    }
    bugs.append(new_bug)
    save("bugs.json", bugs)
    return new_bug


# Drag-and-drop or button click in the kanban triggers this — only the
# status field is updated, everything else stays untouched.
@router.put("/{bug_id}")
def update_status(bug_id: str, payload: BugStatusUpdate):
    if payload.status not in ALLOWED_STATUS:
        raise HTTPException(status_code=400, detail="Unbekannter Status")

    bugs = load("bugs.json")
    for b in bugs:
        if b["id"] == bug_id:
            b["status"] = payload.status
            save("bugs.json", bugs)
            return b
    raise HTTPException(status_code=404, detail="Bug nicht gefunden")
