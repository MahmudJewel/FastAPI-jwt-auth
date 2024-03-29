from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    hashed_password: str
    class Config:
        orm_mode = True

class UserUpdate(UserCreate):
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str