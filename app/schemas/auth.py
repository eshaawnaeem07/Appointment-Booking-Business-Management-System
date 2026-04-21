from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str
    confirm_password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime
    

    class Config:
        from_attributes = True
        
class otpRequest(BaseModel):
    email: EmailStr
    otp: str