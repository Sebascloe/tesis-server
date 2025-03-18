from fastapi import APIRouter, Depends
from schemas.avist import AvistCreate, AvistResponse, AvistUpdate
from sqlmodel import Session
from database import get_session
from services.avist import create_avist, get_all_avist, get_one_avist, update_one_avist
from typing import List

router = APIRouter()

@router.post("/avist", response_model=AvistResponse)
def create_avist_archivo_endpoint(avist:AvistCreate, session: Session = Depends(get_session)):

    return create_avist(session, avist)

@router.get("/avist", response_model=List[AvistResponse])
def get_avists_endpoint(session: Session = Depends(get_session)):
    return get_all_avist(session)

@router.get("/avist/{avist_id}", response_model=AvistResponse)
def get_avist_endpoint(avist_id: int, session: Session = Depends(get_session)):
    return get_one_avist(session, avist_id)

@router.patch("/avist/{avist_id}", response_model=AvistResponse)
def patch_avist_endpoint(avist_id: int, avist: AvistUpdate, session: Session = Depends(get_session)):
    return update_one_avist(session, avist, avist_id)