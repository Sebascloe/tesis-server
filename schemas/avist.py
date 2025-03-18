from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class AvistCreate(BaseModel):
    long: Decimal 
    lati: Decimal 
    user_id: int | None = None
    distrito_id : int | None = None
    
class AvistUpdate(BaseModel):  
    long: Optional[Decimal] = None
    lati: Optional[Decimal] = None
    user_id: Optional[int] = None
    distrito_id: Optional[int] = None
    
class AvistResponse(AvistCreate):
    id: int 