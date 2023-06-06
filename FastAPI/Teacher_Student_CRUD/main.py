from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List



app = FastAPI()

models.Base.metadata.create_all(engine)

async def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# HELLO WORLD

@app.get('/')
def index():
    return "hello world"



# CRUD for Teachers

@app.get('/teachers', response_model=list[schemas.Teacher], tags=['Teachers'], status_code=status.HTTP_200_OK)
def view_all_teachers(db:Session = Depends(get_db)):
    teachers = db.query(models.Teacher).all()
    if not teachers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data in Teacher table")
    return teachers

@app.get('/teachers/{id}', response_model=schemas.Teacher, tags=['Teachers'], status_code=status.HTTP_200_OK)
def view_teacher(id:int, db:Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher with id {id} not found")
    return teacher


@app.post('/teachers', tags=['Teachers'], status_code=status.HTTP_201_CREATED)
def add_teacher(request: schemas.Teacher ,db: Session = Depends(get_db)):
    new_teacher = models.Teacher(name=request.name, subject=request.subject)
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher


@app.put('/teachers/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Teachers'])
def update_teacher(id, request: schemas.Teacher, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id)

    if not teacher.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher with id {id} not found")

    teacher.update({"name": request.name, "subject" : request.subject})
    db.commit()
    return 'teacher updated'


@app.delete('/teachers/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Teachers'])
def delete_teacher(id, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id)
    if not teacher.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher with id {id} not found")
    teacher.delete(synchronize_session=False)
    db.commit()
    return 'Teacher deleted successfully'


# STUDENTS CRUD

@app.get('/students', response_model=list[schemas.Student], tags=['Students'], status_code=status.HTTP_200_OK)
def view_all_students(db:Session = Depends(get_db)):
    students = db.query(models.Student).all()
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data in Student table")
    return students

@app.get('/students/{id}', response_model=schemas.Student, tags=['Students'], status_code=status.HTTP_200_OK)
def view_student(id:int, db:Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")
    return student


@app.post('/students', tags=['Students'], status_code=status.HTTP_201_CREATED)
def add_student(request: schemas.Student ,db: Session = Depends(get_db)):
    new_student = models.Student(name=request.name, department=request.department)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@app.put('/students/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Students'])
def update_teacher(id, request: schemas.Student, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id)

    if not student.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")

    student.update({"name": request.name, "department" : request.department})
    db.commit()
    return 'student updated'


@app.delete('/students/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Students'])
def delete_teacher(id, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id)
    if not student.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")
    student.delete(synchronize_session=False)
    db.commit()
    return 'Student deleted successfully'



# Assign Student To a Particular Teacher
@app.put('/students/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Students'])
def assign_teacher(id, request:schemas.Student, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id)
    if not student.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")
    student.update({"teacher_id": request.teacher_id})