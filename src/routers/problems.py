from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session  

from ..internal import problems_crud
from ..models.problems import ProblemModel, UpdateProblemModel, CreateProblemModel, SimpleProblemModel
from ..utils.dependencies import get_db

router = APIRouter(prefix="/problems", tags=["problems"], responses={404: {"description": "Not found"}})

@router.get("/", response_model=list[SimpleProblemModel])
def get_all_problems(db: Session = Depends(get_db)):
    return problems_crud.get_all_problems(db)

@router.get("/{id}", response_model=ProblemModel)
def get_problem_by_id(id: str, db: Session = Depends(get_db)):
    db_problem = problems_crud.get_problem_by_id(db, id)
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return db_problem

@router.post("/create", response_model=ProblemModel)
def create_problem(problem: CreateProblemModel, db: Session = Depends(get_db)):
    db_problem = problems_crud.get_problem_by_title(db, problem.title)
    if db_problem:
        raise HTTPException(status_code=400, detail="Problem already exists")
    
    try:
        problem = CreateProblemModel(
            title=problem.title,
            points=problem.points,
            hint=problem.hint,
            hint_cost=problem.hint_cost,
            description=problem.description,
            test_cases=problem.test_cases,
            hidden_test_cases=problem.hidden_test_cases,
            input_format=problem.input_format,
            output_format=problem.output_format,
            solution=problem.solution,
            difficulty=problem.difficulty,
            tags=problem.tags,
            author=problem.author,
            status=problem.status,
            solves=problem.solves
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return problems_crud.create_problem(db, problem)

@router.put("/update/{id}", response_model=UpdateProblemModel)
def update_problem(id: str, problem: UpdateProblemModel, db: Session = Depends(get_db)):
    db_problem = problems_crud.get_problem_by_title(db, id)
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    try:
        problem = UpdateProblemModel(
            title=problem.title,
            points=problem.points,
            hint=problem.hint,
            hint_cost=problem.hint_cost,
            description=problem.description,
            test_cases=problem.test_cases,
            hidden_test_cases=problem.hidden_test_cases,
            input_format=problem.input_format,
            output_format=problem.output_format,
            solution=problem.solution,
            difficulty=problem.difficulty,
            tags=problem.tags,
            status=problem.status,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return problems_crud.update_problem(db, id, problem)

@router.delete("/delete/{id}")
def delete_problem(id: str, db: Session = Depends(get_db)):
    db_problem = problems_crud.get_problem_by_title(db, id)
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    return problems_crud.delete_problem(db, id)