from sqlmodel import SQLModel, Field

class Archivos(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    img_url: str = Field(index=True)