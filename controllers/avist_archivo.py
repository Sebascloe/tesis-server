from fastapi import APIRouter, Depends
from schemas.avist_archivo import Avist_ArchivoCreate, Avist_ArchivoResponse
from sqlmodel import Session
from database import get_session
from services.avist_archivo import create_avist_archivo, get_avist_archivos, get_one_avist_archivos, update_one_avist_archivos
from typing import List

router = APIRouter()



@router.post("/avist_archivo", response_model=Avist_ArchivoResponse)
def create_avist_archivo_archivo_endpoint(avist_archivo: Avist_ArchivoCreate, session: Session = Depends(get_session)):
    return create_avist_archivo(session, avist_archivo)

# @app.get("/planta", response_model=List[Planta])
# def get_plantas(session:session_dep):
#     planta = session.exec(select(Planta)).all()
#     return planta

@router.get("/avist_archivo", response_model=List[Avist_ArchivoResponse])
def get_avist_archivo_endpoint(session: Session = Depends(get_session)):
    return get_avist_archivos(session)

@router.get("/avist_archivo/{avist_archivo_id}", response_model= Avist_ArchivoResponse)
def get_avist_Archivo_endpoint(avist_archivo_id: int, session: Session = Depends(get_session)):
    return get_one_avist_archivos(session, avist_archivo_id)

@router.patch("/avist_archivo/{avist_archivo_id}", response_model=Avist_ArchivoResponse)
def patch_avist_Archivo_endpoint(avist_archivo_id: int, avist_archivo: Avist_ArchivoCreate, session: Session = Depends(get_session)):
    return update_one_avist_archivos(session, avist_archivo, avist_archivo_id)