from fastapi import APIRouter, Depends, HTTPException
from ..utils.dependencies import get_db, get_current_user
from ..internal.users_crud import get_users, get_user_by_student_id, create_user
from ..models.users import ResponseUserModel, CreateUserModel

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})

@router.get("", response_model=list[ResponseUserModel])
def get_all_users(db=Depends(get_db)):
    return get_users(db)

@router.get("/{student_id}", response_model=ResponseUserModel)
def get_user_by_id(student_id: str, db=Depends(get_db)):
    student_id = str(student_id)
    if len(student_id) != 8:
        raise HTTPException(status_code=400, detail="Invalid student id")
    try:
        get_user_by_student_id(db, student_id)
    except:
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/create-admin", response_model=ResponseUserModel) 
def create_admin(creds: CreateUserModel, token: str, db=Depends(get_db)):
    db_user = get_user_by_student_id(db, creds.student_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user = get_current_user(db, token)
    if user:
        if user.role == "admin": # type: ignore
            return create_user(db, creds, "admin")
        
    raise HTTPException(status_code=401, detail="Unauthorized")
    