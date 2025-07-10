from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import SessionLocal, engine, Base
from model import User

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db #return 
    finally:
        db.close()



class UserCreate(BaseModel):
    email: EmailStr
    name: str
    age: int

@app.get("/health")
async def hello(name: str = "world"):
    return{"message" : f"Hello {name}"}

@app.get("/show")
def show(name: str = "world"):
    return{"message": f"hello{name}"}


@app.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(email=user.email, username=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


