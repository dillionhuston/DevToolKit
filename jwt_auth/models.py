from sqlmodel import Field, Session, SQLModel, create_engine
from typing import Optional
from datetime import datetime
from uuid import uuid4
import database


engine = database.engine

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    created_at: datetime = Field(default_factory=datetime.fromtimestamp)




    def Adduser(username, password, email)->str:
        new_user = User(username, password, email, id=uuid4())
        session = Session(engine)
        session.add(new_user)
        print("add new user")
        session.commit()
        session.close()
        return new_user