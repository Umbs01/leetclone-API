from sqlalchemy.orm import Session
from ..database.db_models.users import User
from ..models.submission import SubmissionModel

def submit(db: Session, submission: SubmissionModel):
    pass
