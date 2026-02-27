from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=25)
    password_replay: str = Field(..., min_length=6, max_length=25)
    oauth: bool


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=25)
    oauth: bool

