from pydantic import BaseModel

class ArchivosCreate(BaseModel):
    img_url: str 
    
class ArchivosResponse(ArchivosCreate):
    id: int