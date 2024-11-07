from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..utils.security import hash_password 
from fastapi import HTTPException
import re
from ..database.db_models.users import User
from ..models import users

# Get all users
def get_users(db: Session) -> list[User]:
    return db.query(User).all()

# Get user by student_id or email
def get_user(db: Session, student_id: str, email: str) -> User:
    return db.query(User).filter(or_(User.student_id == student_id, User.email == email)).first()

# Create user referencing the fastapi docs
def create_user(db: Session, user_model: users.CreateUserModel, role: str = "student") -> User:
    # validate the user input
    if user_model.email and len(user_model.email) > 128 or user_model.username and len(user_model.username) > 128 or user_model.password and len(user_model.password) > 128 or user_model.student_id and len(user_model.student_id) > 128:
          raise HTTPException(status_code=400, detail="Invalid input")
    if not re.match(r'^[0-9]+$', user_model.student_id):
        raise HTTPException(status_code=400, detail="student_id must be in numbers")
    if len(user_model.student_id) != 8:
        raise HTTPException(status_code=400, detail="student_id must be 8 digits")
    
    try: 
        user = users.CreateUserModel(
            student_id=user_model.student_id,
            username=user_model.username,
            email=user_model.email,
            password=user_model.password,
            solved_problems=[],
            score=0,
            role=role,
            hint_used=[]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    hashed_password = hash_password(user.password)
    db_user = User(student_id = user.student_id
                   , username = user.username
                   , email = user.email
                   , password = hashed_password
                   , solved_problems = user.solved_problems
                   , score = user.score
                   , role = user.role
                   )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# Get user by student_id
def get_user_by_student_id(db: Session, student_id: str) -> User:
    return db.query(User).filter(User.student_id == student_id).first()

