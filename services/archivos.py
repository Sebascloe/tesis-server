from sqlmodel import Session, select
from models.archivos import Archivos
from schemas.archivos import ArchivosCreate


def crear_archivo(session: Session, archivo_data: ArchivosCreate):
    archivo = Archivos(**archivo_data.model_dump(exclude={"id"}))
    session.add(archivo)
    session.commit()
    session.refresh(archivo)
    return archivo

def get_all_archivos(session: Session):
    archivos = session.exec(select(Archivos)).all()
    return archivos

def get_one_archivo(session: Session, archivo_id: int):
    archivo = session.get(Archivos, archivo_id)
    return archivo

# @app.patch('/heroes/{hero_id}', response_model=HeroPublic)
# def update_hero(hero_id: int, hero: HeroUpdate, session: session_dep):
#     hero_db = session.get(Hero, hero_id)
#     if not hero_db:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     hero_data = hero.model_dump(exclude_unset=True)
#     hero_db.sqlmodel_update(hero_data)
#     session.add(hero_db)
#     session.commit()
#     session.refresh(hero_db)
#     return hero_db

def update_one_archivo(session: Session, archivo: ArchivosCreate, archivo_id: int):
    archivo_db = session.get(Archivos, archivo_id)
    archivo_data = archivo.model_dump(exclude_unset=True)
    archivo_db.sqlmodel_update(archivo_data)
    session.add(archivo_db)
    session.commit()
    session.refresh(archivo_db)
    return archivo_db

def delete_one_archivo(session: Session, archivo_id: int):
    archivo = session.get(Archivos, archivo_id)
    session.delete(archivo)
    session.commit()
    return {"ok": True}
    

# @app.delete('/heroes/{hero_id}')
# def delete_hero(hero_id: int, session: session_dep):
#     hero = session.get(Hero,hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     session.delete(hero)
#     session.commit()
#     return {"ok": True}
    