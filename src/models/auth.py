from pydantic import BaseModel

class LoginModel(BaseModel):
    email: str
    password: str

class LoginResponseModel(BaseModel):
    token: str

class RegisterResponseModel(BaseModel):
    student_id: str
    username: str
    role: str

class RegisterModel(LoginModel):
    student_id: str
    username: str
    full_name: str

