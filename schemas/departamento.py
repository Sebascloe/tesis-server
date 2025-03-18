from pydantic import BaseModel

class DepartamentoCreate(BaseModel):
    nombre: str 
    
class DepartamentoResponse(DepartamentoCreate):
    id: int