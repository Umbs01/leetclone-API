from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..utils.security import hash_password 

from .db_models.user import User
from ..models import userModel

# Get user by student_id or email
def get_user(db: Session, student_id: str, email: str):
    return db.query(User).filter(or_(User.student_id == student_id, User.email == email)).first()

# Create user referencing the fastapi docs
def create_user(db: Session, user_model: userModel.CreateUserModel):
    hashed_password = hash_password(user_model.password)
    db_user = User(student_id = user_model.student_id
                   , username = user_model.username
                   , email = user_model.email
                   , password = hashed_password
                   , full_name = user_model.full_name
                   , solved_problems = user_model.solved_problems
                   , score = user_model.score
                   , role = user_model.role
                   )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# Get user by student_id
def get_user_by_student_id(db: Session, student_id: str):
    return db.query(User).filter(User.student_id == student_id).first()

