
from pydantic import BaseModel, EmailStr, StringConstraints


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    age: int
    password: str


class Userlogin(BaseModel):
    email: EmailStr
    password: str



