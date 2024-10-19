from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from ..utils.dependencies import get_db
from ..internal.run_python import run_code, read_output 
from ..models.problems import ProblemSubmitModel
from ..internal.problems_crud import get_problem_by_id

router = APIRouter(prefix="/run-code", tags=["run-code"], responses={404: {"description": "Not found"}})

@router.post("/{id}")
def run(problem: ProblemSubmitModel, id: str, db=Depends(get_db)):
    # validate the test case
    try:
        problem_db = get_problem_by_id(db, id)
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

    if not problem_db:
        return JSONResponse(content={"error": "Problem not found"})
    
    if problem.test_cases != problem_db.test_cases:
        return JSONResponse(content={"error": "Invalid test case"})
    
    # run the code
    run_code(problem.code)
    return JSONResponse(content={"output": read_output()})