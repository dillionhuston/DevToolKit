
from pydantic import BaseModel, EmailStr, StringConstraints




class Userlogin(BaseModel):
    email: EmailStr
    password: str



class Tasks(BaseModel):
    message: str
    