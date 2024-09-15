from pydantic import BaseModel

class BaseUserModel(BaseModel):
    username: str
    email: str
    full_name: str
    student_id: str

    class Config:
        orm_mode = True

class CreateUserModel(BaseUserModel):   
    password: str
    
    class Config:
        orm_mode = True

class UserModel(CreateUserModel):
    solved_problems: list = []
    score: int = 0