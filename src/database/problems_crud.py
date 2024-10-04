from datetime import datetime
from sqlalchemy.orm import Session

from .db_models.problems import Problems
from ..models.problemModel import CreateProblemModel, UpdateProblemModel

# Create problem
def create_problem(db: Session, problem_model: CreateProblemModel):
    time_now = str(datetime.now())
    db_problem = Problems(title = problem_model.title
                          , points = problem_model.points
                          , hint = problem_model.hint
                          , hint_cost = problem_model.hint_cost
                          , description = problem_model.description
                          , test_cases = problem_model.test_cases
                          , hidden_test_cases = problem_model.hidden_test_cases
                          , input_format = problem_model.input_format
                          , output_format = problem_model.output_format
                          , solution = problem_model.solution
                          , difficulty = problem_model.difficulty
                          , tags = problem_model.tags
                          , author = problem_model.author
                          , status = problem_model.status
                          , solves = problem_model.solves
                          , created_at = time_now
                          , updated_at = time_now
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

# get problem by id
def get_problem_by_id(db: Session, id: str):
    return db.query(Problems).filter(Problems.id == id).first()