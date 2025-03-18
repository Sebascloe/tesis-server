from sqlmodel import Session, select
from models.distrito import Distrito
from schemas.distrito import DistritoCreate


def crete_distrito(session: Session, distrito_data:DistritoCreate):
    distrito = Distrito(**distrito_data.model_dump(exclude={"id"}))
    session.add(distrito)
    session.commit()
    session.refresh(distrito)
    return distrito

def get_all_distritos(session: Session):
    distrito = session.exec(select(Distrito)).all()
    return distrito

def get_one_distrito(session: Session, distrito_id: int):
    return session.get(Distrito, distrito_id)

def update_one_distrito(session: Session, distrito: DistritoCreate, distrito_id: int):
    db_distrito = session.get(Distrito, distrito_id)
    distrito_data = distrito.model_dump(exclude_unset=True)
    db_distrito.sqlmodel_update(distrito_data)
    session.add(db_distrito)
    session.commit()
    session.refresh(db_distrito)
    return db_distrito