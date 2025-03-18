from sqlmodel import SQLModel, Field, Column, Integer, ForeignKey

class Distrito(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    
    provincia_id: int = Field(default=None, sa_column=Column(Integer, ForeignKey("provincia.id")))