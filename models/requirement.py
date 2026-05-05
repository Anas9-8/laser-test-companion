from typing import Optional
from pydantic import BaseModel


# One row of the IEC 62304 traceability matrix (RTM)
class Requirement(BaseModel):
    id: str  # e.g. REQ-SAFETY-03
    title: str
    user_need: str  # USR-1 ...
    system_req: str  # SYS-3 ...
    architecture: str  # SafetyController ...
    risk_class: str  # A | B | C
    description: str
