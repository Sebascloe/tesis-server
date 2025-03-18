from fastapi import APIRouter , Depends
from schemas.distrito import DistritoCreate, DistrtoResponse
from sqlmodel import Session
from database import get_session
from services.distrito import crete_distrito, get_all_distritos, get_one_distrito, update_one_distrito
from typing import List

router = APIRouter()

@router.post("/distrito", response_model=DistrtoResponse)
def crete_distrito_archivo_endpoint(distrito:DistritoCreate, session: Session = Depends(get_session)):
    return crete_distrito(session, distrito)

@router.get("/distrito", response_model=List[DistrtoResponse])
def get_distritos_endpoint(session: Session = Depends(get_session)):
    return get_all_distritos(session)

@router.get("/distrito/{distrito_id}", response_model=DistrtoResponse)
def get_distrito_endpoint(distrito_id: int, session: Session = Depends(get_session)):
    return get_one_distrito(session, distrito_id)

@router.patch("/distrito/{distrito_id}", response_model=DistrtoResponse)
def update_distrito_endpoint(distrito_id: int, distrito: DistritoCreate, session: Session = Depends(get_session)):
    return update_one_distrito(session, distrito, distrito_id)







