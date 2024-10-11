from sqlalchemy import Column, String, UUID, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from uuid import uuid4

from ..database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4)
    owner = Column(String, ForeignKey("users.student_id"))
    problem = Column(UUID(as_uuid=True), ForeignKey("problems.id"))
    code = Column(String)
    is_accepted = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)

    own = relationship("User", back_populates="submissions")
    prob = relationship("Problems", back_populates="submissions")