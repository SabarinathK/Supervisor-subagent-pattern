from typing import List
from pydantic import BaseModel

class PlanOutput(BaseModel):
    tasks: List[str]


class ReviewOutput(BaseModel):
    success: bool
    feedback: str
