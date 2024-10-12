from fastapi import APIRouter, Depends
from ..utils.dependencies import get_db
from ..internal.users_crud import get_users, get_user_by_student_id
from ..models.users import ResponseUserModel

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})

@router.get("", response_model=list[ResponseUserModel])
def get_all_users(db=Depends(get_db)):
    return get_users(db)

@router.get("/{student_id}", response_model=ResponseUserModel)
def get_user_by_id(student_id: str, db=Depends(get_db)):
    return get_user_by_student_id(db, student_id)

