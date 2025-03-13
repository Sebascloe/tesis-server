from fastapi import FastAPI, Depends
from fastapi.concurrency import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, Field, func, select
from typing import Annotated, List

url_connection = "mysql+pymysql://root:root1234@192.168.38.77:3306/demo"
engine = create_engine(url_connection)

def create_db_tables():
    SQLModel.metadata.create_all(engine)

def mario_destroyer():
    SQLModel.metadata.drop_all(engine)

def session():
    with Session(engine) as session:
        yield session

session_dep = Annotated[Session, Depends(session)]

class Planta(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    password: str = Field(index=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    
    create_db_tables()
    yield
    # Clean up the ML models and release the resources
    mario_destroyer()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"msg":"waza"}


@app.get("/planta-get", response_model=List[Planta])
def get_plantas(session:session_dep):
    waza = session.exec(select(Planta)).all()
    return waza
@app.get("/planta/{planta_id}", response_model=Planta)
def get_planta(session: session_dep, planta_id:int):
    waza = session.get(Planta, planta_id)
    return waza

@app.post("/planta", response_model=Planta)
def create_planta(planta: Planta, session:session_dep):
    db_plantas = Planta(name=planta.name, password=planta.password)
    session.add(db_plantas)
    session.commit()
    session.refresh(db_plantas)
    return db_plantas.model_dump()
