from pydantic import BaseModel, Field


class PreferenceCreate(BaseModel):
    age: int = Field(..., gt=12)
    gender: str = Field(..., )

class PreferenceResponse(BaseModel):
    id: int
    age: int
    gender: str

    class Config:
        from_attributes = True