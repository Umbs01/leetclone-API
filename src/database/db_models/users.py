from sqlalchemy import Column, Integer, String, PickleType
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from sqlalchemy.orm import relationship

from ..database import Base

class User(Base):
    __tablename__ = "users"

    student_id = Column(String, unique=True, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    solved_problems = Column(MutableList.as_mutable(PickleType), default=[]) # type: ignore
    score = Column(Integer, default=0)
    role = Column(String, default="student")
    
    submissions = relationship("Submission", back_populates="own")