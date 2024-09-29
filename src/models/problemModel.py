from pydantic import BaseModel

class ProblemModel(BaseModel):
    title: str
    description: str
    difficulty: str
    points: int
    hint: str
    tags: list
    hint_cost: int
    test_cases: list
    io_format: str
    author: str
    status: str
    solves: int

class CreateProblemModel(ProblemModel):
    hidden_test_cases: list
    solution: str
    created_at: str

class SimpleProblemModel(BaseModel):
    title: str
    difficulty: str
    points: int
    tags: list