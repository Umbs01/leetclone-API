from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..auth import hashed

from .db_models.user import User
from ..models import userModel

def get_user(db: Session, student_id: str, email: str):
    return db.query(User).filter(or_(User.student_id == student_id, User.email == email)).first()

def create_user(db: Session, user_model: userModel.CreateUserModel):
    hashed_password = hashed.hash_password(user_model.password)
    db_user = User(student_id=user_model.student_id, username=user_model.username, email=user_model.email, password=hashed_password, full_name=user_model.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

