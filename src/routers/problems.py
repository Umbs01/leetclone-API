from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session  

from ..database import problems_crud
from ..models.problemModel import ProblemModel, UpdateProblemModel, CreateProblemModel, SimpleProblemModel
from ..utils.dependencies import get_db

router = APIRouter(prefix="/problems", tags=["problems"], responses={404: {"description": "Not found"}})


@router.get("/all", response_model=list[SimpleProblemModel])
def get_all_problems(db: Session = Depends(get_db)):
    try:
        return problems_crud.get_all_problems(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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

@router.patch("/update/{id}", response_model=CreateProblemModel)
def update_problem(id: str, problem: UpdateProblemModel, db: Session = Depends(get_db)):
    db_problem = problems_crud.get_problem_by_title(db, id)
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    update_data = problem.dict(exclude_unset=True)
    try:
        for key, value in update_data.items():
            setattr(db_problem, key, value) 
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return problems_crud.update_problem(db, id, problem)