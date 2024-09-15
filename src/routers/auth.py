from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from ..database.db_models import user
from ..database import crud
from ..database.database import SessionLocal, engine
from ..models.userModel import UserModel, CreateUserModel

router = APIRouter(prefix="/auth", tags=["auth"], responses={404: {"description": "Not found"}})

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserModel)
async def register(user: CreateUserModel, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user.student_id, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Student already registered")
    return crud.create_user(db, user)

