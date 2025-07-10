from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import SessionLocal, engine, Base
from model import User
import auth 
from schemeas import UserCreate, Userlogin

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db #return 
    finally:
        db.close()

@app.get("/health")
async def hello(name: str = "world"):
    return{"message" : f"Hello {name}"}

@app.get("/show")
def show(name: str = "world"):
    return{"message": f"hello{name}"}


@app.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = auth.hash_password(user.password)
    db_user = User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/login")
async def login(user: Userlogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not auth.verify_password(user.password,db_user.password):
        raise HTTPException(status_code=404, detail="user doesnt exist or wrong password")
    
    token = auth.jwt_generate({"email": db_user.email})
    return {"access_token": token, "token_type": "bearer"}


