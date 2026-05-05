from fastapi import APIRouter, HTTPException

from models.test_case import TestCase, TestCaseCreate
from routes.storage import load, save

router = APIRouter(prefix="/api/test-cases", tags=["test-cases"])


# Return every known test case so the Test-Case-Manager can render its grid.
@router.get("")
def list_test_cases():
    return load("test_cases.json")


# Look up a single test case by its id (e.g. TC-1042).
@router.get("/{tc_id}")
def get_test_case(tc_id: str):
    cases = load("test_cases.json")
    for c in cases:
        if c["id"] == tc_id:
            return c
    raise HTTPException(status_code=404, detail="Testfall nicht gefunden")


# Create a new test case from the "+ Neuen Testfall anlegen"-form.
# We auto-generate the next TC-id by looking at what we already have.
@router.post("", status_code=201)
def create_test_case(payload: TestCaseCreate):
    cases = load("test_cases.json")

    # Build a new TC-id by taking the largest existing number and adding one
    next_num = max((int(c["id"].split("-")[1]) for c in cases), default=1000) + 1
    new_id = f"TC-{next_num}"

    new_case = TestCase(
        id=new_id,
        title=payload.title,
        module=payload.module,
        status="in_arbeit",
        requirement_id=payload.requirement_id,
        squish_script=f"tst_{next_num}_{payload.title.lower().replace(' ', '_')[:20]}.py",
        steps=payload.steps,
        last_run_result="WIP",
    ).model_dump()

    cases.append(new_case)
    save("test_cases.json", cases)
    return new_case


# Update an existing test case (used after a run to write back pass/fail).
@router.put("/{tc_id}")
def update_test_case(tc_id: str, payload: dict):
    cases = load("test_cases.json")
    for c in cases:
        if c["id"] == tc_id:
            c.update(payload)
            save("test_cases.json", cases)
            return c
    raise HTTPException(status_code=404, detail="Testfall nicht gefunden")
