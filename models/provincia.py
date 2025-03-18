from sqlmodel import SQLModel, Field, Column, Integer, ForeignKey

class Provincia(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    
    departamento_id: int = Field(default=None, sa_column=Column(Integer, ForeignKey("departamento.id")))