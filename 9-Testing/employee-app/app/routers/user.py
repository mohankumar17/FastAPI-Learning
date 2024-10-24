from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, models, utils

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=201, response_model=schemas.UserResponse)
def create_user(requestBody: schemas.UserRequest, db: Session = Depends(get_db)):

    #Hash the password
    requestBody.user_password = utils.get_hash_pwd(requestBody.user_password)

    new_user = models.User(**requestBody.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/{userID}", response_model=schemas.UserResponse)
def fetch_user(userID: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == userID).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail=f"No user found with ID: {userID}")
    
    return user