import database as db
from model import User
from typing import Annotated, Union
from main import get_db
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
