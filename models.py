from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional

Base = declarative_base()

class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

class Tasks(Base):
    __tablename__ = "Tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)


class TodoCreate(BaseModel):
    title: str
    description: str

class TodoQuery(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
