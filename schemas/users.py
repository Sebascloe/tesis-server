from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str 
    email: str 
    phone: str 
    dni: str 
    distrito_id : int | None = None
    
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    dni: Optional[str] = None
    distrito_id: Optional[int] = None
    
class UserResponse(UserCreate):
    id: int