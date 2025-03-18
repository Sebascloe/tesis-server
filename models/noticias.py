from sqlmodel import SQLModel, Field, ForeignKey, Column, Integer

class Noticias(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str = Field(index=True)
    
    archivo_id: int = Field(default=None, sa_column=Column(Integer, ForeignKey("archivos.id")))