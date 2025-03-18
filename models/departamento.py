from sqlmodel import SQLModel, Field

class Departamento(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)