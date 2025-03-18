from sqlmodel import Session, select
from models.avist import Avist
from schemas.avist import AvistCreate, AvistUpdate


def create_avist(session: Session, avist_data:AvistCreate):
    asist = Avist(**avist_data.model_dump(exclude={"id"}))
    session.add(asist)
    session.commit()
    session.refresh(asist)
    return asist

def get_all_avist(session: Session):
    avist = session.exec(select(Avist)).all()
    return avist

def get_one_avist(session: Session, avist_id: int):
    return session.get(Avist, avist_id)

def update_one_avist(session: Session, avist: AvistUpdate, avist_id: int):
    db_avist = session.get(Avist, avist_id)
    avist_data = avist.model_dump(exclude_unset=True)
    db_avist.sqlmodel_update(avist_data)
    session.add(db_avist)
    session.commit()
    session.refresh(db_avist)
    return db_avist