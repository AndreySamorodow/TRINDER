from pydantic import BaseModel, Field, field_validator

import re

class ProfileCreate(BaseModel):
    name: str = Field(...,min_length=2, max_length=15)
    city: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., gt=12)
    gender: str
    
    @field_validator('city')
    def validate_city(cls, v):
        v = v.strip().title()
        
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s\-]+$', v):
            raise ValueError('Название города содержит недопустимые символы')
        
        if len(v) < 2:
            raise ValueError('Название города слишком короткое')
            
        return v

class ProfileResponse(BaseModel):
    id: int
    name: str
    city: str
    age: int
    gender: str
    photo: str
    
    class Config:
        from_attributes = True


class ProfileResponseList(BaseModel):
    profiles: list[ProfileResponse]

class TelegramBindSchema(BaseModel):
    telegram_id: int
    code: str