from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models



def get_all(db: Session):
    teachers = db.query(models.Teacher).all()
    if not teachers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data in Teacher table")
    return teachers


def view(db:Session):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher with id {id} not found")
    return teacher


def add(request, db:Session):
    new_teacher = models.Teacher(name=request.name, subject=request.subject)
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher

def update(request, db:Session):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id)

    if not teacher.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher with id {id} not found")

    teacher.update({"name": request.name, "subject" : request.subject})
    db.commit()
    return 'teacher updated'

def destroy(id:int, db : Session):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id)
    if not teacher.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher with id {id} not found")
    teacher.delete(synchronize_session=False)
    db.commit()
    return 'Teacher deleted successfully'