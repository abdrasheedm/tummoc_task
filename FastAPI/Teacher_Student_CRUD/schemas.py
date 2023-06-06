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

    class Config:
        orm_mode = True



class AddTeacher(BaseModel):
    teacher_id : int



class ViewStudentWithTeacher(BaseModel):
    name : str
    department : str
    teacher : Teacher

    class Config:
        orm_mode = True
