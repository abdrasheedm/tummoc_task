from pydantic import BaseModel
from typing import List


class Teacher(BaseModel):
    name : str
    subject : str


    class Config:
        orm_mode = True

class Student(BaseModel):
    name : str
    department : str
    teacher_id : Teacher


    class Config:
        orm_mode = True
