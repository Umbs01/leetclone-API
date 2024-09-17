from sqlalchemy import Column, Integer, String, PickleType

from ..database import Base

class Problems(Base):
    __tablename__ = "problems"

    id = Column(Integer, unique=True, primary_key=True, index=True)
    title = Column(String)
    score = Column(Integer)
    hints = Column(PickleType, default=[])
    hint_cost = Column(Integer, default=0)
    description = Column(String)
    test_cases = Column(PickleType, default=[])
    hidden_test_cases = Column(PickleType, default=[])
    io_format = Column(String)
    solution = Column(String)
    difficulty = Column(String)
    tags = Column(PickleType, default=[])
    author = Column(String, reference="users.username")
    status = Column(String, default="draft")
    solves = Column(Integer, default=0)
    created_at = Column(String)