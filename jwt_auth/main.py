from fastapi import FastAPI
from database import create_db_and_tables
from fastapi.responses import JSONResponse
from models import User


app = FastAPI()

@app.get("/")
def root():
    return {"route": "well"}


@app.post("/register")
def register(username, password, email):
    user = User.Adduser(username, password, email)
    return user
    


def create_db():
    return create_db_and_tables()

if __name__ == "__main__":
    create_db()