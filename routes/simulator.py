from fastapi import APIRouter, HTTPException

from routes.storage import load, save

router = APIRouter(prefix="/api/sprint", tags=["sprint"])


# Status values our sprint board accepts (matches the kanban columns).
ALLOWED_STORY_STATUS = {"TODO", "IN_PROGRESS", "DONE"}


# Return the whole sprint object — number, dates, story-points-totals,
# and the list of stories with their current column.
@router.get("")
def get_sprint():
    return load("sprint.json")


# Move a story between the three sprint columns. We re-compute the
# story-points-done counter so the burndown stays in sync.
@router.put("/story/{story_id}")
def update_story(story_id: str, payload: dict):
    new_status = payload.get("status")
    if new_status not in ALLOWED_STORY_STATUS:
        raise HTTPException(status_code=400, detail="Unbekannter Story-Status")

    sprint = load("sprint.json")
    found = False
    for s in sprint["stories"]:
        if s["id"] == story_id:
            s["status"] = new_status
            found = True
            break

    if not found:
        raise HTTPException(status_code=404, detail="Story nicht gefunden")

    # Re-tally the points that are sitting in the DONE column — the burndown
    # chart on Seite 5 reads this number directly.
    sprint["story_points_done"] = sum(
        s["story_points"] for s in sprint["stories"] if s["status"] == "DONE"
    )
    save("sprint.json", sprint)
    return sprint
