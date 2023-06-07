from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models



def get_all(db: Session):
    students = db.query(models.Student).all()
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data in Student table")
    return students


def view(id, db:Session):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")
    return student


def add(request, db:Session):
    new_student = models.Student(name=request.name, department=request.department)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


def update(id, request, db:Session):
    student = db.query(models.Student).filter(models.Student.id == id)

    if not student.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")

    student.update({"name": request.name, "department" : request.department})
    db.commit()
    return 'student updated'


def destroy(id, db):
    student = db.query(models.Student).filter(models.Student.id == id)
    if not student.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")
    student.delete(synchronize_session=False)
    db.commit()
    return 'Student deleted successfully'


def assign_teacher(id, request, db: Session):
    student = db.query(models.Student).filter(models.Student.id == id)
    if not student.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")
    teacher = db.query(models.Teacher).filter(models.Teacher.id == request.teacher_id)
    if not teacher.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher with id {request.teacher_id} not found")
    student.update({"teacher_id": request.teacher_id})
    db.commit()
    return 'Teacher assigned'


def view_with_teacher(id, db):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")
    if not student.teacher_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher not assigned for this Student")
    return student