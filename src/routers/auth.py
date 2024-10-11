from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session

from ..internal import users_crud
from ..models.users import UserModel, CreateUserModel
from ..models.auth import LoginModel, LoginResponseModel, RegisterModel
from ..utils.dependencies import get_db, authenticate_user, create_access_token


router = APIRouter(prefix="/auth", tags=["auth"], responses={404: {"description": "Not found"}})


@router.post("/register", response_model=UserModel)
def register(creds: RegisterModel, db: Session = Depends(get_db)):
    db_user = users_crud.get_user(db, creds.student_id, creds.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Student already registered")
    
    try: 
        user = CreateUserModel(
            student_id=creds.student_id,
            username=creds.username,
            email=creds.email,
            password=creds.password,
            solved_problems=[],
            score=0,
            role="student"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return users_crud.create_user(db, user)


@router.post("/login", response_model=LoginResponseModel)
def login(creds: LoginModel):
    user = authenticate_user(creds.email, creds.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    access_token = create_access_token(data={"sub": user.student_id, "role": user.role})
    return LoginResponseModel(token=access_token)     