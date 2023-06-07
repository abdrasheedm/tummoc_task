from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, oauth2, database, models, JWT_Token
from sqlalchemy.orm import Session
from ..repository import users
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(
    tags=['Authentication'],
)
get_db = database.get_db



#USER REGISTRATION

@router.post('/register', response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return users.register(request, db)


# USER LOGIN

@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return users.login(request, db)

