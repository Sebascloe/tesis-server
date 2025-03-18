from pydantic import BaseModel

class DistritoCreate(BaseModel):
    nombre: str 
    provincia_id: int | None = None
    
class DistrtoResponse(DistritoCreate):
    id: int