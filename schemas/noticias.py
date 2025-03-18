from pydantic import BaseModel
from typing import Optional

class NoticiasCreate(BaseModel):
    title: str 
    content: str 
    archivo_id: int | None = None
    
class NoticiasUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    archivo_id: Optional[int] = None
    
class NoticiasResponse(NoticiasCreate):
    id: int