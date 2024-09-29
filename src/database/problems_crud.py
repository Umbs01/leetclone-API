from sqlalchemy.orm import Session

from .db_models.problems import Problems
from ..models import problemModel

# Create problem
def create_problem(db: Session, problem_model: problemModel.CreateProblemModel):
    db_problem = Problems(title = problem_model.title
                          , score = problem_model.points
                          , hint = problem_model.hint
                          , hint_cost = problem_model.hint_cost
                          , description = problem_model.description
                          , test_cases = problem_model.test_cases
                          , hidden_test_cases = problem_model.hidden_test_cases
                          , io_format = problem_model.io_format
                          , solution = problem_model.solution
                          , difficulty = problem_model.difficulty
                          , tags = problem_model.tags
                          , author = problem_model.author
                          , status = problem_model.status
                          , solves = problem_model.solves
                          , created_at = problem_model.created_at
                          )
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    
    return db_problem

# get all problems
def get_all_problems(db: Session):
    return db.query(Problems).all()

# get problem by title
def get_problem_by_title(db: Session, title: str):
    return db.query(Problems).filter(Problems.title == title).first()