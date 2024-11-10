from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from ..utils.dependencies import get_db
from ..internal.run_python import run_code, read_output 
from ..models.problems import ProblemSubmitModel
from ..internal.problems_crud import get_problem_by_id

router = APIRouter(prefix="/run-code", tags=["run-code"], responses={404: {"description": "Not found"}})

@router.post("/{id}")
def run(problem_model: ProblemSubmitModel, id: str, db=Depends(get_db)):
    # validate the test case
    try:
        problem = get_problem_by_id(db, id)
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

    if not problem:
        return JSONResponse(content={"error": "Problem not found"})
    
    if problem_model.test_cases != problem.test_cases:
        return JSONResponse(content={"error": "Invalid test case"})
    
    # run the code with or without test cases
    run_code(problem_model.code, *problem.test_cases) if problem.test_cases else run_code(problem_model.code)
    
    return JSONResponse(content={"output": read_output()})