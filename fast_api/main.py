import auth 
import config
import jwt

from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.database import SessionLocal, engine, Base
from auth.model import User
from schemas.schemeas import Userlogin
from task import tasks
from celery.result import AsyncResult

app = FastAPI()
Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        email = payload.get("email")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="disabled user")
    return current_user

@app.get("/health")
async def hello(name: str = "world"):
    return {"message": f"Hello {name}"}

@app.get("/show")
def show(name: str = "world"):
    return {"message": f"hello {name}"}

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
    db: Annotated[Session, Depends(get_db)]
):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if not db_user or not auth.verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    token = auth.jwt_generate({"email": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/user")
async def read_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@app.post("/task")
async def send(num1: int, num2: int):
    result = tasks.add.delay(num1, num2)
    return {"task_id": result.id}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    result = AsyncResult(task_id, app=tasks.celery_app)
    if result.state == 'PENDING':
        return {"status": "pending"}
    elif result.state == 'SUCCESS':
        return {"status": "success", "result": result.result}
    elif result.state == 'FAILURE':
        return {"status": "failure", "error": str(result.result)}
    else:
        return {"status": result.state}