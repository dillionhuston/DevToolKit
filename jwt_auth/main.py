from fastapi import FastAPI, Request
from database import create_db_and_tables
from fastapi.responses import JSONResponse, HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from models import User

templates = Jinja2Templates(directory="templates")
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(name='index.html', request=Request)


@app.post("/register")
def register(username, password, email):
    user = User.Adduser(username, password, email)
    return user
    


def create_db():
    return create_db_and_tables()

if __name__ == "__main__":
    create_db()