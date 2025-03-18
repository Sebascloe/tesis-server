from sqlmodel import Session, select
from models.noticias import Noticias
from schemas.noticias import NoticiasCreate, NoticiasUpdate


def crear_noticias(session: Session, noticia_data:NoticiasCreate):
    noticias = Noticias(**noticia_data.model_dump(exclude={"id"}))
    session.add(noticias)
    session.commit()
    session.refresh(noticias)
    return noticias

def get_all_noticias(session: Session):
    noticia = session.exec(select(Noticias)).all()
    return noticia

def get_one_noticia(session: Session, noticia_id: int):
    return session.get(Noticias, noticia_id)

def update_one_noticia(session: Session, noticia: NoticiasUpdate, noticia_id: int):
    db_noticia = session.get(Noticias, noticia_id)
    noticia_data = noticia.model_dump(exclude_unset=True)
    db_noticia.sqlmodel_update(noticia_data)
    session.add(db_noticia)
    session.commit()
    session.refresh(db_noticia)
    return db_noticia