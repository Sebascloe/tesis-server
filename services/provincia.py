from sqlmodel import Session, select
from models.provincia import Provincia
from schemas.provincia import ProvinciaCreate

def create_provincia(session: Session, provincia_data:ProvinciaCreate):
    provincia = Provincia(**provincia_data.model_dump(exclude={"id"}))
    session.add(provincia)
    session.commit()
    session.refresh(provincia)
    return provincia

def get_all_provincias(session: Session):
    provincia = session.exec(select(Provincia)).all()
    return provincia

def get_one_provincia(session: Session, provincia_id: int):
    return session.get(Provincia, provincia_id)

def update_one_provincia(session: Session, provincia: ProvinciaCreate, provincia_id: int):
    db_provincia = session.get(Provincia, provincia_id)
    provincia_data = provincia.model_dump(exclude_unset=True)
    db_provincia.sqlmodel_update(provincia_data)
    session.add(db_provincia)
    session.commit()
    session.refresh(db_provincia)
    return db_provincia