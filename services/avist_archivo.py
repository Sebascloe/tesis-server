from sqlmodel import Session, select
from models.avist_archivo import Avist_Archivo
from schemas.avist_archivo import Avist_ArchivoCreate


def create_avist_archivo(session: Session, avist_archivo_data: Avist_ArchivoCreate):
    avist_archivo = Avist_Archivo(**avist_archivo_data.model_dump(exclude={"id"}))
    session.add(avist_archivo)
    session.commit()
    session.refresh(avist_archivo)
    return avist_archivo

# @app.get("/planta", response_model=List[Planta])
# def get_plantas(session:session_dep):
#     planta = session.exec(select(Planta)).all()
#     return planta

def get_avist_archivos(session: Session):
    avist_archivo = session.exec(select(Avist_Archivo)).all()
    return avist_archivo

def get_one_avist_archivos(session: Session, avist_archivo_id: int):
    return session.get(Avist_Archivo, avist_archivo_id)

def update_one_avist_archivos(session: Session, avist_archivo: Avist_ArchivoCreate, avist_archivo_id:int):
    db_avist_archivo = session.get(Avist_Archivo, avist_archivo_id)
    avist_archivo_data = avist_archivo.model_dump(exclude_unset=True)
    db_avist_archivo.sqlmodel_update(avist_archivo_data)
    session.add(db_avist_archivo)
    session.commit()
    session.refresh(db_avist_archivo)
    return db_avist_archivo