from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..internal.run_python import run_code, read_output 

router = APIRouter(prefix="/run-code", tags=["run-code"], responses={404: {"description": "Not found"}})

@router.post("/")
def run(text: str):
    run_code(text)
    return JSONResponse(content={"output": read_output()})