from sqlmodel import create_engine, SQLModel, Session

db_connection = "mysql+pymysql://root:root1234@localhost:3306/fastapi"
engine = create_engine(db_connection)

def create_db_tables():
    SQLModel.metadata.create_all(engine)
    
def delete_db_tables():
    SQLModel.metadata.drop_all(engine)

def get_session():
    with Session(engine) as session:
        yield session