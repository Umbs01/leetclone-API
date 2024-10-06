from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ProblemModel(BaseModel):
    title: str
    description: str
    difficulty: str
    points: int
    hint: str
    tags: list
    hint_cost: int
    test_cases: list
    input_format: str
    output_format: str
    author: str
    status: str
    solves: int

class CreateProblemModel(ProblemModel):
    hidden_test_cases: list
    solution: str

class SimpleProblemModel(BaseModel):
    id: UUID
    title: str
    difficulty: str
    points: int
    tags: list

class UpdateProblemModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    difficulty: Optional[str]
    points: Optional[int]
    hint: Optional[str]
    tags: Optional[list]
    hint_cost: Optional[int]
    test_cases: Optional[list]
    input_format: Optional[str]
    output_format: Optional[str]
    status: Optional[str]
    hidden_test_cases: Optional[list]
    solution: Optional[str]