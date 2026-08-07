from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.schemas.user_schema import (
    LoginResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from product.services import user_service


router = APIRouter(prefix="/users", tags=["Users"])  #API Entrypoint


@router.post("/register", response_model=UserResponse, status_code=201) #Create Operation
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db, user_data)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/login", response_model=LoginResponse)
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    try:
        return user_service.login_user(db, login_data)
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
