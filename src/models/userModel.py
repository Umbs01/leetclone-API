from pydantic import BaseModel, EmailStr

class UserModel(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    student_id: str
    role: str = "student"

class CreateUserModel(UserModel):   
    solved_problems: list = []
    score: int = 0
    password: str

class ResponseUserModel(UserModel):
    session: str
    solved_problems: list
    score: int

