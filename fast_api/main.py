import auth 
import config
import jwt


from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError

from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import SessionLocal, engine, Base
from model import User
from schemeas import Userlogin


app = FastAPI()
Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def get_db():
    db = SessionLocal()
    try:
        yield db #return 
    finally:
        db.close()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        user = auth.decode_payload(token)
        if not user:
            raise HTTPException(status_code=404, detail="user doesnt exist or cant be found")
        return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="disabled user")





@app.get("/health")
async def hello(name: str = "world"):
    return{"message" : f"Hello {name}"}





@app.get("/show")
def show(name: str = "world"):
    return{"message": f"hello{name}"}





@app.post("/register")
async def register(user: Userlogin, db: Session = Depends(get_db)):
    hashed_password = auth.hash_password(user.password)
    db_user = User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user





@app.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]):

    db_user = db.query(User).filter(User.email == db_user.email)
    if not db_user or not auth.verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=404, detail="user doesnt exist or wrong password")
    
    token = auth.jwt_generate({"email": db_user.email})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/user")
async def read_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
