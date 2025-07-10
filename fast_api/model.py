from sqlalchemy import column, String, Integer
from database import Base

class User(Base):

    __tablename__ = "users"

    id = column(Integer, primary_key=True, index=True)
    email = column(String, unique=True, index=True)
    username = column(String)
    