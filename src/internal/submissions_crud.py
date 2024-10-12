from sqlalchemy.orm import Session
from datetime import datetime
from ..database.db_models import Submission
from ..models.submission import SubmissionModel
from .grader import isAccepted
from .problems_crud import get_problem_by_id
from .users_crud import get_user_by_student_id

def submit(db: Session, submission: SubmissionModel):
    time_now = datetime.now()
    owner = get_user_by_student_id(db, submission.owner)
    problem = get_problem_by_id(db, submission.problem_id)
    result = isAccepted(submission.code)
    
    if not owner:
        raise ValueError("User not found")
    if not problem:
        raise ValueError("Problem not found")

    db_submission = Submission(owner = submission.owner
                               , problem = submission.problem_id
                               , code = submission.code
                               , is_accepted = result
                               , created_at = time_now 
                               )
    db.add(db_submission)
    
    if result:
        owner.solved_problems.append({"problem_id": submission.problem_id, "difficulty": problem.difficulty})
        owner.score = owner.score + problem.points # type: ignore
        problem.solves = problem.solves + 1 # type: ignore

        db.add(owner)
        db.add(problem)
    
    db.commit()
    db.refresh(db_submission)
    
    return db_submission

def get_submissions_by_user(db: Session, user_id: str):
    return db.query(Submission).filter(Submission.owner == user_id).all()



