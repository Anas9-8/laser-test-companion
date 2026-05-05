from typing import Optional
from pydantic import BaseModel


# Bug ticket as we would store it in Jira — description stays in English
# because that is the documentation language at EXCO
class Bug(BaseModel):
    id: str
    title: str
    module: str
    severity: str  # Blocker | Critical | Major | Minor | Trivial
    status: str  # OPEN | IN_PROGRESS | IN_REVIEW | IN_TEST | CLOSED
    reporter: str
    assignee: Optional[str] = None
    linked_test: Optional[str] = None
    linked_requirement: Optional[str] = None
    description: str
    steps_to_reproduce: Optional[str] = None
    expected: Optional[str] = None
    actual: Optional[str] = None
    component: Optional[str] = None
    created_at: str


# Payload from the bug-report form on the Bug-Tracking page
class BugCreate(BaseModel):
    title: str
    module: str
    severity: str
    linked_test: Optional[str] = None
    linked_requirement: Optional[str] = None
    description: str
    steps_to_reproduce: Optional[str] = None
    expected: Optional[str] = None
    actual: Optional[str] = None


# Used when the kanban column changes (status update only)
class BugStatusUpdate(BaseModel):
    status: str
