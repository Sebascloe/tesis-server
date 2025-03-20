from fastapi import APIRouter, Depends
from schemas.provincia import ProvinciaCreate, ProvinciaResponse
from database import get_session
from sqlmodel import Session
from services.provincia import (
    create_provincia,
    get_all_provincias,
    get_one_provincia,
    update_one_provincia,
)
from typing import List

router = APIRouter()


@router.post("/provincia", response_model=ProvinciaResponse)
def create_provincia_archivo_endpoint(
    provincia: ProvinciaCreate, session: Session = Depends(get_session)
):
    return create_provincia(session, provincia)


@router.get("/provincia", response_model=List[ProvinciaResponse])
def get_provincias_endopoint(session: Session = Depends(get_session)):
    return get_all_provincias(session)


@router.get("/provincia/{provincia_id}", response_model=ProvinciaResponse)
def get_provincia_endpoint(provincia_id: int, session: Session = Depends(get_session)):
    return get_one_provincia(session, provincia_id)


@router.patch("/provincia/{provincia_id}", response_model=ProvinciaResponse)
def patch_provincia_endpoint(
    provincia_id: int,
    provincia: ProvinciaCreate,
    session: Session = Depends(get_session),
):
    return update_one_provincia(session, provincia, provincia_id)
