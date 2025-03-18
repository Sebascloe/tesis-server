from fastapi import APIRouter, Depends
from sqlmodel import Session
from schemas.departamento import DepartamentoCreate, DepartamentoResponse
from database import get_session
from services.departamento import create_departamento, get_all_departamentos, get_one_departamento, update_one_departamento
from typing import List

router = APIRouter()


@router.post("/departamento", response_model=DepartamentoResponse)
def create_departamento_archivo_endpoint(departamento: DepartamentoCreate, session: Session = Depends(get_session)):
    return create_departamento(session, departamento)

@router.get("/departamento", response_model=List[DepartamentoResponse])
def get_departamentos_endpoint(session: Session = Depends(get_session)):
    return get_all_departamentos(session)

@router.get("/departamento/{departamento_id}", response_model=DepartamentoResponse)
def get_departamento_endpoint(departamento_id: int, session: Session = Depends(get_session)):
    return get_one_departamento(session, departamento_id)

@router.patch("/departamento/{departamento_id}", response_model=DepartamentoResponse)
def patch_departamento_endpoint(departamento_id: int, departamento: DepartamentoCreate, session: Session = Depends(get_session)):
    return update_one_departamento(session, departamento, departamento_id)