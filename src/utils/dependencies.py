from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.db_models.users import User
from ..config import get_settings
from ..internal.users_crud import get_user_by_student_id
from ..database.database import SessionLocal 
from ..utils.security import verify_password

from fastapi.security import OAuth2PasswordBearer

# get database session (usage: Depends(get_db))
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db = SessionLocal()

# get the settings
settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Login function () -> None | User
def authenticate_user(email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

# Create access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Users with the token is able to access the protected resources
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # raise an exception if the token is invalid
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        student_id: str = payload.get("sub")
        role: str = payload.get("role")

        if student_id is None or role is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception # error in decoding the token

    user = get_user_by_student_id(db, student_id)
    if user is None:
        raise credentials_exception
    return user
