from fastapi import APIRouter, Depends, status
from .. import schemas, oauth2, database
from sqlalchemy.orm import Session
from ..repository import students

router = APIRouter(
    tags=['Students'],
    prefix= '/student'
)
get_db = database.get_db


# STUDENTS CRUD

#VIEW ALL STUDENTS
@router.get('s/', response_model=list[schemas.Student], status_code=status.HTTP_200_OK)
def view_all_students(db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return students.get_all(db)


#VIEW SPECIFIC STUDENT
@router.get('/{id}', response_model=schemas.Student, status_code=status.HTTP_200_OK)
def view_student(id:int, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return students.view(id, db)


# ADD NEW STUDENT
@router.post('/', status_code=status.HTTP_201_CREATED)
def add_student(request: schemas.Student ,db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return students.add(request, db)


# UPDATE STUDENT
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_teacher(id:int, request: schemas.Student, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return students.update(id,request,db)


# DELETE STUDENT
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(id:int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return students.destroy(id, db)








# Assign Student To a Particular Teacher
@router.put('/assign-teacher/{id}', status_code=status.HTTP_202_ACCEPTED)
def assign_teacher(id:int , request:schemas.AddTeacher, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return students.assign_teacher(id, request, db)



#view Student with assigned Teacher
@router.get('/assigned-teacher/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ViewStudentWithTeacher)
def view_student_with_teacher(id:int , db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return students.view_with_teacher(id, db)

