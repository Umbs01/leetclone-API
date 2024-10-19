from pydantic import BaseModel

class SubmissionModel(BaseModel):
    problem_id: str
    code: str
    owner: str

