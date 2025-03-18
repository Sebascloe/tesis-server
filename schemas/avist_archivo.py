from pydantic import BaseModel

class Avist_ArchivoCreate(BaseModel):
    avist_id: int | None = None
    archivos_id: int | None = None
    
class Avist_ArchivoResponse(Avist_ArchivoCreate):
    id: int