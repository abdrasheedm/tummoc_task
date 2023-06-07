from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, JWT_Token
from ..hashing import Hash



def register(request,db: Session):
    if db.query(models.User).filter(models.User.email == request.email).first():
        raise HTTPException(detail=f"email {request.email} is already taken!. Please try with another one", status_code=status.HTTP_400_BAD_REQUEST)
    
    new_user = models.User(name = request.name, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login(request,db:Session):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentails")
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")
    
    # Generate JWT
    access_token = JWT_Token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

