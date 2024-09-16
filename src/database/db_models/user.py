from sqlalchemy import Column, Integer, String, PickleType

from ..database import Base

class User(Base):
    __tablename__ = "users"

    student_id = Column(String, unique=True, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)
    solved_problems = Column(PickleType, default=[])
    score = Column(Integer, default=0)
    role = Column(String, default="student")


