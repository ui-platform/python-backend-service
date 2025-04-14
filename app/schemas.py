from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    code: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class EmailVerificationRequest(BaseModel):
    email: EmailStr
    send_email: bool