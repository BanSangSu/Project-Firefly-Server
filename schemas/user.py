from pydantic import BaseModel, EmailStr
import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    subscription_level: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

# Model for API response (exclude sensitive information such as password hash)
class UserPublic(UserBase):
    id: int
    subscription_level: str
    created_at: datetime.datetime