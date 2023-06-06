from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class Teacher(Base):
    __tablename__ = 'Teachers'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    subject = Column(String)

    students = relationship("Teacher", back_populates='teacher')


class Student(Base):
    __tablename__ = 'Students'

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    department = Column(String)
    teacher_id = Column(Integer, ForeignKey("Teachers.id"))

    teacher = relationship("Teacher", back_populates="Students")



