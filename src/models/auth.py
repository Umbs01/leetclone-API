from pydantic import BaseModel, EmailStr

class LoginModel(BaseModel):
    email: EmailStr 
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

