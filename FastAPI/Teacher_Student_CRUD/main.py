from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, models, JWT_Token, oauth2

from fastapi.security import OAuth2PasswordRequestForm

from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hash

import math



app = FastAPI()

models.Base.metadata.create_all(engine)

async def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# HELLO WORLD

@app.get('/', tags=['Hello world'])
def index():
    return "hello world"






# CRUD for Teachers

@app.get('/teachers', response_model=list[schemas.Teacher], tags=['Teachers'], status_code=status.HTTP_200_OK)
def view_all_teachers(db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    teachers = db.query(models.Teacher).all()
    if not teachers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data in Teacher table")
    return teachers

@app.get('/teachers/{id}', response_model=schemas.Teacher, tags=['Teachers'], status_code=status.HTTP_200_OK)
def view_teacher(id:int, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher with id {id} not found")
    return teacher


@app.post('/teachers', tags=['Teachers'], status_code=status.HTTP_201_CREATED)
def add_teacher(request: schemas.Teacher ,db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_teacher = models.Teacher(name=request.name, subject=request.subject)
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher


@app.put('/teachers/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Teachers'])
def update_teacher(id, request: schemas.Teacher, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id)

    if not teacher.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher with id {id} not found")

    teacher.update({"name": request.name, "subject" : request.subject})
    db.commit()
    return 'teacher updated'


@app.delete('/teachers/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Teachers'])
def delete_teacher(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id)
    if not teacher.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher with id {id} not found")
    teacher.delete(synchronize_session=False)
    db.commit()
    return 'Teacher deleted successfully'






# STUDENTS CRUD

@app.get('/students', response_model=list[schemas.Student], tags=['Students'], status_code=status.HTTP_200_OK)
def view_all_students(db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    students = db.query(models.Student).all()
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data in Student table")
    return students

@app.get('/students/{id}', response_model=schemas.Student, tags=['Students'], status_code=status.HTTP_200_OK)
def view_student(id:int, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")
    return student


@app.post('/students', tags=['Students'], status_code=status.HTTP_201_CREATED)
def add_student(request: schemas.Student ,db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_student = models.Student(name=request.name, department=request.department)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@app.put('/students/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Students'])
def update_teacher(id, request: schemas.Student, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    student = db.query(models.Student).filter(models.Student.id == id)

    if not student.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")

    student.update({"name": request.name, "department" : request.department})
    db.commit()
    return 'student updated'


@app.delete('/students/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Students'])
def delete_teacher(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    student = db.query(models.Student).filter(models.Student.id == id)
    if not student.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")
    student.delete(synchronize_session=False)
    db.commit()
    return 'Student deleted successfully'








# Assign Student To a Particular Teacher
@app.put('/student/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Assign Teacher'])
def assign_teacher(id:int , request:schemas.AddTeacher, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")
    student.update({"teacher_id": request.teacher_id})
    db.commit()
    return 'Teacher assigned'



#view Student with assigned Teacher
@app.get('/student/{id}', tags=['Assign Teacher'], status_code=status.HTTP_200_OK, response_model=schemas.ViewStudentWithTeacher)
def view_student_with_teacher(id:int , db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")
    if not student.teacher_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher not assigned for this Student")
    return student








#USER AND LOGIN

@app.post('/register', tags=['Authentication'], response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):

    if db.query(models.User).filter(models.User.email == request.email).first():
        raise HTTPException(detail=f"email {request.email} is already taken!. Please try with another one", status_code=status.HTTP_400_BAD_REQUEST)
    
    new_user = models.User(name = request.name, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@app.post('/login', tags=['Authentication'])
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentails")
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")
    
    # Generate JWT
    access_token = JWT_Token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# CALCULATE DISTANCE

@app.post("/distance")
def calculate_distance(request : schemas.Distance):
    # Calculate the distance between two points using the distance formula
    distance = math.sqrt((request.x1 - request.x2)**2 + (request.y1 - request.y2)**2)
    return {"distance": distance}

