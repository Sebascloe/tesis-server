from sqlmodel import Session, select
from models.departamento import Departamento
from schemas.departamento import DepartamentoCreate


def create_departamento(session: Session, departamento_data: DepartamentoCreate):
    departamento = Departamento(**departamento_data.model_dump(exclude={"id"}))
    session.add(departamento)
    session.commit()
    session.refresh(departamento)
    return departamento

def get_all_departamentos(session: Session):
    departamento = session.exec(select(Departamento)).all()
    return departamento

def get_one_departamento(session: Session, departamento_id: int):
    return session.get(Departamento, departamento_id)

def update_one_departamento(session: Session, departamento: DepartamentoCreate, departamento_id: int):
    db_departamento = session.get(Departamento, departamento_id)
    departamento_data = departamento.model_dump(exclude_unset=True)
    db_departamento.sqlmodel_update(departamento_data)
    session.add(db_departamento)
    session.commit()
    session.refresh(db_departamento)
    return db_departamento