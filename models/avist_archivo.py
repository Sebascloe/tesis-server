from sqlmodel import SQLModel, Field, Column, Integer, ForeignKey

class Avist_Archivo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    avist_id: int = Field(default=None, sa_column=Column(Integer, ForeignKey("avist.id")))
    archivos_id: int = Field(default=None, sa_column=Column(Integer, ForeignKey("archivos.id")))