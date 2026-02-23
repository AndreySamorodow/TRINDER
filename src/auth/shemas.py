from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=25)
    password_replay: str = Field(..., min_length=6, max_length=25)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=25)

