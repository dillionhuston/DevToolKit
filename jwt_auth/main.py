from fastapi import FastAPI
from database import create_db_and_tables
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def root():
    return {"route": "well"}


def create_db():
    return create_db_and_tables()

if __name__ == "__main__":
    create_db()