from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..utils.dependencies import get_db
from ..internal.run_python import handle_run_code, combine_code 
from ..models.problems import ProblemSubmitModel
from ..internal.problems_crud import get_problem_by_id
from ..internal.grader import check_output, mutate_to_string

router = APIRouter(prefix="/run-code", tags=["run-code"], responses={404: {"description": "Not found"}})

@router.post("/{id}")
def run(problem_model: ProblemSubmitModel, id: str, db:Session=Depends(get_db)):
    # validate the test case
    try:
        problem = get_problem_by_id(db, id)
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

    if not problem:
        return JSONResponse(content={"error": "Problem not found"})
    
    if problem_model.test_cases != problem.test_cases:
        return JSONResponse(content={"error": "Invalid test case"})
    
    # combine template with the submitted code
    full_code = combine_code(problem.template, problem_model.code)
    
    test_cases = problem.test_cases + problem_model.additional_test_cases
    
    # run the code with or without test cases {input: '...', output: '...'}
    if len(test_cases) > 0: # type: ignore
        outputs = handle_run_code(full_code, test_cases) # type: ignore
    else:
        outputs = handle_run_code(full_code, [])

    # check if the output is correct
    test_cases = mutate_to_string(test_cases) # type: ignore
    results = check_output(outputs, test_cases) # type: ignore
    
    return JSONResponse(content={"results": results})
