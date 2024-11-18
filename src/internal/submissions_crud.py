from sqlalchemy.orm import Session
from datetime import datetime
from ..database.db_models import Submission
from ..models.submission import SubmissionModel
from .run_python import handle_run_code
from .grader import isAccepted, check_output
from .problems_crud import get_problem_by_id
from .users_crud import get_user_by_student_id
from ..internal.run_python import combine_code

def submit(db: Session, submission: SubmissionModel):
    time_now = datetime.now()
    owner = get_user_by_student_id(db, submission.owner)
    problem = get_problem_by_id(db, str(submission.problem_id))

    # combine submitted code with template
    full_code = combine_code(problem.template, submission.code) # type: ignore
    # combine hidden test cases with test cases
    all_test_cases = problem.test_cases + problem.hidden_test_cases # type: ignore
    # run the code and grade it
    outputs = handle_run_code(full_code, all_test_cases) # type: ignore
    code_results = check_output(outputs, all_test_cases) # type: ignore
    result = isAccepted(code_results) # type: ignore
    
    # debug
    # print(f"Problem Template: {problem.template}, Submission Code: {submission.code}")
    # print(f"Test Cases: {problem.test_cases}, Hidden Test Cases: {problem.hidden_test_cases}")
    # print(f"All Test Cases: {all_test_cases}")
    # print(f"Outputs: {outputs}")

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

    # Check if user already solved this problem
    if any(solved_problem["problem_id"] == submission.problem_id for solved_problem in owner.solved_problems):
        raise ValueError("User already solved this problem")

    # If the submission is accepted, update the user's score and the problem's solves
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

