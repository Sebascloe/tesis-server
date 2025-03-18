from fastapi import APIRouter, Depends
from schemas.archivos import ArchivosCreate, ArchivosResponse
from sqlmodel import Session
from database import get_session
from services.archivos import crear_archivo, get_all_archivos, get_one_archivo, update_one_archivo, delete_one_archivo
from typing import List

router = APIRouter()


@router.post("/archivos", response_model=ArchivosResponse)
def crear_archivo_endpoint(archivo: ArchivosCreate, session: Session = Depends(get_session)):
    return crear_archivo(session, archivo)

@router.get("/archivos", response_model= List[ArchivosResponse])
def get_archivos(session: Session = Depends(get_session)):
    return get_all_archivos(session)

@router.get("/archivo/{archivo_id}", response_model=ArchivosResponse)
def get_archivo_endpoint( archivo_id: int, session: Session = Depends(get_session)):
    return get_one_archivo(session, archivo_id)

@router.patch("/archivo/{archivo_id}", response_model=ArchivosResponse)
def patch_archivo_endpoint(archivo_id: int, archivo: ArchivosCreate, session: Session = Depends(get_session)):
    return update_one_archivo(session, archivo, archivo_id)

@router.delete("/archivo/{archivo_id}", response_model=ArchivosResponse)
def delete_archivo_endpoint(archivo_id: int, session: Session = Depends(get_session)):
    return delete_one_archivo(session, archivo_id)