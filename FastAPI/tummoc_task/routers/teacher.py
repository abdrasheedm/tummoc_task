from fastapi import APIRouter, Depends,status
from .. import schemas, oauth2, database
from sqlalchemy.orm import Session
from ..repository import teachers

router = APIRouter(
    tags=['Teachers'],
    prefix= '/teachers'
)
get_db = database.get_db

# VIEW ALL TEACHERS
@router.get('/', response_model=list[schemas.Teacher], status_code=status.HTTP_200_OK)
def view_all_teachers(db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return teachers.get_all(db)

# VIEW SINGLE TEACHER
@router.get('/{id}', response_model=schemas.Teacher, status_code=status.HTTP_200_OK)
def view_teacher(id:int, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return teachers.view(id, db)

# ADD NEW TEACHER
@router.post('/', status_code=status.HTTP_201_CREATED)
def add_teacher(request: schemas.Teacher ,db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return teachers.add(request, db)

# UPDATE A TEACHER
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_teacher(id, request: schemas.Teacher, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return teachers.update(id, request, db)

# DELETE A TEACHER
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return teachers.destroy(id, db)