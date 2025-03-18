from fastapi import APIRouter, Depends
from schemas.noticias import NoticiasCreate, NoticiasResponse, NoticiasUpdate
from sqlmodel import Session
from database import get_session
from services.noticias import crear_noticias, get_all_noticias, get_one_noticia, update_one_noticia
from typing import List

router = APIRouter()

@router.post("/noticias", response_model=NoticiasResponse)
def crear_noticias_archivo_endpoint(noticia:NoticiasCreate, session: Session = Depends(get_session)):
    return crear_noticias(session, noticia)

@router.get("/noticias", response_model=List[NoticiasResponse])
def get_noticias_endpoint(session: Session = Depends (get_session)):
    return get_all_noticias(session)

@router.get("/noticias/{noticia_id}", response_model=NoticiasResponse)
def get_noticia_endpoint(noticia_id: int, session: Session = Depends(get_session)):
    return get_one_noticia(session, noticia_id)

@router.patch("/noticias/{noticia_id}", response_model=NoticiasResponse)
def update_noticia_endpoint(noticia_id: int, noticia: NoticiasUpdate, session: Session = Depends(get_session)):
    return update_one_noticia(session, noticia, noticia_id)