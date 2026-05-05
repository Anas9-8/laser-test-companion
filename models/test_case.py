from typing import List, Optional
from pydantic import BaseModel


# Pydantic model for a single GUI test case targeting the Squish-driven AUT
class TestCase(BaseModel):
    id: str
    title: str
    module: str
    status: str  # implementiert | in_arbeit | failed | zu_reviewen
    requirement_id: str
    last_run_at: Optional[str] = None
    last_run_result: Optional[str] = None  # PASS | FAIL | WIP
    last_run_seconds: Optional[float] = None
    squish_script: str
    steps: List[str] = []
    object_map: List[str] = []
    linked_bug: Optional[str] = None


# Payload that the frontend posts when a tester adds a brand new test case
class TestCaseCreate(BaseModel):
    title: str
    module: str
    requirement_id: str
    steps: List[str] = []
