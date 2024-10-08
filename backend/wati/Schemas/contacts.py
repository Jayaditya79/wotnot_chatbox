from pydantic import BaseModel 
from datetime import datetime

# Pydantic model
class ContactCreate(BaseModel):
    name: str
    email: str
    phone: str
    tags: list[str] = []

class ContactRead(ContactCreate):
    id: int
    created_at: datetime
    