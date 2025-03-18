# from fastapi import FastAPI, Depends, HTTPException, Query
# from typing import Annotated
# from sqlmodel import create_engine, SQLModel, Session, Field, select

# url_conection = 'mysql+pymysql://root:root1234@localhost:3306/prueba'
# engine = create_engine(url_conection)

# def create_db_tables():
#     SQLModel.metadata.create_all(engine)
    
# def get_session():
#     with Session(engine) as session:
#         yield session
    
# session_dep = Annotated[Session, Depends(get_session)]

# # class HeroBase(SQLModel):
# #     name: str = Field(index=True)
# #     age: int | None = Field(default=None, index=True)

# # class Hero(HeroBase, table = True):
# #     id: int = Field(default=None, primary_key=True)
# #     secret_name: str

# # class HeroCreate(HeroBase):
# #     secret_name: str

# # class HeroPublic(HeroBase):
# #     id: int

# class Agent(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     alias: str = Field(index=True)

# app = FastAPI()

# @app.get('/')
# def user_get():
#     return {
#     'message' : "waza1"
#     } 
    
# @app.on_event('startup')
# def on_startup():
#     create_db_tables()
    
# # @app.post('/heroes', response_model=HeroPublic)
# # def create_hero(hero: HeroCreate, session:session_dep):
# #     db_hero = Hero.model_validate(hero)
# #     session.add(db_hero)
# #     session.commit()
# #     session.refresh(db_hero)
# #     return db_hero
    
# @app.post('/planta', response_model=Agent)
# def crear_planta(planta: Agent, session: session_dep):
#     try:
#         # db_plantas = Agent(**planta.model_dump(exclude_unset=True))
#         db_plantas = Agent(name= planta.name, alias = planta.alias)
#         session.add(db_plantas)
#         session.commit()
#         session.refresh(db_plantas)
#         return db_plantas.model_dump()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# @app.get('/plantas', response_model=list[Agent])
# def get_plantas(
#     session: session_dep,
#     offset: int=0, 
#     limit: Annotated[int, Query(le=100)] = 100):
#     planta = session.exec(select(Agent).offset(offset).limit(limit)).all()
#     return planta

# @app.get('/planta/{planta_id}', response_model=Agent)
# def get_planta(
#     session: session_dep,
#     planta_id: int
# ):
#     planta = session.get(Agent, planta_id)
#     if not planta:
#         raise HTTPException(status_code=404, detail="Plant not found")
#     return planta

from fastapi import FastAPI, Depends
from fastapi.concurrency import asynccontextmanager
from sqlmodel import Column, ForeignKey, Integer, SQLModel, create_engine, Session, Field, select, DECIMAL
from typing import Annotated, List
from decimal import Decimal

db_connection = "mysql+pymysql://root:root1234@localhost:3306/prueba"
engine = create_engine(db_connection)

def create_db_tables():
    SQLModel.metadata.create_all(engine)
    
def delete_db_tables():
    SQLModel.metadata.drop_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
        
session_dep = Annotated[Session, Depends(get_session)]
    
@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_tables()
    yield
    # delete_db_tables()



class Users(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True, nullable=False )
    name: str = Field(index=True)
    email: str = Field(index=True)
    phone: str = Field(index=True)
    dni: str = Field(index=True, max_length=8)
    
    distrito_id : int = Field(default=None, sa_column=Column(Integer, ForeignKey("distrito.id")))
    
class Avist(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    long: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10,2)))
    lati: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10,2)))
    
    user_id: int = Field(default=None, sa_column=Column(Integer, ForeignKey("users.id")))
    distrito_id : int = Field(default=None, sa_column=Column(Integer, ForeignKey("distrito.id")))
    
class Archivos(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    img_url: str = Field(index=True)
    
class Noticias(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str = Field(index=True)
    
    archivo_id: int = Field(default=None, sa_column=Column(Integer, ForeignKey("archivos.id")))
    
class Departamento(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)

class Provincia(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    
    departamento_id: int = Field(default=None, sa_column=Column(Integer, ForeignKey("departamento.id")))

class Distrito(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    
    provincia_id: int = Field(default=None, sa_column=Column(Integer, ForeignKey("provincia.id")))
    
class Avist_Archivo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    avist_id: int = Field(default=None, sa_column=Column(Integer, ForeignKey("avist.id")))
    archivos_id: int = Field(default=None, sa_column=Column(Integer, ForeignKey("archivos.id")))

app = FastAPI(lifespan=lifespan)

    
@app.post("/users", response_model=Users)
def create_users(session: session_dep, users:Users):
    db_users = Users(**users.model_dump(exclude={"id"}))
    session.add(db_users)
    session.commit()
    session.refresh(db_users)
    return db_users.model_dump()

@app.post("/avist", response_model=Avist)
def create_avist(session: session_dep, avist:Avist):
    db_asist = Avist(**avist.model_dump(exclude={"id"}))
    session.add(db_asist)
    session.commit()
    session.refresh(db_asist)
    return db_asist.model_dump()

@app.post("/archivos", response_model=Archivos)
def crear_archivo(session: session_dep, archivo: Archivos):
    db_archivos = Archivos(**archivo.model_dump(exclude={"id"}))
    session.add(db_archivos)
    session.commit()
    session.refresh(db_archivos)
    return db_archivos.model_dump()

@app.post("/noticias", response_model=Noticias)
def crear_noticias(session: session_dep, noticia:Noticias):
    db_noticias = Noticias(**noticia.model_dump(exclude={"id"}))
    session.add(db_noticias)
    session.commit()
    session.refresh(db_noticias)
    return db_noticias.model_dump()

@app.post("/departamento", response_model=Departamento)
def create_departamento(session: session_dep, departamento: Departamento):
    db_departamento = Departamento(**departamento.model_dump(exclude={"id"}))
    session.add(db_departamento)
    session.commit()
    session.refresh(db_departamento)
    return db_departamento.model_dump()

@app.post("/provincia", response_model=Provincia)
def create_provincia(session: session_dep, provincia:Provincia):
    db_provincia = Provincia(**provincia.model_dump(exclude={"id"}))
    session.add(db_provincia)
    session.commit()
    session.refresh(db_provincia)
    return db_provincia.model_dump()

@app.post("/distrito", response_model=Distrito)
def crete_distrito(session: session_dep, distrito:Distrito):
    db_distrito = Distrito(**distrito.model_dump(exclude={"id"}))
    session.add(db_distrito)
    session.commit()
    session.refresh(db_distrito)
    return db_distrito.model_dump()

@app.post("/avist_archivo", response_model=Avist_Archivo)
def create_avist_archivo(session: session_dep, avist_archivo: Avist_Archivo):
    db_avist_archivo = avist_archivo(**avist_archivo.model_dump(exclude={"id"}))
    session.add(db_avist_archivo)
    session.commit()
    session.refresh(db_avist_archivo)
    return db_avist_archivo

# @app.get("/planta", response_model=List[Planta])
# def get_plantas(session:session_dep):
#     planta = session.exec(select(Planta)).all()
#     return planta

# @app.get("/planta/{plantas_id}", response_model=Planta)
# def get_planta(session: session_dep, planta_id : int):
#     planta = session.get(Planta, planta_id)
#     return planta