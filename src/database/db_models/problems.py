from sqlalchemy import Column, Integer, String, PickleType, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..database import Base

class Problems(Base):
    __tablename__ = "problems"

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    points = Column(Integer, default=0, nullable=False)
    hint = Column(String)
    hint_cost = Column(Integer, default=0)
    description = Column(String, nullable=False)
    test_cases = Column(PickleType, default=[])
    hidden_test_cases = Column(PickleType, default=[])
    input_format = Column(String, default="")
    output_format = Column(String, default="")
    solution = Column(String, default="")
    difficulty = Column(String, nullable=False)
    tags = Column(PickleType, default=[])
    author = Column(String, ForeignKey("users.student_id"))
    status = Column(String, default="draft")
    solves = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)

    submissions = relationship("Submission", back_populates="prob")