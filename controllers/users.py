from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session
from schemas.users import UserCreate, UserResponse, UserUpdate
from services.users import create_user, get_all_users, get_one_user, update_one_user
from typing import List

router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create_users_archivo_endpoint(user:UserCreate,session: Session = Depends(get_session)):
    return create_user(session, user)

@router.get("/users", response_model=List[UserResponse])
def get_users_endpoint(session: Session = Depends(get_session)):
    return get_all_users(session)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, session: Session = Depends(get_session)):
    return get_one_user(session, user_id)

@router.patch("/Users/{user_ud}", response_model=UserResponse)
def patch_user_endpoint(user_id: int, user: UserUpdate, session: Session = Depends(get_session)):
    return update_one_user(session, user, user_id)