from pydantic import BaseModel

class ProvinciaCreate(BaseModel):
    nombre: str 
    departamento_id: int | None = None
    
class ProvinciaResponse(ProvinciaCreate):
    id: int