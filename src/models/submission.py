from pydantic import BaseModel
from uuid import UUID

class SubmissionModel(BaseModel):
    problem_id: UUID
    code: str
    owner: str

