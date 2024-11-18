from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from ..utils.dependencies import get_db
from ..models.submission import SubmissionModel
from ..internal.submissions_crud import submit, get_submissions_by_user
from ..internal.users_crud import get_user_by_student_id


router = APIRouter(prefix="/submit", tags=["submit"], responses={404: {"description": "Not found"}})

@router.post("")
def submitproblem(submission: SubmissionModel, db = Depends(get_db)):
    try:
        get_user_by_student_id(db, submission.owner)
    except:
        raise HTTPException(status_code=404, detail="User not found")
#    try:
    return submit(db, submission)
#    except Exception as e:
#        return {"error": str(e)}

@router.get("/{user_id}")
def getsubmissions(user_id: str, db = Depends(get_db)):
    try:
        get_submissions_by_user(db, user_id)
    except:
        raise HTTPException(status_code=404, detail="User not found")
